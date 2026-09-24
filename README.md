# ResumeIQ – AI Resume Analyzer

ResumeIQ is an AI-powered resume analysis web application that helps users evaluate and improve their resumes based on a target job description.

The application analyzes resumes for ATS compatibility, identifies matching and missing skills, evaluates resume sections, provides improvement suggestions, and uses a local LLM to generate personalized feedback and rewrite selected sections.

---

## 🚀 Features

### 📄 Resume Upload & Parsing
- Upload resumes in PDF or DOCX format.
- Extract resume text automatically.
- File type and size validation.
- Supports resumes up to 5 MB.

### 🎯 ATS Resume Analysis
- Calculates an ATS-style skill match score.
- Identifies skills present in the resume.
- Identifies skills required by the job description.
- Shows matched and missing skills.
- Categorizes detected skills.

### 📊 Resume Quality Analysis
Analyzes important resume sections including:

- Professional Summary
- Technical Skills
- Projects
- Experience
- Education
- Certifications

Each section contributes to an overall resume quality score.

### 🔍 Job Description Analysis
Extracts useful information from the job description, including:

- Job title
- Required experience
- Education requirements
- Required technical skills

### 💡 Improvement Suggestions
Provides rule-based recommendations based on the resume and target job description.

### 🤖 AI-Powered Feedback
Uses a locally running Ollama model to generate personalized resume feedback.

The project is currently configured to use:

`qwen3:0.6b`

The model can be changed through an environment variable without modifying the application code.

### ✍️ AI Section Rewriting
Users can improve supported resume sections using AI while preserving:

- Existing skills
- Technologies
- Responsibilities
- Dates
- Numbers
- Original meaning

The system is designed to avoid inventing information that is not present in the original resume.

### 📝 Full Resume Improvement
The application can analyze the complete resume and identify priority sections for improvement.

Currently supported priority sections include:

- Professional Summary
- Experience
- Projects

Technical Skills are intentionally not rewritten automatically to avoid introducing skills that are not actually present in the resume.

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- CSS
- Fetch API

### Backend
- Python
- FastAPI
- Pydantic
- PyMuPDF
- python-docx

### AI
- Ollama
- Qwen3

### Resume Analysis
- Python-based skill extraction
- Rule-based section detection
- ATS-style skill matching
- Resume quality analysis

### Development Tools
- Git
- GitHub
- VS Code
- Postman
- Swagger / OpenAPI

---

## 🏗️ Project Architecture

```text
AI-Resume-Analyzer/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── analysis.py
│   │   │
│   │   ├── core/
│   │   │   └── skills.py
│   │   │
│   │   ├── database/
│   │   │
│   │   ├── models/
│   │   │
│   │   ├── schemas/
│   │   │   └── analysis.py
│   │   │
│   │   ├── services/
│   │   │   ├── job_analyzer.py
│   │   │   ├── llm_service.py
│   │   │   ├── resume_analyzer.py
│   │   │   ├── resume_parser.py
│   │   │   ├── section_analyzer.py
│   │   │   ├── section_detector.py
│   │   │   └── skill_matcher.py
│   │   │
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── ResumeAnalyzer.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
