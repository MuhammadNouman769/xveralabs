// ===== Showcase Filter =====
    document.addEventListener("DOMContentLoaded", function() {
        const buttons = document.querySelectorAll(".btr-filter-btn");
        const cards = document.querySelectorAll(".btr-showcase-card");

        buttons.forEach(button => {
            button.addEventListener("click", function() {
                buttons.forEach(btn => btn.classList.remove("active"));
                this.classList.add("active");

                const filter = this.getAttribute("data-filter");

                cards.forEach(card => {
                    if (filter === "all") {
                        card.classList.remove("btr-showcase-hidden");
                    } else {
                        if (card.dataset.category === filter) {
                            card.classList.remove("btr-showcase-hidden");
                        } else {
                            card.classList.add("btr-showcase-hidden");
                        }
                    }
                });
            });
        });
    });

    // ===== Counter Animation =====
    document.addEventListener("DOMContentLoaded", function() {
        const counters = document.querySelectorAll(".btr-counter-number");

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.dataset.count);
                    const duration = 2000;
                    const startTime = performance.now();

                    function updateCounter(currentTime) {
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const eased = 1 - Math.pow(1 - progress, 3);
                        const current = Math.floor(eased * target);

                        entry.target.textContent = current;

                        if (progress < 1) {
                            requestAnimationFrame(updateCounter);
                        } else {
                            entry.target.textContent = target;
                        }
                    }
                    requestAnimationFrame(updateCounter);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    });

    // ===== Tech Cards Interaction =====
    document.addEventListener("DOMContentLoaded", function() {
        const cards = document.querySelectorAll(".btr-tech-card");
        const buttons = document.querySelectorAll(".btr-tech-detail-btn");

        buttons.forEach(function(button) {
            button.addEventListener("click", function(event) {
                event.preventDefault();
                event.stopPropagation();
                const card = button.closest(".btr-tech-card");
                const isActive = card.classList.contains("is-active");

                cards.forEach(function(item) {
                    item.classList.remove("is-active");
                    const itemButton = item.querySelector(".btr-tech-detail-btn");
                    if (itemButton) {
                        itemButton.setAttribute("aria-expanded", "false");
                    }
                });

                if (!isActive) {
                    card.classList.add("is-active");
                    button.setAttribute("aria-expanded", "true");
                }
            });
        });

        cards.forEach(function(card) {
            card.addEventListener("click", function(event) {
                if (event.target.closest(".btr-tech-detail-btn")) {
                    return;
                }
                if (window.matchMedia("(hover: none)").matches) {
                    const isActive = card.classList.contains("is-active");
                    cards.forEach(function(item) {
                        item.classList.remove("is-active");
                        const button = item.querySelector(".btr-tech-detail-btn");
                        if (button) {
                            button.setAttribute("aria-expanded", "false");
                        }
                    });
                    if (!isActive) {
                        card.classList.add("is-active");
                        const button = card.querySelector(".btr-tech-detail-btn");
                        if (button) {
                            button.setAttribute("aria-expanded", "true");
                        }
                    }
                }
            });
        });

        document.addEventListener("click", function(event) {
            if (!event.target.closest(".btr-tech-card")) {
                cards.forEach(function(card) {
                    card.classList.remove("is-active");
                    const button = card.querySelector(".btr-tech-detail-btn");
                    if (button) {
                        button.setAttribute("aria-expanded", "false");
                    }
                });
            }
        });
    });

    // ===== Client Logos: Pause/Resume on Click =====
    document.querySelectorAll('.btrx-scroll-track').forEach((track, index) => {
        track.addEventListener('click', function(e) {
            if (e.target.closest('.btrx-client-item')) return;
            const container = this.querySelector('.btrx-scroll-container');
            if (container) {
                const isPaused = container.style.animationPlayState === 'paused';
                container.style.animationPlayState = isPaused ? 'running' : 'paused';
            }
        });
    });
