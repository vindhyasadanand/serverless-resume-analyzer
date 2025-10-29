"""
Azure Function: Get Statistics
HTTP Trigger function to retrieve overall statistics
"""
import azure.functions as func
import json
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.cosmos_db import CosmosDBHandler


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get overall statistics"""
    logging.info('Processing stats request')
    
    try:
        # Initialize database
        db = CosmosDBHandler()
        
        # Get statistics
        stats = db.get_statistics()
        
        response = {
            'success': True,
            'stats': stats
        }
        
        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logging.error(f'Error in get_stats: {str(e)}')
        return func.HttpResponse(
            json.dumps({'error': f'Failed to fetch stats: {str(e)}'}),
            status_code=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )






