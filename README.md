Resume Optimizer
A Streamlit-based web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and improve their chances of getting noticed by recruiters.

Features
🔧 Core Functionality
Resume Upload: Support for PDF and DOCX file formats

AI-Powered Optimization: Uses OpenAI's GPT-4 to enhance resume content

ATS-Friendly Formatting: Rewrites content to be more compatible with Applicant Tracking Systems

Section Parsing: Automatically identifies and organizes resume sections (Experience, Education, Skills, etc.)

📊 Analysis Tools
Side-by-Side Comparison: Compare original and optimized resumes

ATS Metrics: Calculate ATS compatibility scores for both versions

Improvement Tracking: See how much your resume score improves after optimization

💾 Export Options
Download optimized resume as text file

Clean, professional formatting

Installation
Clone the repository:

bash
git clone <repository-url>
cd resume-optimizer
Install required dependencies:

bash
pip install streamlit openai nltk docx2txt pyresparser pdfplumber
Download NLTK data:

python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
Set up your OpenAI API key:

Create a secret.py file in your project directory

Add your API key: sk = "your-openai-api-key-here"

Usage
Start the application:

bash
streamlit run Reseme_email_optimizer.py
Upload your resume:

Click "Browse files" to upload your PDF or DOCX resume

Supported formats: PDF, DOCX

Enter job description:

Paste the job description you're applying for in the text input field

Optimize your resume:

Click "Optimize Resume" to generate an improved version

View the optimized content in the text area

Download the optimized version using the download button

Compare versions:

Click "Compare Resumes" to see original vs optimized side-by-side

Check ATS metrics:

Click "Show ATS Metrics" to see compatibility scores for both versions

Track your improvement with visual progress bars

File Structure
text
resume-optimizer/
├── Reseme_email_optimizer.py  # Main application file
├── secret.py                  # API keys (create this file)
├── side_by_side_compare.py    # Comparison functionality
├── ats_matric.py             # ATS scoring functionality
└── README.md                 # This file
Dependencies
streamlit: Web application framework

openai: GPT-4 integration for resume optimization

nltk: Natural language processing for text analysis

docx2txt: DOCX file text extraction

pyresparser: Resume parsing and analysis

pdfplumber: PDF file text extraction

How It Works
Text Extraction: Converts uploaded resumes (PDF/DOCX) into plain text

Section Parsing: Identifies and categorizes resume sections (Experience, Education, Skills, etc.)

AI Optimization: Uses GPT-4 to rewrite content for professionalism and ATS compatibility

ATS Scoring: Analyzes keyword matching and format compatibility

Visual Comparison: Provides side-by-side analysis of improvements

Tips for Best Results
Upload resumes with clear section headings

Ensure your original resume is in a readable format

Provide a detailed job description for more accurate optimization

Review the optimized content before downloading

Privacy & Security
Your resume data is processed through OpenAI's API

No data is stored permanently on the server

Always review the optimized content for personal information before sharing
