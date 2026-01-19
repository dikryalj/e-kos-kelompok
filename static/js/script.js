// Modern JavaScript for e_kost application
document.addEventListener("DOMContentLoaded", function () {
  console.log("e_kost application loaded");

  // Scroll-triggered animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, observerOptions);

  // Observe all elements with fade-in-scroll class
  document.querySelectorAll('.fade-in-scroll').forEach(el => {
    observer.observe(el);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Enhanced hover effects for cards
  document.querySelectorAll('.group').forEach(card => {
    card.addEventListener('mouseenter', function () {
      this.style.transform = 'translateY(-8px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function () {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });

  // Parallax effect for hero section
  window.addEventListener('scroll', function () {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero-section');
    if (hero) {
      hero.style.backgroundPositionY = -(scrolled * 0.5) + 'px';
    }
  });

  // Typing effect for hero text (optional)
  const heroTitle = document.querySelector('.hero-title');
  if (heroTitle) {
    const text = heroTitle.textContent;
    heroTitle.textContent = '';
    let i = 0;
    const timer = setInterval(() => {
      if (i < text.length) {
        heroTitle.textContent += text.charAt(i);
        i++;
      } else {
        clearInterval(timer);
      }
    }, 100);
  }

  // Example: Handle form submission
  const bookingForm = document.getElementById("booking-form");
  if (bookingForm) {
    bookingForm.addEventListener("submit", function (e) {
      e.preventDefault();
      alert("Booking submitted!");
    });
  }

  // Add loading animation for buttons
  document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('click', function () {
      this.innerHTML = '<span class="animate-spin">⟳</span> Memproses...';
      setTimeout(() => {
        this.innerHTML = 'Booking Sekarang';
      }, 2000);
    });
  });

  // Mobile menu toggle
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');

      // Animate icon (optional simplicity)
      const icon = mobileMenuBtn.querySelector('svg');
      if (mobileMenu.classList.contains('hidden')) {
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>';
      } else {
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>';
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!mobileMenuBtn.contains(e.target) && !mobileMenu.contains(e.target) && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
        const icon = mobileMenuBtn.querySelector('svg');
        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>';
      }
    });
  }

  // Profile Dropdown Toggle
  const profileDropdownBtn = document.getElementById('profileDropdownBtn');
  const profileDropdownMenu = document.getElementById('profileDropdownMenu');

  if (profileDropdownBtn && profileDropdownMenu) {
    console.log('Profile dropdown initialized');
    profileDropdownBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      e.preventDefault();
      console.log('Dropdown clicked, toggling...');
      profileDropdownMenu.classList.toggle('hidden');
      console.log('Dropdown hidden class:', profileDropdownMenu.classList.contains('hidden'));
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!profileDropdownBtn.contains(e.target) && !profileDropdownMenu.contains(e.target)) {
        profileDropdownMenu.classList.add('hidden');
      }
    });
  }

  // Fetch and update notification badge count
  const notifBadge = document.getElementById('notifBadge');
  if (notifBadge) {
    fetch('/api/unread-notifications-count')
      .then(response => response.json())
      .then(data => {
        if (data.count > 0) {
          notifBadge.textContent = data.count;
          notifBadge.classList.remove('hidden');
        } else {
          notifBadge.classList.add('hidden');
        }
      })
      .catch(error => {
        console.error('Error fetching notification count:', error);
      });
  }
});
