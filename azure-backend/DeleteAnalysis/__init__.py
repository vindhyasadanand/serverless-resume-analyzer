"""
Azure Function: Delete Analysis
HTTP Trigger function to delete specific analysis
"""
import azure.functions as func
import json
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.cosmos_db import CosmosDBHandler


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Delete specific analysis"""
    logging.info('Processing delete analysis request')
    
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
        
        # Delete analysis
        success = db.delete_analysis(analysis_id)
        
        if success:
            response = {
                'success': True,
                'message': 'Analysis deleted successfully'
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
        logging.error(f'Error in delete_analysis: {str(e)}')
        return func.HttpResponse(
            json.dumps({'error': f'Failed to delete analysis: {str(e)}'}),
            status_code=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )






