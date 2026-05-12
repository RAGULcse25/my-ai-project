import sys
import os
sys.path.append('e:/seads/backend')
from core.llm_config import get_llm_response

try:
    print("Testing get_llm_response with 8000 cap...")
    res = get_llm_response("Generate a simple HTML tag", max_tokens=25000, task_type="fast")
    print(f"Success! Length: {len(res)}")
except Exception as e:
    print(f"Failed: {e}")
