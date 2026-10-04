document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    var root = document.querySelector('.dei');
    if (!root) return;

    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var hasIO = 'IntersectionObserver' in window;

    // =============================================
    // SMOOTH SCROLL (header ke neeche rukne ke liye CSS mein scroll-margin-top hai)
    // =============================================
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var href = this.getAttribute('href');
            if (!href || href === '#') return;

            var target = null;
            try { target = document.querySelector(href); } catch (err) { return; }
            if (!target) return;

            e.preventDefault();
            target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        });
    });

    // =============================================
    // REVEAL ON SCROLL
    // =============================================
    if (hasIO && !reduceMotion) {
        root.classList.add('js');

        var revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-in');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        root.querySelectorAll('.dei-reveal').forEach(function (el, i) {
            // Ek row ke cards thora thora delay se aayen
            el.style.transitionDelay = ((i % 3) * 90) + 'ms';
            revealObserver.observe(el);
        });
    }

    // =============================================
    // HERO STATS COUNT-UP
    // =============================================
    function runCount(el) {
        var target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var duration = 1500;
        var start = null;

        function step(ts) {
            if (start === null) start = ts;
            var progress = Math.min((ts - start) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(target * eased) + suffix;
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
});