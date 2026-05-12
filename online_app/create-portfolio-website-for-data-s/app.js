// Core portfolio interaction module
import { Menu, X } from 'lucide-react';
import { toast } from 'react-hot-toast';

// Type definitions
type ToastType = 'success' | 'error' | 'loading' | 'custom';
type FormData = {
  name: string;
  email: string;
  message: string;
};

// Store for mobile menu state
const useUIStore = zustand(set => ({
  isMenuOpen: false,
  toggleMenu: () => set(state => ({ isMenuOpen: !state.isMenuOpen })),
  closeMenu: () => set({ isMenuOpen: false })
}));

// Toast notification system
const showToast = (message: string, type: ToastType = 'success', duration = 4000) => {
  const options = {
    duration,
    position: 'bottom-right',
    className: 'portfolio-toast',
    ariaProps: { role: 'status', 'aria-live': 'polite' }
  };

  switch (type) {
    case 'success':
      return toast.success(message, options);
    case 'error':
      return toast.error(message, options);
    case 'loading':
      return toast.loading(message, options);
    default:
      return toast(message, options);
  }
};

// Smooth scroll for anchor links
const initSmoothScroll = () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (!targetId) return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // Update URL without jumping
        history.pushState(null, '', targetId);
      }
    });
  });
};

// Sticky header functionality
const initStickyHeader = () => {
  const header = document.querySelector('header');
  if (!header) return;

  const observer = new IntersectionObserver(
    ([entry]) => {
      header.classList.toggle('sticky', !entry.isIntersecting);
    },
    { threshold: 0.1 }
  );

  const heroSection = document.querySelector('#hero');
  if (heroSection) observer.observe(heroSection);
};

// Mobile menu toggle
const initMobileMenu = () => {
  const { isMenuOpen, toggleMenu, closeMenu } = useUIStore();
  const menuButton = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-menu]');
  
  if (!menuButton || !menu) return;

  const updateMenuState = () => {
    const icon = menuButton.querySelector('svg');
    if (!icon) return;
    
    if (isMenuOpen) {
      menu.classList.remove('hidden');
      icon.replaceWith(<X size={24} />);
      document.body.style.overflow = 'hidden';
    } else {
      menu.classList.add('hidden');
      icon.replaceWith(<Menu size={24} />);
      document.body.style.overflow = '';
    }
  };

  menuButton.addEventListener('click', () => {
    toggleMenu();
    updateMenuState();
  });

  // Close menu when clicking on nav links
  document.querySelectorAll('[data-menu] a').forEach(link => {
    link.addEventListener('click', () => {
      closeMenu();
      updateMenuState();
    });
  });
};

// Form validation and submission
const initContactForm = () => {
  const form = document.querySelector<HTMLFormElement>('#contact-form');
  if (!form) return;

  const validateEmail = (email: string) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData) as unknown as FormData;

    // Validation
    if (!data.name || data.name.length < 2) {
      showToast('Please enter a valid name', 'error');
      return;
    }

    if (!validateEmail(data.email)) {
      showToast('Please enter a valid email', 'error');
      return;
    }

    if (!data.message || data.message.length < 10) {
      showToast('Message should be at least 10 characters', 'error');
      return;
    }

    // Save to localStorage
    try {
      localStorage.setItem('lastContactAttempt', JSON.stringify({
        ...data,
        timestamp: new Date().toISOString()
      }));
    } catch (err) {
      console.error('LocalStorage error:', err);
    }

    // Simulate form submission
    const loadingToast = showToast('Sending message...', 'loading');
    
    try {
      // In a real app, you would use fetch() here
      await new Promise(resolve => setTimeout(resolve, 1500));
      form.reset();
      showToast('Message sent successfully!', 'success');
    } catch (error) {
      showToast('Failed to send message. Please try again.', 'error');
    } finally {
      toast.dismiss(loadingToast);
    }
  });
};

// Intersection Observer for scroll animations
const initScrollAnimations = () => {
  const animateOnScroll = (entries: IntersectionObserverEntry[]) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
      }
    });
  };

  const observer = new IntersectionObserver(animateOnScroll, {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
  });

  document.querySelectorAll('[data-animate]').forEach(el => {
    observer.observe(el);
  });
};

// Theme persistence (dark/light mode)
const initThemeToggle = () => {
  const themeToggle = document.querySelector('[data-theme-toggle]');
  if (!themeToggle) return;

  const getStoredTheme = () => localStorage.getItem('portfolio-theme');
  const setStoredTheme = (theme: string) => localStorage.setItem('portfolio-theme', theme);

  const applyTheme = (theme: string) => {
    document.documentElement.setAttribute('data-theme', theme);
    setStoredTheme(theme);
  };

  themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
    showToast(`Switched to ${newTheme} mode`);
  });

  // Initialize theme
  const preferredTheme = getStoredTheme() || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(preferredTheme);
};

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  initSmoothScroll();
  initStickyHeader();
  initMobileMenu();
  initContactForm();
  initScrollAnimations();
  initThemeToggle();
  
  // Additional data scientist specific features could be added here
  // For example: interactive data visualizations, project filtering, etc.
});

// Export for potential module usage
export {
  showToast,
  useUIStore,
  initSmoothScroll,
  initStickyHeader,
  initMobileMenu,
  initContactForm,
  initScrollAnimations,
  initThemeToggle
};