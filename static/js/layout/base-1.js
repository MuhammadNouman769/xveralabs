(function() {
            'use strict';

            // =============================================
            // PRELOADER - FIXED: Properly hides and shows content
            // =============================================
            function hidePreloader() {
                const preloader = document.getElementById('btrx-preloader');
                if (preloader) {
                    preloader.classList.add('btrx-hide');
                    console.log('✅ Preloader hidden — homepage revealed.');
                }
            }

            // Wait for everything (images, fonts, etc.) then hide preloader
            window.addEventListener('load', function() {
                // Slight delay to let the progress animation finish gracefully
                setTimeout(hidePreloader, 2000);
            });

            // Fallback: if load event already fired, hide after a short delay
            if (document.readyState === 'complete') {
                setTimeout(hidePreloader, 500);
            }

            // Emergency fallback: force hide after 4 seconds (just in case)
            setTimeout(function() {
                const preloader = document.getElementById('btrx-preloader');
                if (preloader && !preloader.classList.contains('btrx-hide')) {
                    preloader.classList.add('btrx-hide');
                    console.warn('⚠️ Preloader force-hidden after 4s fallback.');
                }
            }, 4000);

            // =============================================
            // CHAT WIDGET - VERTICAL BUTTON
            // =============================================
            const chatToggle = document.getElementById('btrxChatToggle');
            const chatBox = document.getElementById('btrxChatBox');
            const chatBody = document.getElementById('btrxChatBody');
            const chatClose = document.getElementById('btrxChatClose');
            const chatForm = document.getElementById('btrxChatForm');

            // Toggle chat
            if (chatToggle && chatBox) {
                chatToggle.addEventListener('click', function(e) {
                    e.stopPropagation();
                    e.preventDefault();

                    chatBox.classList.toggle('active');
                    this.classList.toggle('active');

                    if (chatBox.classList.contains('active')) {
                        if (chatBody) {
                            chatBody.scrollTop = 0;
                        }
                    }
                });
            }

            // Close chat
            if (chatClose && chatBox) {
                chatClose.addEventListener('click', function(e) {
                    e.stopPropagation();
                    chatBox.classList.remove('active');
                    if (chatToggle) chatToggle.classList.remove('active');
                });
            }

            // Close on outside click
            document.addEventListener('click', function(e) {
                const widget = document.querySelector('.btrx-chat-widget');
                if (widget && !widget.contains(e.target)) {
                    if (chatBox) chatBox.classList.remove('active');
                    if (chatToggle) chatToggle.classList.remove('active');
                }
            });

            // Close on Escape
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && chatBox && chatBox.classList.contains('active')) {
                    chatBox.classList.remove('active');
                    if (chatToggle) chatToggle.classList.remove('active');
                }
            });

            // =============================================
            // FORM SUBMISSION
            // =============================================
            if (chatForm) {
                chatForm.addEventListener('submit', function(e) {
                    e.preventDefault();

                    const name = this.querySelector('input[type="text"]');
                    const email = this.querySelector('input[type="email"]');
                    const phone = this.querySelector('input[type="tel"]');
                    const company = this.querySelectorAll('input[type="text"]')[1];
                    const region = this.querySelectorAll('select')[0];
                    const budget = this.querySelectorAll('select')[1];
                    const message = this.querySelector('textarea');

                    let isValid = true;

                    if (!name.value.trim()) {
                        name.style.borderColor = '#ef4444';
                        isValid = false;
                    } else {
                        name.style.borderColor = '#e2e8f0';
                    }

                    if (!email.value.trim() || !isValidEmail(email.value)) {
                        email.style.borderColor = '#ef4444';
                        isValid = false;
                    } else {
                        email.style.borderColor = '#e2e8f0';
                    }

                    if (!phone.value.trim()) {
                        phone.style.borderColor = '#ef4444';
                        isValid = false;
                    } else {
                        phone.style.borderColor = '#e2e8f0';
                    }

                    if (!company.value.trim()) {
                        company.style.borderColor = '#ef4444';
                        isValid = false;
                    } else {
                        company.style.borderColor = '#e2e8f0';
                    }

                    if (!region.value) {
                        region.style.borderColor = '#ef4444';
                        isValid = false;
                    } else {
                        region.style.borderColor = '#e2e8f0';
                    }

                    if (!budget.value) {
                        budget.style.borderColor = '#ef4444';
                        isValid = false;
                    } else {
                        budget.style.borderColor = '#e2e8f0';
                    }

                    if (!message.value.trim()) {
                        message.style.borderColor = '#ef4444';
                        isValid = false;
                    } else {
                        message.style.borderColor = '#e2e8f0';
                    }

                    if (!isValid) return;

                    const btn = this.querySelector('.btrx-chat-send');
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '<i class="fas fa-check"></i> Sent!';
                    btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
                    btn.disabled = true;

                    setTimeout(function() {
                        btn.innerHTML = originalText;
                        btn.style.background = '';
                        btn.disabled = false;
                        chatForm.reset();
                        if (chatBox) chatBox.classList.remove('active');
                        if (chatToggle) chatToggle.classList.remove('active');
                        alert('✅ Message sent successfully! We\'ll get back to you within 24 hours.');
                    }, 2000);
                });
            }

            // =============================================
            // HELPER FUNCTIONS
            // =============================================
            function isValidEmail(email) {
                return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
            }

            // Input focus effects
            document.querySelectorAll('.btrx-chat-input, .btrx-chat-textarea, .btrx-chat-select').forEach(function(input) {
                input.addEventListener('focus', function() {
                    const label = this.parentElement.querySelector('label');
                    if (label) label.style.color = '#0ebab1';
                });
                input.addEventListener('blur', function() {
                    const label = this.parentElement.querySelector('label');
                    if (label) label.style.color = '';
                });
            });

            // Ctrl+Enter to send
            if (chatForm) {
                const textarea = chatForm.querySelector('textarea');
                if (textarea) {
                    textarea.addEventListener('keydown', function(e) {
                        if (e.ctrlKey && e.key === 'Enter') {
                            e.preventDefault();
                            chatForm.dispatchEvent(new Event('submit'));
                        }
                    });
                }
            }

            console.log('✅ BTR Preloader & Chat Widget initialized successfully!');

        })();
