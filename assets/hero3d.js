/* ============================================================================
   ZET8 hero — the brand "8" as a 3D object.
   Two tangent rings built from colored arc segments (green/yellow/red/blue),
   Phong-lit, slowly oscillating, with pointer parallax.

   Raw WebGL 1, zero dependencies. Progressive enhancement:
   - no WebGL, or prefers-reduced-motion  -> static PNG fallback stays visible
   - offscreen or hidden tab              -> render loop pauses
   ============================================================================ */
(function () {
  'use strict';

  var canvas = document.getElementById('hero3d');
  if (!canvas) return;
  var stage = canvas.parentElement;
  var hero = canvas.closest('.hero') || stage;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var gl = canvas.getContext('webgl', { alpha: true, antialias: true, preserveDrawingBuffer: true })
        || canvas.getContext('experimental-webgl', { alpha: true, antialias: true, preserveDrawingBuffer: true });
  if (!gl) return;

  /* ------------------------------------------------------------- config -- */
  var COLORS = {
    green:  [60 / 255, 179 / 255, 113 / 255],
    yellow: [244 / 255, 200 / 255, 45 / 255],
    red:    [232 / 255, 74 / 255, 56 / 255],
    blue:   [84 / 255, 104 / 255, 232 / 255]
  };
  var RING_R = 0.72;   // ring (major) radius
  var TUBE_R = 0.30;   // tube (minor) radius
  var RING_CY = 0.94;  // ring center offset from group center (rings overlap a touch)
  var RING_CZ = 0.16;  // depth offset so the rings interlock at the crossing
  // Arc layout mirrors the logo: both rings cut along the same 45/225-degree
  // diagonal, cool colors up top. Rounded end-caps extend each arc ~23 deg per
  // side, so the 34-deg nominal gaps leave ~11 deg of visible daylight.
  var ARCS = [
    { cy: +RING_CY, cz: +RING_CZ, color: 'blue',   a0: 62,  a1: 208 },
    { cy: +RING_CY, cz: +RING_CZ, color: 'green',  a0: 242, a1: 388 },
    { cy: -RING_CY, cz: -RING_CZ, color: 'yellow', a0: 62,  a1: 208 },
    { cy: -RING_CY, cz: -RING_CZ, color: 'red',    a0: 242, a1: 388 }
  ];
  var GROUP_SCALE = 0.92;
  var GROUP_TILT_Z = -0.10;      // the logo's slight lean
  var CAMERA_Z = 6.8;
  var FOV = 35 * Math.PI / 180;
  var DPR_CAP = 2;

  /* ------------------------------------------------------------ shaders -- */
  var VS = [
    'attribute vec3 aPos;',
    'attribute vec3 aNormal;',
    'uniform mat4 uMVP;',
    'uniform mat4 uModel;',
    'varying vec3 vN;',
    'varying vec3 vPos;',
    'void main() {',
    '  vN = mat3(uModel[0].xyz, uModel[1].xyz, uModel[2].xyz) * aNormal;',
    '  vPos = (uModel * vec4(aPos, 1.0)).xyz;',
    '  gl_Position = uMVP * vec4(aPos, 1.0);',
    '}'
  ].join('\n');

  var FS = [
    'precision mediump float;',
    'uniform vec3 uColor;',
    'varying vec3 vN;',
    'varying vec3 vPos;',
    'void main() {',
    '  vec3 N = normalize(vN);',
    '  vec3 V = normalize(vec3(0.0, 0.0, ' + CAMERA_Z.toFixed(2) + ') - vPos);',
    '  vec3 L1 = normalize(vec3(-0.45, 0.75, 0.6));',   // key light, upper left
    '  vec3 L2 = normalize(vec3(0.65, -0.35, 0.45));',  // fill, lower right
    '  float diff = max(dot(N, L1), 0.0) * 0.80 + max(dot(N, L2), 0.0) * 0.28 + 0.32;',
    '  vec3 H = normalize(L1 + V);',
    '  float spec = pow(max(dot(N, H), 0.0), 42.0) * 0.45;',
    '  float rim = pow(1.0 - max(dot(N, V), 0.0), 3.0) * 0.22;',
    '  vec3 c = uColor * diff + vec3(1.0) * (spec + rim);',
    '  gl_FragColor = vec4(c, 1.0);',
    '}'
  ].join('\n');

  function compile(type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      throw new Error(gl.getShaderInfoLog(s));
    }
    return s;
  }
  var prog = gl.createProgram();
  gl.attachShader(prog, compile(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, FS));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return; // bail to fallback
  gl.useProgram(prog);

  var loc = {
    aPos: gl.getAttribLocation(prog, 'aPos'),
    aNormal: gl.getAttribLocation(prog, 'aNormal'),
    uMVP: gl.getUniformLocation(prog, 'uMVP'),
    uModel: gl.getUniformLocation(prog, 'uModel'),
    uColor: gl.getUniformLocation(prog, 'uColor')
  };

  /* ----------------------------------------------------------- geometry -- */
  // Torus arc with rounded ends: the arc is extended a few extra rows while
  // the tube radius eases to zero, producing capsule-like caps.
  function buildArc(arc) {
    var U = 64, V = 22, CAP = 7;
    var capLen = (TUBE_R / RING_R) * 0.95;
    var a0 = arc.a0 * Math.PI / 180, a1 = arc.a1 * Math.PI / 180;
    var rows = [], i, j, k;

    for (k = CAP; k >= 1; k--) rows.push({ a: a0 - capLen * k / CAP, s: Math.sqrt(Math.max(0, 1 - k * k / (CAP * CAP))) });
    for (i = 0; i <= U; i++) rows.push({ a: a0 + (a1 - a0) * i / U, s: 1 });
    for (k = 1; k <= CAP; k++) rows.push({ a: a1 + capLen * k / CAP, s: Math.sqrt(Math.max(0, 1 - k * k / (CAP * CAP))) });

    var pos = [], nor = [], idx = [];
    for (i = 0; i < rows.length; i++) {
      var a = rows[i].a, s = rows[i].s;
      var ca = Math.cos(a), sa = Math.sin(a);
      for (j = 0; j <= V; j++) {
        var phi = j / V * Math.PI * 2;
        var cp = Math.cos(phi), sp = Math.sin(phi);
        var nx = ca * cp, ny = sa * cp, nz = sp;
        pos.push(RING_R * ca + TUBE_R * s * nx,
                 RING_R * sa + TUBE_R * s * ny + arc.cy,
                 TUBE_R * s * nz + arc.cz);
        nor.push(nx, ny, nz);
      }
    }
    for (i = 0; i < rows.length - 1; i++) {
      for (j = 0; j < V; j++) {
        var a2 = i * (V + 1) + j, b = a2 + V + 1;
        idx.push(a2, b, a2 + 1, b, b + 1, a2 + 1);
      }
    }
    return {
      color: COLORS[arc.color],
      count: idx.length,
      vbo: makeBuffer(gl.ARRAY_BUFFER, new Float32Array(pos)),
      nbo: makeBuffer(gl.ARRAY_BUFFER, new Float32Array(nor)),
      ibo: makeBuffer(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(idx))
    };
  }
  function makeBuffer(target, data) {
    var b = gl.createBuffer();
    gl.bindBuffer(target, b);
    gl.bufferData(target, data, gl.STATIC_DRAW);
    return b;
  }
  var meshes = ARCS.map(buildArc);

  /* ------------------------------------------------------- mat4 helpers -- */
  function identity() { return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]; }
  function multiply(a, b) {
    var o = new Array(16);
    for (var r = 0; r < 4; r++) for (var c = 0; c < 4; c++) {
      o[c * 4 + r] = a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1] + a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3];
    }
    return o;
  }
  function rotX(t) { var c = Math.cos(t), s = Math.sin(t); return [1,0,0,0, 0,c,s,0, 0,-s,c,0, 0,0,0,1]; }
  function rotY(t) { var c = Math.cos(t), s = Math.sin(t); return [c,0,-s,0, 0,1,0,0, s,0,c,0, 0,0,0,1]; }
  function rotZ(t) { var c = Math.cos(t), s = Math.sin(t); return [c,s,0,0, -s,c,0,0, 0,0,1,0, 0,0,0,1]; }
  function scaleM(s) { return [s,0,0,0, 0,s,0,0, 0,0,s,0, 0,0,0,1]; }
  function translate(x, y, z) { var m = identity(); m[12] = x; m[13] = y; m[14] = z; return m; }
  function perspective(fov, aspect, near, far) {
    var f = 1 / Math.tan(fov / 2), nf = 1 / (near - far);
    return [f / aspect,0,0,0, 0,f,0,0, 0,0,(far + near) * nf,-1, 0,0,2 * far * near * nf,0];
  }

  /* ------------------------------------------------- interaction, state -- */
  var pointerX = 0, pointerY = 0, px = 0, py = 0; // target / smoothed
  hero.addEventListener('pointermove', function (e) {
    var r = hero.getBoundingClientRect();
    pointerX = ((e.clientX - r.left) / r.width - 0.5) * 2;
    pointerY = ((e.clientY - r.top) / r.height - 0.5) * 2;
  });
  hero.addEventListener('pointerleave', function () { pointerX = 0; pointerY = 0; });

  var running = true, visible = true, raf = null;
  var io = new IntersectionObserver(function (es) {
    visible = es[0].isIntersecting;
    schedule();
  }, { threshold: 0 });
  io.observe(canvas);
  document.addEventListener('visibilitychange', function () {
    running = !document.hidden;
    schedule();
  });
  function schedule() {
    var active = running && visible;
    if (active && raf === null) raf = requestAnimationFrame(frame);
    if (!active && raf !== null) { cancelAnimationFrame(raf); raf = null; }
  }

  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, DPR_CAP);
    var w = Math.round(stage.clientWidth * dpr), h = Math.round(stage.clientHeight * dpr);
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w; canvas.height = h;
      gl.viewport(0, 0, w, h);
    }
  }
  window.addEventListener('resize', resize);

  /* --------------------------------------------------------- render loop -- */
  gl.enable(gl.DEPTH_TEST);
  gl.clearColor(0, 0, 0, 0);
  var t0 = performance.now();

  function frame(now) {
    raf = null;
    var t = (now - t0) / 1000;

    resize();
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    px += (pointerX - px) * 0.055;
    py += (pointerY - py) * 0.055;

    var ry = Math.sin(t * 0.24) * 0.5 + px * 0.38;
    var rx = -0.16 + Math.sin(t * 0.15) * 0.05 + py * 0.22;
    var bob = Math.sin(t * 0.55) * 0.05;

    var model = multiply(translate(0, bob, 0),
                multiply(rotZ(GROUP_TILT_Z),
                multiply(rotY(ry),
                multiply(rotX(rx), scaleM(GROUP_SCALE)))));
    var view = translate(0, 0, -CAMERA_Z);
    var proj = perspective(FOV, canvas.width / Math.max(1, canvas.height), 0.1, 30);
    var mvp = multiply(proj, multiply(view, model));

    gl.uniformMatrix4fv(loc.uMVP, false, new Float32Array(mvp));
    gl.uniformMatrix4fv(loc.uModel, false, new Float32Array(model));

    for (var m = 0; m < meshes.length; m++) {
      var mesh = meshes[m];
      gl.uniform3fv(loc.uColor, mesh.color);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vbo);
      gl.enableVertexAttribArray(loc.aPos);
      gl.vertexAttribPointer(loc.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.nbo);
      gl.enableVertexAttribArray(loc.aNormal);
      gl.vertexAttribPointer(loc.aNormal, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, mesh.ibo);
      gl.drawElements(gl.TRIANGLES, mesh.count, gl.UNSIGNED_SHORT, 0);
    }

    if (running && visible) raf = requestAnimationFrame(frame);
  }

  /* --------------------------------------------------------------- go -- */
  stage.classList.add('has-3d'); // swaps the static PNG for the canvas
  resize();
  raf = requestAnimationFrame(frame);

  // Tiny debug/scripting surface: force one synchronous frame.
  window.__zet8Hero3d = { renderFrame: function () { frame(performance.now()); } };
})();
