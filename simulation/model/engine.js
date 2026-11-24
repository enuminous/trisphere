/* Numerical models for the Tri-Sphere laboratory. All times are dimensionless. */
const TriLab = (() => {
  const NAMES = ["Cosmic Return Point","Vesica piscis","3:1:3 hourglass","Tetrahedron","Octahedron","Icosahedron","Filter","Dodecahedron","Cube","Merkaba","Compost hourglass","Toroidal field","Outer shell"];
  const branch = n => n === 0 ? 0 : n < 6 ? 1 : n === 6 ? 2 : n < 12 ? 3 : 4;
  const groups = ["Inner boundary","Time","Space","Phase","Outer boundary"];
  function hopf(a,b,c,d) {
    return [a*a+b*b-c*c-d*d,2*(a*c+b*d),2*(b*c-a*d)];
  }
  const b = 11.25, a = 3;
  function gradient(r,k) {
    const slope = r < b ? r*(1-r/b)**2 : 0;
    const drive = r < a ? k*(1-r/a)**2 : 0;
    return slope-drive;
  }
  function potential(r,k) {
    const y = Math.min(r,b), z = Math.min(r,a);
    return y*y/2-2*y**3/(3*b)+y**4/(4*b*b)-k*(z-z*z/a+z**3/(3*a*a));
  }
  function rk4(r,v,dt,accel) {
    const a1 = accel(r,v);
    const v2 = v+dt*a1/2, a2 = accel(r+dt*v/2,v2);
    const v3 = v+dt*a2/2, a3 = accel(r+dt*v2/2,v3);
    const v4 = v+dt*a3, a4 = accel(r+dt*v3,v4);
    return [r+dt*(v+2*v2+2*v3+v4)/6, v+dt*(a1+2*a2+2*a3+a4)/6];
  }
  // Diagnostic integration stops at the first detected exit. No wall is silently added.
  function simulate(mode,g,k,initial,dt=1/80,span=24) {
    if (![g,k,initial,dt,span].every(Number.isFinite) || g<0 || g>=2 || k<0 ||
        initial<0 || initial>12 || dt<=0 || span<=0 || span/dt>250000)
      throw new RangeError("Parameters outside solver domain");
    const points=[], events=[];
    let status="Time window complete", r=initial, v=0;
    const omega=Math.sqrt(1-g*g/4), period=Math.PI/omega, q=Math.exp(-g*period);
    let E=initial, n=0;
    function store(t,r,v,e){points.push({t,r,v,e});}
    if ((mode==="kick" || mode==="removed") && initial===0) {
      store(0,0,0,0);store(span,0,0,0);
      return {mode,g,k,initial,dt,span,points,events,status:"Rest at center · no return event",period,q};
    }
    for(let i=0;i<=Math.floor(span/dt+1e-9);i++) {
      const t=i*dt;
      if(mode==="kick" || mode==="removed") {
        const j=mode==="kick" ? k : 0;
        while(t>=(n+1)*period) {
          n++; const before=q*E;
          E=before+j;
          events.push({t:n*period,before,after:E});
        }
        const u=t-n*period, speed=Math.sqrt(2*E)*Math.exp(-g*u/2);
        r=speed*Math.sin(omega*u)/omega;
        v=speed*(Math.cos(omega*u)-g*Math.sin(omega*u)/(2*omega));
        store(t,r,v,(r*r+v*v)/2);
      } else if(mode==="coast") {
        // Free plateau flight. Initial value is the speed, starting at the shelf entrance.
        v=initial*Math.exp(-g*t);
        r=b+(g===0?initial*t:initial*(-Math.expm1(-g*t))/g);
        store(t,r,v,v*v/2);
      } else if(mode==="fixed") {
        store(t,r,v,v*v/2+potential(r,k));
        [r,v]=rk4(r,v,dt,(x,y)=>-gradient(x,k)-g*y);
      } else throw new RangeError("Unknown experiment");
      const last=points[points.length-1];
      if(last.r<0 || last.r>12) {status="Exit detected · no wall rule";break;}
    }
    return {mode,g,k,initial,dt,span,points,events,status,period,q};
  }
  return {NAMES,groups,branch,hopf,gradient,potential,rk4,simulate};
})();
if (typeof module !== "undefined") module.exports = TriLab;
