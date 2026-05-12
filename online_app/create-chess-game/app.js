// Import required libraries
import { Toast } from './toast.js';

// Initialize variables
let chessBoard = [];
let selectedPiece = null;
let possibleMoves = [];
let turn = 'white';

// Function to create the chess board
function createBoard() {
  // Create an 8x8 grid
  for (let i = 0; i < 8; i++) {
    chessBoard[i] = [];
    for (let j = 0; j < 8; j++) {
      // Initialize each cell with a null value
      chessBoard[i][j] = null;
    }
  }

  // Initialize the starting positions of the pieces
  initializePieces();
}

// Function to initialize the starting positions of the pieces
function initializePieces() {
  // Initialize the pawns
  for (let i = 0; i < 8; i++) {
    chessBoard[1][i] = { type: 'pawn', color: 'white' };
    chessBoard[6][i] = { type: 'pawn', color: 'black' };
  }

  // Initialize the rooks
  chessBoard[0][0] = { type: 'rook', color: 'white' };
  chessBoard[0][7] = { type: 'rook', color: 'white' };
  chessBoard[7][0] = { type: 'rook', color: 'black' };
  chessBoard[7][7] = { type: 'rook', color: 'black' };

  // Initialize the knights
  chessBoard[0][1] = { type: 'knight', color: 'white' };
  chessBoard[0][6] = { type: 'knight', color: 'white' };
  chessBoard[7][1] = { type: 'knight', color: 'black' };
  chessBoard[7][6] = { type: 'knight', color: 'black' };

  // Initialize the bishops
  chessBoard[0][2] = { type: 'bishop', color: 'white' };
  chessBoard[0][5] = { type: 'bishop', color: 'white' };
  chessBoard[7][2] = { type: 'bishop', color: 'black' };
  chessBoard[7][5] = { type: 'bishop', color: 'black' };

  // Initialize the queens
  chessBoard[0][3] = { type: 'queen', color: 'white' };
  chessBoard[7][3] = { type: 'queen', color: 'black' };

  // Initialize the kings
  chessBoard[0][4] = { type: 'king', color: 'white' };
  chessBoard[7][4] = { type: 'king', color: 'black' };
}

// Function to handle piece selection
function selectPiece(row, col) {
  // Check if the selected cell contains a piece
  if (chessBoard[row][col] !== null) {
    // Check if the piece belongs to the current player
    if (chessBoard[row][col].color === turn) {
      // Update the selected piece
      selectedPiece = { row, col };

      // Calculate the possible moves for the selected piece
      possibleMoves = calculateMoves(row, col);
    }
  }
}

// Function to calculate the possible moves for a piece
function calculateMoves(row, col) {
  let moves = [];

  // Calculate the moves based on the piece type
  switch (chessBoard[row][col].type) {
    case 'pawn':
      moves = calculatePawnMoves(row, col);
      break;
    case 'rook':
      moves = calculateRookMoves(row, col);
      break;
    case 'knight':
      moves = calculateKnightMoves(row, col);
      break;
    case 'bishop':
      moves = calculateBishopMoves(row, col);
      break;
    case 'queen':
      moves = calculateQueenMoves(row, col);
      break;
    case 'king':
      moves = calculateKingMoves(row, col);
      break;
  }

  return moves;
}

// Function to calculate the moves for a pawn
function calculatePawnMoves(row, col) {
  let moves = [];

  // Check if the pawn is at the starting position
  if (turn === 'white' && row === 1) {
    // Add the move to the next row
    moves.push({ row: row + 1, col });
    // Add the move to the row after that
    moves.push({ row: row + 2, col });
  } else if (turn === 'black' && row === 6) {
    // Add the move to the previous row
    moves.push({ row: row - 1, col });
    // Add the move to the row before that
    moves.push({ row: row - 2, col });
  } else {
    // Add the move to the next row
    moves.push({ row: turn === 'white' ? row + 1 : row - 1, col });
  }

  return moves;
}

// Function to calculate the moves for a rook
function calculateRookMoves(row, col) {
  let moves = [];

  // Add the moves to the right
  for (let i = col + 1; i < 8; i++) {
    moves.push({ row, col: i });
  }

  // Add the moves to the left
  for (let i = col - 1; i >= 0; i--) {
    moves.push({ row, col: i });
  }

  // Add the moves down
  for (let i = row + 1; i < 8; i++) {
    moves.push({ row: i, col });
  }

  // Add the moves up
  for (let i = row - 1; i >= 0; i--) {
    moves.push({ row: i, col });
  }

  return moves;
}

// Function to calculate the moves for a knight
function calculateKnightMoves(row, col) {
  let moves = [];

  // Add the moves to the top-left
  moves.push({ row: row - 2, col: col - 1 });
  moves.push({ row: row - 1, col: col - 2 });

  // Add the moves to the top-right
  moves.push({ row: row - 2, col: col + 1 });
  moves.push({ row: row - 1, col: col + 2 });

  // Add the moves to the bottom-left
  moves.push({ row: row + 2, col: col - 1 });
  moves.push({ row: row + 1, col: col - 2 });

  // Add the moves to the bottom-right
  moves.push({ row: row + 2, col: col + 1 });
  moves.push({ row: row + 1, col: col + 2 });

  return moves;
}

