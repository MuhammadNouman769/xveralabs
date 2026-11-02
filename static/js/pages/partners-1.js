// Partner pages (Overview, Investors, Apply): one file, every block is guarded
(function () {
  'use strict';
  var root = document.querySelector('.pt');
  if (!root) return;

  // ----- reveal on scroll -----
  var items = [].slice.call(root.querySelectorAll('.pt-reveal'));
  if (items.length && 'IntersectionObserver' in window) {
    root.classList.add('pt-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  // ----- sticky sub-nav: highlight the section being read -----
  var links = [].slice.call(document.querySelectorAll('#ptSub a[data-spy]'));
  var sections = links.map(function (a) { return document.getElementById(a.getAttribute('data-spy')); }).filter(Boolean);
  if (links.length && sections.length && 'IntersectionObserver' in window) {
    var seen = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { seen[e.target.id] = e.isIntersecting; });
      var current = null;
      sections.forEach(function (s) { if (seen[s.id]) current = s.id; });
      links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('data-spy') === current); });
      var act = document.querySelector('#ptSub a.is-active'), bar = document.querySelector('.pt-sub__in');
      if (act && bar && bar.scrollWidth > bar.clientWidth) bar.scrollTo({ left: act.offsetLeft - 24, behavior: 'smooth' });
    }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  // ----- FAQ: one open at a time -----
  [].slice.call(document.querySelectorAll('[data-faq]')).forEach(function (faq) {
    var all = [].slice.call(faq.querySelectorAll('details'));
    all.forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (d.open) all.forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
  });

  // ----- profit-share illustrator (plain arithmetic, illustration only) -----
  var profit = document.getElementById('calcProfit'), range = document.getElementById('calcRange'),
      rate = document.getElementById('calcRate'), result = document.getElementById('calcResult');
  if (profit && range && rate && result) {
    var fmt = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
    var readProfit = function () { var d = profit.value.replace(/[^\d]/g, ''); return Math.min(d ? parseInt(d, 10) : 0, 1e12); };
    var readRate = function () { var r = parseFloat(rate.value); return isNaN(r) || r < 0 ? 0 : Math.min(r, 100); };
    var render = function () { result.textContent = 'PKR ' + fmt.format(Math.round(readProfit() * readRate() / 100)); };
    profit.addEventListener('input', function () { var n = readProfit(); profit.value = n ? fmt.format(n) : ''; render(); });
    range.addEventListener('input', function () { rate.value = range.value; render(); });
    rate.addEventListener('input', function () { range.value = Math.min(readRate(), parseFloat(range.max)); render(); });
    render();
  }

  // ----- apply form -----
  var form = document.getElementById('ptForm');
  if (!form) return;
  var radios = [].slice.call(form.querySelectorAll('input[name="partner_type"]'));
  var typeErr = document.getElementById('ptTypeErr');
  var investor = document.getElementById('ptInvestor');
  var msg = form.querySelector('textarea[name="message"]'), count = document.getElementById('ptCount');

  function syncInvestor() {
    var on = radios.some(function (r) { return r.checked && r.value === 'investor'; });
    if (investor) {
      investor.hidden = !on;
      [].slice.call(investor.querySelectorAll('select')).forEach(function (s) { s.disabled = !on; });
    }
  }
  radios.forEach(function (r) {
    r.addEventListener('change', function () { syncInvestor(); if (typeErr) typeErr.hidden = true; });
  });
  syncInvestor();

  function updateCount() { if (msg && count) count.textContent = msg.value.length + ' / ' + (msg.getAttribute('maxlength') || 1500); }
  if (msg) { msg.addEventListener('input', updateCount); updateCount(); }

  form.addEventListener('submit', function (e) {
    var chosen = radios.some(function (r) { return r.checked; });
    if (!chosen) {
      e.preventDefault();
      if (typeErr) typeErr.hidden = false;
      if (radios[0]) radios[0].focus();
      return;
    }
    if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return; }
    var btn = form.querySelector('.pt-submit');
    if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }   // stop double submits
  });
})();