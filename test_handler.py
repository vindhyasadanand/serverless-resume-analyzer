"""
Minimal Lambda Handler for Testing
"""
import json


def lambda_handler(event, context):
    """Simple test handler"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Hello from Lambda!', 'status': 'success'})
    }