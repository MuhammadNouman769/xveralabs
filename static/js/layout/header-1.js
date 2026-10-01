(function() {
  'use strict';

  var sidebar = document.getElementById("btrSidebar");
  var openBtn = document.getElementById("btrMenuBtn");
  var closeBtn = document.getElementById("btrClose");
  var overlay = document.getElementById("btrOverlay");
  var header = document.getElementById("btrHeader");

  /* =========================================================
     MEGA MENU — SIRF EK WAQT MEIN EK MENU OPEN
     - Hover: pehla band, doosra open (turant)
     - Click: menu stuck ho jata hai
     - Click again: band
     - Bahar click / Escape: sab band
  ========================================================= */
  var megaParents = document.querySelectorAll('.btrx-mega-parent');

  function closeAllMega(except) {
    megaParents.forEach(function(parent) {
      if (parent !== except) {
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      }
    });
  }

  megaParents.forEach(function(parent) {
    var link = parent.querySelector('.btr-nav__link.has-mega');
    if (!link) return;

    /* ---------- HOVER: sirf ek menu show ho ---------- */
    parent.addEventListener('mouseenter', function() {
      // Agar koi menu clicked (stuck) hai to usay band kar do
      megaParents.forEach(function(p) {
        if (p !== parent && p.dataset.clicked === 'true') {
          p.classList.remove('is-open');
          p.dataset.clicked = '';
        }
      });

      // Pehle sab band karo (except this one)
      closeAllMega(parent);

      // Ab ye open karo
      parent.classList.add('is-open');
    });

    parent.addEventListener('mouseleave', function() {
      // Agar ye clicked (stuck) nahi hai to band kar do
      if (parent.dataset.clicked !== 'true') {
        parent.classList.remove('is-open');
      }
    });

    /* ---------- CLICK: stuck toggle ---------- */
    link.addEventListener('click', function(e) {
      e.preventDefault();

      var wasOpen = parent.classList.contains('is-open');
      var wasClicked = parent.dataset.clicked === 'true';

      // Sab band karo
      closeAllMega(parent);

      if (!wasOpen || !wasClicked) {
        // Open + stuck
        parent.classList.add('is-open');
        parent.dataset.clicked = 'true';
      } else {
        // Already stuck open → close
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      }
    });
  });

  /* Bahar click par sab band */
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.btrx-mega-parent')) {
      megaParents.forEach(function(parent) {
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      });
    }
  });

  /* Escape par sab band */
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      megaParents.forEach(function(parent) {
        parent.classList.remove('is-open');
        parent.dataset.clicked = '';
      });
    }
  });

  /* =========================================================
     SIDEBAR
  ========================================================= */
  if (openBtn && sidebar) {
    openBtn.addEventListener("click", function() {
      sidebar.classList.add("active");
      document.body.style.overflow = "hidden";
    });
  }

  function closeSidebar() {
    sidebar.classList.remove("active");
    document.body.style.overflow = "";
  }

  if (closeBtn) closeBtn.addEventListener("click", closeSidebar);
  if (overlay) overlay.addEventListener("click", closeSidebar);

  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape" && sidebar && sidebar.classList.contains("active")) {
      closeSidebar();
    }
  });

  /* =========================================================
     STICKY HEADER
  ========================================================= */
  var lastScroll = 0;
  window.addEventListener("scroll", function() {
    var currentScroll = window.pageYOffset;
    if (!header) return;
    if (currentScroll > 50) {
      header.classList.add("is-sticky");
    } else {
      header.classList.remove("is-sticky");
    }
    lastScroll = currentScroll;
  }, { passive: true });

})();
