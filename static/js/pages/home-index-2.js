(function () {
  'use strict';

  // ===== Hero carousel =====
  var hero = document.querySelector('.xh-hero');
  if (hero) {
    var slides = [].slice.call(hero.querySelectorAll('.xh-slide'));
    var tabs = [].slice.call(hero.querySelectorAll('.xh-tab'));
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var idx = 0;

    function show(i) {
      idx = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        s.classList.toggle('is-active', n === idx);
        s.setAttribute('aria-hidden', n === idx ? 'false' : 'true');
      });
      tabs.forEach(function (t, n) {
        t.classList.toggle('is-active', n === idx);
        t.setAttribute('aria-pressed', n === idx ? 'true' : 'false');
      });
      hero.classList.remove('is-running');   // restart the timer bar
      void hero.offsetWidth;
      if (!reduce) hero.classList.add('is-running');
    }

    // the timer bar finishing means "go to the next slide"; pausing the bar pauses autoplay
    hero.addEventListener('animationend', function (e) {
      if (e.animationName === 'xhTimer') show(idx + 1);
    });
    tabs.forEach(function (t, n) { t.addEventListener('click', function () { show(n); }); });
    document.getElementById('xhPrev').addEventListener('click', function () { show(idx - 1); });
    document.getElementById('xhNext').addEventListener('click', function () { show(idx + 1); });

    function pause() { hero.classList.add('is-paused'); }
    function resume() { hero.classList.remove('is-paused'); }
    hero.addEventListener('mouseenter', pause);
    hero.addEventListener('mouseleave', resume);
    hero.addEventListener('focusin', pause);
    hero.addEventListener('focusout', resume);
    hero.addEventListener('touchstart', pause, { passive: true });
    hero.addEventListener('touchend', resume, { passive: true });
    document.addEventListener('visibilitychange', function () { document.hidden ? pause() : resume(); });
    hero.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
    show(0);
  }

  // ===== Client logos: seamless marquee =====
  var marquee = document.querySelector('.xh-marquee');
  var track = document.getElementById('xhTrack');
  if (marquee && track && track.children.length) {
    [].slice.call(track.children).forEach(function (li) {
      var c = li.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      var img = c.querySelector('img');
      if (img) img.setAttribute('alt', '');
      track.appendChild(c);
    });
    marquee.classList.add('is-ready');
  }

  // ===== Counters + scroll reveal =====
  var counters = [].slice.call(document.querySelectorAll('.xh-count'));
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

    var items = [].slice.call(document.querySelectorAll('.xh-card, .xh-dcard, .xh-post, .xh-steps li, .xh-head'));
    document.documentElement.classList.add('xh-js');
    items.forEach(function (n) { n.classList.add('xh-reveal'); });
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); ro.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    items.forEach(function (n) { ro.observe(n); });
  } else {
    counters.forEach(function (c) { c.textContent = c.dataset.count; });
  }

  // ===== Contact form: need at least one service (the server checks everything again) =====
  var form = document.getElementById('xhForm');
  if (form) {
    var err = document.getElementById('xhServicesErr');
    form.addEventListener('submit', function (e) {
      var any = form.querySelector('input[name="services"]:checked');
      err.hidden = !!any;
      if (!any) {
        e.preventDefault();
        var first = form.querySelector('input[name="services"]');
        if (first) first.focus();
      }
    });
  }
})();