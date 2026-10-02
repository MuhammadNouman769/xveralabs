(function () {
    'use strict';

    // =============================================
    // PRELOADER
    // =============================================
    (function initPreloader() {
        var preloader = document.getElementById('btrx-preloader');
        if (!preloader) return;

        var MIN_SHOW = 800;    // kam az kam itni der dikhao (ms)
        var MAX_WAIT = 3000;   // is ke baad zabardasti hata do
        var startedAt = Date.now();
        var done = false;

        function hide() {
            if (done) return;
            done = true;
            preloader.classList.add('btrx-hide');
            setTimeout(function () {
                if (preloader.parentNode) preloader.parentNode.removeChild(preloader);
            }, 900);
        }

        function onReady() {
            var wait = Math.max(0, MIN_SHOW - (Date.now() - startedAt));
            setTimeout(hide, wait);
        }

        if (document.readyState === 'complete') {
            onReady();
        } else {
            window.addEventListener('load', onReady);
        }

        setTimeout(hide, MAX_WAIT); // safety net
    })();

    // =============================================
    // CHAT WIDGET
    // =============================================
    var widget = document.querySelector('.btrx-chat-widget');
    var chatToggle = document.getElementById('btrxChatToggle');
    var chatBox = document.getElementById('btrxChatBox');
    var chatBody = document.getElementById('btrxChatBody');
    var chatClose = document.getElementById('btrxChatClose');
    var chatForm = document.getElementById('btrxChatForm');

    if (!widget || !chatToggle || !chatBox) return; // is page pe widget nahi hai

    function openChat() {
        chatBox.classList.add('active');
        chatToggle.classList.add('active');
        chatToggle.setAttribute('aria-expanded', 'true');
        if (chatBody) chatBody.scrollTop = 0;
    }

    function closeChat() {
        chatBox.classList.remove('active');
        chatToggle.classList.remove('active');
        chatToggle.setAttribute('aria-expanded', 'false');
    }

    chatToggle.addEventListener('click', function (e) {
        e.stopPropagation();
        e.preventDefault();
        if (chatBox.classList.contains('active')) closeChat();
        else openChat();
    });

    if (chatClose) {
        chatClose.addEventListener('click', function (e) {
            e.stopPropagation();
            closeChat();
        });
    }

    // Bahar click pe band
    document.addEventListener('click', function (e) {
        if (!widget.contains(e.target)) closeChat();
    });

    // Escape pe band
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && chatBox.classList.contains('active')) closeChat();
    });

    // =============================================
    // FORM VALIDATION + SUBMIT
    // =============================================
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function setInvalid(el, invalid) {
        if (el) el.classList.toggle('is-invalid', invalid);
    }

    if (chatForm) {
        var f = chatForm.elements;
        var requiredFields = [f['full_name'], f['phone'], f['company'], f['region'], f['budget'], f['details']];

        // Type karte hi error hata do
        chatForm.addEventListener('input', function (e) {
            if (e.target.classList) e.target.classList.remove('is-invalid');
            if (e.target.name === 'services') {
                var group = document.getElementById('cf-services');
                if (group) group.classList.remove('is-invalid');
            }
        });
        chatForm.addEventListener('change', function (e) {
            if (e.target.classList) e.target.classList.remove('is-invalid');
        });

        chatForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var isValid = true;

            requiredFields.forEach(function (field) {
                var bad = !field || !field.value.trim();
                setInvalid(field, bad);
                if (bad) isValid = false;
            });

            var emailBad = !f['email'].value.trim() || !isValidEmail(f['email'].value.trim());
            setInvalid(f['email'], emailBad);
            if (emailBad) isValid = false;

            var servicesGroup = document.getElementById('cf-services');
            var anyService = chatForm.querySelector('input[name="services"]:checked');
            if (servicesGroup) servicesGroup.classList.toggle('is-invalid', !anyService);
            if (!anyService) isValid = false;

            if (!isValid) {
                var firstBad = chatForm.querySelector('.is-invalid');
                if (firstBad && firstBad.scrollIntoView) {
                    firstBad.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }

            // TODO: yahan Django view / API pe fetch() se data bhejein
            // var data = new FormData(chatForm);

            var btn = chatForm.querySelector('.btrx-chat-send');
            var originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> Sent!';
            btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
            btn.disabled = true;

            setTimeout(function () {
                btn.innerHTML = originalHTML;
                btn.style.background = '';
                btn.disabled = false;
                chatForm.reset();
                closeChat();
                alert("Message sent successfully! We'll get back to you within 24 hours.");
            }, 1500);
        });

        // Ctrl+Enter se submit
        var textarea = chatForm.querySelector('textarea');
        if (textarea) {
            textarea.addEventListener('keydown', function (e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    if (chatForm.requestSubmit) chatForm.requestSubmit();
                    else chatForm.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            });
        }
    }

    // Focus pe label ka rang
    document.querySelectorAll('.btrx-chat-input, .btrx-chat-textarea, .btrx-chat-select').forEach(function (input) {
        input.addEventListener('focus', function () {
            var label = this.parentElement.querySelector('label');
            if (label) label.style.color = '#0ebab1';
        });
        input.addEventListener('blur', function () {
            var label = this.parentElement.querySelector('label');
            if (label) label.style.color = '';
        });
    });

})();