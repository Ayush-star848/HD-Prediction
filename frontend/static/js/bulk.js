/* ============================================================
   CardioSense AI v2 — bulk.js
   Handles: file drop/browse, CSV upload, results rendering
   ============================================================ */

"use strict";

let _selectedFile = null;
let _allResults   = [];

/* ── File handling ──────────────────────────────────────────── */
function handleDrop(e) {
  e.preventDefault();
  document.getElementById("dropZone").classList.remove("dragging");
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
}

function handleFile(file) {
  if (!file) return;
  if (!file.name.endsWith(".csv")) {
    showBulkError("Please upload a .csv file.");
    return;
  }
  _selectedFile = file;
  document.getElementById("dzSelected").style.display = "flex";
  document.getElementById("dz-inner") && (document.querySelector(".dz-inner").style.display = "none");
  document.getElementById("dzFileName").textContent = file.name;
  document.getElementById("dzFileSize").textContent = formatBytes(file.size);
  document.getElementById("btnBulk").disabled = false;
  hideBulkError();
}

function clearFile() {
  _selectedFile = null;
  document.getElementById("dzSelected").style.display = "none";
  document.querySelector(".dz-inner").style.display    = "block";
  document.getElementById("csvFile").value             = "";
  document.getElementById("btnBulk").disabled          = true;
  document.getElementById("bulkResults").style.display = "none";
  hideBulkError();
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / 1024 / 1024).toFixed(2) + " MB";
}

/* ── Upload & analyse ───────────────────────────────────────── */
async function runBulkAnalysis() {
  if (!_selectedFile) return;
  hideBulkError();

  document.getElementById("bulkResults").style.display = "none";
  document.getElementById("loading").style.display      = "flex";
  document.getElementById("btnBulk").disabled           = true;

  const el = document.getElementById("loadingStep");
  if (el) el.textContent = "Processing all patient records with Voting Ensemble…";

  const formData = new FormData();
  formData.append("file", _selectedFile);

  try {
    const res  = await fetch("/api/bulk", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok || !data.success) {
      showBulkError(data.error || "Bulk analysis failed.");
      return;
    }

    _allResults = data.results || [];
    renderBulkResults(data);
  } catch (err) {
    showBulkError(`Network error: ${err.message}`);
  } finally {
    document.getElementById("loading").style.display  = "none";
    document.getElementById("btnBulk").disabled       = false;
  }
}

/* ── Render bulk results ────────────────────────────────────── */
function renderBulkResults(data) {
  const total = data.total_patients;

  /* Stats */
  const stats = [
    { val: total,                  label: "Total Patients",   cls: "total" },
    { val: data.positive_cases,    label: "Positive Cases",   cls: "pos" },
    { val: data.negative_cases,    label: "Negative Cases",   cls: "low" },
    { val: data.high_risk,         label: "High Risk",        cls: "high" },
    { val: data.medium_risk,       label: "Moderate Risk",    cls: "medium" },
    { val: data.low_risk,          label: "Low Risk",         cls: "low" },
    { val: data.avg_probability + "%", label: "Avg Risk Score", cls: "pos" },
  ];

  const sg = document.getElementById("statsGrid");
  sg.innerHTML = "";
  stats.forEach(s => {
    const d = document.createElement("div");
    d.className = "bstat";
    d.innerHTML = `<span class="bstat-val ${s.cls}">${s.val}</span><span class="bstat-lbl">${s.label}</span>`;
    sg.appendChild(d);
  });

  /* Risk bars */
  document.getElementById("modelUsedBadge").textContent = data.model_used || "Voting Ensemble";
  setTimeout(() => {
    ["High","Med","Low"].forEach(t => {
      const key  = t === "High" ? "high_risk" : t === "Med" ? "medium_risk" : "low_risk";
      const barId = "bar" + t;
      const cntId = "cnt" + t;
      const pct  = total > 0 ? Math.round(data[key] / total * 100) : 0;
      document.getElementById(barId).style.width = pct + "%";
      document.getElementById(cntId).textContent = `${data[key]} (${pct}%)`;
    });
  }, 200);

  /* Table */
  renderTable(data.results);

  document.getElementById("bulkResults").style.display = "block";
  document.getElementById("bulkResults").scrollIntoView({ behavior: "smooth" });
}

