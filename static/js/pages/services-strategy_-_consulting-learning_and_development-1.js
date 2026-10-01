document.addEventListener('DOMContentLoaded', function() {

    // ===== CONSULTATION FORM =====
    const form = document.getElementById('consultationForm');
    if (form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('✅ Consultation request submitted! We\'ll contact you within 24 hours.');
        form.reset();
      });
    }

    // ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });

  });
