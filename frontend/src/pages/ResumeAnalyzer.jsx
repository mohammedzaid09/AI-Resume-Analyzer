import { useState } from "react";
import {
  uploadResume,
  analyzeResume,
  rewriteSection,
  improveResume,
} from "../services/api";

const SECTION_HEADERS = [
  "PROFESSIONAL SUMMARY",
  "EDUCATION",
  "EXPERIENCE",
  "PROJECTS",
  "TECHNICAL SKILLS",
  "RELEVANT COURSEWORK",
  "CERTIFICATIONS & ACHIEVEMENTS",
];

const SECTION_MAP = {
  professional_summary: "PROFESSIONAL SUMMARY",
  education: "EDUCATION",
  experience: "EXPERIENCE",
  projects: "PROJECTS",
  technical_skills: "TECHNICAL SKILLS",
  relevant_coursework: "RELEVANT COURSEWORK",
  certifications: "CERTIFICATIONS & ACHIEVEMENTS",
};

function getSectionContent(resumeText, sectionName) {
  const header = SECTION_MAP[sectionName];

  if (!header) return "";

  const start = resumeText.indexOf(header);

  if (start === -1) return "";

  const contentStart = start + header.length;

  const remainingText = resumeText.slice(contentStart);

  const nextHeaderPositions = SECTION_HEADERS
    .map((nextHeader) => remainingText.indexOf(nextHeader))
    .filter((position) => position !== -1);

  const end =
    nextHeaderPositions.length > 0
      ? Math.min(...nextHeaderPositions)
      : remainingText.length;

  return remainingText.slice(0, end).trim();
}

