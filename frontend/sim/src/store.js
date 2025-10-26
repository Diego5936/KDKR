// Event bus
class Store extends EventTarget {
  constructor() { 
    super(); 
    this.state = null; 
  }

  set(tlm) { 
    this.state = tlm; 
    this.dispatchEvent(new CustomEvent('telemetry', { detail: tlm })); 
  }

  get() { 
    return this.state; 
  }

  on(type, fn) { 
    const h = e => fn(e.detail); 
    this.addEventListener(type, h); 
    return () => this.removeEventListener(type, h); 
  }
}
export const store = new Store();