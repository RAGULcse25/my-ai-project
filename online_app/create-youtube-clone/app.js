// Import required libraries
import { Toast } from './toast.js';

// Initialize variables
let header = document.querySelector('header');
let hamburgerMenu = document.querySelector('.hamburger-menu');
let mobileMenu = document.querySelector('.mobile-menu');
let contactForm = document.querySelector('#contact-form');
let toast = new Toast();

// Function to handle smooth scroll for anchor links
function smoothScroll(event) {
  event.preventDefault();
  const targetId = event.target.getAttribute('href');
  const targetElement = document.querySelector(targetId);
  targetElement.scrollIntoView({ behavior: 'smooth' });
}

// Function to handle sticky header
function stickyHeader() {
  const scrollPosition = window.scrollY;
  if (scrollPosition > 50) {
    header.classList.add('sticky');
  } else {
    header.classList.remove('sticky');
  }
}

// Function to handle mobile hamburger menu toggle
function toggleMobileMenu() {
  mobileMenu.classList.toggle('active');
  hamburgerMenu.classList.toggle('active');
}

// Function to handle form validation
function validateForm(event) {
  event.preventDefault();
  const formData = new FormData(contactForm);
  const name = formData.get('name');
  const email = formData.get('email');
  const message = formData.get('message');

  if (name === '' || email === '' || message === '') {
    toast.showError('Please fill out all fields');
    return;
  }

  // Send form data to server
  fetch('/contact', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        toast.showSuccess('Message sent successfully');
        contactForm.reset();
      } else {
        toast.showError('Error sending message');
      }
    })
    .catch((error) => {
      toast.showError('Error sending message');
    });
}

// Function to handle Intersection Observer for scroll animations
function intersectionObserver() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
      }
    });
  }, { threshold: 0.5 });

  const elements = document.querySelectorAll('.animate-on-scroll');
  elements.forEach((element) => {
    observer.observe(element);
  });
}

// Function to handle localStorage for data persistence
function saveDataToLocalStorage(key, value) {
  localStorage.setItem(key, value);
}

function getDataFromLocalStorage(key) {
  return localStorage.getItem(key);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Add event listener to anchor links for smooth scroll
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach((link) => {
    link.addEventListener('click', smoothScroll);
  });

  // Add event listener to window for sticky header
  window.addEventListener('scroll', stickyHeader);

  // Add event listener to hamburger menu for mobile toggle
  hamburgerMenu.addEventListener('click', toggleMobileMenu);

  // Add event listener to contact form for validation
  if (contactForm) {
    contactForm.addEventListener('submit', validateForm);
  }

  // Initialize Intersection Observer for scroll animations
  intersectionObserver();
});

// Toast notification function
function showToast(message, type) {
  toast.show(message, type);
}

// Export functions for use in other scripts
export { smoothScroll, stickyHeader, toggleMobileMenu, validateForm, intersectionObserver, saveDataToLocalStorage, getDataFromLocalStorage, showToast };