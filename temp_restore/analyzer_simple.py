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
        # Comprehensive tech skills keywords
        self.tech_keywords = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'ruby', 'go', 'golang', 'php', 
            'swift', 'kotlin', 'rust', 'scala', 'perl', 'r', 'matlab', 'dart', 'objective-c', 'vb.net',
            'bash', 'shell', 'powershell',
            
            # Web Frontend
            'react', 'angular', 'vue', 'svelte', 'jquery', 'html', 'html5', 'css', 'css3', 'sass', 'scss',
            'less', 'bootstrap', 'tailwind', 'material-ui', 'mui', 'chakra', 'styled-components',
            
            # Backend Frameworks
            'node', 'nodejs', 'express', 'django', 'flask', 'fastapi', 'spring', 'spring boot', 'springboot',
            'asp.net', '.net', 'dotnet', 'rails', 'laravel', 'symfony', 'nestjs', 'nextjs', 'nuxt',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite',
            'firebase', 'dynamodb', 'cassandra', 'elasticsearch', 'neo4j', 'mariadb', 'couchdb',
            'snowflake', 'bigquery', 'redshift',
            
            # Cloud Platforms
            'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp', 'google cloud', 'heroku',
            'digitalocean', 'linode', 'netlify', 'vercel', 'cloudflare',
            
            # Cloud Services
            'ec2', 's3', 'lambda', 'rds', 'cloudformation', 'elastic beanstalk', 'ecs', 'eks',
            'cloud functions', 'app engine', 'cloud run',
            
            # DevOps & CI/CD
            'docker', 'kubernetes', 'k8s', 'jenkins', 'ci/cd', 'gitlab ci', 'github actions', 'circleci',
            'travis ci', 'terraform', 'ansible', 'puppet', 'chef', 'vagrant', 'prometheus', 'grafana',
            'datadog', 'newrelic', 'splunk',
            
            # Testing
            'junit', 'mockito', 'selenium', 'jest', 'mocha', 'chai', 'pytest', 'unittest', 'testng',
            'cypress', 'playwright', 'puppeteer', 'jasmine', 'karma', 'tdd', 'bdd', 'testing',
            
            # Mobile Development
            'android', 'ios', 'flutter', 'react native', 'xamarin', 'cordova', 'ionic', 'swift', 'swiftui',
            'kotlin', 'java android', 'android studio', 'xcode',
            
            # Methodologies & Practices
            'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'sdlc', 'oop', 'functional programming',
            'design patterns', 'solid', 'clean code', 'code review', 'pair programming',
            
            # Version Control
            'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial', 'version control',
            
            # Architecture & APIs
            'microservices', 'rest', 'restful', 'api', 'graphql', 'soap', 'grpc', 'websocket',
            'serverless', 'event-driven', 'mvc', 'mvvm', 'soa', 'monolith',
            
            # Data Science & ML
            'machine learning', 'ml', 'ai', 'artificial intelligence', 'deep learning', 'neural networks',
            'data science', 'pandas', 'numpy', 'scikit-learn', 'sklearn', 'tensorflow', 'pytorch',
            'keras', 'opencv', 'nlp', 'computer vision', 'data analysis', 'statistics',
            
            # Big Data
            'hadoop', 'spark', 'kafka', 'airflow', 'databricks', 'hive', 'pig', 'flink',
            
            # Project Management & Collaboration
            'jira', 'confluence', 'trello', 'asana', 'slack', 'teams', 'notion',
            
            # Build Tools
            'webpack', 'vite', 'rollup', 'parcel', 'maven', 'gradle', 'npm', 'yarn', 'pip',
            
            # ORM & Data Access
            'hibernate', 'sequelize', 'prisma', 'typeorm', 'mongoose', 'sqlalchemy',
            
            # Security
            'oauth', 'jwt', 'ssl', 'tls', 'encryption', 'authentication', 'authorization',
            
            # Other Tools & Technologies
            'linux', 'unix', 'windows', 'macos', 'vim', 'vscode', 'intellij', 'eclipse',
            'postman', 'swagger', 'graphql', 'ajax', 'json', 'xml', 'yaml', 'regex',
            'rabbitmq', 'celery', 'nginx', 'apache', 'tomcat', 'gunicorn', 'uvicorn'
        }
        
        # Synonym mapping for better matching
        self.synonyms = {
            'js': 'javascript',
            'ts': 'typescript',
            'k8s': 'kubernetes',
            'ml': 'machine learning',
            'restful': 'rest',
            'springboot': 'spring boot',
            'react.js': 'react',
            'node.js': 'node',
            'vue.js': 'vue',
            'angular.js': 'angular',
        }
        
        # Related skills - if resume has these, count as having the key
        self.related_skills = {
            'tdd': ['junit', 'mockito', 'testing', 'pytest', 'jest', 'unittest', 'testng', 'cypress'],
            'test driven development': ['tdd', 'junit', 'mockito', 'pytest', 'testing'],
            'unit testing': ['junit', 'mockito', 'pytest', 'jest', 'unittest', 'testing'],
            'rest': ['api', 'restful', 'rest api', 'web services'],
            'restful': ['rest', 'api', 'rest api'],
            'web services': ['rest', 'soap', 'api', 'restful'],
            'soap': ['web services', 'api'],
            'mobile': ['ios', 'android', 'swift', 'kotlin', 'flutter', 'react native'],
            'mobile development': ['ios', 'android', 'swift', 'kotlin', 'flutter'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud computing'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform'],
            'ci/cd': ['jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci'],
            'agile': ['scrum', 'kanban', 'agile methodologies'],
            'scrum': ['agile', 'scrum master', 'sprint'],
            'backend': ['node', 'django', 'flask', 'spring', 'express', 'api'],
            'frontend': ['react', 'angular', 'vue', 'javascript', 'html', 'css'],
            'fullstack': ['frontend', 'backend', 'react', 'node', 'javascript'],
            'full stack': ['frontend', 'backend', 'fullstack'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle'],
            'sql': ['mysql', 'postgresql', 'sql server', 'oracle', 'database'],
            'nosql': ['mongodb', 'redis', 'cassandra', 'dynamodb'],
            'javascript': ['js', 'node', 'react', 'angular', 'vue'],
            'java': ['spring', 'spring boot', 'hibernate', 'maven', 'gradle'],
            'python': ['django', 'flask', 'pandas', 'numpy'],
            'oop': ['object oriented', 'java', 'c++', 'c#', 'python'],
            'object oriented': ['oop', 'java', 'c++', 'c#'],
        }
        
        # Common words to ignore (not skills)
        self.stopwords = {
            'with', 'their', 'including', 'team', 'experience', 'requirements', 'skills',
            'engineering', 'applications', 'cross', 'methodologies', 'results', 'problems',
            'driven', 'post', 'reviews', 'applying', 'various', 'solving', 'coding', 'units',
            'work', 'years', 'using', 'strong', 'good', 'excellent', 'ability', 'knowledge',
            'understanding', 'developing', 'developed', 'design', 'implementation', 'system'
        }
    
    def analyze(self, resume_text: str, job_description: str) -> Dict:
        """Analyze resume against job description"""
        
        # Normalize text
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Extract keywords
        resume_keywords = self._extract_keywords(resume_lower)
        job_keywords = self._extract_keywords(job_lower)
        
        # Calculate matches with related skills consideration
        matched = resume_keywords & job_keywords
        
        # Check for related skills - if job wants TDD but resume has JUnit, count as match
        additional_matches = set()
        for job_skill in job_keywords:
            if job_skill in self.related_skills:
                related = self.related_skills[job_skill]
                if any(rel in resume_keywords for rel in related):
                    additional_matches.add(job_skill)
        
        matched = matched | additional_matches
        missing = job_keywords - matched
        
        # Calculate score
        if len(job_keywords) > 0:
            match_score = (len(matched) / len(job_keywords)) * 100
        else:
            match_score = 50
        
        # Generate breakdown
        breakdown = {
            'skills': round(min(match_score, 100)),
            'experience': round(self._calculate_experience_score(resume_lower, job_lower)),
            'education': round(self._calculate_education_score(resume_lower, job_lower)),
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
        """Extract keywords from text - focus on tech skills only"""
        found = set()
        
        # Apply synonym replacements
        text_normalized = text
        for synonym, canonical in self.synonyms.items():
            text_normalized = text_normalized.replace(synonym, canonical)
        
        # Find tech keywords (multi-word and single-word)
        for keyword in self.tech_keywords:
            if keyword in text_normalized:
                found.add(keyword)
        
        # Extract words and check against tech keywords
        words = re.findall(r'\b\w+\b', text_normalized)
        for word in words:
            # Only add if it's a tech keyword or similar, ignore stopwords
            if (len(word) > 3 and 
                word.isalpha() and 
                word not in self.stopwords and
                (word in self.tech_keywords or self._is_likely_tech_term(word))):
                found.add(word)
        
        return found
    
    def _is_likely_tech_term(self, word: str) -> bool:
        """Check if a word is likely a technical term"""
        # Check if word has common tech patterns
        tech_patterns = ['sql', 'api', 'sdk', 'cli', 'ide', 'orm', 'mvc', 'aws', 'gcp']
        if any(pattern in word for pattern in tech_patterns):
            return True
        
        # Check if it's an acronym (uppercase)
        if word.isupper() and len(word) >= 2:
            return True
            
        return False
    
    def _calculate_experience_score(self, resume: str, job: str) -> float:
        """Improved experience scoring"""
        score = 0
        
        # Check for years of experience (e.g., "2+ years", "3 years")
        import re
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        years_matches = re.findall(years_pattern, resume)
        if years_matches:
            # Sum up years mentioned
            total_years = sum(int(y) for y in years_matches)
            if total_years >= 2:
                score += 40  # Strong experience indicator
        
        # Count job positions/experience entries
        position_keywords = ['engineer', 'developer', 'intern', 'analyst', 'consultant', 'architect']
        positions = sum(1 for kw in position_keywords if kw in resume)
        score += min(positions * 15, 40)  # Up to 40 points for multiple positions
        
        # Check for experience-related action words
        exp_keywords = ['developed', 'built', 'implemented', 'designed', 'led', 'managed', 'created']
        actions = sum(1 for kw in exp_keywords if kw in resume)
        score += min(actions * 5, 20)  # Up to 20 points for action words
        
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

