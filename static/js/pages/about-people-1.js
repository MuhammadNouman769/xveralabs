// PEOPLE PAGE: the line fills as you scroll, stops light up, the sticky bar follows the section on screen
(function () {
  'use strict';
  var root = document.getElementById('xpRoot');
  if (!root) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;   // page is fully visible without JS

  root.classList.add('xp-js');
  var tracks = [].slice.call(root.querySelectorAll('.xp-track'));
  var stops = [].slice.call(root.querySelectorAll('.xp-stop'));
  tracks.forEach(function (t) { t.style.setProperty('--p', '0'); });

  var ticking = false;
  function update() {
    var mid = window.innerHeight * 0.55;
    tracks.forEach(function (t) {
      var r = t.getBoundingClientRect();
      t.style.setProperty('--p', Math.min(1, Math.max(0, (mid - r.top) / r.height)).toFixed(4));
    });
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', update);
  update();

  var stopIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('is-visited'); stopIO.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -30% 0px', threshold: 0.15 });
  stops.forEach(function (s) { stopIO.observe(s); });

  var links = [].slice.call(document.querySelectorAll('.xp-bar a[data-spy]'));
  var sections = links.map(function (a) { return document.getElementById(a.getAttribute('data-spy')); }).filter(Boolean);
  var visible = {};
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
    var cur = null;
    sections.forEach(function (s) { if (visible[s.id]) cur = s.id; });
    links.forEach(function (a) {
      var on = a.getAttribute('data-spy') === cur;
      a.classList.toggle('is-active', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
  }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });
  sections.forEach(function (s) { spy.observe(s); });
})();