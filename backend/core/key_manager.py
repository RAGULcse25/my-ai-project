import os
import time
import threading
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

# ─────────────────────────────────────────
# API KEY ROTATION MANAGER
# Distributes requests across all keys
# Auto-switches on rate limit
# ─────────────────────────────────────────

class KeyManager:
    def __init__(self):
        
        # Load all keys from .env
        self.groq_keys = self._load_keys("GROQ_KEY_")
        self.openrouter_keys = self._load_keys("OPENROUTER_KEY_")
        
        # Track usage per key
        self.usage_count  = defaultdict(int)
        self.error_count  = defaultdict(int)
        self.last_used    = defaultdict(float)
        self.cooldown     = {}  # key → cooldown_until timestamp
        
        # Thread lock for concurrent requests
        self.lock = threading.Lock()
        
        # Current index for round-robin
        self._groq_idx = 0
        self._or_idx   = 0
        
        print(f"KeyManager initialized:")
        print(f"   Groq keys      : {len(self.groq_keys)}")
        print(f"   OpenRouter keys: {len(self.openrouter_keys)}")
    
    
    def _load_keys(self, prefix: str) -> list:
        """Load all keys with given prefix from .env"""
        keys = []
        # Also check for the single key version (legacy)
        single_key = os.getenv(prefix.rstrip("_"))
        if single_key:
            keys.append(single_key)
            
        i = 1
        while True:
            key = os.getenv(f"{prefix}{i}")
            if not key:
                break
            if key not in keys:
                keys.append(key)
            i += 1
        return keys
    
    
    def get_groq_key(self) -> str:
        """
        Get next available Groq key
        Uses Round Robin + skips cooldown keys
        """
        with self.lock:
            return self._get_next_key(
                self.groq_keys, "_groq_idx"
            )
    
    
    def get_openrouter_key(self) -> str:
        """Get next available OpenRouter key"""
        with self.lock:
            return self._get_next_key(
                self.openrouter_keys, "_or_idx"
            )
    
    
    def _get_next_key(self, keys: list, idx_attr: str) -> str:
        """Round-robin key selection with cooldown skip"""
        
        if not keys:
            return ""
        
        now = time.time()
        attempts = 0
        
        while attempts < len(keys):
            idx = getattr(self, idx_attr)
            key = keys[idx % len(keys)]
            
            # Move to next for next call
            setattr(self, idx_attr, (idx + 1) % len(keys))
            
            # Skip if in cooldown
            if key in self.cooldown:
                if now < self.cooldown[key]:
                    attempts += 1
                    continue
                else:
                    # Cooldown expired
                    del self.cooldown[key]
            
            # Skip if too many errors
            if self.error_count[key] >= 5:
                attempts += 1
                continue
            
            # Use this key!
            self.usage_count[key] += 1
            self.last_used[key] = now
            return key
        
        # All keys in cooldown → use least recently cooled
        print("⚠️  All keys in cooldown. Waiting 10s...")
        time.sleep(10)
        return keys[0]
    
    
    def mark_rate_limited(self, key: str, wait_seconds: int = 60):
        """Put key in cooldown after rate limit hit"""
        self.cooldown[key] = time.time() + wait_seconds
        print(f"  🔄 Key rotated (rate limited, cooldown {wait_seconds}s)")
    
    
    def mark_error(self, key: str):
        """Track errors per key"""
        self.error_count[key] += 1
    
    
    def mark_success(self, key: str):
        """Reset error count on success"""
        self.error_count[key] = 0
    
    
    def get_stats(self) -> dict:
        """Show usage stats for all keys"""
        stats = {}
        for i, key in enumerate(self.groq_keys):
            short = f"...{key[-6:]}" if len(key) > 6 else key
            stats[f"groq_key_{i+1} ({short})"] = {
                "calls"   : self.usage_count[key],
                "errors"  : self.error_count[key],
                "cooldown": key in self.cooldown
            }
        return stats


# Global singleton — one instance for whole app
key_manager = KeyManager()
