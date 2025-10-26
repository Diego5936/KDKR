console.log('[KDKRSim] map.js loaded');

export function initMap({ containerId = 'kdkr-map', center, waypoints }) {
  const map = L.map(containerId, { zoomControl: true }).setView(center, 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

  const latlngs = waypoints.map(wp => [wp[0], wp[1]]);
  L.polyline(latlngs, { weight: 3 }).addTo(map);

  const icon = L.divIcon({ className: 'drone-icon', html: '🚁', iconSize: [24,24], iconAnchor: [12,12] });
  const marker = L.marker(latlngs[0], { icon }).addTo(map);

  return {
    setPose(lat, lon /*, headingDeg */) {
      marker.setLatLng([lat, lon]);
    },
    map
  };
}

// Export also as default to be extra safe against any named-export weirdness
export default { initMap };
