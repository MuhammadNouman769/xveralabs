// Campus Ambassador Program — page interactions
(function () {
  'use strict';

  // Smooth scroll for in-page anchors
  document.querySelectorAll('a[href^="#cap-"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      var targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Fade-in on scroll for each section
  var sections = document.querySelectorAll('.page-about-campuses .cap-section');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    sections.forEach(function (section) {
      section.style.opacity = '0';
      section.style.transform = 'translateY(30px)';
      section.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
      observer.observe(section);
    });
  }

  // Animate stats counter in banner
  var stats = document.querySelectorAll('.page-about-campuses .cap-banner-stats strong');
  stats.forEach(function (el) {
    var text = el.textContent;
    // Only animate if it starts with a number
    var match = text.match(/^(\d+)/);
    if (!match) return;
    var target = parseInt(match[1], 10);
    var suffix = text.replace(/^(\d+)/, '');
    var current = 0;
    var step = Math.max(1, Math.ceil(target / 40));
    var timer = setInterval(function () {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = current + suffix;
    }, 30);
  });

  // FAQ: close other items when one opens (accordion behaviour)
  var faqItems = document.querySelectorAll('.page-about-campuses .cap-faq-item');
  faqItems.forEach(function (item) {
    item.addEventListener('toggle', function () {
      if (this.open) {
        faqItems.forEach(function (other) {
          if (other !== item) other.open = false;
        });
      }
    });
  });

  // Apply button placeholder handler
  document.querySelectorAll('.page-about-campuses .cap-btn-primary').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (this.getAttribute('href') === '#') {
        e.preventDefault();
        alert('Thank you for your interest! The application portal will open soon.');
      }
    });
  });

  console.log('🚀 Campus Ambassador Program page loaded — 8 sections ready.');
})();