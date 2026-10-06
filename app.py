
import streamlit as st
import pdfplumber

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f3f7ff, #e5efff);
    color: #1e293b;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    color: #123b75 !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #174a8b !important;
    font-weight: 700 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff;
    border: 1px solid #d7e5ff;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 4px 14px rgba(30, 64, 175, 0.06);
}

.stButton > button {
    background: #2563eb;
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
}

div[data-testid="stFileUploader"] {
    background: white;
    border: 1px dashed #93b4f5;
    border-radius: 14px;
    padding: 14px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid #d7e5ff;
    border-radius: 12px;
}

hr {
    border-color: #d7e5ff;
}
<style>
    /* Your existing CSS stays here */

    .section-title {
        color: #174ea6;
        font-size: 2rem;
        font-weight: 750;
        padding-bottom: 10px;
        margin-top: 28px;
        border-bottom: 3px solid #dbeafe;
    }
    /* Professional job recommendation cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid #cbdcf5;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 4px 12px rgba(30, 64, 175, 0.06);
}

/* Blue progress indicators */
div[data-testid="stProgress"] > div > div {
    background-color: #2563eb;
}div[data-testid="stProgress"] > div > div {
    background-color: #2563eb;
}
div[data-testid="stProgress"] [data-testid="stProgressBar"] {
    background-color: #2563eb;
    border-radius: 10px;
    overflow: hidden;
}
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    h1 {
        color: #172554;
        font-weight: 800;
    }

    h2, h3 {
        color: #1e3a8a;
    }

    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    div[data-testid="stFileUploader"] {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #dbeafe;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

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

        st.markdown('<h2 class="section-title">📊 Resume Skill Analysis</h2>', unsafe_allow_html=True)

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

        st.markdown('<h2 class="section-title">💼 Job Recommendations</h2>', unsafe_allow_html=True)

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

