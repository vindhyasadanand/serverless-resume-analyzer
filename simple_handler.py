"""
Simple Lambda Handler for Minimal Flask App
"""
import json
from simple_app import app


def lambda_handler(event, context):
    """Lambda handler for simple Flask app"""
    try:
        # Get the path and method from API Gateway event
        path = event.get('path', '/')
        http_method = event.get('httpMethod', 'GET')
        query_params = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')

        # Create basic WSGI environ
        environ = {
            'REQUEST_METHOD': http_method,
            'PATH_INFO': path,
            'QUERY_STRING': '&'.join([f'{k}={v}' for k, v in query_params.items()]),
            'CONTENT_TYPE': headers.get('content-type', 'application/json'),
            'CONTENT_LENGTH': str(len(body) if body else 0),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': body or '',
            'wsgi.errors': None,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }

        # Add headers
        for header_name, header_value in headers.items():
            environ[f'HTTP_{header_name.upper().replace("-", "_")}'] = header_value

        # Handle JSON body for POST requests
        if body and headers.get('content-type') == 'application/json':
            environ['wsgi.input'] = body

        # Response collection
        response_status = None
        response_headers = {}
        response_body = []

        def start_response(status, headers_list, exc_info=None):
            nonlocal response_status, response_headers
            response_status = status
            for name, value in headers_list:
                response_headers[name] = value

        # Call Flask app
        result = app(environ, start_response)

        # Collect response
        for data in result:
            response_body.append(data)

        # Prepare response
        body_content = b''.join(response_body).decode('utf-8')

        # Parse status code
        status_code = int(response_status.split()[0]) if response_status else 200

        return {
            'statusCode': status_code,
            'headers': response_headers,
            'body': body_content
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }