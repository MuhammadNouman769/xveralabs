/* Cookie consent. Stores the choice in a first-party cookie for 180 days.
   Other scripts can read it with window.xveraConsent or listen for the "xvera:consent" event. */
(function () {
  'use strict';

  var COOKIE = 'xv_cookie_consent';
  var VERSION = 1;          // raise this number to ask everyone again after a policy change
  var DAYS = 180;

  var banner = document.getElementById('xckBanner');
  if (!banner) return;

  var main = document.getElementById('xckMain');
  var prefs = document.getElementById('xckPrefs');
  var cbAnalytics = document.getElementById('xckAnalytics');
  var cbMarketing = document.getElementById('xckMarketing');

  /* ---------- storage ---------- */
  function read() {
    try {
      var m = document.cookie.match(new RegExp('(?:^|;\\s*)' + COOKIE + '=([^;]*)'));
      if (!m) return null;
      var d = JSON.parse(decodeURIComponent(m[1]));
      if (!d || d.v !== VERSION) return null;
      return { necessary: true, analytics: !!d.a, marketing: !!d.m, time: d.t || 0 };
    } catch (e) { return null; }
  }

  function write(analytics, marketing) {
    var value = { v: VERSION, a: analytics ? 1 : 0, m: marketing ? 1 : 0, t: Date.now() };
    var expires = new Date(Date.now() + DAYS * 864e5).toUTCString();
    var secure = location.protocol === 'https:' ? '; Secure' : '';
    try {
      document.cookie = COOKIE + '=' + encodeURIComponent(JSON.stringify(value)) +
        '; expires=' + expires + '; path=/; SameSite=Lax' + secure;
    } catch (e) { /* cookies blocked: the banner will simply show again next visit */ }
    var consent = { necessary: true, analytics: !!analytics, marketing: !!marketing };
    try { document.dispatchEvent(new CustomEvent('xvera:consent', { detail: consent })); } catch (e) {}
    return consent;
  }

  /* ---------- views ---------- */
  function showView(which) {
    var isPrefs = which === 'prefs';
    main.hidden = isPrefs;
    prefs.hidden = !isPrefs;
    var title = document.getElementById(isPrefs ? 'xckPrefsTitle' : 'xckTitle');
    if (title) title.focus({ preventScroll: true });
  }

  function open(view, moveFocus) {
    var saved = read();
    cbAnalytics.checked = saved ? saved.analytics : false;
    cbMarketing.checked = saved ? saved.marketing : false;
    banner.hidden = false;
    main.hidden = view === 'prefs';
    prefs.hidden = view !== 'prefs';
    if (moveFocus) {
      var title = document.getElementById(view === 'prefs' ? 'xckPrefsTitle' : 'xckTitle');
      if (title) title.focus({ preventScroll: true });
    }
  }

  function close() { banner.hidden = true; }

  /* ---------- actions ---------- */
  function onAction(name) {
    if (name === 'accept') { write(true, true); close(); }
    else if (name === 'reject') { write(false, false); close(); }
    else if (name === 'customize') { showView('prefs'); }
    else if (name === 'save') { write(cbAnalytics.checked, cbMarketing.checked); close(); }
    else if (name === 'back') { read() ? close() : showView('main'); }
  }

  banner.addEventListener('click', function (e) {
    var btn = e.target.closest ? e.target.closest('[data-xck]') : null;
    if (btn) onAction(btn.getAttribute('data-xck'));
  });

  banner.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !prefs.hidden) onAction('back');
  });

  /* Footer link: <button type="button" data-xck-open>Cookie Settings</button> */
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-xck-open]') : null;
    if (!t) return;
    e.preventDefault();
    open('prefs', true);
  });

  /* ---------- public helper for other scripts ---------- */
  window.xveraConsent = {
    get: function () { return read(); },
    has: function (category) { var c = read(); return !!(c && c[category]); },
    open: function () { open('prefs', true); }
  };

  /* ---------- first visit: show after the preloader has had its moment ---------- */
  if (!read()) {
    var preloaderSkipped = document.documentElement.classList.contains('btrx-skip');
    setTimeout(function () { open('main', false); }, preloaderSkipped ? 400 : 1600);
  }
})();