"""
WSGI Handler for AWS Lambda
This module wraps the Flask application for serverless deployment.
"""
import serverless_wsgi
from app import app

def handler(event, context):
    """
    AWS Lambda handler function
    Routes all HTTP requests through the Flask application
    """
    return serverless_wsgi.handle_request(app, event, context)