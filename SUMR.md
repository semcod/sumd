# SUMD

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Quality Pipeline (`pyqual.yaml`)](#quality-pipeline-pyqualyaml)
- [Dependencies](#dependencies)
- [Source Map](#source-map)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `sumd`
- **version**: `0.3.47`
- **python_requires**: `>=3.10`
- **license**: {'text': 'Apache-2.0'}
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Taskfile.yml, Makefile, testql(3), app.doql.less, pyqual.yaml, goal.yaml, .env.example, src(11 mod), project/(6 analysis files), .swop/manifests/core/commands.yml, .swop/manifests/core/queries.yml, .swop/manifests/core/events.yml

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: sumd;
  version: 0.3.47;
}

dependencies {
  runtime: "click>=8.3.3, pyyaml>=6.0.3, toml>=0.10.2, goal>=2.1.190, costs>=0.1.50, pfix>=0.1.72, mcp>=1.27.0";
  dev: "pytest>=9.0.3, pytest-asyncio>=0.21.0, pytest-cov>=7.1.0, ruff>=0.15.11, build>=1.4.4, twine>=6.2.0, pyqual>=0.1.143, goal>=2.1.190, costs>=0.1.50, pfix>=0.1.72, mcp>=1.27.0";
}

interface[type="cli"] {
  framework: click;
}
interface[type="cli"] page[name="sumd"] {

}

workflow[name="install"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Installing sumd...";
  step-2: run cmd=if command -v uv > /dev/null 2>&1; then \;
  step-3: run cmd=uv pip install -e .; \;
  step-4: run cmd=else \;
  step-5: run cmd=pip install -e .; \;
  step-6: run cmd=fi;
  step-7: run cmd=echo "✅ Installation completed!";
}

workflow[name="install-dev"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Installing sumd with dev dependencies...";
  step-2: run cmd=if command -v uv > /dev/null 2>&1; then \;
  step-3: run cmd=uv pip install -e ".[dev]"; \;
  step-4: run cmd=else \;
  step-5: run cmd=pip install -e ".[dev]"; \;
  step-6: run cmd=fi;
  step-7: run cmd=echo "✅ Dev installation completed!";
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 Running tests...";
  step-2: run cmd=.venv/bin/python -m pytest tests/ -v --tb=short;
}

workflow[name="test-cov"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 Running tests with coverage...";
  step-2: run cmd=.venv/bin/python -m pytest tests/ -v --cov=sumd --cov-report=term-missing --cov-report=json;
}

workflow[name="lint"] {
  trigger: manual;
  step-1: run cmd=echo "🔍 Running linting with ruff...";
  step-2: run cmd=.venv/bin/python -m ruff check sumd/;
  step-3: run cmd=.venv/bin/python -m ruff check tests/;
}

workflow[name="format"] {
  trigger: manual;
  step-1: run cmd=echo "📝 Formatting code with ruff...";
  step-2: run cmd=.venv/bin/python -m ruff format sumd/;
  step-3: run cmd=.venv/bin/python -m ruff format tests/;
}

workflow[name="clean"] {
  trigger: manual;
  step-1: run cmd=echo "🧹 Cleaning temporary files...";
  step-2: run cmd=find . -type f -name "*.pyc" -delete;
  step-3: run cmd=find . -type d -name "__pycache__" -delete;
  step-4: run cmd=find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true;
  step-5: run cmd=rm -rf build/ dist/ .coverage htmlcov/ coverage.json;
  step-6: run cmd=echo "✅ Clean completed!";
}

workflow[name="publish"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Publishing to PyPI...";
  step-2: run cmd=command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build);
  step-3: run cmd=rm -rf dist/ build/ *.egg-info/;
  step-4: run cmd=.venv/bin/python -m build;
  step-5: run cmd=.venv/bin/twine check dist/*;
  step-6: run cmd=echo "⚡ Ready to upload. Run: make publish-confirm to upload to PyPI";
}

workflow[name="publish-confirm"] {
  trigger: manual;
  step-1: run cmd=echo "🚀 Uploading to PyPI...";
  step-2: run cmd=.venv/bin/twine upload dist/*;
}

workflow[name="publish-test"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Publishing to TestPyPI...";
  step-2: run cmd=command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build);
  step-3: run cmd=rm -rf dist/ build/ *.egg-info/;
  step-4: run cmd=.venv/bin/python -m build;
  step-5: run cmd=.venv/bin/twine upload --repository testpypi dist/*;
}

workflow[name="version"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Version information...";
  step-2: run cmd=cat VERSION;
  step-3: run cmd=.venv/bin/python -c "from importlib.metadata import version; print(f'Installed version: {version(\"sumd\")}')";
}

workflow[name="deps:update"] {
  trigger: manual;
  step-1: run cmd=PIP="{{.VENV_PIP}}"
$PIP install --upgrade pip
OUTDATED=$($PIP list --outdated --format=columns 2>/dev/null | tail -n +3 | awk '{print $1}')
if [ -z "$OUTDATED" ]; then
  echo "✅ All packages are up to date."
else
  echo "📦 Upgrading: $OUTDATED"
  echo "$OUTDATED" | xargs $PIP install --upgrade
  echo "✅ Done."
fi;
}

workflow[name="quality"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m pyqual run;
}

workflow[name="quality:fix"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m pyqual run --fix;
}

workflow[name="quality:report"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m pyqual report;
}

workflow[name="test:report"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m pytest --json-report --json-report-file=test-results.json -q;
  step-2: run cmd={{.VENV_PY}} -m testql report test-results.json -o report.html;
}

workflow[name="test:report:example"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m testql report --example -o report.html;
}

workflow[name="fmt"] {
  trigger: manual;
  step-1: run cmd=ruff format .;
}

workflow[name="build"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m build;
}

workflow[name="structure"] {
  trigger: manual;
  step-1: run cmd=echo "📁 Analyzing sumd project structure..."
{{.DOQL_CMD}} adopt {{.PWD}} --output app.doql.less --force
echo "✅ Structure generated: {{.DOQL_OUTPUT}}";
}

workflow[name="doql:adopt"] {
  trigger: manual;
  step-1: run cmd={{.DOQL_CMD}} adopt {{.PWD}} --output app.doql.less --force;
  step-2: run cmd=echo "✅ Captured in app.doql.less";
}

workflow[name="doql:export"] {
  trigger: manual;
  step-1: run cmd=if [ ! -f "app.doql.less" ]; then
  echo "❌ app.doql.less not found. Run: task structure"
  exit 1
fi;
  step-2: run cmd={{.DOQL_CMD}} export --format less -o {{.DOQL_OUTPUT}};
  step-3: run cmd=echo "✅ Exported to {{.DOQL_OUTPUT}}";
}

workflow[name="doql:validate"] {
  trigger: manual;
  step-1: run cmd=if [ ! -f "{{.DOQL_OUTPUT}}" ]; then
  echo "❌ {{.DOQL_OUTPUT}} not found. Run: task structure"
  exit 1
fi;
  step-2: run cmd={{.DOQL_CMD}} validate;
}

workflow[name="doql:doctor"] {
  trigger: manual;
  step-1: run cmd={{.DOQL_CMD}} doctor;
}

workflow[name="doql:build"] {
  trigger: manual;
  step-1: run cmd=if [ ! -f "{{.DOQL_OUTPUT}}" ]; then
  echo "❌ {{.DOQL_OUTPUT}} not found. Run: task structure"
  exit 1
fi;
  step-2: run cmd={{.DOQL_CMD}} build app.doql.less --out build/;
}

workflow[name="docs:build"] {
  trigger: manual;
  step-1: run cmd=echo "Building SUMD documentation...";
  step-2: run cmd={{.VENV_PY}} -m sumd.cli docs/ docs/;
}

workflow[name="sumd"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m sumd.cli scan .;
}

workflow[name="sumr"] {
  trigger: manual;
  step-1: run cmd={{.VENV_PY}} -m sumd.cli scan . --profile refactor;
}

workflow[name="version:bump"] {
  trigger: manual;
  step-1: run cmd=hatch version patch;
  step-2: run cmd=echo "✅ Version bumped:";
  step-3: run cmd=hatch version;
}

workflow[name="doctor"] {
  trigger: manual;
  step-1: run cmd=echo "=== sumd doctor ==="
check() { "$@" > /dev/null 2>&1 && echo "  ✅ $1" || echo "  ❌ $1  (command failed: $*)"; }
check {{.VENV_PY}} -m pyqual doctor
check {{.VENV_PY}} -m pytest --version
check ruff --version
check {{.PWD}}/.venv/bin/sumd --version
check {{.PWD}}/.venv/bin/sumd --help
echo "=== done ===";
}

workflow[name="help"] {
  trigger: manual;
  step-1: run cmd=task --list;
}

workflow[name="analyze"] {
  trigger: manual;
  step-1: run cmd=echo "🔬 Running project analysis...";
  step-2: run cmd=sumd analyze . --tools code2llm,redup,vallm;
}

deploy {
  target: docker;
}

environment[name="local"] {
  runtime: docker-compose;
  env_file: .env;
  python_version: >=3.10;
}
```

### Source Modules

- `sumd.cli`
- `sumd.extractor`
- `sumd.generator`
- `sumd.mcp_server`
- `sumd.models`
- `sumd.parser`
- `sumd.pipeline`
- `sumd.prolog_engine`
- `sumd.renderer`
- `sumd.toon_parser`
- `sumd.validator`

### Architecture Consistency Rules (sumd/rules.pl)

```prolog markpact:file path=sumd/rules.pl
% ─────────────────────────────────────────────────────────────
% 🧠 SUMD ARCHITECTURAL CONSISTENCY RULES
% ─────────────────────────────────────────────────────────────

% ── Layer 1: Structural Consistency ─────────────────────────────

% A workflow must have a trigger
invalid(workflow_missing_trigger(W)) :-
    sumd_workflow(W, '').

% A workflow must have at least one step
invalid(workflow_missing_steps(W)) :-
    sumd_workflow(W, _),
    \+ sumd_workflow_step(W, _, _).


% ── Layer 2: Semantic Consistency ───────────────────────────────

% If deploy target is docker_compose, a compose file must be declared
invalid(deploy_missing_compose_file) :-
    sumd_deploy_target(docker_compose),
    \+ sumd_deploy_compose_file(_).

% If a quality:Gate workflow exists, the gate itself must be declared/expected
invalid(missing_gate_for_quality_workflow(W, Gate)) :-
    sumd_quality_workflow(W, Gate),
    \+ sumd_gate(Gate).


% ── Layer 3: Consistency between Artifacts ─────────────────────

% Any file declared in SUMD.md (via markpact annotations) must exist in the workspace
invalid(declared_file_missing(Path, Kind)) :-
    sumd_declared_file(Path, Kind),
    \+ project_file(Path, _, _).

% Any workflow declared in app.doql.less should have a matching automation task in Makefile or Taskfile
invalid(workflow_missing_automation(W)) :-
    sumd_workflow(W, _),
    \+ makefile_target(W, _),
    \+ taskfile_task(W, _).
```

## Workflows

### Taskfile Tasks (`Taskfile.yml`)

```yaml markpact:taskfile path=Taskfile.yml
# Taskfile.yml — sumd (Structured Unified Markdown Descriptor) project runner
# https://taskfile.dev

version: "3"

vars:
  APP_NAME: sumd
  DOQL_OUTPUT: app.doql.less
  DOQL_CMD: "{{if eq OS \"windows\"}}doql.exe{{else}}doql{{end}}"
  VENV_PY: "{{.PWD}}/.venv/bin/python"
  VENV_PIP: "{{.PWD}}/.venv/bin/pip"

env:
  PYTHONPATH: "{{.PWD}}"

tasks:
  # ─────────────────────────────────────────────────────────────────────────────
  # Development
  # ─────────────────────────────────────────────────────────────────────────────

  install:
    desc: Install Python dependencies (editable)
    cmds:
      - "{{.VENV_PIP}} install -e .[dev]"

  deps:update:
    desc: Upgrade all outdated Python packages in the project venv
    cmds:
      - |
        PIP="{{.VENV_PIP}}"
        $PIP install --upgrade pip
        OUTDATED=$($PIP list --outdated --format=columns 2>/dev/null | tail -n +3 | awk '{print $1}')
        if [ -z "$OUTDATED" ]; then
          echo "✅ All packages are up to date."
        else
          echo "📦 Upgrading: $OUTDATED"
          echo "$OUTDATED" | xargs $PIP install --upgrade
          echo "✅ Done."
        fi

  quality:
    desc: Run pyqual quality pipeline (uses pyqual.yaml from cwd)
    cmds:
      - "{{.VENV_PY}} -m pyqual run"

  quality:fix:
    desc: Run pyqual with auto-fix (uses pyqual.yaml from cwd)
    cmds:
      - "{{.VENV_PY}} -m pyqual run --fix"

  quality:report:
    desc: Generate pyqual quality report (uses pyqual.yaml from cwd)
    cmds:
      - "{{.VENV_PY}} -m pyqual report"

  test:
    desc: Run pytest suite
    cmds:
      - "{{.VENV_PY}} -m pytest -q"

  test:report:
    desc: Run pytest suite and generate HTML report
    cmds:
      - "{{.VENV_PY}} -m pytest --json-report --json-report-file=test-results.json -q"
      - "{{.VENV_PY}} -m testql report test-results.json -o report.html"

  test:report:example:
    desc: Generate example testql HTML report
    cmds:
      - "{{.VENV_PY}} -m testql report --example -o report.html"

  lint:
    desc: Run ruff lint check
    cmds:
      - ruff check .

  fmt:
    desc: Auto-format with ruff
    cmds:
      - ruff format .

  build:
    desc: Build wheel + sdist
    cmds:
      - "{{.VENV_PY}} -m build"

  clean:
    desc: Remove build artefacts
    cmds:
      - rm -rf build/ dist/ *.egg-info

  all:
    desc: Run install, quality check
    cmds:
      - task: install
      - task: quality

  # ─────────────────────────────────────────────────────────────────────────────
  # Doql Integration
  # ─────────────────────────────────────────────────────────────────────────────

  structure:
    desc: Generate project structure (app.doql.less)
    cmds:
      - |
        echo "📁 Analyzing sumd project structure..."
        {{.DOQL_CMD}} adopt {{.PWD}} --output app.doql.less --force
        echo "✅ Structure generated: {{.DOQL_OUTPUT}}"

  doql:adopt:
    desc: Reverse-engineer sumd project structure (LESS format)
    cmds:
      - "{{.DOQL_CMD}} adopt {{.PWD}} --output app.doql.less --force"
      - echo "✅ Captured in app.doql.less"

  doql:export:
    desc: Export app.doql.less to other formats
    cmds:
      - |
        if [ ! -f "app.doql.less" ]; then
          echo "❌ app.doql.less not found. Run: task structure"
          exit 1
        fi
      - "{{.DOQL_CMD}} export --format less -o {{.DOQL_OUTPUT}}"
      - echo "✅ Exported to {{.DOQL_OUTPUT}}"

  doql:validate:
    desc: Validate app.doql.less syntax
    cmds:
      - |
        if [ ! -f "{{.DOQL_OUTPUT}}" ]; then
          echo "❌ {{.DOQL_OUTPUT}} not found. Run: task structure"
          exit 1
        fi
      - "{{.DOQL_CMD}} validate"

  doql:doctor:
    desc: Run doql health checks
    cmds:
      - "{{.DOQL_CMD}} doctor"

  doql:build:
    desc: Generate code from app.doql.less
    cmds:
      - |
        if [ ! -f "{{.DOQL_OUTPUT}}" ]; then
          echo "❌ {{.DOQL_OUTPUT}} not found. Run: task structure"
          exit 1
        fi
      - "{{.DOQL_CMD}} build app.doql.less --out build/"

  analyze:
    desc: Full doql analysis (structure + validate + doctor)
    cmds:
      - task: structure
      - task: doql:validate
      - task: doql:doctor

  # ─────────────────────────────────────────────────────────────────────────────
  # Documentation
  # ─────────────────────────────────────────────────────────────────────────────

  docs:build:
    desc: Build documentation
    cmds:
      - echo "Building SUMD documentation..."
      - "{{.VENV_PY}} -m sumd.cli docs/ docs/"

  # ─────────────────────────────────────────────────────────────────────────────
  # SUMD Documentation Generation
  # ─────────────────────────────────────────────────────────────────────────────

  sumd:
    desc: Generate SUMD.md (full project documentation)
    cmds:
      - "{{.VENV_PY}} -m sumd.cli scan ."

  sumr:
    desc: Generate SUMR.md (pre-refactoring analysis report)
    cmds:
      - "{{.VENV_PY}} -m sumd.cli scan . --profile refactor"

  # ─────────────────────────────────────────────────────────────────────────────
  # Release
  # ─────────────────────────────────────────────────────────────────────────────

  version:bump:
    desc: Bump patch version (hatch)
    cmds:
      - hatch version patch
      - echo "✅ Version bumped:"
      - hatch version

  publish:
    desc: Build and publish to PyPI
    cmds:
      - task: clean
      - task: build
      - "{{.VENV_PY}} -m twine upload dist/*"

  # ─────────────────────────────────────────────────────────────────────────────
  # Utility
  # ─────────────────────────────────────────────────────────────────────────────

  check:
    desc: Full pre-commit check (lint + test + quality)
    cmds:
      - task: lint
      - task: test
      - task: quality

  doctor:
    desc: Smoke-test all external CLI tools used by this project
    cmds:
      - |
        echo "=== sumd doctor ==="
        check() { "$@" > /dev/null 2>&1 && echo "  ✅ $1" || echo "  ❌ $1  (command failed: $*)"; }
        check {{.VENV_PY}} -m pyqual doctor
        check {{.VENV_PY}} -m pytest --version
        check ruff --version
        check {{.PWD}}/.venv/bin/sumd --version
        check {{.PWD}}/.venv/bin/sumd --help
        echo "=== done ==="

  help:
    desc: Show available tasks
    cmds:
      - task --list

  all:
    desc: Install, full check, generate SUMD docs
    cmds:
      - task: install
      - task: check
      - task: sumd
```

## Quality Pipeline (`pyqual.yaml`)

```yaml markpact:pyqual path=pyqual.yaml
pipeline:
  name: quality-loop

  # Quickstart: replace all of this with a single profile line:
  #   profile: python-minimal   # analyze → validate → lint → fix → test
  #   profile: python-publish   # + git-push and make-publish
  #   profile: python-secure    # + pip-audit, bandit, detect-secrets
  #   profile: python           # standard (needs manual stage config)
  #   profile: ci               # CI-only, no fix
  # See: pyqual profiles

  # Quality gates — pipeline iterates until ALL pass
  metrics:
    cc_max: 15           # cyclomatic complexity per function
    vallm_pass_min: 60   # vallm validation pass rate (%)
    coverage_min: 35     # branch+statement coverage (%) — 37% measured with --cov-branch

  # Pipeline stages — use 'tool:' for built-in presets or 'run:' for custom commands
  # See all presets: pyqual tools
  # when: any_stage_fail    — run only when a prior stage in this iteration failed
  # when: metrics_fail      — run only when quality gates are not yet passing
  # when: first_iteration   — run only on iteration 1 (skip re-runs after fix)
  # when: after_fix         — run only after the fix stage ran in this iteration
  stages:
    - name: analyze
      tool: code2llm-filtered   # uses sensible exclude defaults

    - name: validate
      tool: vallm-filtered      # uses sensible exclude defaults

    - name: prefact
      tool: prefact
      optional: true
      when: any_stage_fail
      timeout: 900

    - name: fix
      tool: llx-fix
      optional: true
      when: any_stage_fail
      timeout: 1800

    - name: test
      tool: pytest

    - name: push
      tool: git-push            # built-in: git add + commit + push
      optional: true
      timeout: 120

    - name: publish
      tool: twine-publish       # built-in: python -m build + twine upload
      optional: true
      when: metrics_pass
      timeout: 120

  # Loop behavior
  loop:
    max_iterations: 3
    on_fail: report      # report | create_ticket | block
    ticket_backends:     # backends to sync when on_fail = create_ticket
      - markdown        # TODO.md (default)
      # - github        # GitHub Issues (requires GITHUB_TOKEN)

  # Environment (optional)
  env:
    LLM_MODEL: openrouter/qwen/qwen3-coder-next
```

## Dependencies

### Runtime

```text markpact:deps python
click>=8.3.3
pyyaml>=6.0.3
toml>=0.10.2
goal>=2.1.190
costs>=0.1.50
pfix>=0.1.72
mcp>=1.27.0
```

### Development

```text markpact:deps python scope=dev
pytest>=9.0.3
pytest-asyncio>=0.21.0
pytest-cov>=7.1.0
ruff>=0.15.11
build>=1.4.4
twine>=6.2.0
pyqual>=0.1.143
goal>=2.1.190
costs>=0.1.50
pfix>=0.1.72
mcp>=1.27.0
```

## Source Map

*Top 5 modules by symbol density — signatures for LLM orientation.*

### `sumd.cli` (`sumd/cli.py`)

```python
def _detect_project_type(proj_dir)  # CC=8, fan=4
def _render_doql_boilerplate(project_name, spec, extra_workflows)  # CC=4, fan=3
def _node_framework(deps)  # CC=5, fan=0
def _node_spec_from_package_json(pkg_json)  # CC=7, fan=5
def _build_doql_spec(proj_dir, project_type)  # CC=3, fan=4
def _generate_doql_less(proj_dir, project_name, version, force, project_type)  # CC=7, fan=8
def cli()  # CC=1, fan=2
def validate(file)  # CC=4, fan=8
def export(file, format, output)  # CC=8, fan=11
def info(file)  # CC=3, fan=7
def generate(file, format, output)  # CC=8, fan=15
def extract(file, section)  # CC=5, fan=8
def _is_project_dir(d)  # CC=8, fan=4
def _walk_projects(path, projects, max_depth, depth)  # CC=10, fan=7 ⚠
def _detect_projects(workspace, max_depth)  # CC=1, fan=1
def _ensure_venv(tools_dir, venv_dir, tool_list)  # CC=4, fan=4
def _tool_bin(bin_dir, name)  # CC=2, fan=1
def _run_one_tool(tool, bin_dir, proj_dir, project_output)  # CC=3, fan=5
def _run_analysis_tools(proj_dir, tool_list, skip_tools)  # CC=5, fan=5
def _export_sumd_json(proj_dir, doc)  # CC=2, fan=2
def _render_write_validate(proj_dir, sumd_path, raw, profile)  # CC=5, fan=5
def _echo_scan_result(proj_dir, doc, sources, cb_warnings)  # CC=2, fan=3
def _maybe_generate_doql(proj_dir, fix)  # CC=7, fan=6
def _maybe_generate_testql(proj_dir)  # CC=5, fan=5
def _finalize_scan(proj_dir, doc, sources, cb_warnings, export_json, run_analyze, tool_list, doql_sync, sumd_path)  # CC=9, fan=9
def _scan_one_project(proj_dir, fix, raw, export_json, run_analyze, tool_list, parser_inst, profile, generate_doql, doql_sync, generate_testql)  # CC=10, fan=9 ⚠
def scan(workspace, export_json, report, fix, raw, analyze, tools, profile, depth, recursive, generate_doql, doql_sync, generate_testql, workspace_mode)  # CC=14, fan=18 ⚠
def lint(files, workspace, as_json, strict)  # CC=12, fan=13 ⚠
def _lint_collect_paths(files, workspace)  # CC=6, fan=7
def _lint_print_result(path, r)  # CC=10, fan=3 ⚠
def _setup_tools_venv(venv_dir, tool_list, force)  # CC=7, fan=6
def _run_code2llm_formats(bin_dir, project, project_output)  # CC=5, fan=4
def _run_tool_subprocess(bin_dir, tool, cmd_args)  # CC=3, fan=4
def analyze(project, tools, force)  # CC=11, fan=17 ⚠
def _api_scenario_template(name, scenario_type, endpoints_block, base_path)  # CC=1, fan=3
def _scaffold_write(path, content, force, generated, skipped)  # CC=3, fan=3
def _scaffold_smoke_scenario(paths, base, out_dir, force, generated, skipped)  # CC=6, fan=5
def _scaffold_crud_scenarios(groups, base, out_dir, force, generated, skipped)  # CC=5, fan=7
def _scaffold_from_openapi(spec, out_dir, scenario_type, force, generated, skipped)  # CC=7, fan=12
def _scaffold_generic(out_dir, force, generated, skipped)  # CC=1, fan=3
def scaffold(project, output, force, scenario_type)  # CC=9, fan=18
def map_cmd(project, output, force, stdout)  # CC=7, fan=12
def dsl(directory, command, script, interactive)  # CC=1, fan=13
def cqrs_command(directory, command_type, aggregate_id, data)  # CC=1, fan=19
def nlp_command(text, directory, execute, verbose)  # CC=1, fan=13
def main()  # CC=10, fan=3 ⚠
def main_sumr()  # CC=3, fan=2
```

### `sumd.extractor` (`sumd/extractor.py`)

```python
def _read_toml(path)  # CC=2, fan=2
def extract_pyproject(proj_dir)  # CC=3, fan=5
def _first_task_cmd(cmds)  # CC=4, fan=2
def extract_taskfile(proj_dir)  # CC=6, fan=8
def _parse_openapi_endpoints(paths)  # CC=8, fan=7
def extract_openapi(proj_dir)  # CC=5, fan=7
def _parse_doql_entities(content)  # CC=4, fan=5
def _parse_doql_interfaces(content)  # CC=3, fan=7
def _parse_doql_workflows(content)  # CC=7, fan=10
def _parse_doql_content(content)  # CC=6, fan=14
def extract_doql(proj_dir)  # CC=3, fan=3
def extract_pyqual(proj_dir)  # CC=5, fan=5
def extract_python_modules(proj_dir, pkg_name)  # CC=4, fan=4
def extract_readme_title(proj_dir)  # CC=4, fan=5
def extract_requirements(proj_dir)  # CC=7, fan=7
def extract_makefile(proj_dir)  # CC=7, fan=9
def extract_goal(proj_dir)  # CC=3, fan=7
def extract_env(proj_dir)  # CC=10, fan=9 ⚠
def _parse_dockerfile_line(line, parsed)  # CC=8, fan=6
def extract_dockerfile(proj_dir)  # CC=6, fan=5
def extract_docker_compose(proj_dir)  # CC=10, fan=12 ⚠
def extract_package_json(proj_dir)  # CC=3, fan=6
def _lang_of(path)  # CC=1, fan=2
def _fan_out(func_node)  # CC=5, fan=5
def _cc_estimate(func_node)  # CC=4, fan=4
def _try_radon_cc(src)  # CC=3, fan=1
def _analyse_py_top_funcs(tree, radon_cc)  # CC=5, fan=6
def _analyse_class_methods(node, radon_cc)  # CC=6, fan=6
def _analyse_py_top_classes(tree, radon_cc)  # CC=5, fan=7
def _analyse_py_module(path)  # CC=2, fan=6
def _parse_ignore_file(ignore_path)  # CC=6, fan=7
def _path_matches_pattern(path, pattern)  # CC=18, fan=4 ⚠
def _is_path_ignored(path, proj_dir, ignore_patterns)  # CC=7, fan=3
def _is_map_ignored_path(p)  # CC=4, fan=1
def _collect_map_files(proj_dir)  # CC=8, fan=12
def _render_map_detail(proj_dir, modules)  # CC=5, fan=3
def _map_cc_stats(all_funcs)  # CC=12, fan=8 ⚠
def _render_py_module_detail(rel, info, a)  # CC=7, fan=3
def generate_map_toon(proj_dir)  # CC=5, fan=13
def generate_project_logic(proj_dir)  # CC=20, fan=18 ⚠
def _extract_sumd_semantic_facts(proj_dir)  # CC=15, fan=10 ⚠
def required_tools_for_profile(profile)  # CC=4, fan=0
def extract_source_snippets(proj_dir, pkg_name)  # CC=6, fan=11
def extract_swop(proj_dir)  # CC=9, fan=8
def extract_project_analysis(proj_dir, refactor)  # CC=6, fan=7
```

### `sumd.prolog_engine` (`sumd/prolog_engine.py`)

```python
def is_variable(x)  # CC=6, fan=4
def to_term(x)  # CC=13, fan=14 ⚠
def _split_body_terms(body_str)  # CC=13, fan=3 ⚠
def unify(x, y, subst)  # CC=10, fan=7 ⚠
def resolve_val(x, subst)  # CC=3, fan=1
def deep_resolve(x, subst)  # CC=3, fan=4
def extend_subst(v, val, subst)  # CC=2, fan=2
def occurs_check(v, val, subst)  # CC=4, fan=4
def rename_variables(rule, suffix)  # CC=2, fan=5
class Variable:  # Represents a logical variable in our pure Python engine.
    def __init__(name)  # CC=2
    def __repr__()  # CC=2
    def __eq__(other)  # CC=3
    def __hash__()  # CC=1
class Term:  # Represents a Prolog term (e.g. parent(john, mary)).
    def __init__(op)  # CC=2
    def __repr__()  # CC=2
    def __eq__(other)  # CC=3
class Rule:  # Represents a Prolog rule Head :- Body.
    def __init__(head, body)  # CC=2
    def __repr__()  # CC=2
class PythonPrologDB:  # In-memory Prolog database for pure Python execution.
    def __init__()  # CC=2
    def add_fact(op)  # CC=2
    def add_rule(head, body)  # CC=1
    def parse_and_load(prolog_text)  # CC=6
class PythonPrologEngine:  # SLD Resolution Logic Interpreter.
    def __init__(db)  # CC=2
    def query(goal_str)  # CC=5
    def _find_vars(term)  # CC=1
    def _resolve(goals, subst)  # CC=12 ⚠
class HybridPrologEngine:  # Hybrid Logic Engine delegating queries based on backend avai
    def __init__(prolog_file_path)  # CC=2
    def query(query_str)  # CC=5
    def _query_pyswip(query_str)  # CC=4
    def _query_subprocess(query_str)  # CC=9
    def _query_python(query_str)  # CC=1
    def _swipl_executable_exists()  # CC=2
```

### `sumd.mcp_server` (`sumd/mcp_server.py`)

```python
def _doc_to_dict(doc)  # CC=2, fan=0
def _resolve_path(path)  # CC=2, fan=3
def list_tools()  # CC=1, fan=2
def _tool_parse_sumd(arguments)  # CC=1, fan=5
def _tool_validate_sumd(arguments)  # CC=1, fan=7
def _tool_export_sumd(arguments)  # CC=5, fan=8
def _tool_list_sections(arguments)  # CC=2, fan=4
def _tool_get_section(arguments)  # CC=5, fan=6
def _tool_info_sumd(arguments)  # CC=2, fan=5
def _tool_generate_sumd(arguments)  # CC=5, fan=5
def _tool_execute_command(arguments)  # CC=3, fan=6
def _tool_execute_query(arguments)  # CC=3, fan=5
def _tool_get_events(arguments)  # CC=3, fan=6
def _tool_get_aggregate(arguments)  # CC=3, fan=4
def _tool_execute_dsl(arguments)  # CC=3, fan=5
def _tool_dsl_shell_info(arguments)  # CC=2, fan=3
def call_tool(name, arguments)  # CC=3, fan=4
def main()  # CC=1, fan=3
```

### `sumd.pipeline` (`sumd/pipeline.py`)

```python
def _refresh_map_toon(proj_dir)  # CC=5, fan=4
def _find_tools_bin_dir(proj_dir)  # CC=3, fan=1
def _run_tool_if_present(bin_dir, name, args, proj_dir)  # CC=3, fan=3
def _refresh_analysis_files(proj_dir, profile)  # CC=7, fan=5
def _collect_tool_sources(pyproj, reqs, tasks, makefile, scenarios)  # CC=7, fan=3
def _doql_sources(doql)  # CC=4, fan=1
def _collect_pkg_sources(pyproj, reqs, tasks, makefile, scenarios, openapi, doql, pyqual, goal, env_vars)  # CC=5, fan=6
def _collect_infra_sources(dockerfile, compose, pkg_json, modules, project_analysis)  # CC=6, fan=3
def _collect_sources(pyproj, reqs, tasks, makefile, scenarios, openapi, doql, pyqual, goal, env_vars, dockerfile, compose, pkg_json, modules, project_analysis, swop)  # CC=2, fan=4
def _inject_toc(content)  # CC=3, fan=6
class RenderPipeline:  # Collect project data → build sections → render → inject TOC.
    def __init__(proj_dir, raw_sources)  # CC=1
    def _collect()  # CC=3
    def _build_registered_sections(ctx, profile)  # CC=4
    def _render_legacy_sections(ctx)  # CC=1
    def _assemble(ctx, profile)  # CC=4
    def run(profile, return_sources)  # CC=2
```

## Call Graph

*215 nodes · 213 edges · 31 modules · CC̄=3.9*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `print` *(in test)* | 0 | 84 | 0 | **84** |
| `generate_project_logic` *(in sumd.extractor)* | 20 ⚠ | 2 | 71 | **73** |
| `run` *(in examples.mcp.mcp_client)* | 11 ⚠ | 1 | 53 | **54** |
| `create_builtin_registry` *(in sumd.dsl.commands)* | 1 | 2 | 45 | **47** |
| `to_term` *(in sumd.prolog_engine)* | 13 ⚠ | 14 | 29 | **43** |
| `to_term` *(in sumd_logic_validator.sumd_logic_validator.engine)* | 13 ⚠ | 4 | 29 | **33** |
| `analyze` *(in sumd.cli)* | 11 ⚠ | 0 | 33 | **33** |
| `_collect` *(in sumd.pipeline.RenderPipeline)* | 3 | 0 | 31 | **31** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/oqlos/sumd
# generated in 0.13s
# nodes: 215 | edges: 213 | modules: 31
# CC̄=3.9

HUBS[20]:
  test.print
    CC=0  in:84  out:0  total:84
  sumd.extractor.generate_project_logic
    CC=20  in:2  out:71  total:73
  examples.mcp.mcp_client.run
    CC=11  in:1  out:53  total:54
  sumd.dsl.commands.create_builtin_registry
    CC=1  in:2  out:45  total:47
  sumd.prolog_engine.to_term
    CC=13  in:14  out:29  total:43
  sumd_logic_validator.sumd_logic_validator.engine.to_term
    CC=13  in:4  out:29  total:33
  sumd.cli.analyze
    CC=11  in:0  out:33  total:33
  sumd.pipeline.RenderPipeline._collect
    CC=3  in:0  out:31  total:31
  sumd.sections.call_graph._render_call_graph
    CC=7  in:0  out:28  total:28
  sumd.extractor.generate_map_toon
    CC=5  in:3  out:24  total:27
  sumd.dsl.shell.DSLShell._handle_shell_command
    CC=14  in:0  out:24  total:24
  sumd.cli.lint
    CC=12  in:0  out:23  total:23
  sumd.extractor.extract_pyproject
    CC=3  in:5  out:17  total:22
  sumd.parser.SUMDParser.parse_file
    CC=1  in:20  out:2  total:22
  sumd.sections.quality._render_quality_parsed
    CC=9  in:1  out:21  total:22
  sumd.cli.map_cmd
    CC=7  in:0  out:20  total:20
  sumd.sections.dependencies._render_deps_runtime
    CC=6  in:1  out:19  total:20
  sumd.extractor._parse_doql_content
    CC=6  in:1  out:19  total:20
  sumd.sections.interfaces._render_interfaces_openapi
    CC=6  in:1  out:19  total:20
  sumd.extractor._path_matches_pattern
    CC=18  in:2  out:18  total:20

MODULES:
  examples.llm.anthropic_example  [2 funcs]
    ask  CC=1  out:3
    main  CC=2  out:14
  examples.llm.openai_example  [3 funcs]
    ask  CC=1  out:3
    build_context  CC=5  out:9
    main  CC=2  out:15
  examples.mcp.mcp_client  [2 funcs]
    main  CC=3  out:12
    run  CC=11  out:53
  sumd.cli  [38 funcs]
    _api_scenario_template  CC=1  out:3
    _build_doql_spec  CC=3  out:4
    _detect_project_type  CC=8  out:4
    _detect_projects  CC=1  out:1
    _echo_scan_result  CC=2  out:4
    _ensure_venv  CC=4  out:7
    _export_sumd_json  CC=2  out:2
    _finalize_scan  CC=9  out:16
    _generate_doql_less  CC=7  out:10
    _is_project_dir  CC=8  out:4
  sumd.cqrs.queries  [5 funcs]
    _handle_get_project_info  CC=3  out:11
    _handle_get_sumd_document  CC=3  out:4
    _handle_get_sumd_section  CC=4  out:7
    _handle_get_validation_results  CC=4  out:9
    _handle_list_sumd_sections  CC=3  out:4
  sumd.cqrs.sumd_aggregate  [1 funcs]
    create_from_file  CC=6  out:12
  sumd.dsl.commands  [5 funcs]
    _cmd_help  CC=2  out:3
    _cmd_sumd_info  CC=3  out:3
    _cmd_sumd_map  CC=6  out:7
    _cmd_sumd_validate  CC=2  out:7
    create_builtin_registry  CC=1  out:45
  sumd.dsl.engine  [2 funcs]
    _builtin_print  CC=1  out:1
    execute_text  CC=3  out:5
  sumd.dsl.parser  [2 funcs]
    _match  CC=2  out:2
    parse_dsl  CC=1  out:4
  sumd.dsl.schema_commands  [2 funcs]
    _cmd_sumd_info  CC=3  out:3
    _cmd_sumd_validate  CC=2  out:6
  sumd.dsl.shell  [7 funcs]
    __init__  CC=4  out:6
    _execute_line  CC=9  out:12
    _handle_shell_command  CC=14  out:24
    execute_command  CC=2  out:3
    execute_script  CC=9  out:17
    run  CC=9  out:15
    execute_dsl  CC=4  out:7
  sumd.extractor  [37 funcs]
    _analyse_class_methods  CC=6  out:6
    _analyse_py_module  CC=2  out:6
    _analyse_py_top_classes  CC=5  out:8
    _analyse_py_top_funcs  CC=5  out:7
    _cc_estimate  CC=4  out:4
    _collect_map_files  CC=8  out:13
    _fan_out  CC=5  out:8
    _first_task_cmd  CC=4  out:4
    _is_map_ignored_path  CC=4  out:1
    _is_path_ignored  CC=7  out:4
  sumd.mcp_server  [9 funcs]
    _doc_to_dict  CC=2  out:0
    _resolve_path  CC=2  out:4
    _tool_export_sumd  CC=5  out:12
    _tool_generate_sumd  CC=5  out:11
    _tool_get_section  CC=5  out:8
    _tool_info_sumd  CC=2  out:5
    _tool_list_sections  CC=2  out:4
    _tool_parse_sumd  CC=1  out:5
    _tool_validate_sumd  CC=1  out:7
  sumd.parser  [1 funcs]
    parse_file  CC=1  out:2
  sumd.pipeline  [12 funcs]
    _collect  CC=3  out:31
    run  CC=2  out:3
    _collect_infra_sources  CC=6  out:10
    _collect_pkg_sources  CC=5  out:11
    _collect_sources  CC=2  out:4
    _collect_tool_sources  CC=7  out:6
    _doql_sources  CC=4  out:4
    _find_tools_bin_dir  CC=3  out:1
    _inject_toc  CC=3  out:9
    _refresh_analysis_files  CC=7  out:11
  sumd.prolog_engine  [13 funcs]
    add_fact  CC=2  out:4
    parse_and_load  CC=6  out:16
    _resolve  CC=12  out:15
    query  CC=5  out:8
    _split_body_terms  CC=13  out:7
    deep_resolve  CC=3  out:4
    extend_subst  CC=2  out:2
    is_variable  CC=6  out:5
    occurs_check  CC=4  out:4
    rename_variables  CC=2  out:8
  sumd.sections.architecture  [8 funcs]
    _render_architecture  CC=6  out:13
    _render_architecture_doql_parsed  CC=1  out:4
    _render_architecture_doql_section  CC=6  out:14
    _render_architecture_rules  CC=3  out:10
    _render_doql_app  CC=3  out:8
    _render_doql_entities  CC=6  out:9
    _render_doql_integrations  CC=5  out:9
    _render_doql_interfaces  CC=6  out:10
  sumd.sections.call_graph  [6 funcs]
    _parse_calls_header  CC=6  out:12
    _parse_calls_hubs  CC=8  out:4
    _parse_calls_toon  CC=1  out:3
    _parse_hub_stat_line  CC=2  out:9
    _process_in_hubs_line  CC=6  out:6
    _render_call_graph  CC=7  out:28
  sumd.sections.code_analysis  [2 funcs]
    render  CC=1  out:1
    _render_code_analysis  CC=9  out:15
  sumd.sections.dependencies  [3 funcs]
    _render_dependencies  CC=2  out:6
    _render_deps_dev  CC=6  out:15
    _render_deps_runtime  CC=6  out:19
  sumd.sections.deployment  [5 funcs]
    _render_deployment  CC=1  out:5
    _render_deployment_docker  CC=8  out:7
    _render_deployment_install  CC=2  out:11
    _render_deployment_reqs  CC=5  out:9
    _render_dockerfile_info  CC=6  out:9
  sumd.sections.environment  [3 funcs]
    render  CC=1  out:4
    _render_env_section  CC=3  out:7
    _render_goal_section  CC=9  out:17
  sumd.sections.extras  [3 funcs]
    _render_extras  CC=3  out:3
    _render_makefile_targets  CC=3  out:4
    _render_pkg_json_scripts  CC=7  out:16
  sumd.sections.interfaces  [6 funcs]
    _render_interfaces  CC=5  out:9
    _render_interfaces_openapi  CC=6  out:19
    _render_interfaces_testql  CC=3  out:4
    _render_testql_extras  CC=7  out:9
    _render_testql_one_structured  CC=7  out:13
    _render_testql_raw  CC=4  out:12
  sumd.sections.quality  [3 funcs]
    _render_quality  CC=3  out:4
    _render_quality_parsed  CC=9  out:21
    _render_quality_raw  CC=2  out:7
  sumd.sections.workflows  [3 funcs]
    _render_workflows  CC=4  out:5
    _render_workflows_doql  CC=4  out:7
    _render_workflows_taskfile  CC=6  out:17
  sumd.toon_parser  [7 funcs]
    _parse_toon_block_api  CC=6  out:4
    _parse_toon_block_assert  CC=7  out:9
    _parse_toon_block_config  CC=9  out:8
    _parse_toon_block_navigate  CC=7  out:5
    _parse_toon_block_performance  CC=7  out:8
    _parse_toon_file  CC=4  out:16
    extract_testql_scenarios  CC=7  out:12
  sumd.validator  [10 funcs]
    _check_empty_links  CC=2  out:1
    _check_h1  CC=3  out:2
    _check_metadata_fields  CC=9  out:7
    _check_required_sections  CC=7  out:6
    _check_unclosed_fences  CC=4  out:2
    _validate_markpact_meta  CC=5  out:9
    validate_codeblocks  CC=9  out:17
    validate_markdown  CC=1  out:6
    validate_project_architecture  CC=8  out:15
    validate_sumd_file  CC=4  out:8
  sumd_logic_validator.sumd_logic_validator.cli  [3 funcs]
    get_engine  CC=4  out:9
    query  CC=6  out:14
    shell  CC=10  out:16
  sumd_logic_validator.sumd_logic_validator.engine  [11 funcs]
    add_fact  CC=2  out:4
    parse_and_load  CC=7  out:17
    _resolve  CC=12  out:15
    query  CC=5  out:8
    deep_resolve  CC=3  out:4
    extend_subst  CC=2  out:2
    is_variable  CC=6  out:4
    occurs_check  CC=4  out:4
    resolve_val  CC=3  out:1
    to_term  CC=13  out:29
  test  [1 funcs]
    print  CC=0  out:0

EDGES:
  examples.llm.anthropic_example.ask → sumd.parser.SUMDParser.parse_file
  examples.llm.anthropic_example.main → test.print
  examples.llm.anthropic_example.main → examples.llm.anthropic_example.ask
  examples.llm.openai_example.build_context → sumd.parser.SUMDParser.parse_file
  examples.llm.openai_example.ask → examples.llm.openai_example.build_context
  examples.llm.openai_example.main → test.print
  examples.mcp.mcp_client.run → test.print
  examples.mcp.mcp_client.main → test.print
  sumd.toon_parser._parse_toon_file → sumd.dsl.parser.DSLParser._match
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_config
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_api
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_assert
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_performance
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_navigate
  sumd.toon_parser.extract_testql_scenarios → sumd.toon_parser._parse_toon_file
  sumd.validator.validate_codeblocks → sumd.validator._validate_markpact_meta
  sumd.validator.validate_markdown → sumd.validator._check_empty_links
  sumd.validator.validate_markdown → sumd.validator._check_unclosed_fences
  sumd.validator.validate_markdown → sumd.validator._check_metadata_fields
  sumd.validator.validate_markdown → sumd.validator._check_h1
  sumd.validator.validate_markdown → sumd.validator._check_required_sections
  sumd.validator.validate_project_architecture → sumd.extractor.generate_project_logic
  sumd.validator.validate_sumd_file → sumd.validator.validate_markdown
  sumd.validator.validate_sumd_file → sumd.validator.validate_codeblocks
  sumd.validator.validate_sumd_file → sumd.validator.validate_project_architecture
  sumd.cli._node_spec_from_package_json → sumd.cli._node_framework
  sumd.cli._build_doql_spec → sumd.extractor.extract_package_json
  sumd.cli._build_doql_spec → sumd.cli._node_spec_from_package_json
  sumd.cli._generate_doql_less → sumd.cli._build_doql_spec
  sumd.cli._generate_doql_less → sumd.cli._render_doql_boilerplate
  sumd.cli.validate → sumd.parser.SUMDParser.parse_file
  sumd.cli.export → sumd.parser.SUMDParser.parse_file
  sumd.cli.info → sumd.parser.SUMDParser.parse_file
  sumd.cli.extract → sumd.parser.SUMDParser.parse_file
  sumd.cli._walk_projects → sumd.cli._is_project_dir
  sumd.cli._detect_projects → sumd.cli._walk_projects
  sumd.cli._run_one_tool → sumd.cli._tool_bin
  sumd.cli._run_analysis_tools → sumd.cli._ensure_venv
  sumd.cli._run_analysis_tools → sumd.cli._run_one_tool
  sumd.cli._render_write_validate → sumd.validator.validate_sumd_file
  sumd.cli._render_write_validate → sumd.parser.SUMDParser.parse_file
  sumd.cli._maybe_generate_doql → sumd.cli._detect_project_type
  sumd.cli._maybe_generate_doql → sumd.extractor.extract_pyproject
  sumd.cli._maybe_generate_doql → sumd.cli._generate_doql_less
  sumd.cli._maybe_generate_doql → sumd.extractor.extract_package_json
  sumd.cli._finalize_scan → sumd.cli._echo_scan_result
  sumd.cli._finalize_scan → sumd.cli._export_sumd_json
  sumd.cli._finalize_scan → sumd.cli._run_analysis_tools
  sumd.cli._scan_one_project → sumd.cli._render_write_validate
  sumd.cli._scan_one_project → sumd.cli._finalize_scan
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (2)

**`CLI Command Tests`**

**`sumd-cli.testql.toon.yaml — CLI command and pipeline validation`**
- assert `command_scan_status == 0`
- assert `command_lint_status == 0`
- assert `command_info_status == 0`
- perf `execution_time_ms < 5000`
- perf `memory_peak_mb < 128`

### Integration (1)

**`Auto-generated from Python Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/oqlos/sumd
# generated in 0.13s
# nodes: 215 | edges: 213 | modules: 31
# CC̄=3.9

HUBS[20]:
  test.print
    CC=0  in:84  out:0  total:84
  sumd.extractor.generate_project_logic
    CC=20  in:2  out:71  total:73
  examples.mcp.mcp_client.run
    CC=11  in:1  out:53  total:54
  sumd.dsl.commands.create_builtin_registry
    CC=1  in:2  out:45  total:47
  sumd.prolog_engine.to_term
    CC=13  in:14  out:29  total:43
  sumd_logic_validator.sumd_logic_validator.engine.to_term
    CC=13  in:4  out:29  total:33
  sumd.cli.analyze
    CC=11  in:0  out:33  total:33
  sumd.pipeline.RenderPipeline._collect
    CC=3  in:0  out:31  total:31
  sumd.sections.call_graph._render_call_graph
    CC=7  in:0  out:28  total:28
  sumd.extractor.generate_map_toon
    CC=5  in:3  out:24  total:27
  sumd.dsl.shell.DSLShell._handle_shell_command
    CC=14  in:0  out:24  total:24
  sumd.cli.lint
    CC=12  in:0  out:23  total:23
  sumd.extractor.extract_pyproject
    CC=3  in:5  out:17  total:22
  sumd.parser.SUMDParser.parse_file
    CC=1  in:20  out:2  total:22
  sumd.sections.quality._render_quality_parsed
    CC=9  in:1  out:21  total:22
  sumd.cli.map_cmd
    CC=7  in:0  out:20  total:20
  sumd.sections.dependencies._render_deps_runtime
    CC=6  in:1  out:19  total:20
  sumd.extractor._parse_doql_content
    CC=6  in:1  out:19  total:20
  sumd.sections.interfaces._render_interfaces_openapi
    CC=6  in:1  out:19  total:20
  sumd.extractor._path_matches_pattern
    CC=18  in:2  out:18  total:20

MODULES:
  examples.llm.anthropic_example  [2 funcs]
    ask  CC=1  out:3
    main  CC=2  out:14
  examples.llm.openai_example  [3 funcs]
    ask  CC=1  out:3
    build_context  CC=5  out:9
    main  CC=2  out:15
  examples.mcp.mcp_client  [2 funcs]
    main  CC=3  out:12
    run  CC=11  out:53
  sumd.cli  [38 funcs]
    _api_scenario_template  CC=1  out:3
    _build_doql_spec  CC=3  out:4
    _detect_project_type  CC=8  out:4
    _detect_projects  CC=1  out:1
    _echo_scan_result  CC=2  out:4
    _ensure_venv  CC=4  out:7
    _export_sumd_json  CC=2  out:2
    _finalize_scan  CC=9  out:16
    _generate_doql_less  CC=7  out:10
    _is_project_dir  CC=8  out:4
  sumd.cqrs.queries  [5 funcs]
    _handle_get_project_info  CC=3  out:11
    _handle_get_sumd_document  CC=3  out:4
    _handle_get_sumd_section  CC=4  out:7
    _handle_get_validation_results  CC=4  out:9
    _handle_list_sumd_sections  CC=3  out:4
  sumd.cqrs.sumd_aggregate  [1 funcs]
    create_from_file  CC=6  out:12
  sumd.dsl.commands  [5 funcs]
    _cmd_help  CC=2  out:3
    _cmd_sumd_info  CC=3  out:3
    _cmd_sumd_map  CC=6  out:7
    _cmd_sumd_validate  CC=2  out:7
    create_builtin_registry  CC=1  out:45
  sumd.dsl.engine  [2 funcs]
    _builtin_print  CC=1  out:1
    execute_text  CC=3  out:5
  sumd.dsl.parser  [2 funcs]
    _match  CC=2  out:2
    parse_dsl  CC=1  out:4
  sumd.dsl.schema_commands  [2 funcs]
    _cmd_sumd_info  CC=3  out:3
    _cmd_sumd_validate  CC=2  out:6
  sumd.dsl.shell  [7 funcs]
    __init__  CC=4  out:6
    _execute_line  CC=9  out:12
    _handle_shell_command  CC=14  out:24
    execute_command  CC=2  out:3
    execute_script  CC=9  out:17
    run  CC=9  out:15
    execute_dsl  CC=4  out:7
  sumd.extractor  [37 funcs]
    _analyse_class_methods  CC=6  out:6
    _analyse_py_module  CC=2  out:6
    _analyse_py_top_classes  CC=5  out:8
    _analyse_py_top_funcs  CC=5  out:7
    _cc_estimate  CC=4  out:4
    _collect_map_files  CC=8  out:13
    _fan_out  CC=5  out:8
    _first_task_cmd  CC=4  out:4
    _is_map_ignored_path  CC=4  out:1
    _is_path_ignored  CC=7  out:4
  sumd.mcp_server  [9 funcs]
    _doc_to_dict  CC=2  out:0
    _resolve_path  CC=2  out:4
    _tool_export_sumd  CC=5  out:12
    _tool_generate_sumd  CC=5  out:11
    _tool_get_section  CC=5  out:8
    _tool_info_sumd  CC=2  out:5
    _tool_list_sections  CC=2  out:4
    _tool_parse_sumd  CC=1  out:5
    _tool_validate_sumd  CC=1  out:7
  sumd.parser  [1 funcs]
    parse_file  CC=1  out:2
  sumd.pipeline  [12 funcs]
    _collect  CC=3  out:31
    run  CC=2  out:3
    _collect_infra_sources  CC=6  out:10
    _collect_pkg_sources  CC=5  out:11
    _collect_sources  CC=2  out:4
    _collect_tool_sources  CC=7  out:6
    _doql_sources  CC=4  out:4
    _find_tools_bin_dir  CC=3  out:1
    _inject_toc  CC=3  out:9
    _refresh_analysis_files  CC=7  out:11
  sumd.prolog_engine  [13 funcs]
    add_fact  CC=2  out:4
    parse_and_load  CC=6  out:16
    _resolve  CC=12  out:15
    query  CC=5  out:8
    _split_body_terms  CC=13  out:7
    deep_resolve  CC=3  out:4
    extend_subst  CC=2  out:2
    is_variable  CC=6  out:5
    occurs_check  CC=4  out:4
    rename_variables  CC=2  out:8
  sumd.sections.architecture  [8 funcs]
    _render_architecture  CC=6  out:13
    _render_architecture_doql_parsed  CC=1  out:4
    _render_architecture_doql_section  CC=6  out:14
    _render_architecture_rules  CC=3  out:10
    _render_doql_app  CC=3  out:8
    _render_doql_entities  CC=6  out:9
    _render_doql_integrations  CC=5  out:9
    _render_doql_interfaces  CC=6  out:10
  sumd.sections.call_graph  [6 funcs]
    _parse_calls_header  CC=6  out:12
    _parse_calls_hubs  CC=8  out:4
    _parse_calls_toon  CC=1  out:3
    _parse_hub_stat_line  CC=2  out:9
    _process_in_hubs_line  CC=6  out:6
    _render_call_graph  CC=7  out:28
  sumd.sections.code_analysis  [2 funcs]
    render  CC=1  out:1
    _render_code_analysis  CC=9  out:15
  sumd.sections.dependencies  [3 funcs]
    _render_dependencies  CC=2  out:6
    _render_deps_dev  CC=6  out:15
    _render_deps_runtime  CC=6  out:19
  sumd.sections.deployment  [5 funcs]
    _render_deployment  CC=1  out:5
    _render_deployment_docker  CC=8  out:7
    _render_deployment_install  CC=2  out:11
    _render_deployment_reqs  CC=5  out:9
    _render_dockerfile_info  CC=6  out:9
  sumd.sections.environment  [3 funcs]
    render  CC=1  out:4
    _render_env_section  CC=3  out:7
    _render_goal_section  CC=9  out:17
  sumd.sections.extras  [3 funcs]
    _render_extras  CC=3  out:3
    _render_makefile_targets  CC=3  out:4
    _render_pkg_json_scripts  CC=7  out:16
  sumd.sections.interfaces  [6 funcs]
    _render_interfaces  CC=5  out:9
    _render_interfaces_openapi  CC=6  out:19
    _render_interfaces_testql  CC=3  out:4
    _render_testql_extras  CC=7  out:9
    _render_testql_one_structured  CC=7  out:13
    _render_testql_raw  CC=4  out:12
  sumd.sections.quality  [3 funcs]
    _render_quality  CC=3  out:4
    _render_quality_parsed  CC=9  out:21
    _render_quality_raw  CC=2  out:7
  sumd.sections.workflows  [3 funcs]
    _render_workflows  CC=4  out:5
    _render_workflows_doql  CC=4  out:7
    _render_workflows_taskfile  CC=6  out:17
  sumd.toon_parser  [7 funcs]
    _parse_toon_block_api  CC=6  out:4
    _parse_toon_block_assert  CC=7  out:9
    _parse_toon_block_config  CC=9  out:8
    _parse_toon_block_navigate  CC=7  out:5
    _parse_toon_block_performance  CC=7  out:8
    _parse_toon_file  CC=4  out:16
    extract_testql_scenarios  CC=7  out:12
  sumd.validator  [10 funcs]
    _check_empty_links  CC=2  out:1
    _check_h1  CC=3  out:2
    _check_metadata_fields  CC=9  out:7
    _check_required_sections  CC=7  out:6
    _check_unclosed_fences  CC=4  out:2
    _validate_markpact_meta  CC=5  out:9
    validate_codeblocks  CC=9  out:17
    validate_markdown  CC=1  out:6
    validate_project_architecture  CC=8  out:15
    validate_sumd_file  CC=4  out:8
  sumd_logic_validator.sumd_logic_validator.cli  [3 funcs]
    get_engine  CC=4  out:9
    query  CC=6  out:14
    shell  CC=10  out:16
  sumd_logic_validator.sumd_logic_validator.engine  [11 funcs]
    add_fact  CC=2  out:4
    parse_and_load  CC=7  out:17
    _resolve  CC=12  out:15
    query  CC=5  out:8
    deep_resolve  CC=3  out:4
    extend_subst  CC=2  out:2
    is_variable  CC=6  out:4
    occurs_check  CC=4  out:4
    resolve_val  CC=3  out:1
    to_term  CC=13  out:29
  test  [1 funcs]
    print  CC=0  out:0

EDGES:
  examples.llm.anthropic_example.ask → sumd.parser.SUMDParser.parse_file
  examples.llm.anthropic_example.main → test.print
  examples.llm.anthropic_example.main → examples.llm.anthropic_example.ask
  examples.llm.openai_example.build_context → sumd.parser.SUMDParser.parse_file
  examples.llm.openai_example.ask → examples.llm.openai_example.build_context
  examples.llm.openai_example.main → test.print
  examples.mcp.mcp_client.run → test.print
  examples.mcp.mcp_client.main → test.print
  sumd.toon_parser._parse_toon_file → sumd.dsl.parser.DSLParser._match
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_config
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_api
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_assert
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_performance
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_navigate
  sumd.toon_parser.extract_testql_scenarios → sumd.toon_parser._parse_toon_file
  sumd.validator.validate_codeblocks → sumd.validator._validate_markpact_meta
  sumd.validator.validate_markdown → sumd.validator._check_empty_links
  sumd.validator.validate_markdown → sumd.validator._check_unclosed_fences
  sumd.validator.validate_markdown → sumd.validator._check_metadata_fields
  sumd.validator.validate_markdown → sumd.validator._check_h1
  sumd.validator.validate_markdown → sumd.validator._check_required_sections
  sumd.validator.validate_project_architecture → sumd.extractor.generate_project_logic
  sumd.validator.validate_sumd_file → sumd.validator.validate_markdown
  sumd.validator.validate_sumd_file → sumd.validator.validate_codeblocks
  sumd.validator.validate_sumd_file → sumd.validator.validate_project_architecture
  sumd.cli._node_spec_from_package_json → sumd.cli._node_framework
  sumd.cli._build_doql_spec → sumd.extractor.extract_package_json
  sumd.cli._build_doql_spec → sumd.cli._node_spec_from_package_json
  sumd.cli._generate_doql_less → sumd.cli._build_doql_spec
  sumd.cli._generate_doql_less → sumd.cli._render_doql_boilerplate
  sumd.cli.validate → sumd.parser.SUMDParser.parse_file
  sumd.cli.export → sumd.parser.SUMDParser.parse_file
  sumd.cli.info → sumd.parser.SUMDParser.parse_file
  sumd.cli.extract → sumd.parser.SUMDParser.parse_file
  sumd.cli._walk_projects → sumd.cli._is_project_dir
  sumd.cli._detect_projects → sumd.cli._walk_projects
  sumd.cli._run_one_tool → sumd.cli._tool_bin
  sumd.cli._run_analysis_tools → sumd.cli._ensure_venv
  sumd.cli._run_analysis_tools → sumd.cli._run_one_tool
  sumd.cli._render_write_validate → sumd.validator.validate_sumd_file
  sumd.cli._render_write_validate → sumd.parser.SUMDParser.parse_file
  sumd.cli._maybe_generate_doql → sumd.cli._detect_project_type
  sumd.cli._maybe_generate_doql → sumd.extractor.extract_pyproject
  sumd.cli._maybe_generate_doql → sumd.cli._generate_doql_less
  sumd.cli._maybe_generate_doql → sumd.extractor.extract_package_json
  sumd.cli._finalize_scan → sumd.cli._echo_scan_result
  sumd.cli._finalize_scan → sumd.cli._export_sumd_json
  sumd.cli._finalize_scan → sumd.cli._run_analysis_tools
  sumd.cli._scan_one_project → sumd.cli._render_write_validate
  sumd.cli._scan_one_project → sumd.cli._finalize_scan
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 62f 16900L | python:55,perl:4,shell:3 | 2026-05-21
# CC̄=4.0 | critical:6/542 | dups:6 | cycles:0

HEALTH[8]:
  🔴 DUP   6 classes duplicated
  🔴 GOD   sumd/dsl/parser.py = 666L, 6 classes, 29m, max CC=23
  🟡 CC    _path_matches_pattern CC=18 (limit:15)
  🟡 CC    generate_project_logic CC=20 (limit:15)
  🟡 CC    _extract_sumd_semantic_facts CC=15 (limit:15)
  🟡 CC    _execute_expression CC=15 (limit:15)
  🟡 CC    _parse_statement CC=23 (limit:15)
  🟡 CC    _parse_primary CC=22 (limit:15)

REFACTOR[3]:
  1. rm duplicates  (-6 dup classes)
  2. split sumd/dsl/parser.py  (god module)
  3. split 6 high-CC methods  (CC>15)

PIPELINES[317]:
  [1] Src [main]: main → ask → parse_file
      PURITY: 100% pure
  [2] Src [main]: main → ask → build_context → parse_file
      PURITY: 100% pure
  [3] Src [main]: main → run
      PURITY: 100% pure
  [4] Src [_validate_yaml_body]: _validate_yaml_body
      PURITY: 100% pure
  [5] Src [_validate_less_css_body]: _validate_less_css_body
      PURITY: 100% pure

LAYERS:
  sumd/                           CC̄=4.0    ←in:28  →out:4  ×DUP
  │ !! cli                       1999L  0C   47m  CC=14     ←0
  │ !! extractor                 1282L  0C   45m  CC=20     ←6
  │ !! mcp_server                 714L  0C   18m  CC=5      ←0
  │ !! parser                     666L  6C   29m  CC=23     ←3
  │ !! commands                   656L  2C   30m  CC=9      ←1
  │ !! engine                     594L  2C   38m  CC=15     ←0  ×DUP
  │ !! schema_commands            517L  2C   33m  CC=10     ←0
  │ pipeline                   451L  1C   16m  CC=7      ←0
  │ nlp                        447L  3C   21m  CC=7      ←0
  │ prolog_engine              430L  6C   32m  CC=13     ←1  ×DUP
  │ queries                    419L  13C   17m  CC=10     ←0
  │ validator                  383L  1C   16m  CC=9      ←4
  │ shell                      359L  2C   14m  CC=14     ←0
  │ schema                     351L  14C    3m  CC=1      ←0  ×DUP
  │ sumd_aggregate             344L  3C   18m  CC=6      ←0
  │ commands                   265L  12C    8m  CC=9      ←0
  │ aggregates                 220L  6C   23m  CC=4      ←0
  │ parser                     195L  1C    9m  CC=9      ←9
  │ events                     184L  8C    8m  CC=7      ←0
  │ toon_parser                173L  0C    8m  CC=9      ←2
  │ architecture               170L  1C    9m  CC=6      ←0
  │ interfaces                 157L  1C    8m  CC=7      ←0
  │ call_graph                 156L  1C    7m  CC=8      ←0
  │ deployment                 110L  1C    5m  CC=8      ←0
  │ __init__                   106L  0C    0m  CC=0.0    ←0
  │ dependencies                97L  1C    4m  CC=6      ←0
  │ base                        94L  2C    2m  CC=1      ←0
  │ workflows                   86L  1C    4m  CC=6      ←0
  │ quality                     81L  1C    3m  CC=9      ←0
  │ api_stubs                   76L  1C    2m  CC=11     ←0
  │ extras                      72L  1C    4m  CC=7      ←0
  │ environment                 72L  1C    4m  CC=9      ←0
  │ refactor_analysis           68L  1C    1m  CC=3      ←0
  │ code_analysis               68L  1C    3m  CC=9      ←0
  │ source_snippets             68L  1C    1m  CC=8      ←0
  │ swop                        68L  1C    2m  CC=9      ←0
  │ metadata                    51L  1C    1m  CC=5      ←0
  │ models                      45L  3C    0m  CC=0.0    ←0
  │ configuration               43L  1C    1m  CC=1      ←0
  │ rules.pl                    41L  0C    0m  CC=0.0    ←0
  │ __init__                    35L  0C    0m  CC=0.0    ←0
  │ renderer                    29L  0C    1m  CC=1      ←0
  │ render                      25L  0C    1m  CC=1      ←0
  │ should_render               25L  0C    2m  CC=1      ←0
  │ __init__                    18L  0C    0m  CC=0.0    ←0
  │ generator                   15L  0C    0m  CC=0.0    ←0
  │ __init__                    14L  0C    0m  CC=0.0    ←0
  │ __init__                    12L  0C    0m  CC=0.0    ←0
  │ __main__                     5L  0C    0m  CC=0.0    ←0
  │
  sumd_logic_validator/           CC̄=4.0    ←in:0  →out:0  ×DUP
  │ !! rules.pl                  1234L  0C    0m  CC=0.0    ←0
  │ !! rules.pl                  1234L  0C    0m  CC=0.0    ←0
  │ engine                     434L  6C   32m  CC=14     ←0  ×DUP
  │ cli                        114L  0C    5m  CC=10     ←0
  │ main                         4L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ project.sh                  55L  0C    0m  CC=0.0    ←0
  │ print_errors                 6L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ bootstrap.sh                69L  0C    0m  CC=0.0    ←0
  │
  project/                        CC̄=0.0    ←in:0  →out:0
  │ !! logic.pl                  1188L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                                                                                  sumd                                   sumd.dsl  sumd_logic_validator.sumd_logic_validator                                  sumd.cqrs
                                       sumd                                         ──                                          4                                        ←11                                        ←10  hub
                                   sumd.dsl                                          7                                         ──                                                                                      
  sumd_logic_validator.sumd_logic_validator                                         11                                                                                    ──                                             !! fan-out
                                  sumd.cqrs                                         10                                                                                                                               ──  !! fan-out
  CYCLES: none
  HUB: sumd/ (fan-in=28)
  SMELL: sumd.cqrs/ fan-out=10 → split needed
  SMELL: sumd_logic_validator.sumd_logic_validator/ fan-out=11 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 27 groups | 57f 13292L | 2026-05-21

SUMMARY:
  files_scanned: 57
  total_lines:   13292
  dup_groups:    27
  dup_fragments: 54
  saved_lines:   247
  scan_ms:       18652

HOTSPOTS[7] (files with most duplication):
  sumd_logic_validator/sumd_logic_validator/engine.py  dup=210L  groups=21  frags=21  (1.6%)
  sumd/prolog_engine.py  dup=203L  groups=21  frags=21  (1.5%)
  sumd/toon_parser.py  dup=28L  groups=1  frags=2  (0.2%)
  sumd/parser.py  dup=22L  groups=1  frags=2  (0.2%)
  sumd/dsl/commands.py  dup=20L  groups=1  frags=2  (0.2%)
  sumd/dsl/engine.py  dup=6L  groups=2  frags=2  (0.0%)
  sumd/dsl/schema.py  dup=6L  groups=2  frags=2  (0.0%)

DUPLICATES[27] (ranked by impact):
  [6c27a8b7267e13d7] ! EXAC  _query_subprocess  L=42 N=2 saved=42 sim=1.00
      sumd/prolog_engine.py:378-419  (_query_subprocess)
      sumd_logic_validator/sumd_logic_validator/engine.py:375-423  (_query_subprocess)
  [a9a2b89811f17647]   EXAC  unify  L=22 N=2 saved=22 sim=1.00
      sumd/prolog_engine.py:168-189  (unify)
      sumd_logic_validator/sumd_logic_validator/engine.py:166-187  (unify)
  [a67c25b9011708c8]   EXAC  query  L=22 N=2 saved=22 sim=1.00
      sumd/prolog_engine.py:246-267  (query)
      sumd_logic_validator/sumd_logic_validator/engine.py:244-265  (query)
  [841890ca83127ecd]   EXAC  rename_variables  L=16 N=2 saved=16 sim=1.00
      sumd/prolog_engine.py:222-237  (rename_variables)
      sumd_logic_validator/sumd_logic_validator/engine.py:220-235  (rename_variables)
  [6bc9796b08ce37e6]   EXAC  _query_pyswip  L=16 N=2 saved=16 sim=1.00
      sumd/prolog_engine.py:361-376  (_query_pyswip)
      sumd_logic_validator/sumd_logic_validator/engine.py:358-373  (_query_pyswip)
  [ec6388d8055c3e57]   STRU  _parse_toon_block_performance  L=14 N=2 saved=14 sim=1.00
      sumd/toon_parser.py:70-83  (_parse_toon_block_performance)
      sumd/toon_parser.py:102-115  (_parse_toon_block_gui)
  [d1ab1a804f1b435b]   STRU  parse  L=11 N=2 saved=11 sim=1.00
      sumd/parser.py:150-160  (parse)
      sumd/parser.py:163-173  (parse_file)
  [9b8c09535672da3f]   EXAC  _find_vars  L=10 N=2 saved=10 sim=1.00
      sumd/prolog_engine.py:269-278  (_find_vars)
      sumd_logic_validator/sumd_logic_validator/engine.py:267-276  (_find_vars)
  [a73c4e5f2b96ddaa]   STRU  _cmd_cat  L=10 N=2 saved=10 sim=1.00
      sumd/dsl/commands.py:313-322  (_cmd_cat)
      sumd/dsl/commands.py:647-656  (_cmd_read_file)
  [5257855825b21dc5]   EXAC  __init__  L=9 N=2 saved=9 sim=1.00
      sumd/prolog_engine.py:328-336  (__init__)
      sumd_logic_validator/sumd_logic_validator/engine.py:325-333  (__init__)
  [bcd1189046b690c0]   EXAC  rename  L=8 N=2 saved=8 sim=1.00
      sumd/prolog_engine.py:226-233  (rename)
      sumd_logic_validator/sumd_logic_validator/engine.py:224-231  (rename)
  [a5b94fdf8e33a4d1]   EXAC  occurs_check  L=7 N=2 saved=7 sim=1.00
      sumd/prolog_engine.py:213-219  (occurs_check)
      sumd_logic_validator/sumd_logic_validator/engine.py:211-217  (occurs_check)
  [43d89fdde36f380f]   EXAC  extend_subst  L=6 N=2 saved=6 sim=1.00
      sumd/prolog_engine.py:205-210  (extend_subst)
      sumd_logic_validator/sumd_logic_validator/engine.py:203-208  (extend_subst)
  [85268e3910522b4b]   EXAC  _swipl_executable_exists  L=6 N=2 saved=6 sim=1.00
      sumd/prolog_engine.py:425-430  (_swipl_executable_exists)
      sumd_logic_validator/sumd_logic_validator/engine.py:429-434  (_swipl_executable_exists)
  [d48551a6bad80f43]   EXAC  collect  L=6 N=2 saved=6 sim=1.00
      sumd/prolog_engine.py:271-276  (collect)
      sumd_logic_validator/sumd_logic_validator/engine.py:269-274  (collect)
  [2974f1521921ca23]   EXAC  deep_resolve  L=5 N=2 saved=5 sim=1.00
      sumd/prolog_engine.py:198-202  (deep_resolve)
      sumd_logic_validator/sumd_logic_validator/engine.py:196-200  (deep_resolve)
  [80e26c3323c304e6]   EXAC  resolve_val  L=4 N=2 saved=4 sim=1.00
      sumd/prolog_engine.py:192-195  (resolve_val)
      sumd_logic_validator/sumd_logic_validator/engine.py:190-193  (resolve_val)
  [b34584e45495fb0a]   EXAC  __repr__  L=4 N=2 saved=4 sim=1.00
      sumd/prolog_engine.py:40-43  (__repr__)
      sumd_logic_validator/sumd_logic_validator/engine.py:40-43  (__repr__)
  [2cbecec5d6886745]   EXAC  __eq__  L=4 N=2 saved=4 sim=1.00
      sumd/prolog_engine.py:45-48  (__eq__)
      sumd_logic_validator/sumd_logic_validator/engine.py:45-48  (__eq__)
  [f1a0f3644b1097f5]   EXAC  __repr__  L=4 N=2 saved=4 sim=1.00
      sumd/prolog_engine.py:57-60  (__repr__)
      sumd_logic_validator/sumd_logic_validator/engine.py:57-60  (__repr__)
  [fa6ad8230cb122f6]   EXAC  set_variable  L=3 N=2 saved=3 sim=1.00
      sumd/dsl/engine.py:35-37  (set_variable)
      sumd/dsl/schema.py:163-165  (set_variable)
  [f59133a9d98b31d5]   EXAC  get_variable  L=3 N=2 saved=3 sim=1.00
      sumd/dsl/engine.py:39-41  (get_variable)
      sumd/dsl/schema.py:167-169  (get_variable)
  [0622d41f358b07b3]   EXAC  __init__  L=3 N=2 saved=3 sim=1.00
      sumd/prolog_engine.py:36-38  (__init__)
      sumd_logic_validator/sumd_logic_validator/engine.py:36-38  (__init__)
  [eaae1aeec51c77d3]   EXAC  __init__  L=3 N=2 saved=3 sim=1.00
      sumd/prolog_engine.py:53-55  (__init__)
      sumd_logic_validator/sumd_logic_validator/engine.py:53-55  (__init__)
  [6e1ae427e1b0dd92]   EXAC  __init__  L=3 N=2 saved=3 sim=1.00
      sumd/prolog_engine.py:242-244  (__init__)
      sumd_logic_validator/sumd_logic_validator/engine.py:240-242  (__init__)
  [85a8a3cd76963d11]   EXAC  _query_python  L=3 N=2 saved=3 sim=1.00
      sumd/prolog_engine.py:421-423  (_query_python)
      sumd_logic_validator/sumd_logic_validator/engine.py:425-427  (_query_python)
  [aaae754bdb04529d]   STRU  cli  L=3 N=2 saved=3 sim=1.00
      sumd/cli.py:454-456  (cli)
      sumd_logic_validator/sumd_logic_validator/cli.py:29-31  (main)

REFACTOR[27] (ranked by priority):
  [1] ◐ extract_class      → utils/_query_subprocess.py
      WHY: 2 occurrences of 42-line block across 2 files — saves 42 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [2] ○ extract_function   → utils/unify.py
      WHY: 2 occurrences of 22-line block across 2 files — saves 22 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [3] ○ extract_class      → utils/query.py
      WHY: 2 occurrences of 22-line block across 2 files — saves 22 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [4] ○ extract_function   → utils/rename_variables.py
      WHY: 2 occurrences of 16-line block across 2 files — saves 16 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [5] ○ extract_class      → utils/_query_pyswip.py
      WHY: 2 occurrences of 16-line block across 2 files — saves 16 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [6] ○ extract_function   → sumd/utils/_parse_toon_block_performance.py
      WHY: 2 occurrences of 14-line block across 1 files — saves 14 lines
      FILES: sumd/toon_parser.py
  [7] ○ extract_function   → sumd/utils/parse.py
      WHY: 2 occurrences of 11-line block across 1 files — saves 11 lines
      FILES: sumd/parser.py
  [8] ○ extract_class      → utils/_find_vars.py
      WHY: 2 occurrences of 10-line block across 2 files — saves 10 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [9] ○ extract_function   → sumd/dsl/utils/_cmd_cat.py
      WHY: 2 occurrences of 10-line block across 1 files — saves 10 lines
      FILES: sumd/dsl/commands.py
  [10] ○ extract_class      → utils/__init__.py
      WHY: 2 occurrences of 9-line block across 2 files — saves 9 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [11] ○ extract_function   → utils/rename.py
      WHY: 2 occurrences of 8-line block across 2 files — saves 8 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [12] ○ extract_function   → utils/occurs_check.py
      WHY: 2 occurrences of 7-line block across 2 files — saves 7 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [13] ○ extract_function   → utils/extend_subst.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [14] ○ extract_class      → utils/_swipl_executable_exists.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [15] ○ extract_function   → utils/collect.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [16] ○ extract_function   → utils/deep_resolve.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [17] ○ extract_function   → utils/resolve_val.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [18] ○ extract_class      → utils/__repr__.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [19] ○ extract_class      → utils/__eq__.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [20] ○ extract_class      → utils/__repr__.py
      WHY: 2 occurrences of 4-line block across 2 files — saves 4 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [21] ○ extract_class      → sumd/dsl/utils/set_variable.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/dsl/engine.py, sumd/dsl/schema.py
  [22] ○ extract_class      → sumd/dsl/utils/get_variable.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/dsl/engine.py, sumd/dsl/schema.py
  [23] ○ extract_class      → utils/__init__.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [24] ○ extract_class      → utils/__init__.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [25] ○ extract_class      → utils/__init__.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [26] ○ extract_class      → utils/_query_python.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/prolog_engine.py, sumd_logic_validator/sumd_logic_validator/engine.py
  [27] ○ extract_function   → utils/cli.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/cli.py, sumd_logic_validator/sumd_logic_validator/cli.py

QUICK_WINS[14] (low risk, high savings — do first):
  [2] extract_function   saved=22L  → utils/unify.py
      FILES: prolog_engine.py, engine.py
  [3] extract_class      saved=22L  → utils/query.py
      FILES: prolog_engine.py, engine.py
  [4] extract_function   saved=16L  → utils/rename_variables.py
      FILES: prolog_engine.py, engine.py
  [5] extract_class      saved=16L  → utils/_query_pyswip.py
      FILES: prolog_engine.py, engine.py
  [6] extract_function   saved=14L  → sumd/utils/_parse_toon_block_performance.py
      FILES: toon_parser.py
  [7] extract_function   saved=11L  → sumd/utils/parse.py
      FILES: parser.py
  [8] extract_class      saved=10L  → utils/_find_vars.py
      FILES: prolog_engine.py, engine.py
  [9] extract_function   saved=10L  → sumd/dsl/utils/_cmd_cat.py
      FILES: commands.py
  [10] extract_class      saved=9L  → utils/__init__.py
      FILES: prolog_engine.py, engine.py
  [11] extract_function   saved=8L  → utils/rename.py
      FILES: prolog_engine.py, engine.py

DEPENDENCY_RISK[22] (duplicates spanning multiple packages):
  _query_subprocess  packages=2  files=2
      sumd/prolog_engine.py
      sumd_logic_validator/sumd_logic_validator/engine.py
  unify  packages=2  files=2
      sumd/prolog_engine.py
      sumd_logic_validator/sumd_logic_validator/engine.py
  query  packages=2  files=2
      sumd/prolog_engine.py
      sumd_logic_validator/sumd_logic_validator/engine.py
  rename_variables  packages=2  files=2
      sumd/prolog_engine.py
      sumd_logic_validator/sumd_logic_validator/engine.py
  _query_pyswip  packages=2  files=2
      sumd/prolog_engine.py
      sumd_logic_validator/sumd_logic_validator/engine.py
  _find_vars  packages=2  files=2
      sumd/prolog_engine.py
      sumd_logic_validator/sumd_logic_validator/engine.py
  __init__  packages=2  files=2
      sumd/prolog_engine.py
      sumd_logic_validator/sumd_logic_validator/engine.py

EFFORT_ESTIMATE (total ≈ 16.5h):
  hard   _query_subprocess                   saved=42L  ~252min
  medium unify                               saved=22L  ~88min
  medium query                               saved=22L  ~88min
  medium rename_variables                    saved=16L  ~64min
  medium _query_pyswip                       saved=16L  ~64min
  easy   _parse_toon_block_performance       saved=14L  ~28min
  easy   parse                               saved=11L  ~22min
  medium _find_vars                          saved=10L  ~40min
  easy   _cmd_cat                            saved=10L  ~20min
  medium __init__                            saved=9L  ~36min
  ... +17 more (~288min)

METRICS-TARGET:
  dup_groups:  27 → 0
  saved_lines: 247 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 541 func | 46f | 2026-05-21
# generated in 0.00s

NEXT[8] (ranked by impact):
  [1] !! SPLIT           sumd/cli.py
      WHY: 1999L, 0 classes, max CC=14
      EFFORT: ~4h  IMPACT: 27986

  [2] !! SPLIT           sumd/extractor.py
      WHY: 1282L, 0 classes, max CC=20
      EFFORT: ~4h  IMPACT: 25640

  [3] !  SPLIT-FUNC      generate_project_logic  CC=20  fan=22
      WHY: CC=20 exceeds 15
      EFFORT: ~1h  IMPACT: 440

  [4] !  SPLIT-FUNC      DSLParser._parse_primary  CC=22  fan=18
      WHY: CC=22 exceeds 15
      EFFORT: ~1h  IMPACT: 396

  [5] !  SPLIT-FUNC      _extract_sumd_semantic_facts  CC=15  fan=19
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 285

  [6] !  SPLIT-FUNC      DSLParser._parse_statement  CC=23  fan=10
      WHY: CC=23 exceeds 15
      EFFORT: ~1h  IMPACT: 230

  [7] !  SPLIT-FUNC      DSLEngine._execute_expression  CC=15  fan=13
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 195

  [8] !! SPLIT           sumd_logic_validator/sumd_logic_validator/logic/rules.pl
      WHY: 1234L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[3]:
  ⚠ Splitting sumd/cli.py may break 47 import paths
  ⚠ Splitting sumd/extractor.py may break 45 import paths
  ⚠ Splitting sumd_logic_validator/sumd_logic_validator/logic/rules.pl may break 0 import paths

METRICS-TARGET:
  CC̄:          3.9 → ≤2.7
  max-CC:      23 → ≤11
  god-modules: 12 → 0
  high-CC(≥15): 6 → ≤3
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=3.9 → now CC̄=3.9
```

### Validation (`project/validation.toon.yaml`)

```toon markpact:analysis path=project/validation.toon.yaml
# vallm batch | 162f | 89✓ 8⚠ 13✗ | 2026-05-21

SUMMARY:
  scanned: 162  passed: 89 (54.9%)  warnings: 8  errors: 13  unsupported: 57

WARNINGS[8]{path,score}:
  /home/tom/github/oqlos/sumd/project/logic.pl,0.78
    issues[1]{rule,severity,message,line}:
      syntax.unsupported,warning,Could not parse perl: maximum recursion depth exceeded,
  /home/tom/github/oqlos/sumd/sumd_logic_validator/logic/rules.pl,0.78
    issues[1]{rule,severity,message,line}:
      syntax.unsupported,warning,Could not parse perl: maximum recursion depth exceeded,
  /home/tom/github/oqlos/sumd/sumd_logic_validator/sumd_logic_validator/logic/rules.pl,0.78
    issues[1]{rule,severity,message,line}:
      syntax.unsupported,warning,Could not parse perl: maximum recursion depth exceeded,
  /home/tom/github/oqlos/sumd/sumd/dsl/parser.py,0.93
    issues[4]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_parse_statement has cyclomatic complexity 23 (max: 15),213
      complexity.cyclomatic,warning,_parse_primary has cyclomatic complexity 22 (max: 15),411
      complexity.lizard_cc,warning,_parse_statement: CC=23 exceeds limit 15,213
      complexity.lizard_cc,warning,_parse_primary: CC=22 exceeds limit 15,411
  /home/tom/github/oqlos/sumd/sumd/dsl/commands.py,0.97
    issues[1]{rule,severity,message,line}:
      complexity.lizard_length,warning,create_builtin_registry: 177 lines exceeds limit 100,104
  /home/tom/github/oqlos/sumd/sumd/dsl/nlp.py,0.97
    issues[1]{rule,severity,message,line}:
      complexity.lizard_length,warning,_initialize_default_intents: 106 lines exceeds limit 100,32
  /home/tom/github/oqlos/sumd/sumd/dsl/engine.py,0.98
    issues[1]{rule,severity,message,line}:
      complexity.maintainability,warning,Low maintainability index: 19.9 (threshold: 20),
  /home/tom/github/oqlos/sumd/sumd/dsl/schema_commands.py,0.98
    issues[1]{rule,severity,message,line}:
      complexity.maintainability,warning,Low maintainability index: 19.3 (threshold: 20),

ERRORS[13]{path,score}:
  /home/tom/github/oqlos/sumd/sumd/rules.pl,0.00
    issues[1]{rule,severity,message,line}:
      syntax.tree_sitter,error,tree-sitter found 21 parse error(s) in perl,
  /home/tom/github/oqlos/sumd/sumd_logic_validator/tests/test_engine.py,0.71
    issues[2]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,1
      python.import.resolvable,error,Module 'sumd_logic_validator.engine' not found,3
  /home/tom/github/oqlos/sumd/sumd/mcp_server.py,0.91
    issues[4]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'mcp.server.stdio' not found,30
      python.import.resolvable,error,Module 'mcp.types' not found,31
      python.import.resolvable,error,Module 'mcp.server' not found,32
      python.import.resolvable,error,Module 'toml' not found,417
  /home/tom/github/oqlos/sumd/tests/test_architectural_logic.py,0.91
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,1
  /home/tom/github/oqlos/sumd/tests/test_cli.py,0.93
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,7
  /home/tom/github/oqlos/sumd/tests/test_dogfood.py,0.93
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,17
  /home/tom/github/oqlos/sumd/tests/test_pipeline.py,0.93
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,7
  /home/tom/github/oqlos/sumd/tests/test_dsl.py,0.94
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,3
  /home/tom/github/oqlos/sumd/tests/test_cqrs_es.py,0.95
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,3
  /home/tom/github/oqlos/sumd/sumd/extractor.py,0.96
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'toml' not found,26
  /home/tom/github/oqlos/sumd/tests/test_mcp_server.py,0.96
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,8
  /home/tom/github/oqlos/sumd/sumd/cli.py,0.97
    issues[2]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'toml' not found,589
      python.import.resolvable,error,Module 'toml' not found,527
  /home/tom/github/oqlos/sumd/tests/test_mcp_cqrs_dsl.py,0.97
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,3

UNSUPPORTED[5]{bucket,count}:
  *.md,24
  Dockerfile*,1
  *.txt,3
  *.yml,6
  other,23
```

## Intent

SUMD - Structured Unified Markdown Descriptor for AI-aware project documentation
