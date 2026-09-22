const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, options);

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error("Invalid response from server.");
  }

  if (!response.ok) {
    throw new Error(
      data.detail || data.message || "Request failed."
    );
  }

  return data;
}

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/api/upload-resume", {
    method: "POST",
    body: formData,
  });
}

export async function analyzeResume(resumeText, jobDescription) {
  return request("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  });
}

export async function rewriteSection(sectionName, content) {
  return request("/api/rewrite-section", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      section_name: sectionName,
      content,
    }),
  });
}

export async function improveResume(resumeText, jobDescription) {
  return request("/api/improve-resume", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  });
}