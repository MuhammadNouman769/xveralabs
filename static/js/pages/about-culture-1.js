function initCultureCarousels() {

    const culturePage = document.querySelector('.mn-life-page');
    if (!culturePage) return;
    const cultureImageBase = culturePage.dataset.cultureImageBase;

    const cultureImages = [
        {
            src: `${cultureImageBase}qawali.png`,
            title: "Qawali Night"
        },
        {
            src: `${cultureImageBase}jashan.png`,
            title: "Jashn-e-Baharan"
        },
        {
            src: `${cultureImageBase}sportsday.png`,
            title: "Sports Day"
        },
        {
            src: `${cultureImageBase}revo.png`,
            title: "Her Revolution"
        },
        {
            src: `${cultureImageBase}khel.png`,
            title: "Khel ka Janoon"
        },
        {
            src: `${cultureImageBase}basanat.png`,
            title: "Basanat"
        }
    ];

    const dayImages = [
        {
            src: `${cultureImageBase}coffe.png`,
            title: "Morning Coffee",
            desc: "Starting the day right"
        },
        {
            src: `${cultureImageBase}meeting.png`,
            title: "Stand-up Meeting",
            desc: "Aligning with the team"
        },
        {
            src: `${cultureImageBase}pair.png`,
            title: "Pair Programming",
            desc: "Collaborative problem-solving"
        },
        {
            src: `${cultureImageBase}deep.png`,
            title: "Deep Focus",
            desc: "Heads down, getting things done"
        },
        {
            src: `${cultureImageBase}dinner.png`,
            title: "Team Dinner",
            desc: "Good food, great company"
        },
        {
            src: `${cultureImageBase}gyms.png`,
            title: "Gym Session",
            desc: "Recharge and stay fit"
        },
        {
            src: `${cultureImageBase}office-space.png`,
            title: "Office Spaces",
            desc: "Built for collaboration"
        },
        {
            src: `${cultureImageBase}relax.png`,
            title: "Relax Area",
            desc: "Unwind and connect"
        }
    ];

    const cultureTrack = document.getElementById("cultureTrack");
    const dayTrack = document.getElementById("dayTrack");
    const culturePrev = document.getElementById("culturePrev");
    const cultureNext = document.getElementById("cultureNext");
    const dayPrev = document.getElementById("dayPrev");
    const dayNext = document.getElementById("dayNext");

    if (!cultureTrack || !dayTrack || !culturePrev || !cultureNext || !dayPrev || !dayNext) return;

    function createCultureItems() {
        const items = [...cultureImages, ...cultureImages];

        cultureTrack.innerHTML = items.map(function (item) {
            return `
                <div class="carousel-item">
                    <img src="${item.src}" alt="${item.title}" loading="lazy">
                    <div class="carousel-content">
                        <h4>${item.title}</h4>
                    </div>
                </div>
            `;
        }).join("");
    }

    function createDayItems() {
        const items = [...dayImages, ...dayImages];

        dayTrack.innerHTML = items.map(function (item) {
            return `
                <div class="day-item">
                    <img src="${item.src}" alt="${item.title}" loading="lazy">
                    <div class="day-caption">
                        <h5>${item.title}</h5>
                        <p>${item.desc}</p>
                    </div>
                </div>
            `;
        }).join("");
    }

    createCultureItems();
    createDayItems();

    function getItemWidth(track) {
        const firstItem = track.children[0];

        if (!firstItem) {
            return 0;
        }

        const style = window.getComputedStyle(track);
        const gap = parseFloat(style.columnGap || style.gap) || 0;

        return firstItem.offsetWidth + gap;
    }

    function setupCarousel(track, prevButton, nextButton, intervalTime) {
        let position = 0;
        let timer = null;

        function move(direction) {
            const originalCount = Math.floor(track.children.length / 2);

            position += direction;

            if (position >= originalCount) {
                position = 0;
            }

            if (position < 0) {
                position = originalCount - 1;
            }

            const itemWidth = getItemWidth(track);

            track.style.transform =
                `translateX(-${position * itemWidth}px)`;
        }

        function startAutoSlide() {
            clearInterval(timer);

            timer = setInterval(function () {
                move(1);
            }, intervalTime);
        }

        function stopAutoSlide() {
            clearInterval(timer);
        }

        nextButton.addEventListener("click", function () {
            move(1);
            startAutoSlide();
        });

        prevButton.addEventListener("click", function () {
            move(-1);
            startAutoSlide();
        });

        const wrapper = track.parentElement;

        wrapper.addEventListener("mouseenter", stopAutoSlide);
        wrapper.addEventListener("mouseleave", startAutoSlide);

        window.addEventListener("resize", function () {
            const itemWidth = getItemWidth(track);

            track.style.transform =
                `translateX(-${position * itemWidth}px)`;
        });

        startAutoSlide();
    }

    setupCarousel(cultureTrack, culturePrev, cultureNext, 3000);
    setupCarousel(dayTrack, dayPrev, dayNext, 3000);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCultureCarousels, { once: true });
} else {
    initCultureCarousels();
}
