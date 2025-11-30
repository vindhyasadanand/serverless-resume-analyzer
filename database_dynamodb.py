"""
DynamoDB Database Module for AWS Lambda
Handles data persistence using AWS DynamoDB
"""
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import boto3
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal to float for JSON serialization"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class Database:
    """DynamoDB database handler for storing analysis results"""
    
    def __init__(self):
        self.table_name = os.environ.get('DYNAMODB_TABLE', 'resume-analyzer-dev')
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)
        print(f"✅ DynamoDB initialized: {self.table_name}")
    
    def _convert_floats_to_decimal(self, obj):
        """Convert floats to Decimal for DynamoDB"""
        if isinstance(obj, dict):
            return {k: self._convert_floats_to_decimal(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_floats_to_decimal(v) for v in obj]
        elif isinstance(obj, float):
            return Decimal(str(obj))
        return obj
    
    def store_analysis(
        self,
        filename: str,
        resume_data: Dict,
        job_description: str,
        result: Dict
    ) -> str:
        """
        Store analysis result in DynamoDB
        Returns the ID of the inserted record
        """
        analysis_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Convert floats to Decimal for DynamoDB
        item = self._convert_floats_to_decimal({
            'id': analysis_id,
            'filename': filename,
            'job_description': job_description,
            'overall_score': result['overall_score'],
            'breakdown': result['breakdown'],
            'matched_skills': result['matched_skills'],
            'missing_skills': result['missing_skills'],
            'recommendations': result['recommendations'],
            'resume_data': resume_data,
            'created_at': timestamp
        })
        
        self.table.put_item(Item=item)
        print(f"✅ Analysis stored with ID: {analysis_id}")
        return analysis_id
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict]:
        """Retrieve a specific analysis by ID"""
        try:
            response = self.table.get_item(Key={'id': analysis_id})
            if 'Item' in response:
                return json.loads(json.dumps(response['Item'], cls=DecimalEncoder))
            return None
        except Exception as e:
            print(f"Error retrieving analysis: {e}")
            return None
    
    def get_all_analyses(self, limit: int = 50) -> List[Dict]:
        """Retrieve all analyses"""
        try:
            response = self.table.scan(Limit=limit)
            items = response.get('Items', [])
            # Sort by created_at descending
            items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return json.loads(json.dumps(items, cls=DecimalEncoder))
        except Exception as e:
            print(f"Error retrieving analyses: {e}")
            return []
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """Delete a specific analysis"""
        try:
            self.table.delete_item(Key={'id': analysis_id})
            return True
        except Exception as e:
            print(f"Error deleting analysis: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            
            if not items:
                return {
                    'total_analyses': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'lowest_score': 0
                }
            
            scores = [float(item.get('overall_score', 0)) for item in items]
            
            return {
                'total_analyses': len(items),
                'average_score': round(sum(scores) / len(scores), 2),
                'highest_score': round(max(scores), 2),
                'lowest_score': round(min(scores), 2)
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_analyses': 0,
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0
            }
