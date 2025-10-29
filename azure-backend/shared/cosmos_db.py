"""
Azure Cosmos DB Handler
Manages database operations for resume analyses
"""
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from azure.cosmos import CosmosClient, PartitionKey, exceptions


class CosmosDBHandler:
    """Handles Cosmos DB operations"""
    
    def __init__(self):
        # Get connection details from environment
        connection_string = os.environ.get('COSMOS_CONNECTION_STRING')
        database_name = os.environ.get('COSMOS_DATABASE', 'resumeDB')
        container_name = os.environ.get('COSMOS_CONTAINER', 'analyses')
        
        if not connection_string:
            raise ValueError("COSMOS_CONNECTION_STRING environment variable not set")
        
        # Initialize Cosmos client
        self.client = CosmosClient.from_connection_string(connection_string)
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)
    
    def store_analysis(
        self,
        filename: str,
        resume_data: Dict,
        job_description: str,
        result: Dict
    ) -> str:
        """Store analysis result in Cosmos DB"""
        analysis_id = str(uuid.uuid4())
        
        document = {
            'id': analysis_id,
            'filename': filename,
            'job_description': job_description,
            'overall_score': result['overall_score'],
            'breakdown': result['breakdown'],
            'matched_skills': result['matched_skills'],
            'missing_skills': result['missing_skills'],
            'recommendations': result['recommendations'],
            'skill_match_percentage': result.get('skill_match_percentage', 0),
            'resume_data': {
                'skills': resume_data.get('skills', []),
                'education': resume_data.get('education', []),
                'experience': resume_data.get('experience', []),
                'sections': resume_data.get('sections', {})
            },
            'created_at': datetime.utcnow().isoformat(),
            'timestamp': datetime.utcnow().timestamp()
        }
        
        try:
            self.container.create_item(body=document)
            return analysis_id
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to store analysis: {str(e)}")
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict]:
        """Retrieve a specific analysis by ID"""
        try:
            item = self.container.read_item(
                item=analysis_id,
                partition_key=analysis_id
            )
            return self._format_document(item)
        except exceptions.CosmosResourceNotFoundError:
            return None
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to retrieve analysis: {str(e)}")
    
    def get_all_analyses(self, limit: int = 50) -> List[Dict]:
        """Retrieve all analyses, most recent first"""
        query = f"SELECT * FROM c ORDER BY c.timestamp DESC OFFSET 0 LIMIT {limit}"
        
        try:
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return [self._format_document(item) for item in items]
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to retrieve analyses: {str(e)}")
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """Delete a specific analysis"""
        try:
            self.container.delete_item(
                item=analysis_id,
                partition_key=analysis_id
            )
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
        except exceptions.CosmosHttpResponseError as e:
            raise Exception(f"Failed to delete analysis: {str(e)}")
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        # Query for statistics
        count_query = "SELECT VALUE COUNT(1) FROM c"
        avg_query = "SELECT VALUE AVG(c.overall_score) FROM c"
        max_query = "SELECT VALUE MAX(c.overall_score) FROM c"
        min_query = "SELECT VALUE MIN(c.overall_score) FROM c"
        
        try:
            count = list(self.container.query_items(
                query=count_query,
                enable_cross_partition_query=True
            ))[0] if list(self.container.query_items(query=count_query, enable_cross_partition_query=True)) else 0
            
            avg = list(self.container.query_items(
                query=avg_query,
                enable_cross_partition_query=True
            ))[0] if list(self.container.query_items(query=avg_query, enable_cross_partition_query=True)) else 0
            
            max_score = list(self.container.query_items(
                query=max_query,
                enable_cross_partition_query=True
            ))[0] if list(self.container.query_items(query=max_query, enable_cross_partition_query=True)) else 0
            
            min_score = list(self.container.query_items(
                query=min_query,
                enable_cross_partition_query=True
            ))[0] if list(self.container.query_items(query=min_query, enable_cross_partition_query=True)) else 0
            
            return {
                'total_analyses': count or 0,
                'average_score': round(avg, 2) if avg else 0,
                'highest_score': round(max_score, 2) if max_score else 0,
                'lowest_score': round(min_score, 2) if min_score else 0
            }
        except Exception as e:
            # Return default stats if queries fail
            return {
                'total_analyses': 0,
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0
            }
    
    def _format_document(self, doc: Dict) -> Dict:
        """Format document for response"""
        return {
            'id': doc.get('id'),
            'filename': doc.get('filename'),
            'job_description': doc.get('job_description'),
            'overall_score': doc.get('overall_score'),
            'breakdown': doc.get('breakdown', {}),
            'matched_skills': doc.get('matched_skills', []),
            'missing_skills': doc.get('missing_skills', []),
            'recommendations': doc.get('recommendations', []),
            'skill_match_percentage': doc.get('skill_match_percentage', 0),
            'created_at': doc.get('created_at')
        }






