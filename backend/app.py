"""
Flask application for AI-Powered Resume Analyzer.
Provides REST API endpoints for resume analysis and ATS scoring.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import logging
from datetime import datetime

from config import (
    UPLOAD_FOLDER, API_PREFIX, DEBUG, SECRET_KEY
)
from resume_parser import extract_text_from_file, extract_resume_metadata
from matcher import (
    extract_skills, calculate_ats_score, match_resume_jd
)
from utils import (
    allowed_file, validate_file_size, generate_suggestions,
    clean_text
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - API information."""
    return jsonify({
        'name': 'AI-Powered Resume Analyzer API',
        'version': '1.0.0',
        'description': 'Analyze resumes and match against job descriptions with AI-powered insights',
        'endpoints': {
            'POST /api/v1/analyze': 'Analyze resume and match with job description',
            'POST /api/v1/extract-skills': 'Extract skills from text',
            'GET /api/v1/health': 'Health check endpoint'
        },
        'status': 'active'
    })


@app.route(f'{API_PREFIX}/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Resume Analyzer API'
    })


@app.route(f'{API_PREFIX}/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze resume and optionally match against job description.
    
    Form Parameters:
        resume (file): Resume file (PDF, DOCX, or TXT)
        job_description (str, optional): Job description text
        
    Returns:
        JSON response with analysis results
    """
    try:
        # Validate file upload
        if 'resume' not in request.files:
            return jsonify({
                'error': 'No resume file provided',
                'message': 'Please upload a resume file (PDF, DOCX, or TXT)'
            }), 400
        
        resume_file = request.files['resume']
        
        if resume_file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select a file to upload'
            }), 400
        
        # Validate file type
        if not allowed_file(resume_file.filename):
            return jsonify({
                'error': 'Invalid file type',
                'message': 'Supported formats: PDF, DOCX, TXT'
            }), 400
        
        # Validate file size
        if not validate_file_size(resume_file):
            return jsonify({
                'error': 'File too large',
                'message': 'Maximum file size is 5MB'
            }), 400
        
        # Save file
        filename = f"{uuid.uuid4().hex}_{resume_file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(filepath)
        
        logger.info(f"File uploaded: {filename}")
        
        # Extract text from resume
        try:
            resume_text = extract_text_from_file(filepath)
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return jsonify({
                'error': 'Text extraction failed',
                'message': str(e)
            }), 500
        
        # Extract resume metadata
        metadata = extract_resume_metadata(resume_text)
        
        # Extract skills from resume
        resume_skills = extract_skills(resume_text)
        categorized_skills = extract_skills(resume_text, categorize=True)
        
        # Prepare response
        response = {
            'success': True,
            'resume_info': {
                'filename': resume_file.filename,
                'word_count': metadata['word_count'],
                'emails': metadata['emails'],
                'phones': metadata['phones'],
                'urls': metadata['urls']
            },
            'skills': {
                'all_skills': resume_skills,
                'categorized_skills': categorized_skills,
                'total_count': len(resume_skills)
            },
            'resume_preview': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text
        }
        
        # If job description provided, perform matching
        job_description = request.form.get('job_description', '').strip()
        
        if job_description:
            logger.info("Performing resume-JD matching")
            
            # Calculate ATS score
            ats_result = calculate_ats_score(resume_text, job_description)
            
            # Generate suggestions
            suggestions = generate_suggestions(
                ats_result['skills']['resume_skills'],
                ats_result['skills']['jd_skills'],
                ats_result['skills']['missing_skills'],
                ats_result['overall_score']
            )
            
            response['ats_analysis'] = {
                'overall_score': ats_result['overall_score'],
                'rating': ats_result['rating'],
                'breakdown': ats_result['breakdown'],
                'skills_match': {
                    'jd_skills': ats_result['skills']['jd_skills'],
                    'matching_skills': ats_result['skills']['matching_skills'],
                    'missing_skills': ats_result['skills']['missing_skills'],
                    'match_percentage': round(
                        (len(ats_result['skills']['matching_skills']) / 
                         len(ats_result['skills']['jd_skills']) * 100) 
                        if ats_result['skills']['jd_skills'] else 0, 2
                    )
                },
                'format_analysis': ats_result['format_analysis'],
                'suggestions': suggestions
            }
        
        # Clean up uploaded file (optional - comment out to keep files)
        # os.remove(filepath)
        
        logger.info("Analysis completed successfully")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Unexpected error in analyze_resume: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route(f'{API_PREFIX}/extract-skills', methods=['POST'])
def extract_skills_endpoint():
    """
    Extract skills from provided text.
    
    JSON Parameters:
        text (str): Text to extract skills from
        categorize (bool, optional): Whether to categorize skills
        
    Returns:
        JSON response with extracted skills
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided',
                'message': 'Please provide text in JSON body with key "text"'
            }), 400
        
        text = data.get('text', '')
        categorize = data.get('categorize', False)
        
        skills = extract_skills(text, categorize=categorize)
        
        return jsonify({
            'success': True,
            'skills': skills,
            'count': len(skills) if isinstance(skills, list) else sum(len(v) for v in skills.values())
        })
    
    except Exception as e:
        logger.error(f"Error in extract_skills_endpoint: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        'error': 'File too large',
        'message': 'Maximum file size is 5MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    logger.info("Starting Resume Analyzer API server")
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
