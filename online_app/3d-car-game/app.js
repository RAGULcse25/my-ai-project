// Import required libraries
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Toast } from './toast.js';

// Initialize variables
let header = document.querySelector('header');
let hamburgerMenu = document.querySelector('.hamburger-menu');
let contactForm = document.querySelector('form');
let toast = new Toast();

// Function to handle smooth scroll for anchor links
function handleSmoothScroll(event) {
  if (event.target.tagName === 'A') {
    event.preventDefault();
    const targetId = event.target.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    gsap.to(window, {
      duration: 1,
      scrollTo: targetElement.offsetTop,
      ease: 'power2.inOut',
    });
  }
}

// Function to handle sticky header
function handleStickyHeader() {
  const headerHeight = header.offsetHeight;
  const scrollPosition = window.scrollY;
  if (scrollPosition > headerHeight) {
    header.classList.add('sticky');
  } else {
    header.classList.remove('sticky');
  }
}

// Function to handle mobile hamburger menu toggle
function handleHamburgerMenuToggle() {
  hamburgerMenu.addEventListener('click', () => {
    hamburgerMenu.classList.toggle('active');
    document.querySelector('nav').classList.toggle('active');
  });
}

// Function to handle form validation
function handleFormValidation(event) {
  event.preventDefault();
  const formData = new FormData(contactForm);
  const name = formData.get('name');
  const email = formData.get('email');
  const message = formData.get('message');
  if (name && email && message) {
    // Send form data to server
    fetch('/api/contact', {
      method: 'POST',
      body: JSON.stringify({ name, email, message }),
      headers: { 'Content-Type': 'application/json' },
    })
      .then((response) => response.json())
      .then((data) => {
        toast.show('Message sent successfully!');
        contactForm.reset();
      })
      .catch((error) => {
        toast.show('Error sending message!');
      });
  } else {
    toast.show('Please fill out all fields!');
  }
}

// Function to handle Intersection Observer for scroll animations
function handleIntersectionObserver() {
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

// Function to handle toast notification
function showToast(message) {
  toast.show(message);
}

// Function to handle localStorage for data persistence
function handleLocalStorage() {
  const storedData = localStorage.getItem('gameData');
  if (storedData) {
    const parsedData = JSON.parse(storedData);
    // Update game state with stored data
  }
}

// Function to handle 3D car game logic
function handleGameLogic() {
  // Initialize game state
  const gameState = {
    score: 0,
    speed: 0,
    acceleration: 0,
  };

  // Update game state on user input
  document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowUp') {
      gameState.acceleration += 0.1;
    } else if (event.key === 'ArrowDown') {
      gameState.acceleration -= 0.1;
    }
  });

  // Update game state on frame
  function updateGameState() {
    gameState.speed += gameState.acceleration;
    gameState.score += gameState.speed;
    // Update game UI with new state
  }

  // Render game frame
  function renderGameFrame() {
    // Clear previous frame
    // Render new frame with updated game state
  }

  // Main game loop
  function gameLoop() {
    updateGameState();
    renderGameFrame();
    requestAnimationFrame(gameLoop);
  }

  gameLoop();
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', handleSmoothScroll);
  window.addEventListener('scroll', handleStickyHeader);
  handleHamburgerMenuToggle();
  if (contactForm) {
    contactForm.addEventListener('submit', handleFormValidation);
  }
  handleIntersectionObserver();
  handleLocalStorage();
  handleGameLogic();
});