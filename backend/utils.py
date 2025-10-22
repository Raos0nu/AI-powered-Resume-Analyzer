"""
Utility functions for the Resume Analyzer application.
"""
import os
import re
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename (str): Name of the file
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file_size(file):
    """
    Validate that file size is within allowed limits.
    
    Args:
        file: FileStorage object from Flask
        
    Returns:
        bool: True if file size is valid, False otherwise
    """
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    return file_size <= MAX_FILE_SIZE


def clean_text(text):
    """
    Clean and normalize text for processing.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned and normalized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep important ones
    text = re.sub(r'[^\w\s\-\.\+\#]', ' ', text)
    
    # Normalize case
    text = text.lower()
    
    return text.strip()


def extract_email(text):
    """
    Extract email addresses from text.
    
    Args:
        text (str): Text to search for email
        
    Returns:
        list: List of email addresses found
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)


def extract_phone(text):
    """
    Extract phone numbers from text.
    
    Args:
        text (str): Text to search for phone numbers
        
    Returns:
        list: List of phone numbers found
    """
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    ]
    
    phones = []
    for pattern in phone_patterns:
        phones.extend(re.findall(pattern, text))
    
    return list(set(phones))


def extract_urls(text):
    """
    Extract URLs from text (LinkedIn, GitHub, Portfolio, etc.).
    
    Args:
        text (str): Text to search for URLs
        
    Returns:
        dict: Dictionary of URLs categorized by type
    """
    urls = {
        'linkedin': [],
        'github': [],
        'portfolio': [],
        'other': []
    }
    
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    found_urls = re.findall(url_pattern, text)
    
    for url in found_urls:
        if 'linkedin.com' in url.lower():
            urls['linkedin'].append(url)
        elif 'github.com' in url.lower():
            urls['github'].append(url)
        elif any(domain in url.lower() for domain in ['portfolio', 'personal', 'website']):
            urls['portfolio'].append(url)
        else:
            urls['other'].append(url)
    
    return urls


def calculate_keyword_density(text, keywords):
    """
    Calculate the density of keywords in text.
    
    Args:
        text (str): Text to analyze
        keywords (list): List of keywords to search for
        
    Returns:
        float: Keyword density percentage
    """
    if not text or not keywords:
        return 0.0
    
    text = clean_text(text)
    words = text.split()
    total_words = len(words)
    
    if total_words == 0:
        return 0.0
    
    keyword_count = sum(1 for word in words if word in [k.lower() for k in keywords])
    
    return round((keyword_count / total_words) * 100, 2)


def generate_suggestions(resume_skills, jd_skills, missing_skills, match_score):
    """
    Generate actionable suggestions for resume improvement.
    
    Args:
        resume_skills (list): Skills found in resume
        jd_skills (list): Skills found in job description
        missing_skills (list): Skills in JD but not in resume
        match_score (float): Overall match score
        
    Returns:
        list: List of suggestion strings
    """
    suggestions = []
    
    # Skills suggestions
    if missing_skills:
        if len(missing_skills) <= 3:
            suggestions.append(f"Add these critical skills: {', '.join(missing_skills)}")
        else:
            top_missing = missing_skills[:5]
            suggestions.append(f"Add these top missing skills: {', '.join(top_missing)}")
    
    # Match score suggestions
    if match_score < 50:
        suggestions.append("Low match score. Consider tailoring your resume more closely to the job description.")
    elif match_score < 70:
        suggestions.append("Good start! Add more relevant keywords from the job description to improve your score.")
    else:
        suggestions.append("Excellent match! Your resume is well-aligned with the job description.")
    
    # General suggestions
    if len(resume_skills) < 5:
        suggestions.append("Add more technical skills to demonstrate your expertise.")
    
    suggestions.append("Ensure your resume includes quantifiable achievements (e.g., 'improved performance by 30%').")
    suggestions.append("Use action verbs like 'developed', 'implemented', 'optimized', 'led', etc.")
    suggestions.append("Keep your resume to 1-2 pages for better readability.")
    
    return suggestions

