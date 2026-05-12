# core/rule_engine.py
# ============================================================
# RULE ENGINE — modular, extendable rules for all app types
# Chess rules, Ludo rules, Social app rules, all in one place
# Used by GameLogicAgent to generate correct game code
# ============================================================

from dataclasses import dataclass, field
from typing import List, Dict, Any

# ─────────────────────────────────────────────────────────────
# BASE RULE CLASS
# ─────────────────────────────────────────────────────────────
@dataclass
class Rule:
    name:        str
    description: str
    priority:    int = 0  # Higher = checked first
    enabled:     bool = True

    def validate(self, state: dict) -> bool:
        """Override in subclasses"""
        return True


# ═══════════════════════════════════════════════════════════
#  CHESS RULES
# ═══════════════════════════════════════════════════════════
CHESS_RULES = {
    "pawn": {
        "moves": [
            "Forward 1 square if empty",
            "Forward 2 squares from starting rank if both squares empty",
            "Diagonal capture: 1 square diagonally forward to occupied enemy square",
        ],
        "special": [
            "En passant: capture pawn that just moved 2 squares past capture point",
            "Promotion: reaching 8th rank → choose Q/R/B/N (default Queen)",
        ],
        "code_pattern": """
function getPawnMoves(board, row, col, color, enPassantTarget) {
    const moves = [];
    const dir = color === 'w' ? -1 : 1;
    const startRow = color === 'w' ? 6 : 1;
    // Forward 1
    if (isEmpty(board, row+dir, col))
        moves.push({r:row+dir, c:col});
    // Forward 2 from start
    if (row === startRow && isEmpty(board, row+dir, col) && isEmpty(board, row+2*dir, col))
        moves.push({r:row+2*dir, c:col, special:'double'});
    // Diagonal captures
    for (const dc of [-1, 1]) {
        if (isEnemy(board, row+dir, col+dc, color))
            moves.push({r:row+dir, c:col+dc});
        // En passant
        if (enPassantTarget && enPassantTarget.r===row+dir && enPassantTarget.c===col+dc)
            moves.push({r:row+dir, c:col+dc, special:'enpassant'});
    }
    return moves;
}"""
    },
    "rook": {
        "moves": ["Any number of squares horizontally or vertically", "Blocked by pieces"],
        "special": ["Castling with unmoved king (both unmoved, no pieces between, king not in check)"],
        "code_pattern": """
function getRookMoves(board, row, col, color) {
    const moves = [];
    for (const [dr, dc] of [[1,0],[-1,0],[0,1],[0,-1]]) {
        let r=row+dr, c=col+dc;
        while (inBounds(r,c)) {
            if (isEmpty(board,r,c)) { moves.push({r,c}); r+=dr; c+=dc; }
            else { if (isEnemy(board,r,c,color)) moves.push({r,c}); break; }
        }
    }
    return moves;
}"""
    },
    "knight": {
        "moves": ["L-shape: 2+1 or 1+2 squares", "Jumps over pieces"],
        "special": [],
        "code_pattern": """
function getKnightMoves(board, row, col, color) {
    return [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]
        .map(([dr,dc]) => ({r:row+dr, c:col+dc}))
        .filter(({r,c}) => inBounds(r,c) && !isAlly(board,r,c,color));
}"""
    },
    "bishop": {
        "moves": ["Any number of squares diagonally", "Blocked by pieces"],
        "special": [],
        "code_pattern": """
function getBishopMoves(board, row, col, color) {
    const moves = [];
    for (const [dr,dc] of [[1,1],[1,-1],[-1,1],[-1,-1]]) {
        let r=row+dr, c=col+dc;
        while (inBounds(r,c)) {
            if (isEmpty(board,r,c)) { moves.push({r,c}); r+=dr; c+=dc; }
            else { if (isEnemy(board,r,c,color)) moves.push({r,c}); break; }
        }
    }
    return moves;
}"""
    },
    "queen": {
        "moves": ["Combines rook + bishop movements"],
        "special": [],
        "code_pattern": "// Queen = rook moves + bishop moves combined"
    },
    "king": {
        "moves": ["1 square in any direction", "Cannot move into check"],
        "special": [
            "Castling kingside: king moves 2 right, rook jumps to left of king",
            "Castling queenside: king moves 2 left, rook jumps to right of king",
            "Cannot castle through check, while in check, or if pieces between",
        ],
        "code_pattern": """
function getKingMoves(board, row, col, color, castlingRights) {
    const moves = [];
    for (const [dr,dc] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]) {
        const r=row+dr, c=col+dc;
        if (inBounds(r,c) && !isAlly(board,r,c,color)) moves.push({r,c});
    }
    // Castling
    if (!isInCheck(board, row, col, color)) {
        if (castlingRights[color].kingSide && canCastle(board,row,col,'k',color))
            moves.push({r:row, c:col+2, special:'castle-k'});
        if (castlingRights[color].queenSide && canCastle(board,row,col,'q',color))
            moves.push({r:row, c:col-2, special:'castle-q'});
    }
    return moves;
}"""
    },
    "check_detection": {
        "rules": [
            "King is in check if any enemy piece can capture it",
            "Legal moves: only moves that don't leave king in check",
            "Checkmate: in check + no legal moves",
            "Stalemate: NOT in check + no legal moves",
        ],
        "code_pattern": """
function isInCheck(board, kingR, kingC, color) {
    // Find king position
    for (let r=0; r<8; r++) for (let c=0; c<8; c++)
        if (board[r][c]?.type==='K' && board[r][c]?.color===color) { kingR=r; kingC=c; }
    const enemy = color==='w'?'b':'w';
    // Check all enemy pieces
    for (let r=0; r<8; r++) for (let c=0; c<8; c++) {
        if (board[r][c]?.color===enemy) {
            const moves = getRawMoves(board,r,c);
            if (moves.some(m=>m.r===kingR&&m.c===kingC)) return true;
        }
    }
    return false;
}"""
    },
}

