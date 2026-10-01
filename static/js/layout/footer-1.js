(function() {
        'use strict';

        // === BACK TO TOP ===
        const backBtn = document.getElementById('btrBackTop');
        let isVisible = false;

        function toggleBackTop() {
            const scrollY = window.pageYOffset || document.documentElement.scrollTop;
            if (scrollY > 300 && !isVisible) {
                backBtn.classList.add('visible');
                isVisible = true;
            } else if (scrollY <= 300 && isVisible) {
                backBtn.classList.remove('visible');
                isVisible = false;
            }
        }

        if (backBtn) {
            window.addEventListener('scroll', toggleBackTop, { passive: true });
            window.addEventListener('load', toggleBackTop, { passive: true });
            backBtn.addEventListener('click', function(e) {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }

        // === NEWSLETTER FORM ===
        const newsletterForm = document.querySelector('.btr-ft-form');
        if (newsletterForm) {
            newsletterForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const input = this.querySelector('input[type="email"]');
                if (input && input.value.trim()) {
                    // Show success message
                    const btn = this.querySelector('button');
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '✓';
                    btn.style.background = '#22c55e';
                    
                    setTimeout(() => {
                        btn.innerHTML = originalText;
                        btn.style.background = '';
                    }, 2000);
                    
                    input.value = '';
                } else {
                    input.style.borderColor = '#ef4444';
                    setTimeout(() => {
                        input.style.borderColor = '';
                    }, 2000);
                }
            });
        }

        // === SOCIAL ICON INTERACTION ===
        document.querySelectorAll('.btr-ft-social a').forEach(function(link) {
            link.addEventListener('mouseenter', function() {
                // subtle ripple effect via JS
            });
        });

    })();
