// =====================================================================
// Partners overview: reveal on scroll, sub-nav scroll-spy, FAQ single-open
// =====================================================================
(function () {
    "use strict";

    var root = document.querySelector(".btrp");
    if (!root) return;

    // ---------- reveal on scroll ----------
    var items = Array.prototype.slice.call(root.querySelectorAll(".btrp-reveal"));
    if (items.length && "IntersectionObserver" in window) {
        root.classList.add("btrp-js");
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-in");
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
        items.forEach(function (el) { io.observe(el); });
    }

    // ---------- sub-nav scroll-spy ----------
    var links = Array.prototype.slice.call(document.querySelectorAll("#btrpoSub a[data-spy]"));
    var sections = links
        .map(function (a) { return document.getElementById(a.getAttribute("data-spy")); })
        .filter(Boolean);

    if (links.length && sections.length && "IntersectionObserver" in window) {
        var visible = {};

        function setActive() {
            var current = null;
            sections.forEach(function (s) { if (visible[s.id]) current = s.id; });
            links.forEach(function (a) {
                a.classList.toggle("is-active", a.getAttribute("data-spy") === current);
            });
            // keep the active chip in view on small screens
            var active = document.querySelector("#btrpoSub a.is-active");
            var bar = document.querySelector(".btrpo-sub__in");
            if (active && bar && bar.scrollWidth > bar.clientWidth) {
                bar.scrollTo({ left: active.offsetLeft - 24, behavior: "smooth" });
            }
        }

        var spy = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) { visible[entry.target.id] = entry.isIntersecting; });
            setActive();
        }, { rootMargin: "-35% 0px -55% 0px", threshold: 0 });

        sections.forEach(function (s) { spy.observe(s); });
    }

    // ---------- FAQ: one open at a time ----------
    var faq = document.getElementById("btrpoFaq");
    if (faq) {
        var details = Array.prototype.slice.call(faq.querySelectorAll("details"));
        details.forEach(function (d) {
            d.addEventListener("toggle", function () {
                if (!d.open) return;
                details.forEach(function (other) { if (other !== d) other.open = false; });
            });
        });
    }
})();
