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

        // ===== CHATBOX TOGGLE =====
        const toggle = document.getElementById('chatToggle');
        const widget = document.getElementById('chatWidget');
        const close = document.getElementById('chatClose');

        if (toggle && widget) {
            toggle.addEventListener('click', function() {
                widget.classList.toggle('active');
                if (widget.classList.contains('active')) {
                    document.getElementById('chatInput').focus();
                }
            });
        }
        if (close && widget) {
            close.addEventListener('click', function() {
                widget.classList.remove('active');
            });
        }

        // ===== CHAT SEND =====
        const input = document.getElementById('chatInput');
        const sendBtn = document.getElementById('chatSend');
        const messages = document.getElementById('chatMessages');

        function sendMessage() {
            if (!input || !messages) return;
            const text = input.value.trim();
            if (!text) return;

            const userDiv = document.createElement('div');
            userDiv.className = 'chat-message user';
            userDiv.innerHTML = `
                <div class="chat-avatar user-avatar">👤</div>
                <div class="chat-bubble">${escapeHtml(text)}</div>
            `;
            messages.appendChild(userDiv);

            setTimeout(function() {
                const replies = [
                    'Thanks for your message! Our team will get back to you shortly.',
                    'Great question! Let me connect you with an expert.',
                    'We appreciate your interest! How can we assist you further?',
                    'That\'s a great point! Would you like to schedule a call?'
                ];
                const reply = replies[Math.floor(Math.random() * replies.length)];
                const botDiv = document.createElement('div');
                botDiv.className = 'chat-message bot';
                botDiv.innerHTML = `
                    <div class="chat-avatar">🤖</div>
                    <div class="chat-bubble">${reply}</div>
                `;
                messages.appendChild(botDiv);
                messages.scrollTop = messages.scrollHeight;
            }, 600);

            input.value = '';
            messages.scrollTop = messages.scrollHeight;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        if (sendBtn && input) {
            sendBtn.addEventListener('click', sendMessage);
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    sendMessage();
                }
            });
        }

        // ===== CLOSE CHAT ON ESC =====
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && widget && widget.classList.contains('active')) {
                widget.classList.remove('active');
            }
        });

    });
