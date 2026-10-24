// ===== Cloud & DevOps: filter =====
document.addEventListener("DOMContentLoaded", function () {
    var root = document.querySelector(".btrsc");
    if (!root) return;

    var buttons = Array.prototype.slice.call(root.querySelectorAll(".btrsc__filter"));
    var cards = Array.prototype.slice.call(root.querySelectorAll(".btrsc__card"));

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            buttons.forEach(function (b) {
                b.classList.remove("is-active");
                b.setAttribute("aria-pressed", "false");
            });
            button.classList.add("is-active");
            button.setAttribute("aria-pressed", "true");

            var filter = button.getAttribute("data-filter");

            cards.forEach(function (card) {
                var show = filter === "all" || card.getAttribute("data-category") === filter;
                card.classList.toggle("is-hidden", !show);
                if (show) {
                    // restart the fade-in animation
                    card.classList.remove("is-entering");
                    void card.offsetWidth;
                    card.classList.add("is-entering");
                }
            });
        });
    });
});

// ===== Counter Animation =====
document.addEventListener("DOMContentLoaded", function () {
    const counters = document.querySelectorAll(".btr-counter-number");

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.dataset.count, 10);
                const duration = 2000;
                const startTime = performance.now();

                function updateCounter(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    el.textContent = Math.floor(eased * target);

                    if (progress < 1) {
                        requestAnimationFrame(updateCounter);
                    } else {
                        el.textContent = target;
                    }
                }
                requestAnimationFrame(updateCounter);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(function (counter) { observer.observe(counter); });
});

// ===== Who We Are: staggered cards reveal on scroll =====
document.addEventListener("DOMContentLoaded", function () {
    const section = document.querySelector(".btrwho-section");
    if (!section) return;

    const cards = Array.from(section.querySelectorAll(".btrwho-card"));
    if (!cards.length) return;

    // IntersectionObserver na ho to cards waise hi dikhte rahenge
    if (!("IntersectionObserver" in window)) return;

    section.classList.add("btrwho-js");

    function reveal(card) {
        // column ke hisaab se halka sa delay (1st col -> 2nd col -> 3rd col)
        const col = card.closest(".btrwho-column");
        const colIndex = col ? Array.from(col.parentElement.children).indexOf(col) : 0;
        const rowIndex = col ? Array.from(col.children).indexOf(card) : 0;
        card.style.transitionDelay = (colIndex * 120 + rowIndex * 90) + "ms";
        card.classList.add("is-visible");

        // delay hover animation ko slow na kare, isliye reveal ke baad hata do
        setTimeout(function () { card.style.transitionDelay = ""; }, 1200);
    }

    const io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                reveal(entry.target);
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    cards.forEach(function (card) { io.observe(card); });
});

// ===== Tech Cards Interaction (desktop accordion) =====
document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".btr-tech-card");
    const buttons = document.querySelectorAll(".btr-tech-detail-btn");

    function resetAll() {
        cards.forEach(function (item) {
            item.classList.remove("is-active");
            const b = item.querySelector(".btr-tech-detail-btn");
            if (b) b.setAttribute("aria-expanded", "false");
        });
    }

    buttons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();
            const card = button.closest(".btr-tech-card");
            const isActive = card.classList.contains("is-active");
            resetAll();
            if (!isActive) {
                card.classList.add("is-active");
                button.setAttribute("aria-expanded", "true");
            }
        });
    });

    cards.forEach(function (card) {
        card.addEventListener("click", function (event) {
            if (event.target.closest(".btr-tech-detail-btn")) return;
            // slider mode (≤1000px) mein accordion ki zaroorat nahi
            if (window.matchMedia("(max-width: 1000px)").matches) return;
            if (window.matchMedia("(hover: none)").matches) {
                const isActive = card.classList.contains("is-active");
                resetAll();
                if (!isActive) {
                    card.classList.add("is-active");
                    const b = card.querySelector(".btr-tech-detail-btn");
                    if (b) b.setAttribute("aria-expanded", "true");
                }
            }
        });
    });

    document.addEventListener("click", function (event) {
        if (!event.target.closest(".btr-tech-card")) resetAll();
    });
});

