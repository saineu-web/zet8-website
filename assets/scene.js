/* ============================================================================
   ZET8 scroll scene — a camera journey along a glowing lemniscate (the brand's
   "8") with one stop per product. Each stop is a floating 3D panel rendered
   with the product's real content (drawn to a canvas texture), synced with an
   HTML text card, HUD, minimap and progress rail.

   Raw WebGL 1, zero dependencies. Reads product data from window.ZET8_PRODUCTS
   (injected by build.py — single source of truth).

   Progressive enhancement: without WebGL or with prefers-reduced-motion the
   page never gets the `scene-on` class and renders as a normal static page.
   ============================================================================ */
(function () {
  'use strict';

  var canvas = document.getElementById('scene');
  var products = window.ZET8_PRODUCTS;
  if (!canvas || !products) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var gl = canvas.getContext('webgl', { alpha: false, antialias: true, preserveDrawingBuffer: true });
  if (!gl) return;

  document.documentElement.classList.add('scene-on');

  /* ------------------------------------------------------------- config -- */
  var STEPS = products.length + 2;             // hero + products + outro
  var ACCENT = '#F4C82D';
  var A = 130, DROP = 78;                      // lemniscate size / descent
  var FOG_D = 0.0052;
  var LOOK_AHEAD = 0.028;

  /* -------------------------------------------------------- small math -- */
  function v3(x, y, z) { return [x, y, z]; }
  function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function add(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  function scl(a, s) { return [a[0] * s, a[1] * s, a[2] * s]; }
  function cross(a, b) {
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  }
  function norm(a) {
    var l = Math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]) || 1;
    return [a[0] / l, a[1] / l, a[2] / l];
  }
  function mul4(a, b) {
    var o = new Array(16);
    for (var r = 0; r < 4; r++) for (var c = 0; c < 4; c++) {
      o[c * 4 + r] = a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1] + a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3];
    }
    return o;
  }
  function ident() { return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]; }
  function persp(fov, aspect, near, far) {
    var f = 1 / Math.tan(fov / 2), nf = 1 / (near - far);
    return [f / aspect,0,0,0, 0,f,0,0, 0,0,(far + near) * nf,-1, 0,0,2 * far * near * nf,0];
  }
  function lookAtM(eye, target, up) {
    var z = norm(sub(eye, target));
    var x = norm(cross(up, z));
    var y = cross(z, x);
    return [x[0],y[0],z[0],0, x[1],y[1],z[1],0, x[2],y[2],z[2],0,
            -(x[0]*eye[0]+x[1]*eye[1]+x[2]*eye[2]),
            -(y[0]*eye[0]+y[1]*eye[1]+y[2]*eye[2]),
            -(z[0]*eye[0]+z[1]*eye[1]+z[2]*eye[2]), 1];
  }

  /* ---------------------------------------------- the "8" as a 3D path -- */
  function curveAt(u) {
    var t = u * Math.PI * 2 + Math.PI / 2;
    var den = 1 + Math.sin(t) * Math.sin(t);
    return v3(A * Math.cos(t) / den, -u * DROP, A * Math.sin(t) * Math.cos(t) / den);
  }
  function tangentAt(u) {
    return norm(sub(curveAt(Math.min(u + 0.001, 1)), curveAt(Math.max(u - 0.001, 0))));
  }
  var UP = [0, 1, 0];

  /* ------------------------------------------------------------ shaders -- */
  function program(vs, fs) {
    function sh(type, src) {
      var s = gl.createShader(type);
      gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    }
    var p = gl.createProgram();
    gl.attachShader(p, sh(gl.VERTEX_SHADER, vs));
    gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(p);
    return p;
  }
  var FOG_FN =
    'float fogf(float d){ float f = exp(-' + FOG_D + '*' + FOG_D + '*d*d); return clamp(f,0.0,1.0); }';

  var flatProg = program(
    'attribute vec3 aPos; uniform mat4 uMVP; uniform mat4 uMV; varying float vDist; uniform float uPointSize;' +
    'void main(){ vec4 mv = uMV * vec4(aPos,1.0); vDist = length(mv.xyz);' +
    ' gl_PointSize = uPointSize * (140.0 / max(vDist, 1.0)); gl_Position = uMVP * vec4(aPos,1.0); }',
    'precision mediump float; uniform vec3 uColor; uniform float uOpacity; varying float vDist;' + FOG_FN +
    'void main(){ gl_FragColor = vec4(uColor, uOpacity * fogf(vDist)); }'
  );
  var texProg = program(
    'attribute vec3 aPos; attribute vec2 aUV; uniform mat4 uMVP; uniform mat4 uMV;' +
    'varying vec2 vUV; varying float vDist;' +
    'void main(){ vec4 mv = uMV * vec4(aPos,1.0); vDist = length(mv.xyz); vUV = aUV;' +
    ' gl_Position = uMVP * vec4(aPos,1.0); }',
    'precision mediump float; uniform sampler2D uTex; uniform float uOpacity; varying vec2 vUV; varying float vDist;' + FOG_FN +
    'void main(){ vec4 c = texture2D(uTex, vUV); float f = fogf(vDist);' +
    ' gl_FragColor = vec4(mix(vec3(0.0), c.rgb, f), c.a * uOpacity); }'
  );
  function locs(p, names) {
    var o = {};
    names.forEach(function (n) {
      o[n] = n[0] === 'a' ? gl.getAttribLocation(p, n) : gl.getUniformLocation(p, n);
    });
    return o;
  }
  var FL = locs(flatProg, ['aPos', 'uMVP', 'uMV', 'uColor', 'uOpacity', 'uPointSize']);
  var TL = locs(texProg, ['aPos', 'aUV', 'uMVP', 'uMV', 'uTex', 'uOpacity']);

  function buffer(target, data) {
    var b = gl.createBuffer();
    gl.bindBuffer(target, b);
    gl.bufferData(target, data, gl.STATIC_DRAW);
    return b;
  }

  /* --------------------------------------------------------- geometries -- */
  // Tube swept along the lemniscate (the glowing rail).
  function tubeMesh(radius, uSteps, vSteps) {
    var pos = [], idx = [], i, j;
    for (i = 0; i <= uSteps; i++) {
      var u = i / uSteps;
      var c = curveAt(u), tan = tangentAt(u);
      var side = norm(cross(tan, UP)), up2 = norm(cross(side, tan));
      for (j = 0; j <= vSteps; j++) {
        var a = j / vSteps * Math.PI * 2;
        var off = add(scl(side, Math.cos(a) * radius), scl(up2, Math.sin(a) * radius));
        pos.push(c[0] + off[0], c[1] + off[1], c[2] + off[2]);
      }
    }
    for (i = 0; i < uSteps; i++) for (j = 0; j < vSteps; j++) {
      var q = i * (vSteps + 1) + j, b = q + vSteps + 1;
      idx.push(q, b, q + 1, b, b + 1, q + 1);
    }
    return { vbo: buffer(gl.ARRAY_BUFFER, new Float32Array(pos)),
             ibo: buffer(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(idx)),
             count: idx.length, mode: gl.TRIANGLES };
  }
  var rail = tubeMesh(0.28, 420, 6);
  var railGlow = tubeMesh(1.5, 220, 6);

  // Floor grid (line list).
  var gridLines = (function () {
    var p = [], S = 1400, N = 70, y = -110;
    for (var i = 0; i <= N; i++) {
      var v = -S / 2 + (i / N) * S;
      p.push(-S / 2, y, v, S / 2, y, v, v, y, -S / 2, v, y, S / 2);
    }
    return { vbo: buffer(gl.ARRAY_BUFFER, new Float32Array(p)), count: p.length / 3, mode: gl.LINES };
  })();

  // Ambient dust (points).
  var dustCount = window.innerWidth < 860 ? 600 : 1400;
  var dust = (function () {
    var p = new Float32Array(dustCount * 3);
    for (var i = 0; i < dustCount; i++) {
      p[i * 3] = (Math.random() - 0.5) * 520;
      p[i * 3 + 1] = (Math.random() - 0.5) * 220 - 40;
      p[i * 3 + 2] = (Math.random() - 0.5) * 520;
    }
    return { vbo: buffer(gl.ARRAY_BUFFER, p), count: dustCount, mode: gl.POINTS };
  })();

  // Accent ring (line loop, baked per node with a tilt).
  function ringLines(center, radius, tilt) {
    var p = [], N = 72;
    var ex = [1, 0, 0], ey = [0, Math.sin(tilt), Math.cos(tilt)];
    for (var i = 0; i < N; i++) {
      var a0 = i / N * Math.PI * 2, a1 = (i + 1) / N * Math.PI * 2;
      var q0 = add(center, add(scl(ex, Math.cos(a0) * radius), scl(ey, Math.sin(a0) * radius)));
      var q1 = add(center, add(scl(ex, Math.cos(a1) * radius), scl(ey, Math.sin(a1) * radius)));
      p.push(q0[0], q0[1], q0[2], q1[0], q1[1], q1[2]);
    }
    return { vbo: buffer(gl.ARRAY_BUFFER, new Float32Array(p)), count: p.length / 3, mode: gl.LINES };
  }

  // Unit quad (billboarded per frame in JS). w/h in world units, UVs for tex.
  function quad(w, h, z) {
    var x = w / 2, y = h / 2;
    return {
      vbo: buffer(gl.ARRAY_BUFFER, new Float32Array([-x,-y,z, x,-y,z, x,y,z, -x,y,z])),
      uvo: buffer(gl.ARRAY_BUFFER, new Float32Array([0,1, 1,1, 1,0, 0,0])),
      ibo: buffer(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array([0,1,2, 0,2,3])),
      count: 6, mode: gl.TRIANGLES
    };
  }

  /* ------------------------------------- product panel canvas textures -- */
  function hexRGB(hex) {
    return [parseInt(hex.slice(1, 3), 16) / 255,
            parseInt(hex.slice(3, 5), 16) / 255,
            parseInt(hex.slice(5, 7), 16) / 255];
  }
  function drawPanel(p) {
    var W = 512, H = 640, c = document.createElement('canvas');
    c.width = W; c.height = H;
    var x = c.getContext('2d');
    var disp = '"Space Grotesk",Bahnschrift,"Segoe UI",sans-serif';
    var mono = '"JetBrains Mono",Consolas,monospace';

    function rr(x0, y0, w, h, r) {
      x.beginPath();
      x.moveTo(x0 + r, y0);
      x.arcTo(x0 + w, y0, x0 + w, y0 + h, r);
      x.arcTo(x0 + w, y0 + h, x0, y0 + h, r);
      x.arcTo(x0, y0 + h, x0, y0, r);
      x.arcTo(x0, y0, x0 + w, y0, r);
      x.closePath();
    }
    x.clearRect(0, 0, W, H);
    rr(6, 6, W - 12, H - 12, 26);
    x.fillStyle = '#0B0C0E'; x.fill();
    x.strokeStyle = p.hex; x.lineWidth = 3; x.stroke();

    // window chrome dots
    x.fillStyle = '#26292E';
    [0, 1, 2].forEach(function (i) {
      x.beginPath(); x.arc(44 + i * 26, 46, 6, 0, 7); x.fill();
    });
    x.font = '500 19px ' + mono;
    x.fillStyle = '#79837A';
    x.textAlign = 'right';
    x.fillText(p.domain, W - 42, 53);
    x.textAlign = 'left';

    // category chip
    x.font = '500 20px ' + mono;
    var cw = x.measureText(p.cat.toUpperCase()).width;
    rr(40, 92, cw + 34, 40, 8);
    x.fillStyle = p.hex + '22'; x.fill();
    x.fillStyle = p.hex;
    x.fillText(p.cat.toUpperCase(), 57, 119);

    // name + tagline
    x.fillStyle = '#F4F1EA';
    x.font = '700 62px ' + disp;
    x.fillText(p.name, 40, 208);
    x.font = '500 27px ' + disp;
    x.fillStyle = p.hex;
    wrap(p.tagline, 40, 254, W - 80, 34);

    // features (up to four)
    x.font = '400 23px ' + disp;
    var fy = 348;
    p.features.forEach(function (f) {
      x.fillStyle = p.hex;
      x.beginPath(); x.arc(50, fy - 8, 5, 0, 7); x.fill();
      x.fillStyle = '#C9CEC6';
      x.fillText(f, 72, fy);
      fy += 56;
    });

    // divider + pricing
    x.strokeStyle = '#22252A'; x.lineWidth = 2;
    x.beginPath(); x.moveTo(40, H - 84); x.lineTo(W - 40, H - 84); x.stroke();
    x.font = '500 20px ' + mono;
    x.fillStyle = '#79837A';
    wrap(p.pricing, 40, H - 46, W - 80, 26);

    function wrap(text, tx, ty, maxW, lh) {
      var words = text.split(' '), line = '';
      words.forEach(function (w) {
        var t = line ? line + ' ' + w : w;
        if (x.measureText(t).width > maxW && line) { x.fillText(line, tx, ty); ty += lh; line = w; }
        else line = t;
      });
      x.fillText(line, tx, ty);
    }
    return c;
  }
  function textureFrom(cnv) {
    var t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cnv);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    return t;
  }

  /* --------------------------------------------------------- the nodes -- */
  // Portrait screens get half-size panels, floated above the text card and
  // pulled toward the track center so they stay fully in frame.
  var NARROW = window.innerWidth < 860;
  var PS = NARROW ? 0.5 : 1;
  var SIDE_OFF = NARROW ? 2.6 : 13;
  var UP_OFF = NARROW ? 6.0 : 2.5;
  var screenQuad = quad(15 * PS, 18.75 * PS, 0);
  var backQuad = quad(16 * PS, 19.75 * PS, -0.25);
  var nodes = products.map(function (p, i) {
    var anchor = (i + 1) / (STEPS - 1);
    var u = Math.min(anchor * 0.965 + 0.012 + 0.032, 1);
    var base = curveAt(u), tan = tangentAt(u);
    var side = norm(cross(tan, UP));
    var center = add(add(base, scl(side, SIDE_OFF)), scl(UP, UP_OFF));
    var node = {
      center: center,
      seed: i * 1.7,
      hex: p.hex,
      rgb: hexRGB(p.hex),
      ring: ringLines(center, NARROW ? 5.8 : 11.5, Math.PI / 2.3),
      tex: textureFrom(drawPanel(p))
    };
    return node;
  });
  // Re-render panel textures once webfonts are in.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      nodes.forEach(function (n, i) {
        gl.bindTexture(gl.TEXTURE_2D, n.tex);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, drawPanel(products[i]));
      });
    });
  }

  /* --------------------------------------------------- DOM interactions -- */
  var cards = Array.prototype.slice.call(document.querySelectorAll('.scard'));
  var hudU = document.getElementById('hudU');
  var hudN = document.getElementById('hudN');
  var railFill = document.getElementById('railFill');
  var mmPath = document.getElementById('mmPath');
  var mmDot = document.getElementById('mmDot');

  (function () { // minimap traces the same "8"
    var d = '';
    for (var i = 0; i <= 160; i++) {
      var t = (i / 160) * Math.PI * 2 + Math.PI / 2;
      var den = 1 + Math.sin(t) * Math.sin(t);
      d += (i ? 'L' : 'M') + (43 + 38 * Math.cos(t) / den).toFixed(2) + ' '
         + (23 + 34 * Math.sin(t) * Math.cos(t) / den).toFixed(2) + ' ';
    }
    mmPath.setAttribute('d', d);
  })();
  var mmLen = mmPath.getTotalLength();

  var target = 0, current = 0, tmx = 0, tmy = 0, mx = 0, my = 0;
  var runway = document.querySelector('.runway');
  function readScroll() {
    var max = runway.offsetTop + runway.offsetHeight - window.innerHeight;
    target = max > 0 ? Math.min(Math.max(window.scrollY / max, 0), 1) : 0;
  }
  window.addEventListener('scroll', readScroll, { passive: true });
  window.addEventListener('pointermove', function (e) {
    tmx = e.clientX / window.innerWidth - 0.5;
    tmy = e.clientY / window.innerHeight - 0.5;
  }, { passive: true });

  function resize() {
    var w = window.innerWidth, h = window.innerHeight;
    var dpr = Math.min(window.devicePixelRatio || 1, w < 860 ? 1.5 : 2);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
  window.addEventListener('resize', resize);

  /* --------------------------------------------------------- rendering -- */
  gl.enable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.enable(gl.CULL_FACE);   // hide tube interiors when the camera rides inside
  gl.cullFace(gl.BACK);
  gl.clearColor(0, 0, 0, 1);

  function drawFlat(mesh, mvp, mv, color, opacity, pointSize) {
    gl.useProgram(flatProg);
    gl.uniformMatrix4fv(FL.uMVP, false, new Float32Array(mvp));
    gl.uniformMatrix4fv(FL.uMV, false, new Float32Array(mv));
    gl.uniform3fv(FL.uColor, color);
    gl.uniform1f(FL.uOpacity, opacity);
    gl.uniform1f(FL.uPointSize, pointSize || 1);
    gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vbo);
    gl.enableVertexAttribArray(FL.aPos);
    gl.vertexAttribPointer(FL.aPos, 3, gl.FLOAT, false, 0, 0);
    if (mesh.ibo) {
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, mesh.ibo);
      gl.drawElements(mesh.mode, mesh.count, gl.UNSIGNED_SHORT, 0);
    } else {
      gl.drawArrays(mesh.mode, 0, mesh.count);
    }
  }
  function drawTex(mesh, mvp, mv, tex, opacity) {
    gl.useProgram(texProg);
    gl.uniformMatrix4fv(TL.uMVP, false, new Float32Array(mvp));
    gl.uniformMatrix4fv(TL.uMV, false, new Float32Array(mv));
    gl.uniform1f(TL.uOpacity, opacity);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.uniform1i(TL.uTex, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vbo);
    gl.enableVertexAttribArray(TL.aPos);
    gl.vertexAttribPointer(TL.aPos, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, mesh.uvo);
    gl.enableVertexAttribArray(TL.aUV);
    gl.vertexAttribPointer(TL.aUV, 2, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, mesh.ibo);
    gl.drawElements(mesh.mode, mesh.count, gl.UNSIGNED_SHORT, 0);
  }
  function billboard(center, eye, bobY, tiltZ) {
    var fwd = norm(sub(eye, center));
    var right = norm(cross(UP, fwd));
    var up2 = cross(fwd, right);
    var cz = Math.cos(tiltZ), sz = Math.sin(tiltZ);
    var r = [right[0] * cz + up2[0] * sz, right[1] * cz + up2[1] * sz, right[2] * cz + up2[2] * sz];
    var u = [up2[0] * cz - right[0] * sz, up2[1] * cz - right[1] * sz, up2[2] * cz - right[2] * sz];
    return [r[0],r[1],r[2],0, u[0],u[1],u[2],0, fwd[0],fwd[1],fwd[2],0,
            center[0], center[1] + bobY, center[2], 1];
  }

  var accentRGB = hexRGB(ACCENT);
  var creamRGB = hexRGB('#F4F1EA');
  var last = 0, raf = null, running = true;
  var sceneDone = false;

  function frame(now) {
    raf = null;
    var dt = Math.min((now - last) / 1000, 0.05); last = now;

    current += (target - current) * 0.075;
    mx += (tmx - mx) * 0.06;
    my += (tmy - my) * 0.06;

    resize();
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    var w = window.innerWidth, h = window.innerHeight;
    var fov = (w < 860 ? 68 : 56) * Math.PI / 180;
    var proj = persp(fov, canvas.width / Math.max(1, canvas.height), 0.1, 1200);

    var u = Math.min(Math.max(current * 0.965 + 0.012, 0.001), 0.999);
    var eye = curveAt(u);
    var look = curveAt(Math.min(u + LOOK_AHEAD, 1));
    look[0] += mx * 14; look[1] += my * 8 - 1.5;
    var view = lookAtM(eye, look, UP);
    var vp = mul4(proj, view);
    var I = ident();
    var mvpI = mul4(vp, I);

    // -- opaque content panels (billboarded, real product content) --
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    gl.depthMask(true);
    nodes.forEach(function (n) {
      var bob = Math.sin(now / 1100 + n.seed) * 0.55;
      var tilt = Math.sin(now / 1600 + n.seed) * 0.045;
      var model = billboard(n.center, eye, bob, tilt);
      var mv = mul4(view, model);
      var mvp = mul4(vp, model);
      drawFlat(backQuad, mvp, mv, [0.04, 0.045, 0.05], 1, 1);
      drawTex(screenQuad, mvp, mv, n.tex, 1);
    });

    // -- additive glow layers --
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
    gl.depthMask(false);
    drawFlat(rail, mvpI, view, accentRGB, 0.5, 1);
    drawFlat(railGlow, mvpI, view, accentRGB, 0.05, 1);
    drawFlat(gridLines, mvpI, view, accentRGB, 0.06, 1);
    drawFlat(dust, mvpI, view, creamRGB, 0.35, 2.2);
    nodes.forEach(function (n) {
      drawFlat(n.ring, mvpI, view, n.rgb, 0.4, 1);
    });
    gl.depthMask(true);

    // -- HTML sync: cards, HUD, minimap, rail --
    var activeNode = 0;
    cards.forEach(function (card, i) {
      var anchor = i / (STEPS - 1);
      var dist = Math.abs(current - anchor) * (STEPS - 1);
      var o = Math.max(0, Math.min(1, 1 - dist * 1.45));
      card.style.opacity = o.toFixed(3);
      var dy = ((current - anchor) * (STEPS - 1) * -16).toFixed(1);
      card.style.transform = card.classList.contains('scard-center')
        ? 'translate(-50%,calc(-50% + ' + dy + 'px))'
        : (w <= 860 ? 'translateY(' + dy + 'px)' : 'translateY(calc(-50% + ' + dy + 'px))');
      card.classList.toggle('on', o > 0.02);
      if (o > 0.5 && i >= 1 && i <= products.length) activeNode = i;
    });
    hudU.textContent = current.toFixed(3);
    hudN.textContent = String(activeNode).padStart(2, '0');
    railFill.style.width = (current * 100).toFixed(2) + '%';
    var mp = mmPath.getPointAtLength(mmLen * current);
    mmDot.setAttribute('cx', mp.x); mmDot.setAttribute('cy', mp.y);

    // fade the scene chrome once the journey ends
    var done = current > 0.985;
    if (done !== sceneDone) {
      sceneDone = done;
      document.documentElement.classList.toggle('scene-done', done);
    }

    if (running) raf = requestAnimationFrame(frame);
  }

  document.addEventListener('visibilitychange', function () {
    running = !document.hidden;
    if (running && raf === null) raf = requestAnimationFrame(frame);
    if (!running && raf !== null) { cancelAnimationFrame(raf); raf = null; }
  });

  resize();
  readScroll();
  current = target;
  raf = requestAnimationFrame(frame);

  // Debug/scripting surface: jump the camera to a track position and render.
  window.__zet8Scene = {
    setU: function (v) { current = target = v; frame(performance.now()); },
    renderFrame: function () { frame(performance.now()); }
  };
})();
