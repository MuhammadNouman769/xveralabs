(function () {
  'use strict';

  var BREAKPOINT = 1280; // CSS ke 1280px se match hona chahiye

  var header = document.getElementById('btrHeader');
  var openBtn = document.getElementById('btrMenuBtn');
  var nav = document.getElementById('btrPrimaryNav');
  var megaParents = document.querySelectorAll('.btrx-mega-parent');

  function isDesktop() {
    return window.innerWidth > BREAKPOINT;
  }

  function resetParent(parent) {
    parent.classList.remove('is-open');
    parent.dataset.clicked = '';
  }

  function closeAllMega(except) {
    megaParents.forEach(function (parent) {
      if (parent !== except) resetParent(parent);
    });
  }

  function setMobileMenuOpen(isOpen) {
    if (!header || !openBtn) return;
    header.classList.toggle('mobile-menu-open', isOpen);
    openBtn.setAttribute('aria-expanded', String(isOpen));
    if (!isOpen) closeAllMega(null);
  }

  function toggleParent(parent) {
    var wasOpen = parent.classList.contains('is-open');
    var wasClicked = parent.dataset.clicked === 'true';

    closeAllMega(parent);

    if (!wasOpen || !wasClicked) {
      parent.classList.add('is-open');
      parent.dataset.clicked = 'true';
    } else {
      resetParent(parent);
    }
  }

  megaParents.forEach(function (parent) {
    var link = parent.querySelector('.btr-nav__link.has-mega');
    if (!link) return;

    // Desktop: hover se open/close
    parent.addEventListener('mouseenter', function () {
      if (!isDesktop()) return;
      closeAllMega(parent);
      parent.classList.add('is-open');
    });

    parent.addEventListener('mouseleave', function () {
      if (isDesktop() && parent.dataset.clicked !== 'true') {
        parent.classList.remove('is-open');
      }
    });

    link.addEventListener('click', function (e) {
      var href = link.getAttribute('href');
      var isDummy = !href || href === '#' || href === '#!';

      if (!isDesktop()) {
        // Mobile: tap par submenu khulta/band hota hai
        e.preventDefault();
        toggleParent(parent);
        return;
      }

      // Desktop: sirf dummy links par preventDefault, real links normal navigate karein
      if (isDummy) {
        e.preventDefault();
        toggleParent(parent);
      }
    });
  });

  // Hamburger toggle
  if (openBtn) {
    openBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (!nav) return;
      var isOpen = header && header.classList.contains('mobile-menu-open');
      setMobileMenuOpen(!isOpen);
    });
  }

  // Mobile menu mein kisi final link par click karne se menu band ho
  if (nav) {
    nav.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || isDesktop()) return;
      if (a.classList.contains('has-mega')) return; // yeh accordion toggle hai
      setMobileMenuOpen(false);
    });
  }

  // Bahar click par sab band
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.btr-header')) {
      setMobileMenuOpen(false);
    }
    if (!e.target.closest('.btrx-mega-parent')) {
      megaParents.forEach(resetParent);
    }
  });

  // Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      setMobileMenuOpen(false);
      megaParents.forEach(resetParent);
    }
  });

  // Resize: desktop par aate hi mobile state reset
  window.addEventListener('resize', function () {
    if (isDesktop()) {
      setMobileMenuOpen(false);
      megaParents.forEach(resetParent);
    }
  });

  // Sticky header
  window.addEventListener('scroll', function () {
    if (!header) return;
    if (window.pageYOffset > 50) {
      header.classList.add('is-sticky');
    } else {
      header.classList.remove('is-sticky');
    }
  }, { passive: true });
})();