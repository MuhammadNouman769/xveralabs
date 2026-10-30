// =====================================================================
// PEOPLE PAGE: line progress fills as you scroll, stops light up,
// line selector follows the section you are reading
// =====================================================================
(function () {
    "use strict";

    var root = document.querySelector(".pm");
    if (!root) return;

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var stops = Array.prototype.slice.call(root.querySelectorAll(".pm-stop"));
    var tracks = Array.prototype.slice.call(root.querySelectorAll(".pm-track"));

    if (reduce || !("IntersectionObserver" in window)) return; // page is fully visible without JS

    root.classList.add("pm-js");
    tracks.forEach(function (t) { t.style.setProperty("--p", "0"); });

    // 1) the coloured line grows as the reader moves down the track
    var ticking = false;
    function update() {
        var mid = window.innerHeight * 0.55;
        tracks.forEach(function (track) {
            var r = track.getBoundingClientRect();
            var p = Math.min(1, Math.max(0, (mid - r.top) / r.height));
            track.style.setProperty("--p", p.toFixed(4));
        });
        ticking = false;
    }
    function onScroll() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(update);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();

    // 2) a stop lights up when the line reaches it
    var stopIO = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visited");
                stopIO.unobserve(entry.target);
            }
        });
    }, { rootMargin: "0px 0px -35% 0px", threshold: 0.15 });
    stops.forEach(function (s) { stopIO.observe(s); });

    // 3) the sticky line selector follows the section on screen
    var pills = Array.prototype.slice.call(document.querySelectorAll(".pm-bar a[data-spy]"));
    var sections = pills.map(function (a) { return document.getElementById(a.getAttribute("data-spy")); }).filter(Boolean);
    var visible = {};
    var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
        var current = null;
        sections.forEach(function (s) { if (visible[s.id]) current = s.id; });
        pills.forEach(function (a) {
            var on = a.getAttribute("data-spy") === current;
            a.classList.toggle("is-active", on);
            if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
        });
    }, { rootMargin: "-35% 0px -55% 0px", threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
})();