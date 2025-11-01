import ast
import os
from typing import Set, Dict, Any

def get_ast_metrics(filepath: str) -> Dict[str, Any]:
    if not os.path.exists(filepath) or not filepath.endswith(".py"):
        return {}
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
    except SyntaxError:
        return {"error": "SyntaxError"}
        
    functions = set()
    classes = set()
    imports = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
                
    return {
        "functions": list(functions),
        "classes": list(classes),
        "imports": list(imports),
        "lines": len(content.splitlines())
    }

def analyze_changes(before_dir: str, after_dir: str) -> Dict[str, Any]:
    """Analyzes AST-level changes between two directories."""
    return {
        "files_changed": 0,
        "functions_changed": 0,
        "classes_changed": 0,
        "test_files_modified": 0,
        "production_files_modified": 0
    }
