const API_BASE = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', async () => {
    const speciesSelect = document.getElementById('species');
    const analyzeBtn = document.getElementById('analyze-btn');
    const tbody = document.querySelector('#matchup-table tbody');
    const statsUsedEl = document.getElementById('stats-used');

    // 1. Initial Load: Populate the Species Dropdown
    try {
        const res = await fetch(`${API_BASE}/api/dinos`);
        if (!res.ok) throw new Error('Failed to load dinosaurs');
        const data = await res.json();
        
        // Sort alphabetically for UX
        data.dinosaurs.sort((a, b) => a.Dinosaur.localeCompare(b.Dinosaur));
        
        data.dinosaurs.forEach(d => {
            const opt = document.createElement('option');
            opt.value = d.Dinosaur;
            opt.textContent = d.Dinosaur;
            speciesSelect.appendChild(opt);
        });
    } catch (err) {
        console.error('Error fetching dinos:', err);
        statsUsedEl.textContent = 'Error: Could not connect to API. Is the server running?';
        statsUsedEl.style.color = '#ff6b6b';
    }

    // 2. Handle Analysis Submit
    analyzeBtn.addEventListener('click', async () => {
        const species = speciesSelect.value;
        const growth_pct = parseFloat(document.getElementById('growth').value) || 100;
        const is_prime = document.getElementById('prime').checked;
        const dietFilter = document.getElementById('diet-filter').value;

        analyzeBtn.textContent = "Analyzing...";
        analyzeBtn.disabled = true;

        try {
            const res = await fetch(`${API_BASE}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ species, growth_pct, is_prime })
            });

            if (!res.ok) throw new Error('Failed to analyze matchup');
            const data = await res.json();
            
            // Fetch the play guide profile
            try {
                const guideRes = await fetch(`${API_BASE}/guide/${species}`);
                const guideData = await guideRes.json();
                const guideEl = document.getElementById('playstyle-guide');
                if (guideEl && guideData.playstyle_tips && guideData.playstyle_tips.length > 0) {
                    guideEl.style.display = 'block';
                    guideEl.innerHTML = '<strong>Playstyle Guide:</strong><ul>' + 
                        guideData.playstyle_tips.map(t => `<li>${t}</li>`).join('') + 
                        '</ul>';
                } else if (guideEl) {
                    guideEl.style.display = 'none';
                }
            } catch (err) {
                console.error("Guide fetch failed:", err);
            }
            
            // Display exactly what stats the backend mathematically applied
            const s = data.stats_used;
            statsUsedEl.innerHTML = `Interpolated Attacker Stats: <strong>${s.calc_mass_kg.toFixed(1)}kg</strong> Mass | <strong>${s.calc_bite_N.toFixed(1)}N</strong> Bite Force | <strong>${s.calc_sprint_kmh.toFixed(1)}km/h</strong> Sprint<br><em>(Growth Applied: ${s.growth_applied}%, Prime: ${s.is_prime})</em>`;
            statsUsedEl.style.color = '#888';
            
            const attackerMechs = (data.attacker_mechanics || []).map(mech => mech.Mechanic_Name || mech.Ability_Name).filter(Boolean);
            const attackerMechsEl = document.getElementById('attacker-mechanics');
            if (attackerMechsEl) {
                attackerMechsEl.textContent = `Attacker Abilities/Mechanics: ${attackerMechs.length > 0 ? attackerMechs.join(', ') : 'None'}`;
                attackerMechsEl.style.color = '#888';
            }
            
            // Render Table Rows
            tbody.innerHTML = '';
            
            // Sort by verdict ease (Engage, Caution, Flee)
            const order = { 'Engage': 1, 'Caution': 2, 'Flee': 3 };
            let sortedMatchups = data.matchups.sort((a, b) => order[a.verdict] - order[b.verdict]);

            // Filter by diet
            if (dietFilter !== 'All') {
                sortedMatchups = sortedMatchups.filter(m => m.opponent_diet === dietFilter);
            }

            sortedMatchups.forEach(m => {
                const tr = document.createElement('tr');
                
                let verdictClass = '';
                if (m.verdict === 'Engage') verdictClass = 'verdict-engage';
                else if (m.verdict === 'Caution') verdictClass = 'verdict-caution';
                else if (m.verdict === 'Flee') verdictClass = 'verdict-flee';

                const mechs = (m.opponent_mechanics || []).map(mech => {
                    const name = mech.Mechanic_Name || mech.Ability_Name;
                    if (!name) return null;
                    const tooltip = `<strong>${name}</strong><br>Type: ${mech.Type || 'Unspecified'}<br>Effect: ${mech.Effect || 'Unknown'}<br>Impact: ${mech.Gameplay_Impact || 'N/A'}`;
                    return `<span class="mechanic-item">${name}<div class="mechanic-tooltip">${tooltip}</div></span>`;
                }).filter(Boolean);
                const mechsStr = mechs.length > 0 ? mechs.join(', ') : 'None';

                let dietColor = '#aaa';
                if (m.opponent_diet === 'Carnivore') dietColor = '#ff6b6b';
                else if (m.opponent_diet === 'Herbivore') dietColor = '#8bc34a';
                else if (m.opponent_diet === 'Omnivore') dietColor = '#ffd54f';

                const speedDiff = (m.attacker_sprint_kmh - m.defender_sprint_kmh).toFixed(1);
                const isFaster = speedDiff > 0;
                const speedColor = isFaster ? '#8bc34a' : '#ff6b6b';
                const speedText = `${m.defender_sprint_kmh.toFixed(1)} km/h (<span style="color:${speedColor}">${isFaster ? '+' : ''}${speedDiff}</span>)`;

                tr.innerHTML = `
                    <td><strong>${m.opponent}</strong></td>
                    <td style="color:${dietColor}">${m.opponent_diet}</td>
                    <td style="font-size: 0.85em; font-style: italic; color: #aaa;">${mechsStr}</td>
                    <td>${m.hits_to_kill_them_body} | <span style="color:#ffb74d">${m.hits_to_kill_them_head}</span></td>
                    <td>${m.hits_for_them_to_kill_you_body} | <span style="color:#ffb74d">${m.hits_for_them_to_kill_you_head}</span></td>
                    <td>${speedText}</td>
                    <td class="${verdictClass}">${m.verdict}</td>
                `;
                tbody.appendChild(tr);
            });
        } catch (err) {
            console.error('Error analyzing:', err);
            statsUsedEl.textContent = 'Error: Analysis failed. See console.';
            statsUsedEl.style.color = '#ff6b6b';
        } finally {
            analyzeBtn.textContent = "Analyze Matchups";
            analyzeBtn.disabled = false;
        }
    });
});
