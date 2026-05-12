// Toast notification function
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `fixed bottom-4 right-4 px-4 py-2 rounded-md text-white ${
    type === 'error' ? 'bg-red-500' : 'bg-blue-500'
  }`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

// Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
});

// Sticky header
window.addEventListener('scroll', () => {
  const header = document.querySelector('header');
  if (window.scrollY > 50) {
    header.classList.add('sticky');
  } else {
    header.classList.remove('sticky');
  }
});

// Mobile hamburger menu toggle
document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      navMenu.classList.toggle('active');
    });
  }
});

// Form validation
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]');
      const message = form.querySelector('textarea');

      if (!email.value || !message.value) {
        showToast('Please fill in all fields', 'error');
        return;
      }

      if (!/\S+@\S+\.\S+/.test(email.value)) {
        showToast('Please enter a valid email address', 'error');
        return;
      }

      // Simulate form submission
      showToast('Message sent successfully!');
      form.reset();
    });
  }
});

// Intersection Observer for scroll animations
document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate');
        }
      });
    },
    {
      threshold: 0.1
    }
  );

  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
  });
});

// Chess game logic
document.addEventListener('DOMContentLoaded', () => {
  const chessboard = document.querySelector('.chessboard');
  if (!chessboard) return;

  let board = Array.from({ length: 8 }, () => Array(8).fill(null));
  let currentPlayer = 'white';
  let selectedPiece = null;

  // Initialize board
  const pieces = {
    white: {
      rook: '♖',
      knight: '♘',
      bishop: '♗',
      queen: '♕',
      king: '♔',
      pawn: '♙'
    },
    black: {
      rook: '♜',
      knight: '♞',
      bishop: '♝',
      queen: '♛',
      king: '♚',
      pawn: '♟'
    }
  };

  // Initialize board state
  function initializeBoard() {
    board[0] = [
      pieces.black.rook,
      pieces.black.knight,
      pieces.black.bishop,
      pieces.black.queen,
      pieces.black.king,
      pieces.black.bishop,
      pieces.black.knight,
      pieces.black.rook
    ];
    board[1] = Array(8).fill(pieces.black.pawn);
    board[6] = Array(8).fill(pieces.white.pawn);
    board[7] = [
      pieces.white.rook,
      pieces.white.knight,
      pieces.white.bishop,
      pieces.white.queen,
      pieces.white.king,
      pieces.white.bishop,
      pieces.white.knight,
      pieces.white.rook
    ];
  }

  // Render board
  function renderBoard() {
    chessboard.innerHTML = '';
    board.forEach((row, i) => {
      row.forEach((piece, j) => {
        const cell = document.createElement('div');
        cell.className = `cell ${(i + j) % 2 === 0 ? 'white' : 'black'}`;
        cell.dataset.row = i;
        cell.dataset.col = j;
        if (piece) {
          cell.textContent = piece;
          cell.classList.add('piece');
        }
        cell.addEventListener('click', handleCellClick);
        chessboard.appendChild(cell);
      });
    });
  }

  // Handle cell click
  function handleCellClick(e) {
    const cell = e.target;
    const row = parseInt(cell.dataset.row);
    const col = parseInt(cell.dataset.col);

    if (selectedPiece) {
      movePiece(row, col);
    } else if (board[row][col] && getPieceColor(board[row][col]) === currentPlayer) {
      selectPiece(row, col);
    }
  }

  // Select piece
  function selectPiece(row, col) {
    selectedPiece = { row, col };
    highlightValidMoves(row, col);
  }

  // Move piece
  function movePiece(row, col) {
    const { row: fromRow, col: fromCol } = selectedPiece;
    const piece = board[fromRow][fromCol];

    if (isValidMove(fromRow, fromCol, row, col)) {
      board[row][col] = piece;
      board[fromRow][fromCol] = null;
      currentPlayer = currentPlayer === 'white' ? 'black' : 'white';
      selectedPiece = null;
      renderBoard();
      checkGameStatus();
    } else {
      showToast('Invalid move', 'error');
    }
  }

  // Check game status
  function checkGameStatus() {
    // Basic checkmate logic would go here
  }

  // Highlight valid moves
  function highlightValidMoves(row, col) {
    // Highlight logic would go here
  }

  // Check if move is valid
  function isValidMove(fromRow, fromCol, toRow, toCol) {
    // Basic move validation logic would go here
    return true; // Placeholder
  }

  // Get piece color
  function getPieceColor(piece) {
    return Object.values(pieces.white).includes(piece) ? 'white' : 'black';
  }

  // Initialize game
  initializeBoard();
  renderBoard();
});

// localStorage persistence example
document.addEventListener('DOMContentLoaded', () => {
  const saveGameBtn = document.querySelector('#save-game');
  if (saveGameBtn) {
    saveGameBtn.addEventListener('click', () => {
      localStorage.setItem('chessGameState', JSON.stringify(board));
      showToast('Game saved!');
    });
  }

  const loadGameBtn = document.querySelector('#load-game');
  if (loadGameBtn) {
    loadGameBtn.addEventListener('click', () => {
      const savedState = localStorage.getItem('chessGameState');
      if (savedState) {
        board = JSON.parse(savedState);
        renderBoard();
        showToast('Game loaded!');
      } else {
        showToast('No saved game found', 'error');
      }
    });
  }
});