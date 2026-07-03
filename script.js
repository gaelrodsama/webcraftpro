/* ================================================================ */
/*  SCRIPT.JS — Soberanes Bienes Raíces                             */
/*  Scroll reveal · Navbar · Hamburger · Smooth scroll              */
/*  Sin dependencias externas · Vanilla JS                          */
/* ================================================================ */

(function () {
  'use strict';

  /* ------------------------------------------------------------------ */
  /*  1. SCROLL REVEAL — IntersectionObserver                            */
  /* ------------------------------------------------------------------ */
  function initScrollReveal() {
    const elements = document.querySelectorAll('[data-reveal]');

    if (elements.length === 0) return;

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var el = entry.target;
            var delay = el.getAttribute('data-delay') || 0;
            setTimeout(function () {
              el.classList.add('revealed');
            }, parseInt(delay, 10));
            observer.unobserve(el);
          }
        });
      },
      {
        threshold: 0.15,
        rootMargin: '0px 0px -40px 0px'
      }
    );

    elements.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ------------------------------------------------------------------ */
  /*  2. NAVBAR SCROLL EFFECT                                           */
  /* ------------------------------------------------------------------ */
  function initNavbarScroll() {
    var navbar = document.getElementById('navbar');
    if (!navbar) return;

    var scrollHandler = function () {
      if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    };

    window.addEventListener('scroll', scrollHandler, { passive: true });
    // Run once on load to set initial state
    scrollHandler();
  }

  /* ------------------------------------------------------------------ */
  /*  3. HAMBURGER MENU TOGGLE (Mobile)                                 */
  /* ------------------------------------------------------------------ */
  function initHamburgerMenu() {
    var toggle = document.getElementById('navToggle');
    var menu = document.getElementById('navMenu');

    if (!toggle || !menu) return;

    toggle.addEventListener('click', function () {
      var isOpen = menu.classList.toggle('open');
      toggle.classList.toggle('active');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close menu on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /*  4. CLOSE NAV — called from HTML onclick                            */
  /* ------------------------------------------------------------------ */
  window.closeNav = function () {
    var menu = document.getElementById('navMenu');
    var toggle = document.getElementById('navToggle');
    if (menu && menu.classList.contains('open')) {
      menu.classList.remove('open');
      if (toggle) {
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
      }
      document.body.style.overflow = '';
    }
  };

  /* ------------------------------------------------------------------ */
  /*  5. SMOOTH SCROLL — for any anchor link with href="#..."           */
  /* ------------------------------------------------------------------ */
  function initSmoothScroll() {
    document.addEventListener('click', function (e) {
      var target = e.target.closest('a[href^="#"]');
      if (!target) return;

      var id = target.getAttribute('href');
      if (!id || id === '#') return;

      var section = document.querySelector(id);
      if (!section) return;

      e.preventDefault();

      var navHeight = window.innerWidth <= 768
        ? 64   // mobile nav height
        : 72;  // desktop nav height

      var top = section.getBoundingClientRect().top + window.pageYOffset - navHeight;

      window.scrollTo({
        top: top,
        behavior: 'smooth'
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /*  6. INIT — run everything on DOM ready                              */
  /* ------------------------------------------------------------------ */
  function init() {
    initScrollReveal();
    initNavbarScroll();
    initHamburgerMenu();
    initSmoothScroll();
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();