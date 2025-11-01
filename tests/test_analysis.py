import pytest
from specdrift.analysis.ast_analyzer import get_ast_metrics
from specdrift.analysis.diff_analyzer import analyze_diff
import os

def test_ast_analyzer_missing_file():
    metrics = get_ast_metrics("nonexistent.py")
    assert metrics == {}

def test_ast_analyzer_valid(tmp_path):
    p = tmp_path / "hello.py"
    p.write_text("import sys\n\ndef hello():\n    pass\n\nclass World:\n    pass")
    metrics = get_ast_metrics(str(p))
    assert "sys" in metrics["imports"]
    assert "hello" in metrics["functions"]
    assert "World" in metrics["classes"]
    assert metrics["lines"] == 7

def test_diff_analyzer_basic(tmp_path):
    d1 = tmp_path / "d1"
    d2 = tmp_path / "d2"
    d1.mkdir()
    d2.mkdir()
    
    (d1 / "f1.txt").write_text("Hello\nWorld")
    (d2 / "f1.txt").write_text("Hello\nUniverse\n!")
    
    res = analyze_diff(str(d1), str(d2))
    assert res["files_changed"] == 1
    assert res["lines_added"] > 0
    assert res["lines_removed"] > 0
