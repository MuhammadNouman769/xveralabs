// Campus Ambassador page: reveal on scroll, FAQ one-open-at-a-time, form helpers
(function () {
  'use strict';
  var root = document.querySelector('.cp');
  if (!root) return;

  var items = [].slice.call(root.querySelectorAll('.cp-reveal'));
  if (items.length && 'IntersectionObserver' in window) {
    root.classList.add('cp-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  [].slice.call(document.querySelectorAll('[data-faq]')).forEach(function (faq) {
    var all = [].slice.call(faq.querySelectorAll('details'));
    all.forEach(function (d) {
      d.addEventListener('toggle', function () { if (d.open) all.forEach(function (o) { if (o !== d) o.open = false; }); });
    });
  });

  var form = document.getElementById('cpForm');
  if (!form) return;
  [].slice.call(form.querySelectorAll('[data-count-for]')).forEach(function (counter) {
    var area = form.querySelector('textarea[name="' + counter.getAttribute('data-count-for') + '"]');
    if (!area) return;
    var upd = function () { counter.textContent = area.value.length + ' / ' + (area.getAttribute('maxlength') || 1000); };
    area.addEventListener('input', upd); upd();
  });
  form.addEventListener('submit', function (e) {
    if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return; }
    var btn = form.querySelector('.cp-submit');
    if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }   // stop double submits
  });
})();