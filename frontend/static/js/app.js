/* ============================================================
   CardioSense AI v2 — app.js
   Handles: theme toggle, single prediction, summary redirect
   ============================================================ */

"use strict";

/* ── Theme ─────────────────────────────────────────────────── */
(function initTheme() {
  const saved = localStorage.getItem("cs-theme") || "dark";
  document.documentElement.setAttribute("data-theme", saved);
  updateThemeIcon(saved);
})();

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "dark";
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("cs-theme", next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  document.querySelectorAll(".theme-icon").forEach(el => {
    el.textContent = theme === "dark" ? "🌙" : "☀️";
  });
}

/* ── Model chips ────────────────────────────────────────────── */
document.querySelectorAll(".mchip").forEach(chip => {
  chip.addEventListener("click", () => chip.classList.toggle("active"));
});

/* ── Collect form ───────────────────────────────────────────── */
function collectInputs() {
  const ids = ["age","sex","cp","trestbps","chol","fbs","restecg",
               "thalach","exang","oldpeak","slope","ca","thal","bmi"];
  const payload = {};
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el && el.value.trim() !== "") payload[id] = parseFloat(el.value);
  });
  const active = [...document.querySelectorAll(".mchip.active")];
  if (active.length > 0) {
    payload.selected_models = active.map(c => c.dataset.model);
  }
  return payload;
}

/* ── Loading messages ───────────────────────────────────────── */
const LOADING_MSGS = [
  "Initialising ensemble models…",
  "Scaling clinical features…",
  "Running Logistic Regression & SVM…",
  "Running Random Forest & XGBoost…",
  "Computing Gradient Boosting…",
  "Aggregating Voting Ensemble…",
  "Generating risk profile…",
  "Building personalised recommendations…",
];
let _loadingInterval;

function startLoadingMessages() {
  const el = document.getElementById("loadingStep");
  if (!el) return;
  let i = 0;
  el.textContent = LOADING_MSGS[0];
  _loadingInterval = setInterval(() => {
    i = (i + 1) % LOADING_MSGS.length;
    el.textContent = LOADING_MSGS[i];
  }, 750);
}
function stopLoadingMessages() {
  clearInterval(_loadingInterval);
}

/* ── Submit prediction ──────────────────────────────────────── */
let _lastSummary = null;

async function submitPrediction() {
  const errBox = document.getElementById("formError");
  errBox.style.display = "none";

  const payload = collectInputs();
  const required = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"];
  const missing = required.filter(f => payload[f] === undefined);
  if (missing.length > 0) {
    errBox.innerHTML = `⚠ Please fill in: <strong>${missing.join(", ").toUpperCase()}</strong>`;
    errBox.style.display = "block";
    return;
  }
  const activeChips = document.querySelectorAll(".mchip.active");
  if (activeChips.length === 0) {
    errBox.innerHTML = "⚠ Please select at least one ML model.";
    errBox.style.display = "block";
    return;
  }

  document.getElementById("results").style.display = "none";
  document.getElementById("loading").style.display  = "flex";
  document.getElementById("btnPredict").disabled    = true;
  startLoadingMessages();

  try {
    const res  = await fetch("/api/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok || !data.success) {
      const msgs = data.errors || [data.error || "Prediction failed."];
      errBox.innerHTML = msgs.map(m => `• ${m}`).join("<br>");
      errBox.style.display = "block";
      return;
    }

    _lastSummary = data.summary;
    renderResults(data);
  } catch (err) {
    errBox.innerHTML = `⚠ Network error: ${err.message}`;
    errBox.style.display = "block";
  } finally {
    document.getElementById("loading").style.display  = "none";
    document.getElementById("btnPredict").disabled    = false;
    stopLoadingMessages();
  }
}

