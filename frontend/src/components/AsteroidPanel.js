import { getAsteroids } from '../services/api.js';

export async function initAsteroidPanel() {
  const listEl = document.getElementById('asteroidList');
  const errorEl = document.getElementById('asteroidError');
  if (!listEl) return;

  const asteroids = await getAsteroids();

  if (!asteroids || asteroids.length === 0) {
    if (errorEl) errorEl.classList.remove('hidden');
    return;
  }

  listEl.innerHTML = '';

  asteroids.slice(0, 5).forEach((ast) => {
    const item = document.createElement('div');
    item.className = 'asteroid-item';

    const name = document.createElement('div');
    name.className = 'asteroid-name';
    name.textContent = ast.name;

    const meta1 = document.createElement('div');
    meta1.className = 'asteroid-meta';
    meta1.textContent = 'Distance: ' + ast.distance + ' LD';

    const meta2 = document.createElement('div');
    meta2.className = 'asteroid-meta';
    meta2.textContent = 'Velocity: ' + ast.velocity + ' km/s';

    const risk = document.createElement('div');
    risk.className = 'asteroid-risk';
    risk.textContent = 'Risk: ' + ast.risk;

    item.appendChild(name);
    item.appendChild(meta1);
    item.appendChild(meta2);
    item.appendChild(risk);

    listEl.appendChild(item);
  });
}
