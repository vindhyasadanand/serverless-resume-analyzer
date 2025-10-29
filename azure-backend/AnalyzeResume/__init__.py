"""
Azure Function: Analyze Resume
HTTP Trigger function to analyze resume against job description
"""
import azure.functions as func
import json
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from shared.resume_parser import ResumeParser
from shared.analyzer import ResumeAnalyzer
from shared.cosmos_db import CosmosDBHandler


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Analyze resume against job description
    Expects multipart/form-data with:
    - resume: file (PDF, TXT, DOCX)
    - job_description: text
    """
    logging.info('Processing resume analysis request')
    
    try:
        # Get job description from form data
        job_description = req.form.get('job_description')
        if not job_description:
            return func.HttpResponse(
                json.dumps({'error': 'No job description provided'}),
                status_code=400,
                mimetype='application/json'
            )
        
        # Get resume file
        resume_file = req.files.get('resume')
        if not resume_file:
            return func.HttpResponse(
                json.dumps({'error': 'No resume file provided'}),
                status_code=400,
                mimetype='application/json'
            )
        
        filename = resume_file.filename
        if not filename:
            return func.HttpResponse(
                json.dumps({'error': 'No file selected'}),
                status_code=400,
                mimetype='application/json'
            )
        
        # Validate file type
        allowed_extensions = ['pdf', 'txt', 'docx']
        ext = filename.lower().split('.')[-1]
        if ext not in allowed_extensions:
            return func.HttpResponse(
                json.dumps({'error': f'Invalid file type. Allowed: {", ".join(allowed_extensions)}'}),
                status_code=400,
                mimetype='application/json'
            )
        
        # Read file bytes
        file_bytes = resume_file.read()
        
        # Check file size (5MB limit)
        if len(file_bytes) > 5 * 1024 * 1024:
            return func.HttpResponse(
                json.dumps({'error': 'File size exceeds 5MB limit'}),
                status_code=400,
                mimetype='application/json'
            )
        
        logging.info(f'Parsing resume: {filename}')
        
        # Initialize components
        parser = ResumeParser()
        analyzer = ResumeAnalyzer()
        db = CosmosDBHandler()
        
        # Parse resume
        resume_data = parser.parse_resume_from_bytes(file_bytes, filename)
        
        # Analyze compatibility
        logging.info('Analyzing compatibility...')
        analysis_result = analyzer.analyze(resume_data, job_description)
        
        # Store in database
        logging.info('Storing analysis in database...')
        analysis_id = db.store_analysis(
            filename=filename,
            resume_data=resume_data,
            job_description=job_description,
            result=analysis_result
        )
        
        # Prepare response
        response = {
            'success': True,
            'analysis_id': analysis_id,
            'score': analysis_result['overall_score'],
            'breakdown': analysis_result['breakdown'],
            'matched_skills': analysis_result['matched_skills'],
            'missing_skills': analysis_result['missing_skills'],
            'recommendations': analysis_result['recommendations'],
            'skill_match_percentage': analysis_result.get('skill_match_percentage', 0)
        }
        
        logging.info(f'Analysis complete. Score: {analysis_result["overall_score"]}')
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logging.error(f'Error in analyze_resume: {str(e)}')
        return func.HttpResponse(
            json.dumps({'error': f'Analysis failed: {str(e)}'}),
            status_code=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )






