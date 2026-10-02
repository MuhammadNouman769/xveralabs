document.addEventListener("DOMContentLoaded", function () {

    /* ---------- 1. Logo columns: duplicate cards so the -50% loop is seamless ---------- */
    document.querySelectorAll(".btrx-column").forEach(function (col) {
        if (col.dataset.cloned) return;
        Array.from(col.children).forEach(function (card) {
            var clone = card.cloneNode(true);
            clone.setAttribute("aria-hidden", "true");
            var img = clone.querySelector("img");
            if (img) img.alt = "";
            col.appendChild(clone);
        });
        col.dataset.cloned = "true";
    });

    /* ---------- 2. Team slider ---------- */
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