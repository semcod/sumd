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
- **version**: `0.3.54`
- **python_requires**: `>=3.10`
- **license**: {'text': 'Apache-2.0'}
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Taskfile.yml, Makefile, testql(3), app.doql.less, pyqual.yaml, goal.yaml, .env.example, src(13 mod), project/(6 analysis files), .swop/manifests/core/commands.yml, .swop/manifests/core/queries.yml, .swop/manifests/core/events.yml

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: sumd;
  version: 0.3.54;
}

dependencies {
  runtime: "click>=8.4.0, pyyaml>=6.0.3, toml>=0.10.2, goal>=2.1.190, costs>=0.1.51, pfix>=0.1.73, mcp>=1.27.1";
  dev: "pytest>=9.0.3, pytest-asyncio>=0.21.0, pytest-cov>=7.1.0, ruff>=0.15.11, build>=1.4.4, twine>=6.2.0, pyqual>=0.1.143, goal>=2.1.190, costs>=0.1.51, pfix>=0.1.73, mcp>=1.27.1";
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
- `sumd.cli_doql`
- `sumd.cli_scan`
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
click>=8.4.0
pyyaml>=6.0.3
toml>=0.10.2
goal>=2.1.190
costs>=0.1.51
pfix>=0.1.73
mcp>=1.27.1
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
costs>=0.1.51
pfix>=0.1.73
mcp>=1.27.1
```

## Source Map

*Top 5 modules by symbol density — signatures for LLM orientation.*

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
def _match_dir_pattern(path, path_str, dir_pattern)  # CC=4, fan=2
def _match_absolute_pattern(path_str, pattern)  # CC=2, fan=1
def _match_recursive_pattern(path_str, pattern)  # CC=3, fan=1
def _match_regular_pattern(path, path_str, pattern)  # CC=5, fan=1
def _path_matches_pattern(path, pattern)  # CC=5, fan=7
def _is_path_ignored(path, proj_dir, ignore_patterns)  # CC=7, fan=3
def _is_map_ignored_path(p)  # CC=4, fan=1
def _collect_map_files(proj_dir)  # CC=8, fan=12
def _render_map_detail(proj_dir, modules)  # CC=5, fan=3
def _map_cc_stats(all_funcs)  # CC=10, fan=7 ⚠
def _render_py_module_detail(rel, info, a)  # CC=7, fan=3
def generate_map_toon(proj_dir)  # CC=5, fan=13
def _facts_project_metadata(proj_dir)  # CC=4, fan=3
def _facts_project_files(proj_dir)  # CC=2, fan=4
def _facts_python_analysis(proj_dir)  # CC=4, fan=5
def _facts_dependencies(proj_dir)  # CC=4, fan=3
def _facts_makefile(proj_dir)  # CC=3, fan=3
def _facts_taskfile(proj_dir)  # CC=3, fan=4
def _facts_env_variables(proj_dir)  # CC=3, fan=3
def _facts_testql_scenarios(proj_dir)  # CC=3, fan=4
def generate_project_logic(proj_dir)  # CC=2, fan=13
def _extract_markpact_files(content)  # CC=4, fan=5
def _extract_doql_interfaces(doql_content)  # CC=3, fan=5
def _extract_doql_workflows(doql_content)  # CC=5, fan=8
def _extract_doql_facts(proj_dir)  # CC=2, fan=5
def _extract_deploy_facts(proj_dir)  # CC=2, fan=2
def _extract_pyqual_gates(proj_dir)  # CC=3, fan=7
def _extract_sumd_semantic_facts(proj_dir)  # CC=2, fan=7
def required_tools_for_profile(profile)  # CC=4, fan=0
def extract_source_snippets(proj_dir, pkg_name)  # CC=6, fan=11
def extract_swop(proj_dir)  # CC=9, fan=8
def extract_project_analysis(proj_dir, refactor)  # CC=6, fan=7
```

### `sumd.cli` (`sumd/cli.py`)

```python
def cli()  # CC=1, fan=2
def validate(file)  # CC=4, fan=8
def export(file, format, output)  # CC=8, fan=11
def info(file)  # CC=3, fan=7
def generate(file, format, output)  # CC=8, fan=15
def extract(file, section)  # CC=5, fan=8
def scan(workspace, export_json, report, fix, raw, analyze, tools, profile, depth, recursive, generate_doql, doql_sync, generate_testql, workspace_mode)  # CC=14, fan=18 ⚠
def lint(files, workspace, as_json, strict)  # CC=6, fan=13
def _lint_classify_issues(r, strict)  # CC=6, fan=1
def _lint_collect_paths(files, workspace)  # CC=6, fan=7
def _lint_print_result(path, r, strict)  # CC=6, fan=4
def _setup_tools_venv(venv_dir, tool_list, force)  # CC=7, fan=6
def _run_code2llm_formats(bin_dir, project, project_output)  # CC=5, fan=4
def _run_tool_subprocess(bin_dir, tool, cmd_args)  # CC=3, fan=4
def _run_analyze_tool(tool, bin_dir, project, project_output)  # CC=4, fan=3
def analyze(project, tools, force)  # CC=7, fan=11
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

### `sumd.validator` (`sumd/validator.py`)

```python
def _validate_yaml_body(body, path)  # CC=2, fan=1
def _validate_less_css_body(body, path)  # CC=2, fan=1
def _validate_mermaid_body(body, path)  # CC=3, fan=4
def _validate_toon_body(body, path)  # CC=2, fan=1
def _validate_bash_body(body, path)  # CC=4, fan=1
def _validate_deps_body(body, path)  # CC=5, fan=6
def _validate_markpact_meta(mp, line_no, lang, meta, issues)  # CC=5, fan=6
def validate_codeblocks(content, source)  # CC=11, fan=11 ⚠
def _check_h1(lines, source)  # CC=3, fan=2
def _check_required_sections(lines, source, profile)  # CC=7, fan=6
def _check_metadata_fields(lines, source)  # CC=9, fan=6
def _check_unclosed_fences(lines, source)  # CC=4, fan=2
def _check_empty_links(content, source)  # CC=2, fan=1
def validate_markdown(content, source, profile)  # CC=1, fan=6
def validate_project_architecture(proj_dir)  # CC=8, fan=11
def validate_sumd_file(path, profile)  # CC=4, fan=8
class CodeBlockIssue:
```

## Call Graph

*234 nodes · 224 edges · 33 modules · CC̄=3.7*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `print` *(in test)* | 0 | 84 | 0 | **84** |
| `run` *(in examples.mcp.mcp_client)* | 11 ⚠ | 1 | 53 | **54** |
| `create_builtin_registry` *(in sumd.dsl.commands)* | 1 | 2 | 45 | **47** |
| `to_term` *(in sumd.utils.prolog_core)* | 13 ⚠ | 9 | 30 | **39** |
| `_collect` *(in sumd.pipeline.RenderPipeline)* | 3 | 0 | 31 | **31** |
| `_render_call_graph` *(in sumd.sections.call_graph)* | 7 | 0 | 28 | **28** |
| `generate_map_toon` *(in sumd.extractor)* | 5 | 3 | 24 | **27** |
| `generate_project_logic` *(in sumd.extractor)* | 2 | 2 | 22 | **24** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/oqlos/sumd
# generated in 0.11s
# nodes: 234 | edges: 224 | modules: 33
# CC̄=3.7

HUBS[20]:
  test.print
    CC=0  in:84  out:0  total:84
  examples.mcp.mcp_client.run
    CC=11  in:1  out:53  total:54
  sumd.dsl.commands.create_builtin_registry
    CC=1  in:2  out:45  total:47
  sumd.utils.prolog_core.to_term
    CC=13  in:9  out:30  total:39
  sumd.pipeline.RenderPipeline._collect
    CC=3  in:0  out:31  total:31
  sumd.sections.call_graph._render_call_graph
    CC=7  in:0  out:28  total:28
  sumd.extractor.generate_map_toon
    CC=5  in:3  out:24  total:27
  sumd.extractor.generate_project_logic
    CC=2  in:2  out:22  total:24
  sumd.dsl.shell.DSLShell._handle_shell_command
    CC=14  in:0  out:24  total:24
  sumd.extractor.extract_pyproject
    CC=3  in:5  out:17  total:22
  sumd.sections.quality._render_quality_parsed
    CC=9  in:1  out:21  total:22
  sumd.parser.SUMDParser.parse_file
    CC=1  in:20  out:2  total:22
  sumd.cli.lint
    CC=6  in:0  out:21  total:21
  sumd.cli.map_cmd
    CC=7  in:0  out:20  total:20
  sumd.extractor._parse_doql_content
    CC=6  in:1  out:19  total:20
  sumd.sections.interfaces._render_interfaces_openapi
    CC=6  in:1  out:19  total:20
  sumd.sections.dependencies._render_deps_runtime
    CC=6  in:1  out:19  total:20
  sumd.cli.analyze
    CC=7  in:0  out:20  total:20
  sumd.extractor.extract_package_json
    CC=3  in:4  out:15  total:19
  sumd.extractor._extract_doql_workflows
    CC=5  in:1  out:18  total:19

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
  sumd.cli  [23 funcs]
    _api_scenario_template  CC=1  out:3
    _lint_classify_issues  CC=6  out:1
    _lint_collect_paths  CC=6  out:7
    _lint_print_result  CC=6  out:9
    _run_analyze_tool  CC=4  out:7
    _run_code2llm_formats  CC=5  out:7
    _run_tool_subprocess  CC=3  out:5
    _scaffold_crud_scenarios  CC=5  out:7
    _scaffold_from_openapi  CC=7  out:14
    _scaffold_generic  CC=1  out:3
  sumd.cli_doql  [6 funcs]
    _build_doql_spec  CC=3  out:4
    _detect_project_type  CC=8  out:4
    _generate_doql_less  CC=7  out:10
    _node_framework  CC=5  out:0
    _node_spec_from_package_json  CC=7  out:12
    _render_doql_boilerplate  CC=4  out:3
  sumd.cli_scan  [14 funcs]
    _detect_projects  CC=1  out:1
    _echo_scan_result  CC=2  out:4
    _ensure_venv  CC=4  out:7
    _export_sumd_json  CC=2  out:2
    _finalize_scan  CC=9  out:16
    _is_project_dir  CC=8  out:4
    _maybe_generate_doql  CC=7  out:9
    _maybe_generate_testql  CC=5  out:8
    _render_write_validate  CC=5  out:5
    _run_analysis_tools  CC=5  out:5
  sumd.cqrs.queries  [5 funcs]
    _handle_get_project_info  CC=3  out:11
    _handle_get_sumd_document  CC=3  out:4
    _handle_get_sumd_section  CC=4  out:7
    _handle_get_validation_results  CC=4  out:9
    _handle_list_sumd_sections  CC=3  out:4
  sumd.cqrs.sumd_aggregate  [1 funcs]
    create_from_file  CC=6  out:12
  sumd.dsl.commands  [7 funcs]
    _cmd_cat  CC=3  out:4
    _cmd_help  CC=2  out:3
    _cmd_read_file  CC=1  out:1
    _cmd_sumd_info  CC=3  out:3
    _cmd_sumd_map  CC=6  out:7
    _cmd_sumd_validate  CC=2  out:7
    create_builtin_registry  CC=1  out:45
  sumd.dsl.engine  [2 funcs]
    _builtin_print  CC=1  out:1
    execute_text  CC=3  out:5
  sumd.dsl.parser  [1 funcs]
    parse_dsl  CC=1  out:4
  sumd.dsl.parser_base  [1 funcs]
    _match  CC=2  out:2
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
  sumd.extractor  [57 funcs]
    _analyse_class_methods  CC=6  out:6
    _analyse_py_module  CC=2  out:6
    _analyse_py_top_classes  CC=5  out:8
    _analyse_py_top_funcs  CC=5  out:7
    _cc_estimate  CC=4  out:4
    _collect_map_files  CC=8  out:13
    _extract_deploy_facts  CC=2  out:3
    _extract_doql_facts  CC=2  out:6
    _extract_doql_interfaces  CC=3  out:9
    _extract_doql_workflows  CC=5  out:18
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
  sumd.parser  [3 funcs]
    parse_file  CC=1  out:2
    parse  CC=1  out:2
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
  sumd.toon_parser  [9 funcs]
    _parse_generic_block  CC=7  out:9
    _parse_toon_block_api  CC=6  out:4
    _parse_toon_block_assert  CC=7  out:9
    _parse_toon_block_config  CC=9  out:8
    _parse_toon_block_gui  CC=1  out:1
    _parse_toon_block_navigate  CC=7  out:5
    _parse_toon_block_performance  CC=1  out:1
    _parse_toon_file  CC=4  out:16
    extract_testql_scenarios  CC=7  out:12
  sumd.utils.prolog_core  [12 funcs]
    add_fact  CC=2  out:4
    parse_and_load  CC=7  out:17
    _resolve  CC=12  out:15
    query  CC=5  out:8
    deep_resolve  CC=3  out:4
    extend_subst  CC=2  out:2
    is_variable  CC=6  out:5
    occurs_check  CC=4  out:4
    rename_variables  CC=2  out:8
    resolve_val  CC=3  out:1
  sumd.validator  [10 funcs]
    _check_empty_links  CC=2  out:1
    _check_h1  CC=3  out:2
    _check_metadata_fields  CC=9  out:7
    _check_required_sections  CC=7  out:6
    _check_unclosed_fences  CC=4  out:2
    _validate_markpact_meta  CC=5  out:9
    validate_codeblocks  CC=11  out:17
    validate_markdown  CC=1  out:6
    validate_project_architecture  CC=8  out:15
    validate_sumd_file  CC=4  out:8
  sumd_logic_validator.sumd_logic_validator.cli  [3 funcs]
    get_engine  CC=4  out:9
    query  CC=6  out:14
    shell  CC=10  out:16
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
  sumd.toon_parser._parse_toon_block_performance → sumd.toon_parser._parse_generic_block
  sumd.toon_parser._parse_toon_block_gui → sumd.toon_parser._parse_generic_block
  sumd.toon_parser._parse_toon_file → sumd.dsl.parser_base.DSLParserBase._match
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_config
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_api
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_assert
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_performance
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_navigate
  sumd.toon_parser.extract_testql_scenarios → sumd.toon_parser._parse_toon_file
  sumd.extractor.extract_pyproject → sumd.extractor._read_toml
  sumd.extractor.extract_taskfile → sumd.extractor._first_task_cmd
  sumd.extractor._parse_doql_content → sumd.extractor._parse_doql_interfaces
  sumd.extractor._parse_doql_content → sumd.extractor._parse_doql_entities
  sumd.extractor._parse_doql_content → sumd.extractor._parse_doql_workflows
  sumd.extractor.extract_doql → sumd.extractor._parse_doql_content
  sumd.extractor.extract_dockerfile → sumd.extractor._parse_dockerfile_line
  sumd.extractor._analyse_py_top_funcs → sumd.extractor._fan_out
  sumd.extractor._analyse_py_top_funcs → sumd.extractor._cc_estimate
  sumd.extractor._analyse_class_methods → sumd.extractor._fan_out
  sumd.extractor._analyse_class_methods → sumd.extractor._cc_estimate
  sumd.extractor._analyse_py_top_classes → sumd.extractor._analyse_class_methods
  sumd.extractor._analyse_py_module → sumd.extractor._try_radon_cc
  sumd.extractor._analyse_py_module → sumd.extractor._analyse_py_top_funcs
  sumd.extractor._analyse_py_module → sumd.extractor._analyse_py_top_classes
  sumd.extractor._path_matches_pattern → sumd.extractor._match_regular_pattern
  sumd.extractor._path_matches_pattern → sumd.extractor._match_dir_pattern
  sumd.extractor._path_matches_pattern → sumd.extractor._match_absolute_pattern
  sumd.extractor._path_matches_pattern → sumd.extractor._match_recursive_pattern
  sumd.extractor._is_path_ignored → sumd.extractor._path_matches_pattern
  sumd.extractor._collect_map_files → sumd.extractor._parse_ignore_file
  sumd.extractor._collect_map_files → sumd.extractor._is_map_ignored_path
  sumd.extractor._collect_map_files → sumd.extractor._is_path_ignored
  sumd.extractor._collect_map_files → sumd.extractor._lang_of
  sumd.extractor._render_map_detail → sumd.extractor._analyse_py_module
  sumd.extractor.generate_map_toon → sumd.extractor._collect_map_files
  sumd.extractor.generate_map_toon → sumd.extractor._render_map_detail
  sumd.extractor.generate_map_toon → sumd.extractor._map_cc_stats
  sumd.extractor._facts_project_metadata → sumd.extractor.extract_pyproject
  sumd.extractor._facts_project_metadata → sumd.extractor.extract_package_json
  sumd.extractor._facts_project_files → sumd.extractor._collect_map_files
  sumd.extractor._facts_python_analysis → sumd.extractor._collect_map_files
  sumd.extractor._facts_python_analysis → sumd.extractor._render_map_detail
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (2)

**`CLI Command Tests`**

**`sumd-cli.testql.toon.yaml — CLI command and pipeline validation`**

### Integration (1)

**`Auto-generated from Python Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/oqlos/sumd
# generated in 0.11s
# nodes: 234 | edges: 224 | modules: 33
# CC̄=3.7

HUBS[20]:
  test.print
    CC=0  in:84  out:0  total:84
  examples.mcp.mcp_client.run
    CC=11  in:1  out:53  total:54
  sumd.dsl.commands.create_builtin_registry
    CC=1  in:2  out:45  total:47
  sumd.utils.prolog_core.to_term
    CC=13  in:9  out:30  total:39
  sumd.pipeline.RenderPipeline._collect
    CC=3  in:0  out:31  total:31
  sumd.sections.call_graph._render_call_graph
    CC=7  in:0  out:28  total:28
  sumd.extractor.generate_map_toon
    CC=5  in:3  out:24  total:27
  sumd.extractor.generate_project_logic
    CC=2  in:2  out:22  total:24
  sumd.dsl.shell.DSLShell._handle_shell_command
    CC=14  in:0  out:24  total:24
  sumd.extractor.extract_pyproject
    CC=3  in:5  out:17  total:22
  sumd.sections.quality._render_quality_parsed
    CC=9  in:1  out:21  total:22
  sumd.parser.SUMDParser.parse_file
    CC=1  in:20  out:2  total:22
  sumd.cli.lint
    CC=6  in:0  out:21  total:21
  sumd.cli.map_cmd
    CC=7  in:0  out:20  total:20
  sumd.extractor._parse_doql_content
    CC=6  in:1  out:19  total:20
  sumd.sections.interfaces._render_interfaces_openapi
    CC=6  in:1  out:19  total:20
  sumd.sections.dependencies._render_deps_runtime
    CC=6  in:1  out:19  total:20
  sumd.cli.analyze
    CC=7  in:0  out:20  total:20
  sumd.extractor.extract_package_json
    CC=3  in:4  out:15  total:19
  sumd.extractor._extract_doql_workflows
    CC=5  in:1  out:18  total:19

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
  sumd.cli  [23 funcs]
    _api_scenario_template  CC=1  out:3
    _lint_classify_issues  CC=6  out:1
    _lint_collect_paths  CC=6  out:7
    _lint_print_result  CC=6  out:9
    _run_analyze_tool  CC=4  out:7
    _run_code2llm_formats  CC=5  out:7
    _run_tool_subprocess  CC=3  out:5
    _scaffold_crud_scenarios  CC=5  out:7
    _scaffold_from_openapi  CC=7  out:14
    _scaffold_generic  CC=1  out:3
  sumd.cli_doql  [6 funcs]
    _build_doql_spec  CC=3  out:4
    _detect_project_type  CC=8  out:4
    _generate_doql_less  CC=7  out:10
    _node_framework  CC=5  out:0
    _node_spec_from_package_json  CC=7  out:12
    _render_doql_boilerplate  CC=4  out:3
  sumd.cli_scan  [14 funcs]
    _detect_projects  CC=1  out:1
    _echo_scan_result  CC=2  out:4
    _ensure_venv  CC=4  out:7
    _export_sumd_json  CC=2  out:2
    _finalize_scan  CC=9  out:16
    _is_project_dir  CC=8  out:4
    _maybe_generate_doql  CC=7  out:9
    _maybe_generate_testql  CC=5  out:8
    _render_write_validate  CC=5  out:5
    _run_analysis_tools  CC=5  out:5
  sumd.cqrs.queries  [5 funcs]
    _handle_get_project_info  CC=3  out:11
    _handle_get_sumd_document  CC=3  out:4
    _handle_get_sumd_section  CC=4  out:7
    _handle_get_validation_results  CC=4  out:9
    _handle_list_sumd_sections  CC=3  out:4
  sumd.cqrs.sumd_aggregate  [1 funcs]
    create_from_file  CC=6  out:12
  sumd.dsl.commands  [7 funcs]
    _cmd_cat  CC=3  out:4
    _cmd_help  CC=2  out:3
    _cmd_read_file  CC=1  out:1
    _cmd_sumd_info  CC=3  out:3
    _cmd_sumd_map  CC=6  out:7
    _cmd_sumd_validate  CC=2  out:7
    create_builtin_registry  CC=1  out:45
  sumd.dsl.engine  [2 funcs]
    _builtin_print  CC=1  out:1
    execute_text  CC=3  out:5
  sumd.dsl.parser  [1 funcs]
    parse_dsl  CC=1  out:4
  sumd.dsl.parser_base  [1 funcs]
    _match  CC=2  out:2
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
  sumd.extractor  [57 funcs]
    _analyse_class_methods  CC=6  out:6
    _analyse_py_module  CC=2  out:6
    _analyse_py_top_classes  CC=5  out:8
    _analyse_py_top_funcs  CC=5  out:7
    _cc_estimate  CC=4  out:4
    _collect_map_files  CC=8  out:13
    _extract_deploy_facts  CC=2  out:3
    _extract_doql_facts  CC=2  out:6
    _extract_doql_interfaces  CC=3  out:9
    _extract_doql_workflows  CC=5  out:18
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
  sumd.parser  [3 funcs]
    parse_file  CC=1  out:2
    parse  CC=1  out:2
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
  sumd.toon_parser  [9 funcs]
    _parse_generic_block  CC=7  out:9
    _parse_toon_block_api  CC=6  out:4
    _parse_toon_block_assert  CC=7  out:9
    _parse_toon_block_config  CC=9  out:8
    _parse_toon_block_gui  CC=1  out:1
    _parse_toon_block_navigate  CC=7  out:5
    _parse_toon_block_performance  CC=1  out:1
    _parse_toon_file  CC=4  out:16
    extract_testql_scenarios  CC=7  out:12
  sumd.utils.prolog_core  [12 funcs]
    add_fact  CC=2  out:4
    parse_and_load  CC=7  out:17
    _resolve  CC=12  out:15
    query  CC=5  out:8
    deep_resolve  CC=3  out:4
    extend_subst  CC=2  out:2
    is_variable  CC=6  out:5
    occurs_check  CC=4  out:4
    rename_variables  CC=2  out:8
    resolve_val  CC=3  out:1
  sumd.validator  [10 funcs]
    _check_empty_links  CC=2  out:1
    _check_h1  CC=3  out:2
    _check_metadata_fields  CC=9  out:7
    _check_required_sections  CC=7  out:6
    _check_unclosed_fences  CC=4  out:2
    _validate_markpact_meta  CC=5  out:9
    validate_codeblocks  CC=11  out:17
    validate_markdown  CC=1  out:6
    validate_project_architecture  CC=8  out:15
    validate_sumd_file  CC=4  out:8
  sumd_logic_validator.sumd_logic_validator.cli  [3 funcs]
    get_engine  CC=4  out:9
    query  CC=6  out:14
    shell  CC=10  out:16
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
  sumd.toon_parser._parse_toon_block_performance → sumd.toon_parser._parse_generic_block
  sumd.toon_parser._parse_toon_block_gui → sumd.toon_parser._parse_generic_block
  sumd.toon_parser._parse_toon_file → sumd.dsl.parser_base.DSLParserBase._match
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_config
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_api
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_assert
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_performance
  sumd.toon_parser._parse_toon_file → sumd.toon_parser._parse_toon_block_navigate
  sumd.toon_parser.extract_testql_scenarios → sumd.toon_parser._parse_toon_file
  sumd.extractor.extract_pyproject → sumd.extractor._read_toml
  sumd.extractor.extract_taskfile → sumd.extractor._first_task_cmd
  sumd.extractor._parse_doql_content → sumd.extractor._parse_doql_interfaces
  sumd.extractor._parse_doql_content → sumd.extractor._parse_doql_entities
  sumd.extractor._parse_doql_content → sumd.extractor._parse_doql_workflows
  sumd.extractor.extract_doql → sumd.extractor._parse_doql_content
  sumd.extractor.extract_dockerfile → sumd.extractor._parse_dockerfile_line
  sumd.extractor._analyse_py_top_funcs → sumd.extractor._fan_out
  sumd.extractor._analyse_py_top_funcs → sumd.extractor._cc_estimate
  sumd.extractor._analyse_class_methods → sumd.extractor._fan_out
  sumd.extractor._analyse_class_methods → sumd.extractor._cc_estimate
  sumd.extractor._analyse_py_top_classes → sumd.extractor._analyse_class_methods
  sumd.extractor._analyse_py_module → sumd.extractor._try_radon_cc
  sumd.extractor._analyse_py_module → sumd.extractor._analyse_py_top_funcs
  sumd.extractor._analyse_py_module → sumd.extractor._analyse_py_top_classes
  sumd.extractor._path_matches_pattern → sumd.extractor._match_regular_pattern
  sumd.extractor._path_matches_pattern → sumd.extractor._match_dir_pattern
  sumd.extractor._path_matches_pattern → sumd.extractor._match_absolute_pattern
  sumd.extractor._path_matches_pattern → sumd.extractor._match_recursive_pattern
  sumd.extractor._is_path_ignored → sumd.extractor._path_matches_pattern
  sumd.extractor._collect_map_files → sumd.extractor._parse_ignore_file
  sumd.extractor._collect_map_files → sumd.extractor._is_map_ignored_path
  sumd.extractor._collect_map_files → sumd.extractor._is_path_ignored
  sumd.extractor._collect_map_files → sumd.extractor._lang_of
  sumd.extractor._render_map_detail → sumd.extractor._analyse_py_module
  sumd.extractor.generate_map_toon → sumd.extractor._collect_map_files
  sumd.extractor.generate_map_toon → sumd.extractor._render_map_detail
  sumd.extractor.generate_map_toon → sumd.extractor._map_cc_stats
  sumd.extractor._facts_project_metadata → sumd.extractor.extract_pyproject
  sumd.extractor._facts_project_metadata → sumd.extractor.extract_package_json
  sumd.extractor._facts_project_files → sumd.extractor._collect_map_files
  sumd.extractor._facts_python_analysis → sumd.extractor._collect_map_files
  sumd.extractor._facts_python_analysis → sumd.extractor._render_map_detail
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 75f 16700L | python:65,shell:6,perl:4 | 2026-05-22
# CC̄=3.7 | critical:0/543 | dups:0 | cycles:0

HEALTH[0]: ok

REFACTOR[0]: none needed

PIPELINES[308]:
  [1] Src [main]: main → ask → build_context → parse_file
      PURITY: 100% pure
  [2] Src [main]: main → ask → parse_file
      PURITY: 100% pure
  [3] Src [main]: main → run
      PURITY: 100% pure
  [4] Src [parse]: parse
      PURITY: 100% pure
  [5] Src [_parse_header]: _parse_header
      PURITY: 100% pure

LAYERS:
  sumd_logic_validator/           CC̄=4.6    ←in:0  →out:0
  │ !! rules.pl                  1234L  0C    0m  CC=0.0    ←0
  │ !! rules.pl                  1234L  0C    0m  CC=0.0    ←0
  │ cli                        114L  0C    5m  CC=10     ←0
  │ engine                      39L  0C    0m  CC=0.0    ←0
  │ main                         4L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │
  sumd/                           CC̄=3.7    ←in:17  →out:4
  │ !! extractor                 1344L  0C   63m  CC=10     ←8
  │ !! cli                       1212L  0C   29m  CC=14     ←0
  │ !! mcp_server                 714L  0C   18m  CC=5      ←0
  │ !! commands                   649L  2C   30m  CC=9      ←1
  │ !! engine                     526L  2C   40m  CC=9      ←0
  │ !! schema_commands            517L  2C   33m  CC=10     ←0
  │ pipeline                   451L  1C   16m  CC=7      ←0
  │ nlp                        447L  3C   21m  CC=7      ←0
  │ cli_doql                   439L  0C    6m  CC=8      ←1
  │ prolog_core                432L  6C   32m  CC=14     ←0
  │ queries                    419L  13C   17m  CC=10     ←0
  │ cli_scan                   392L  0C   14m  CC=10     ←1
  │ validator                  386L  1C   16m  CC=11     ←5
  │ shell                      359L  2C   14m  CC=14     ←0
  │ schema                     345L  14C    1m  CC=1      ←0
  │ sumd_aggregate             344L  3C   18m  CC=6      ←0
  │ commands                   265L  12C    8m  CC=9      ←0
  │ aggregates                 220L  6C   23m  CC=4      ←0
  │ parser_primary             207L  1C   10m  CC=7      ←0
  │ parser                     187L  1C    9m  CC=9      ←10
  │ events                     184L  8C    8m  CC=7      ←0
  │ toon_parser                176L  0C    9m  CC=9      ←2
  │ parser                     171L  1C   11m  CC=6      ←2
  │ architecture               170L  1C    9m  CC=6      ←0
  │ interfaces                 157L  1C    8m  CC=7      ←0
  │ call_graph                 156L  1C    7m  CC=8      ←0
  │ lexer                      132L  3C    2m  CC=7      ←0
  │ parser_expr                115L  1C    6m  CC=4      ←0
  │ deployment                 110L  1C    5m  CC=8      ←0
  │ __init__                   106L  0C    0m  CC=0.0    ←0
  │ dependencies                97L  1C    4m  CC=6      ←0
  │ base                        94L  2C    2m  CC=1      ←0
  │ workflows                   86L  1C    4m  CC=6      ←0
  │ quality                     81L  1C    3m  CC=9      ←0
  │ api_stubs                   76L  1C    2m  CC=11     ←0
  │ extras                      72L  1C    4m  CC=7      ←0
  │ environment                 72L  1C    4m  CC=9      ←0
  │ parser_base                 69L  1C    9m  CC=5      ←1
  │ refactor_analysis           68L  1C    1m  CC=3      ←0
  │ code_analysis               68L  1C    3m  CC=9      ←0
  │ source_snippets             68L  1C    1m  CC=8      ←0
  │ swop                        68L  1C    2m  CC=9      ←0
  │ ast_nodes                   54L  2C    1m  CC=11     ←0
  │ metadata                    51L  1C    1m  CC=5      ←0
  │ models                      45L  3C    0m  CC=0.0    ←0
  │ configuration               43L  1C    1m  CC=1      ←0
  │ rules.pl                    41L  0C    0m  CC=0.0    ←0
  │ prolog_engine               39L  0C    0m  CC=0.0    ←0
  │ __init__                    35L  0C    0m  CC=0.0    ←0
  │ renderer                    29L  0C    1m  CC=1      ←0
  │ render                      25L  0C    1m  CC=1      ←0
  │ should_render               25L  0C    2m  CC=1      ←0
  │ __init__                    18L  0C    0m  CC=0.0    ←0
  │ context_mixin               17L  1C    2m  CC=1      ←0
  │ generator                   15L  0C    0m  CC=0.0    ←0
  │ __init__                    14L  0C    0m  CC=0.0    ←0
  │ __init__                    12L  0C    0m  CC=0.0    ←0
  │ __main__                     5L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ project.sh                  55L  0C    0m  CC=0.0    ←0
  │ print_errors                 6L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  .planfile/                      CC̄=0.0    ←in:0  →out:0
  │ setup-autopilot-host.sh     13L  0C    0m  CC=0.0    ←0
  │ run-autonomous.sh            6L  0C    0m  CC=0.0    ←0
  │ shell-env.sh                 5L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ bootstrap.sh                69L  0C    0m  CC=0.0    ←0
  │
  project/                        CC̄=0.0    ←in:0  →out:0
  │ !! logic.pl                  1195L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                  sumd   sumd.dsl  sumd.cqrs
       sumd         ──          4        ←10  hub
   sumd.dsl          7         ──           
  sumd.cqrs         10                    ──  !! fan-out
  CYCLES: none
  HUB: sumd/ (fan-in=17)
  SMELL: sumd.cqrs/ fan-out=10 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 2 groups | 67f 13061L | 2026-05-22

SUMMARY:
  files_scanned: 67
  total_lines:   13061
  dup_groups:    2
  dup_fragments: 4
  saved_lines:   8
  scan_ms:       16777

HOTSPOTS[3] (files with most duplication):
  sumd/toon_parser.py  dup=10L  groups=1  frags=2  (0.1%)
  sumd/cli.py  dup=3L  groups=1  frags=1  (0.0%)
  sumd_logic_validator/sumd_logic_validator/cli.py  dup=3L  groups=1  frags=1  (0.0%)

DUPLICATES[2] (ranked by impact):
  [b10c3c5641fc272f]   STRU  _parse_toon_block_performance  L=5 N=2 saved=5 sim=1.00
      sumd/toon_parser.py:91-95  (_parse_toon_block_performance)
      sumd/toon_parser.py:114-118  (_parse_toon_block_gui)
  [aaae754bdb04529d]   STRU  cli  L=3 N=2 saved=3 sim=1.00
      sumd/cli.py:50-52  (cli)
      sumd_logic_validator/sumd_logic_validator/cli.py:29-31  (main)

REFACTOR[2] (ranked by priority):
  [1] ○ extract_function   → sumd/utils/_parse_toon_block_performance.py
      WHY: 2 occurrences of 5-line block across 1 files — saves 5 lines
      FILES: sumd/toon_parser.py
  [2] ○ extract_function   → utils/cli.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: sumd/cli.py, sumd_logic_validator/sumd_logic_validator/cli.py

DEPENDENCY_RISK[1] (duplicates spanning multiple packages):
  cli  packages=2  files=2
      sumd/cli.py
      sumd_logic_validator/sumd_logic_validator/cli.py

EFFORT_ESTIMATE (total ≈ 0.4h):
  easy   _parse_toon_block_performance       saved=5L  ~10min
  easy   cli                                 saved=3L  ~12min

METRICS-TARGET:
  dup_groups:  2 → 0
  saved_lines: 8 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 542 func | 53f | 2026-05-22
# generated in 0.00s

NEXT[3] (ranked by impact):
  [1] !! SPLIT           sumd/cli.py
      WHY: 1212L, 0 classes, max CC=14
      EFFORT: ~4h  IMPACT: 16968

  [2] !! SPLIT           deps.json
      WHY: 6478L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0

  [3] !! SPLIT           sumd_logic_validator/sumd_logic_validator/logic/rules.pl
      WHY: 1234L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[3]:
  ⚠ Splitting deps.json may break 0 import paths
  ⚠ Splitting sumd_logic_validator/sumd_logic_validator/logic/rules.pl may break 0 import paths
  ⚠ Splitting sumd/cli.py may break 29 import paths

METRICS-TARGET:
  CC̄:          3.7 → ≤2.6
  max-CC:      14 → ≤7
  god-modules: 10 → 0
  high-CC(≥15): 0 → ≤0
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
  prev CC̄=3.6 → now CC̄=3.7
```

### Validation (`project/validation.toon.yaml`)

```toon markpact:analysis path=project/validation.toon.yaml
# vallm batch | 211f | 114✓ 6⚠ 13✗ | 2026-05-22

SUMMARY:
  scanned: 211  passed: 114 (54.0%)  warnings: 6  errors: 13  unsupported: 81

WARNINGS[6]{path,score}:
  /home/tom/github/oqlos/sumd/project/logic.pl,0.78
    issues[1]{rule,severity,message,line}:
      syntax.unsupported,warning,Could not parse perl: maximum recursion depth exceeded,
  /home/tom/github/oqlos/sumd/sumd_logic_validator/logic/rules.pl,0.78
    issues[1]{rule,severity,message,line}:
      syntax.unsupported,warning,Could not parse perl: maximum recursion depth exceeded,
  /home/tom/github/oqlos/sumd/sumd_logic_validator/sumd_logic_validator/logic/rules.pl,0.78
    issues[1]{rule,severity,message,line}:
      syntax.unsupported,warning,Could not parse perl: maximum recursion depth exceeded,
  /home/tom/github/oqlos/sumd/sumd/dsl/commands.py,0.97
    issues[1]{rule,severity,message,line}:
      complexity.lizard_length,warning,create_builtin_registry: 177 lines exceeds limit 100,104
  /home/tom/github/oqlos/sumd/sumd/dsl/nlp.py,0.97
    issues[1]{rule,severity,message,line}:
      complexity.lizard_length,warning,_initialize_default_intents: 106 lines exceeds limit 100,32
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
  /home/tom/github/oqlos/sumd/tests/test_cli.py,0.96
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,7
  /home/tom/github/oqlos/sumd/tests/test_mcp_server.py,0.96
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,8
  /home/tom/github/oqlos/sumd/tests/test_mcp_cqrs_dsl.py,0.97
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'pytest' not found,3
  /home/tom/github/oqlos/sumd/sumd/cli.py,0.98
    issues[2]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'toml' not found,185
      python.import.resolvable,error,Module 'toml' not found,123

UNSUPPORTED[5]{bucket,count}:
  *.md,25
  Dockerfile*,1
  *.txt,5
  *.yml,6
  other,44
```

## Intent

SUMD - Structured Unified Markdown Descriptor for AI-aware project documentation
