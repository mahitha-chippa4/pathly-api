import io
import re
import pdfplumber

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text

def parse_resume(file_bytes: bytes, filename: str) -> str:
    filename = filename.lower()
    
    text = ""
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    else:
        # Fallback for txt or other unsupported right now
        try:
            text = file_bytes.decode("utf-8")
        except:
            text = str(file_bytes)
            
    # Basic cleaning
    text = re.sub(r'\s+', ' ', text).strip()
    
    # If text is empty (e.g. image-based PDF without OCR), we return a fallback for demo purposes
    if len(text) < 50:
        return "Experienced Software Engineer with a background in Python, Java, Machine Learning, and AWS. Built various side projects including a full-stack Next.js application."
        
    return text

def extract_skills(text: str) -> list[str]:
    # Mock skill extraction - in a real scenario we use spaCy NER or a specialized LLM
    common_skills = ["Python", "Java", "C++", "Machine Learning", "Deep Learning", "React", "Next.js", "SQL", "AWS", "Docker", "Kubernetes", "PyTorch", "TensorFlow", "FastAPI"]
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills
