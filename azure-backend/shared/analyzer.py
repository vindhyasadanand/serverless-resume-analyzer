"""
Resume Analyzer Module for Azure Functions
Performs NLP-based analysis using TF-IDF and cosine similarity
"""
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple


class ResumeAnalyzer:
    """Analyzes resume compatibility with job descriptions using NLP"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=500,
            ngram_range=(1, 2)
        )
    
    def analyze(self, resume_data: Dict, job_description: str) -> Dict:
        """Main analysis function"""
        resume_text = resume_data['raw_text']
        resume_skills = resume_data['skills']
        
        # Calculate overall similarity score
        overall_score = self._calculate_similarity(resume_text, job_description)
        
        # Extract job requirements
        job_skills = self._extract_job_skills(job_description)
        job_requirements = self._extract_requirements(job_description)
        
        # Skills matching
        matched_skills, missing_skills = self._match_skills(resume_skills, job_skills)
        
        # Calculate category breakdown
        breakdown = self._calculate_breakdown(
            resume_data, 
            job_description, 
            matched_skills, 
            job_skills
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            overall_score,
            matched_skills,
            missing_skills,
            resume_data
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'breakdown': breakdown,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'job_requirements': job_requirements,
            'recommendations': recommendations,
            'skill_match_percentage': self._calculate_skill_percentage(matched_skills, job_skills)
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts using TF-IDF"""
        try:
            text1_clean = self._preprocess_text(text1)
            text2_clean = self._preprocess_text(text2)
            
            tfidf_matrix = self.vectorizer.fit_transform([text1_clean, text2_clean])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity * 100
        
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = ' '.join(text.split())
        return text
    
    def _extract_job_skills(self, job_description: str) -> List[str]:
        """Extract required skills from job description"""
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express', 'fastapi',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'dynamodb',
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'data science', 'ai',
            'html', 'css', 'rest', 'api', 'graphql', 'microservices', 'agile', 'scrum',
            'git', 'github', 'gitlab', 'linux', 'bash', 'shell scripting',
            'kafka', 'rabbitmq', 'spark', 'hadoop', 'pandas', 'numpy', 'scikit-learn',
            'tensorflow', 'pytorch', 'keras', 'tableau', 'power bi', 'excel'
        ]
        
        job_desc_lower = job_description.lower()
        found_skills = []
        
        for skill in skill_keywords:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, job_desc_lower):
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_requirements(self, job_description: str) -> List[str]:
        """Extract key requirements from job description"""
        requirements = []
        lines = job_description.split('\n')
        
        for line in lines:
            line = line.strip()
            if re.match(r'^[\-\*•]\s+', line) or re.match(r'^\d+[\.)]\s+', line):
                clean_line = re.sub(r'^[\-\*•\d\.)]+\s+', '', line)
                if len(clean_line) > 10:
                    requirements.append(clean_line)
        
        return requirements[:10]
    
    def _match_skills(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[List[str], List[str]]:
        """Compare resume skills with job requirements"""
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matched = [skill for skill in job_skills_lower if skill in resume_skills_lower]
        missing = [skill for skill in job_skills_lower if skill not in resume_skills_lower]
        
        return matched, missing
    
    def _calculate_breakdown(
        self, 
        resume_data: Dict, 
        job_description: str, 
        matched_skills: List[str],
        job_skills: List[str]
    ) -> Dict[str, float]:
        """Calculate score breakdown by category"""
        # Skills score
        if job_skills:
            skills_score = (len(matched_skills) / len(job_skills)) * 100
        else:
            skills_score = 50
        
        # Experience score
        experience_score = 0
        if resume_data['experience']:
            experience_score = 70
            exp_text = ' '.join(resume_data['experience'])
            if len(exp_text) > 100:
                experience_score += 20
        
        # Education score
        education_score = 0
        if resume_data['education']:
            education_score = 80
            job_lower = job_description.lower()
            for edu in resume_data['education']:
                if 'master' in edu.lower() and 'master' in job_lower:
                    education_score = 100
                elif 'bachelor' in edu.lower() and 'bachelor' in job_lower:
                    education_score = 90
        
        # Format score
        sections = resume_data['sections']
        section_score = sum([
            30 if sections.get('skills') else 0,
            30 if sections.get('experience') else 0,
            25 if sections.get('education') else 0,
            15 if sections.get('projects') else 0
        ])
        
        return {
            'skills': round(min(skills_score, 100), 2),
            'experience': round(min(experience_score, 100), 2),
            'education': round(min(education_score, 100), 2),
            'format': round(min(section_score, 100), 2)
        }
    
    def _calculate_skill_percentage(self, matched_skills: List[str], job_skills: List[str]) -> float:
        """Calculate percentage of required skills that are matched"""
        if not job_skills:
            return 100.0
        return round((len(matched_skills) / len(job_skills)) * 100, 2)
    
    def _generate_recommendations(
        self,
        overall_score: float,
        matched_skills: List[str],
        missing_skills: List[str],
        resume_data: Dict
    ) -> List[str]:
        """Generate personalized recommendations for improvement"""
        recommendations = []
        
        if overall_score < 50:
            recommendations.append(
                "Your resume shows low compatibility with this job. Consider tailoring "
                "your resume to better highlight relevant skills and experience."
            )
        elif overall_score < 70:
            recommendations.append(
                "Good match, but there's room for improvement. Focus on emphasizing "
                "key skills mentioned in the job description."
            )
        else:
            recommendations.append(
                "Excellent match! Your resume aligns well with the job requirements. "
                "Make sure to highlight your achievements in these areas."
            )
        
        if missing_skills:
            top_missing = missing_skills[:5]
            recommendations.append(
                f"Consider adding these in-demand skills: {', '.join(top_missing)}. "
                "Take online courses or work on projects to develop these competencies."
            )
        
        sections = resume_data['sections']
        if not sections.get('projects'):
            recommendations.append(
                "Add a Projects section to showcase practical applications of your skills."
            )
        
        if not sections.get('certifications'):
            recommendations.append(
                "Include relevant certifications to strengthen your profile."
            )
        
        if not resume_data['experience']:
            recommendations.append(
                "Add internships, volunteer work, or academic projects to demonstrate experience."
            )
        
        return recommendations






