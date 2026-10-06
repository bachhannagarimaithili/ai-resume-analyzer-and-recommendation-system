
import streamlit as st
import pdfplumber

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Analyzer and Job Recommendation System")
st.write("Upload your resume to analyze skills and find suitable jobs.")

resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if resume is not None:
    try:
        with pdfplumber.open(resume) as pdf:
            resume_text = ""

            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"

        if not resume_text.strip():
            st.warning("No readable text found in this PDF.")
            st.stop()

        st.success("Resume text extracted successfully!")

        with st.expander("View Extracted Resume Text"):
            st.text_area("Resume Text", resume_text, height=250)

        # Detect skills
        skills_list = [
            "Python", "Java", "C++", "SQL", "HTML", "CSS",
            "JavaScript", "Machine Learning", "Data Analysis",
            "Excel", "Power BI", "Deep Learning",
            "Communication", "Problem Solving", "Git",
            "React", "APIs", "Django", "Flask", "Data Science",
            "Statistics", "Teamwork"
        ]

        resume_lower = resume_text.lower()

        detected_skills = [
            skill for skill in skills_list
            if skill.lower() in resume_lower
        ]

        st.header("Resume Skill Analysis")

        if detected_skills:
            st.success(f"Identified {len(detected_skills)} skills.")
            st.write(", ".join(detected_skills))
        else:
            st.warning("No matching skills detected.")

        # Sample job profiles
        jobs = [
            {
                "title": "Python Developer",
                "skills": ["Python", "Git", "SQL", "APIs"]
            },
            {
                "title": "Data Analyst",
                "skills": ["Python", "SQL", "Excel", "Power BI"]
            },
            {
                "title": "Machine Learning Engineer",
                "skills": [
                    "Python", "Machine Learning",
                    "SQL", "Deep Learning"
                ]
            },
            {
                "title": "Web Developer",
                "skills": ["HTML", "CSS", "JavaScript", "Git"]
            },
            {
                "title": "Software Developer",
                "skills": ["Python", "Java", "SQL", "Git"]
            },
            {
                "title": "Data Scientist",
                "skills": [
                    "Python", "Data Science",
                    "Statistics", "Machine Learning"
                    ]
            }
        ]

        # Match resume skills against job requirements
        detected_lower = {s.lower() for s in detected_skills}
        results = []

        for job in jobs:
            required = job["skills"]

            matched = [
                skill for skill in required
                if skill.lower() in detected_lower
            ]

            missing = [
                skill for skill in required
                if skill.lower() not in detected_lower
            ]

            score = round(len(matched) / len(required) * 100)

            results.append({
                "title": job["title"],
                "skills": matched,
                "missing": missing,
                "score": score
            })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        st.header("Job Recommendations")

        for job in results:
            with st.container(border=True):
                st.subheader(job["title"])
                st.write(f"Match score: {job['score']}%")
                st.progress(job["score"] / 100)

                st.write(
                    "Matching skills:",
                    ", ".join(job["skills"])
                    if job["skills"] else "None yet"
                )

                st.write(
                    "Skills to learn:",
                    ", ".join(job["missing"])
                    if job["missing"] else "None"
                )

        st.caption(
            "Scores compare your detected skills with sample job "
            "requirements. These are not live vacancies."
        )

    except Exception as error:
        st.error(f"Could not analyze the PDF: {error}")

else:
    st.info("Please upload a PDF resume to begin.")

