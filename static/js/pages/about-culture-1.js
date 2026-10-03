function initCultureCarousels() {
    'use strict';

    var culturePage = document.querySelector('.mn-life-page');
    if (!culturePage) return;
    var base = culturePage.dataset.cultureImageBase || '';

    var cultureImages = [
        { src: base + 'qawali.png',  title: 'Qawali Night' },
        { src: base + 'jashan.png',  title: 'Jashn-e-Baharan' },
        { src: base + 'sportsday.png', title: 'Sports Day' },
        { src: base + 'revo.png',    title: 'Her Revolution' },
        { src: base + 'khel.png',    title: 'Khel ka Janoon' },
        { src: base + 'basanat.png', title: 'Basanat' }
    ];

    var dayImages = [
        { src: base + 'coffe.png',   title: 'Morning Coffee',   desc: 'Starting the day right' },
        { src: base + 'meeting.png', title: 'Stand-up Meeting', desc: 'Aligning with the team' },
        { src: base + 'pair.png',    title: 'Pair Programming', desc: 'Collaborative problem-solving' },
        { src: base + 'deep.png',    title: 'Deep Focus',       desc: 'Heads down, getting things done' },
        { src: base + 'dinner.png',  title: 'Team Dinner',      desc: 'Good food, great company' },
        { src: base + 'gyms.png',    title: 'Gym Session',      desc: 'Recharge and stay fit' },
        { src: base + 'office-space.png', title: 'Office Spaces', desc: 'Built for collaboration' },
        { src: base + 'relax.png',   title: 'Relax Area',       desc: 'Unwind and connect' }
    ];

    var cultureTrack = document.getElementById('cultureTrack');
    var dayTrack = document.getElementById('dayTrack');
    var culturePrev = document.getElementById('culturePrev');
    var cultureNext = document.getElementById('cultureNext');
    var dayPrev = document.getElementById('dayPrev');
    var dayNext = document.getElementById('dayNext');

    if (!cultureTrack || !dayTrack || !culturePrev || !cultureNext || !dayPrev || !dayNext) return;

    function escapeAttr(text) {
        return String(text).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
    }

    // Items do baar banate hain (asli + clone) taake loop beech mein na tootay.
    // Clone screen readers se chhupa diya hai.
    function renderCulture() {
        cultureTrack.innerHTML = cultureImages.concat(cultureImages).map(function (item, i) {
            var clone = i >= cultureImages.length;
            return '<div class="carousel-item"' + (clone ? ' aria-hidden="true"' : '') + '>' +
                '<img src="' + item.src + '" alt="' + (clone ? '' : escapeAttr(item.title)) + '" loading="lazy" draggable="false">' +
                '<div class="carousel-content"><h4>' + item.title + '</h4></div>' +
                '</div>';
        }).join('');
    }

    function renderDay() {
        dayTrack.innerHTML = dayImages.concat(dayImages).map(function (item, i) {
            var clone = i >= dayImages.length;
            return '<div class="day-item"' + (clone ? ' aria-hidden="true"' : '') + '>' +
                '<img src="' + item.src + '" alt="' + (clone ? '' : escapeAttr(item.title)) + '" loading="lazy" draggable="false">' +
                '<div class="day-caption"><h5>' + item.title + '</h5><p>' + item.desc + '</p></div>' +
                '</div>';
        }).join('');
    }

    renderCulture();
    renderDay();

    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function setupCarousel(track, prevButton, nextButton, intervalTime) {
        var wrapper = track.parentElement;
        var total = Math.floor(track.children.length / 2);
        var position = 0;
        var timer = null;

        function stepWidth() {
            var first = track.children[0];
            if (!first) return 0;
            var style = window.getComputedStyle(track);
            var gap = parseFloat(style.columnGap || style.gap) || 0;
            return first.offsetWidth + gap;
        }

        function apply(animate) {
            if (!animate) track.style.transition = 'none';
            track.style.transform = 'translateX(' + (-position * stepWidth()) + 'px)';
            if (!animate) {
                void track.offsetWidth;          // reflow
                track.style.transition = '';
            }
        }

        // Clone tak pohnch gaye to chupke se asli par wapas (jump nazar nahi aata)
        track.addEventListener('transitionend', function (e) {
            if (e.target !== track || e.propertyName !== 'transform') return;
            if (position >= total) {
                position = position - total;
                apply(false);
            }
        });

        function move(direction) {
            if (direction > 0) {
                if (position >= total) return;   // reset hone tak intezar
                position += 1;
                apply(true);
            } else {
                if (position <= 0) {
                    position = total;            // clones ke end par chupke se jao
                    apply(false);
                }
                requestAnimationFrame(function () {
                    position -= 1;
                    apply(true);
                });
            }
        }

        function stopAutoSlide() {
            clearInterval(timer);
            timer = null;
        }

        function startAutoSlide() {
            stopAutoSlide();
            if (reduceMotion) return;
            timer = setInterval(function () { move(1); }, intervalTime);
        }

        nextButton.addEventListener('click', function () { move(1); startAutoSlide(); });
        prevButton.addEventListener('click', function () { move(-1); startAutoSlide(); });

        // Hover / focus pe ruk jaye
        wrapper.addEventListener('mouseenter', stopAutoSlide);
        wrapper.addEventListener('mouseleave', startAutoSlide);
        wrapper.addEventListener('focusin', stopAutoSlide);
        wrapper.addEventListener('focusout', startAutoSlide);

        // Mobile swipe
        var startX = 0, startY = 0, swiping = false;
        wrapper.addEventListener('touchstart', function (e) {
            var t = e.touches[0];
            startX = t.clientX;
            startY = t.clientY;
            swiping = true;
            stopAutoSlide();
        }, { passive: true });
        wrapper.addEventListener('touchend', function (e) {
            if (swiping) {
                var t = e.changedTouches[0];
                var dx = t.clientX - startX;
                var dy = t.clientY - startY;
                if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
                    move(dx < 0 ? 1 : -1);
                }
            }
            swiping = false;
            startAutoSlide();
        }, { passive: true });

        // Tab hide ho to ruk jaye
        document.addEventListener('visibilitychange', function () {
            if (document.hidden) stopAutoSlide();
            else startAutoSlide();
        });

        // Resize / rotate pe item width dobara hisab karo
        var resizeTimer;
        window.addEventListener('resize', function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () { apply(false); }, 100);
        });

        // Images load hone ke baad bhi width theek rahe
        window.addEventListener('load', function () { apply(false); });

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