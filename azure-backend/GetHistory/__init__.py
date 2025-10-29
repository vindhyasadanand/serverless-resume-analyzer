"""
Azure Function: Get History
HTTP Trigger function to retrieve analysis history
"""
import azure.functions as func
import json
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.cosmos_db import CosmosDBHandler


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get all analysis history"""
    logging.info('Processing history request')
    
    try:
        # Get limit parameter
        limit = req.params.get('limit', '50')
        try:
            limit = int(limit)
        except ValueError:
            limit = 50
        
        # Initialize database
        db = CosmosDBHandler()
        
        # Get analyses
        history = db.get_all_analyses(limit=limit)
        
        response = {
            'success': True,
            'count': len(history),
            'analyses': history
        }
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logging.error(f'Error in get_history: {str(e)}')
        return func.HttpResponse(
            json.dumps({'error': f'Failed to fetch history: {str(e)}'}),
            status_code=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )






