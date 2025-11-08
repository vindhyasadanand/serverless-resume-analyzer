"""
Database Module
Handles data persistence using SQLite (easily adaptable to PostgreSQL for cloud)
Stores analysis history and results
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional


class Database:
    """SQLite database handler for storing analysis results"""
    
    def __init__(self, db_path: str = 'resume_analyzer.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create analyses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                job_description TEXT NOT NULL,
                overall_score REAL NOT NULL,
                skills_score REAL,
                experience_score REAL,
                education_score REAL,
                format_score REAL,
                matched_skills TEXT,
                missing_skills TEXT,
                recommendations TEXT,
                resume_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database initialized at {self.db_path}")
    
    def store_analysis(
        self,
        filename: str,
        resume_data: Dict,
        job_description: str,
        result: Dict
    ) -> int:
        """
        Store analysis result in database
        Returns the ID of the inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analyses (
                filename,
                job_description,
                overall_score,
                skills_score,
                experience_score,
                education_score,
                format_score,
                matched_skills,
                missing_skills,
                recommendations,
                resume_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            job_description,
            result['overall_score'],
            result['breakdown']['skills'],
            result['breakdown']['experience'],
            result['breakdown']['education'],
            result['breakdown']['format'],
            json.dumps(result['matched_skills']),
            json.dumps(result['missing_skills']),
            json.dumps(result['recommendations']),
            json.dumps(resume_data)
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Analysis stored with ID: {analysis_id}")
        return analysis_id
    
    def get_analysis(self, analysis_id: int) -> Optional[Dict]:
        """Retrieve a specific analysis by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analyses WHERE id = ?
        ''', (analysis_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_all_analyses(self, limit: int = 50) -> List[Dict]:
        """Retrieve all analyses, most recent first"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analyses 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """Delete a specific analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_analyses,
                AVG(overall_score) as avg_score,
                MAX(overall_score) as max_score,
                MIN(overall_score) as min_score
            FROM analyses
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total_analyses': row[0] or 0,
            'average_score': round(row[1], 2) if row[1] else 0,
            'highest_score': round(row[2], 2) if row[2] else 0,
            'lowest_score': round(row[3], 2) if row[3] else 0
        }
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Convert SQLite row to dictionary"""
        return {
            'id': row['id'],
            'filename': row['filename'],
            'job_description': row['job_description'],
            'overall_score': row['overall_score'],
            'breakdown': {
                'skills': row['skills_score'],
                'experience': row['experience_score'],
                'education': row['education_score'],
                'format': row['format_score']
            },
            'matched_skills': json.loads(row['matched_skills']),
            'missing_skills': json.loads(row['missing_skills']),
            'recommendations': json.loads(row['recommendations']),
            'created_at': row['created_at']
        }






