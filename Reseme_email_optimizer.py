import streamlit as st
from openai import OpenAI
import docx2txt
import streamlit as st
import nltk
import ssl
from pyresparser import ResumeParser
import pdfplumber
import re
import secret
import side_by_side_compare
from ats_matric import ats_martic

if 'text' not in st.session_state:
    st.session_state.text = None
if 'optimized_text' not in st.session_state:
    st.session_state.optimized_text = None

# Fix SSL certificate issues for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

client = OpenAI(api_key= secret.sk) 


st.title("Resume Optimizer")
file_uploader = st.file_uploader("Upload your resume", type=["pdf", "docx"])
job_description= st.text_input("inter your job desription")

#email = st.text_input("Past your email: ")

def extract_text_from_each_file(file):
    if file.type == "application/pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = docx2txt.process(file)
        return text
    else:
        return None

def optimize_fun(text):
    user_prompt = f"Optimize the following resume for a job application:\n\n{text}\n\nMake it more professional and concise. Rewrite sentences to be ATS-friendly."
    sys_massage = "You are an expert resume optimizer. Your task is to enhance the resume content to make it more professional and ATS-friendly."
    response = client.chat.completions.create(model="gpt-4o-mini",
                                              messages=[
                                                  {"role":"system", "content": sys_massage},
                                                  {"role":"user", "content": user_prompt}
                                              ])
    return response.choices[0].message.content
def  display_sections(parsed_sections):
    # col1, col2 = st.columns([2, 1])
    # with col1:
    #     if "experience" in parsed_sections:
    #         st.subheader("Experience")
    #         st.write(parsed_sections["experience"])
    #     if "education" in parsed_sections:
    #         st.subheader("Education")
    #         st.write(parsed_sections["education"])
    #     if "skills" in parsed_sections:
    #         st.subheader('Skills')
    #         st.write(parsed_sections["skills"])
    #     if "certifications" in parsed_sections:
    #         st.subheader("Certifications")
    #         st.write(parsed_sections["certifications"])
    # with col2:
    #     if "contact" in parsed_sections:
    #         st.subheader("Contact")
    #         st.write (parsed_sections["contract"])
    # st.markdown("---")
    sections_order = ["title", "contact", "experience", "education", "skills", "certifications"]
    #st.markdown('</div>', unsafe_allow_html=True)

    # for s in sections_order:
    #     if s in parsed_sections and parsed_sections[s]:
    #         if s == "experience":
    #             st.subheader("Experience")
    #             st.write(parsed_sections["experience"])
    #         elif s == "education":
    #             st.subheader("Education")
    #             st.write(parsed_sections["education"])
    #         elif s == "skills":
    #             st.subheader("Skills")
    #             st.write(parsed_sections["skills"])

    #         elif s == "certifications":
    #             st.subheader("Certifications")
    #             st.write(parsed_sections["certifications"])
    #         elif s == "contact":
    #             st.subheader("Contact")
    #             st.write(parsed_sections["contact"])

    full_text =''
    for s in parsed_sections:
        full_text += f"{s.upper()}:\n{parsed_sections[s]}\n\n"
    return full_text
def parser_fun(text):   
    sections = {}
    current = "title"

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        lower_line = line.lower()
        if any(x in lower_line for x in ["experience"]):
            current = "experience"
        elif any(x in lower_line for x in ["education", "degree"]):
            current = "education"
        elif any(x in lower_line for x in ["skills", "competencies"]):
            current = "skills"
        elif any(x in lower_line for x in ["certifications", "awards"]):
            current = "certifications"
        elif any(x in lower_line for x in ["contact"]):
            current = "contact"
        else:
            if current not in sections:
                sections[current] = line
            else:
                sections[current] +="\n" + line
    return sections  


if st.button("Optimize Resume"):
    #my bad way
    #print(optimize_fun(extract_text_from_each_file(file_uploader)))
    # the correct way
    if file_uploader is not None:
        try:
            with st.spinner("Optimizing your resume..."):
                st.session_state.text = extract_text_from_each_file(file_uploader)
                if st.session_state.text:
                    st.session_state.optimized_text = optimize_fun(st.session_state.text)
                    parsed_sections = parser_fun(st.session_state.optimized_text)
                    full_text = display_sections(parsed_sections)

                    # display the opitmized resume
                    st.subheader("optimized resume")
                    st.text_area("Optimized Resume", 
                                 value=full_text,
                                  height=400)

                    # add download button
                    st.download_button(
                        label="Download optimized resume",
                        data=st.session_state.optimized_text,
                        file_name="optimized_resume.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        except Exception as e:
            st.error(f"An error occurred while optimizing the resume: {e}")
    else:
        st.warning("Please upload a resume file to optimize.")
# Side-by-side comparison function
if st.button("Compare Resumes"):
    if st.session_state.text and st.session_state.optimized_text:
        if st.session_state.text is not None and st.session_state.optimized_text is not None:
            side_by_side_compare.side_by_side_compare(st.session_state.text, 
                                                      st.session_state.optimized_text)
        else:
            st.warning("Please optimize your resume first before comparing.")

# ATS Metrics
# if st.button("Show ATS Metrics"):
#     if st.session_state.optimized_text and job_description:
#           # Added check for job_description
#         # Create instance
#         analyzer = ats_martic(st.session_state.optimized_text, job_description)
        
#         # Call methods
#         score = analyzer.calculate_ats_score()
#         analyzer.show()
        
#         # Show extracted keywords
#         keywords = analyzer.extract_keywords(job_description)
#         st.write("🔑 **Top Keywords from Job Description:**")
#         st.write(", ".join(keywords))
#         st.text("Note this ATS is for the optimized version")
        
#     elif not job_description:
#         st.warning("Please enter a job description first!")
#     else:
#         st.warning("Please optimize your resume first!")
############################################33
if st.button("Show ATS Metrics"):
    if st.session_state.text and st.session_state.optimized_text and job_description:
        # create instances fo both resmues
        original_analyzer = ats_martic(st.session_state.text, job_description)
        optimized_analyzer = ats_martic(st.session_state.optimized_text, job_description)

        # get scores
        original_score = original_analyzer.calculate_ats_score()
        optimized_score = optimized_analyzer.calculate_ats_score()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("original resume")
            st.write(f"ATS Score: {original_score}/100")
            st.progress(original_score/100)
        with col2:
            st.subheader("Optimized Resume")
            st.write(f"ATS Score: {optimized_score}/100")
            st.progress(optimized_score/100)
        #show imporvement
        st.markdown("---")
        improve = optimized_score - original_score
        if improve > 0:
            st.success(f"Improvement: +{improve}")
        elif improve < 0:
            st.warning(f"Score decreased: {improve}")
        else:
            st.info(" No change in ATS score")

        
    elif not job_description:
        st.warning("Please inter a job desribption first")
    else:
        st.warning("Please optimize your resume first")
