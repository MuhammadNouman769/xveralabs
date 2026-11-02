// Legal pages: highlight the table-of-contents link of the section being read
(function () {
  'use strict';
  var links = [].slice.call(document.querySelectorAll('.lg-toc a[href^="#"]'));
  var sections = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); }).filter(Boolean);
  if (!links.length || !sections.length || !('IntersectionObserver' in window)) return;

  var seen = {};
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { seen[e.target.id] = e.isIntersecting; });
    var current = null;
    sections.forEach(function (s) { if (seen[s.id]) current = s.id; });
    if (!current) return;
    links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + current); });
  }, { rootMargin: '-20% 0px -65% 0px', threshold: 0 });
  sections.forEach(function (s) { io.observe(s); });
})();