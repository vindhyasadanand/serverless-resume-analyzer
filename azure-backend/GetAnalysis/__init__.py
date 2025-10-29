"""
Azure Function: Get Analysis
HTTP Trigger function to retrieve specific analysis by ID
"""
import azure.functions as func
import json
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.cosmos_db import CosmosDBHandler


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get specific analysis by ID"""
    logging.info('Processing get analysis request')
    
    try:
        # Get analysis ID from route parameters
        analysis_id = req.route_params.get('id')
        
        if not analysis_id:
            return func.HttpResponse(
                json.dumps({'error': 'Analysis ID is required'}),
                status_code=400,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )
        
        # Initialize database
        db = CosmosDBHandler()
        
        # Get analysis
        analysis = db.get_analysis(analysis_id)
        
        if analysis:
            response = {
                'success': True,
                'analysis': analysis
            }
            return func.HttpResponse(
                json.dumps(response),
                status_code=200,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )
        else:
            return func.HttpResponse(
                json.dumps({'error': 'Analysis not found'}),
                status_code=404,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )
        
    except Exception as e:
        logging.error(f'Error in get_analysis: {str(e)}')
        return func.HttpResponse(
            json.dumps({'error': f'Failed to fetch analysis: {str(e)}'}),
            status_code=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )






