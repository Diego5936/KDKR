console.log('[KDKRSim] map.js loaded');

export function initMap({ containerId = 'kdkr-map', center, waypoints, 
                          allWaypoints = [], visitedIds = [], path = []}) {
  const map = L.map(containerId, { zoomControl: true }).setView(center, 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

  // Draw all waypoints
  const visitedSet = new Set(visitedIds);
  const allGroup = L.layerGroup().addTo(map);

  for (const wp of allWaypoints) {
    const isVisited = visitedSet.has(wp.id);
    L.circleMarker([wp.lat, wp.lon], {
      radius: 4,
      color: isVisited ? 'green' : 'red',
      weight: 2,
      fillOpacity: 0.9,
    }).addTo(allGroup);
  }

  // Draw mission path
  if (path && path.length > 1) {
    const latlngs = path.map(p => [p[0], p[1]]);
    L.polyline(latlngs, { weight: 3, color: 'purple' }).addTo(map);
  }

  // Draw drone marker
  let start = null;
  if (path && path.length) {
    start = [path[0][0], path[0][1]];
  }
  else if (waypoints && waypoints.length) {
    start = [waypoints[0][0], waypoints[0][1]];
  }
  else {
    start = center;
  }

  const icon = L.divIcon({ className: 'drone-icon', html: '🚁', iconSize: [24,24], iconAnchor: [12,12] });
  const marker = L.marker(start, { icon }).addTo(map);

  return {
    setPose(lat, lon /*, headingDeg */) {
      marker.setLatLng([lat, lon]);
    },
    map
  };
}

export default { initMap };