/* ── Render results ─────────────────────────────────────────── */
function renderResults(data) {
  const tier = data.risk_tier;
  const prob = data.ensemble_prob;

  /* --- Risk card --- */
  const card = document.getElementById("riskCard");
  card.className = `risk-card ${tier}`;

  document.getElementById("riskTierLabel").className = `risk-tier-label ${tier}`;
  document.getElementById("riskTierLabel").textContent = tier.charAt(0).toUpperCase() + tier.slice(1) + " Risk Detected";

  const titleEl = document.getElementById("riskTitle");
  titleEl.className = `risk-title ${tier}`;
  titleEl.textContent =
    tier === "high"   ? "⚠ High Cardiovascular Risk" :
    tier === "medium" ? "🔔 Moderate Risk Profile"   : "✅ Low Risk Profile";

  document.getElementById("riskDesc").textContent =
    tier === "high"
      ? "Your clinical parameters indicate significant cardiovascular disease risk. Immediate cardiology consultation is strongly advised."
    : tier === "medium"
      ? "Several modifiable risk factors are present. Proactive lifestyle intervention and regular monitoring can meaningfully reduce your risk."
      : "Your current profile is reassuring. Maintaining healthy habits will help keep it that way.";

  /* Gauge */
  const gaugeArc = document.getElementById("gaugeArc");
  const pctEl    = document.getElementById("gaugePct");
  const totalLen = 188.5;
  gaugeArc.style.stroke = tier === "high" ? "#e63946" : tier === "medium" ? "#ffd166" : "#06d6a0";
  pctEl.textContent = prob + "%";
  pctEl.style.color = tier === "high" ? "#e63946" : tier === "medium" ? "#ffd166" : "#06d6a0";
  setTimeout(() => {
    gaugeArc.style.strokeDashoffset = totalLen * (1 - prob / 100);
  }, 100);

  document.getElementById("ensembleNote").innerHTML =
    `${data.positive_count} / ${data.total_models} models predict positive<br/>` +
    `Best model: <strong>${data.best_model?.display_name || "Ensemble"}</strong> ` +
    `(${data.best_model?.accuracy || 96}% acc)`;

  /* Badge */
  document.getElementById("modelBadge").textContent = `${data.total_models} models`;

  /* --- Per-model cards --- */
  const grid = document.getElementById("modelCards");
  grid.innerHTML = "";
  (data.model_results || []).forEach((r, i) => {
    const barColor = r.probability >= 60 ? "#e63946" : r.probability >= 40 ? "#ffd166" : "#06d6a0";
    const c = document.createElement("div");
    c.className = "mrc";
    c.style.animationDelay = `${i * 0.07}s`;
    c.innerHTML = `
      <div class="mrc-name">${r.display_name}</div>
      <div class="mrc-verdict ${r.prediction === 1 ? 'pos' : 'neg'}">
        ${r.prediction === 1 ? "Positive" : "Negative"}
      </div>
      <div class="mrc-meta">Risk: ${r.probability}% · Acc: ${r.accuracy}%</div>
      <div class="mrc-bar">
        <div class="mrc-fill" style="background:${barColor}" data-w="${r.probability}"></div>
      </div>`;
    grid.appendChild(c);
  });
  setTimeout(() => {
    document.querySelectorAll(".mrc-fill").forEach(el => {
      el.style.width = el.dataset.w + "%";
    });
  }, 200);

  /* --- Recommendations --- */
  const recGrid = document.getElementById("recCards");
  recGrid.innerHTML = "";
  (data.recommendations || []).forEach((rec, i) => {
    const c = document.createElement("div");
    c.className = `recc ${rec.priority}`;
    c.style.animationDelay = `${i * 0.05}s`;
    c.innerHTML = `
      <span class="recc-icon">${rec.icon}</span>
      <div class="recc-title">${rec.title}</div>
      <div class="recc-body">${rec.body}</div>`;
    recGrid.appendChild(c);
  });

  /* Show */
  const resultsEl = document.getElementById("results");
  resultsEl.style.display = "block";
  resultsEl.style.animation = "slideUp 0.5s ease";
  resultsEl.scrollIntoView({ behavior: "smooth", block: "start" });
}

/* ── Go to summary page ─────────────────────────────────────── */
function goToSummary() {
  if (!_lastSummary) return;
  const encoded = encodeURIComponent(JSON.stringify(_lastSummary));
  window.location.href = `/summary?data=${encoded}`;
}

/* ── Reset ──────────────────────────────────────────────────── */
function resetForm() {
  document.getElementById("results").style.display   = "none";
  document.getElementById("formError").style.display = "none";
  _lastSummary = null;

  ["age","sex","cp","trestbps","chol","fbs","restecg","thalach",
   "exang","oldpeak","slope","ca","thal","bmi"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });
  document.querySelectorAll(".mchip").forEach(c => c.classList.add("active"));
  window.scrollTo({ top: 0, behavior: "smooth" });
}
