// ===== Showcase Filter =====
document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".btr-filter-btn");
    const cards = document.querySelectorAll(".btr-showcase-card");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            buttons.forEach(function (btn) { btn.classList.remove("active"); });
            this.classList.add("active");

            const filter = this.getAttribute("data-filter");

            cards.forEach(function (card) {
                if (filter === "all" || card.dataset.category === filter) {
                    card.classList.remove("btr-showcase-hidden");
                } else {
                    card.classList.add("btr-showcase-hidden");
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

// ===== Testimonials: card-by-card, right → left =====
document.addEventListener("DOMContentLoaded", function () {
    const track = document.querySelector(".btr-testimonials-track");
    if (!track) return;

    const originals = Array.from(track.children);
    const total = originals.length;
    if (total < 2) return;

    // seamless loop ke liye clones (screen par jitne cards dikhte hain unse zyada hone chahiye)
    originals.forEach(function (card) {
        const clone = card.cloneNode(true);
        clone.setAttribute("aria-hidden", "true");
        track.appendChild(clone);
    });

    const cards = track.children;
    const DELAY = 3000;
    const SPEED = 800;
    let index = 0;
    let timer = null;
    let jumpTimer = null;

    function stepSize() {
        return cards[1].offsetLeft - cards[0].offsetLeft;
    }

    function move(animate) {
        track.style.transition = animate
            ? "transform " + SPEED + "ms cubic-bezier(.22,.61,.36,1)"
            : "none";
        track.style.transform = "translateX(" + (-index * stepSize()) + "px)";
    }

    function next() {
        index++;
        move(true);
        if (index >= total) {
            // clone par pohanch gaye -> animation ke baad chupke se asli pehle card par jump
            clearTimeout(jumpTimer);
            jumpTimer = setTimeout(function () {
                index = 0;
                move(false);
            }, SPEED + 50);
        }
    }

    function stop() {
        if (timer) { clearInterval(timer); timer = null; }
    }

    function start() {
        stop();
        timer = setInterval(next, DELAY);
    }

    track.addEventListener("mouseenter", stop);
    track.addEventListener("mouseleave", start);
    track.addEventListener("touchstart", stop, { passive: true });
    track.addEventListener("touchend", start, { passive: true });

    window.addEventListener("resize", function () { move(false); });

    start();
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