function renderTable(results) {
  const tbody = document.getElementById("resultsBody");
  tbody.innerHTML = "";
  results.forEach(r => {
    if (r.error) return;
    const tr = document.createElement("tr");
    tr.dataset.tier = r.risk_tier;
    tr.dataset.id   = r.patient_id;
    const sex = r.inputs?.sex == 1 ? "Male" : "Female";
    const tierHtml = `<span class="tier-badge ${r.risk_tier}">${r.risk_tier.charAt(0).toUpperCase() + r.risk_tier.slice(1)}</span>`;
    const predHtml = r.prediction === 1
      ? `<span class="pred-pos">Positive</span>`
      : `<span class="pred-neg">Negative</span>`;
    tr.innerHTML = `
      <td>${r.patient_id}</td>
      <td>${r.inputs?.age ?? "—"}</td>
      <td>${sex}</td>
      <td>${r.inputs?.trestbps ?? "—"}</td>
      <td>${r.inputs?.chol ?? "—"}</td>
      <td>${r.probability}%</td>
      <td>${tierHtml}</td>
      <td>${predHtml}</td>`;
    tbody.appendChild(tr);
  });
}

/* ── Filter table ───────────────────────────────────────────── */
function filterTable() {
  const search = (document.getElementById("tableSearch")?.value || "").toLowerCase();
  const tier   = document.getElementById("tierFilter")?.value || "";
  const rows   = document.querySelectorAll("#resultsBody tr");
  rows.forEach(row => {
    const rowTier = row.dataset.tier || "";
    const rowId   = row.dataset.id   || "";
    const tierOk  = !tier || rowTier === tier;
    const searchOk = !search || row.textContent.toLowerCase().includes(search);
    row.style.display = tierOk && searchOk ? "" : "none";
  });
}

/* ── Export CSV ─────────────────────────────────────────────── */
function exportCSV() {
  if (!_allResults.length) return;
  const headers = ["patient_id","age","sex","trestbps","chol","oldpeak","probability","risk_tier","prediction"];
  const rows = _allResults
    .filter(r => !r.error)
    .map(r => [
      r.patient_id,
      r.inputs?.age,
      r.inputs?.sex == 1 ? "Male" : "Female",
      r.inputs?.trestbps,
      r.inputs?.chol,
      r.inputs?.oldpeak,
      r.probability + "%",
      r.risk_tier,
      r.prediction === 1 ? "Positive" : "Negative",
    ].join(","));

  const csv = [headers.join(","), ...rows].join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const url  = URL.createObjectURL(blob);
  const a    = Object.assign(document.createElement("a"), {
    href: url, download: "cardiosense_bulk_results.csv"
  });
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

/* ── Sample CSV download ────────────────────────────────────── */
function downloadSample() {
  const sample = `age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
55,1,3,140,250,0,1,140,1,2.3,1,1,3
48,0,1,120,200,0,0,165,0,0.5,0,0,1
63,1,0,145,233,1,0,150,0,2.3,0,0,1
37,1,2,130,250,0,1,187,0,3.5,0,0,2
41,0,1,130,204,0,0,172,0,1.4,2,0,2
56,1,1,120,236,0,1,178,0,0.8,2,0,2
57,0,0,120,354,0,1,163,1,0.6,2,0,2
57,1,0,140,192,0,1,148,0,0.4,1,0,1
44,1,1,120,263,0,1,173,0,0,2,0,3
52,1,2,172,199,1,1,162,0,0.5,2,0,3
57,1,2,150,168,0,1,174,0,1.6,2,0,2
54,1,0,140,239,0,1,160,0,1.2,2,0,2
48,0,2,130,275,0,1,139,0,0.2,2,0,2
49,1,1,130,266,0,1,171,0,0.6,2,0,2
64,1,3,110,211,0,0,144,1,1.8,1,0,2
58,0,3,150,283,1,0,162,0,1.0,2,0,2
50,0,2,120,219,0,1,158,0,1.6,1,0,2
58,1,0,120,340,0,1,172,0,0,2,0,2
66,0,3,150,226,0,1,114,0,2.6,0,0,2
43,1,0,150,247,0,1,171,0,1.5,2,0,2`;
  const blob = new Blob([sample], { type: "text/csv" });
  const url  = URL.createObjectURL(blob);
  const a    = Object.assign(document.createElement("a"), {
    href: url, download: "cardiosense_sample_patients.csv"
  });
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

/* ── Helpers ────────────────────────────────────────────────── */
function showBulkError(msg) {
  const el = document.getElementById("bulkError");
  if (el) { el.textContent = "⚠ " + msg; el.style.display = "block"; }
}
function hideBulkError() {
  const el = document.getElementById("bulkError");
  if (el) el.style.display = "none";
}
