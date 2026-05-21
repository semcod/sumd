import pytest
from pathlib import Path
from textwrap import dedent
from sumd.prolog_engine import PythonPrologDB, PythonPrologEngine
from sumd.validator import validate_project_architecture, validate_sumd_file


def test_pure_python_prolog_basic():
    """Test the zero-dependency pure-Python Prolog SLD engine on basic facts."""
    db = PythonPrologDB()
    db.parse_and_load(dedent("""
        project_file('src/main.py', 100, 'python').
        project_file('src/utils.py', 50, 'python').
        
        has_large_file(F) :- project_file(F, L, _), L \\= 50.
    """))
    
    engine = PythonPrologEngine(db)
    
    # Query facts
    res = engine.query("project_file(F, 100, 'python')")
    assert len(res) == 1
    assert res[0]["F"] == "src/main.py"
    
    # Query rules with inequality
    res_rule = engine.query("has_large_file(File)")
    assert len(res_rule) == 1
    assert res_rule[0]["File"] == "src/main.py"


def test_architectural_validation_missing_file(tmp_path):
    """Test Layer 3 consistency: declared file is missing from filesystem."""
    proj_dir = tmp_path
    
    # 1. Create a minimal SUMD.md with a markpact block declaring missing.py
    sumd_content = dedent("""\
        # test_project - Minimal Test
        
        ## Metadata
        - **name**: test_project
        - **version**: 1.0.0
        
        ## Architecture
        ```python markpact:file path=missing.py
        print("This file does not exist")
        ```
    """)
    (proj_dir / "SUMD.md").write_text(sumd_content, encoding="utf-8")
    (proj_dir / "Makefile").write_text("", encoding="utf-8")
    
    # Run validation (missing.py does not exist in workspace, so it should report an error)
    errors = validate_project_architecture(proj_dir)
    
    assert len(errors) > 0
    assert any("declared_file_missing" in err and "missing.py" in err for err in errors)


def test_architectural_validation_aligned(tmp_path):
    """Test that an entirely consistent project reports no errors."""
    proj_dir = tmp_path
    
    # 1. Create app.doql.less declaring a workflow and matching task/makefile
    doql_content = dedent("""\
        app {
          name: test;
          version: 1.0.0;
        }
        workflow[name="build"] {
          trigger: manual;
          step-1: run cmd=echo build;
        }
    """)
    (proj_dir / "app.doql.less").write_text(doql_content, encoding="utf-8")
    
    # 2. Create matching SUMD.md
    sumd_content = dedent("""\
        # test - Minimal Aligned Test
        
        ## Metadata
        - **name**: test
        - **version**: 1.0.0
        
        ## Architecture
        ```less markpact:doql path=app.doql.less
        // content
        ```
    """)
    (proj_dir / "SUMD.md").write_text(sumd_content, encoding="utf-8")
    
    # 3. Create Makefile or Taskfile to satisfy "workflow_missing_automation"
    makefile_content = dedent("""\
        build:
        \techo building
    """)
    (proj_dir / "Makefile").write_text(makefile_content, encoding="utf-8")
    
    # Run validation - should be fully consistent!
    errors = validate_project_architecture(proj_dir)
    assert errors == []


def test_architectural_validation_missing_automation(tmp_path):
    """Test Layer 3: workflow exists but Makefile / Taskfile has no matching automation."""
    proj_dir = tmp_path
    
    # Declare a workflow "deploy" but don't provide Makefile target or Taskfile task
    doql_content = dedent("""\
        app { name: test; }
        workflow[name="deploy"] {
          trigger: manual;
          step-1: run cmd=echo deploy;
        }
    """)
    (proj_dir / "app.doql.less").write_text(doql_content, encoding="utf-8")
    
    sumd_content = dedent("""\
        # test - Missing Automation
        
        ## Metadata
        - **name**: test
        - **version**: 1.0.0
        
        ## Architecture
        ```less markpact:doql path=app.doql.less
        ```
    """)
    (proj_dir / "SUMD.md").write_text(sumd_content, encoding="utf-8")
    
    errors = validate_project_architecture(proj_dir)
    assert len(errors) > 0
    assert any("workflow_missing_automation" in err and "deploy" in err for err in errors)


def test_architectural_validation_missing_gate(tmp_path):
    """Test Layer 2: quality workflow exists but no matching pyqual gate is declared."""
    proj_dir = tmp_path
    
    doql_content = dedent("""\
        app { name: test; }
        workflow[name="quality:regix"] {
          trigger: manual;
          step-1: run cmd=echo pyqual;
        }
    """)
    (proj_dir / "app.doql.less").write_text(doql_content, encoding="utf-8")
    
    sumd_content = dedent("""\
        # test - Missing Gate
        
        ## Metadata
        - **name**: test
        - **version**: 1.0.0
        
        ## Architecture
        ```less markpact:doql path=app.doql.less
        ```
    """)
    (proj_dir / "SUMD.md").write_text(sumd_content, encoding="utf-8")
    
    # We also provide a Makefile target so we don't trigger "workflow_missing_automation"
    (proj_dir / "Makefile").write_text("quality:regix:\n\techo running\n", encoding="utf-8")
    
    # Run validation - since pyqual.yaml is missing, the regix gate is missing!
    errors = validate_project_architecture(proj_dir)
    assert len(errors) > 0
    assert any("missing_gate_for_quality_workflow" in err and "regix" in err for err in errors)
