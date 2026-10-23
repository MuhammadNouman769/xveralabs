(function () {
  'use strict';

  var backBtn = document.getElementById('btrBackTop');
  if (!backBtn) return;

  var SHOW_AFTER = 300;
  var isVisible = false;

  function toggleBackTop() {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    var shouldShow = y > SHOW_AFTER;
    if (shouldShow !== isVisible) {
      backBtn.classList.toggle('visible', shouldShow);
      isVisible = shouldShow;
    }
  }

  window.addEventListener('scroll', toggleBackTop, { passive: true });
  window.addEventListener('load', toggleBackTop);
  toggleBackTop();

  backBtn.addEventListener('click', function () {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });
})();