function formatSectionName(sectionName) {
  return sectionName
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function ResumeAnalyzer() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [result, setResult] = useState(null);

  const [rewrittenSections, setRewrittenSections] = useState({});
  const [rewritingSection, setRewritingSection] = useState("");

  const [improvedResume, setImprovedResume] = useState(null);
  const [improvingResume, setImprovingResume] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    const fileName = selectedFile.name.toLowerCase();

    if (
      !fileName.endsWith(".pdf") &&
      !fileName.endsWith(".docx")
    ) {
      setError("Please upload a PDF or DOCX resume.");
      setFile(null);
      return;
    }

    setError("");
    setFile(selectedFile);
    setResumeText("");
    setResult(null);
    setRewrittenSections({});
    setImprovedResume(null);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please upload your resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter the job description.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);
      setRewrittenSections({});
      setImprovedResume(null);

      const uploadResult = await uploadResume(file);
      const extractedText = uploadResult.resume_text;

      if (!extractedText) {
        throw new Error("Could not extract text from the resume.");
      }

      setResumeText(extractedText);

      const analysisResult = await analyzeResume(
        extractedText,
        jobDescription
      );

      setResult(analysisResult);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const handleRewriteSection = async (sectionName) => {
    if (!resumeText) {
      setError("Resume content is not available.");
      return;
    }

    const sectionContent = getSectionContent(
      resumeText,
      sectionName
    );

    if (!sectionContent) {
      setError(
        `Could not find the ${formatSectionName(
          sectionName
        )} section in the resume.`
      );
      return;
    }

    try {
      setRewritingSection(sectionName);
      setError("");

      const response = await rewriteSection(
        sectionName,
        sectionContent
      );

      if (!response?.improved_content) {
        throw new Error("No improved content was returned.");
      }

      setRewrittenSections((previous) => ({
        ...previous,
        [sectionName]: response.improved_content,
      }));
    } catch (err) {
      setError(
        err.message || "Failed to rewrite the section."
      );
    } finally {
      setRewritingSection("");
    }
  };

  const handleImproveResume = async () => {
    if (!resumeText || !jobDescription.trim()) {
      setError(
        "Please analyze your resume and enter a job description first."
      );
      return;
    }

    try {
      setImprovingResume(true);
      setError("");
      setImprovedResume(null);

      const data = await improveResume(
        resumeText,
        jobDescription
      );

      if (!data?.success) {
        throw new Error(
          "Could not improve the resume."
        );
      }

      setImprovedResume(data);
    } catch (err) {
      setError(
        err.message || "Failed to improve the resume."
      );
    } finally {
      setImprovingResume(false);
    }
  };

  const scores = result?.scores;
  const skills = result?.skill_analysis;
  const sections = result?.section_analysis;
  const job = result?.job_analysis;

  return (
    <main className="resume-analyzer">
      <header className="header">
        <h1>AI Resume Analyzer</h1>

        <p>
          Analyze your resume against a job description
          and identify areas for improvement.
        </p>
      </header>

      <div className="container">
        <section className="card">
          <h2>Upload Resume</h2>

          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
          />

          {file && (
            <p className="file-name">
              {file.name}
            </p>
          )}
        </section>

        <section className="card">
          <h2>Job Description</h2>

          <textarea
            value={jobDescription}
            onChange={(event) =>
              setJobDescription(event.target.value)
            }
            placeholder="Paste the job description here..."
            rows={10}
          />
        </section>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        <div className="resume-actions">
          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Resume"}
          </button>

          <button
            className="improve-resume-button"
            onClick={handleImproveResume}
            disabled={
              improvingResume ||
              !resumeText ||
              !jobDescription.trim()
            }
          >
            {improvingResume
              ? "Improving Resume..."
              : "Improve Full Resume"}
          </button>
        </div>

        {result && (
          <section className="results">

            {/* Analysis Results */}
            <div className="card">
              <h2>Analysis Results</h2>

              <div className="scores">
                <div className="score">
                  <span>ATS Score</span>

                  <strong>
                    {scores?.ats_score ?? 0}
                  </strong>

                  <small>/100</small>
                </div>

                <div className="score">
                  <span>Resume Quality</span>

                  <strong>
                    {scores?.resume_quality_score ?? 0}
                  </strong>

                  <small>/100</small>
                </div>

                <div className="score">
                  <span>Skill Match</span>

                  <strong>
                    {skills?.match_percentage ?? 0}
                  </strong>

                  <small>%</small>
                </div>
              </div>
            </div>

            {/* Full Resume Improvements */}
            {improvedResume && (
              <div className="card">
                <h2>Full Resume Improvements</h2>

                {improvedResume.missing_skills?.length > 0 && (
                  <>
                    <h3>Missing Skills</h3>

                    <div className="skills">
                      {improvedResume.missing_skills.map(
                        (skill) => (
                          <span
                            className="skill missing"
                            key={skill}
                          >
                            {skill}
                          </span>
                        )
                      )}
                    </div>
                  </>
                )}

                {improvedResume.missing_sections?.length > 0 && (
                  <>
                    <h3>Missing Sections</h3>

                    <div className="skills">
                      {improvedResume.missing_sections.map(
                        (section) => (
                          <span
                            className="skill missing"
                            key={section}
                          >
                            {formatSectionName(section)}
                          </span>
                        )
                      )}
                    </div>
                  </>
                )}

                {improvedResume.sections_improved?.length > 0 && (
                  <>
                    <h3>Improved Sections</h3>

                    {improvedResume.sections_improved.map(
                      (section) => (
                        <div
                          className="improved-resume-section"
                          key={section.section_name}
                        >
                          <h4>
                            {formatSectionName(
                              section.section_name
                            )}
                          </h4>

                          <div className="original-content">
                            <strong>Original</strong>

                            <p>
                              {section.original_content}
                            </p>
                          </div>

                          <div className="improved-content">
                            <strong>Improved</strong>

                            <p>
                              {section.improved_content}
                            </p>
                          </div>
                        </div>
                      )
                    )}
                  </>
                )}

                {improvedResume.suggestions?.length > 0 && (
                  <>
                    <h3>Suggestions</h3>

                    <ol>
                      {improvedResume.suggestions.map(
                        (suggestion, index) => (
                          <li key={index}>
                            {suggestion}
                          </li>
                        )
                      )}
                    </ol>
                  </>
                )}

                {!improvedResume.sections_improved?.length &&
                  !improvedResume.missing_skills?.length &&
                  !improvedResume.missing_sections?.length &&
                  !improvedResume.suggestions?.length && (
                    <p>
                      No additional improvements were identified.
                    </p>
                  )}
              </div>
            )}

            {/* Job Analysis */}
            {job && (
              <div className="card">
                <h2>Job Analysis</h2>

                <p>
                  <strong>Target Role:</strong>{" "}
                  {job.job_title || "Not specified"}
                </p>

                {job.experience_requirement && (
                  <p>
                    <strong>Experience:</strong>{" "}
                    {job.experience_requirement}
                  </p>
                )}

                {job.education_requirement && (
                  <p>
                    <strong>Education:</strong>{" "}
                    {job.education_requirement}
                  </p>
                )}
              </div>
            )}

            {/* Skill Analysis */}
            <div className="card">
              <h2>Skill Analysis</h2>

              <h3>Matched Skills</h3>

              <div className="skills">
                {skills?.matched?.length ? (
                  skills.matched.map((skill) => (
                    <span
                      className="skill matched"
                      key={skill}
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <p>None</p>
                )}
              </div>

              <h3>Missing Skills</h3>

              <div className="skills">
                {skills?.missing?.length ? (
                  skills.missing.map((skill) => (
                    <span
                      className="skill missing"
                      key={skill}
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <p>None</p>
                )}
              </div>
            </div>

            {/* Section Analysis */}
            {sections?.analysis && (
              <div className="card">
                <h2>Section Analysis</h2>

                {Object.entries(sections.analysis).map(
                  ([sectionName, section]) => (
                    <div
                      className="section-item"
                      key={sectionName}
                    >
                      <h3>
                        {formatSectionName(sectionName)}
                      </h3>

                      <p>
                        <strong>Status:</strong>{" "}
                        {section.status}
                      </p>

                      <p>
                        <strong>Score:</strong>{" "}
                        {section.score}/100
                      </p>

                      {section.feedback?.length > 0 && (
                        <ul>
                          {section.feedback.map(
                            (feedback, index) => (
                              <li key={index}>
                                {feedback}
                              </li>
                            )
                          )}
                        </ul>
                      )}

                      {resumeText &&
                        section.status === "present" &&
                        SECTION_MAP[sectionName] && (
                          <button
                            className="rewrite-button"
                            onClick={() =>
                              handleRewriteSection(
                                sectionName
                              )
                            }
                            disabled={
                              rewritingSection ===
                              sectionName
                            }
                          >
                            {rewritingSection ===
                            sectionName
                              ? "Improving..."
                              : "Improve Section"}
                          </button>
                        )}

                      {rewrittenSections[sectionName] && (
                        <div className="rewritten-content">
                          <h4>Improved Version</h4>

                          <p>
                            {rewrittenSections[sectionName]}
                          </p>
                        </div>
                      )}
                    </div>
                  )
                )}
              </div>
            )}

            {/* Missing Sections */}
            {sections?.missing_sections?.length > 0 && (
              <div className="card">
                <h2>Missing Sections</h2>

                <div className="skills">
                  {sections.missing_sections.map(
                    (section) => (
                      <span
                        className="skill missing"
                        key={section}
                      >
                        {formatSectionName(section)}
                      </span>
                    )
                  )}
                </div>
              </div>
            )}

            {/* Improvement Suggestions */}
            {result.improvement_suggestions?.length > 0 && (
              <div className="card">
                <h2>Improvement Suggestions</h2>

                <ol>
                  {result.improvement_suggestions.map(
                    (suggestion, index) => (
                      <li key={index}>
                        {suggestion}
                      </li>
                    )
                  )}
                </ol>
              </div>
            )}

            {/* AI Feedback */}
            {result.ai_feedback && (
              <div className="card">
                <h2>AI Feedback</h2>

                {result.ai_feedback
                  .split("\n")
                  .filter(Boolean)
                  .map((feedback, index) => (
                    <p key={index}>
                      {feedback.replace(
                        /^-\s*/,
                        ""
                      )}
                    </p>
                  ))}
              </div>
            )}

          </section>
        )}
      </div>
    </main>
  );
}

export default ResumeAnalyzer;