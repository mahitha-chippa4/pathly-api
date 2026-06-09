def generate_roadmap(match_result: dict) -> dict:
    missing_skills = match_result.get("missing_skills", [])
    found_skills = match_result.get("found_skills", [])
    
    # Calculate dynamic timeline based on missing skills
    # Assume each missing skill takes roughly 0.5 to 1.5 months to learn depending on complexity
    base_time_per_skill = 0.8
    total_months = len(missing_skills) * base_time_per_skill
    
    # If they know a lot, they learn faster
    if len(found_skills) > 5:
        total_months *= 0.8
        
    estimated_duration = round(max(0.5, total_months), 1)
    
    milestones = []
    
    for i, skill in enumerate(missing_skills):
        milestones.append({
            "id": i + 1,
            "title": f"Master {skill}",
            "description": f"Focus on understanding the core concepts and practical applications of {skill}.",
            "duration": "2-3 weeks",
            "resources": [
                {"type": "course", "title": f"Complete {skill} Bootcamp", "platform": "Coursera"},
                {"type": "video", "title": f"{skill} in 100 Seconds", "platform": "YouTube"}
            ],
            "projects": [
                {"title": f"Build a {skill} Integration", "difficulty": "Intermediate"}
            ]
        })
        
    if not milestones:
        milestones.append({
            "id": 1,
            "title": "Advanced Interview Prep",
            "description": "You already have the necessary skills! Focus entirely on LeetCode and System Design.",
            "duration": "1 month",
            "resources": [],
            "projects": []
        })
        
    return {
        "estimated_duration_months": estimated_duration,
        "confidence_score": "85%",
        "milestones": milestones,
        "recommended_projects": [],
        "coding_questions": []
    }
