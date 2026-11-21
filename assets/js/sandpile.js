/**
 * Bak-Tang-Wiesenfeld Abelian Sandpile (z_c = 4) on a rounded-corner lattice
 * Pre-relaxed into a Self-Organized Criticality (SOC) recurrent state
 * + scroll-reveal choreography for yuxichau.com homepage
 */
(function () {
  var canvas = document.getElementById('sj-sandpile');
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext('2d', { alpha: false });
    var countEl = document.getElementById('sj-sand-count');
    var pauseBtn = document.getElementById('sj-sand-pause');
    var resetBtn = document.getElementById('sj-sand-reset');

    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var BG = '#f5f4ef';
    var COLORS = [
      '#f5f4ef', // 0: warm paper
      '#e2eae0', // 1: whisper sage
      '#a6bcad', // 2: muted lichen
      '#235a47', // 3: deep forest (critical threshold)
      '#8d4c2d'  // 4+: vermilion topple flash
    ];

    var cols = 0;
    var rows = 0;
    var cell = 13;
    var gap = 2;
    var offsetX = 0;
    var offsetY = 0;
    var cssW = 960;
    var cssH = 480;
    var grid = null;
    var nextGrid = null;
    var mask = null;
    var flash = null;

    var paused = reducedMotion;
    var inView = true;
    var dragging = false;
    var totalTopples = 0;
    var lastDrip = 0;
    var lastTick = 0;

    function initGrid() {
      var rect = canvas.getBoundingClientRect();
      cssW = Math.max(260, Math.floor(rect.width));
      cssH = Math.max(220, Math.floor(rect.height));
      var dpr = Math.min(window.devicePixelRatio || 1, 2);

      canvas.width = Math.floor(cssW * dpr);
      canvas.height = Math.floor(cssH * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      cell = cssW < 540 ? 11 : 13;
      gap = 2;
      var step = cell + gap;

      cols = Math.max(18, Math.floor((cssW - 8) / step));
      rows = Math.max(12, Math.floor((cssH - 8) / step));
      offsetX = Math.floor((cssW - (cols * step - gap)) / 2);
      offsetY = Math.floor((cssH - (rows * step - gap)) / 2);

      grid = new Uint16Array(cols * rows);
      nextGrid = new Uint16Array(cols * rows);
      mask = new Uint8Array(cols * rows);
      flash = new Uint8Array(cols * rows);

      // Rounded-rectangle (cartographic plate) cell mask: corners step inward smoothly
      var cornerR = Math.max(4, Math.min(Math.floor(rows * 0.38), Math.floor(cols * 0.22)));
      var innerX1 = cornerR - 0.5;
      var innerX2 = cols - 1 - (cornerR - 0.5);
      var innerY1 = cornerR - 0.5;
      var innerY2 = rows - 1 - (cornerR - 0.5);
      var r2 = cornerR * cornerR;

      for (var y = 0; y < rows; y++) {
        for (var x = 0; x < cols; x++) {
          var dx = 0;
          var dy = 0;
          if (x < innerX1) dx = innerX1 - x;
          else if (x > innerX2) dx = x - innerX2;
          if (y < innerY1) dy = innerY1 - y;
          else if (y > innerY2) dy = y - innerY2;
          if (dx * dx + dy * dy <= r2) {
            mask[y * cols + x] = 1;
          }
        }
      }

      seedCriticalState();
      draw();
      updateCounter();
    }

    function seedCriticalState() {
      grid.fill(0);
      flash.fill(0);
      var len = cols * rows;
      for (var i = 0; i < len; i++) {
        if (!mask[i]) continue;
        var h = (((i + 1) * 2654435761) >>> 0);
        grid[i] = 3 + ((h & 3) === 0 ? 1 : 0) + ((h & 15) === 0 ? 1 : 0);
      }
      for (var iter = 0; iter < 450; iter++) {
        if (!stepRelax(false)) break;
      }
      for (var d = 0; d < 24; d++) {
        var rx = Math.floor(((d * 37 + 13) % cols));
        var ry = Math.floor(((d * 19 + 7) % rows));
        var idx = ry * cols + rx;
        if (mask[idx]) {
          grid[idx] += 1;
          for (var s = 0; s < 80; s++) {
            if (!stepRelax(false)) break;
          }
        }
      }
      flash.fill(0);
      totalTopples = 0;
    }

    function stepRelax(recordFlash) {
      var toppled = false;
      nextGrid.set(grid);

      for (var y = 0; y < rows; y++) {
        var rowOff = y * cols;
        for (var x = 0; x < cols; x++) {
          var idx = rowOff + x;
          if (!mask[idx]) continue;
          var val = grid[idx];
          if (val >= 4) {
            toppled = true;
            var spills = val >> 2;
            nextGrid[idx] -= spills << 2;
            if (x > 0 && mask[idx - 1]) nextGrid[idx - 1] += spills;
            if (x + 1 < cols && mask[idx + 1]) nextGrid[idx + 1] += spills;
            if (y > 0 && mask[idx - cols]) nextGrid[idx - cols] += spills;
            if (y + 1 < rows && mask[idx + cols]) nextGrid[idx + cols] += spills;
            if (recordFlash) {
              flash[idx] = 2;
              totalTopples += spills;
            }
          }
        }
      }

      if (toppled) {
        var tmp = grid;
        grid = nextGrid;
        nextGrid = tmp;
      }
      return toppled;
    }

    function drawTile(px, py, size, radius) {
      if (ctx.roundRect) {
        ctx.beginPath();
        ctx.roundRect(px, py, size, size, radius);
        ctx.fill();
      } else {
        ctx.fillRect(px, py, size, size);
      }
    }

    function draw() {
      ctx.fillStyle = BG;
      ctx.fillRect(0, 0, cssW, cssH);

      var step = cell + gap;
      var tileR = 2.5;
      for (var y = 0; y < rows; y++) {
        var py = offsetY + y * step;
        var rowOff = y * cols;
        for (var x = 0; x < cols; x++) {
          var idx = rowOff + x;
          if (!mask[idx]) continue;
          var v = grid[idx];
          var f = flash[idx];
          var color;
          if (f > 0 || v >= 4) {
            color = COLORS[4];
            if (f > 0) flash[idx] = f - 1;
          } else {
            color = COLORS[v];
          }
          if (color !== BG) {
            ctx.fillStyle = color;
            drawTile(offsetX + x * step, py, cell, tileR);
          }
        }
      }
    }

    function updateCounter() {
      if (countEl) {
        countEl.textContent = totalTopples.toLocaleString() + ' topples';
      }
    }

    function dropAtClient(clientX, clientY, amount) {
      var rect = canvas.getBoundingClientRect();
      var step = cell + gap;
      var gx = Math.floor((clientX - rect.left - offsetX) / step);
      var gy = Math.floor((clientY - rect.top - offsetY) / step);
      if (gx >= 0 && gx < cols && gy >= 0 && gy < rows && mask[gy * cols + gx]) {
        var idx = gy * cols + gx;
        grid[idx] += amount;
        flash[idx] = 2;
        if (paused) {
          stepRelax(true);
          draw();
          updateCounter();
        }
      }
    }

    function loop(ts) {
      requestAnimationFrame(loop);
      if (paused || !inView || document.hidden) return;

      if (ts - lastDrip > 700) {
        lastDrip = ts;
        for (var tries = 0; tries < 8; tries++) {
          var rx = Math.floor(Math.random() * cols);
          var ry = Math.floor(Math.random() * rows);
          var idx = ry * cols + rx;
          if (mask[idx]) {
            grid[idx] += 1;
            break;
          }
        }
      }

      if (ts - lastTick >= 45) {
        lastTick = ts;
        var didTopple = stepRelax(true);
        draw();
        if (didTopple) updateCounter();
      }
    }

    canvas.addEventListener('pointerdown', function (e) {
      dragging = true;
      dropAtClient(e.clientX, e.clientY, 4);
    });
    window.addEventListener('pointerup', function () { dragging = false; });
    canvas.addEventListener('pointermove', function (e) {
      if (dragging) dropAtClient(e.clientX, e.clientY, 2);
    });

    if (pauseBtn) {
      var syncPause = function () {
        pauseBtn.textContent = paused ? 'resume' : 'pause';
        pauseBtn.setAttribute('aria-pressed', String(paused));
      };
      syncPause();
      pauseBtn.addEventListener('click', function () {
        paused = !paused;
        syncPause();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        seedCriticalState();
        draw();
        updateCounter();
      });
    }

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
      }, { threshold: 0.05 }).observe(canvas);
    }

    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(initGrid, 150);
    });

    initGrid();
    requestAnimationFrame(loop);
  }

  // Reveal site header once user scrolls past the opening sandpile stage
  var stage = document.getElementById('sj-opening');
  var header = document.querySelector('body.layout--home .sj-header');
  if (stage && header && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      header.classList.toggle('is-visible', !entries[0].isIntersecting);
    }, { threshold: 0.35 }).observe(stage);
  } else if (header) {
    header.classList.add('is-visible');
  }

  // Reveal narrative beats one by one on scroll
  var beats = Array.prototype.slice.call(document.querySelectorAll('.sj-beat'));
  if (beats.length && 'IntersectionObserver' in window && !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var beatObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          beatObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.32 });
    beats.forEach(function (b) { beatObserver.observe(b); });
  } else {
    beats.forEach(function (b) { b.classList.add('is-visible'); });
  }
})();
