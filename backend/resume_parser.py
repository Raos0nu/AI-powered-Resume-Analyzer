from PyPDF2 import PdfReader
import docx

def extract_text_from_file(path):
    lower_path = path.lower()
    if lower_path.endswith('.pdf'):
        reader = PdfReader(path)
        texts = []
        for p in reader.pages:
            t = p.extract_text()
            if t:
                texts.append(t)
        return "\n".join(texts)
    elif lower_path.endswith('.docx'):
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
