import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.services.parser import parse_resume
from app.services.ml_engine import calculate_match
from app.services.roadmap_engine import generate_roadmap

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    target_role = request.args.get('target_role', 'ML Engineer')
    
    file_bytes = file.read()
    filename = file.filename
    
    # 1. Parse resume
    resume_text = parse_resume(file_bytes, filename)
    
    # 2. Extract skills and match with role
    match_result = calculate_match(resume_text, target_role)
    
    # 3. Generate Roadmap
    roadmap = generate_roadmap(match_result)
    
    return jsonify({
        "match_result": match_result,
        "roadmap": roadmap
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
