// Service pages: reveal on scroll, on-page nav highlight, FAQ one-open-at-a-time
(function () {
  'use strict';
  var root = document.querySelector('.sv');
  if (!root) return;

  var items = [].slice.call(root.querySelectorAll('.sv-reveal'));
  if (items.length && 'IntersectionObserver' in window) {
    root.classList.add('sv-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  var links = [].slice.call(document.querySelectorAll('#svSub a[data-spy]'));
  var sections = links.map(function (a) { return document.getElementById(a.getAttribute('data-spy')); }).filter(Boolean);
  if (links.length && sections.length && 'IntersectionObserver' in window) {
    var seen = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { seen[e.target.id] = e.isIntersecting; });
      var current = null;
      sections.forEach(function (s) { if (seen[s.id]) current = s.id; });
      links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('data-spy') === current); });
      var act = document.querySelector('#svSub a.is-active'), bar = document.querySelector('.sv-sub__in');
      if (act && bar && bar.scrollWidth > bar.clientWidth) bar.scrollTo({ left: act.offsetLeft - 24, behavior: 'smooth' });
    }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  [].slice.call(document.querySelectorAll('[data-faq]')).forEach(function (faq) {
    var all = [].slice.call(faq.querySelectorAll('details'));
    all.forEach(function (d) {
      d.addEventListener('toggle', function () { if (d.open) all.forEach(function (o) { if (o !== d) o.open = false; }); });
    });
  });
})();