# ═══════════════════════════════════════════════════════════
#  LUDO RULES
# ═══════════════════════════════════════════════════════════
LUDO_RULES = {
    "board": {
        "size": "15x15 grid",
        "home_areas": {
            "red":    {"row": "0-5",  "col": "0-5"},
            "green":  {"row": "0-5",  "col": "9-14"},
            "yellow": {"row": "9-14", "col": "9-14"},
            "blue":   {"row": "9-14", "col": "0-5"},
        },
        "shared_path": "52 squares going clockwise",
        "home_columns": "6 squares per color leading to center",
        "safe_squares": [8, 13, 21, 26, 34, 39, 47, 0],  # positions on shared path
    },
    "tokens": {
        "count_per_player": 4,
        "start_position": -1,  # -1 = in yard
        "finish_position": 57,  # 0-51 shared + 52-57 home column
    },
    "dice": {
        "range": [1, 6],
        "rules": [
            "Roll 6 to bring token from yard to start position",
            "Roll 6 grants an extra turn",
            "Three consecutive 6s: turn skipped, first token goes back to yard",
        ],
    },
    "movement": {
        "rules": [
            "Move any token forward by dice value",
            "Cannot occupy own token's square (stack not allowed in standard)",
            "Landing on safe square: cannot be captured",
            "Exact count needed to enter home column",
            "Must have exact count to finish (enter center)",
        ],
        "code_pattern": """
// Ludo path coordinates (52 shared + 6 home per color)
function buildPath(color) {
    // Standard Ludo path: starts at color's entry point
    // Returns array of {row, col} for each of 58 positions (0-57)
    const sharedPath = getSharedPath(); // 52 positions clockwise
    const homePath = getHomePath(color); // 6 positions to center
    const colorOffset = {red:0, green:13, yellow:26, blue:39};
    const start = colorOffset[color];
    // Rotate shared path to start at color's entry
    const rotated = [...sharedPath.slice(start), ...sharedPath.slice(0,start)];
    return [...rotated, ...homePath];
}

function canCapture(pos, color) {
    const SAFE = [8,13,21,26,34,39,47];
    return pos >= 0 && pos < 52 && !SAFE.includes(pos);
}

function moveToken(gameState, playerColor, tokenIndex, diceValue) {
    const token = gameState.tokens[playerColor][tokenIndex];
    // From yard: need 6
    if (token.pos === -1) {
        if (diceValue === 6) { token.pos = 0; return {moved:true, capture:checkCapture(gameState,playerColor,0)}; }
        return {moved:false};
    }
    const newPos = token.pos + diceValue;
    if (newPos > 57) return {moved:false}; // Can't overshoot finish
    token.pos = newPos;
    return {moved:true, finished:newPos===57, capture:checkCapture(gameState,playerColor,newPos)};
}"""
    },
    "winning": {
        "condition": "First player to get all 4 tokens to position 57",
        "celebration": "Show winner overlay on canvas with color name",
    },
    "ai_strategy": {
        "priority_order": [
            "1. Move token that can finish (pos + dice = 57)",
            "2. Capture opponent token (land on same square, non-safe)",
            "3. Move token closest to finish",
            "4. Bring new token from yard if dice = 6",
            "5. Move furthest advanced token",
        ],
    },
}

