// frontend/app.js
// Form handling and API calls for the EvrimaDinoAnalyzer MVP UI.
// Assumes the FastAPI backend is running at http://localhost:8000

const API_BASE = "http://localhost:8000";

const form         = document.getElementById("analyzer-form");
const speciesSelect = document.getElementById("species");
const resultsPanel = document.getElementById("results-panel");
const statsSummary = document.getElementById("stats-summary");
const matchupBody  = document.getElementById("matchup-body");

// --- Populate species dropdown on load ---
async function loadSpecies() {
  try {
    const res = await fetch(`${API_BASE}/dinos`);
    if (!res.ok) throw new Error(`Failed to load species: ${res.status}`);
    const dinos = await res.json();
    dinos.forEach(({ name }) => {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      speciesSelect.appendChild(opt);
    });
  } catch (err) {
    console.warn("Could not load species list (API may not be running yet):", err.message);
  }
}

// --- Render matchup results ---
function renderResults(data) {
  // Stats summary
  const stats = data.interpolated_stats;
  statsSummary.innerHTML = `
    <p><strong>${data.species}</strong> — ${data.growth_pct}% growth${data.is_prime ? " (Prime)" : ""}</p>
    <ul>
      ${Object.entries(stats).map(([k, v]) => `<li>${k}: ${v}</li>`).join("")}
    </ul>
  `;

  // Matchup table rows
  matchupBody.innerHTML = "";
  data.matchups.forEach(row => {
    const tr = document.createElement("tr");
    tr.className = `verdict-${row.verdict.toLowerCase()}`;
    tr.innerHTML = `
      <td>${row.opponent}</td>
      <td>${row.opponent_growth_pct}%</td>
      <td>${row.attacker_hits_to_kill.toFixed(1)}</td>
      <td>${row.defender_hits_to_kill.toFixed(1)}</td>
      <td class="verdict">${row.verdict}</td>
    `;
    matchupBody.appendChild(tr);
  });

  resultsPanel.hidden = false;
}

// --- Form submit ---
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    species:    speciesSelect.value,
    growth_pct: parseFloat(document.getElementById("growth").value),
    is_prime:   document.getElementById("prime").checked,
  };

  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    renderResults(await res.json());
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
});

loadSpecies();
