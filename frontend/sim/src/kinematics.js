const toRad = d => d * Math.PI / 180;
const toDeg = r => r * 180 / Math.PI;

export function haversineM(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const dlat = toRad(lat2 - lat1), dlon = toRad(lon2 - lon1);
  const a = Math.sin(dlat/2)**2 +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dlon/2)**2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

export function bearingDeg(lat1, lon1, lat2, lon2) {
  const y = Math.sin(toRad(lon2 - lon1)) * Math.cos(toRad(lat2));
  const x = Math.cos(toRad(lat1)) * Math.sin(toRad(lat2)) -
            Math.sin(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.cos(toRad(lon2 - lon1));
  return (toDeg(Math.atan2(y, x)) + 360) % 360;
}

export function stepTowards(lat, lon, tgtLat, tgtLon, distM) {
  const br = toRad(bearingDeg(lat, lon, tgtLat, tgtLon));
  const R = 6371000;
  const d = distM / R;
  const lat1 = toRad(lat), lon1 = toRad(lon);
  const lat2 = Math.asin(Math.sin(lat1) * Math.cos(d) +
                         Math.cos(lat1) * Math.sin(d) * Math.cos(br));
  const lon2 = lon1 + Math.atan2(Math.sin(br) * Math.sin(d) * Math.cos(lat1),
                                 Math.cos(d) - Math.sin(lat1) * Math.sin(lat2));
  return [toDeg(lat2), toDeg(lon2)];
}