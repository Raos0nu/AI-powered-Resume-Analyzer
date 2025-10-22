# 🤝 Contributing to AI-Powered Resume Analyzer

First off, thank you for considering contributing to the AI-Powered Resume Analyzer! It's people like you that make this tool better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)

---

## Code of Conduct

This project and everyone participating in it is governed by a simple principle: **Be respectful and constructive**.

### Our Pledge

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:
- **Clear title** - Describe the issue briefly
- **Steps to reproduce** - Detailed steps to reproduce the behavior
- **Expected behavior** - What you expected to happen
- **Actual behavior** - What actually happened
- **Screenshots** - If applicable
- **Environment** - OS, Python version, browser (if frontend issue)
- **Error messages** - Full error logs or stack traces

**Bug Report Template:**
```markdown
## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Upload file '...'
4. See error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: Windows 10
- Python: 3.9.5
- Browser: Chrome 96

## Error Messages
```
[Paste error logs here]
```
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear title** - Describe the enhancement
- **Provide detailed description** - Explain why this would be useful
- **Include examples** - Show how it would work
- **Consider alternatives** - Mention other solutions you've considered

### 🔧 Code Contributions

1. **Fork the repository**
2. **Create a branch** - `git checkout -b feature/AmazingFeature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit** - `git commit -m 'Add some AmazingFeature'`
6. **Push** - `git push origin feature/AmazingFeature`
7. **Open a Pull Request**

---

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git
- Code editor (VS Code, PyCharm, etc.)

### Setup Steps

1. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-powered-Resume-Analyzer.git
   cd AI-powered-Resume-Analyzer
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/AI-powered-Resume-Analyzer.git
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate it
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

5. **Create a branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

6. **Make changes and test**
   ```bash
   # Run tests
   python -m unittest discover tests/
   
   # Start server for manual testing
   cd backend
   python app.py
   ```

---

## Coding Standards

### Python Code Style

We follow **PEP 8** - the Python Style Guide.

#### Key Points:
- **Indentation:** 4 spaces (no tabs)
- **Line length:** Max 88 characters (Black formatter standard)
- **Naming conventions:**
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Imports:** Grouped and sorted (standard library, third-party, local)
- **Docstrings:** Use Google or NumPy style

#### Example:

```python
"""
Module docstring explaining the purpose.
"""
import os
import sys

from flask import Flask, request
from sklearn.feature_extraction.text import TfidfVectorizer

from config import API_PREFIX
from utils import clean_text


def calculate_similarity(text1, text2):
    """
    Calculate similarity between two texts using TF-IDF.
    
    Args:
        text1 (str): First text to compare
        text2 (str): Second text to compare
        
    Returns:
        float: Similarity score between 0 and 100
        
    Raises:
        ValueError: If either text is empty
    """
    if not text1 or not text2:
        raise ValueError("Both texts must be non-empty")
    
    # Implementation here
    pass
```

### JavaScript Code Style

- **Indentation:** 2 spaces
- **Semicolons:** Use them
- **Quotes:** Single quotes for strings
- **Variables:** Use `const` and `let`, avoid `var`
- **Functions:** Arrow functions preferred for callbacks

#### Example:

```javascript
const analyzeResume = async (file, jobDescription) => {
  const formData = new FormData();
  formData.append('resume', file);
  
  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      body: formData
    });
    
    return await response.json();
  } catch (error) {
    console.error('Analysis failed:', error);
    throw error;
  }
};
```

### Documentation

- **All functions** must have docstrings
- **Complex logic** should have inline comments
- **API changes** must update docs/API.md
- **New features** should update README.md

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No linter errors

### PR Description Template

```markdown
## Description
[Clear description of changes]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## How Has This Been Tested?
[Describe testing process]

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally

## Screenshots (if applicable)
[Add screenshots]
```

### Review Process

1. **Automated checks** run (if configured)
2. **Maintainer reviews** code
3. **Changes requested** or **approved**
4. **Merge** after approval

---

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name files `test_*.py`
- Use descriptive test names
- Test both success and failure cases
- Aim for good coverage

#### Example Test:

```python
import unittest
from matcher import extract_skills

class TestSkillExtraction(unittest.TestCase):
    """Test cases for skill extraction."""
    
    def test_extract_skills_basic(self):
        """Test basic skill extraction from text."""
        text = "I know Python, JavaScript, and React"
        skills = extract_skills(text)
        
        self.assertIn('python', skills)
        self.assertIn('javascript', skills)
        self.assertIn('react', skills)
    
    def test_extract_skills_empty(self):
        """Test skill extraction with empty text."""
        skills = extract_skills("")
        self.assertEqual(skills, [])
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests/test_matcher.py

# Run with coverage (if installed)
coverage run -m unittest discover tests/
coverage report
```

---

## Project Structure

```
backend/
├── app.py              # Main Flask app
├── config.py           # Configuration
├── matcher.py          # Skill matching logic
├── resume_parser.py    # File parsing
└── utils.py            # Utility functions

frontend/
├── index.html          # Main HTML
├── styles.css          # Styling
└── script.js           # Frontend logic

tests/
├── test_matcher.py     # Matcher tests
└── test_utils.py       # Utils tests

docs/
├── API.md              # API documentation
└── QUICKSTART.md       # Quick start guide
```

---

## Areas for Contribution

### High Priority
- 🐛 Bug fixes
- 📝 Documentation improvements
- ✅ Test coverage increase
- 🎨 UI/UX enhancements

### Feature Ideas
- PDF resume generation
- Database integration
- User authentication
- Comparison feature
- Industry-specific analysis
- Cover letter analysis
- LinkedIn integration

### Technical Improvements
- Caching implementation
- Rate limiting
- Docker containerization
- CI/CD pipeline
- Cloud deployment
- Performance optimization

---

## Getting Help

- **Documentation:** Check README.md and docs/
- **Issues:** Search existing issues
- **Discussions:** Start a discussion on GitHub
- **Email:** your.email@example.com

---

## Recognition

Contributors will be:
- Listed in the README.md
- Credited in release notes
- Appreciated greatly! 🎉

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🚀**

Your efforts help make job searching easier for everyone!

