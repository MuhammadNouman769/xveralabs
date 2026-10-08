/* =============================================
   XVERA LABS – EMPLOYEE BENEFITS
   Minimal JS: smooth reveal on scroll + hover polish
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {
  // ---- 1. Smooth reveal animation for benefit sections ----
  const benefitSections = document.querySelectorAll('.xb-benefits');

  const revealOnScroll = function () {
    const windowHeight = window.innerHeight;
    const revealPoint = 100;

    benefitSections.forEach(section => {
      const sectionTop = section.getBoundingClientRect().top;
      if (sectionTop < windowHeight - revealPoint) {
        section.style.opacity = '1';
        section.style.transform = 'translateY(0)';
      }
    });
  };

  // Set initial state
  benefitSections.forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(40px)';
    section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
  });

  // Trigger on load & scroll
  window.addEventListener('load', revealOnScroll);
  window.addEventListener('scroll', revealOnScroll);
  // Also call immediately in case sections are already in view
  setTimeout(revealOnScroll, 100);

  // ---- 2. Subtle parallax on hero background (optional) ----
  const hero = document.querySelector('.xb-hero');
  if (hero) {
    window.addEventListener('scroll', function () {
      const scrolled = window.pageYOffset;
      // Only apply on wider screens where background-attachment is fixed-ish
      if (window.innerWidth > 820) {
        hero.style.backgroundPositionY = (scrolled * 0.15) + 'px';
      }
    });
  }

  // ---- 3. Hover tilt on benefit images (very light) ----
  const images = document.querySelectorAll('.xb-benefits-image');
  images.forEach(img => {
    img.addEventListener('mouseenter', function () {
      this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
    });
  });

  // ---- 4. CTA button click (demo) ----
  const ctaBtn = document.querySelector('.xb-cta-btn');
  if (ctaBtn) {
    ctaBtn.addEventListener('click', function (e) {
      e.preventDefault();
      // You can replace with a real redirect or modal
      alert('Thanks for your interest! Our careers page will open soon.');
    });
  }
});