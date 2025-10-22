// Configuration
const API_URL = 'http://localhost:5000/api/v1';

// DOM Elements
const analyzeForm = document.getElementById('analyzeForm');
const resumeFileInput = document.getElementById('resumeFile');
const fileLabel = document.querySelector('.file-upload-label');
const fileName = document.querySelector('.file-name');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const analyzeBtn = document.getElementById('analyzeBtn');

// File upload handling
resumeFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = file.name;
        fileLabel.style.borderColor = 'var(--primary)';
        fileLabel.style.background = 'rgba(102, 126, 234, 0.05)';
    }
});

// Drag and drop functionality
fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = 'var(--primary)';
    fileLabel.style.background = 'rgba(102, 126, 234, 0.1)';
});

fileLabel.addEventListener('dragleave', () => {
    fileLabel.style.borderColor = 'var(--border)';
    fileLabel.style.background = 'var(--bg-primary)';
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    
    if (file) {
        resumeFileInput.files = e.dataTransfer.files;
        fileName.textContent = file.name;
        fileLabel.style.borderColor = 'var(--primary)';
        fileLabel.style.background = 'rgba(102, 126, 234, 0.05)';
    }
});

// Form submission
analyzeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide error and results
    hideError();
    resultsSection.style.display = 'none';
    
    // Validate file
    const file = resumeFileInput.files[0];
    if (!file) {
        showError('Please select a resume file');
        return;
    }
    
    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showError('File size must be less than 5MB');
        return;
    }
    
    // Validate file type
    const validExtensions = ['pdf', 'docx', 'txt', 'doc'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!validExtensions.includes(fileExtension)) {
        showError('Invalid file type. Please upload PDF, DOCX, or TXT file');
        return;
    }
    
    // Show loading
    showLoading();
    
    // Prepare form data
    const formData = new FormData();
    formData.append('resume', file);
    
    const jobDescription = document.getElementById('jobDescription').value.trim();
    if (jobDescription) {
        formData.append('job_description', jobDescription);
    }
    
    try {
        // Make API call
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Analysis failed');
        }
        
        const data = await response.json();
        
        // Hide loading
        hideLoading();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        hideLoading();
        showError(error.message || 'An error occurred during analysis. Please try again.');
        console.error('Error:', error);
    }
});

// Show loading spinner
function showLoading() {
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div> Analyzing...';
    loadingSpinner.style.display = 'block';
    window.scrollTo({ top: loadingSpinner.offsetTop - 100, behavior: 'smooth' });
}

