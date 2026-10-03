document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // ===== CONSULTATION FORM =====
    var form = document.getElementById('consultationForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            // TODO: yahan Django view / API pe fetch() se data bhejein
            alert("Consultation request submitted! We'll contact you within 24 hours.");
            form.reset();
        });
    }

    // ===== PAGE CHATBOX =====
    var toggle = document.getElementById('chatToggle');
    var widget = document.getElementById('chatWidget');   // pehle 'ch atWidget' typo tha, is liye chat khulta hi nahi tha
    var closeBtn = document.getElementById('chatClose');
    var input = document.getElementById('chatInput');
    var sendBtn = document.getElementById('chatSend');
    var messages = document.getElementById('chatMessages');

    function openChat() {
        if (!widget) return;
        widget.classList.add('active');
        if (toggle) toggle.setAttribute('aria-expanded', 'true');
        if (input) input.focus();
    }

    function closeChat() {
        if (!widget) return;
        widget.classList.remove('active');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
    }

    if (toggle && widget) {
        toggle.addEventListener('click', function () {
            if (widget.classList.contains('active')) closeChat();
            else openChat();
        });
    }

    if (closeBtn) closeBtn.addEventListener('click', closeChat);

    // Escape pe band
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && widget && widget.classList.contains('active')) closeChat();
    });

    // ===== CHAT SEND =====
    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function addMessage(type, html) {
        var div = document.createElement('div');
        div.className = 'chat-message ' + type;
        div.innerHTML =
            '<div class="chat-avatar' + (type === 'user' ? ' user-avatar' : '') + '">' +
            (type === 'user' ? '👤' : '🤖') + '</div>' +
            '<div class="chat-bubble">' + html + '</div>';
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    var replies = [
        'Thanks for your message! Our team will get back to you shortly.',
        'Great question! Let me connect you with an expert.',
        'We appreciate your interest! How can we assist you further?',
        "That's a great point! Would you like to schedule a call?"
    ];

    function sendMessage() {
        if (!input || !messages) return;
        var text = input.value.trim();
        if (!text) return;

        addMessage('user', escapeHtml(text));
        input.value = '';

        setTimeout(function () {
            addMessage('bot', replies[Math.floor(Math.random() * replies.length)]);
        }, 600);
    }

    if (sendBtn && input) {
        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keydown', function (e) {   // keypress deprecated hai
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});