# ═══════════════════════════════════════════════════════════
#  SOCIAL APP RULES (LinkedIn/Instagram)
# ═══════════════════════════════════════════════════════════
SOCIAL_APP_RULES = {
    "feed": {
        "rules": [
            "Posts sorted by timestamp descending",
            "Like button toggles: liked state changes icon+count",
            "Comment adds new item to comments array",
            "Share copies link to clipboard, shows toast notification",
            "Infinite scroll: load 5 more posts when bottom reached",
        ],
        "data_structure": """
const MOCK_FEED = [
    {id:1, author:"Ragul V", role:"Data Scientist", avatar:"R",
     content:"Built a multi-agent AI system today! 🚀", 
     likes:42, comments:8, shares:3, time:"2h", liked:false,
     media:null},
    // ... more posts
];"""
    },
    "profile": {
        "sections": ["Hero (avatar+name+title)", "About", "Experience", "Skills", "Education"],
        "interactions": ["Connect button (toggles)", "Message button", "Follow button"],
    },
    "notifications": {
        "types": ["like", "comment", "connection", "job", "mention"],
        "badge": "Red dot count on nav icon, clear on click",
    },
    "search": {
        "rules": [
            "Real-time filter as user types",
            "Search across: name, title, content, skills",
            "Highlight matching text in results",
            "Show 'No results' state",
        ],
    },
    "no_alert_rules": [
        "NEVER use alert() — show toast notification instead",
        "Toast: appear bottom-right, fade out after 3s",
        "Errors: show inline below input field",
        "Success: green toast notification",
        "Loading: spinner inside button, disable during request",
    ],
}

# ─────────────────────────────────────────────────────────────
# RULE REGISTRY — lookup rules by game/app type
# ─────────────────────────────────────────────────────────────
RULE_REGISTRY = {
    "chess":     CHESS_RULES,
    "ludo":      LUDO_RULES,
    "linkedin":  SOCIAL_APP_RULES,
    "instagram": SOCIAL_APP_RULES,
    "social":    SOCIAL_APP_RULES,
}

def get_rules(idea: str) -> dict:
    """Get relevant rules for given idea"""
    u = idea.lower()
    for key, rules in RULE_REGISTRY.items():
        if key in u:
            return {"type": key, "rules": rules}
    return {"type": "generic", "rules": {}}

def get_code_patterns(idea: str) -> str:
    """Extract code patterns for use in prompts"""
    u = idea.lower()
    patterns = []

    if "chess" in u:
        for piece, data in CHESS_RULES.items():
            if isinstance(data, dict) and "code_pattern" in data:
                patterns.append(data["code_pattern"])

    if "ludo" in u:
        patterns.append(LUDO_RULES["movement"]["code_pattern"])

    return "\n".join(patterns[:3])  # Limit to save tokens
