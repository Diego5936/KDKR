// frontend/sim/src/energy.js
export function powerW(vMps, climbMps = 0) {
  const P_hover = 120;   // base hover draw (W)
  const k_drag = 0.8;    // air drag factor * v^2
  const k_climb = 30;    // extra draw when climbing (per m/s)
  return P_hover + k_drag*(vMps**2) + k_climb*Math.max(0, climbMps);
}

export function updateSoc(socPct, powerWatt, dtS, packWh = 222) {
  const wh = powerWatt * (dtS / 3600);
  const drop = (wh / packWh) * 100;
  return Math.max(0, socPct - drop);
}
