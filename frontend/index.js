document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const statusDiv = document.getElementById("status");

  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // stop page reload

    // Show loader
    statusDiv.innerHTML = `<div class="loader"></div> Fetching results...`;

    const formData = new FormData();
    const questionsFile = document.getElementById("questions").files[0];
    const dataFile = document.getElementById("dataFile").files[0];
    const imageFile = document.getElementById("imageFile").files[0];

    // Validation
    if (!questionsFile) {
      statusDiv.innerHTML = "❌ Please upload a questions file.";
      return;
    }

    // Append files with field names matching backend
    formData.append("questions", questionsFile);
    if (dataFile) formData.append("data", dataFile);
    if (imageFile) formData.append("image", imageFile);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/", {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        throw new Error(`HTTP ${res.status} - ${res.statusText}`);
      }

      const result = await res.json();

      // Pretty-print the JSON response
      statusDiv.innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;

    } catch (err) {
      statusDiv.innerHTML = `<span style="color:red">❌ Error: ${err.message}</span>`;
    }
  });
});