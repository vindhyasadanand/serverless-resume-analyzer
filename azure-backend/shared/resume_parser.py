"""
Resume Parser Module for Azure Functions
Extracts text and structured information from resume files (PDF, TXT, DOCX)
"""
import re
import fitz  # PyMuPDF
from docx import Document
from typing import Dict, List
import io


class ResumeParser:
    """Parses resumes and extracts structured information"""
    
    def __init__(self):
        # Common section headers
        self.section_keywords = {
            'education': ['education', 'academic', 'qualification', 'degree'],
            'experience': ['experience', 'employment', 'work history', 'professional experience'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
            'projects': ['projects', 'personal projects', 'academic projects'],
            'certifications': ['certifications', 'certificates', 'licenses']
        }
        
        # Common programming languages and technologies
        self.tech_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'data science',
            'html', 'css', 'rest', 'api', 'graphql', 'microservices', 'agile', 'scrum'
        ]
    
    def parse_resume_from_bytes(self, file_bytes: bytes, filename: str) -> Dict:
        """
        Parse resume from bytes
        Returns structured data including text, skills, education, experience
        """
        # Extract text based on file extension
        ext = filename.lower().split('.')[-1]
        text = self._extract_text_from_bytes(file_bytes, ext)
        
        # Extract structured information
        skills = self._extract_skills(text)
        education = self._extract_education(text)
        experience = self._extract_experience(text)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        
        return {
            'raw_text': text,
            'skills': skills,
            'education': education,
            'experience': experience,
            'contact': {
                'email': email,
                'phone': phone
            },
            'sections': self._identify_sections(text)
        }
    
    def _extract_text_from_bytes(self, file_bytes: bytes, ext: str) -> str:
        """Extract text from bytes based on file extension"""
        if ext == 'pdf':
            return self._extract_from_pdf_bytes(file_bytes)
        elif ext == 'docx':
            return self._extract_from_docx_bytes(file_bytes)
        elif ext == 'txt':
            return file_bytes.decode('utf-8', errors='ignore')
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _extract_from_pdf_bytes(self, file_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        text = ""
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")
        return text
    
    def _extract_from_docx_bytes(self, file_bytes: bytes) -> str:
        """Extract text from DOCX bytes"""
        try:
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")
        return text
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.tech_keywords:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        # Also look for skills in a dedicated skills section
        skills_section = self._extract_section(text, 'skills')
        if skills_section:
            additional_skills = re.findall(r'[A-Za-z][A-Za-z0-9+#.\s]+', skills_section)
            found_skills.extend([s.strip() for s in additional_skills if len(s.strip()) > 2])
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(found_skills))
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_section = self._extract_section(text, 'education')
        
        degrees = []
        degree_patterns = [
            r'(Bachelor|B\.S\.|B\.A\.|BS|BA|B\.Tech|B\.E\.).*',
            r'(Master|M\.S\.|M\.A\.|MS|MA|M\.Tech|MBA).*',
            r'(Ph\.?D\.?|Doctorate).*',
            r'(Associate|A\.S\.|A\.A\.).*'
        ]
        
        section_to_search = education_section if education_section else text
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, section_to_search, re.IGNORECASE)
            degrees.extend([m if isinstance(m, str) else m[0] for m in matches])
        
        return list(set(degrees))
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience information"""
        experience_section = self._extract_section(text, 'experience')
        
        if not experience_section:
            return []
        
        experience_entries = re.findall(
            r'((?:19|20)\d{2}[\s\-–]+(?:(?:19|20)\d{2}|Present|Current)).*',
            experience_section,
            re.IGNORECASE
        )
        
        return experience_entries[:5]
    
    def _extract_section(self, text: str, section_type: str) -> str:
        """Extract a specific section from resume"""
        keywords = self.section_keywords.get(section_type, [])
        
        for keyword in keywords:
            pattern = rf'(?i){keyword}\s*:?\s*\n(.*?)(?=\n[A-Z][a-z]+\s*:?\s*\n|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _identify_sections(self, text: str) -> Dict[str, bool]:
        """Identify which sections are present in the resume"""
        sections_found = {}
        text_lower = text.lower()
        
        for section_name, keywords in self.section_keywords.items():
            sections_found[section_name] = any(
                keyword in text_lower for keyword in keywords
            )
        
        return sections_found
    
    def _extract_email(self, text: str) -> str:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number"""
        phone_patterns = [
            r'\+?1?\s*\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})',
            r'\+?\d{1,3}[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                if isinstance(matches[0], tuple):
                    return '-'.join(matches[0])
                return matches[0]
        
        return ""