// ===== Tech Cards: one-by-one slider (≤1000px) =====
document.addEventListener("DOMContentLoaded", function () {
    const wrap = document.getElementById("btrTechCards");
    const dotsBox = document.getElementById("btrTechDots");
    if (!wrap || !dotsBox) return;

    const slides = Array.from(wrap.querySelectorAll(".btr-tech-card"));
    if (!slides.length) return;

    const mq = window.matchMedia("(max-width: 1000px)");
    const DELAY = 3500;
    let index = 0;
    let timer = null;
    let scrollTimer = null;

    // dots banao
    slides.forEach(function (_, i) {
        const d = document.createElement("button");
        d.type = "button";
        d.className = "btr-tech-dot";
        d.setAttribute("aria-label", "Go to slide " + (i + 1));
        d.addEventListener("click", function () {
            goTo(i);
            start();
        });
        dotsBox.appendChild(d);
    });
    const dots = Array.from(dotsBox.querySelectorAll(".btr-tech-dot"));

    function setDot(i) {
        dots.forEach(function (d, n) { d.classList.toggle("active", n === i); });
    }

    function goTo(i) {
        index = (i + slides.length) % slides.length;
        wrap.scrollTo({ left: slides[index].offsetLeft, behavior: "smooth" });
        setDot(index);
    }

    function stop() {
        if (timer) { clearInterval(timer); timer = null; }
    }

    function start() {
        stop();
        if (!mq.matches) return;
        timer = setInterval(function () { goTo(index + 1); }, DELAY);
    }

    // swipe / manual scroll ke baad current index detect karo
    wrap.addEventListener("scroll", function () {
        if (!mq.matches) return;
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(function () {
            let nearest = 0;
            let min = Infinity;
            slides.forEach(function (s, n) {
                const diff = Math.abs(s.offsetLeft - wrap.scrollLeft);
                if (diff < min) { min = diff; nearest = n; }
            });
            index = nearest;
            setDot(index);
        }, 80);
    }, { passive: true });

    // user touch kare to pause, chhodne par dobara start
    wrap.addEventListener("touchstart", stop, { passive: true });
    wrap.addEventListener("touchend", start, { passive: true });
    wrap.addEventListener("mouseenter", stop);
    wrap.addEventListener("mouseleave", start);

    // screen size badle (desktop <-> tablet/mobile)
    function onModeChange() {
        wrap.scrollLeft = 0;
        index = 0;
        setDot(0);
        start();
    }
    if (mq.addEventListener) {
        mq.addEventListener("change", onModeChange);
    } else if (mq.addListener) {
        mq.addListener(onModeChange);
    }

    setDot(0);
    start();
});

// ===== Client Voices: featured testimonial carousel =====
document.addEventListener("DOMContentLoaded", function () {
    var root = document.querySelector(".btrtm");
    if (!root) return;

    var slides = Array.prototype.slice.call(root.querySelectorAll(".btrtm__slide"));
    var prev = document.getElementById("btrtmPrev");
    var next = document.getElementById("btrtmNext");
    var count = document.getElementById("btrtmCount");
    var bar = document.getElementById("btrtmBar");
    if (slides.length < 2) return;

    var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var index = 0;

    function pad(n) { return n < 10 ? "0" + n : String(n); }

    function restartBar() {
        if (!bar) return;
        bar.classList.remove("is-running");
        void bar.offsetWidth;
        if (!reduceMotion) bar.classList.add("is-running");
    }

    function show(i) {
        index = (i + slides.length) % slides.length;
        slides.forEach(function (slide, n) {
            var active = n === index;
            slide.classList.toggle("is-active", active);
            slide.setAttribute("aria-hidden", active ? "false" : "true");
        });
        if (count) count.textContent = pad(index + 1) + " / " + pad(slides.length);
        restartBar();
    }

    // the progress bar finishing = time for the next slide (pausing the bar pauses autoplay)
    if (bar) {
        bar.addEventListener("animationend", function () { show(index + 1); });
    }

    if (prev) prev.addEventListener("click", function () { show(index - 1); });
    if (next) next.addEventListener("click", function () { show(index + 1); });

    function pause() { root.classList.add("is-paused"); }
    function resume() { root.classList.remove("is-paused"); }

    root.addEventListener("mouseenter", pause);
    root.addEventListener("mouseleave", resume);
    root.addEventListener("focusin", pause);
    root.addEventListener("focusout", resume);
    root.addEventListener("touchstart", pause, { passive: true });
    root.addEventListener("touchend", resume, { passive: true });

    root.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { show(index - 1); }
        if (e.key === "ArrowRight") { show(index + 1); }
    });

    // do not rotate while the tab is hidden
    document.addEventListener("visibilitychange", function () {
        if (document.hidden) { pause(); } else { resume(); }
    });

    show(0);
});

// ===== Contact form: validation (no fake success, the server handles the submit) =====
document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("btrctForm");
    if (!form) return;

    var services = form.querySelector(".btrct__services");
    var boxes = Array.prototype.slice.call(form.querySelectorAll('input[name="services"]'));
    if (!services || !boxes.length) return;

    var error = document.createElement("p");
    error.className = "btrct__services-error";
    error.setAttribute("role", "alert");
    error.hidden = true;
    error.textContent = "Please choose at least one service.";
    services.appendChild(error);

    function servicesOk() {
        return boxes.some(function (b) { return b.checked; });
    }
    function showServices() {
        var ok = servicesOk();
        services.classList.toggle("is-invalid", !ok);
        error.hidden = ok;
    }

    boxes.forEach(function (b) {
        b.addEventListener("change", function () {
            if (form.classList.contains("was-validated")) showServices();
        });
    });

    form.addEventListener("submit", function (e) {
        form.classList.add("was-validated");
        var fieldsOk = form.checkValidity();
        var svcOk = servicesOk();
        showServices();
        if (!fieldsOk || !svcOk) {
            e.preventDefault();
            var firstBad = form.querySelector(":invalid");
            if (firstBad) { firstBad.focus(); } else { boxes[0].focus(); }
        }
    });
});

// ===== Client Logos: Pause/Resume on Click =====
document.querySelectorAll(".btrx-scroll-track").forEach(function (track) {
    track.addEventListener("click", function (e) {
        if (e.target.closest(".btrx-client-item")) return;
        const container = this.querySelector(".btrx-scroll-container");
        if (container) {
            const isPaused = container.style.animationPlayState === "paused";
            container.style.animationPlayState = isPaused ? "running" : "paused";
        }
    });
});