(function () {
  var FRAMES = 48, COLS = 7, ROWS = 7;
  var sprite = document.getElementById('sprite');
  var story = document.getElementById('story');
  var bar = document.getElementById('bar');
  if (!sprite || !story) return;
  var last = -1, ticking = false;
  function setFrame(f) {
    if (f === last) return;
    last = f;
    var c = f % COLS, r = Math.floor(f / COLS);
    sprite.style.backgroundPosition = (c * 100 / (COLS - 1)) + '% ' + (r * 100 / (ROWS - 1)) + '%';
  }
  function update() {
    ticking = false;
    var rect = story.getBoundingClientRect();
    var travel = story.offsetHeight - window.innerHeight;
    var p = travel > 0 ? Math.min(1, Math.max(0, -rect.top / travel)) : 0;
    setFrame(Math.min(FRAMES - 1, Math.floor(p * FRAMES)));
    if (bar) bar.classList.toggle('solid', window.scrollY > 40);
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
