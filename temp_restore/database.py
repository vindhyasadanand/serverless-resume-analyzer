import sqlite3
import json
import os
from datetime import datetime

class ResumeDatabase:
    def __init__(self):
        # Use /tmp for AWS Elastic Beanstalk write permissions
        self.db_path = '/tmp/resume_analyzer.db'
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    resume_name TEXT,
                    job_description TEXT,
                    overall_score INTEGER,
                    breakdown TEXT,
                    matched_skills TEXT,
                    matched_keywords TEXT,
                    missing_skills TEXT,
                    missing_keywords TEXT,
                    recommendations TEXT,
                    created_at TEXT,
                    date TEXT
                )
            ''')
            conn.commit()

    def save_analysis(self, data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO analysis_history (
                    filename, resume_name, job_description, overall_score, breakdown,
                    matched_skills, matched_keywords, missing_skills, missing_keywords, 
                    recommendations, created_at, date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('resume_name', 'Unknown'),  # filename for frontend
                data.get('resume_name', 'Unknown'),  # keep resume_name for compatibility
                data.get('job_description', ''),
                data.get('overall_score', 0),
                json.dumps(data.get('breakdown', {})),
                json.dumps(data.get('matched_keywords', [])),  # matched_skills for frontend
                json.dumps(data.get('matched_keywords', [])),  # keep matched_keywords
                json.dumps(data.get('missing_keywords', [])),  # missing_skills for frontend
                json.dumps(data.get('missing_keywords', [])),  # keep missing_keywords
                json.dumps(data.get('recommendations', [])),
                timestamp,  # created_at for frontend
                timestamp   # keep date for compatibility
            ))
            conn.commit()
            return cursor.lastrowid

    def get_history(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM analysis_history ORDER BY id DESC')
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                item = dict(row)
                # Parse JSON strings back to objects for the frontend
                try:
                    item['breakdown'] = json.loads(item['breakdown'])
                    item['matched_skills'] = json.loads(item['matched_skills'])
                    item['matched_keywords'] = json.loads(item['matched_keywords'])
                    item['missing_skills'] = json.loads(item['missing_skills'])
                    item['missing_keywords'] = json.loads(item['missing_keywords'])
                    item['recommendations'] = json.loads(item['recommendations'])
                except:
                    pass
                
                # Ensure created_at exists and is properly formatted
                if not item.get('created_at'):
                    # Use date field as fallback, or use current time
                    item['created_at'] = item.get('date') or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                history.append(item)
            return history

    def delete_analysis(self, analysis_id):
        """Delete an analysis record by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM analysis_history WHERE id = ?', (analysis_id,))
            conn.commit()
            return cursor.rowcount > 0