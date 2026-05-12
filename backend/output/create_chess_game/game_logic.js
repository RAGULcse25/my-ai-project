```javascript
// Chess Game in JavaScript
class Piece {
  constructor(color, type, x, y) {
    this.color = color;
    this.type = type;
    this.x = x;
    this.y = y;
  }
}

class Board {
  constructor() {
    this.board = this.initializeBoard();
    this.selectedPiece = null;
    this.capturedPieces = [];
    this.enPassant = null;
    this.castling = {
      white: { king: true, queen: true, kingRook: true, queenRook: true },
      black: { king: true, queen: true, kingRook: true, queenRook: true },
    };
  }

  initializeBoard() {
    let board = [];
    for (let i = 0; i < 8; i++) {
      board[i] = [];
      for (let j = 0; j < 8; j++) {
        if (i === 1) {
          board[i][j] = new Piece("black", "pawn", j, i);
        } else if (i === 6) {
          board[i][j] = new Piece("white", "pawn", j, i);
        } else if (i === 0) {
          if (j === 0 || j === 7) {
            board[i][j] = new Piece("black", "rook", j, i);
          } else if (j === 1 || j === 6) {
            board[i][j] = new Piece("black", "knight", j, i);
          } else if (j === 2 || j === 5) {
            board[i][j] = new Piece("black", "bishop", j, i);
          } else if (j === 3) {
            board[i][j] = new Piece("black", "queen", j, i);
          } else if (j === 4) {
            board[i][j] = new Piece("black", "king", j, i);
          }
        } else if (i === 7) {
          if (j === 0 || j === 7) {
            board[i][j] = new Piece("white", "rook", j, i);
          } else if (j === 1 || j === 6) {
            board[i][j] = new Piece("white", "knight", j, i);
          } else if (j === 2 || j === 5) {
            board[i][j] = new Piece("white", "bishop", j, i);
          } else if (j === 3) {
            board[i][j] = new Piece("white", "queen", j, i);
          } else if (j === 4) {
            board[i][j] = new Piece("white", "king", j, i);
          }
        } else {
          board[i][j] = null;
        }
      }
    }
    return board;
  }

  movePiece(x1, y1, x2, y2) {
    if (this.board[y1][x1] !== null) {
      let piece = this.board[y1][x1];
      if (this.isValidMove(piece, x1, y1, x2, y2)) {
        if (piece.type === "king") {
          if (Math.abs(x2 - x1) === 2) {
            this.castling[piece.color].king = false;
            if (x2 === 2) {
              this.board[y1][0].x = 3;
              this.board[y1][3] = this.board[y1][0];
              this.board[y1][0] = null;
            } else if (x2 === 6) {
              this.board[y1][7].x = 5;
              this.board[y1][5] = this.board[y1][7];
              this.board[y1][7] = null;
            }
          }
        }
        if (piece.type === "rook") {
          if (piece.x === 0 || piece.x === 7) {
            if (piece.color === "white") {
              if (piece.x === 0) {
                this.castling.white.kingRook = false;
              } else {
                this.castling.white.queenRook = false;
              }
            } else {
              if (piece.x === 0) {
                this.castling.black.kingRook = false;
              } else {
                this.castling.black.queenRook = false;
              }
            }
          }
        }
        if (piece.type === "pawn") {
          if (Math.abs(y2 - y1) === 2) {
            this.enPassant = { x: x1, y: y1 };
          }
          if (y2 === 0 || y2 === 7) {
            this.promotePawn(piece, x2, y2);
          }
        }
        this.board[y2][x2] = piece;
        this.board[y1][x1] = null;
        piece.x = x2;
        piece.y = y2;
        this.selectedPiece = null;
      }
    }
  }

  promotePawn(piece, x, y) {
    let promotion = prompt("Enter promotion (Q, R, B, N): ");
    if (promotion === "Q") {
      piece.type = "queen";
    } else if (promotion === "R") {
      piece.type = "rook";
    } else if (promotion === "B") {
      piece.type = "bishop";
    } else if (promotion === "N") {
      piece.type = "knight";
    }
  }

  isValidMove(piece, x1, y1, x2, y2) {
    if (piece.type === "king") {
      return this.isValidKingMove(piece, x1, y1, x2, y2);
    } else if (piece.type === "queen") {
      return this.isValidQueenMove(piece, x1, y1, x2, y2);
    } else if (piece.type === "rook") {
      return this.isValidRookMove(piece, x1, y1, x2, y2);
    } else if (piece.type === "bishop") {
      return this.isValidBishopMove(piece, x1, y1, x2, y2);
    } else if (piece.type === "knight") {
      return this.isValidKnightMove(piece, x1, y1, x2, y2);
    } else if (piece.type === "pawn") {
      return this.isValidPawnMove(piece, x1, y1, x2, y2);
    }
  }

  isValidKingMove(piece, x1, y1, x2, y2) {
    if (Math.abs(x2 - x1) <= 1 && Math.abs(y2 - y1) <= 1) {
      if (this.board[y2][x2] !== null && this.board[y2][x2].color === piece.color) {
        return false;
      }
      return true;
    }
    if (Math.abs(x2 - x1) === 2 && y2 === y1) {
      if (x2 === 2) {
        if (this.board[y1][1] !== null || this.board[y1][2] !== null || this.board[y1][3] !== null) {
          return false;
        }
      } else if (x2 === 6) {
        if (this.board[y1][5] !== null || this.board[y1][6] !== null) {
          return false;
        }
      }
      return true;
    }
    return false;
  }

  isValidQueenMove(piece, x1, y1, x2, y2) {
    if (this.isValidBishopMove(piece, x1, y1, x2, y2) || this.isValidRookMove(piece, x1, y1, x2, y2)) {
      return true;
    }
    return false;
  }

  isValidRookMove(piece, x1, y1, x2, y2) {
    if (x1 === x2) {
      for (let i = Math.min(y1, y2) + 1; i < Math.max(y1, y2); i++) {
        if (this.board[i][x1] !== null) {
          return false;
        }
      }
      return true;
    } else if (y1 === y2) {
      for (let i = Math.min(x1, x2) + 1; i < Math.max(x1, x2); i++) {
        if (this.board[y1][i] !== null) {
          return false;
        }
      }
      return true;
    }
    return false;
  }

  isValidBishopMove(piece, x1, y1, x2, y2) {
    if (Math.abs(x2 - x1) === Math.abs(y2 - y1)) {
      let dx = x2 > x1 ? 1 : -1;
      let dy = y2 > y1 ? 1 : -1;
      for (let i = 1; i < Math.abs(x2 - x1); i++) {
        if (this.board[y1 + i * dy][x1 + i * dx] !== null) {
          return false;
        }
      }
      return true;
    }
    return false;
  }

  isValidKnightMove(piece, x1, y1, x2, y2) {
    if ((Math.abs(x2 - x1) === 2 && Math.abs(y2 - y1) === 1) || (Math.abs(x2 - x1) === 1 && Math.abs(y2 - y1) === 2)) {
      return true;
    }
    return false;
  }

  isValidPawnMove(piece, x1, y1, x2, y2) {
    if (piece.color === "white") {
      if (y1 === 1 && y2 === 3 && x1 === x2 && this.board[y1 + 1][x1] === null && this.board[y2][x2] === null) {
        return true;
      }
      if (y2 === y1 + 1 && x1 === x2 && this.board[y2][x2] === null) {
        return true;
      }
      if (y2 === y1 + 1 && Math.abs(x2 - x1) === 1 && this.board[y2][x2] !== null && this.board[y2][x2].color === "black") {
        return true;
      }
      if (this.enPassant !== null && this.enPassant.x === x2 && this.enPassant.y === y1) {
        return true;
      }
    } else {
      if (y1 === 6 && y2 === 4 && x1 === x2 && this.board[y1 - 1][x1] === null && this.board[y2][x2] === null) {
        return true;
      }
      if (y2 === y1 - 1 && x1 === x2 && this.board[y2][x2] === null) {
        return true;
      }
      if (y2 === y1 - 1 && Math.abs(x2 - x1) === 1 && this.board[y2][x2] !== null && this.board[y2][x2].color === "white") {
        return true;
      }
      if (this.enPassant !== null && this.enPassant.x === x2 && this.enPassant.y === y1) {
        return true;
      }
    }
    return false;
  }

  checkCheck(color) {
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 8; j++) {
        if (this.board[i][j] !== null && this.board[i][j].color === color && this.board[i][j].type === "king") {
          for (let k = 0; k < 8; k++) {
            for (let l = 0; l < 8; l++) {
              if (this.board[k][l] !== null && this.board[k][l].color !== color) {
                if (this.isValidMove(this.board[k][l], l, k, j, i)) {
                  return true;
                }
              }
            }
          }
        }
      }
    }
    return false;
  }

  checkCheckmate(color) {
    if (this.checkCheck(color)) {
      for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
          if (this.board[i][j] !== null && this.board[i][j].color === color) {
            for (let k = 0; k < 8; k++) {
              for (let l = 0; l < 8; l++) {
                if (this.isValidMove(this.board[i][j], j, i, l, k)) {
                  let temp = this.board[k][l];
                  this.board[k][l] = this.board[i][j];
                  this.board[i][j] = null;
                  this.board[k][l].x = l;
                  this.board[k][l].y = k;
                  if (!this.checkCheck(color)) {
                    this.board[i][j] = this.board[k][l];
                    this.board[k][l] = temp;
                    this.board[i][j].x = j;
                    this.board[i][j].y = i;
                    return false;
                  }
                  this.board[i][j] = this.board[k][l];
                  this.board[k][l] = temp;
                  this.board[i][j].x = j;
                  this.board[i][j].y = i;
                }
              }
            }
          }
        }
      }
      return true;
    }
    return false;
  }
}

class AI {
  constructor(board) {
    this.board = board;
  }

  minimax(depth, isMaximizing) {
    if (depth === 0 || this.board.checkCheckmate("black")) {
      if (this.board.checkCheckmate("black")) {
        return -10000;
      } else if (this.board.checkCheckmate("white")) {
        return 10000;
      } else {
        return 0;
      }
    }
    if (isMaximizing) {
      let bestScore = -10000;
      for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
          if (this.board.board[i][j] !== null && this.board.board[i][j].color === "black") {
            for (let k = 0; k < 8; k++) {
              for (let l = 0; l < 8; l++) {
                if (this.board.isValidMove(this.board.board[i][j], j, i, l, k)) {
                  let temp = this.board.board[k][l];
                  this.board.board[k][l] = this.board.board[i][j];
                  this.board.board[i][j] = null;
                  this.board.board[k][l].x = l;
                  this.board.board[k][l].y = k;
                  let score = this.minimax(depth - 1, false);
                  this.board.board[i][j] = this.board.board[k][l];
                  this.board.board[k][l] = temp;
                  this.board.board[i][j].x = j;
                  this.board.board[i][j].y = i;
                  bestScore = Math.max(score, bestScore);
                }
              }
            }
          }
        }
      }
      return bestScore;
    } else {
      let bestScore = 10000;
      for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
          if (this.board.board[i][j] !== null && this.board.board[i][j].color === "white") {
            for (let k = 0; k < 8; k++) {
              for (let l = 0; l < 8; l++) {
                if (this.board.isValidMove(this.board.board[i][j], j, i, l, k