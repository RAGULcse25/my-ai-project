# core/smart_key_manager.py
# ============================================================
# SMART MULTI-PROVIDER KEY MANAGER
# Priority: Groq (free) -> Cerebras (free) -> Together (free)
#           -> Gemini (free) -> OpenRouter (paid $3 backup)
# Auto-switches provider when tokens run out
# Fixed: Windows cp1252 UnicodeEncodeError (emoji removed from print)
# ============================================================

import os, time, json, threading
from collections import defaultdict
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# -- Daily token limits (free tiers) -------------------------
PROVIDER_LIMITS = {
    "groq": {
        "tpd": 500_000,        # tokens per day per key (x6 keys = 3M/day)
        "tpm": 6_000,
        "rpm": 30,
        "cost": 0,
        "models": {
            "fast":   "llama-3.1-8b-instant",        # Fastest, lightest
            "smart":  "llama-3.3-70b-versatile",     # Best reasoning on Groq
            "search": "llama-3.3-70b-versatile",     # Research + reasoning
            "code":   "llama-3.3-70b-versatile",     # Strong coder
            "verify": "llama-3.3-70b-versatile",     # Deep audit/review
        }
    },
    "cerebras": {
        "tpd": 1_000_000,      # 1M tokens/day per key (x2 keys = 2M/day)
        "tpm": 60_000,
        "rpm": 30,
        "cost": 0,
        "models": {
            "fast":   "llama-3.3-70b",   # 900 tok/s — blazing fast
            "smart":  "llama-3.3-70b",
            "search": "llama-3.3-70b",
            "code":   "llama-3.3-70b",   # Primary code workhorse
            "verify": "llama-3.3-70b",
        }
    },
    "together": {
        "tpd": 1_000_000,
        "tpm": 60_000,
        "rpm": 60,
        "cost": 0,
        "models": {
            "fast":   "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "smart":  "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "search": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "code":   "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "verify": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        }
    },
    "gemini": {
        "tpd": 1_000_000,
        "tpm": 32_000,
        "rpm": 60,
        "cost": 0,
        "models": {
            "fast":   "gemini-2.0-flash",
            "smart":  "gemini-2.0-flash",   # Flash is generous + fast
            "search": "gemini-2.0-flash",
            "code":   "gemini-2.0-flash",
            "verify": "gemini-2.0-flash",
        }
    },
    "openrouter": {
        "tpd": 999_999_999,    # Paid -- use as last resort
        "tpm": 999_999,
        "rpm": 200,
        "cost": 0.14,
        "models": {
            "fast":   "deepseek/deepseek-chat",
            "smart":  "deepseek/deepseek-r1",
            "search": "deepseek/deepseek-r1",
            "code":   "deepseek/deepseek-coder",
            "verify": "anthropic/claude-3.5-sonnet",
        }
    },
}

USAGE_FILE = ".token_usage.json"

def safe_print(msg: str):
    """Print with Windows cp1252 safe fallback."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))

class SmartKeyManager:
    def __init__(self):
        self.lock      = threading.Lock()
        self.usage     = self._load_usage()
        self.cooldowns = {}

        # Load all keys from .env
        self.keys = {
            "groq":       self._load_keys("GROQ_KEY_"),
            "cerebras":   self._load_keys("CEREBRAS_KEY_"),
            "together":   self._load_keys("TOGETHER_KEY_"),
            "gemini":     self._load_keys("GEMINI_KEY_"),
            "openrouter": self._load_keys("OPENROUTER_KEY_"),
        }

        # Round-robin index per provider
        self._idx = defaultdict(int)

        self._print_status()

    def _load_keys(self, prefix: str) -> list:
        """Load all numbered keys (KEY_1, KEY_2 ...) plus the bare API_KEY env var."""
        keys = []
        # Numbered keys first: GROQ_KEY_1, GROQ_KEY_2, ...
        i = 1
        while True:
            k = os.getenv(f"{prefix}{i}")
            if not k:
                break
            keys.append(k)
            i += 1

        # Also load bare env var (e.g. GROQ_API_KEY, GEMINI_API_KEY)
        # even if numbered keys exist — it's likely a different/extra key
        bare_name = prefix.rstrip("_").replace("_KEY", "_API_KEY")
        bare_k = os.getenv(bare_name)
        if bare_k and bare_k not in keys:
            keys.append(bare_k)

        return keys

    def _load_usage(self) -> dict:
        today = str(date.today())
        if os.path.exists(USAGE_FILE):
            try:
                with open(USAGE_FILE) as f:
                    data = json.load(f)
                if data.get("date") != today:
                    return self._fresh_usage(today)
                return data
            except Exception:
                pass
        return self._fresh_usage(today)

    def _fresh_usage(self, today: str) -> dict:
        return {
            "date": today,
            "providers": {p: {"tokens": 0, "requests": 0, "cost": 0.0}
                          for p in PROVIDER_LIMITS},
            "total_tokens": 0,
            "total_cost":   0.0,
        }

    def _save_usage(self):
        try:
            with open(USAGE_FILE, "w") as f:
                json.dump(self.usage, f, indent=2)
        except Exception:
            pass

    def _print_status(self):
        safe_print("\n[KEY MANAGER] SmartKeyManager initialized:")
        for provider, keys in self.keys.items():
            if keys:
                limit = PROVIDER_LIMITS[provider]
                used  = self.usage["providers"][provider]["tokens"]
                total = limit["tpd"] * len(keys)
                pct   = int(used / max(total, 1) * 100)
                cost  = limit["cost"]
                safe_print(f"   {provider:12} {len(keys)} key(s) | "
                      f"{used:,}/{total:,} tokens ({pct}%) | "
                      f"{'FREE' if cost == 0 else f'${cost}/1M'}")

    def get_provider_status(self) -> dict:
        """Get real-time status of all providers"""
        status = {}
        for provider, keys in self.keys.items():
            if not keys:
                continue
            limit     = PROVIDER_LIMITS[provider]
            used      = self.usage["providers"][provider]["tokens"]
            total     = limit["tpd"] * len(keys)
            remaining = total - used
            status[provider] = {
                "keys":      len(keys),
                "used":      used,
                "total":     total,
                "remaining": remaining,
                "pct_used":  int(used / max(total, 1) * 100),
                "available": remaining > 1000,
                "cost":      limit["cost"],
            }
        return status

    def get_best_key(self, task_type: str = "smart",
                     max_tokens: int = 5000) -> tuple:
        """
        Returns (provider, api_key, model_name)
        Priority: free providers first, paid last
        Skips providers that are near daily limit or in cooldown
        """
        # v14 routing: Cerebras first for code (900 tok/s!), Groq for reasoning
        # Only include providers that actually have keys configured.
        def has(p): return bool(self.keys.get(p))

        if task_type == "code":
            # OpenRouter (DeepSeek Coder) prioritized as requested
            order = ["openrouter", "cerebras", "groq", "together", "gemini"]
        elif task_type == "fast":
            # Fastest first — Cerebras wins here
            order = ["cerebras", "groq", "together", "gemini", "openrouter"]
        elif task_type == "search":
            # Groq DeepSeek-R1 great for research, Gemini for broad context
            order = ["groq", "gemini", "openrouter", "cerebras", "together"]
        elif task_type == "verify":
            # More capable models preferred for quality checks
            order = ["groq", "openrouter", "cerebras", "together", "gemini"]
        elif task_type == "smart":
            # Planning/architecture: Groq DeepSeek-R1 best for reasoning
            order = ["groq", "cerebras", "gemini", "together", "openrouter"]
        else:
            # Default: free first, paid last
            order = ["groq", "cerebras", "together", "gemini", "openrouter"]

        priority = [p for p in order if has(p)]

        if not priority:
            raise Exception(
                "No API keys configured! Check .env file — "
                "add GROQ_KEY_1, CEREBRAS_KEY_1, GEMINI_KEY_1, or OPENROUTER_KEY_1."
            )

        with self.lock:
            now = time.time()
            for provider in priority:
                keys = self.keys.get(provider, [])
                if not keys:
                    continue

                limit  = PROVIDER_LIMITS[provider]
                used   = self.usage["providers"][provider]["tokens"]
                total  = limit["tpd"] * len(keys)
                buffer = max_tokens * 2  # keep 2x buffer

                # Skip if near daily limit
                if used + buffer > total:
                    pct = int(used / max(total, 1) * 100)
                    safe_print(f"  [WARN] {provider} at {pct}% daily -- skipping")
                    continue

                # Round-robin through keys, skip cooldown ones
                tried = 0
                while tried < len(keys):
                    idx = self._idx[provider] % len(keys)
                    self._idx[provider] = (idx + 1) % len(keys)
                    key = keys[idx]

                    # Check per-key cooldown
                    cd_key = f"{provider}:{key}"
                    if cd_key in self.cooldowns and now < self.cooldowns[cd_key]:
                        tried += 1
                        continue  # Skip cooled-down key

                    model = limit["models"].get(task_type, limit["models"]["smart"])
                    return provider, key, model

            # Fallback to OpenRouter only
            safe_print("[ALERT] OpenRouter cooldown -- retrying OpenRouter fallback...")
            fallback_order = ["openrouter"]
            for provider in fallback_order:
                keys = self.keys.get(provider, [])
                if not keys:
                    continue
                # Skip if ALL keys have long cooldowns (3600s = permanently broken)
                short_cd_keys = []
                for key in keys:
                    cd_key = f"{provider}:{key}"
                    remaining = self.cooldowns.get(cd_key, 0) - now
                    if remaining < 120:  # Only use if cooldown < 2min (rate-limit) vs 1h (broken)
                        short_cd_keys.append(key)
                if short_cd_keys:
                    key = short_cd_keys[0]
                    model = PROVIDER_LIMITS[provider]["models"].get(task_type, PROVIDER_LIMITS[provider]["models"]["smart"])
                    safe_print(f"  [FORCE] Using {provider} (short cooldown)")
                    return provider, key, model

            # True last resort -- if everything is cooled down, only force if it's a short cooldown
            for provider in fallback_order:
                keys = self.keys.get(provider, [])
                if keys:
                    key = keys[0]
                    cd_key = f"{provider}:{key}"
                    remaining = self.cooldowns.get(cd_key, 0) - now
                    if remaining > 3000: # If it's a hard error (3600s), fail fast instead of forcing
                        raise Exception(f"All keys for {provider} are strictly rate-limited / erroring. (Cooldown remaining: {int(remaining)}s)")
                    
                    model = PROVIDER_LIMITS[provider]["models"].get(task_type, PROVIDER_LIMITS[provider]["models"]["smart"])
                    safe_print(f"  [LAST-RESORT] Using {provider}")
                    return provider, key, model

        raise Exception("No API keys available across any provider!")

    def record_usage(self, provider: str, tokens: int):
        """Track tokens used per provider"""
        with self.lock:
            self.usage["providers"][provider]["tokens"]   += tokens
            self.usage["providers"][provider]["requests"] += 1
            self.usage["total_tokens"]                    += tokens

            cost_per_token = PROVIDER_LIMITS[provider]["cost"] / 1_000_000
            cost = tokens * cost_per_token
            self.usage["providers"][provider]["cost"] += cost
            self.usage["total_cost"]                  += cost

            self._save_usage()

            # Warn at 80%+
            limit = PROVIDER_LIMITS[provider]
            total = limit["tpd"] * max(len(self.keys.get(provider, [])), 1)
            used  = self.usage["providers"][provider]["tokens"]
            pct   = int(used / max(total, 1) * 100)
            if pct >= 80:
                safe_print(f"  [WARN] {provider} at {pct}% daily limit!")

    def mark_rate_limited(self, provider: str, key: str, seconds: int = 65):
        cd_key = f"{provider}:{key}"
        self.cooldowns[cd_key] = time.time() + seconds
        safe_print(f"  [RATE] {provider} key ...{key[-6:]} rate-limited -- cooling {seconds}s")

    def _send_alert(self):
        safe_print("\n" + "="*55)
        safe_print("[ALERT] TOKEN LIMIT -- ALL FREE PROVIDERS NEAR LIMIT")
        safe_print("="*55)
        status = self.get_provider_status()
        for p, s in status.items():
            bar_filled = int(s["pct_used"] / 5)
            bar = "#" * bar_filled + "-" * (20 - bar_filled)
            safe_print(f"  {p:12} [{bar}] {s['pct_used']}%")
        safe_print("\n[TIP] Solutions:")
        safe_print("   1. Add more GROQ_KEY_ entries to .env")
        safe_print("   2. Add CEREBRAS_KEY_ entries (1M tokens/day FREE)")
        safe_print("   3. Add GEMINI_KEY_ entries (free tier)")
        safe_print("   4. Wait for midnight reset (daily limits reset)")
        safe_print("="*55 + "\n")

    def get_daily_report(self) -> str:
        u = self.usage
        lines = [
            f"[REPORT] Daily Token Report -- {u['date']}",
            f"{'-'*42}",
            f"Total tokens : {u['total_tokens']:,}",
            f"Total cost   : ${u['total_cost']:.4f}",
            f"{'-'*42}",
        ]
        for p, data in u["providers"].items():
            if data["tokens"] > 0:
                lines.append(
                    f"{p:12} {data['tokens']:>8,} tokens | "
                    f"{data['requests']:>4} reqs | "
                    f"${data['cost']:.4f}"
                )
        return "\n".join(lines)


# Global singleton -- one instance for whole app
smart_key_manager = SmartKeyManager()
