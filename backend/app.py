from flask import Flask, request, jsonify
import os, uuid
from resume_parser import extract_text_from_file
from matcher import extract_skills, match_resume_jd

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error":"Upload a 'resume' file (pdf/docx/txt)"}), 400
    f = request.files['resume']
    filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{f.filename}")
    f.save(filename)

    resume_text = extract_text_from_file(filename)
    job_description = request.form.get('job_description', '')

    skills = extract_skills(resume_text)
    result = {"skills": skills, "resume_text_snippet": resume_text[:1000]}

    if job_description.strip():
        score, details = match_resume_jd(resume_text, job_description)
        result["match_score"] = score
        result["details"] = details

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
