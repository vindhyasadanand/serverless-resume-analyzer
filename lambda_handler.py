"""
Simple Lambda Handler for Flask App
Direct HTTP handling without serverless-wsgi dependency
"""
from app import app
import json


def lambda_handler(event, context):
    """
    AWS Lambda handler function for API Gateway
    Handles HTTP requests and routes them to the Flask app
    """
    try:
        # Extract request information from API Gateway event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_params = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')

        # Create WSGI environ
        environ = {
            'REQUEST_METHOD': http_method,
            'PATH_INFO': path,
            'QUERY_STRING': '&'.join([f'{k}={v}' for k, v in query_params.items()]),
            'CONTENT_TYPE': headers.get('content-type', 'application/json'),
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': body,
            'wsgi.errors': None,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }

        # Add headers to environ
        for header_name, header_value in headers.items():
            environ[f'HTTP_{header_name.upper().replace("-", "_")}'] = header_value

        # Collect response
        response_data = []
        response_headers = {}
        response_status = None

        def start_response(status, response_headers_list, exc_info=None):
            nonlocal response_status, response_headers
            response_status = status
            for name, value in response_headers_list:
                response_headers[name] = value

        # Call the Flask app
        result = app(environ, start_response)

        # Collect response body
        for data in result:
            response_data.append(data)

        # Prepare API Gateway response
        response_body = b''.join(response_data).decode('utf-8')

        # Try to parse JSON response
        try:
            json_body = json.loads(response_body)
            return {
                'statusCode': int(response_status.split()[0]),
                'headers': response_headers,
                'body': json.dumps(json_body)
            }
        except json.JSONDecodeError:
            # Return as plain text if not JSON
            return {
                'statusCode': int(response_status.split()[0]),
                'headers': response_headers,
                'body': response_body
            }

    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }