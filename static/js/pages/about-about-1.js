// ABOUT PAGE: ONE file (reveal, counters, ecosystem tabs, leadership slider)
(function () {
  'use strict';

  // ===== Counters + scroll reveal =====
  var counters = [].slice.call(document.querySelectorAll('.xa-count'));
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, target = parseInt(el.dataset.count, 10) || 0, start = performance.now();
        (function step(now) {
          var p = Math.min((now - start) / 1600, 1);
          el.textContent = Math.floor((1 - Math.pow(1 - p, 3)) * target);
          if (p < 1) requestAnimationFrame(step); else el.textContent = target;
        })(start);
        co.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { co.observe(c); });

    var items = [].slice.call(document.querySelectorAll('.xa-reveal'));
    if (items.length) {
      document.documentElement.classList.add('xa-js');
      var ro = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('is-in'); ro.unobserve(en.target); }
        });
      }, { threshold: 0.12 });
      items.forEach(function (n, i) { n.style.transitionDelay = ((i % 3) * 0.08) + 's'; ro.observe(n); });
    }
  } else {
    counters.forEach(function (c) { c.textContent = c.dataset.count; });
  }

  // ===== Ecosystem tabs (click + arrow keys) =====
  var tabs = [].slice.call(document.querySelectorAll('#xaEcoBox [role="tab"]'));
  if (tabs.length) {
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    var select = function (i, focus) {
      tabs.forEach(function (tab, n) {
        var on = n === i;
        tab.classList.toggle('is-active', on);
        tab.setAttribute('aria-selected', on ? 'true' : 'false');
        tab.tabIndex = on ? 0 : -1;
        if (panels[n]) { panels[n].hidden = !on; panels[n].classList.toggle('is-active', on); }
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(i, false); });
      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') next = (i + 1) % tabs.length;
        if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') next = (i - 1 + tabs.length) % tabs.length;
        if (e.key === 'Home') next = 0;
        if (e.key === 'End') next = tabs.length - 1;
        if (next !== null) { e.preventDefault(); select(next, true); }
      });
    });
  }
})();

// ===== Leadership slider =====
document.addEventListener('DOMContentLoaded', function () {
  var slider = document.getElementById('xaSlider');
  var left = document.getElementById('leftBtn');
  var right = document.getElementById('rightBtn');
  if (!slider || !left || !right) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function step() {   // one card + the gap
    var card = slider.querySelector('.xa-member');
    var gap = parseFloat(getComputedStyle(slider).columnGap) || 0;
    return (card ? card.getBoundingClientRect().width : 320) + gap;
  }
  function update() {
    var max = slider.scrollWidth - slider.clientWidth - 2;
    left.disabled = slider.scrollLeft <= 2;
    right.disabled = slider.scrollLeft >= max;
  }
  function go(dir) { slider.scrollBy({ left: dir * step(), behavior: reduce ? 'auto' : 'smooth' }); }

  right.addEventListener('click', function () { go(1); });
  left.addEventListener('click', function () { go(-1); });
  var ticking = false;
  slider.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { update(); ticking = false; });
  }, { passive: true });
  window.addEventListener('resize', update);
  update();
});