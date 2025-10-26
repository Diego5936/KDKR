import { haversineM, stepTowards, bearingDeg } from './kinematics.js';
import { powerW, updateSoc } from './energy.js';

export class Engine {
  constructor({ missionId, waypoints, speedMps = 12, simSpeed = 1 }) {
    this.missionId = missionId;
    this.wps = waypoints;
    this.idx = 0;
    [this.lat, this.lon, this.alt] = this.wps[0];
    this.speed = speedMps;
    this.soc = 100;
    this.dist = 0;
    this.state = 'RUNNING';
    this.simT = 0;
    this.simSpeed = simSpeed;
  }

  step(dtWall) {
    if (this.state !== 'RUNNING') 
      return this.snapshot(0);
    const dt = dtWall * this.simSpeed;

    // Target waypoint
    const next = Math.min(this.idx + 1, this.wps.length - 1);
    let [tLat, tLon] = [this.wps[next][0], this.wps[next][1]];
    let segRem = haversineM(this.lat, this.lon, tLat, tLon);

    // Advance waypoint if close
    if (segRem < 2 && this.idx < this.wps.length - 2) {
      this.idx++;
      [tLat, tLon] = [this.wps[this.idx + 1][0], this.wps[this.idx + 1][1]];
      segRem = haversineM(this.lat, this.lon, tLat, tLon);
    }

    // Move
    const step = Math.min(this.speed * dt, segRem);
    const [nLat, nLon] = stepTowards(this.lat, this.lon, tLat, tLon, step);
    this.dist += haversineM(this.lat, this.lon, nLat, nLon);
    this.lat = nLat;
    this.lon = nLon;
    this.simT += dt;

    // Energy
    const P = powerW(this.speed);
    this.soc = updateSoc(this.soc, P, dt);
    if (this.soc <= 5) 
      this.state = 'FINISHED';

    return this.snapshot(segRem - step);
  }

  snapshot(segRem) {
    const next = Math.min(this.idx + 1, this.wps.length - 1);
    const heading = bearingDeg(this.lat, this.lon, this.wps[next][0], this.wps[next][1]);
    const P = powerW(this.speed);

    return {
      ts_wall: new Date().toISOString(),
      ts_sim: this.simT,
      sim_speed: this.simSpeed,
      mission_id: this.missionId,
      state: this.state,
      drone: {
        id: 'uav-1',
        lat: this.lat, 
        lon: this.lon, 
        alt_m: this.alt,
        ground_speed_mps: this.speed,
        heading_deg: heading,
        battery: {
          soc_pct: this.soc,
          voltage_v: 14.8,
          current_a: P / 14.8,
          power_w: P,
          est_remaining_s: Math.max(0, (this.soc/100)*3600*222 / P)
        }
      },
      mission: {
        waypoints: this.wps,
        active_wp_index: this.idx,
        segment_dist_remaining_m: segRem,
        total_dist_traveled_m: this.dist
      },
      alerts: []
    };
  }
}