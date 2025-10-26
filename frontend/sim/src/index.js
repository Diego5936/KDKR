import { store } from './store.js';
import { Engine } from './engine.js';
import * as MapMod from './map.js';
const { initMap } = MapMod;

const DEFAULT_WPS = [
  [28.6022, -81.2002, 50],
  [28.6028, -81.1990, 50],
  [28.6035, -81.2005, 50],
  [28.6026, -81.2012, 50]
];

function makeHud(root) {
  const hud = document.createElement('div'); 
  hud.className = 'kdkr-hud';
  hud.innerHTML = `
    <div>Battery: <span id="kdkr-batt">--%</span></div>
    <div>Waypoint: <span id="kdkr-wp">-- / --</span></div>
    <div>Sim Time: <span id="kdkr-ts">0.0s</span></div>`;
  root.appendChild(hud);

  return {
    update(tlm) {
      root.querySelector('#kdkr-batt').textContent = `${tlm.drone.battery.soc_pct.toFixed(0)}%`;
      root.querySelector('#kdkr-wp').textContent = `${tlm.mission.active_wp_index+1} / ${tlm.mission.waypoints.length}`;
      root.querySelector('#kdkr-ts').textContent = `${tlm.ts_sim.toFixed(1)}s`;
    }
  };
}

function mount(host, options = {}) {
  // Container skeleton
  const root = document.createElement('div'); 
  root.className = 'kdkr-sim';
  const mapDiv = document.createElement('div'); 
  mapDiv.className = 'kdkr-map'; 
  mapDiv.id = 'kdkr-map';

  // Fallback size
  mapDiv.style.width = '100%';
  mapDiv.style.height = '420px';
  
  root.appendChild(mapDiv); 
  host.innerHTML = ''; 
  host.appendChild(root);

  const waypoints = options.waypoints || DEFAULT_WPS;
  const missionId = options.missionId || 'demo-001';
  const speedMps = options.speedMps ?? 12;
  const simSpeed  = options.simSpeed  ?? 1;

  // View and engine
  const view = initMap({ center: [waypoints[0][0], waypoints[0][1]], waypoints, containerId: 'kdkr-map' });
  const hud  = makeHud(root);
  const eng  = new Engine({ missionId, waypoints, speedMps, simSpeed });

  // Animation loop
  let rafId = null, last = performance.now(); 
  
  let running = true;
  function frame() {
    const now = performance.now(); 
    const dt = (now - last)/1000; 
    last = now;

    const tlm = eng.step(dt); 
    store.set(tlm);

    hud.update(tlm); 
    view.setPose(tlm.drone.lat, tlm.drone.lon, tlm.drone.heading_deg);
    if (running && tlm.state === 'RUNNING') 
      rafId = requestAnimationFrame(frame);
  }
  rafId = requestAnimationFrame(frame);

  // Controls
  const controls = {
    pause() { 
      running = false; 
      if (rafId) 
        cancelAnimationFrame(rafId); 
    },
    resume() { 
      if (!running) { 
        running = true; 
        last = performance.now(); 
        rafId = requestAnimationFrame(frame); 
      } 
    },
    reset(opts = {}) {
      controls.pause();
      return mount(host, { ...options, ...opts });
    },
    start: () => {},
  };

  // Expose API
  return {
    unmount() { 
      controls.pause(); 
      host.innerHTML = ''; 
    },
    controls,
  };
}

// Global API
window.KDKRSim = {
  mount,
  on: (event, fn) => store.on(event, fn),
  getState: () => store.get()
};
export default window.KDKRSim;

document.addEventListener('DOMContentLoaded', () => {
  console.log('[KDKRSim] index.js loaded, trying to mount');
  const host = document.getElementById('host');
  if (!host) {
    console.warn('[KDKRSim] #host not found');
    return;
  }
  window.KDKRSim.mount(host, {
    speedMps: 12,
    simSpeed: 1,
  });
});