import os
import docx2txt
import PyPDF2

# List of common LinkedIn sections
LINKEDIN_SECTIONS = [
    "About", "Experience", "Education", "Skills", "Licenses & Certifications", "Volunteer Experience", "Projects", "Honors & Awards", "Languages", "Interests"
]

# Example keywords for optimization (customize as needed)
KEYWORDS = ["Python", "Machine Learning", "Data Analysis", "Project Management", "Leadership", "Communication", "SQL", "Java", "AWS", "Teamwork"]

def extract_text_from_linkedin_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif ext in [".docx", ".doc"]:
        text = docx2txt.process(file_path) or ""
    else:
        raise ValueError("Unsupported file type: {}".format(ext))
    return text

def analyze_linkedin_profile(text):
    results = {}
    lower_text = text.lower()
    # Section completeness
    missing_sections = []
    for section in LINKEDIN_SECTIONS:
        if section.lower() not in lower_text:
            missing_sections.append(section)
    results["missing_sections"] = missing_sections
    # Keyword optimization
    keyword_counts = {}
    for kw in KEYWORDS:
        count = lower_text.count(kw.lower())
        keyword_counts[kw] = count
    results["keyword_counts"] = keyword_counts
    # Suggestions
    suggestions = []
    if missing_sections:
        suggestions.append(f"Add missing sections: {', '.join(missing_sections)}.")
    low_keywords = [kw for kw, c in keyword_counts.items() if c == 0]
    if low_keywords:
        suggestions.append(f"Consider adding these keywords: {', '.join(low_keywords)}.")
    results["suggestions"] = suggestions
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python linkedin_profile_analyzer.py <linkedin_profile.pdf|docx>")
        sys.exit(1)
    file_path = sys.argv[1]
    text = extract_text_from_linkedin_file(file_path)
    analysis = analyze_linkedin_profile(text)
    print("Analysis Results:")
    print(analysis)
