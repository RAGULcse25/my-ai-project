import subprocess
import os
import sys
from agents.fixer_agent import run_fixer
from core.logger import log_test_result, log_fix_attempt

# ─────────────────────────────────────────
# TESTER AGENT
# Input  : project folder path
# Output : all files pass syntax & run test
# ─────────────────────────────────────────

MAX_FIX_ATTEMPTS = 3  # Retry limit per file


def run_syntax_check(file_path: str) -> tuple[bool, str]:
    """
    Check Python syntax using py_compile
    Returns: (passed, error_message)
    """
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", file_path],
        capture_output=True,
        text=True,
        timeout=15
    )
    
    if result.returncode == 0:
        return True, ""
    else:
        return False, result.stderr


def run_quick_test(file_path: str) -> tuple[bool, str]:
    """
    Try running the file for 5 seconds
    Returns: (passed, error_message)
    """
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=8,          # 8 second timeout
            cwd=os.path.dirname(file_path)
        )
        
        # If no error output → pass
        if result.returncode == 0 or not result.stderr:
            return True, ""
        
        # Filter out harmless warnings
        errors = [
            line for line in result.stderr.split("\n")
            if "Error" in line or "Traceback" in line
        ]
        
        if not errors:
            return True, ""
            
        return False, result.stderr
        
    except subprocess.TimeoutExpired:
        # Timeout = probably waiting for input = OK for now
        return True, ""
    except Exception as e:
        return False, str(e)


def test_and_fix_file(file_path: str) -> bool:
    """
    Test one file → fix if broken → retry
    Returns True if file passes
    """
    
    filename = os.path.basename(file_path)
    
    # Skip non-Python files
    if not filename.endswith(".py"):
        print(f"  ⏭️  Skipping {filename} (not Python)")
        return True
    
    print(f"\n  🧪 Testing: {filename}")
    
    for attempt in range(1, MAX_FIX_ATTEMPTS + 1):
        
        # ── Step 1: Syntax Check ──────────────
        syntax_ok, syntax_error = run_syntax_check(file_path)
        
        if not syntax_ok:
            print(f"    ❌ Syntax Error (attempt {attempt}/{MAX_FIX_ATTEMPTS})")
            print(f"    📋 Error: {syntax_error[:200]}")
            
            log_test_result(filename, False, syntax_error)
            
            # Fix it
            with open(file_path, "r", encoding="utf-8") as f:
                broken_code = f.read()
            
            fixed_code = run_fixer(filename, broken_code, syntax_error)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code)
            
            log_fix_attempt(filename, attempt, True)
            continue  # Retry
        
        # ── Step 2: Run Test ──────────────────
        run_ok, run_error = run_quick_test(file_path)
        
        if not run_ok:
            print(f"    ❌ Runtime Error (attempt {attempt}/{MAX_FIX_ATTEMPTS})")
            print(f"    📋 Error: {run_error[:200]}")
            
            log_test_result(filename, False, run_error)
            
            # Fix it
            with open(file_path, "r", encoding="utf-8") as f:
                broken_code = f.read()
            
            fixed_code = run_fixer(filename, broken_code, run_error)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(fixed_code)
            
            log_fix_attempt(filename, attempt, True)
            continue  # Retry
        
        # ── All Passed ────────────────────────
        print(f"    ✅ {filename} passed!")
        log_test_result(filename, True)
        return True
    
    # All attempts exhausted
    print(f"    ⚠️  {filename} — max attempts reached. Manual review needed.")
    return False


def run_tester(folder_path: str) -> dict:
    """
    Main tester function
    Tests all .py files in the project folder
    Returns summary report
    """
    
    print(f"\n🧪 TESTER AGENT: Starting tests...")
    print(f"📂 Folder: {folder_path}\n")
    
    all_files = os.listdir(folder_path)
    py_files = [f for f in all_files if f.endswith(".py")]
    
    print(f"📋 Python files found: {py_files}")
    
    results = {
        "passed": [],
        "failed": [],
        "skipped": []
    }
    
    for filename in all_files:
        file_path = os.path.join(folder_path, filename)
        
        if filename.endswith(".py"):
            passed = test_and_fix_file(file_path)
            if passed:
                results["passed"].append(filename)
            else:
                results["failed"].append(filename)
        else:
            results["skipped"].append(filename)
    
    # ── Print Summary ─────────────────────────
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"  ✅ Passed  : {len(results['passed'])} → {results['passed']}")
    print(f"  ❌ Failed  : {len(results['failed'])} → {results['failed']}")
    print(f"  ⏭️  Skipped : {len(results['skipped'])} → {results['skipped']}")
    
    total = len(results["passed"]) + len(results["failed"])
    if total > 0:
        score = (len(results["passed"]) / total) * 100
        print(f"\n  🎯 Score   : {score:.0f}%")
    
    return results
