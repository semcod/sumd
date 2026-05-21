import pytest
from pathlib import Path
from sumd_logic_validator.engine import HybridPrologEngine, PythonPrologDB, PythonPrologEngine

@pytest.fixture
def engine():
    rules_path = Path(__file__).resolve().parent.parent / "logic" / "rules.pl"
    return HybridPrologEngine(rules_path)

def test_detects_architectural_inconsistencies(engine):
    # Query the database for any rule violations
    results = engine.query("invalid(Error)")
    print("\nDetected architectural issues:", results)
    
    # We assert that the validation engine successfully parsed the DB and detected the expected rules warnings
    assert len(results) > 0
    assert any("workflow_missing_steps" in str(r["Error"]) for r in results)

def test_project_structure_facts(engine):
    # Verify that metadata and files facts were successfully generated and loaded
    res = engine.query("project_metadata(Name, Version, Type)")
    assert len(res) == 1
    assert res[0]["Name"] == "sumd"
    assert res[0]["Type"] == "python"
    
    # Verify that python_function facts were generated
    funcs = engine.query("python_function('sumd/cli.py', 'main', _, _, _)")
    assert len(funcs) >= 1
