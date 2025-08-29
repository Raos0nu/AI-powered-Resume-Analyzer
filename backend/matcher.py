import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "python","java","c","c++","react","javascript","html","css","docker","jenkins",
    "gcp","aws","sql","mysql","postgresql","tensorflow","pytorch","nlp","spacy",
    "scikit-learn","git","ci/cd","linux","networking","scapy"
]

def normalize(text):
    return re.sub(r'\s+',' ', (text or "").lower())

def extract_skills(text):
    t = normalize(text)
    found = []
    for s in SKILLS:
        if s in t:
            found.append(s)
    return sorted(set(found))

def match_resume_jd(resume_text, jd_text):
    corpus = [resume_text or "", jd_text or ""]
    vect = TfidfVectorizer(stop_words='english').fit_transform(corpus)
    sim = 0.0
    if vect.shape[0] == 2:
        sim = cosine_similarity(vect[0:1], vect[1:2])[0][0]
    score = round(float(sim) * 100, 2)
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)
    missing_skills = [s for s in jd_skills if s not in resume_skills]
    details = {"resume_skills": resume_skills, "jd_skills": jd_skills, "missing_skills": missing_skills}
    return score, details
