"""
Unit tests for utils module.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import unittest
from io import BytesIO
from werkzeug.datastructures import FileStorage
from utils import (
    allowed_file,
    clean_text,
    extract_email,
    extract_phone,
    extract_urls,
    calculate_keyword_density,
    generate_suggestions
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_allowed_file(self):
        """Test file extension validation."""
        self.assertTrue(allowed_file('resume.pdf'))
        self.assertTrue(allowed_file('resume.docx'))
        self.assertTrue(allowed_file('resume.txt'))
        self.assertTrue(allowed_file('RESUME.PDF'))  # Case insensitive
        
        self.assertFalse(allowed_file('resume.exe'))
        self.assertFalse(allowed_file('resume.jpg'))
        self.assertFalse(allowed_file('resume'))  # No extension
    
    def test_clean_text(self):
        """Test text cleaning."""
        dirty_text = "Hello    World!\n\nThis   is   a    test."
        clean = clean_text(dirty_text)
        
        self.assertEqual(clean, "hello world this is a test")
        self.assertNotIn('\n', clean)
        self.assertNotIn('  ', clean)
    
    def test_clean_text_empty(self):
        """Test cleaning empty text."""
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")
    
    def test_extract_email(self):
        """Test email extraction."""
        text = "Contact me at john.doe@example.com or jane@test.org"
        emails = extract_email(text)
        
        self.assertEqual(len(emails), 2)
        self.assertIn('john.doe@example.com', emails)
        self.assertIn('jane@test.org', emails)
    
    def test_extract_email_none(self):
        """Test email extraction with no emails."""
        text = "No emails here"
        emails = extract_email(text)
        
        self.assertEqual(len(emails), 0)
    
    def test_extract_phone(self):
        """Test phone number extraction."""
        text = "Call me at (123) 456-7890 or 987-654-3210"
        phones = extract_phone(text)
        
        self.assertGreater(len(phones), 0)
    
    def test_extract_urls(self):
        """Test URL extraction."""
        text = """
        LinkedIn: https://linkedin.com/in/johndoe
        GitHub: https://github.com/johndoe
        Portfolio: https://johndoe.com
        """
        urls = extract_urls(text)
        
        self.assertIsInstance(urls, dict)
        self.assertIn('linkedin', urls)
        self.assertIn('github', urls)
        self.assertEqual(len(urls['linkedin']), 1)
        self.assertEqual(len(urls['github']), 1)
    
    def test_calculate_keyword_density(self):
        """Test keyword density calculation."""
        text = "python java python javascript python"
        keywords = ['python', 'java']
        
        density = calculate_keyword_density(text, keywords)
        
        self.assertIsInstance(density, float)
        self.assertGreaterEqual(density, 0)
        self.assertLessEqual(density, 100)
    
    def test_calculate_keyword_density_empty(self):
        """Test keyword density with empty inputs."""
        self.assertEqual(calculate_keyword_density("", ['python']), 0.0)
        self.assertEqual(calculate_keyword_density("some text", []), 0.0)
    
    def test_generate_suggestions(self):
        """Test suggestion generation."""
        resume_skills = ['python', 'flask']
        jd_skills = ['python', 'flask', 'docker', 'kubernetes']
        missing_skills = ['docker', 'kubernetes']
        match_score = 65.0
        
        suggestions = generate_suggestions(
            resume_skills, jd_skills, missing_skills, match_score
        )
        
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)
        self.assertTrue(any('docker' in s.lower() or 'missing' in s.lower() 
                           for s in suggestions))
    
    def test_generate_suggestions_high_score(self):
        """Test suggestions with high match score."""
        suggestions = generate_suggestions(
            ['python', 'flask', 'docker'],
            ['python', 'flask', 'docker'],
            [],
            85.0
        )
        
        self.assertGreater(len(suggestions), 0)
        self.assertTrue(any('excellent' in s.lower() for s in suggestions))


if __name__ == '__main__':
    unittest.main()

