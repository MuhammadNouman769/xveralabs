document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    var root = document.querySelector('.es');
    if (!root) return;

    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var hasIO = 'IntersectionObserver' in window;

    // JS chal raha hai to reveal animations on (warna sab kuch seedha dikhta hai)
    if (hasIO && !reduceMotion) root.classList.add('js');

    // =============================================
    // REVEAL ON SCROLL
    // =============================================
    var reveals = root.querySelectorAll('.es-reveal');
    if (hasIO && !reduceMotion) {
        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-in');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        reveals.forEach(function (el) { revealObserver.observe(el); });
    }

    // =============================================
    // COUNT-UP NUMBERS
    // =============================================
    function formatNumber(value, decimals) {
        return decimals ? value.toFixed(decimals) : String(Math.round(value));
    }

    function runCount(el) {
        var target = parseFloat(el.getAttribute('data-count'));
        var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
        var suffix = el.getAttribute('data-suffix') || '';
        var duration = 1600;
        var start = null;

        function step(ts) {
            if (start === null) start = ts;
            var progress = Math.min((ts - start) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = formatNumber(target * eased, decimals) + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }

    var counters = root.querySelectorAll('[data-count]');
    if (hasIO && !reduceMotion) {
        var countObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    runCount(entry.target);
                    countObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.6 });
        counters.forEach(function (el) { countObserver.observe(el); });
    }

    // =============================================
    // PROGRAM TABS
    // =============================================
    var tabs = Array.prototype.slice.call(root.querySelectorAll('.es-tab'));
    var panels = Array.prototype.slice.call(root.querySelectorAll('.es-panel'));

    function activateTab(tab, focus) {
        var key = tab.getAttribute('data-tab');
        tabs.forEach(function (t) {
            var on = t === tab;
            t.classList.toggle('is-active', on);
            t.setAttribute('aria-selected', on ? 'true' : 'false');
            t.setAttribute('tabindex', on ? '0' : '-1');
        });
        panels.forEach(function (p) {
            p.hidden = p.id !== 'panel-' + key;
        });
        if (focus) tab.focus();
        if (tab.scrollIntoView) tab.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
    }

    tabs.forEach(function (tab, i) {
        tab.addEventListener('click', function () { activateTab(tab, false); });
        tab.addEventListener('keydown', function (e) {
            var next = null;
            if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
            if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
            if (e.key === 'Home') next = tabs[0];
            if (e.key === 'End') next = tabs[tabs.length - 1];
            if (next) {
                e.preventDefault();
                activateTab(next, true);
            }
        });
    });

    // =============================================
    // TESTIMONIAL SLIDER
    // =============================================
    var slider = document.getElementById('esSlider');
    if (slider) {
        var slides = Array.prototype.slice.call(slider.querySelectorAll('.es-slide'));
        var dotsWrap = document.getElementById('esDots');
        var prevBtn = document.getElementById('esPrev');
        var nextBtn = document.getElementById('esNext');
        var current = 0;
        var timer = null;
        var dots = [];

        slides.forEach(function (_, i) {
            var dot = document.createElement('button');
            dot.type = 'button';
            dot.className = 'es-dot' + (i === 0 ? ' is-active' : '');
            dot.setAttribute('aria-label', 'Go to testimonial ' + (i + 1));
            dot.addEventListener('click', function () { goTo(i); restart(); });
            dotsWrap.appendChild(dot);
            dots.push(dot);
        });

        function goTo(index) {
            current = (index + slides.length) % slides.length;
            slides.forEach(function (s, i) {
                s.classList.toggle('is-active', i === current);
                s.setAttribute('aria-hidden', i === current ? 'false' : 'true');
            });
            dots.forEach(function (d, i) { d.classList.toggle('is-active', i === current); });
        }

        function stop() { clearInterval(timer); timer = null; }
        function start() {
            stop();
            if (reduceMotion) return;
            timer = setInterval(function () { goTo(current + 1); }, 6000);
        }
        function restart() { start(); }

        prevBtn.addEventListener('click', function () { goTo(current - 1); restart(); });
        nextBtn.addEventListener('click', function () { goTo(current + 1); restart(); });

        slider.addEventListener('mouseenter', stop);
        slider.addEventListener('mouseleave', start);
        slider.addEventListener('focusin', stop);
        slider.addEventListener('focusout', start);

        // Mobile swipe
        var startX = 0, startY = 0;
        slider.addEventListener('touchstart', function (e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            stop();
        }, { passive: true });
        slider.addEventListener('touchend', function (e) {
            var dx = e.changedTouches[0].clientX - startX;
            var dy = e.changedTouches[0].clientY - startY;
            if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
                goTo(current + (dx < 0 ? 1 : -1));
            }
            start();
        }, { passive: true });

        // Tab hide ho to ruk jaye
        document.addEventListener('visibilitychange', function () {
            if (document.hidden) stop(); else start();
        });

        goTo(0);
        start();
    }

    // =============================================
    // FAQ: ek waqt mein ek hi khula rahe
    // =============================================
    var faq = document.getElementById('esFaq');
    if (faq) {
        var items = faq.querySelectorAll('details');
        items.forEach(function (item) {
            item.addEventListener('toggle', function () {
                if (!item.open) return;
                items.forEach(function (other) {
                    if (other !== item) other.open = false;
                });
            });
        });
    }
});