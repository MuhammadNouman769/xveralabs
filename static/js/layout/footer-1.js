(function () {
  'use strict';
  var btn = document.getElementById('xfTop');
  if (!btn) return;
  var on = false;
  function check() {
    var show = (window.pageYOffset || document.documentElement.scrollTop) > 300;
    if (show !== on) { btn.classList.toggle('is-on', show); on = show; }
  }
  window.addEventListener('scroll', check, { passive: true });
  window.addEventListener('load', check);
  check();
  btn.addEventListener('click', function () {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
})();