// Hide loading spinner
function hideLoading() {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8" stroke-width="2"/>
            <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        </svg>
        Analyze Resume
    `;
    loadingSpinner.style.display = 'none';
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    window.scrollTo({ top: errorMessage.offsetTop - 100, behavior: 'smooth' });
}

// Hide error message
function hideError() {
    errorMessage.style.display = 'none';
}

// Display results
function displayResults(data) {
    resultsSection.style.display = 'block';
    
    // Display resume info
    displayResumeInfo(data.resume_info);
    
    // Display skills
    displaySkills(data.skills);
    
    // Display ATS analysis if job description was provided
    if (data.ats_analysis) {
        displayATSScore(data.ats_analysis);
        displaySkillsMatch(data.ats_analysis.skills_match);
        displaySuggestions(data.ats_analysis.suggestions);
    } else {
        document.getElementById('atsScoreCard').style.display = 'none';
        document.getElementById('skillsMatchCard').style.display = 'none';
        document.getElementById('suggestionsCard').style.display = 'none';
    }
    
    // Scroll to results
    window.scrollTo({ top: resultsSection.offsetTop - 100, behavior: 'smooth' });
}

// Display ATS score
function displayATSScore(atsAnalysis) {
    const scoreCard = document.getElementById('atsScoreCard');
    scoreCard.style.display = 'block';
    
    const score = atsAnalysis.overall_score;
    const rating = atsAnalysis.rating;
    const breakdown = atsAnalysis.breakdown;
    
    // Animate score
    animateScore(score);
    
    // Update rating badge
    document.getElementById('ratingBadge').textContent = rating;
    
    // Update breakdown
    updateBreakdownBar('skillMatchScore', 'skillMatchBar', breakdown.skill_match);
    updateBreakdownBar('contentSimScore', 'contentSimBar', breakdown.content_similarity);
    updateBreakdownBar('formatScore', 'formatBar', breakdown.format_quality);
    updateBreakdownBar('keywordScore', 'keywordBar', breakdown.keyword_density);
}

// Animate score circle
function animateScore(score) {
    const scoreElement = document.getElementById('atsScore');
    const progressCircle = document.getElementById('progressCircle');
    const circumference = 2 * Math.PI * 90; // 90 is the radius
    
    // Animate number
    let currentScore = 0;
    const increment = score / 50; // 50 frames
    const scoreInterval = setInterval(() => {
        currentScore += increment;
        if (currentScore >= score) {
            currentScore = score;
            clearInterval(scoreInterval);
        }
        scoreElement.textContent = Math.round(currentScore);
    }, 20);
    
    // Animate circle
    const offset = circumference - (score / 100) * circumference;
    progressCircle.style.strokeDashoffset = offset;
}

// Update breakdown bar
function updateBreakdownBar(scoreId, barId, value) {
    document.getElementById(scoreId).textContent = `${value}%`;
    setTimeout(() => {
        document.getElementById(barId).style.width = `${value}%`;
    }, 100);
}

// Display skills match
function displaySkillsMatch(skillsMatch) {
    const skillsCard = document.getElementById('skillsMatchCard');
    skillsCard.style.display = 'block';
    
    // Update stats
    document.getElementById('matchingSkillsCount').textContent = skillsMatch.matching_skills.length;
    document.getElementById('missingSkillsCount').textContent = skillsMatch.missing_skills.length;
    document.getElementById('totalResumeSkills').textContent = 
        skillsMatch.matching_skills.length + skillsMatch.missing_skills.length;
    
    // Display matching skills
    const matchingList = document.getElementById('matchingSkillsList');
    matchingList.innerHTML = '';
    
    if (skillsMatch.matching_skills.length === 0) {
        matchingList.innerHTML = '<p style="color: var(--text-secondary);">No matching skills found</p>';
    } else {
        skillsMatch.matching_skills.forEach(skill => {
            const skillElement = document.createElement('div');
            skillElement.className = 'skill-item matching';
            skillElement.textContent = skill;
            matchingList.appendChild(skillElement);
        });
    }
    
    // Display missing skills
    const missingList = document.getElementById('missingSkillsList');
    missingList.innerHTML = '';
    
    if (skillsMatch.missing_skills.length === 0) {
        missingList.innerHTML = '<p style="color: var(--text-secondary);">No missing skills - Great job!</p>';
    } else {
        skillsMatch.missing_skills.forEach(skill => {
            const skillElement = document.createElement('div');
            skillElement.className = 'skill-item missing';
            skillElement.textContent = skill;
            missingList.appendChild(skillElement);
        });
    }
}

// Display all skills
function displaySkills(skills) {
    // Display categorized skills
    const categorizedSkillsDiv = document.getElementById('categorizedSkills');
    categorizedSkillsDiv.innerHTML = '';
    
    if (skills.categorized_skills && Object.keys(skills.categorized_skills).length > 0) {
        for (const [category, categorySkills] of Object.entries(skills.categorized_skills)) {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'skill-category';
            
            const title = document.createElement('div');
            title.className = 'category-title';
            title.textContent = category.replace(/_/g, ' ');
            
            const skillsDiv = document.createElement('div');
            skillsDiv.className = 'category-skills';
            
            categorySkills.forEach(skill => {
                const skillTag = document.createElement('span');
                skillTag.className = 'category-skill-tag';
                skillTag.textContent = skill;
                skillsDiv.appendChild(skillTag);
            });
            
            categoryDiv.appendChild(title);
            categoryDiv.appendChild(skillsDiv);
            categorizedSkillsDiv.appendChild(categoryDiv);
        }
    }
    
    // Display all skills as tags
    const allSkillsList = document.getElementById('allSkillsList');
    allSkillsList.innerHTML = '';
    
    if (skills.all_skills && skills.all_skills.length > 0) {
        skills.all_skills.forEach(skill => {
            const skillTag = document.createElement('span');
            skillTag.className = 'skill-tag';
            skillTag.textContent = skill;
            allSkillsList.appendChild(skillTag);
        });
    } else {
        allSkillsList.innerHTML = '<p style="color: var(--text-secondary);">No technical skills detected</p>';
    }
}

// Display suggestions
function displaySuggestions(suggestions) {
    const suggestionsCard = document.getElementById('suggestionsCard');
    
    if (!suggestions || suggestions.length === 0) {
        suggestionsCard.style.display = 'none';
        return;
    }
    
    suggestionsCard.style.display = 'block';
    
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    
    suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
}

// Display resume info
function displayResumeInfo(resumeInfo) {
    const resumeInfoDiv = document.getElementById('resumeInfo');
    resumeInfoDiv.innerHTML = '';
    
    // Filename
    addInfoItem(resumeInfoDiv, 'Filename', resumeInfo.filename);
    
    // Word count
    addInfoItem(resumeInfoDiv, 'Word Count', resumeInfo.word_count);
    
    // Email
    if (resumeInfo.emails && resumeInfo.emails.length > 0) {
        addInfoItem(resumeInfoDiv, 'Email', resumeInfo.emails[0]);
    }
    
    // Phone
    if (resumeInfo.phones && resumeInfo.phones.length > 0) {
        addInfoItem(resumeInfoDiv, 'Phone', resumeInfo.phones[0]);
    }
    
    // LinkedIn
    if (resumeInfo.urls && resumeInfo.urls.linkedin && resumeInfo.urls.linkedin.length > 0) {
        addInfoItem(resumeInfoDiv, 'LinkedIn', 
            `<a href="${resumeInfo.urls.linkedin[0]}" target="_blank" style="color: var(--primary);">View Profile</a>`);
    }
    
    // GitHub
    if (resumeInfo.urls && resumeInfo.urls.github && resumeInfo.urls.github.length > 0) {
        addInfoItem(resumeInfoDiv, 'GitHub', 
            `<a href="${resumeInfo.urls.github[0]}" target="_blank" style="color: var(--primary);">View Profile</a>`);
    }
}

// Helper function to add info item
function addInfoItem(container, label, value) {
    const div = document.createElement('div');
    div.className = 'info-item';
    
    const labelDiv = document.createElement('div');
    labelDiv.className = 'info-label';
    labelDiv.textContent = label;
    
    const valueDiv = document.createElement('div');
    valueDiv.className = 'info-value';
    valueDiv.innerHTML = value;
    
    div.appendChild(labelDiv);
    div.appendChild(valueDiv);
    container.appendChild(div);
}

// Check API health on load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) {
            console.warn('API health check failed');
        }
    } catch (error) {
        console.warn('Could not connect to API:', error);
        showError('Warning: Could not connect to the backend API. Please ensure the Flask server is running on http://localhost:5000');
    }
}

// Initialize
checkAPIHealth();

