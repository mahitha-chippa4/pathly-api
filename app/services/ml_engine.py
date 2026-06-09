import json
import os
import random
from app.services.parser import extract_skills

# Try loading ML libraries, fallback if not available yet
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    model = SentenceTransformer('all-MiniLM-L6-v2')
    USE_ML = True
except ImportError:
    USE_ML = False
    print("Warning: ML libraries not found. Using fallback exact matching.")

def load_roles():
    roles_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'roles.json')
    with open(roles_path, 'r') as f:
        return json.load(f)

def calculate_match(resume_text: str, target_role: str) -> dict:
    roles = load_roles()
    if target_role not in roles:
        target_role = "Software Engineer" # Default fallback
        
    role_data = roles[target_role]
    required = role_data["required_skills"]
    preferred = role_data["preferred_skills"]
    
    # Extract skills from resume
    user_skills = extract_skills(resume_text)
    
    # If ML is available, use semantic matching
    if USE_ML and len(user_skills) > 0:
        # Create embeddings for target skills
        target_skills = required + preferred
        target_embeddings = model.encode(target_skills)
        user_embeddings = model.encode(user_skills)
        
        # Calculate similarity
        sim_matrix = cosine_similarity(user_embeddings, target_embeddings)
        
        # Find best match for each target skill
        match_scores = []
        found_skills = []
        missing_skills = []
        
        for i, target_skill in enumerate(target_skills):
            # Best match for this target skill from any user skill
            best_sim = np.max(sim_matrix[:, i])
            if best_sim > 0.6:  # Threshold for "knowing" the skill
                found_skills.append(target_skill)
                match_scores.append(best_sim)
            else:
                missing_skills.append(target_skill)
                
        # Calculate overall score
        base_score = sum(match_scores) / len(target_skills) if target_skills else 0
        overall_score = int(min(100, base_score * 100 + 20)) # Boost score a bit
        
    else:
        # Fallback exact string matching
        found_skills = [s for s in required + preferred if s.lower() in [us.lower() for us in user_skills]]
        missing_skills = [s for s in required + preferred if s not in found_skills]
        
        # Calculate score (weighted towards required)
        req_found = [s for s in required if s in found_skills]
        pref_found = [s for s in preferred if s in found_skills]
        
        score_pct = (len(req_found) * 2 + len(pref_found)) / (len(required) * 2 + len(preferred)) if required else 0.5
        overall_score = int(score_pct * 100)
        
    # Readness score
    readiness_score = max(0, overall_score - random.randint(5, 15))
        
    return {
        "role": target_role,
        "match_score": overall_score,
        "readiness_score": readiness_score,
        "found_skills": found_skills,
        "missing_skills": missing_skills,
        "user_skills_extracted": user_skills
    }