// Function to calculate the moves for a bishop
function calculateBishopMoves(row, col) {
  let moves = [];

  // Add the moves to the top-left
  for (let i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
    moves.push({ row: i, col: j });
  }

  // Add the moves to the top-right
  for (let i = row - 1, j = col + 1; i >= 0 && j < 8; i--, j++) {
    moves.push({ row: i, col: j });
  }

  // Add the moves to the bottom-left
  for (let i = row + 1, j = col - 1; i < 8 && j >= 0; i++, j--) {
    moves.push({ row: i, col: j });
  }

  // Add the moves to the bottom-right
  for (let i = row + 1, j = col + 1; i < 8 && j < 8; i++, j++) {
    moves.push({ row: i, col: j });
  }

  return moves;
}

// Function to calculate the moves for a queen
function calculateQueenMoves(row, col) {
  let moves = [];

  // Add the moves to the right
  for (let i = col + 1; i < 8; i++) {
    moves.push({ row, col: i });
  }

  // Add the moves to the left
  for (let i = col - 1; i >= 0; i--) {
    moves.push({ row, col: i });
  }

  // Add the moves down
  for (let i = row + 1; i < 8; i++) {
    moves.push({ row: i, col });
  }

  // Add the moves up
  for (let i = row - 1; i >= 0; i--) {
    moves.push({ row: i, col });
  }

  // Add the moves to the top-left
  for (let i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
    moves.push({ row: i, col: j });
  }

  // Add the moves to the top-right
  for (let i = row - 1, j = col + 1; i >= 0 && j < 8; i--, j++) {
    moves.push({ row: i, col: j });
  }

  // Add the moves to the bottom-left
  for (let i = row + 1, j = col - 1; i < 8 && j >= 0; i++, j--) {
    moves.push({ row: i, col: j });
  }

  // Add the moves to the bottom-right
  for (let i = row + 1, j = col + 1; i < 8 && j < 8; i++, j++) {
    moves.push({ row: i, col: j });
  }

  return moves;
}

// Function to calculate the moves for a king
function calculateKingMoves(row, col) {
  let moves = [];

  // Add the moves to the right
  moves.push({ row, col: col + 1 });

  // Add the moves to the left
  moves.push({ row, col: col - 1 });

  // Add the moves down
  moves.push({ row: row + 1, col });

  // Add the moves up
  moves.push({ row: row - 1, col });

  // Add the moves to the top-left
  moves.push({ row: row - 1, col: col - 1 });

  // Add the moves to the top-right
  moves.push({ row: row - 1, col: col + 1 });

  // Add the moves to the bottom-left
  moves.push({ row: row + 1, col: col - 1 });

  // Add the moves to the bottom-right
  moves.push({ row: row + 1, col: col + 1 });

  return moves;
}

// Function to handle piece movement
function movePiece(row, col) {
  // Check if the selected piece can move to the target cell
  if (possibleMoves.find(move => move.row === row && move.col === col)) {
    // Update the position of the selected piece
    chessBoard[row][col] = chessBoard[selectedPiece.row][selectedPiece.col];
    chessBoard[selectedPiece.row][selectedPiece.col] = null;

    // Update the turn
    turn = turn === 'white' ? 'black' : 'white';

    // Reset the selected piece and possible moves
    selectedPiece = null;
    possibleMoves = [];
  }
}

// Function to handle anchor link clicks
function handleAnchorLinkClick(event) {
  // Prevent the default behavior
  event.preventDefault();

  // Get the target element
  const target = event.target.getAttribute('href');

  // Scroll to the target element
  document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
}

// Function to handle sticky header
function handleStickyHeader() {
  // Get the header element
  const header = document.querySelector('header');

  // Add the sticky class when the header is scrolled
  if (window.scrollY > 0) {
    header.classList.add('sticky');
  } else {
    header.classList.remove('sticky');
  }
}

// Function to handle mobile hamburger menu toggle
function handleHamburgerMenuToggle() {
  // Get the hamburger menu element
  const hamburgerMenu = document.querySelector('.hamburger-menu');

  // Toggle the menu
  hamburgerMenu.classList.toggle('active');
}

// Function to handle form validation
function handleFormValidation(event) {
  // Prevent the default behavior
  event.preventDefault();

  // Get the form elements
  const formElements = event.target.elements;

  // Validate the form elements
  for (const element of formElements) {
    if (element.type === 'text' || element.type === 'email') {
      if (element.value.trim() === '') {
        // Show an error message
        showToast('Please fill in all fields');
        return;
      }
    }
  }

  // Submit the form
  event.target.submit();
}

// Function to handle intersection observer
function handleIntersectionObserver() {
  // Get the elements to observe
  const elements = document.querySelectorAll('.observe');

  // Create an intersection observer
  const observer = new IntersectionObserver((entries) => {
    // Loop through the entries
    for (const entry of entries) {
      // Check if the element is visible
      if (entry.isIntersecting) {
        // Add the visible class
        entry.target.classList.add('visible');
      } else {
        // Remove the visible class
        entry.target.classList.remove('visible');
      }
    }
  }, { threshold: 0.5 });

  // Observe the elements
  elements.forEach(element => observer.observe(element));
}

// Function to show a toast notification
function showToast(message) {