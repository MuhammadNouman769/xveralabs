// FAQ Accordion
        document.querySelectorAll('.faq-question').forEach(question => {
            question.addEventListener('click', () => {
                const item = question.parentElement;
                const isActive = item.classList.contains('active');
                
                // Close all other items
                document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
                
                // Toggle current
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        });

        // Smooth Scroll for internal links (optional)
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });

        // Navbar scroll effect (optional)
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (window.scrollY > 50) {
                header.style.background = 'rgba(15, 23, 42, 0.95)';
                header.style.padding = '10px 0';
            } else {
                header.style.background = 'transparent';
                header.style.padding = '20px 0';
            }
        });
