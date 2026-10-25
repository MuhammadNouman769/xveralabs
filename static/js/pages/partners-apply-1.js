// =====================================================================
// Partner application: prefill from the link, investor fields, validation
// The server handles the real submit (no fake success message here).
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
        }, { threshold: 0.08 });
        items.forEach(function (el) { io.observe(el); });
    }

    var form = document.getElementById("btrpaForm");
    if (!form) return;

    var radios = Array.prototype.slice.call(form.querySelectorAll('input[name="partner_type"]'));
    var typeBox = form.querySelector(".btrpa-types");
    var typeError = document.getElementById("paTypeError");
    var investor = document.getElementById("paInvestor");
    var moduleSel = document.getElementById("paModule");
    var rangeSel = document.getElementById("paRange");
    var message = document.getElementById("paMessage");
    var counter = document.getElementById("paCount");

    // ---------- investor-only fields ----------
    function syncInvestor() {
        var isInvestor = radios.some(function (r) { return r.checked && r.value === "investor"; });
        if (investor) investor.hidden = !isInvestor;
        // disabled fields are not sent, so non-investors never submit empty investor data
        if (moduleSel) moduleSel.disabled = !isInvestor;
        if (rangeSel) rangeSel.disabled = !isInvestor;
    }

    function typeChosen() {
        return radios.some(function (r) { return r.checked; });
    }

    function showTypeError() {
        var ok = typeChosen();
        if (typeBox) typeBox.classList.toggle("is-invalid", !ok);
        if (typeError) typeError.hidden = ok;
    }

    radios.forEach(function (r) {
        r.addEventListener("change", function () {
            syncInvestor();
            if (form.classList.contains("was-validated")) showTypeError();
        });
    });

    // ---------- prefill from ?type=...&module=... ----------
    try {
        var params = new URLSearchParams(window.location.search);
        var wantedType = params.get("type");
        var wantedModule = params.get("module");

        if (wantedType) {
            radios.forEach(function (r) { if (r.value === wantedType) r.checked = true; });
        }
        if (wantedModule && moduleSel) {
            Array.prototype.slice.call(moduleSel.options).forEach(function (o) {
                if (o.value === wantedModule) moduleSel.value = wantedModule;
            });
        }
    } catch (e) { /* old browser: the form still works */ }

    syncInvestor();

    // ---------- character counter ----------
    function updateCount() {
        if (!message || !counter) return;
        var max = parseInt(message.getAttribute("maxlength"), 10) || 1500;
        counter.textContent = message.value.length + " / " + max;
    }
    if (message) {
        message.addEventListener("input", updateCount);
        updateCount();
    }

    // ---------- validation ----------
    form.addEventListener("submit", function (e) {
        form.classList.add("was-validated");
        var fieldsOk = form.checkValidity();
        var typeOk = typeChosen();
        showTypeError();

        if (!fieldsOk || !typeOk) {
            e.preventDefault();
            if (!typeOk && radios.length) {
                radios[0].focus();
                if (typeBox) typeBox.scrollIntoView({ behavior: "smooth", block: "center" });
                return;
            }
            var firstBad = form.querySelector(":invalid");
            if (firstBad) firstBad.focus();
            return;
        }

        // stop double submits
        var btn = form.querySelector(".btrpa-submit");
        if (btn) {
            btn.disabled = true;
            btn.textContent = "Sending...";
        }
    });
})();
