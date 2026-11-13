(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function headerOffset() {
    var bar = document.getElementById('bar');
    return (bar ? bar.offsetHeight : 64) + 12;
  }

  function smoothScrollToY(targetY) {
    window.scrollTo({
      top: Math.max(0, targetY),
      behavior: reduceMotion ? 'auto' : 'smooth',
    });
  }

  function scrollToId(id, updateHash) {
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    var y = el.getBoundingClientRect().top + window.scrollY - headerOffset();
    smoothScrollToY(y);
    if (updateHash && history.replaceState) {
      history.replaceState(null, '', '#' + id);
    } else if (updateHash) {
      location.hash = id;
    }
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest('a[href^="#"]');
    if (!link) return;
    var raw = link.getAttribute('href');
    if (!raw || raw === '#') return;
    var id = decodeURIComponent(raw.slice(1));
    var target = document.getElementById(id);
    if (!target) return;
    if (link.target === '_blank' || event.defaultPrevented) return;
    event.preventDefault();
    scrollToId(id, true);
    if (!reduceMotion) target.focus({ preventScroll: true });
  });

  if (location.hash.length > 1) {
    requestAnimationFrame(function () {
      scrollToId(decodeURIComponent(location.hash.slice(1)), false);
    });
  }

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
