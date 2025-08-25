import streamlit as st

import re
class ats_martic:
    def __init__(self, resume_text, job_description):
        self.resume_text = resume_text
        self.job_description = job_description
    
    def extract_keywords(self, text):  # Added self
        """Extract important keywords from text by removing stop words and common words"""
        stop_words = set(['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'a', 'an', 'of'])
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return [word for word in words if word not in stop_words][:20]
    
    def calculate_keyword_score(self):  # Added self, removed parameters
        if not self.job_description:
            return 20
        
        job_keywords = self.extract_keywords(self.job_description)  # Use self
        matches = 0
        for keyword in job_keywords:
            if keyword.lower() in self.resume_text.lower():  # Use self
                matches += 1
        
        match_percentage = (matches / len(job_keywords)) * 100
        return min(40, match_percentage * 0.4)
    
    def check_formatting(self):  # Added self, removed parameter
        score = 30
        if "table" in self.resume_text.lower():  # Use self
            score -= 10
        if "column" in self.resume_text.lower():  # Use self
            score -= 5
        
        word_count = len(self.resume_text.split())  # Use self
        if word_count < 300:
            score -= 5
        elif word_count > 800:
            score -= 5
        
        return max(0, score)
    
    def check_completeness(self):  # Added self, removed parameter
        score = 0
        text_lower = self.resume_text.lower()  # Use self
        
        if "experience" in text_lower or "work" in text_lower:
            score += 5
        if "education" in text_lower:
            score += 5
        if "skill" in text_lower:
            score += 5
        if "contact" in text_lower or "@" in text_lower:
            score += 5
        
        return score
    
    def check_readability(self):  # Added self, removed parameter
        sentences = self.resume_text.count('.') + self.resume_text.count('!') + self.resume_text.count('?')  # Use self
        words = len(self.resume_text.split())  # Use self
        
        if sentences == 0:
            return 0
        
        avg_sentence_length = words / sentences
        
        if avg_sentence_length < 20:
            return 10
        elif avg_sentence_length < 30:
            return 7
        else:
            return 3
    
    # ADD THIS MISSING METHOD:
    def calculate_ats_score(self):
        """Calculate total ATS score"""
        keyword_score = self.calculate_keyword_score()
        formatting_score = self.check_formatting()
        completeness_score = self.check_completeness()
        readability_score = self.check_readability()
        
        return keyword_score + formatting_score + completeness_score + readability_score
    
    def show(self):  # Added self, removed parameters
        ats_score = self.calculate_ats_score()  # Use self

        keyword_score = self.calculate_keyword_score()
        formatting_score = self.check_formatting()
        completeness_score = self.check_completeness()
        readability_score = self.check_readability()
        st.write(f"📊 ATS Score: {ats_score}/100")


        if ats_score >= 80:
            progress_color = "green"
        elif ats_score >= 60:
            progress_color = "orange"
        else:
            progress_color = 'red'

        st.progress(ats_score/100, text=f'{ats_score}% ATS compatible')
        metrics = [
        {"name": "🔑 Keyword Match", "score": keyword_score, "max": 40, "color": "blue"},
        {"name": "🎨 Formatting", "score": formatting_score, "max": 30, "color": "purple"},
        {"name": "📋 Completeness", "score": completeness_score, "max": 20, "color": "teal"},
        {"name": "📖 Readability", "score": readability_score, "max": 10, "color": "pink"}
    ]
        for metric in metrics:
            st.write(f"{metric["name"]}:")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"{metric['score']}/{metric["max"]}")
            with col2:
                st.progress(metric["score"]/metric["max"])
        
        st.write("💡 Recommendations:")
        if keyword_score < 20:
            st.info("• Add more keywords from the job description")
        if formatting_score < 20:
            st.info("• Simplify formatting, avoid tables and columns")
        if completeness_score < 10:
            st.info("• Add missing sections (Experience, Education, Skills)")
        if readability_score < 5:
            st.info("• Use shorter sentences and bullet points")