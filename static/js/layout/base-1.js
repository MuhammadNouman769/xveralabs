(function () {
    'use strict';

    // =============================================
    // PRELOADER (shown once per visit; later pages skip it)
    // =============================================
    (function initPreloader() {
        var pre = document.getElementById('btrx-preloader');
        if (!pre) return;
        var KEY = 'btrx_seen';
        function remove() { if (pre && pre.parentNode) pre.parentNode.removeChild(pre); }

        var seen = false;
        try { seen = sessionStorage.getItem(KEY) === '1'; } catch (e) { /* private mode */ }
        if (seen) { remove(); return; }

        var MIN_SHOW = 900, MAX_WAIT = 3500;
        var pct = document.getElementById('btrxPct');
        var fill = pre.querySelector('.btrx-pl__bar span');
        var start = Date.now();
        var shown = 0, target = 8, finished = false, raf = 0;

        function paint(v) {
            if (pct) pct.textContent = Math.round(v) + '%';
            if (fill) fill.style.transform = 'scaleX(' + (v / 100) + ')';
        }
        (function tick() {
            if (finished) return;
            target = Math.min(target + (target < 70 ? 1.1 : 0.2), 92);
            shown += (target - shown) * 0.1;
            paint(shown);
            raf = requestAnimationFrame(tick);
        })();

        function finish() {
            if (finished) return;
            setTimeout(function () {
                finished = true;
                cancelAnimationFrame(raf);
                paint(100);
                try { sessionStorage.setItem(KEY, '1'); } catch (e) { /* ignore */ }
                setTimeout(function () {
                    pre.classList.add('btrx-hide');
                    setTimeout(remove, 800);
                }, 260);
            }, Math.max(0, MIN_SHOW - (Date.now() - start)));
        }
        if (document.readyState === 'complete') finish(); else window.addEventListener('load', finish);
        setTimeout(finish, MAX_WAIT);
    })();

    // =============================================
    // CHAT SIDEBAR (posts to the contact_us backend)
    // =============================================
    var widget = document.querySelector('.btrx-chat-widget');
    var toggle = document.getElementById('btrxChatToggle');
    var box = document.getElementById('btrxChatBox');
    var backdrop = document.getElementById('btrxChatBackdrop');
    var closeBtn = document.getElementById('btrxChatClose');
    var form = document.getElementById('btrxChatForm');
    if (!widget || !toggle || !box || !form) return;

    var body = document.getElementById('btrxChatBody');
    var steps = [].slice.call(form.querySelectorAll('.btrx-step'));
    var stepper = [].slice.call(document.querySelectorAll('#btrxStepper li'));
    var stepperEl = document.getElementById('btrxStepper');
    var backBtn = document.getElementById('btrxBack');
    var nextBtn = document.getElementById('btrxNext');
    var sendBtn = document.getElementById('btrxSend');
    var formErr = document.getElementById('btrxFormErr');
    var nav = document.querySelector('#btrxFoot .btrx-nav');
    var done = document.getElementById('btrxDone');
    var doneClose = document.getElementById('btrxDoneClose');
    var refEl = document.getElementById('btrxRef');
    var current = 1, lastFocus = null;

    // budget steps come from the backend (json_script in base.html)
    var BUDGETS = [];
    try { BUDGETS = JSON.parse(document.getElementById('cf-budget-steps').textContent); } catch (e) { /* ignore */ }

    // ---------- open / close ----------
    function isOpen() { return box.classList.contains('active'); }

    function resetUI() {
        form.hidden = false; done.hidden = true; stepperEl.hidden = false; nav.hidden = false;
        showStep(1);
    }

    function openChat() {
        if (isOpen()) return;
        lastFocus = document.activeElement;
        if (!done.hidden) resetUI();
        document.getElementById('cf-page').value = location.href;
        box.classList.add('active');
        backdrop.classList.add('active');
        toggle.classList.add('active');
        box.setAttribute('aria-hidden', 'false');
        toggle.setAttribute('aria-expanded', 'true');
        document.documentElement.classList.add('btrx-lock');
        restoreDraft();
        setTimeout(function () {
            var first = form.querySelector('.btrx-step.is-active input, .btrx-step.is-active select, .btrx-step.is-active textarea');
            if (first) first.focus({ preventScroll: true });
        }, 350);
    }

    function closeChat() {
        if (!isOpen()) return;
        box.classList.remove('active');
        backdrop.classList.remove('active');
        toggle.classList.remove('active');
        box.setAttribute('aria-hidden', 'true');
        toggle.setAttribute('aria-expanded', 'false');
        document.documentElement.classList.remove('btrx-lock');
        if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }

    toggle.addEventListener('click', function (e) { e.preventDefault(); isOpen() ? closeChat() : openChat(); });
    if (closeBtn) closeBtn.addEventListener('click', closeChat);
    if (backdrop) backdrop.addEventListener('click', closeChat);
    if (doneClose) doneClose.addEventListener('click', closeChat);

    // any element with data-open-chat opens the sidebar; also window.btrxChat.open()
    document.addEventListener('click', function (e) {
        var t = e.target.closest ? e.target.closest('[data-open-chat]') : null;
        if (t) { e.preventDefault(); openChat(); }
    });
    window.btrxChat = { open: openChat, close: closeChat };

    document.addEventListener('keydown', function (e) {
        if (!isOpen()) return;
        if (e.key === 'Escape') { closeChat(); return; }
        if (e.key === 'Tab') {   // keep focus inside the drawer
            var f = [].slice.call(box.querySelectorAll('a[href], button:not([disabled]):not([hidden]), input:not([type=hidden]):not([tabindex="-1"]):not([disabled]), select, textarea'))
                .filter(function (el) { return el.offsetParent !== null; });
            if (!f.length) return;
            var first = f[0], last = f[f.length - 1];
            if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
            else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
        }
    });

    // ---------- steps ----------
    function showStep(n) {
        current = n;
        steps.forEach(function (s) {
            var on = Number(s.getAttribute('data-step')) === n;
            s.hidden = !on;
            s.classList.toggle('is-active', on);
        });
        stepper.forEach(function (li) {
            var s = Number(li.getAttribute('data-s'));
            li.classList.toggle('is-active', s === n);
            li.classList.toggle('is-done', s < n);
        });
        stepperEl.style.setProperty('--prog', String((n - 1) / (steps.length - 1)));
        backBtn.hidden = n === 1;
        nextBtn.hidden = n === steps.length;
        sendBtn.hidden = n !== steps.length;
        formErr.hidden = true;
        body.scrollTop = 0;
    }

    // ---------- validation (the server checks everything again) ----------
    var RULES = {
        full_name: function (v) { return v.trim().length >= 2 ? '' : 'Please enter your name.'; },
        email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) ? '' : 'Enter a valid email address.'; },
        phone: function (v) { return /^\d{6,15}$/.test(v.replace(/[\s\-()]/g, '')) ? '' : 'Enter a valid phone number.'; },
        company: function (v) { return v.trim() ? '' : 'Please enter your company name.'; },
        company_url: function (v) { return !v.trim() || /^(https?:\/\/)?[^\s.]+\.[^\s]{2,}$/i.test(v.trim()) ? '' : 'Enter a valid website address.'; },
        region: function (v) { return v ? '' : 'Please choose your region.'; },
        topic: function (v) { return v ? '' : 'Please choose a topic.'; },
        details: function (v) { return v.trim().length >= 10 ? '' : 'Please add a few details (at least 10 characters).'; }
    };
    var STEP_FIELDS = { 1: ['full_name', 'email', 'phone', 'company', 'company_url', 'region'], 2: ['topic', 'services'], 3: ['details', 'consent'] };

    function holderOf(name) {
        if (name === 'services') return document.getElementById('cf-services');
        var el = form.elements[name];
        return el ? el.closest('.btrx-f') : null;
    }

    function showMsg(holder, message) {
        var p = holder.nextElementSibling && holder.nextElementSibling.classList.contains('btrx-err') ? holder.nextElementSibling : null;
        if (!message) { if (p) p.remove(); return; }
        if (!p) {
            p = document.createElement('p');
            p.className = 'btrx-err';
            p.setAttribute('role', 'alert');
            holder.parentNode.insertBefore(p, holder.nextSibling);
        }
        p.textContent = message;
    }

    function setError(name, message) {
        if (name === 'country_code') name = 'phone';
        var h = holderOf(name);
        if (!h) return;
        h.classList.toggle('is-invalid', !!message);
        showMsg(h, message);
    }

    function checkField(name) {
        var msg = '';
        if (name === 'services') msg = form.querySelector('input[name="services"]:checked') ? '' : 'Choose at least one service.';
        else if (name === 'consent') msg = form.elements.consent.checked ? '' : 'Please confirm to continue.';
        else msg = RULES[name](form.elements[name].value || '');
        setError(name, msg);
        return !msg;
    }

    function validateStep(n) {
        var ok = true, firstBad = null;
        STEP_FIELDS[n].forEach(function (name) {
            if (!checkField(name)) { ok = false; if (!firstBad) firstBad = name; }
        });
        if (!ok) {
            var el = firstBad === 'services' ? form.querySelector('input[name="services"]') : form.elements[firstBad];
            if (el && el.focus) el.focus();
        }
        return ok;
    }

    form.addEventListener('input', function (e) {
        var n = e.target.name, h = n && holderOf(n);
        if (RULES[n] && h && h.classList.contains('is-invalid')) checkField(n);
        saveDraft();
    });
    form.addEventListener('change', function (e) {
        var n = e.target.name;
        if (n === 'services' && document.getElementById('cf-services').classList.contains('is-invalid')) checkField('services');
        if (n === 'consent' && holderOf('consent').classList.contains('is-invalid')) checkField('consent');
        if (RULES[n] && (n === 'region' || n === 'topic')) checkField(n);
    });

    nextBtn.addEventListener('click', function () { if (validateStep(current)) showStep(current + 1); });
    backBtn.addEventListener('click', function () { if (current > 1) showStep(current - 1); });
    form.addEventListener('keydown', function (e) {   // Enter goes forward instead of submitting early
        if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA' && current < steps.length) { e.preventDefault(); nextBtn.click(); }
    });

    // ---------- budget slider (optional) ----------
    var slider = document.getElementById('cf-budget');
    var out = document.getElementById('cf-budget-out');
    var val = document.getElementById('cf-budget-val');
    var skip = document.getElementById('cf-budget-skip');
    slider.max = String(Math.max(BUDGETS.length - 1, 0));

    function budgetPicked() {
        var b = BUDGETS[Number(slider.value)];
        if (!b) return;
        val.value = b[0];
        out.textContent = b[1];
    }
    slider.addEventListener('input', function () { skip.checked = false; budgetPicked(); });
    skip.addEventListener('change', function () {
        slider.disabled = skip.checked;
        if (skip.checked) { val.value = 'not-sure'; out.textContent = 'Not sure yet'; }
        else { val.value = ''; out.textContent = 'Slide to choose'; }
    });

    // ---------- details counter ----------
    var details = document.getElementById('cf-details');
    var counter = document.getElementById('cf-count');
    function updateCount() { counter.textContent = details.value.length + ' / ' + (details.getAttribute('maxlength') || 2000); }
    details.addEventListener('input', updateCount);

    // ---------- keep a draft for this browser session (no budget, no consent) ----------
    var DRAFT_KEY = 'btrx_chat_draft';
    var DRAFT_FIELDS = ['full_name', 'email', 'phone', 'company', 'company_url', 'region', 'topic', 'details'];
    function saveDraft() {
        try {
            var d = {};
            DRAFT_FIELDS.forEach(function (n) { d[n] = form.elements[n].value; });
            sessionStorage.setItem(DRAFT_KEY, JSON.stringify(d));
        } catch (e) { /* ignore */ }
    }
    function restoreDraft() {
        try {
            var d = JSON.parse(sessionStorage.getItem(DRAFT_KEY) || 'null');
            if (!d) return;
            DRAFT_FIELDS.forEach(function (n) { if (d[n] && !form.elements[n].value) form.elements[n].value = d[n]; });
            updateCount();
        } catch (e) { /* ignore */ }
    }

    // ---------- submit ----------
    function csrfToken() {
        var f = form.querySelector('input[name="csrfmiddlewaretoken"]');
        if (f) return f.value;
        var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
        return m ? decodeURIComponent(m[1]) : '';
    }
    function showFormError(text) { formErr.textContent = text; formErr.hidden = false; }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        for (var n = 1; n <= steps.length; n++) {
            if (!validateStep(n)) { if (current !== n) { showStep(n); validateStep(n); } return; }
        }
        var endpoint = form.getAttribute('data-endpoint');
        if (!endpoint) { showFormError('Sending is not available right now. Please use WhatsApp or call us.'); return; }

        sendBtn.disabled = true;
        var label = sendBtn.innerHTML;
        sendBtn.textContent = 'Sending...';
        formErr.hidden = true;

        fetch(endpoint, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken() },
            credentials: 'same-origin'
        }).then(function (res) {
            return res.json().catch(function () { return {}; }).then(function (data) { return { data: data }; });
        }).then(function (r) {
            var d = r.data || {};
            if (d.ok) {
                try { sessionStorage.removeItem(DRAFT_KEY); } catch (err) { /* ignore */ }
                form.reset();
                updateCount();
                slider.disabled = false; val.value = ''; out.textContent = 'Slide to choose';
                refEl.textContent = d.ref || '-';
                form.hidden = true; nav.hidden = true; stepperEl.hidden = true; done.hidden = false;
                return;
            }
            if (d.errors) {   // show server messages and jump to the first step that has one
                var firstStep = 4;
                Object.keys(d.errors).forEach(function (name) {
                    var key = name === 'country_code' ? 'phone' : name;
                    setError(key, d.errors[name]);
                    for (var s = 1; s <= 3; s++) if (STEP_FIELDS[s].indexOf(key) !== -1) firstStep = Math.min(firstStep, s);
                });
                if (firstStep <= 3) showStep(firstStep);
            }
            showFormError(d.error || 'We could not send your message. Please check the form and try again.');
        }).catch(function () {
            showFormError('Network problem. Please try again, or message us on WhatsApp.');
        }).then(function () {
            sendBtn.disabled = false;
            sendBtn.innerHTML = label;
        });
    });

    showStep(1);
    updateCount();
})();