(function () {
  'use strict';

  var BREAKPOINT = 1280;   // must match the CSS 1280px breakpoint
  var CLOSE_DELAY = 150;   // ms, so the menu doesn't flicker on hover

  var header = document.getElementById('btrHeader');
  var openBtn = document.getElementById('btrMenuBtn');
  var nav = document.getElementById('btrPrimaryNav');
  var parents = Array.prototype.slice.call(document.querySelectorAll('.btrx-mega-parent'));

  function isDesktop() {
    return window.innerWidth > BREAKPOINT;
  }

  function setOpen(parent, open) {
    var trigger = parent.querySelector('.has-mega');
    parent.classList.toggle('is-open', open);
    if (trigger) trigger.setAttribute('aria-expanded', String(open));
    if (!open) parent.dataset.pinned = '';
  }

  function closeAll(except) {
    parents.forEach(function (p) {
      if (p !== except) {
        clearTimeout(p._timer);
        setOpen(p, false);
      }
    });
  }

  function setMobileMenuOpen(isOpen) {
    if (!header || !openBtn) return;
    header.classList.toggle('mobile-menu-open', isOpen);
    openBtn.setAttribute('aria-expanded', String(isOpen));
    if (!isOpen) closeAll(null);
  }

  parents.forEach(function (parent) {
    var trigger = parent.querySelector('.has-mega');
    if (!trigger) return;

    // Desktop: hover opens, small delay on leave
    parent.addEventListener('mouseenter', function () {
      if (!isDesktop()) return;
      clearTimeout(parent._timer);
      closeAll(parent);
      setOpen(parent, true);
    });

    parent.addEventListener('mouseleave', function () {
      if (!isDesktop() || parent.dataset.pinned === 'true') return;
      parent._timer = setTimeout(function () {
        setOpen(parent, false);
      }, CLOSE_DELAY);
    });

    // Click / Enter / Space (buttons fire click for keyboard too)
    trigger.addEventListener('click', function () {
      var isOpen = parent.classList.contains('is-open');

      if (!isDesktop()) {
        // Mobile: accordion
        closeAll(parent);
        setOpen(parent, !isOpen);
        return;
      }

      // Desktop: first click pins a hover-opened menu, second click closes it
      closeAll(parent);
      if (isOpen && parent.dataset.pinned !== 'true') {
        parent.dataset.pinned = 'true';
      } else if (isOpen) {
        setOpen(parent, false);
      } else {
        setOpen(parent, true);
        parent.dataset.pinned = 'true';
      }
    });
  });

  // Hamburger
  if (openBtn) {
    openBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var isOpen = header && header.classList.contains('mobile-menu-open');
      setMobileMenuOpen(!isOpen);
    });
  }

  // Close the mobile menu after tapping a real link
  if (nav) {
    nav.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (a && !isDesktop()) setMobileMenuOpen(false);
    });
  }

  // Click outside closes everything
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.btr-header')) setMobileMenuOpen(false);
    if (!e.target.closest('.btrx-mega-parent')) closeAll(null);
  });

  // Escape closes and returns focus to the trigger
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var openParent = parents.filter(function (p) { return p.classList.contains('is-open'); })[0];
    var focusInside = openParent && openParent.contains(document.activeElement);
    setMobileMenuOpen(false);
    closeAll(null);
    if (focusInside) {
      var t = openParent.querySelector('.has-mega');
      if (t) t.focus();
    }
  });

  // Keyboard: close the menu when focus leaves it
  parents.forEach(function (parent) {
    parent.addEventListener('focusout', function (e) {
      if (!isDesktop()) return;
      if (e.relatedTarget && parent.contains(e.relatedTarget)) return;
      if (parent.dataset.pinned === 'true') {
        // pinned menus close when focus moves elsewhere
        setOpen(parent, false);
      }
    });
  });

  // Reset state when crossing the breakpoint
  window.addEventListener('resize', function () {
    setMobileMenuOpen(false);
    closeAll(null);
  });

  // Sticky header
  window.addEventListener('scroll', function () {
    if (!header) return;
    header.classList.toggle('is-sticky', window.pageYOffset > 50);
  }, { passive: true });
})();