"""
Unit tests for matcher module.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import unittest
from matcher import (
    extract_skills,
    calculate_skill_match_score,
    calculate_content_similarity,
    analyze_resume_format,
    calculate_ats_score
)


class TestMatcher(unittest.TestCase):
    """Test cases for matcher functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_resume = """
        John Doe
        Software Engineer
        
        Experience:
        - Developed web applications using Python, Flask, and React
        - Implemented REST APIs and integrated with PostgreSQL database
        - Led team of 3 developers in agile environment
        
        Skills:
        Python, JavaScript, React, Flask, PostgreSQL, Docker, Git
        
        Education:
        B.S. in Computer Science
        """
        
        self.sample_jd = """
        We are looking for a skilled Software Engineer with experience in:
        - Python and Flask framework
        - React and JavaScript
        - PostgreSQL or MySQL
        - Docker and Kubernetes
        - Git version control
        
        Nice to have:
        - AWS or GCP experience
        - CI/CD pipelines
        """
    
    def test_extract_skills_basic(self):
        """Test basic skill extraction."""
        skills = extract_skills(self.sample_resume)
        
        self.assertIsInstance(skills, list)
        self.assertIn('python', skills)
        self.assertIn('flask', skills)
        self.assertIn('react', skills)
        self.assertGreater(len(skills), 0)
    
    def test_extract_skills_categorized(self):
        """Test categorized skill extraction."""
        categorized = extract_skills(self.sample_resume, categorize=True)
        
        self.assertIsInstance(categorized, dict)
        self.assertTrue(any('python' in skills for skills in categorized.values()))
    
    def test_extract_skills_empty_text(self):
        """Test skill extraction with empty text."""
        skills = extract_skills("")
        self.assertEqual(skills, [])
        
        categorized = extract_skills("", categorize=True)
        self.assertEqual(categorized, {})
    
    def test_calculate_skill_match_score(self):
        """Test skill match score calculation."""
        resume_skills = ['python', 'flask', 'react', 'postgresql', 'docker']
        jd_skills = ['python', 'flask', 'react', 'postgresql', 'docker', 'kubernetes']
        
        score = calculate_skill_match_score(resume_skills, jd_skills)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertAlmostEqual(score, 83.33, places=1)
    
    def test_calculate_skill_match_score_no_jd_skills(self):
        """Test skill match with no JD skills."""
        score = calculate_skill_match_score(['python'], [])
        self.assertEqual(score, 100.0)
    
    def test_calculate_skill_match_score_no_resume_skills(self):
        """Test skill match with no resume skills."""
        score = calculate_skill_match_score([], ['python', 'java'])
        self.assertEqual(score, 0.0)
    
    def test_calculate_content_similarity(self):
        """Test content similarity calculation."""
        similarity = calculate_content_similarity(self.sample_resume, self.sample_jd)
        
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 100)
    
    def test_calculate_content_similarity_empty(self):
        """Test content similarity with empty text."""
        similarity = calculate_content_similarity("", "some text")
        self.assertEqual(similarity, 0.0)
    
    def test_analyze_resume_format(self):
        """Test resume format analysis."""
        analysis = analyze_resume_format(self.sample_resume)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('score', analysis)
        self.assertIn('issues', analysis)
        self.assertIn('strengths', analysis)
        self.assertGreaterEqual(analysis['score'], 0)
        self.assertLessEqual(analysis['score'], 100)
    
    def test_analyze_resume_format_empty(self):
        """Test format analysis with empty resume."""
        analysis = analyze_resume_format("")
        
        self.assertEqual(analysis['score'], 0)
        self.assertIn('Empty resume', analysis['issues'])
    
    def test_calculate_ats_score(self):
        """Test comprehensive ATS score calculation."""
        result = calculate_ats_score(self.sample_resume, self.sample_jd)
        
        self.assertIsInstance(result, dict)
        self.assertIn('overall_score', result)
        self.assertIn('rating', result)
        self.assertIn('breakdown', result)
        self.assertIn('skills', result)
        self.assertIn('format_analysis', result)
        
        # Check score range
        self.assertGreaterEqual(result['overall_score'], 0)
        self.assertLessEqual(result['overall_score'], 100)
        
        # Check rating
        self.assertIn(result['rating'], ['Excellent', 'Good', 'Fair', 'Needs Improvement'])
        
        # Check skills
        self.assertIn('resume_skills', result['skills'])
        self.assertIn('jd_skills', result['skills'])
        self.assertIn('missing_skills', result['skills'])
        self.assertIn('matching_skills', result['skills'])


if __name__ == '__main__':
    unittest.main()

