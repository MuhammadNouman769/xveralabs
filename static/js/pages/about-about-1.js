// =====================================================================
// ABOUT PAGE
//   PART 1 (new): reveal on scroll, hero marquee, ecosystem tabs
//   PART 2: team slider (UNCHANGED from your original file)
// =====================================================================

/* ---------- PART 1: new design ---------- */
(function () {
    "use strict";

    var root = document.querySelector(".ab");
    if (!root) return;

    // reveal on scroll
    var items = Array.prototype.slice.call(root.querySelectorAll(".ab-reveal"));
    if (items.length && "IntersectionObserver" in window) {
        root.classList.add("ab-js");
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-in");
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });
        items.forEach(function (el) { io.observe(el); });
    }

    // hero marquee: duplicate the words so the -50% loop is seamless
    var track = document.getElementById("abMarquee");
    if (track && !track.dataset.cloned) {
        var originals = Array.prototype.slice.call(track.children);
        // repeat until one half is wider than the screen
        var need = Math.max(2, Math.ceil((window.innerWidth * 1.2) / Math.max(track.scrollWidth, 1)));
        for (var n = 1; n < need; n++) originals.forEach(function (el) { track.appendChild(el.cloneNode(true)); });
        var half = Array.prototype.slice.call(track.children);
        half.forEach(function (el) { track.appendChild(el.cloneNode(true)); });
        track.dataset.cloned = "true";
    }

    // ecosystem tabs (click + arrow keys)
    var tabs = Array.prototype.slice.call(document.querySelectorAll("#abEco [role='tab']"));
    if (tabs.length) {
        var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });

        function select(index, focus) {
            tabs.forEach(function (tab, i) {
                var on = i === index;
                tab.classList.toggle("is-active", on);
                tab.setAttribute("aria-selected", on ? "true" : "false");
                tab.tabIndex = on ? 0 : -1;
                if (panels[i]) {
                    panels[i].hidden = !on;
                    panels[i].classList.toggle("is-active", on);
                }
            });
            if (focus) tabs[index].focus();
        }

        tabs.forEach(function (tab, i) {
            tab.addEventListener("click", function () { select(i, false); });
            tab.addEventListener("keydown", function (e) {
                var next = null;
                if (e.key === "ArrowDown" || e.key === "ArrowRight") next = (i + 1) % tabs.length;
                if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = (i - 1 + tabs.length) % tabs.length;
                if (e.key === "Home") next = 0;
                if (e.key === "End") next = tabs.length - 1;
                if (next !== null) { e.preventDefault(); select(next, true); }
            });
        });
    }
})();

/* ---------- PART 2: TEAM SLIDER (unchanged) ---------- */
document.addEventListener("DOMContentLoaded", function () {

    var slider   = document.getElementById("btrlxSlider");
    var leftBtn  = document.getElementById("leftBtn");
    var rightBtn = document.getElementById("rightBtn");
    if (!slider || !leftBtn || !rightBtn) return;

    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // scroll by exactly one card (works on every screen size)
    function step() {
        var card = slider.querySelector(".btrlx-card");
        return card ? card.getBoundingClientRect().width : 340;
    }

    function updateButtons() {
        var max = slider.scrollWidth - slider.clientWidth - 2;
        leftBtn.disabled  = slider.scrollLeft <= 2;
        rightBtn.disabled = slider.scrollLeft >= max;
    }

    function scrollSlider(dir) {
        slider.scrollBy({ left: dir * step(), behavior: reduceMotion ? "auto" : "smooth" });
    }

    rightBtn.addEventListener("click", function () { scrollSlider(1); });
    leftBtn.addEventListener("click",  function () { scrollSlider(-1); });

    var ticking = false;
    slider.addEventListener("scroll", function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () { updateButtons(); ticking = false; });
    }, { passive: true });

    window.addEventListener("resize", updateButtons);
    updateButtons();
});