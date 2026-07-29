/* ============================================================================
   ZET8 hero — the full brand mark ("ZET." + the segmented 8) as a 3D object.

   - Letters: extruded 2D polygons (ear-clip triangulation), flat-shaded sides.
   - The 8: two tangent rings built from colored torus arcs with rounded caps.
   - Phong + rim lighting, slow oscillation, pointer parallax.

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
  var CENTER_X = -0.88;  // recenters the whole "ZET.8" composition
  var DEPTH = 0.55;      // letter extrusion depth

  /* The 8 --------------------------------------------------------------- */
  var RING_R = 0.78, TUBE_R = 0.32;
  var RING_CY = 1.02;    // ring centers sit just past tangency
  var RING_CZ = 0.16;    // depth offset so the rings interlock
  var EIGHT_X = 4.25 + CENTER_X;
  // Both rings cut along the 45/225-degree diagonal like the logo. Rounded
  // caps extend each arc ~23 deg per side; 34-deg nominal gaps stay visible.
  var ARCS = [
    { cy: +RING_CY, cz: +RING_CZ, color: 'blue',   a0: 62,  a1: 208 },
    { cy: +RING_CY, cz: +RING_CZ, color: 'green',  a0: 242, a1: 388 },
    { cy: -RING_CY, cz: -RING_CZ, color: 'yellow', a0: 62,  a1: 208 },
    { cy: -RING_CY, cz: -RING_CZ, color: 'red',    a0: 242, a1: 388 }
  ];

  /* The letters ---------------------------------------------------------- */
  // Chunky angular Z / E / T outlines (x right, y up), baseline at y = 0.
  var LETTER_Y = -1.55; // baseline offset within the composition
  var SHAPES = [
    { color: 'green', x: -3.60 + CENTER_X, pts: [       // Z
        0, 2.35, 1.75, 2.35, 1.75, 1.75, 0.62, 0.60, 1.75, 0.60,
        1.75, 0, 0, 0, 0, 0.60, 1.13, 1.75, 0, 1.75] },
    { color: 'yellow', x: -1.55 + CENTER_X, pts: [      // E
        0, 0, 1.55, 0, 1.55, 0.55, 0.55, 0.55, 0.55, 0.915,
        1.42, 0.915, 1.42, 1.435, 0.55, 1.435, 0.55, 1.80,
        1.55, 1.80, 1.55, 2.35, 0, 2.35] },
    { color: 'red', x: 0.30 + CENTER_X, pts: [          // T
        0, 2.35, 1.65, 2.35, 1.65, 1.75, 1.135, 1.75, 1.135, 0,
        0.515, 0, 0.515, 1.75, 0, 1.75] },
    { color: 'blue', x: 2.05 + CENTER_X, pts: (function () { // the dot "."
        var p = [], N = 22, r = 0.30;
        for (var i = 0; i < N; i++) {
          var a = i / N * Math.PI * 2;
          p.push(0.30 + r * Math.cos(a), 0.30 + r * Math.sin(a));
        }
        return p;
      })() }
  ];

  /* Camera / motion ------------------------------------------------------ */
  var GROUP_SCALE = 0.66;
  var GROUP_TILT_Z = -0.04;
  var CAMERA_Z = 8.4;
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

  function makeBuffer(target, data) {
    var b = gl.createBuffer();
    gl.bindBuffer(target, b);
    gl.bufferData(target, data, gl.STATIC_DRAW);
    return b;
  }
  function finishMesh(color, pos, nor, idx) {
    return {
      color: COLORS[color],
      count: idx.length,
      vbo: makeBuffer(gl.ARRAY_BUFFER, new Float32Array(pos)),
      nbo: makeBuffer(gl.ARRAY_BUFFER, new Float32Array(nor)),
      ibo: makeBuffer(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(idx))
    };
  }

  /* ------------------------------------------------ geometry: torus arcs -- */
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
        pos.push(RING_R * ca + TUBE_R * s * nx + EIGHT_X,
                 RING_R * sa + TUBE_R * s * ny + arc.cy,
                 TUBE_R * s * nz + arc.cz);
        nor.push(nx, ny, nz);
      }
    }
    for (i = 0; i < rows.length - 1; i++) {
      for (j = 0; j < V; j++) {
        var q = i * (V + 1) + j, b = q + V + 1;
        idx.push(q, b, q + 1, b, b + 1, q + 1);
      }
    }
    return finishMesh(arc.color, pos, nor, idx);
  }

  /* -------------------------------------- geometry: extruded 2D outlines -- */
  function signedArea(p) {
    var a = 0, n = p.length / 2;
    for (var i = 0; i < n; i++) {
      var j = (i + 1) % n;
      a += p[2 * i] * p[2 * j + 1] - p[2 * j] * p[2 * i + 1];
    }
    return a / 2;
  }
  function inTriangle(ax, ay, bx, by, cx, cy, px, py) {
    var v0x = cx - ax, v0y = cy - ay, v1x = bx - ax, v1y = by - ay, v2x = px - ax, v2y = py - ay;
    var d00 = v0x * v0x + v0y * v0y, d01 = v0x * v1x + v0y * v1y, d02 = v0x * v2x + v0y * v2y;
    var d11 = v1x * v1x + v1y * v1y, d12 = v1x * v2x + v1y * v2y;
    var inv = 1 / (d00 * d11 - d01 * d01);
    var u = (d11 * d02 - d01 * d12) * inv, v = (d00 * d12 - d01 * d02) * inv;
    return u >= 0 && v >= 0 && u + v < 1;
  }
  // Ear-clipping triangulation of a simple CCW polygon (flat [x,y,...] array).
  function triangulate(p) {
    var n = p.length / 2, V = [], i;
    for (i = 0; i < n; i++) V.push(i);
    var idx = [], guard = 2 * n, v = n - 1;
    while (V.length > 2 && guard-- > 0) {
      var u = v % V.length; v = (u + 1) % V.length; var w = (v + 1) % V.length;
      var ax = p[2 * V[u]], ay = p[2 * V[u] + 1];
      var bx = p[2 * V[v]], by = p[2 * V[v] + 1];
      var cx = p[2 * V[w]], cy = p[2 * V[w] + 1];
      var ear = ((bx - ax) * (cy - ay) - (by - ay) * (cx - ax)) > 1e-9;
      if (ear) {
        for (i = 0; i < V.length && ear; i++) {
          if (i === u || i === v || i === w) continue;
          if (inTriangle(ax, ay, bx, by, cx, cy, p[2 * V[i]], p[2 * V[i] + 1])) ear = false;
        }
      }
      if (ear) {
        idx.push(V[u], V[v], V[w]);
        V.splice(v, 1);
        guard = 2 * V.length;
      }
    }
    return idx;
  }
  function buildExtruded(shape) {
    var p = shape.pts.slice();
    if (signedArea(p) < 0) { // normalize to CCW so side normals face outward
      var r = [];
      for (var q = p.length - 2; q >= 0; q -= 2) r.push(p[q], p[q + 1]);
      p = r;
    }
    var n = p.length / 2, hd = DEPTH / 2, i, j;
    var tris = triangulate(p);
    var pos = [], nor = [], idx = [];

    for (i = 0; i < n; i++) { pos.push(p[2 * i] + shape.x, p[2 * i + 1] + LETTER_Y, hd); nor.push(0, 0, 1); }
    for (i = 0; i < n; i++) { pos.push(p[2 * i] + shape.x, p[2 * i + 1] + LETTER_Y, -hd); nor.push(0, 0, -1); }
    for (i = 0; i < tris.length; i += 3) {
      idx.push(tris[i], tris[i + 1], tris[i + 2]);                 // front
      idx.push(n + tris[i], n + tris[i + 2], n + tris[i + 1]);     // back
    }
    for (i = 0; i < n; i++) {                                      // side walls
      j = (i + 1) % n;
      var dx = p[2 * j] - p[2 * i], dy = p[2 * j + 1] - p[2 * i + 1];
      var len = Math.sqrt(dx * dx + dy * dy) || 1;
      var nx = dy / len, ny = -dx / len;
      var base = pos.length / 3;
      pos.push(p[2 * i] + shape.x, p[2 * i + 1] + LETTER_Y, hd,
               p[2 * j] + shape.x, p[2 * j + 1] + LETTER_Y, hd,
               p[2 * j] + shape.x, p[2 * j + 1] + LETTER_Y, -hd,
               p[2 * i] + shape.x, p[2 * i + 1] + LETTER_Y, -hd);
      nor.push(nx, ny, 0, nx, ny, 0, nx, ny, 0, nx, ny, 0);
      idx.push(base, base + 1, base + 2, base, base + 2, base + 3);
    }
    return finishMesh(shape.color, pos, nor, idx);
  }

  var meshes = ARCS.map(buildArc).concat(SHAPES.map(buildExtruded));

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

    var ry = Math.sin(t * 0.22) * 0.30 + px * 0.28;
    var rx = -0.14 + Math.sin(t * 0.15) * 0.04 + py * 0.18;
    var bob = Math.sin(t * 0.55) * 0.05;

    var model = multiply(translate(0, bob, 0),
                multiply(rotZ(GROUP_TILT_Z),
                multiply(rotY(ry),
                multiply(rotX(rx), scaleM(GROUP_SCALE)))));
    var view = translate(0, 0, -CAMERA_Z);
    var proj = perspective(FOV, canvas.width / Math.max(1, canvas.height), 0.1, 40);
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
