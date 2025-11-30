"""
Minimal Resume Analyzer - Simplified Version
For AWS Lambda deployment with minimal dependencies
"""
import os
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def simple_text_similarity(text1, text2):
    """Simple keyword-based similarity without ML libraries"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    if not union:
        return 0.0

    return len(intersection) / len(union)


def analyze_resume_simple(resume_text, job_description):
    """Simple resume analysis without complex ML"""
    # Extract basic keywords
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    # Simple skill matching
    common_skills = [
        'python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes',
        'react', 'node.js', 'machine learning', 'data analysis', 'git'
    ]

    matched_skills = []
    missing_skills = []

    for skill in common_skills:
        if skill in resume_lower:
            matched_skills.append(skill)
        elif skill in job_lower:
            missing_skills.append(skill)

    # Calculate similarity score
    similarity = simple_text_similarity(resume_text, job_description)
    overall_score = min(100, int(similarity * 100))

    return {
        'overall_score': overall_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'recommendations': [
            'Consider adding missing skills to your resume',
            'Highlight relevant experience more prominently',
            'Use similar keywords from the job description'
        ]
    }


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Resume Analyzer API is running',
        'version': '1.0.0'
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze resume against job description"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        resume_text = data.get('resume', '')
        job_description = data.get('job_description', '')

        if not resume_text or not job_description:
            return jsonify({'error': 'Both resume and job_description are required'}), 400

        result = analyze_resume_simple(resume_text, job_description)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Resume Analyzer API',
        'endpoints': {
            'GET /health': 'Health check',
            'POST /analyze': 'Analyze resume'
        }
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)