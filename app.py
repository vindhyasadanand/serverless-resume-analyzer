"""
Resume Analyzer - Main Flask Application
Project Group 20: Cloud Computing Course
Team: Keyur Nareshkumar Modi, Naveen John, Vindhya Sadanand Hegde

This module handles file uploads, API endpoints, and coordinates the 
resume analysis pipeline using NLP techniques (TF-IDF, cosine similarity).

Architecture: RESTful API with serverless-ready design
Database: SQLite (local) / Cosmos DB (Azure)
NLP: scikit-learn + spaCy for intelligent resume matching
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
from datetime import datetime

from resume_parser import ResumeParser
try:
    from analyzer import ResumeAnalyzer
except ImportError:
    from analyzer_simple import ResumeAnalyzer
from database import Database

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize components
db = Database()
parser = ResumeParser()
analyzer = ResumeAnalyzer()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Resume Analyzer API v1.0',
        'endpoints': [
            'POST /api/analyze',
            'GET /api/history',
            'GET /api/analysis/<id>',
            'DELETE /api/analysis/<id>'
        ]
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    Main endpoint to analyze resume against job description
    Accepts: multipart/form-data with 'resume' file and 'job_description' text
    """
    try:
        # Check if resume file is present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not job_description:
            return jsonify({'error': 'No job description provided'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, TXT, DOCX'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # Parse resume
            print(f"Parsing resume: {filepath}")
            resume_data = parser.parse_resume(filepath)
            
            # Analyze compatibility
            print("Analyzing compatibility...")
            analysis_result = analyzer.analyze(resume_data, job_description)
            
            # Store in database
            analysis_id = db.store_analysis(
                filename=filename,
                resume_data=resume_data,
                job_description=job_description,
                result=analysis_result
            )
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'analysis_id': analysis_id,
                'score': analysis_result['overall_score'],
                'breakdown': analysis_result['breakdown'],
                'matched_skills': analysis_result['matched_skills'],
                'missing_skills': analysis_result['missing_skills'],
                'recommendations': analysis_result['recommendations'],
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as parse_error:
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            raise parse_error
            
    except Exception as e:
        print(f"Error in analyze_resume: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get all analysis history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = db.get_all_analyses(limit=limit)
        return jsonify({
            'success': True,
            'count': len(history),
            'analyses': history
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch history: {str(e)}'}), 500


@app.route('/api/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get specific analysis by ID"""
    try:
        analysis = db.get_analysis(analysis_id)
        if analysis:
            return jsonify({
                'success': True,
                'analysis': analysis
            }), 200
        else:
            return jsonify({'error': 'Analysis not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to fetch analysis: {str(e)}'}), 500


@app.route('/api/analysis/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Delete specific analysis"""
    try:
        success = db.delete_analysis(analysis_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Analysis deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Analysis not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete analysis: {str(e)}'}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        stats = db.get_statistics()
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to fetch stats: {str(e)}'}), 500


if __name__ == '__main__':
    print("🚀 Starting Resume Analyzer API...")
    print("📍 Server running at http://localhost:5001")
    print("📝 Upload resumes and get compatibility scores!")
    app.run(debug=True, host='0.0.0.0', port=5001)






