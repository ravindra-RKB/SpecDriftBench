import difflib
import os
from typing import Dict, Any

def analyze_diff(before_dir: str, after_dir: str) -> Dict[str, Any]:
    """Provides a generic unified-diff fallback analysis."""
    lines_added = 0
    lines_removed = 0
    files_changed = 0
    
    # Simple recursive directory walk
    for root, _, files in os.walk(after_dir):
        for file in files:
            after_path = os.path.join(root, file)
            rel_path = os.path.relpath(after_path, after_dir)
            before_path = os.path.join(before_dir, rel_path)
            
            with open(after_path, "r", encoding="utf-8", errors="ignore") as f:
                after_lines = f.readlines()
                
            if os.path.exists(before_path):
                with open(before_path, "r", encoding="utf-8", errors="ignore") as f:
                    before_lines = f.readlines()
            else:
                before_lines = []
                
            diff = list(difflib.unified_diff(before_lines, after_lines))
            if diff:
                files_changed += 1
                for line in diff:
                    if line.startswith('+') and not line.startswith('+++'):
                        lines_added += 1
                    elif line.startswith('-') and not line.startswith('---'):
                        lines_removed += 1
                        
    return {
        "files_changed": files_changed,
        "lines_added": lines_added,
        "lines_removed": lines_removed
    }
