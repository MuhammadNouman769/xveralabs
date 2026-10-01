(function() {
  'use strict';

  var header = document.getElementById('btrHeader');
  var openBtn = document.getElementById('btrMenuBtn');
  var nav = document.getElementById('btrPrimaryNav');
  var megaParents = document.querySelectorAll('.btrx-mega-parent');

  function closeAllMega(except) {
    megaParents.forEach(function(parent) {
      if (parent !== except) {
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      }
    });
  }

  function setMobileMenuOpen(isOpen) {
    if (!header || !openBtn) return;

    header.classList.toggle('mobile-menu-open', isOpen);
    openBtn.setAttribute('aria-expanded', String(isOpen));

    if (!isOpen) {
      closeAllMega(null);
    }
  }

  megaParents.forEach(function(parent) {
    var link = parent.querySelector('.btr-nav__link.has-mega');
    if (!link) return;

    parent.addEventListener('mouseenter', function() {
      if (window.innerWidth > 992) {
        megaParents.forEach(function(p) {
          if (p !== parent && p.dataset.clicked === 'true') {
            p.classList.remove('is-open');
            p.dataset.clicked = '';
          }
        });
        closeAllMega(parent);
        parent.classList.add('is-open');
      }
    });

    parent.addEventListener('mouseleave', function() {
      if (window.innerWidth > 992 && parent.dataset.clicked !== 'true') {
        parent.classList.remove('is-open');
      }
    });

    link.addEventListener('click', function(e) {
      if (window.innerWidth <= 992) {
        e.preventDefault();
        var wasOpen = parent.classList.contains('is-open');
        var wasClicked = parent.dataset.clicked === 'true';

        closeAllMega(parent);

        if (!wasOpen || !wasClicked) {
          parent.classList.add('is-open');
          parent.dataset.clicked = 'true';
        } else {
          parent.classList.remove('is-open');
          parent.dataset.clicked = '';
        }
        return;
      }

      e.preventDefault();
      var wasOpenDesktop = parent.classList.contains('is-open');
      var wasClickedDesktop = parent.dataset.clicked === 'true';

      closeAllMega(parent);

      if (!wasOpenDesktop || !wasClickedDesktop) {
        parent.classList.add('is-open');
        parent.dataset.clicked = 'true';
      } else {
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      }
    });
  });

  if (openBtn) {
    openBtn.addEventListener('click', function() {
      if (!nav) return;
      var isOpen = header && header.classList.contains('mobile-menu-open');
      setMobileMenuOpen(!isOpen);
    });
  }

  document.addEventListener('click', function(e) {
    var clickedInsideHeader = e.target.closest('.btr-header');
    if (!clickedInsideHeader && header) {
      setMobileMenuOpen(false);
    }

    if (!e.target.closest('.btrx-mega-parent')) {
      megaParents.forEach(function(parent) {
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      });
    }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      setMobileMenuOpen(false);
      megaParents.forEach(function(parent) {
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      });
    }
  });

  window.addEventListener('resize', function() {
    if (window.innerWidth > 992) {
      setMobileMenuOpen(false);
    }
  });

  var lastScroll = 0;
  window.addEventListener('scroll', function() {
    var currentScroll = window.pageYOffset;
    if (!header) return;
    if (currentScroll > 50) {
      header.classList.add('is-sticky');
    } else {
      header.classList.remove('is-sticky');
    }
    lastScroll = currentScroll;
  }, { passive: true });
})();
