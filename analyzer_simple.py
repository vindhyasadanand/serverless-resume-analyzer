"""
Lightweight Resume Analyzer for AWS Lambda
Group 20: Keyur Modi, Naveen John, Vindhya Hegde

Simple keyword-based matching (Lambda-compatible, no heavy ML libraries)
"""
import re
from typing import Dict, List, Set
from collections import Counter


class ResumeAnalyzer:
    """Lightweight analyzer using keyword matching"""
    
    def __init__(self):
        self.tech_keywords = {
            'python', 'java', 'javascript', 'react', 'node', 'aws', 'docker',
            'kubernetes', 'sql', 'mongodb', 'django', 'flask', 'spring',
            'microservices', 'api', 'rest', 'graphql', 'ci/cd', 'jenkins',
            'git', 'agile', 'scrum', 'machine learning', 'ai', 'data science'
        }
    
    def analyze(self, resume_text: str, job_description: str) -> Dict:
        """Analyze resume against job description"""
        
        # Normalize text
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Extract keywords
        resume_keywords = self._extract_keywords(resume_lower)
        job_keywords = self._extract_keywords(job_lower)
        
        # Calculate matches
        matched = resume_keywords & job_keywords
        missing = job_keywords - resume_keywords
        
        # Calculate score
        if len(job_keywords) > 0:
            match_score = (len(matched) / len(job_keywords)) * 100
        else:
            match_score = 50
        
        # Generate breakdown
        breakdown = {
            'skills': min(match_score, 100),
            'experience': self._calculate_experience_score(resume_lower, job_lower),
            'education': self._calculate_education_score(resume_lower, job_lower),
            'format': 85  # Static score for format
        }
        
        overall_score = sum(breakdown.values()) / len(breakdown)
        
        return {
            'overall_score': round(overall_score, 2),
            'breakdown': breakdown,
            'matched_keywords': list(matched)[:20],
            'missing_keywords': list(missing)[:10],
            'recommendations': self._generate_recommendations(overall_score, list(missing)[:5])
        }
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text"""
        words = set(re.findall(r'\b\w+\b', text))
        # Find matching tech keywords
        found = set()
        for keyword in self.tech_keywords:
            if keyword in text:
                found.add(keyword)
        # Add other significant words
        for word in words:
            if len(word) > 3 and word.isalpha():
                found.add(word)
        return found
    
    def _calculate_experience_score(self, resume: str, job: str) -> float:
        """Simple experience scoring"""
        exp_keywords = ['years', 'experience', 'worked', 'developed', 'managed', 'led']
        score = sum(1 for kw in exp_keywords if kw in resume) * 10
        return min(score, 100)
    
    def _calculate_education_score(self, resume: str, job: str) -> float:
        """Simple education scoring"""
        edu_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        score = sum(1 for kw in edu_keywords if kw in resume) * 15
        return min(score, 100)
    
    def _generate_recommendations(self, score: float, missing: List[str]) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if score < 50:
            recommendations.append("Consider adding more relevant skills from the job description")
        if score < 70:
            recommendations.append("Highlight projects that match the job requirements")
        
        if missing:
            recommendations.append(f"Add these skills to your resume: {', '.join(missing[:3])}")
        
        if score >= 80:
            recommendations.append("Strong match! Emphasize your matching skills in your application")
        
        return recommendations or ["Your resume looks good!"]

