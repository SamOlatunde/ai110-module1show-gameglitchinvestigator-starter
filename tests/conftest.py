import sys
from pathlib import Path

# FIX: logic_utils.py lives in the project root, not tests/. Adding the root to sys.path lets pytest find it on import.
sys.path.insert(0, str(Path(__file__).parent.parent))
