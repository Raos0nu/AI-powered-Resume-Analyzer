"""
Advanced matching and skill extraction for resume analysis.
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import ALL_SKILLS, TECHNICAL_SKILLS, ATS_WEIGHTS
from utils import clean_text, calculate_keyword_density


def extract_skills(text, categorize=False):
    """
    Extract technical skills from text.
    
    Args:
        text (str): Text to extract skills from
        categorize (bool): If True, return skills categorized by type
        
    Returns:
        list or dict: List of skills found, or categorized dict if categorize=True
    """
    if not text:
        return {} if categorize else []
    
    cleaned_text = clean_text(text)
    
    if categorize:
        categorized_skills = {}
        for category, skills in TECHNICAL_SKILLS.items():
            found_skills = []
            for skill in skills:
                # More sophisticated matching
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, cleaned_text):
                    found_skills.append(skill)
            
            if found_skills:
                categorized_skills[category] = sorted(set(found_skills))
        
        return categorized_skills
    else:
        found_skills = []
        for skill in ALL_SKILLS:
            # Word boundary matching for better accuracy
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, cleaned_text):
                found_skills.append(skill)
        
        return sorted(set(found_skills))


def calculate_skill_match_score(resume_skills, jd_skills):
    """
    Calculate how well resume skills match job description skills.
    
    Args:
        resume_skills (list): Skills from resume
        jd_skills (list): Skills from job description
        
    Returns:
        float: Skill match score (0-100)
    """
    if not jd_skills:
        return 100.0  # No specific requirements
    
    if not resume_skills:
        return 0.0
    
    matching_skills = set(resume_skills) & set(jd_skills)
    score = (len(matching_skills) / len(jd_skills)) * 100
    
    return round(score, 2)


def calculate_content_similarity(resume_text, jd_text):
    """
    Calculate semantic similarity between resume and job description using TF-IDF.
    
    Args:
        resume_text (str): Resume text
        jd_text (str): Job description text
        
    Returns:
        float: Similarity score (0-100)
    """
    if not resume_text or not jd_text:
        return 0.0
    
    corpus = [resume_text, jd_text]
    
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams for better context
            max_features=1000
        )
        
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        if tfidf_matrix.shape[0] == 2:
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(float(similarity) * 100, 2)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
    
    return 0.0


def analyze_resume_format(resume_text):
    """
    Analyze resume format quality for ATS compatibility.
    
    Args:
        resume_text (str): Resume text
        
    Returns:
        dict: Format analysis results
    """
    analysis = {
        'score': 0,
        'issues': [],
        'strengths': []
    }
    
    if not resume_text:
        analysis['issues'].append("Empty resume")
        return analysis
    
    word_count = len(resume_text.split())
    line_count = len(resume_text.split('\n'))
    
    # Check word count (ideal: 400-800 words)
    if word_count < 300:
        analysis['issues'].append("Resume is too short. Add more details about your experience.")
        analysis['score'] += 10
    elif word_count > 1000:
        analysis['issues'].append("Resume is too long. Try to be more concise.")
        analysis['score'] += 15
    else:
        analysis['strengths'].append("Good resume length")
        analysis['score'] += 25
    
    # Check for sections
    sections = ['experience', 'education', 'skills', 'projects']
    found_sections = sum(1 for section in sections if section in resume_text.lower())
    
    if found_sections >= 3:
        analysis['strengths'].append("Well-structured with clear sections")
        analysis['score'] += 25
    else:
        analysis['issues'].append("Missing key sections (Experience, Education, Skills, Projects)")
        analysis['score'] += 10
    
    # Check for bullet points or lists
    if '•' in resume_text or '-' in resume_text or resume_text.count('\n') > 10:
        analysis['strengths'].append("Uses bullet points for readability")
        analysis['score'] += 25
    else:
        analysis['issues'].append("Consider using bullet points for better readability")
        analysis['score'] += 15
    
    # Check for action verbs
    action_verbs = ['developed', 'implemented', 'led', 'managed', 'created', 'designed', 
                    'optimized', 'improved', 'built', 'launched', 'achieved']
    found_verbs = sum(1 for verb in action_verbs if verb in resume_text.lower())
    
    if found_verbs >= 3:
        analysis['strengths'].append("Uses strong action verbs")
        analysis['score'] += 25
    else:
        analysis['issues'].append("Add more action verbs to describe achievements")
        analysis['score'] += 15
    
    analysis['score'] = min(analysis['score'], 100)
    
    return analysis


def calculate_ats_score(resume_text, jd_text):
    """
    Calculate comprehensive ATS (Applicant Tracking System) score.
    
    Args:
        resume_text (str): Resume text
        jd_text (str): Job description text
        
    Returns:
        dict: Detailed ATS scoring breakdown
    """
    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    missing_skills = [s for s in jd_skills if s not in resume_skills]
    
    # Calculate component scores
    skill_match_score = calculate_skill_match_score(resume_skills, jd_skills)
    content_similarity = calculate_content_similarity(resume_text, jd_text)
    format_analysis = analyze_resume_format(resume_text)
    keyword_density = calculate_keyword_density(resume_text, jd_skills)
    
    # Calculate weighted overall score
    overall_score = (
        skill_match_score * ATS_WEIGHTS['skill_match'] +
        content_similarity * ATS_WEIGHTS['content_similarity'] +
        format_analysis['score'] * ATS_WEIGHTS['format_quality'] +
        min(keyword_density * 10, 100) * ATS_WEIGHTS['keyword_density']
    )
    
    overall_score = round(overall_score, 2)
    
    # Determine rating
    if overall_score >= 80:
        rating = "Excellent"
    elif overall_score >= 70:
        rating = "Good"
    elif overall_score >= 60:
        rating = "Fair"
    else:
        rating = "Needs Improvement"
    
    return {
        'overall_score': overall_score,
        'rating': rating,
        'breakdown': {
            'skill_match': skill_match_score,
            'content_similarity': content_similarity,
            'format_quality': format_analysis['score'],
            'keyword_density': min(keyword_density * 10, 100)
        },
        'skills': {
            'resume_skills': resume_skills,
            'jd_skills': jd_skills,
            'missing_skills': missing_skills,
            'matching_skills': [s for s in resume_skills if s in jd_skills]
        },
        'format_analysis': format_analysis
    }


def match_resume_jd(resume_text, jd_text):
    """
    Main function to match resume against job description.
    Legacy function maintained for backward compatibility.
    
    Args:
        resume_text (str): Resume text
        jd_text (str): Job description text
        
    Returns:
        tuple: (score, details_dict)
    """
    ats_result = calculate_ats_score(resume_text, jd_text)
    
    details = {
        'resume_skills': ats_result['skills']['resume_skills'],
        'jd_skills': ats_result['skills']['jd_skills'],
        'missing_skills': ats_result['skills']['missing_skills'],
        'matching_skills': ats_result['skills']['matching_skills']
    }
    
    return ats_result['overall_score'], details
