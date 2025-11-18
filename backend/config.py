"""
Configuration settings for the Resume Analyzer application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Upload settings
# Use /tmp for serverless environments (Vercel, AWS Lambda, etc.)
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'doc'}

# Flask settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# CORS settings
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

# API settings
API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'

# Skill categories with expanded skills list
TECHNICAL_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'go', 
        'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab'
    ],
    'web_technologies': [
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 
        'fastapi', 'html', 'css', 'scss', 'sass', 'tailwind', 'bootstrap',
        'jquery', 'webpack', 'redux', 'next.js', 'nuxt.js'
    ],
    'databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 
        'dynamodb', 'oracle', 'sqlite', 'mariadb', 'elasticsearch'
    ],
    'cloud_devops': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
        'ansible', 'ci/cd', 'github actions', 'gitlab ci', 'circleci', 'linux',
        'unix', 'shell scripting', 'bash'
    ],
    'data_science_ai': [
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
        'nlp', 'spacy', 'nltk', 'machine learning', 'deep learning', 
        'computer vision', 'opencv', 'data analysis', 'data visualization',
        'matplotlib', 'seaborn', 'plotly', 'tableau', 'power bi'
    ],
    'tools_frameworks': [
        'git', 'github', 'gitlab', 'bitbucket', 'jira', 'agile', 'scrum',
        'rest api', 'graphql', 'microservices', 'testing', 'junit', 'pytest',
        'selenium', 'postman', 'swagger'
    ],
    'security_networking': [
        'networking', 'cybersecurity', 'penetration testing', 'scapy',
        'wireshark', 'nmap', 'oauth', 'jwt', 'ssl/tls', 'firewall'
    ]
}

# Flatten all skills for easier matching
ALL_SKILLS = []
for category, skills in TECHNICAL_SKILLS.items():
    ALL_SKILLS.extend(skills)

# ATS scoring weights
ATS_WEIGHTS = {
    'skill_match': 0.40,
    'keyword_density': 0.30,
    'content_similarity': 0.20,
    'format_quality': 0.10
}

# Minimum scores
MIN_SKILL_MATCH = 60
MIN_OVERALL_SCORE = 70

