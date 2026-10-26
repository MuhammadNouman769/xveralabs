// =====================================================================
// Why Choose Us: reveal on scroll, side-rail scroll-spy, project stage tabs
// =====================================================================
(function () {
    "use strict";

    var root = document.getElementById("btrwRoot");
    if (!root) return;

    // ---------- reveal on scroll ----------
    var items = Array.prototype.slice.call(root.querySelectorAll(".btrw-reveal"));
    if (items.length && "IntersectionObserver" in window) {
        root.classList.add("btrw-js");
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

    // ---------- side rail scroll-spy ----------
    var links = Array.prototype.slice.call(document.querySelectorAll("#btrwRail a[data-spy]"));
    var sections = links
        .map(function (a) { return document.getElementById(a.getAttribute("data-spy")); })
        .filter(Boolean);

    if (links.length && sections.length && "IntersectionObserver" in window) {
        var visible = {};
        var spy = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
            var current = null;
            sections.forEach(function (s) { if (visible[s.id]) current = s.id; });
            links.forEach(function (a) {
                var on = a.getAttribute("data-spy") === current;
                a.classList.toggle("is-active", on);
                if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
            });
        }, { rootMargin: "-30% 0px -55% 0px", threshold: 0 });
        sections.forEach(function (s) { spy.observe(s); });
    }

    // ---------- project stage tabs (with arrow-key support) ----------
    var wrap = document.getElementById("btrwStages");
    if (!wrap) return;

    var tabs = Array.prototype.slice.call(wrap.querySelectorAll('[role="tab"]'));
    var panels = Array.prototype.slice.call(wrap.querySelectorAll('[role="tabpanel"]'));
    var bar = document.getElementById("btrwStageBar");

    function select(i, focus) {
        tabs.forEach(function (tab, n) {
            var on = n === i;
            tab.classList.toggle("is-active", on);
            tab.setAttribute("aria-selected", on ? "true" : "false");
            tab.tabIndex = on ? 0 : -1;
            if (on && focus) tab.focus();
        });
        panels.forEach(function (panel, n) {
            var on = n === i;
            panel.hidden = !on;
            panel.classList.toggle("is-active", on);
        });
        if (bar) bar.style.width = ((i + 1) / tabs.length * 100) + "%";
    }

    tabs.forEach(function (tab, i) {
        tab.addEventListener("click", function () { select(i, false); });
        tab.addEventListener("keydown", function (e) {
            var n = tabs.length;
            if (e.key === "ArrowRight") { e.preventDefault(); select((i + 1) % n, true); }
            if (e.key === "ArrowLeft") { e.preventDefault(); select((i - 1 + n) % n, true); }
            if (e.key === "Home") { e.preventDefault(); select(0, true); }
            if (e.key === "End") { e.preventDefault(); select(n - 1, true); }
        });
    });

    select(0, false);
})();