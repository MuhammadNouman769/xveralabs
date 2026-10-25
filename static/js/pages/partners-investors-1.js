// =====================================================================
// Investor page: reveal on scroll, profit-share illustrator, FAQ single-open
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

    // ---------- profit-share illustrator (simple arithmetic, illustration only) ----------
    var profitInput = document.getElementById("calcProfit");
    var range = document.getElementById("calcRange");
    var rateInput = document.getElementById("calcRate");
    var result = document.getElementById("calcResult");

    if (profitInput && range && rateInput && result) {
        var MAX_PROFIT = 1000000000000;
        var fmt = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });

        function readProfit() {
            var digits = profitInput.value.replace(/[^\d]/g, "");
            var n = digits ? parseInt(digits, 10) : 0;
            return Math.min(n, MAX_PROFIT);
        }

        function readRate() {
            var r = parseFloat(rateInput.value);
            if (isNaN(r) || r < 0) r = 0;
            if (r > 100) r = 100;
            return r;
        }

        function render() {
            var share = readProfit() * (readRate() / 100);
            result.textContent = "PKR " + fmt.format(Math.round(share));
        }

        profitInput.addEventListener("input", function () {
            var n = readProfit();
            // keep the caret at the end while adding thousands separators
            profitInput.value = n ? fmt.format(n) : "";
            render();
        });

        range.addEventListener("input", function () {
            rateInput.value = range.value;
            render();
        });

        rateInput.addEventListener("input", function () {
            var r = readRate();
            range.value = Math.min(r, parseFloat(range.max));
            render();
        });

        render();
    }

    // ---------- FAQ: one open at a time ----------
    var faq = document.getElementById("btrpiFaq");
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
