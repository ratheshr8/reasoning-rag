const noticeEl = document.getElementById("provider-notice");
const sampleSelect = document.getElementById("sample-id");
const uploadLimits = document.getElementById("upload-limits");
const form = document.getElementById("ask-form");
const errorEl = document.getElementById("error");
const resultPanel = document.getElementById("result-panel");
const answerText = document.getElementById("answer-text");
const citationsEl = document.getElementById("citations");
const conflictsEl = document.getElementById("conflicts");
const traceSummaryEl = document.getElementById("trace-summary");
const rawJsonEl = document.getElementById("raw-json");

function showError(message) {
  errorEl.hidden = !message;
  errorEl.textContent = message || "";
}

async function loadSamples() {
  const response = await fetch("/api/samples");
  if (!response.ok) {
    throw new Error("Failed to load samples");
  }
  const data = await response.json();
  noticeEl.textContent = data.provider_notice.message;
  uploadLimits.textContent = `Upload limit: ${data.max_upload_bytes} bytes. Markdown only (.md, .markdown).`;
  sampleSelect.innerHTML = "";
  for (const sample of data.samples) {
    const option = document.createElement("option");
    option.value = sample.id;
    option.textContent = `${sample.title} (${sample.access_classification})`;
    sampleSelect.appendChild(option);
  }
  if (!data.samples.length) {
    showError("No sample documents found. Run the demo from the repository root.");
  }
}

function renderResult(payload) {
  const result = payload.result;
  resultPanel.hidden = false;
  if (result.answer.abstained) {
    answerText.textContent = `ABSTAIN: ${result.answer.abstention_reason || "not enough evidence"}`;
  } else {
    answerText.textContent = result.answer.text;
  }

  citationsEl.innerHTML = "";
  for (const link of result.answer.claim_links || []) {
    const div = document.createElement("div");
    div.className = "cite";
    div.textContent = `Claim: ${link.claim} → ${link.evidence_ids.join(", ")}`;
    citationsEl.appendChild(div);
  }

  conflictsEl.innerHTML = "";
  const conflicts = result.verification?.conflicts || [];
  for (const conflict of conflicts) {
    const div = document.createElement("div");
    div.className = "conflict";
    div.textContent = `Conflict (${conflict.topic}): ${conflict.values.join(", ")}`;
    conflictsEl.appendChild(div);
  }

  const summary = payload.trace_summary;
  traceSummaryEl.textContent = JSON.stringify(summary, null, 2);
  rawJsonEl.textContent = JSON.stringify(payload, null, 2);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("");
  const button = form.querySelector("button");
  button.disabled = true;
  try {
    const question = document.getElementById("question").value.trim();
    const mode = document.getElementById("mode").value;
    const fileInput = document.getElementById("upload");
    let response;
    if (fileInput.files && fileInput.files[0]) {
      const body = new FormData();
      body.append("question", question);
      body.append("retrieval_mode", mode);
      body.append("synthetic", "true");
      body.append("file", fileInput.files[0]);
      response = await fetch("/api/ask/upload", { method: "POST", body });
    } else {
      response = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          sample_id: sampleSelect.value,
          retrieval_mode: mode,
          synthetic: true,
        }),
      });
    }
    const payload = await response.json();
    if (!response.ok) {
      const detail = payload.detail;
      const message =
        typeof detail === "object" && detail?.error
          ? `${detail.code || "error"}: ${detail.error}`
          : payload.error || response.statusText;
      throw new Error(message);
    }
    renderResult(payload);
  } catch (err) {
    showError(err.message || String(err));
  } finally {
    button.disabled = false;
  }
});

loadSamples().catch((err) => showError(err.message || String(err)));
