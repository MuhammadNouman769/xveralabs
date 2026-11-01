(function () {
  'use strict';
  var BP = 1200, DELAY = 140;
  var header = document.getElementById('xvHeader');
  var burger = document.getElementById('xvBurger');
  var items = [].slice.call(document.querySelectorAll('.xv-item'));
  var desktop = function () { return window.innerWidth > BP; };

  function setOpen(item, on) {
    item.classList.toggle('is-open', on);
    var t = item.querySelector('.xv-trigger');
    if (t) t.setAttribute('aria-expanded', String(on));
  }
  function closeAll(except) {
    items.forEach(function (i) { if (i !== except) { clearTimeout(i._t); setOpen(i, false); } });
  }
  function setMenu(on) {
    header.classList.toggle('is-menu', on);
    burger.setAttribute('aria-expanded', String(on));
    burger.setAttribute('aria-label', on ? 'Close menu' : 'Open menu');
    if (!on) closeAll();
  }
  function showPane(item, id) {
    item.querySelectorAll('.xv-tab').forEach(function (b) { b.classList.toggle('is-on', b.dataset.pane === id); });
    item.querySelectorAll('.xv-pane').forEach(function (p) { p.classList.toggle('is-on', p.id === id); });
  }

  items.forEach(function (item) {
    var trigger = item.querySelector('.xv-trigger');
    item.addEventListener('mouseenter', function () {
      if (!desktop()) return;
      clearTimeout(item._t); closeAll(item); setOpen(item, true);
    });
    item.addEventListener('mouseleave', function () {
      if (!desktop()) return;
      item._t = setTimeout(function () { setOpen(item, false); }, DELAY);
    });
    trigger.addEventListener('click', function () {
      var open = item.classList.contains('is-open');
      closeAll(item);
      setOpen(item, desktop() ? true : !open);
    });
    item.querySelectorAll('.xv-tab').forEach(function (tab) {
      tab.addEventListener('mouseenter', function () { if (desktop()) showPane(item, tab.dataset.pane); });
      tab.addEventListener('click', function () { showPane(item, tab.dataset.pane); });
      tab.addEventListener('focus', function () { showPane(item, tab.dataset.pane); });
    });
  });

  burger.addEventListener('click', function (e) {
    e.stopPropagation();
    setMenu(!header.classList.contains('is-menu'));
  });
  header.addEventListener('click', function (e) {
    if (e.target.closest('a')) { closeAll(); setMenu(false); }
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.xv-header')) { closeAll(); setMenu(false); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = items.filter(function (i) { return i.classList.contains('is-open'); })[0];
    closeAll(); setMenu(false);
    if (open) open.querySelector('.xv-trigger').focus();
  });
  window.addEventListener('resize', function () { setMenu(false); closeAll(); });
  window.addEventListener('scroll', function () {
    header.classList.toggle('is-stuck', window.pageYOffset > 10);
  }, { passive: true });
})();