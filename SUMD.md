# SUMD

SUMD - Structured Unified Markdown Descriptor for AI-aware project documentation

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [SWOP](#swop)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Quality Pipeline (`pyqual.yaml`)](#quality-pipeline-pyqualyaml)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Source Map](#source-map)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `sumd`
- **version**: `0.3.51`
- **python_requires**: `>=3.10`
- **license**: {'text': 'Apache-2.0'}
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Taskfile.yml, Makefile, testql(3), app.doql.less, pyqual.yaml, goal.yaml, .env.example, src(13 mod), project/(3 analysis files), .swop/manifests/core/commands.yml, .swop/manifests/core/queries.yml, .swop/manifests/core/events.yml

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: sumd;
  version: 0.3.51;
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

## SWOP

SWOP - Bi-directional runtime reconciler and drift-aware state graph for full-stack systems.

### Context: `core`

#### Commands (`.swop/manifests/core/commands.yml`)

```yaml markpact:swop path=.swop/manifests/core/commands.yml
version: 1
context: core
commands:
  GenerateSUMD:
    module: sumd.cli
    fields:
      - name: project_dir
        type: Path
        required: true
      - name: profile
        type: str
        required: false
  ExtractSwop:
    module: sumd.extractor
    fields:
      - name: proj_dir
        type: Path
        required: true
```

#### Queries (`.swop/manifests/core/queries.yml`)

```yaml markpact:swop path=.swop/manifests/core/queries.yml
version: 1
context: core
queries:
  ListProjects:
    module: sumd.pipeline
    fields:
      - name: workspace
        type: Path
        required: true
      - name: max_depth
        type: int
        required: false
```

#### Events (`.swop/manifests/core/events.yml`)

```yaml markpact:swop path=.swop/manifests/core/events.yml
version: 1
context: core
events:
  SUMDGenerated:
    module: sumd.generator
    fields:
      - name: project_name
        type: str
        required: true
      - name: sections
        type: list
        required: true
```

## Interfaces

### CLI Entry Points

- `sumd`
- `sumr`
- `sumd-mcp`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -msumd
  timeout_ms, 10000

LOG[3]{message}:
  "Test CLI help command"
  "Test CLI version command"
  "Test CLI main workflow"
```

#### `testql-scenarios/generated-from-pytests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-from-pytests.testql.toon.yaml
# SCENARIO: Auto-generated from Python Tests
# TYPE: integration
# GENERATED: true

LOG[8]{message}:
  "Test: TestExtractEnv_test_captures_inline_comment"
  "Test: TestExtractRequirements_test_parses_requirements_txt"
  "Test: test_captures_inline_comment"
  "Test: test_parses_requirements_txt"
  "Test: TestExtractEnv_test_captures_inline_comment"
  "Test: TestExtractRequirements_test_parses_requirements_txt"
  "Test: test_captures_inline_comment"
  "Test: test_parses_requirements_txt"
```

#### `testql-scenarios/sumd-cli.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/sumd-cli.testql.toon.yaml
# SCENARIO: sumd-cli.testql.toon.yaml — CLI command and pipeline validation
# TYPE: cli
# GENERATED: false

# ── Configuration ──────────────────────────────────────
CONFIG[4]{key, value}:
  cli_command, python -m sumd
  timeout_ms, 15000
  test_mode, cli
  validate_output, true

# ── CLI Commands and Assertions ────────────────────────
ASSERT[5]{field, op, expected}:
  command_scan_status, ==, 0
  command_lint_status, ==, 0
  command_info_status, ==, 0
  command_export_status, ==, 0
  help_contains, ==, "SUMD - Structured Unified Markdown Descriptor"

# ── Navigation and GUI actions for DSL shell ───────────
# Even though this is a CLI command, we can represent DSL commands
# that are executed within the shell during this scenario.
GUI[4]{action, selector}:
  execute, "scan ."
  execute, "lint SUMD.md"
  execute, "info SUMD.md"
  execute, "export SUMD.md --format json"

PERFORMANCE[2]{metric, threshold}:
  execution_time_ms, 5000
  memory_peak_mb, 128
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

## Configuration

```yaml
project:
  name: sumd
  version: 0.3.51
  env: local
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

## Deployment

```bash markpact:run
pip install sumd

# development install
pip install -e .[dev]
```

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | `*(not set)*` | Required: OpenRouter API key (https://openrouter.ai/keys) |
| `LLM_MODEL` | `openrouter/qwen/qwen3-coder-next` | Model (default: openrouter/qwen/qwen3-coder-next) |
| `PFIX_AUTO_APPLY` | `true` | true = apply fixes without asking |
| `PFIX_AUTO_INSTALL_DEPS` | `true` | true = auto pip/uv install |
| `PFIX_AUTO_RESTART` | `false` | true = os.execv restart after fix |
| `PFIX_MAX_RETRIES` | `3` |  |
| `PFIX_DRY_RUN` | `false` |  |
| `PFIX_ENABLED` | `true` |  |
| `PFIX_GIT_COMMIT` | `false` | true = auto-commit fixes |
| `PFIX_GIT_PREFIX` | `pfix:` | commit message prefix |
| `PFIX_CREATE_BACKUPS` | `false` | false = disable .pfix_backups/ directory |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`statement`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `sumd/__init__.py:__version__`

## Makefile Targets

- `help` — Default target
- `install` — Installation
- `install-dev`
- `test` — Testing
- `test-cov`
- `lint` — Code quality
- `format`
- `clean` — Utilities
- `publish` — Release helpers
- `publish-confirm`
- `publish-test`
- `version`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# sumd | 94f 17173L | python:85,shell:7,less:2 | 2026-05-21
# stats: 313 func | 163 cls | 94 mod | CC̄=4.3 | critical:14 | cycles:0
# alerts[5]: CC scan=14; CC _split_body_terms=14; CC to_term=13; CC run=11; CC main=11
# hotspots[5]: cqrs_command fan=19; scan fan=18; scaffold fan=18; generate fan=15; to_term fan=15
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[94]:
  app.doql.less,255
  examples/app.doql.less,60
  examples/basic/demo.sh,50
  examples/llm/anthropic_example.py,61
  examples/llm/llm_cli_example.sh,37
  examples/llm/ollama_example.sh,38
  examples/llm/openai_example.py,89
  examples/mcp/mcp_client.py,139
  print_errors.py,7
  project.sh,55
  scripts/bootstrap.sh,70
  scripts/install_testql_autoloop.sh,157
  sumd/__init__.py,36
  sumd/__main__.py,6
  sumd/cli.py,1213
  sumd/cli_doql.py,440
  sumd/cli_scan.py,393
  sumd/cqrs/__init__.py,19
  sumd/cqrs/aggregates.py,221
  sumd/cqrs/commands.py,266
  sumd/cqrs/events.py,185
  sumd/cqrs/queries.py,420
  sumd/cqrs/sumd_aggregate.py,345
  sumd/dsl/__init__.py,15
  sumd/dsl/ast_nodes.py,55
  sumd/dsl/commands.py,650
  sumd/dsl/context_mixin.py,18
  sumd/dsl/engine.py,538
  sumd/dsl/lexer.py,133
  sumd/dsl/nlp.py,448
  sumd/dsl/parser.py,172
  sumd/dsl/parser_base.py,70
  sumd/dsl/parser_expr.py,116
  sumd/dsl/parser_primary.py,208
  sumd/dsl/schema.py,346
  sumd/dsl/schema_commands.py,518
  sumd/dsl/shell.py,360
  sumd/extractor.py,1345
  sumd/generator.py,16
  sumd/mcp_server.py,715
  sumd/models.py,46
  sumd/parser.py,188
  sumd/pipeline.py,452
  sumd/prolog_engine.py,40
  sumd/renderer.py,30
  sumd/sections/__init__.py,107
  sumd/sections/api_stubs.py,77
  sumd/sections/architecture.py,171
  sumd/sections/base.py,95
  sumd/sections/call_graph.py,157
  sumd/sections/code_analysis.py,69
  sumd/sections/configuration.py,44
  sumd/sections/dependencies.py,98
  sumd/sections/deployment.py,111
  sumd/sections/environment.py,73
  sumd/sections/extras.py,73
  sumd/sections/interfaces.py,158
  sumd/sections/metadata.py,52
  sumd/sections/quality.py,82
  sumd/sections/refactor_analysis.py,69
  sumd/sections/source_snippets.py,69
  sumd/sections/swop.py,69
  sumd/sections/test_contracts.py,78
  sumd/sections/utils/__init__.py,13
  sumd/sections/utils/render.py,26
  sumd/sections/utils/should_render.py,26
  sumd/sections/workflows.py,87
  sumd/toon_parser.py,177
  sumd/utils/__init__.py,2
  sumd/utils/prolog_core.py,433
  sumd/validator.py,384
  sumd_logic_validator/logic/__init__.py,2
  sumd_logic_validator/sumd_logic_validator/__init__.py,4
  sumd_logic_validator/sumd_logic_validator/cli.py,115
  sumd_logic_validator/sumd_logic_validator/engine.py,40
  sumd_logic_validator/sumd_logic_validator/logic/__init__.py,2
  sumd_logic_validator/sumd_logic_validator/main.py,5
  sumd_logic_validator/tests/__init__.py,1
  sumd_logic_validator/tests/test_engine.py,29
  test_gitignore.py,1
  test_ignore.py,1
  tests/test_architectural_logic.py,167
  tests/test_cli.py,348
  tests/test_cqrs_es.py,389
  tests/test_dogfood.py,148
  tests/test_dsl.py,470
  tests/test_extractor.py,313
  tests/test_mcp_cqrs_dsl.py,465
  tests/test_mcp_server.py,239
  tests/test_parser.py,145
  tests/test_pipeline.py,136
  tests/test_sections.py,298
  tests/test_statement.py,12
  tree.sh,2
D:
  examples/llm/anthropic_example.py:
    e: ask,main
    ask(sumd_path;question;model)
    main()
  examples/llm/openai_example.py:
    e: build_context,ask,main
    build_context(sumd_path)
    ask(sumd_path;question;model)
    main()
  examples/mcp/mcp_client.py:
    e: run,main
    run(sumd_file;single_tool;tool_args)
    main()
  print_errors.py:
  sumd/__init__.py:
  sumd/__main__.py:
  sumd/cli.py:
    e: cli,validate,export,info,generate,extract,scan,lint,_lint_classify_issues,_lint_collect_paths,_lint_print_result,_setup_tools_venv,_run_code2llm_formats,_run_tool_subprocess,_run_analyze_tool,analyze,_api_scenario_template,_scaffold_write,_scaffold_smoke_scenario,_scaffold_crud_scenarios,_scaffold_from_openapi,_scaffold_generic,scaffold,map_cmd,dsl,cqrs_command,nlp_command,main,main_sumr
    cli()
    validate(file)
    export(file;format;output)
    info(file)
    generate(file;format;output)
    extract(file;section)
    scan(workspace;export_json;report;fix;raw;analyze;tools;profile;depth;recursive;generate_doql;doql_sync;generate_testql;workspace_mode)
    lint(files;workspace;as_json;strict)
    _lint_classify_issues(r;strict)
    _lint_collect_paths(files;workspace)
    _lint_print_result(path;r;strict)
    _setup_tools_venv(venv_dir;tool_list;force)
    _run_code2llm_formats(bin_dir;project;project_output)
    _run_tool_subprocess(bin_dir;tool;cmd_args)
    _run_analyze_tool(tool;bin_dir;project;project_output)
    analyze(project;tools;force)
    _api_scenario_template(name;scenario_type;endpoints_block;base_path)
    _scaffold_write(path;content;force;generated;skipped)
    _scaffold_smoke_scenario(paths;base;out_dir;force;generated;skipped)
    _scaffold_crud_scenarios(groups;base;out_dir;force;generated;skipped)
    _scaffold_from_openapi(spec;out_dir;scenario_type;force;generated;skipped)
    _scaffold_generic(out_dir;force;generated;skipped)
    scaffold(project;output;force;scenario_type)
    map_cmd(project;output;force;stdout)
    dsl(directory;command;script;interactive)
    cqrs_command(directory;command_type;aggregate_id;data)
    nlp_command(text;directory;execute;verbose)
    main()
    main_sumr()
  sumd/cli_doql.py:
    e: _detect_project_type,_render_doql_boilerplate,_node_framework,_node_spec_from_package_json,_build_doql_spec,_generate_doql_less
    _detect_project_type(proj_dir)
    _render_doql_boilerplate(project_name;spec;extra_workflows)
    _node_framework(deps)
    _node_spec_from_package_json(pkg_json)
    _build_doql_spec(proj_dir;project_type)
    _generate_doql_less(proj_dir;project_name;version;force;project_type)
  sumd/cli_scan.py:
    e: _is_project_dir,_walk_projects,_detect_projects,_ensure_venv,_tool_bin,_run_one_tool,_run_analysis_tools,_export_sumd_json,_render_write_validate,_echo_scan_result,_maybe_generate_doql,_maybe_generate_testql,_finalize_scan,_scan_one_project
    _is_project_dir(d)
    _walk_projects(path;projects;max_depth;depth)
    _detect_projects(workspace;max_depth)
    _ensure_venv(tools_dir;venv_dir;tool_list)
    _tool_bin(bin_dir;name)
    _run_one_tool(tool;bin_dir;proj_dir;project_output)
    _run_analysis_tools(proj_dir;tool_list;skip_tools)
    _export_sumd_json(proj_dir;doc)
    _render_write_validate(proj_dir;sumd_path;raw;profile)
    _echo_scan_result(proj_dir;doc;sources;cb_warnings)
    _maybe_generate_doql(proj_dir;fix)
    _maybe_generate_testql(proj_dir)
    _finalize_scan(proj_dir;doc;sources;cb_warnings;export_json;run_analyze;tool_list;doql_sync;sumd_path)
    _scan_one_project(proj_dir;fix;raw;export_json;run_analyze;tool_list;parser_inst;profile;generate_doql;doql_sync;generate_testql)
  sumd/cqrs/__init__.py:
  sumd/cqrs/aggregates.py:
    e: AggregateRoot,EntityState,Entity,ValueObject,Repository,EventSourcedRepository
    AggregateRoot: __init__(1),aggregate_id(0),version(0),uncommitted_events(0),set_event_store(1),apply_event(1),mark_events_as_committed(0),load_from_history(1),_when(1),commit(0),get_state(0)  # Base aggregate root for event sourcing.
    EntityState:  # Base entity state for aggregates.
    Entity: __init__(1),id(0),domain_events(0),add_domain_event(1),clear_domain_events(0),get_state(0)  # Base entity for domain objects.
    ValueObject: __eq__(1),__hash__(0),get_state(0)  # Base value object.
    Repository: get_by_id(1),save(1),delete(1)  # Base repository for aggregates.
    EventSourcedRepository: __init__(2),get_by_id(1),save(1),delete(1),clear_cache(0)  # Event-sourced repository implementation.
  sumd/cqrs/commands.py:
    e: Command,CommandHandler,CommandBus,CreateSumdDocument,UpdateSumdDocument,AddSumdSection,RemoveSumdSection,ValidateSumdDocument,ScanProject,GenerateMap,ExecuteDslCommand,SumdCommandHandler
    Command:  # Base command class for CQRS pattern.
    CommandHandler: handle(1),can_handle(1)  # Base command handler interface.
    CommandBus: __init__(1),register_handler(2),dispatch(1)  # Command bus for dispatching commands to appropriate handlers
    CreateSumdDocument:  # Command to create a new SUMD document.
    UpdateSumdDocument:  # Command to update an existing SUMD document.
    AddSumdSection:  # Command to add a section to a SUMD document.
    RemoveSumdSection:  # Command to remove a section from a SUMD document.
    ValidateSumdDocument:  # Command to validate a SUMD document.
    ScanProject:  # Command to scan a project and generate SUMD.
    GenerateMap:  # Command to generate project map.
    ExecuteDslCommand:  # Command to execute DSL command.
    SumdCommandHandler: __init__(1),can_handle(1),handle(1)  # Base handler for SUMD commands.
  sumd/cqrs/events.py:
    e: Event,EventStore,SumdDocumentCreated,SumdDocumentUpdated,SumdSectionAdded,SumdSectionRemoved,SumdDocumentValidated,SumdCommandExecuted
    Event: to_dict(0),from_dict(2)  # Base event class for event sourcing.
    EventStore: __init__(1),save_event(1),get_events(2),get_all_events(0),_persist_event(1),_load_events(0)  # In-memory event store with optional file persistence.
    SumdDocumentCreated:  # Event fired when a SUMD document is created.
    SumdDocumentUpdated:  # Event fired when a SUMD document is updated.
    SumdSectionAdded:  # Event fired when a section is added to SUMD document.
    SumdSectionRemoved:  # Event fired when a section is removed from SUMD document.
    SumdDocumentValidated:  # Event fired when a SUMD document is validated.
    SumdCommandExecuted:  # Event fired when a SUMD command is executed.
  sumd/cqrs/queries.py:
    e: Query,QueryHandler,QueryBus,GetSumdDocument,ListSumdSections,GetSumdSection,GetProjectInfo,GetEventHistory,GetAllEvents,SearchDocuments,GetValidationResults,ExecuteDslQuery,SumdQueryHandler
    Query:  # Base query class for CQRS pattern.
    QueryHandler: handle(1),can_handle(1)  # Base query handler interface.
    QueryBus: __init__(1),register_handler(2),dispatch(1)  # Query bus for dispatching queries to appropriate handlers.
    GetSumdDocument:  # Query to get a SUMD document.
    ListSumdSections:  # Query to list sections in a SUMD document.
    GetSumdSection:  # Query to get a specific section from a SUMD document.
    GetProjectInfo:  # Query to get project information.
    GetEventHistory:  # Query to get event history for an aggregate.
    GetAllEvents:  # Query to get all events from the event store.
    SearchDocuments:  # Query to search SUMD documents.
    GetValidationResults:  # Query to get validation results for a document.
    ExecuteDslQuery:  # Query to execute DSL query.
    SumdQueryHandler: __init__(1),can_handle(1),handle(1),_handle_get_sumd_document(1),_handle_list_sumd_sections(1),_handle_get_sumd_section(1),_handle_get_project_info(1),_handle_get_event_history(1),_handle_get_all_events(1),_handle_search_documents(1),_handle_get_validation_results(1),_handle_execute_dsl_query(1)  # Handler for SUMD queries.
  sumd/cqrs/sumd_aggregate.py:
    e: SumdSection,SumdDocumentState,SumdAggregate
    SumdSection: to_dict(0),from_dict(2)  # Represents a section in a SUMD document.
    SumdDocumentState:  # State of a SUMD document aggregate.
    SumdAggregate: __init__(1),state(0),_when(1),_when_document_created(1),_when_document_updated(1),_when_section_added(1),_when_section_removed(1),_when_document_validated(1),create_document(4),update_document(1),add_section(5),remove_section(1),validate_document(2),get_section(1),has_section(1),get_state(0),create_from_file(2)  # SUMD document aggregate root.
  sumd/dsl/__init__.py:
  sumd/dsl/ast_nodes.py:
    e: DSLExpressionType,DSLExpression
    DSLExpressionType:  # Types of DSL expressions.
    DSLExpression: __str__(0)  # Expression in DSL.
  sumd/dsl/commands.py:
    e: create_builtin_registry,_cmd_cat,_cmd_ls,_cmd_edit,_cmd_mkdir,_cmd_rm,_cmd_sumd_scan,_cmd_sumd_map,_cmd_sumd_validate,_cmd_sumd_info,_cmd_find,_cmd_grep,_cmd_echo,_cmd_pwd,_cmd_cd,_cmd_help,_cmd_clear,_cmd_set,_cmd_get,_cmd_unset,_cmd_vars,_cmd_exists,_cmd_read_file,DSLCommand,DSLCommandRegistry
    DSLCommand: __post_init__(0)  # DSL command definition.
    DSLCommandRegistry: __init__(0),register(1),get_command(1),list_commands(1),list_categories(0),get_help(1)  # Registry for DSL commands.
    create_builtin_registry()
    _cmd_cat(context;args)
    _cmd_ls(context;args)
    _cmd_edit(context;args)
    _cmd_mkdir(context;args)
    _cmd_rm(context;args)
    _cmd_sumd_scan(context;args)
    _cmd_sumd_map(context;args)
    _cmd_sumd_validate(context;args)
    _cmd_sumd_info(context;args)
    _cmd_find(context;args)
    _cmd_grep(context;args)
    _cmd_echo(context;args)
    _cmd_pwd(context;args)
    _cmd_cd(context;args)
    _cmd_help(context;args)
    _cmd_clear(context;args)
    _cmd_set(context;args)
    _cmd_get(context;args)
    _cmd_unset(context;args)
    _cmd_vars(context;args)
    _cmd_exists(context;args)
    _cmd_read_file(context;args)
  sumd/dsl/context_mixin.py:
    e: VariableMixin
    VariableMixin: set_variable(2),get_variable(1)  # Mixin providing set_variable / get_variable helpers.
  sumd/dsl/engine.py:
    e: DSLContext,DSLEngine
    DSLContext: __init__(1),register_function(2),get_function(1)  # Execution context for DSL expressions.
    DSLEngine: __init__(3),execute(2),execute_text(2),_is_natural_language(1),process_natural_language(1),get_suggestions(1),_build_dispatch_table(0),_execute_expression(2),_execute_assignment(2),_resolve_schema_call(3),_evaluate_args(2),_execute_command(2),_execute_function_call(2),_execute_property_access(2),_execute_comparison(2),_execute_logical(2),_execute_arithmetic(2),_execute_pipeline(2),_execute_list(2),_execute_dict(2),_execute_block(2),_execute_sumd_command(3),_call_function(3),_initialize_builtin_functions(0),_builtin_print(2),_builtin_len(2),_builtin_str(2),_builtin_int(2),_builtin_float(2),_builtin_bool(2),_builtin_type(2),_builtin_write_file(3),_builtin_list_files(2),_builtin_cwd(1),_builtin_cd(2),_builtin_help(1)  # Engine for executing DSL expressions.
  sumd/dsl/lexer.py:
    e: DSLTokenType,DSLToken,DSLLexer
    DSLTokenType:  # Token types for DSL parsing.
    DSLToken:  # Token in DSL.
    DSLLexer: __init__(1),tokenize(0)  # Lexer for tokenizing DSL expressions.
  sumd/dsl/nlp.py:
    e: NLPProcessor,NLPIntegration,SimpleNLPModel
    NLPProcessor: __init__(1),_initialize_default_intents(0),_initialize_default_entities(0),parse_natural_language(1),_text_matches_intent(2),_extract_entities(2),_extract_entity_value(2),_extract_command_fallback(1),_extract_entities_fallback(1),generate_dsl_command(2),suggest_commands(1)  # Natural Language Processor for DSL commands.
    NLPIntegration: __init__(1),process_natural_language(1),get_suggestions(1),add_custom_intent(1),add_custom_entity(1),get_available_intents(0),get_intent_examples(1)  # NLP integration for DSL engine.
    SimpleNLPModel: __init__(0),predict_intent(1),extract_entities(2)  # Simple NLP model implementation for basic functionality.
  sumd/dsl/parser.py:
    e: parse_dsl,DSLParser
    DSLParser: parse(0),_looks_like_command(0),_peek_next_type(0),_is_command_boundary(0),_collect_command_args(0),_build_pipeline_or_cmd(2),_try_parse_command(0),_parse_statement(0),_parse_pipeline(0),_parse_assignment(0)  # Parser for DSL expressions.
    parse_dsl(text)
  sumd/dsl/parser_base.py:
    e: DSLParserBase
    DSLParserBase: __init__(1),_is_at_end(0),_peek(0),_previous(0),_advance(0),_check(2),_check_next(2),_match(2),_consume(2)  # Base parser class with token traversal utilities.
  sumd/dsl/parser_expr.py:
    e: DSLExpressionParser
    DSLExpressionParser: _parse_logical_or(0),_parse_logical_and(0),_parse_comparison(0),_parse_arithmetic(0),_parse_term(0),_parse_factor(0)  # Expression parsing methods for math and logic operations.
  sumd/dsl/parser_primary.py:
    e: DSLPrimaryParser
    DSLPrimaryParser: _parse_paren_or_collection(0),_parse_identifier_command(1),_parse_identifier_forms(0),_parse_literal_value(0),_parse_primary(0),_parse_command(0),_parse_function_call(0),_parse_property_access(0),_parse_list(0),_parse_dict(0)  # Primary expression parsing methods for literals, identifiers
  sumd/dsl/schema.py:
    e: DSLDataType,DSLCommandType,DSLActionType,DSLParameter,DSLCommandSchema,DSLProjectSchema,DSLExpression,DSLStatement,DSLScript,NLPIntent,NLPEntity,NLPModel,DSLContext,DSLCommandResult
    DSLDataType:  # Supported data types in DSL.
    DSLCommandType:  # Supported command types in DSL.
    DSLActionType:  # Supported action types in DSL.
    DSLParameter:  # DSL parameter definition.
    DSLCommandSchema:  # DSL command schema definition.
    DSLProjectSchema:  # DSL project schema definition.
    DSLExpression:  # DSL expression model.
    DSLStatement:  # DSL statement model.
    DSLScript:  # DSL script model.
    NLPIntent:  # NLP intent model.
    NLPEntity:  # NLP entity model.
    NLPModel:  # NLP model configuration.
    DSLContext: register_function(2)  # DSL execution context model.
    DSLCommandResult:  # DSL command execution result.
  sumd/dsl/schema_commands.py:
    e: SchemaCommandRegistry,SchemaBasedCommands
    SchemaCommandRegistry: __init__(1),_register_commands(0),get_command(1),list_commands(1),validate_command_call(2),_validate_parameter_type(2),process_natural_language(1),get_suggestions(1)  # Registry for schema-based DSL commands.
    SchemaBasedCommands: __init__(2),execute_command(2),_execute_sumd_command(2),_execute_file_command(2),_execute_search_command(2),_execute_utility_command(2),_execute_nlp_command(2),_execute_schema_command(2),_cmd_sumd_scan(1),_cmd_sumd_validate(1),_cmd_sumd_info(1),_cmd_cat(1),_cmd_ls(1),_cmd_edit(1),_cmd_find(1),_cmd_grep(1),_cmd_echo(1),_cmd_pwd(1),_cmd_cd(1),_cmd_ask(1),_cmd_summarize(1),_cmd_analyze_sentiment(1),_cmd_schema_info(1),_cmd_list_commands(1),_cmd_command_help(1)  # Implementation of schema-based DSL commands.
  sumd/dsl/shell.py:
    e: main,DSLShell,DSLShellServer
    DSLShell: __init__(3),_setup_readline(0),_completer(2),_register_commands(0),run(0),_get_prompt(0),_handle_shell_command(1),_execute_line(1),execute_script(1),execute_command(1)  # Interactive shell for SUMD DSL.
    DSLShellServer: __init__(1),execute_dsl(2),get_shell_info(0)  # Server for DSL shell operations (for MCP integration).
    main()
  sumd/extractor.py:
    e: _read_toml,extract_pyproject,_first_task_cmd,extract_taskfile,_parse_openapi_endpoints,extract_openapi,_parse_doql_entities,_parse_doql_interfaces,_parse_doql_workflows,_parse_doql_content,extract_doql,extract_pyqual,extract_python_modules,extract_readme_title,extract_requirements,extract_makefile,extract_goal,extract_env,_parse_dockerfile_line,extract_dockerfile,extract_docker_compose,extract_package_json,_lang_of,_fan_out,_cc_estimate,_try_radon_cc,_analyse_py_top_funcs,_analyse_class_methods,_analyse_py_top_classes,_analyse_py_module,_parse_ignore_file,_match_dir_pattern,_match_absolute_pattern,_match_recursive_pattern,_match_regular_pattern,_path_matches_pattern,_is_path_ignored,_is_map_ignored_path,_collect_map_files,_render_map_detail,_map_cc_stats,_render_py_module_detail,generate_map_toon,_facts_project_metadata,_facts_project_files,_facts_python_analysis,_facts_dependencies,_facts_makefile,_facts_taskfile,_facts_env_variables,_facts_testql_scenarios,generate_project_logic,_extract_markpact_files,_extract_doql_interfaces,_extract_doql_workflows,_extract_doql_facts,_extract_deploy_facts,_extract_pyqual_gates,_extract_sumd_semantic_facts,required_tools_for_profile,extract_source_snippets,extract_swop,extract_project_analysis
    _read_toml(path)
    extract_pyproject(proj_dir)
    _first_task_cmd(cmds)
    extract_taskfile(proj_dir)
    _parse_openapi_endpoints(paths)
    extract_openapi(proj_dir)
    _parse_doql_entities(content)
    _parse_doql_interfaces(content)
    _parse_doql_workflows(content)
    _parse_doql_content(content)
    extract_doql(proj_dir)
    extract_pyqual(proj_dir)
    extract_python_modules(proj_dir;pkg_name)
    extract_readme_title(proj_dir)
    extract_requirements(proj_dir)
    extract_makefile(proj_dir)
    extract_goal(proj_dir)
    extract_env(proj_dir)
    _parse_dockerfile_line(line;parsed)
    extract_dockerfile(proj_dir)
    extract_docker_compose(proj_dir)
    extract_package_json(proj_dir)
    _lang_of(path)
    _fan_out(func_node)
    _cc_estimate(func_node)
    _try_radon_cc(src)
    _analyse_py_top_funcs(tree;radon_cc)
    _analyse_class_methods(node;radon_cc)
    _analyse_py_top_classes(tree;radon_cc)
    _analyse_py_module(path)
    _parse_ignore_file(ignore_path)
    _match_dir_pattern(path;path_str;dir_pattern)
    _match_absolute_pattern(path_str;pattern)
    _match_recursive_pattern(path_str;pattern)
    _match_regular_pattern(path;path_str;pattern)
    _path_matches_pattern(path;pattern)
    _is_path_ignored(path;proj_dir;ignore_patterns)
    _is_map_ignored_path(p)
    _collect_map_files(proj_dir)
    _render_map_detail(proj_dir;modules)
    _map_cc_stats(all_funcs)
    _render_py_module_detail(rel;info;a)
    generate_map_toon(proj_dir)
    _facts_project_metadata(proj_dir)
    _facts_project_files(proj_dir)
    _facts_python_analysis(proj_dir)
    _facts_dependencies(proj_dir)
    _facts_makefile(proj_dir)
    _facts_taskfile(proj_dir)
    _facts_env_variables(proj_dir)
    _facts_testql_scenarios(proj_dir)
    generate_project_logic(proj_dir)
    _extract_markpact_files(content)
    _extract_doql_interfaces(doql_content)
    _extract_doql_workflows(doql_content)
    _extract_doql_facts(proj_dir)
    _extract_deploy_facts(proj_dir)
    _extract_pyqual_gates(proj_dir)
    _extract_sumd_semantic_facts(proj_dir)
    required_tools_for_profile(profile)
    extract_source_snippets(proj_dir;pkg_name)
    extract_swop(proj_dir)
    extract_project_analysis(proj_dir;refactor)
  sumd/generator.py:
  sumd/mcp_server.py:
    e: _doc_to_dict,_resolve_path,list_tools,_tool_parse_sumd,_tool_validate_sumd,_tool_export_sumd,_tool_list_sections,_tool_get_section,_tool_info_sumd,_tool_generate_sumd,_tool_execute_command,_tool_execute_query,_tool_get_events,_tool_get_aggregate,_tool_execute_dsl,_tool_dsl_shell_info,call_tool,main
    _doc_to_dict(doc)
    _resolve_path(path)
    list_tools()
    _tool_parse_sumd(arguments)
    _tool_validate_sumd(arguments)
    _tool_export_sumd(arguments)
    _tool_list_sections(arguments)
    _tool_get_section(arguments)
    _tool_info_sumd(arguments)
    _tool_generate_sumd(arguments)
    _tool_execute_command(arguments)
    _tool_execute_query(arguments)
    _tool_get_events(arguments)
    _tool_get_aggregate(arguments)
    _tool_execute_dsl(arguments)
    _tool_dsl_shell_info(arguments)
    call_tool(name;arguments)
    main()
  sumd/models.py:
    e: SectionType,Section,SUMDDocument
    SectionType:  # SUMD section types.
    Section:  # Represents a SUMD section.
    SUMDDocument:  # Represents a parsed SUMD document.
  sumd/parser.py:
    e: parse,parse_file,validate,SUMDParser
    SUMDParser: __init__(0),parse(1),parse_file(1),_parse_header(1),_parse_sections(1),validate(1)  # Parser for SUMD markdown documents.
    parse(content)
    parse_file(path)
    validate(document)
  sumd/pipeline.py:
    e: _refresh_map_toon,_find_tools_bin_dir,_run_tool_if_present,_refresh_analysis_files,_collect_tool_sources,_doql_sources,_collect_pkg_sources,_collect_infra_sources,_collect_sources,_inject_toc,RenderPipeline
    RenderPipeline: __init__(2),_collect(0),_build_registered_sections(2),_render_legacy_sections(1),_assemble(2),run(2)  # Collect project data → build sections → render → inject TOC.
    _refresh_map_toon(proj_dir)
    _find_tools_bin_dir(proj_dir)
    _run_tool_if_present(bin_dir;name;args;proj_dir)
    _refresh_analysis_files(proj_dir;profile)
    _collect_tool_sources(pyproj;reqs;tasks;makefile;scenarios)
    _doql_sources(doql)
    _collect_pkg_sources(pyproj;reqs;tasks;makefile;scenarios;openapi;doql;pyqual;goal;env_vars)
    _collect_infra_sources(dockerfile;compose;pkg_json;modules;project_analysis)
    _collect_sources(pyproj;reqs;tasks;makefile;scenarios;openapi;doql;pyqual;goal;env_vars;dockerfile;compose;pkg_json;modules;project_analysis;swop)
    _inject_toc(content)
  sumd/prolog_engine.py:
  sumd/renderer.py:
    e: generate_sumd_content
    generate_sumd_content(proj_dir;return_sources;raw_sources;profile)
  sumd/sections/__init__.py:
  sumd/sections/api_stubs.py:
    e: _render_api_stubs,ApiStubsSection
    ApiStubsSection: should_render(1)
    _render_api_stubs(openapi)
  sumd/sections/architecture.py:
    e: _render_architecture_doql_section,_render_architecture_modules,_render_doql_app,_render_doql_entities,_render_doql_interfaces,_render_doql_integrations,_render_architecture_doql_parsed,_render_architecture_rules,_render_architecture,ArchitectureSection
    ArchitectureSection:
    _render_architecture_doql_section(doql;proj_dir;raw_sources;L)
    _render_architecture_modules(modules;name;L)
    _render_doql_app(doql;L)
    _render_doql_entities(doql;L)
    _render_doql_interfaces(doql;L)
    _render_doql_integrations(doql;L)
    _render_architecture_doql_parsed(doql;L)
    _render_architecture_rules(proj_dir;L)
    _render_architecture(doql;modules;name;proj_dir;raw_sources)
  sumd/sections/base.py:
    e: RenderContext,Section
    RenderContext:  # All extracted data for a project, passed to every Section.re
    Section: should_render(1),render(1)  # Protocol for all SUMD section renderers.
  sumd/sections/call_graph.py:
    e: _parse_calls_header,_parse_hub_stat_line,_process_in_hubs_line,_parse_calls_hubs,_parse_calls_toon,_render_call_graph,CallGraphSection
    CallGraphSection: should_render(1)
    _parse_calls_header(lines)
    _parse_hub_stat_line(line)
    _process_in_hubs_line(line;hubs;current_hub)
    _parse_calls_hubs(lines)
    _parse_calls_toon(content)
    _render_call_graph(project_analysis)
  sumd/sections/code_analysis.py:
    e: _render_code_analysis,CodeAnalysisSection
    CodeAnalysisSection: should_render(1),render(1)
    _render_code_analysis(project_analysis;skip_files)
  sumd/sections/configuration.py:
    e: _render_configuration_section,ConfigurationSection
    ConfigurationSection:
    _render_configuration_section(name;version)
  sumd/sections/dependencies.py:
    e: _render_deps_runtime,_render_deps_dev,_render_dependencies,DependenciesSection
    DependenciesSection: should_render(1)
    _render_deps_runtime(deps;node_deps;L)
    _render_deps_dev(dev_deps;node_dev;L)
    _render_dependencies(deps;dev_deps;pkg_json)
  sumd/sections/deployment.py:
    e: _render_deployment_install,_render_deployment_reqs,_render_dockerfile_info,_render_deployment_docker,_render_deployment,DeploymentSection
    DeploymentSection:
    _render_deployment_install(pkg_json;name;L)
    _render_deployment_reqs(reqs;L)
    _render_dockerfile_info(dockerfile;a)
    _render_deployment_docker(dockerfile;compose;L)
    _render_deployment(pkg_json;name;reqs;dockerfile;compose)
  sumd/sections/environment.py:
    e: _render_env_section,_render_goal_section,EnvironmentSection
    EnvironmentSection: should_render(1),render(1)
    _render_env_section(env_vars)
    _render_goal_section(goal)
  sumd/sections/extras.py:
    e: _render_makefile_targets,_render_pkg_json_scripts,_render_extras,ExtrasSection
    ExtrasSection: should_render(1)
    _render_makefile_targets(makefile;a)
    _render_pkg_json_scripts(pkg_json;a)
    _render_extras(makefile;pkg_json)
  sumd/sections/interfaces.py:
    e: _render_interfaces_openapi,_render_testql_raw,_render_testql_endpoint,_render_testql_extras,_render_testql_one_structured,_render_interfaces_testql,_render_interfaces,InterfacesSection
    InterfacesSection: should_render(1)
    _render_interfaces_openapi(openapi;proj_dir;raw_sources;L)
    _render_testql_raw(scenarios;proj_dir;L)
    _render_testql_endpoint(ep;L)
    _render_testql_extras(sc;L)
    _render_testql_one_structured(sc;L)
    _render_interfaces_testql(scenarios;proj_dir;raw_sources;L)
    _render_interfaces(scripts;openapi;scenarios;proj_dir;raw_sources)
  sumd/sections/metadata.py:
    e: MetadataSection
    MetadataSection: render(1)  # Render ## Metadata — always present, all profiles.
  sumd/sections/quality.py:
    e: _render_quality_raw,_render_quality_parsed,_render_quality,QualitySection
    QualitySection:
    _render_quality_raw(proj_dir;L)
    _render_quality_parsed(pyqual;L)
    _render_quality(pyqual;proj_dir;raw_sources)
  sumd/sections/refactor_analysis.py:
    e: RefactorAnalysisSection
    RefactorAnalysisSection: render(1)
  sumd/sections/source_snippets.py:
    e: _render_source_snippets,SourceSnippetsSection
    SourceSnippetsSection:
    _render_source_snippets(source_snippets;top_n)
  sumd/sections/swop.py:
    e: _render_swop_section,SwopSection
    SwopSection: should_render(1)
    _render_swop_section(swop;raw_sources)
  sumd/sections/test_contracts.py:
    e: _render_scenario_contract,_render_test_contracts,TestContractsSection
    TestContractsSection:
    _render_scenario_contract(sc;a)
    _render_test_contracts(scenarios)
  sumd/sections/utils/__init__.py:
  sumd/sections/utils/render.py:
    e: call_with_ctx
    call_with_ctx(render_fn)
  sumd/sections/utils/should_render.py:
    e: always,has_attr
    always(_self;_ctx)
    has_attr(attr)
  sumd/sections/workflows.py:
    e: _render_workflows_doql,_render_workflows_taskfile,_render_workflows,WorkflowsSection
    WorkflowsSection: should_render(1)
    _render_workflows_doql(doql;L)
    _render_workflows_taskfile(tasks;proj_dir;raw_sources;L)
    _render_workflows(doql;tasks;proj_dir;raw_sources)
  sumd/toon_parser.py:
    e: _parse_toon_block_config,_parse_toon_block_api,_parse_toon_block_assert,_parse_generic_block,_parse_toon_block_performance,_parse_toon_block_navigate,_parse_toon_block_gui,_parse_toon_file,extract_testql_scenarios
    _parse_toon_block_config(lines)
    _parse_toon_block_api(content)
    _parse_toon_block_assert(lines)
    _parse_generic_block(lines;block_prefix;pattern;key_names)
    _parse_toon_block_performance(lines)
    _parse_toon_block_navigate(lines)
    _parse_toon_block_gui(lines)
    _parse_toon_file(f)
    extract_testql_scenarios(proj_dir)
  sumd/utils/__init__.py:
  sumd/utils/prolog_core.py:
    e: is_variable,to_term,_split_body_terms,unify,resolve_val,deep_resolve,extend_subst,occurs_check,rename_variables,Variable,Term,Rule,PythonPrologDB,PythonPrologEngine,HybridPrologEngine
    Variable: __init__(1),__repr__(0),__eq__(1),__hash__(0)  # Represents a logical variable in our pure Python engine.
    Term: __init__(1),__repr__(0),__eq__(1)  # Represents a Prolog term (e.g. parent(john, mary)).
    Rule: __init__(2),__repr__(0)  # Represents a Prolog rule Head :- Body.
    PythonPrologDB: __init__(0),add_fact(1),add_rule(2),parse_and_load(1)  # In-memory Prolog database for pure Python execution.
    PythonPrologEngine: __init__(1),query(1),_find_vars(1),_resolve(2)  # SLD Resolution Logic Interpreter.
    HybridPrologEngine: __init__(1),query(1),_query_pyswip(1),_query_subprocess(1),_query_python(1),_swipl_executable_exists(0)  # Hybrid Logic Engine delegating queries based on backend avai
    is_variable(x)
    to_term(x)
    _split_body_terms(body_str)
    unify(x;y;subst)
    resolve_val(x;subst)
    deep_resolve(x;subst)
    extend_subst(v;val;subst)
    occurs_check(v;val;subst)
    rename_variables(rule;suffix)
  sumd/validator.py:
    e: _validate_yaml_body,_validate_less_css_body,_validate_mermaid_body,_validate_toon_body,_validate_bash_body,_validate_deps_body,_validate_markpact_meta,validate_codeblocks,_check_h1,_check_required_sections,_check_metadata_fields,_check_unclosed_fences,_check_empty_links,validate_markdown,validate_project_architecture,validate_sumd_file,CodeBlockIssue
    CodeBlockIssue:
    _validate_yaml_body(body;path)
    _validate_less_css_body(body;path)
    _validate_mermaid_body(body;path)
    _validate_toon_body(body;path)
    _validate_bash_body(body;path)
    _validate_deps_body(body;path)
    _validate_markpact_meta(mp;line_no;lang;meta;issues)
    validate_codeblocks(content;source)
    _check_h1(lines;source)
    _check_required_sections(lines;source;profile)
    _check_metadata_fields(lines;source)
    _check_unclosed_fences(lines;source)
    _check_empty_links(content;source)
    validate_markdown(content;source;profile)
    validate_project_architecture(proj_dir)
    validate_sumd_file(path;profile)
  sumd_logic_validator/logic/__init__.py:
  sumd_logic_validator/sumd_logic_validator/__init__.py:
  sumd_logic_validator/sumd_logic_validator/cli.py:
    e: get_engine,main,info,query,shell
    get_engine()
    main()
    info()
    query(query_str)
    shell()
  sumd_logic_validator/sumd_logic_validator/engine.py:
  sumd_logic_validator/sumd_logic_validator/logic/__init__.py:
  sumd_logic_validator/sumd_logic_validator/main.py:
  sumd_logic_validator/tests/__init__.py:
  sumd_logic_validator/tests/test_engine.py:
    e: engine,test_detects_architectural_inconsistencies,test_project_structure_facts
    engine()
    test_detects_architectural_inconsistencies(engine)
    test_project_structure_facts(engine)
  test_gitignore.py:
  test_ignore.py:
  tests/test_architectural_logic.py:
    e: test_pure_python_prolog_basic,test_architectural_validation_missing_file,test_architectural_validation_aligned,test_architectural_validation_missing_automation,test_architectural_validation_missing_gate
    test_pure_python_prolog_basic()
    test_architectural_validation_missing_file(tmp_path)
    test_architectural_validation_aligned(tmp_path)
    test_architectural_validation_missing_automation(tmp_path)
    test_architectural_validation_missing_gate(tmp_path)
  tests/test_cli.py:
    e: sumd_file,TestValidateCommand,TestInfoCommand,TestExportCommand,TestCliVersion,TestCliHelp,TestProjectDetection,TestNodeSpecFromPackageJson,TestGenerateDoqlLess
    TestValidateCommand: test_valid_file_exits_zero(1),test_valid_file_prints_ok(1),test_missing_file_exits_nonzero(1)
    TestInfoCommand: test_info_runs(1)
    TestExportCommand: test_export_json(1),test_export_to_output_file(2),test_export_markdown(1)
    TestCliVersion: test_version_option(0)
    TestCliHelp: test_help(0),test_validate_help(0),test_export_help(0),test_scan_help(0)
    TestProjectDetection: test_is_project_dir_accepts_language_marker(3),test_is_project_dir_accepts_glob_markers(3),test_empty_dir_is_not_project(1),test_detect_projects_finds_mixed_languages(1),test_detect_projects_non_recursive_skips_nested(1),test_detect_projects_recursive_finds_nested(1)  # Detection must work across all supported languages/project t
    TestNodeSpecFromPackageJson: test_framework_detection(2),test_spec_uses_real_scripts_and_extras(0),test_spec_falls_back_without_scripts(0)  # Node DOQL spec must mirror real package.json (scripts + fram
    TestGenerateDoqlLess: _pkg(1),test_fresh_generation_for_node_uses_real_scripts(1),test_force_regenerates_autogen_file_without_duplicating(1),test_force_preserves_user_authored_file(1),test_no_force_skips_existing(1)  # Refresh behaviour for app.doql.less generation.
    sumd_file(tmp_path)
  tests/test_cqrs_es.py:
    e: TestEventStore,TestSumdAggregate,TestCommandBus,TestQueryBus,TestEventSourcedRepository,TestIntegration
    TestEventStore: test_save_and_get_events(0),test_persistence(0),test_get_events_from_version(0)  # Test EventStore functionality.
    TestSumdAggregate: test_create_document(0),test_add_section(0),test_remove_section(0),test_load_from_history(0)  # Test SumdAggregate functionality.
    TestCommandBus: test_dispatch_command(0)  # Test CommandBus functionality.
    TestQueryBus: test_dispatch_query(0)  # Test QueryBus functionality.
    TestEventSourcedRepository: test_save_and_get_aggregate(0)  # Test EventSourcedRepository functionality.
    TestIntegration: test_full_workflow(0)  # Integration tests for CQRS ES architecture.
  tests/test_dogfood.py:
    e: _run,project_copy,test_sumd_scans_itself,test_sumd_scans_all_profiles,test_sumr_generates_sumr_md,test_sumd_lint_passes_on_generated_output,test_sumd_version_flag,test_sumd_scan_produces_no_unhandled_exceptions
    _run(cmd;cwd;timeout)
    project_copy(tmp_path_factory)
    test_sumd_scans_itself(project_copy)
    test_sumd_scans_all_profiles(project_copy;profile)
    test_sumr_generates_sumr_md(project_copy)
    test_sumd_lint_passes_on_generated_output(project_copy)
    test_sumd_version_flag()
    test_sumd_scan_produces_no_unhandled_exceptions(project_copy)
  tests/test_dsl.py:
    e: TestDSLLexer,TestDSLParser,TestDSLEngine,TestDSLCommandRegistry,TestDSLShell,TestDSLIntegration
    TestDSLLexer: test_tokenize_simple_command(0),test_tokenize_function_call(0),test_tokenize_arithmetic(0),test_tokenize_string_literals(0),test_tokenize_comments(0)  # Test DSL lexer functionality.
    TestDSLParser: test_parse_simple_command(0),test_parse_function_call(0),test_parse_arithmetic(0),test_parse_assignment(0),test_parse_pipeline(0),test_parse_comparison(0),test_parse_logical(0)  # Test DSL parser functionality.
    TestDSLEngine: test_execute_literal(0),test_execute_arithmetic(0),test_execute_comparison(0),test_execute_logical(0),test_execute_assignment(0),test_execute_function_call(0),test_execute_pipeline(0)  # Test DSL engine functionality.
    TestDSLCommandRegistry: test_builtin_registry(0),test_command_categories(0),test_help_system(0)  # Test DSL command registry.
    TestDSLShell: test_shell_initialization(0),test_execute_command(0),test_execute_script(0)  # Test DSL shell functionality.
    TestDSLIntegration: test_dsl_with_sumd_commands(0),test_complex_dsl_expressions(0),test_error_handling(0)  # Integration tests for DSL functionality.
  tests/test_extractor.py:
    e: TestExtractPyproject,TestExtractTaskfile,TestExtractPyqual,TestExtractPythonModules,TestExtractReadmeTitle,TestExtractEnv,TestExtractGoal,TestExtractProjectAnalysis,TestExtractRequirements,TestExtractMakefile
    TestExtractPyproject: test_missing_file_returns_empty(1),test_basic_fields(1),test_dependencies_parsed(1),test_dev_dependencies_from_optional(1),test_fallback_name_is_dir_name(1),test_corrupt_toml_returns_empty(1)
    TestExtractTaskfile: test_missing_returns_empty(1),test_parses_tasks(1),test_task_without_desc(1),test_multiple_tasks(1)
    TestExtractPyqual: test_missing_returns_empty(1),test_parses_pipeline(1),test_flat_format(1)
    TestExtractPythonModules: test_missing_pkg_dir_returns_empty(1),test_lists_modules(1),test_excludes_dunder_files(1)
    TestExtractReadmeTitle: test_missing_returns_empty(1),test_extracts_h1(1),test_no_h1_returns_empty(1),test_first_h1_only(1)
    TestExtractEnv: test_missing_returns_empty(1),test_parses_key_value(1),test_captures_preceding_comment(1),test_captures_inline_comment(1),test_empty_value_becomes_not_set(1)
    TestExtractGoal: test_missing_returns_empty(1),test_parses_project_and_versioning(1)
    TestExtractProjectAnalysis: test_missing_project_dir_returns_empty(1),test_loads_calls_toon_yaml(1),test_refactor_mode_loads_extra_files(1),test_missing_files_skipped(1)
    TestExtractRequirements: test_no_requirements_returns_empty(1),test_parses_requirements_txt(1),test_ignores_comments_and_flags(1)
    TestExtractMakefile: test_missing_returns_empty(1),test_parses_targets(1),test_comment_captured(1)
  tests/test_mcp_cqrs_dsl.py:
    e: TestMCPCQRSCommands,TestMCPDSLCommands,TestMCPIntegration,TestMCPErrorHandling
    TestMCPCQRSCommands: test_execute_command(0),test_execute_command_error(0),test_execute_query(0),test_get_events(0),test_get_aggregate(0)  # Test MCP CQRS command tools.
    TestMCPDSLCommands: test_execute_dsl(0),test_dsl_shell_info(0)  # Test MCP DSL command tools.
    TestMCPIntegration: test_full_cqrs_workflow_via_mcp(0),test_dsl_integration_via_mcp(0)  # Integration tests for MCP server with CQRS ES and DSL.
    TestMCPErrorHandling: test_unknown_command_type(0),test_unknown_query_type(0),test_aggregate_not_found(0)  # Test error handling in MCP tools.
  tests/test_mcp_server.py:
    e: sumd_file,run,TestDocToDict,TestResolvePath,TestListTools,TestParseSumd,TestValidateSumd,TestExportSumd,TestListSections,TestGetSection,TestInfoSumd,TestGenerateSumd,TestUnknownTool
    TestDocToDict: test_has_required_keys(1),test_section_has_fields(1)
    TestResolvePath: test_absolute_path_unchanged(1),test_relative_resolves_from_cwd(0)
    TestListTools: test_returns_thirteen_tools(0),test_tool_names(0),test_each_tool_has_input_schema(0)
    TestParseSumd: test_returns_json(1),test_missing_file_returns_error(1)
    TestValidateSumd: test_valid_file(1),test_missing_file_returns_error(1)
    TestExportSumd: test_export_json(1),test_export_markdown(1),test_export_to_file(2)
    TestListSections: test_returns_list(1),test_section_has_name(1)
    TestGetSection: test_found_section(1),test_missing_section(1)
    TestInfoSumd: test_returns_info(1)
    TestGenerateSumd: test_generate_content(0),test_generate_to_file(1)
    TestUnknownTool: test_unknown_returns_error(0)
    sumd_file(tmp_path)
    run(coro)
  tests/test_parser.py:
    e: test_parse_basic,test_parse_sections,test_validate_valid_document,test_validate_missing_intent,test_parse_file,test_parser_class,test_markpact_semantic_kinds_valid,test_markpact_unknown_kind_error,test_markpact_missing_path_error
    test_parse_basic()
    test_parse_sections()
    test_validate_valid_document()
    test_validate_missing_intent()
    test_parse_file(tmp_path)
    test_parser_class()
    test_markpact_semantic_kinds_valid()
    test_markpact_unknown_kind_error()
    test_markpact_missing_path_error()
  tests/test_pipeline.py:
    e: proj_dir,test_pipeline_run_returns_string,test_pipeline_output_has_h1,test_pipeline_output_has_metadata,test_pipeline_return_sources,test_pipeline_profile_minimal,test_pipeline_profile_refactor,test_pipeline_with_modules,test_pipeline_with_taskfile,test_pipeline_with_dependencies,test_pipeline_injects_toc,test_required_tools_rich,test_required_tools_refactor,test_required_tools_minimal,test_refresh_map_toon_writes_file,test_refresh_analysis_files_noop_without_tools
    proj_dir(tmp_path)
    test_pipeline_run_returns_string(proj_dir)
    test_pipeline_output_has_h1(proj_dir)
    test_pipeline_output_has_metadata(proj_dir)
    test_pipeline_return_sources(proj_dir)
    test_pipeline_profile_minimal(proj_dir)
    test_pipeline_profile_refactor(proj_dir)
    test_pipeline_with_modules(proj_dir)
    test_pipeline_with_taskfile(proj_dir)
    test_pipeline_with_dependencies(proj_dir)
    test_pipeline_injects_toc(proj_dir)
    test_required_tools_rich()
    test_required_tools_refactor()
    test_required_tools_minimal()
    test_refresh_map_toon_writes_file(tmp_path)
    test_refresh_analysis_files_noop_without_tools(tmp_path)
  tests/test_sections.py:
    e: make_ctx,TestMetadataSection,TestArchitectureSection,TestDependenciesSection,TestWorkflowsSection,TestQualitySection,TestEnvironmentSection,TestCallGraphSection,TestCodeAnalysisSection,TestRefactorAnalysisSection,TestSourceSnippetsSection
    TestMetadataSection: test_always_renders(0),test_contains_name_and_version(0),test_contains_metadata_header(0),test_optional_fields_omitted_when_empty(0)
    TestArchitectureSection: test_always_renders(0),test_header_present(0),test_modules_listed(0),test_no_modules_no_source_modules_section(0)
    TestDependenciesSection: test_renders_when_deps_present(0),test_runtime_deps_listed(0),test_no_deps_shows_fallback(0),test_dev_deps_section(0)
    TestWorkflowsSection: test_no_render_when_empty(0),test_renders_with_tasks(0),test_header_present(0)
    TestQualitySection: test_no_render_when_empty(0),test_renders_with_pyqual(0),test_pipeline_name_in_output(0)
    TestEnvironmentSection: test_no_render_when_empty(0),test_renders_with_vars(0)
    TestCallGraphSection: test_no_render_without_calls(0),test_no_render_without_calls_file(0),test_renders_with_calls_file(0)
    TestCodeAnalysisSection: test_no_render_when_only_calls(0),test_renders_with_map(0)
    TestRefactorAnalysisSection: test_no_render_when_empty(0),test_renders_with_analysis_files(0),test_map_toon_excluded(0)
    TestSourceSnippetsSection: test_no_render_when_empty(0),test_renders_with_snippets(0)
    make_ctx()
  tests/test_statement.py:
    e: test_placeholder,test_import
    test_placeholder()
    test_import()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('sumd', '0.3.51', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 255, 'less').
project_file('examples/app.doql.less', 60, 'less').
project_file('examples/basic/demo.sh', 50, 'shell').
project_file('examples/llm/anthropic_example.py', 61, 'python').
project_file('examples/llm/llm_cli_example.sh', 37, 'shell').
project_file('examples/llm/ollama_example.sh', 38, 'shell').
project_file('examples/llm/openai_example.py', 89, 'python').
project_file('examples/mcp/mcp_client.py', 139, 'python').
project_file('print_errors.py', 7, 'python').
project_file('project.sh', 55, 'shell').
project_file('scripts/bootstrap.sh', 70, 'shell').
project_file('scripts/install_testql_autoloop.sh', 157, 'shell').
project_file('sumd/__init__.py', 36, 'python').
project_file('sumd/__main__.py', 6, 'python').
project_file('sumd/cli.py', 1213, 'python').
project_file('sumd/cli_doql.py', 440, 'python').
project_file('sumd/cli_scan.py', 393, 'python').
project_file('sumd/cqrs/__init__.py', 19, 'python').
project_file('sumd/cqrs/aggregates.py', 221, 'python').
project_file('sumd/cqrs/commands.py', 266, 'python').
project_file('sumd/cqrs/events.py', 185, 'python').
project_file('sumd/cqrs/queries.py', 420, 'python').
project_file('sumd/cqrs/sumd_aggregate.py', 345, 'python').
project_file('sumd/dsl/__init__.py', 15, 'python').
project_file('sumd/dsl/ast_nodes.py', 55, 'python').
project_file('sumd/dsl/commands.py', 650, 'python').
project_file('sumd/dsl/context_mixin.py', 18, 'python').
project_file('sumd/dsl/engine.py', 538, 'python').
project_file('sumd/dsl/lexer.py', 133, 'python').
project_file('sumd/dsl/nlp.py', 448, 'python').
project_file('sumd/dsl/parser.py', 172, 'python').
project_file('sumd/dsl/parser_base.py', 70, 'python').
project_file('sumd/dsl/parser_expr.py', 116, 'python').
project_file('sumd/dsl/parser_primary.py', 208, 'python').
project_file('sumd/dsl/schema.py', 346, 'python').
project_file('sumd/dsl/schema_commands.py', 518, 'python').
project_file('sumd/dsl/shell.py', 360, 'python').
project_file('sumd/extractor.py', 1345, 'python').
project_file('sumd/generator.py', 16, 'python').
project_file('sumd/mcp_server.py', 715, 'python').
project_file('sumd/models.py', 46, 'python').
project_file('sumd/parser.py', 188, 'python').
project_file('sumd/pipeline.py', 452, 'python').
project_file('sumd/prolog_engine.py', 40, 'python').
project_file('sumd/renderer.py', 30, 'python').
project_file('sumd/sections/__init__.py', 107, 'python').
project_file('sumd/sections/api_stubs.py', 77, 'python').
project_file('sumd/sections/architecture.py', 171, 'python').
project_file('sumd/sections/base.py', 95, 'python').
project_file('sumd/sections/call_graph.py', 157, 'python').
project_file('sumd/sections/code_analysis.py', 69, 'python').
project_file('sumd/sections/configuration.py', 44, 'python').
project_file('sumd/sections/dependencies.py', 98, 'python').
project_file('sumd/sections/deployment.py', 111, 'python').
project_file('sumd/sections/environment.py', 73, 'python').
project_file('sumd/sections/extras.py', 73, 'python').
project_file('sumd/sections/interfaces.py', 158, 'python').
project_file('sumd/sections/metadata.py', 52, 'python').
project_file('sumd/sections/quality.py', 82, 'python').
project_file('sumd/sections/refactor_analysis.py', 69, 'python').
project_file('sumd/sections/source_snippets.py', 69, 'python').
project_file('sumd/sections/swop.py', 69, 'python').
project_file('sumd/sections/test_contracts.py', 78, 'python').
project_file('sumd/sections/utils/__init__.py', 13, 'python').
project_file('sumd/sections/utils/render.py', 26, 'python').
project_file('sumd/sections/utils/should_render.py', 26, 'python').
project_file('sumd/sections/workflows.py', 87, 'python').
project_file('sumd/toon_parser.py', 177, 'python').
project_file('sumd/utils/__init__.py', 2, 'python').
project_file('sumd/utils/prolog_core.py', 433, 'python').
project_file('sumd/validator.py', 384, 'python').
project_file('sumd_logic_validator/logic/__init__.py', 2, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/__init__.py', 4, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/cli.py', 115, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/engine.py', 40, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/logic/__init__.py', 2, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/main.py', 5, 'python').
project_file('sumd_logic_validator/tests/__init__.py', 1, 'python').
project_file('sumd_logic_validator/tests/test_engine.py', 29, 'python').
project_file('test_gitignore.py', 1, 'python').
project_file('test_ignore.py', 1, 'python').
project_file('tests/test_architectural_logic.py', 167, 'python').
project_file('tests/test_cli.py', 348, 'python').
project_file('tests/test_cqrs_es.py', 389, 'python').
project_file('tests/test_dogfood.py', 148, 'python').
project_file('tests/test_dsl.py', 470, 'python').
project_file('tests/test_extractor.py', 313, 'python').
project_file('tests/test_mcp_cqrs_dsl.py', 465, 'python').
project_file('tests/test_mcp_server.py', 239, 'python').
project_file('tests/test_parser.py', 145, 'python').
project_file('tests/test_pipeline.py', 136, 'python').
project_file('tests/test_sections.py', 298, 'python').
project_file('tests/test_statement.py', 12, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/llm/anthropic_example.py', 'ask', 3, 1, 3).
python_function('examples/llm/anthropic_example.py', 'main', 0, 2, 8).
python_function('examples/llm/openai_example.py', 'build_context', 1, 5, 5).
python_function('examples/llm/openai_example.py', 'ask', 3, 1, 3).
python_function('examples/llm/openai_example.py', 'main', 0, 2, 8).
python_function('examples/mcp/mcp_client.py', 'run', 3, 11, 12).
python_function('examples/mcp/mcp_client.py', 'main', 0, 3, 9).
python_function('sumd/cli.py', 'cli', 0, 1, 2).
python_function('sumd/cli.py', 'validate', 1, 4, 8).
python_function('sumd/cli.py', 'export', 3, 8, 11).
python_function('sumd/cli.py', 'info', 1, 3, 7).
python_function('sumd/cli.py', 'generate', 3, 8, 15).
python_function('sumd/cli.py', 'extract', 2, 5, 8).
python_function('sumd/cli.py', 'scan', 14, 14, 18).
python_function('sumd/cli.py', 'lint', 4, 6, 13).
python_function('sumd/cli.py', '_lint_classify_issues', 2, 6, 1).
python_function('sumd/cli.py', '_lint_collect_paths', 2, 6, 7).
python_function('sumd/cli.py', '_lint_print_result', 3, 6, 4).
python_function('sumd/cli.py', '_setup_tools_venv', 3, 7, 6).
python_function('sumd/cli.py', '_run_code2llm_formats', 3, 5, 4).
python_function('sumd/cli.py', '_run_tool_subprocess', 3, 3, 4).
python_function('sumd/cli.py', '_run_analyze_tool', 4, 4, 3).
python_function('sumd/cli.py', 'analyze', 3, 7, 11).
python_function('sumd/cli.py', '_api_scenario_template', 4, 1, 3).
python_function('sumd/cli.py', '_scaffold_write', 5, 3, 3).
python_function('sumd/cli.py', '_scaffold_smoke_scenario', 6, 6, 5).
python_function('sumd/cli.py', '_scaffold_crud_scenarios', 6, 5, 7).
python_function('sumd/cli.py', '_scaffold_from_openapi', 6, 7, 12).
python_function('sumd/cli.py', '_scaffold_generic', 4, 1, 3).
python_function('sumd/cli.py', 'scaffold', 4, 9, 18).
python_function('sumd/cli.py', 'map_cmd', 4, 7, 12).
python_function('sumd/cli.py', 'dsl', 4, 1, 13).
python_function('sumd/cli.py', 'cqrs_command', 4, 1, 19).
python_function('sumd/cli.py', 'nlp_command', 4, 1, 13).
python_function('sumd/cli.py', 'main', 0, 10, 3).
python_function('sumd/cli.py', 'main_sumr', 0, 3, 2).
python_function('sumd/cli_doql.py', '_detect_project_type', 1, 8, 4).
python_function('sumd/cli_doql.py', '_render_doql_boilerplate', 3, 4, 3).
python_function('sumd/cli_doql.py', '_node_framework', 1, 5, 0).
python_function('sumd/cli_doql.py', '_node_spec_from_package_json', 1, 7, 5).
python_function('sumd/cli_doql.py', '_build_doql_spec', 2, 3, 4).
python_function('sumd/cli_doql.py', '_generate_doql_less', 5, 7, 8).
python_function('sumd/cli_scan.py', '_is_project_dir', 1, 8, 4).
python_function('sumd/cli_scan.py', '_walk_projects', 4, 10, 7).
python_function('sumd/cli_scan.py', '_detect_projects', 2, 1, 1).
python_function('sumd/cli_scan.py', '_ensure_venv', 3, 4, 4).
python_function('sumd/cli_scan.py', '_tool_bin', 2, 2, 1).
python_function('sumd/cli_scan.py', '_run_one_tool', 4, 3, 5).
python_function('sumd/cli_scan.py', '_run_analysis_tools', 3, 5, 5).
python_function('sumd/cli_scan.py', '_export_sumd_json', 2, 2, 2).
python_function('sumd/cli_scan.py', '_render_write_validate', 4, 5, 5).
python_function('sumd/cli_scan.py', '_echo_scan_result', 4, 2, 3).
python_function('sumd/cli_scan.py', '_maybe_generate_doql', 2, 7, 6).
python_function('sumd/cli_scan.py', '_maybe_generate_testql', 1, 5, 5).
python_function('sumd/cli_scan.py', '_finalize_scan', 9, 9, 9).
python_function('sumd/cli_scan.py', '_scan_one_project', 11, 10, 9).
python_function('sumd/dsl/commands.py', 'create_builtin_registry', 0, 1, 3).
python_function('sumd/dsl/commands.py', '_cmd_cat', 2, 3, 3).
python_function('sumd/dsl/commands.py', '_cmd_ls', 2, 9, 9).
python_function('sumd/dsl/commands.py', '_cmd_edit', 2, 2, 5).
python_function('sumd/dsl/commands.py', '_cmd_mkdir', 2, 2, 2).
python_function('sumd/dsl/commands.py', '_cmd_rm', 2, 4, 5).
python_function('sumd/dsl/commands.py', '_cmd_sumd_scan', 2, 6, 6).
python_function('sumd/dsl/commands.py', '_cmd_sumd_map', 2, 6, 6).
python_function('sumd/dsl/commands.py', '_cmd_sumd_validate', 2, 2, 5).
python_function('sumd/dsl/commands.py', '_cmd_sumd_info', 2, 3, 3).
python_function('sumd/dsl/commands.py', '_cmd_find', 2, 6, 9).
python_function('sumd/dsl/commands.py', '_cmd_grep', 2, 9, 11).
python_function('sumd/dsl/commands.py', '_cmd_echo', 2, 1, 1).
python_function('sumd/dsl/commands.py', '_cmd_pwd', 2, 1, 1).
python_function('sumd/dsl/commands.py', '_cmd_cd', 2, 4, 5).
python_function('sumd/dsl/commands.py', '_cmd_help', 2, 2, 2).
python_function('sumd/dsl/commands.py', '_cmd_clear', 2, 2, 1).
python_function('sumd/dsl/commands.py', '_cmd_set', 2, 3, 5).
python_function('sumd/dsl/commands.py', '_cmd_get', 2, 3, 2).
python_function('sumd/dsl/commands.py', '_cmd_unset', 2, 3, 1).
python_function('sumd/dsl/commands.py', '_cmd_vars', 2, 2, 3).
python_function('sumd/dsl/commands.py', '_cmd_exists', 2, 2, 2).
python_function('sumd/dsl/commands.py', '_cmd_read_file', 2, 1, 1).
python_function('sumd/dsl/parser.py', 'parse_dsl', 1, 1, 4).
python_function('sumd/dsl/shell.py', 'main', 0, 11, 12).
python_function('sumd/extractor.py', '_read_toml', 1, 2, 2).
python_function('sumd/extractor.py', 'extract_pyproject', 1, 3, 5).
python_function('sumd/extractor.py', '_first_task_cmd', 1, 4, 2).
python_function('sumd/extractor.py', 'extract_taskfile', 1, 6, 8).
python_function('sumd/extractor.py', '_parse_openapi_endpoints', 1, 8, 7).
python_function('sumd/extractor.py', 'extract_openapi', 1, 5, 7).
python_function('sumd/extractor.py', '_parse_doql_entities', 1, 4, 5).
python_function('sumd/extractor.py', '_parse_doql_interfaces', 1, 3, 7).
python_function('sumd/extractor.py', '_parse_doql_workflows', 1, 7, 10).
python_function('sumd/extractor.py', '_parse_doql_content', 1, 6, 14).
python_function('sumd/extractor.py', 'extract_doql', 1, 3, 3).
python_function('sumd/extractor.py', 'extract_pyqual', 1, 5, 5).
python_function('sumd/extractor.py', 'extract_python_modules', 2, 4, 4).
python_function('sumd/extractor.py', 'extract_readme_title', 1, 4, 5).
python_function('sumd/extractor.py', 'extract_requirements', 1, 7, 7).
python_function('sumd/extractor.py', 'extract_makefile', 1, 7, 9).
python_function('sumd/extractor.py', 'extract_goal', 1, 3, 7).
python_function('sumd/extractor.py', 'extract_env', 1, 10, 9).
python_function('sumd/extractor.py', '_parse_dockerfile_line', 2, 8, 6).
python_function('sumd/extractor.py', 'extract_dockerfile', 1, 6, 5).
python_function('sumd/extractor.py', 'extract_docker_compose', 1, 10, 12).
python_function('sumd/extractor.py', 'extract_package_json', 1, 3, 6).
python_function('sumd/extractor.py', '_lang_of', 1, 1, 2).
python_function('sumd/extractor.py', '_fan_out', 1, 5, 5).
python_function('sumd/extractor.py', '_cc_estimate', 1, 4, 4).
python_function('sumd/extractor.py', '_try_radon_cc', 1, 3, 1).
python_function('sumd/extractor.py', '_analyse_py_top_funcs', 2, 5, 6).
python_function('sumd/extractor.py', '_analyse_class_methods', 2, 6, 6).
python_function('sumd/extractor.py', '_analyse_py_top_classes', 2, 5, 7).
python_function('sumd/extractor.py', '_analyse_py_module', 1, 2, 6).
python_function('sumd/extractor.py', '_parse_ignore_file', 1, 6, 7).
python_function('sumd/extractor.py', '_match_dir_pattern', 3, 4, 2).
python_function('sumd/extractor.py', '_match_absolute_pattern', 2, 2, 1).
python_function('sumd/extractor.py', '_match_recursive_pattern', 2, 3, 1).
python_function('sumd/extractor.py', '_match_regular_pattern', 3, 5, 1).
python_function('sumd/extractor.py', '_path_matches_pattern', 2, 5, 7).
python_function('sumd/extractor.py', '_is_path_ignored', 3, 7, 3).
python_function('sumd/extractor.py', '_is_map_ignored_path', 1, 4, 1).
python_function('sumd/extractor.py', '_collect_map_files', 1, 8, 12).
python_function('sumd/extractor.py', '_render_map_detail', 2, 5, 3).
python_function('sumd/extractor.py', '_map_cc_stats', 1, 10, 7).
python_function('sumd/extractor.py', '_render_py_module_detail', 3, 7, 3).
python_function('sumd/extractor.py', 'generate_map_toon', 1, 5, 13).
python_function('sumd/extractor.py', '_facts_project_metadata', 1, 4, 3).
python_function('sumd/extractor.py', '_facts_project_files', 1, 2, 4).
python_function('sumd/extractor.py', '_facts_python_analysis', 1, 4, 5).
python_function('sumd/extractor.py', '_facts_dependencies', 1, 4, 3).
python_function('sumd/extractor.py', '_facts_makefile', 1, 3, 3).
python_function('sumd/extractor.py', '_facts_taskfile', 1, 3, 4).
python_function('sumd/extractor.py', '_facts_env_variables', 1, 3, 3).
python_function('sumd/extractor.py', '_facts_testql_scenarios', 1, 3, 4).
python_function('sumd/extractor.py', 'generate_project_logic', 1, 2, 13).
python_function('sumd/extractor.py', '_extract_markpact_files', 1, 4, 5).
python_function('sumd/extractor.py', '_extract_doql_interfaces', 1, 3, 5).
python_function('sumd/extractor.py', '_extract_doql_workflows', 1, 5, 8).
python_function('sumd/extractor.py', '_extract_doql_facts', 1, 2, 5).
python_function('sumd/extractor.py', '_extract_deploy_facts', 1, 2, 2).
python_function('sumd/extractor.py', '_extract_pyqual_gates', 1, 3, 7).
python_function('sumd/extractor.py', '_extract_sumd_semantic_facts', 1, 2, 7).
python_function('sumd/extractor.py', 'required_tools_for_profile', 1, 4, 0).
python_function('sumd/extractor.py', 'extract_source_snippets', 2, 6, 11).
python_function('sumd/extractor.py', 'extract_swop', 1, 9, 8).
python_function('sumd/extractor.py', 'extract_project_analysis', 2, 6, 7).
python_function('sumd/mcp_server.py', '_doc_to_dict', 1, 2, 0).
python_function('sumd/mcp_server.py', '_resolve_path', 1, 2, 3).
python_function('sumd/mcp_server.py', 'list_tools', 0, 1, 2).
python_function('sumd/mcp_server.py', '_tool_parse_sumd', 1, 1, 5).
python_function('sumd/mcp_server.py', '_tool_validate_sumd', 1, 1, 7).
python_function('sumd/mcp_server.py', '_tool_export_sumd', 1, 5, 8).
python_function('sumd/mcp_server.py', '_tool_list_sections', 1, 2, 4).
python_function('sumd/mcp_server.py', '_tool_get_section', 1, 5, 6).
python_function('sumd/mcp_server.py', '_tool_info_sumd', 1, 2, 5).
python_function('sumd/mcp_server.py', '_tool_generate_sumd', 1, 5, 5).
python_function('sumd/mcp_server.py', '_tool_execute_command', 1, 3, 6).
python_function('sumd/mcp_server.py', '_tool_execute_query', 1, 3, 5).
python_function('sumd/mcp_server.py', '_tool_get_events', 1, 3, 6).
python_function('sumd/mcp_server.py', '_tool_get_aggregate', 1, 3, 4).
python_function('sumd/mcp_server.py', '_tool_execute_dsl', 1, 3, 5).
python_function('sumd/mcp_server.py', '_tool_dsl_shell_info', 1, 2, 3).
python_function('sumd/mcp_server.py', 'call_tool', 2, 3, 4).
python_function('sumd/mcp_server.py', 'main', 0, 1, 3).
python_function('sumd/parser.py', 'parse', 1, 1, 2).
python_function('sumd/parser.py', 'parse_file', 1, 1, 2).
python_function('sumd/parser.py', 'validate', 1, 6, 2).
python_function('sumd/pipeline.py', '_refresh_map_toon', 1, 5, 4).
python_function('sumd/pipeline.py', '_find_tools_bin_dir', 1, 3, 1).
python_function('sumd/pipeline.py', '_run_tool_if_present', 4, 3, 3).
python_function('sumd/pipeline.py', '_refresh_analysis_files', 2, 7, 5).
python_function('sumd/pipeline.py', '_collect_tool_sources', 5, 7, 3).
python_function('sumd/pipeline.py', '_doql_sources', 1, 4, 1).
python_function('sumd/pipeline.py', '_collect_pkg_sources', 10, 5, 6).
python_function('sumd/pipeline.py', '_collect_infra_sources', 5, 6, 3).
python_function('sumd/pipeline.py', '_collect_sources', 16, 2, 4).
python_function('sumd/pipeline.py', '_inject_toc', 1, 3, 6).
python_function('sumd/renderer.py', 'generate_sumd_content', 4, 1, 2).
python_function('sumd/sections/api_stubs.py', '_render_api_stubs', 1, 11, 9).
python_function('sumd/sections/architecture.py', '_render_architecture_doql_section', 4, 6, 8).
python_function('sumd/sections/architecture.py', '_render_architecture_modules', 3, 2, 1).
python_function('sumd/sections/architecture.py', '_render_doql_app', 2, 3, 3).
python_function('sumd/sections/architecture.py', '_render_doql_entities', 2, 6, 4).
python_function('sumd/sections/architecture.py', '_render_doql_interfaces', 2, 6, 5).
python_function('sumd/sections/architecture.py', '_render_doql_integrations', 2, 5, 5).
python_function('sumd/sections/architecture.py', '_render_architecture_doql_parsed', 2, 1, 4).
python_function('sumd/sections/architecture.py', '_render_architecture_rules', 2, 3, 4).
python_function('sumd/sections/architecture.py', '_render_architecture', 5, 6, 5).
python_function('sumd/sections/call_graph.py', '_parse_calls_header', 1, 6, 5).
python_function('sumd/sections/call_graph.py', '_parse_hub_stat_line', 1, 2, 3).
python_function('sumd/sections/call_graph.py', '_process_in_hubs_line', 3, 6, 5).
python_function('sumd/sections/call_graph.py', '_parse_calls_hubs', 1, 8, 3).
python_function('sumd/sections/call_graph.py', '_parse_calls_toon', 1, 1, 3).
python_function('sumd/sections/call_graph.py', '_render_call_graph', 1, 7, 8).
python_function('sumd/sections/code_analysis.py', '_render_code_analysis', 2, 9, 4).
python_function('sumd/sections/configuration.py', '_render_configuration_section', 2, 1, 0).
python_function('sumd/sections/dependencies.py', '_render_deps_runtime', 3, 6, 2).
python_function('sumd/sections/dependencies.py', '_render_deps_dev', 3, 6, 2).
python_function('sumd/sections/dependencies.py', '_render_dependencies', 3, 2, 4).
python_function('sumd/sections/deployment.py', '_render_deployment_install', 3, 2, 2).
python_function('sumd/sections/deployment.py', '_render_deployment_reqs', 2, 5, 2).
python_function('sumd/sections/deployment.py', '_render_dockerfile_info', 2, 6, 3).
python_function('sumd/sections/deployment.py', '_render_deployment_docker', 3, 8, 4).
python_function('sumd/sections/deployment.py', '_render_deployment', 5, 1, 4).
python_function('sumd/sections/environment.py', '_render_env_section', 1, 3, 2).
python_function('sumd/sections/environment.py', '_render_goal_section', 1, 9, 3).
python_function('sumd/sections/extras.py', '_render_makefile_targets', 2, 3, 1).
python_function('sumd/sections/extras.py', '_render_pkg_json_scripts', 2, 7, 4).
python_function('sumd/sections/extras.py', '_render_extras', 2, 3, 3).
python_function('sumd/sections/interfaces.py', '_render_interfaces_openapi', 4, 6, 7).
python_function('sumd/sections/interfaces.py', '_render_testql_raw', 3, 4, 7).
python_function('sumd/sections/interfaces.py', '_render_testql_endpoint', 2, 3, 2).
python_function('sumd/sections/interfaces.py', '_render_testql_extras', 2, 7, 3).
python_function('sumd/sections/interfaces.py', '_render_testql_one_structured', 2, 7, 4).
python_function('sumd/sections/interfaces.py', '_render_interfaces_testql', 4, 3, 3).
python_function('sumd/sections/interfaces.py', '_render_interfaces', 5, 5, 4).
python_function('sumd/sections/quality.py', '_render_quality_raw', 2, 2, 4).
python_function('sumd/sections/quality.py', '_render_quality_parsed', 2, 9, 3).
python_function('sumd/sections/quality.py', '_render_quality', 3, 3, 3).
python_function('sumd/sections/source_snippets.py', '_render_source_snippets', 2, 8, 4).
python_function('sumd/sections/swop.py', '_render_swop_section', 2, 9, 5).
python_function('sumd/sections/test_contracts.py', '_render_scenario_contract', 2, 9, 2).
python_function('sumd/sections/test_contracts.py', '_render_test_contracts', 1, 5, 9).
python_function('sumd/sections/utils/render.py', 'call_with_ctx', 1, 1, 2).
python_function('sumd/sections/utils/should_render.py', 'always', 2, 1, 0).
python_function('sumd/sections/utils/should_render.py', 'has_attr', 1, 1, 2).
python_function('sumd/sections/workflows.py', '_render_workflows_doql', 2, 4, 3).
python_function('sumd/sections/workflows.py', '_render_workflows_taskfile', 4, 6, 4).
python_function('sumd/sections/workflows.py', '_render_workflows', 4, 4, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_config', 1, 9, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_api', 1, 6, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_assert', 1, 7, 5).
python_function('sumd/toon_parser.py', '_parse_generic_block', 4, 7, 6).
python_function('sumd/toon_parser.py', '_parse_toon_block_performance', 1, 1, 1).
python_function('sumd/toon_parser.py', '_parse_toon_block_navigate', 1, 7, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_gui', 1, 1, 1).
python_function('sumd/toon_parser.py', '_parse_toon_file', 1, 4, 13).
python_function('sumd/toon_parser.py', 'extract_testql_scenarios', 1, 7, 8).
python_function('sumd/utils/prolog_core.py', 'is_variable', 1, 6, 4).
python_function('sumd/utils/prolog_core.py', 'to_term', 1, 13, 15).
python_function('sumd/utils/prolog_core.py', '_split_body_terms', 1, 14, 4).
python_function('sumd/utils/prolog_core.py', 'unify', 3, 10, 7).
python_function('sumd/utils/prolog_core.py', 'resolve_val', 2, 3, 1).
python_function('sumd/utils/prolog_core.py', 'deep_resolve', 2, 3, 4).
python_function('sumd/utils/prolog_core.py', 'extend_subst', 3, 2, 2).
python_function('sumd/utils/prolog_core.py', 'occurs_check', 3, 4, 4).
python_function('sumd/utils/prolog_core.py', 'rename_variables', 2, 2, 5).
python_function('sumd/validator.py', '_validate_yaml_body', 2, 2, 1).
python_function('sumd/validator.py', '_validate_less_css_body', 2, 2, 1).
python_function('sumd/validator.py', '_validate_mermaid_body', 2, 3, 4).
python_function('sumd/validator.py', '_validate_toon_body', 2, 2, 1).
python_function('sumd/validator.py', '_validate_bash_body', 2, 4, 1).
python_function('sumd/validator.py', '_validate_deps_body', 2, 5, 6).
python_function('sumd/validator.py', '_validate_markpact_meta', 5, 5, 6).
python_function('sumd/validator.py', 'validate_codeblocks', 2, 9, 11).
python_function('sumd/validator.py', '_check_h1', 2, 3, 2).
python_function('sumd/validator.py', '_check_required_sections', 3, 7, 6).
python_function('sumd/validator.py', '_check_metadata_fields', 2, 9, 6).
python_function('sumd/validator.py', '_check_unclosed_fences', 2, 4, 2).
python_function('sumd/validator.py', '_check_empty_links', 2, 2, 1).
python_function('sumd/validator.py', 'validate_markdown', 3, 1, 6).
python_function('sumd/validator.py', 'validate_project_architecture', 1, 8, 11).
python_function('sumd/validator.py', 'validate_sumd_file', 2, 4, 8).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'get_engine', 0, 4, 6).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'main', 0, 1, 1).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'info', 0, 2, 3).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'query', 1, 6, 11).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'shell', 0, 10, 11).
python_function('sumd_logic_validator/tests/test_engine.py', 'engine', 0, 1, 3).
python_function('sumd_logic_validator/tests/test_engine.py', 'test_detects_architectural_inconsistencies', 1, 3, 5).
python_function('sumd_logic_validator/tests/test_engine.py', 'test_project_structure_facts', 1, 5, 2).
python_function('tests/test_architectural_logic.py', 'test_pure_python_prolog_basic', 0, 5, 6).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_missing_file', 1, 3, 5).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_aligned', 1, 2, 3).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_missing_automation', 1, 3, 5).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_missing_gate', 1, 3, 5).
python_function('tests/test_cli.py', 'sumd_file', 1, 1, 1).
python_function('tests/test_dogfood.py', '_run', 3, 1, 1).
python_function('tests/test_dogfood.py', 'project_copy', 1, 1, 5).
python_function('tests/test_dogfood.py', 'test_sumd_scans_itself', 1, 5, 5).
python_function('tests/test_dogfood.py', 'test_sumd_scans_all_profiles', 2, 3, 4).
python_function('tests/test_dogfood.py', 'test_sumr_generates_sumr_md', 1, 5, 5).
python_function('tests/test_dogfood.py', 'test_sumd_lint_passes_on_generated_output', 1, 3, 3).
python_function('tests/test_dogfood.py', 'test_sumd_version_flag', 0, 3, 4).
python_function('tests/test_dogfood.py', 'test_sumd_scan_produces_no_unhandled_exceptions', 1, 3, 2).
python_function('tests/test_mcp_server.py', 'sumd_file', 1, 1, 1).
python_function('tests/test_mcp_server.py', 'run', 1, 1, 2).
python_function('tests/test_parser.py', 'test_parse_basic', 0, 4, 2).
python_function('tests/test_parser.py', 'test_parse_sections', 0, 6, 1).
python_function('tests/test_parser.py', 'test_validate_valid_document', 0, 2, 3).
python_function('tests/test_parser.py', 'test_validate_missing_intent', 0, 3, 4).
python_function('tests/test_parser.py', 'test_parse_file', 1, 2, 2).
python_function('tests/test_parser.py', 'test_parser_class', 0, 3, 3).
python_function('tests/test_parser.py', 'test_markpact_semantic_kinds_valid', 0, 5, 2).
python_function('tests/test_parser.py', 'test_markpact_unknown_kind_error', 0, 2, 2).
python_function('tests/test_parser.py', 'test_markpact_missing_path_error', 0, 2, 2).
python_function('tests/test_pipeline.py', 'proj_dir', 1, 1, 1).
python_function('tests/test_pipeline.py', 'test_pipeline_run_returns_string', 1, 3, 4).
python_function('tests/test_pipeline.py', 'test_pipeline_output_has_h1', 1, 5, 4).
python_function('tests/test_pipeline.py', 'test_pipeline_output_has_metadata', 1, 4, 2).
python_function('tests/test_pipeline.py', 'test_pipeline_return_sources', 1, 4, 3).
python_function('tests/test_pipeline.py', 'test_pipeline_profile_minimal', 1, 4, 2).
python_function('tests/test_pipeline.py', 'test_pipeline_profile_refactor', 1, 5, 2).
python_function('tests/test_pipeline.py', 'test_pipeline_with_modules', 1, 2, 4).
python_function('tests/test_pipeline.py', 'test_pipeline_with_taskfile', 1, 3, 3).
python_function('tests/test_pipeline.py', 'test_pipeline_with_dependencies', 1, 3, 3).
python_function('tests/test_pipeline.py', 'test_pipeline_injects_toc', 1, 2, 2).
python_function('tests/test_pipeline.py', 'test_required_tools_rich', 0, 2, 1).
python_function('tests/test_pipeline.py', 'test_required_tools_refactor', 0, 2, 1).
python_function('tests/test_pipeline.py', 'test_required_tools_minimal', 0, 2, 1).
python_function('tests/test_pipeline.py', 'test_refresh_map_toon_writes_file', 1, 2, 2).
python_function('tests/test_pipeline.py', 'test_refresh_analysis_files_noop_without_tools', 1, 1, 1).
python_function('tests/test_sections.py', 'make_ctx', 0, 1, 4).
python_function('tests/test_statement.py', 'test_placeholder', 0, 2, 0).
python_function('tests/test_statement.py', 'test_import', 0, 1, 0).

% ── Python Classes ───────────────────────────────────────
python_class('sumd/cqrs/aggregates.py', 'AggregateRoot').
python_method('AggregateRoot', '__init__', 1, 1, 0).
python_method('AggregateRoot', 'aggregate_id', 0, 1, 0).
python_method('AggregateRoot', 'version', 0, 1, 0).
python_method('AggregateRoot', 'uncommitted_events', 0, 1, 1).
python_method('AggregateRoot', 'set_event_store', 1, 1, 0).
python_method('AggregateRoot', 'apply_event', 1, 3, 3).
python_method('AggregateRoot', 'mark_events_as_committed', 0, 1, 1).
python_method('AggregateRoot', 'load_from_history', 1, 4, 2).
python_method('AggregateRoot', '_when', 1, 1, 0).
python_method('AggregateRoot', 'commit', 0, 3, 3).
python_method('AggregateRoot', 'get_state', 0, 1, 0).
python_class('sumd/cqrs/aggregates.py', 'EntityState').
python_class('sumd/cqrs/aggregates.py', 'Entity').
python_method('Entity', '__init__', 1, 1, 0).
python_method('Entity', 'id', 0, 1, 0).
python_method('Entity', 'domain_events', 0, 1, 1).
python_method('Entity', 'add_domain_event', 1, 1, 1).
python_method('Entity', 'clear_domain_events', 0, 1, 1).
python_method('Entity', 'get_state', 0, 1, 0).
python_class('sumd/cqrs/aggregates.py', 'ValueObject').
python_method('ValueObject', '__eq__', 1, 2, 1).
python_method('ValueObject', '__hash__', 0, 1, 4).
python_method('ValueObject', 'get_state', 0, 1, 1).
python_class('sumd/cqrs/aggregates.py', 'Repository').
python_method('Repository', 'get_by_id', 1, 3, 0).
python_method('Repository', 'save', 1, 1, 0).
python_method('Repository', 'delete', 1, 2, 0).
python_class('sumd/cqrs/aggregates.py', 'EventSourcedRepository').
python_method('EventSourcedRepository', '__init__', 2, 1, 0).
python_method('EventSourcedRepository', 'get_by_id', 1, 3, 4).
python_method('EventSourcedRepository', 'save', 1, 1, 2).
python_method('EventSourcedRepository', 'delete', 1, 2, 0).
python_method('EventSourcedRepository', 'clear_cache', 0, 1, 1).
python_class('sumd/cqrs/commands.py', 'Command').
python_class('sumd/cqrs/commands.py', 'CommandHandler').
python_method('CommandHandler', 'handle', 1, 9, 0).
python_method('CommandHandler', 'can_handle', 1, 1, 0).
python_class('sumd/cqrs/commands.py', 'CommandBus').
python_method('CommandBus', '__init__', 1, 1, 0).
python_method('CommandBus', 'register_handler', 2, 1, 0).
python_method('CommandBus', 'dispatch', 1, 4, 5).
python_class('sumd/cqrs/commands.py', 'CreateSumdDocument').
python_class('sumd/cqrs/commands.py', 'UpdateSumdDocument').
python_class('sumd/cqrs/commands.py', 'AddSumdSection').
python_class('sumd/cqrs/commands.py', 'RemoveSumdSection').
python_class('sumd/cqrs/commands.py', 'ValidateSumdDocument').
python_class('sumd/cqrs/commands.py', 'ScanProject').
python_class('sumd/cqrs/commands.py', 'GenerateMap').
python_class('sumd/cqrs/commands.py', 'ExecuteDslCommand').
python_class('sumd/cqrs/commands.py', 'SumdCommandHandler').
python_method('SumdCommandHandler', '__init__', 1, 1, 0).
python_method('SumdCommandHandler', 'can_handle', 1, 1, 0).
python_method('SumdCommandHandler', 'handle', 1, 9, 10).
python_class('sumd/cqrs/events.py', 'Event').
python_method('Event', 'to_dict', 0, 1, 1).
python_method('Event', 'from_dict', 2, 1, 2).
python_class('sumd/cqrs/events.py', 'EventStore').
python_method('EventStore', '__init__', 1, 2, 1).
python_method('EventStore', 'save_event', 1, 6, 4).
python_method('EventStore', 'get_events', 2, 3, 1).
python_method('EventStore', 'get_all_events', 0, 2, 3).
python_method('EventStore', '_persist_event', 1, 2, 5).
python_method('EventStore', '_load_events', 0, 7, 7).
python_class('sumd/cqrs/events.py', 'SumdDocumentCreated').
python_class('sumd/cqrs/events.py', 'SumdDocumentUpdated').
python_class('sumd/cqrs/events.py', 'SumdSectionAdded').
python_class('sumd/cqrs/events.py', 'SumdSectionRemoved').
python_class('sumd/cqrs/events.py', 'SumdDocumentValidated').
python_class('sumd/cqrs/events.py', 'SumdCommandExecuted').
python_class('sumd/cqrs/queries.py', 'Query').
python_class('sumd/cqrs/queries.py', 'QueryHandler').
python_method('QueryHandler', 'handle', 1, 10, 0).
python_method('QueryHandler', 'can_handle', 1, 1, 0).
python_class('sumd/cqrs/queries.py', 'QueryBus').
python_method('QueryBus', '__init__', 1, 1, 0).
python_method('QueryBus', 'register_handler', 2, 1, 0).
python_method('QueryBus', 'dispatch', 1, 3, 4).
python_class('sumd/cqrs/queries.py', 'GetSumdDocument').
python_class('sumd/cqrs/queries.py', 'ListSumdSections').
python_class('sumd/cqrs/queries.py', 'GetSumdSection').
python_class('sumd/cqrs/queries.py', 'GetProjectInfo').
python_class('sumd/cqrs/queries.py', 'GetEventHistory').
python_class('sumd/cqrs/queries.py', 'GetAllEvents').
python_class('sumd/cqrs/queries.py', 'SearchDocuments').
python_class('sumd/cqrs/queries.py', 'GetValidationResults').
python_class('sumd/cqrs/queries.py', 'ExecuteDslQuery').
python_class('sumd/cqrs/queries.py', 'SumdQueryHandler').
python_method('SumdQueryHandler', '__init__', 1, 1, 0).
python_method('SumdQueryHandler', 'can_handle', 1, 1, 0).
python_method('SumdQueryHandler', 'handle', 1, 10, 10).
python_method('SumdQueryHandler', '_handle_get_sumd_document', 1, 3, 4).
python_method('SumdQueryHandler', '_handle_list_sumd_sections', 1, 3, 4).
python_method('SumdQueryHandler', '_handle_get_sumd_section', 1, 4, 5).
python_method('SumdQueryHandler', '_handle_get_project_info', 1, 3, 5).
python_method('SumdQueryHandler', '_handle_get_event_history', 1, 3, 4).
python_method('SumdQueryHandler', '_handle_get_all_events', 1, 3, 5).
python_method('SumdQueryHandler', '_handle_search_documents', 1, 6, 11).
python_method('SumdQueryHandler', '_handle_get_validation_results', 1, 4, 4).
python_method('SumdQueryHandler', '_handle_execute_dsl_query', 1, 2, 2).
python_class('sumd/cqrs/sumd_aggregate.py', 'SumdSection').
python_method('SumdSection', 'to_dict', 0, 1, 0).
python_method('SumdSection', 'from_dict', 2, 1, 2).
python_class('sumd/cqrs/sumd_aggregate.py', 'SumdDocumentState').
python_class('sumd/cqrs/sumd_aggregate.py', 'SumdAggregate').
python_method('SumdAggregate', '__init__', 1, 1, 3).
python_method('SumdAggregate', 'state', 0, 1, 0).
python_method('SumdAggregate', '_when', 1, 6, 6).
python_method('SumdAggregate', '_when_document_created', 1, 1, 1).
python_method('SumdAggregate', '_when_document_updated', 1, 6, 2).
python_method('SumdAggregate', '_when_section_added', 1, 3, 4).
python_method('SumdAggregate', '_when_section_removed', 1, 3, 2).
python_method('SumdAggregate', '_when_document_validated', 1, 1, 1).
python_method('SumdAggregate', 'create_document', 4, 2, 3).
python_method('SumdAggregate', 'update_document', 1, 2, 3).
python_method('SumdAggregate', 'add_section', 5, 3, 3).
python_method('SumdAggregate', 'remove_section', 1, 4, 5).
python_method('SumdAggregate', 'validate_document', 2, 2, 3).
python_method('SumdAggregate', 'get_section', 1, 3, 1).
python_method('SumdAggregate', 'has_section', 1, 1, 1).
python_method('SumdAggregate', 'get_state', 0, 5, 5).
python_method('SumdAggregate', 'create_from_file', 2, 6, 10).
python_class('sumd/dsl/ast_nodes.py', 'DSLExpressionType').
python_class('sumd/dsl/ast_nodes.py', 'DSLExpression').
python_method('DSLExpression', '__str__', 0, 11, 2).
python_class('sumd/dsl/commands.py', 'DSLCommand').
python_method('DSLCommand', '__post_init__', 0, 2, 0).
python_class('sumd/dsl/commands.py', 'DSLCommandRegistry').
python_method('DSLCommandRegistry', '__init__', 0, 1, 0).
python_method('DSLCommandRegistry', 'register', 1, 4, 1).
python_method('DSLCommandRegistry', 'get_command', 1, 1, 1).
python_method('DSLCommandRegistry', 'list_commands', 1, 5, 3).
python_method('DSLCommandRegistry', 'list_categories', 0, 1, 2).
python_method('DSLCommandRegistry', 'get_help', 1, 7, 4).
python_class('sumd/dsl/context_mixin.py', 'VariableMixin').
python_method('VariableMixin', 'set_variable', 2, 1, 0).
python_method('VariableMixin', 'get_variable', 1, 1, 1).
python_class('sumd/dsl/engine.py', 'DSLContext').
python_method('DSLContext', '__init__', 1, 2, 1).
python_method('DSLContext', 'register_function', 2, 1, 0).
python_method('DSLContext', 'get_function', 1, 1, 1).
python_class('sumd/dsl/engine.py', 'DSLEngine').
python_method('DSLEngine', '__init__', 3, 2, 4).
python_method('DSLEngine', 'execute', 2, 1, 1).
python_method('DSLEngine', 'execute_text', 2, 3, 5).
python_method('DSLEngine', '_is_natural_language', 1, 4, 4).
python_method('DSLEngine', 'process_natural_language', 1, 1, 1).
python_method('DSLEngine', 'get_suggestions', 1, 1, 1).
python_method('DSLEngine', '_build_dispatch_table', 0, 1, 0).
python_method('DSLEngine', '_execute_expression', 2, 5, 5).
python_method('DSLEngine', '_execute_assignment', 2, 3, 4).
python_method('DSLEngine', '_resolve_schema_call', 3, 4, 4).
python_method('DSLEngine', '_evaluate_args', 2, 2, 1).
python_method('DSLEngine', '_execute_command', 2, 6, 5).
python_method('DSLEngine', '_execute_function_call', 2, 4, 4).
python_method('DSLEngine', '_execute_property_access', 2, 5, 5).
python_method('DSLEngine', '_execute_comparison', 2, 4, 8).
python_method('DSLEngine', '_execute_logical', 2, 9, 3).
python_method('DSLEngine', '_execute_arithmetic', 2, 5, 5).
python_method('DSLEngine', '_execute_pipeline', 2, 6, 4).
python_method('DSLEngine', '_execute_list', 2, 2, 2).
python_method('DSLEngine', '_execute_dict', 2, 2, 3).
python_method('DSLEngine', '_execute_block', 2, 2, 1).
python_method('DSLEngine', '_execute_sumd_command', 3, 5, 6).
python_method('DSLEngine', '_call_function', 3, 2, 2).
python_method('DSLEngine', '_initialize_builtin_functions', 0, 1, 0).
python_method('DSLEngine', '_builtin_print', 2, 1, 1).
python_method('DSLEngine', '_builtin_len', 2, 2, 2).
python_method('DSLEngine', '_builtin_str', 2, 2, 2).
python_method('DSLEngine', '_builtin_int', 2, 2, 2).
python_method('DSLEngine', '_builtin_float', 2, 2, 2).
python_method('DSLEngine', '_builtin_bool', 2, 2, 2).
python_method('DSLEngine', '_builtin_type', 2, 2, 2).
python_method('DSLEngine', '_builtin_write_file', 3, 1, 2).
python_method('DSLEngine', '_builtin_list_files', 2, 3, 4).
python_method('DSLEngine', '_builtin_cwd', 1, 1, 1).
python_method('DSLEngine', '_builtin_cd', 2, 2, 3).
python_method('DSLEngine', '_builtin_help', 1, 1, 1).
python_class('sumd/dsl/lexer.py', 'DSLTokenType').
python_class('sumd/dsl/lexer.py', 'DSLToken').
python_class('sumd/dsl/lexer.py', 'DSLLexer').
python_method('DSLLexer', '__init__', 1, 1, 0).
python_method('DSLLexer', 'tokenize', 0, 7, 8).
python_class('sumd/dsl/nlp.py', 'NLPProcessor').
python_method('NLPProcessor', '__init__', 1, 1, 2).
python_method('NLPProcessor', '_initialize_default_intents', 0, 1, 1).
python_method('NLPProcessor', '_initialize_default_entities', 0, 1, 1).
python_method('NLPProcessor', 'parse_natural_language', 1, 4, 6).
python_method('NLPProcessor', '_text_matches_intent', 2, 1, 5).
python_method('NLPProcessor', '_extract_entities', 2, 4, 2).
python_method('NLPProcessor', '_extract_entity_value', 2, 5, 3).
python_method('NLPProcessor', '_extract_command_fallback', 1, 3, 3).
python_method('NLPProcessor', '_extract_entities_fallback', 1, 3, 1).
python_method('NLPProcessor', 'generate_dsl_command', 2, 7, 5).
python_method('NLPProcessor', 'suggest_commands', 1, 4, 6).
python_class('sumd/dsl/nlp.py', 'NLPIntegration').
python_method('NLPIntegration', '__init__', 1, 1, 1).
python_method('NLPIntegration', 'process_natural_language', 1, 3, 4).
python_method('NLPIntegration', 'get_suggestions', 1, 2, 1).
python_method('NLPIntegration', 'add_custom_intent', 1, 1, 0).
python_method('NLPIntegration', 'add_custom_entity', 1, 1, 0).
python_method('NLPIntegration', 'get_available_intents', 0, 1, 2).
python_method('NLPIntegration', 'get_intent_examples', 1, 2, 0).
python_class('sumd/dsl/nlp.py', 'SimpleNLPModel').
python_method('SimpleNLPModel', '__init__', 0, 1, 0).
python_method('SimpleNLPModel', 'predict_intent', 1, 5, 4).
python_method('SimpleNLPModel', 'extract_entities', 2, 4, 1).
python_class('sumd/dsl/parser.py', 'DSLParser').
python_method('DSLParser', 'parse', 0, 6, 7).
python_method('DSLParser', '_looks_like_command', 0, 3, 3).
python_method('DSLParser', '_peek_next_type', 0, 2, 1).
python_method('DSLParser', '_is_command_boundary', 0, 4, 2).
python_method('DSLParser', '_collect_command_args', 0, 5, 5).
python_method('DSLParser', '_build_pipeline_or_cmd', 2, 4, 3).
python_method('DSLParser', '_try_parse_command', 0, 4, 5).
python_method('DSLParser', '_parse_statement', 0, 4, 4).
python_method('DSLParser', '_parse_pipeline', 0, 2, 4).
python_method('DSLParser', '_parse_assignment', 0, 3, 5).
python_class('sumd/dsl/parser_base.py', 'DSLParserBase').
python_method('DSLParserBase', '__init__', 1, 1, 0).
python_method('DSLParserBase', '_is_at_end', 0, 1, 1).
python_method('DSLParserBase', '_peek', 0, 1, 0).
python_method('DSLParserBase', '_previous', 0, 1, 0).
python_method('DSLParserBase', '_advance', 0, 2, 2).
python_method('DSLParserBase', '_check', 2, 5, 2).
python_method('DSLParserBase', '_check_next', 2, 5, 1).
python_method('DSLParserBase', '_match', 2, 2, 2).
python_method('DSLParserBase', '_consume', 2, 2, 4).
python_class('sumd/dsl/parser_expr.py', 'DSLExpressionParser').
python_method('DSLExpressionParser', '_parse_logical_or', 0, 2, 4).
python_method('DSLExpressionParser', '_parse_logical_and', 0, 2, 4).
python_method('DSLExpressionParser', '_parse_comparison', 0, 2, 4).
python_method('DSLExpressionParser', '_parse_arithmetic', 0, 3, 4).
python_method('DSLExpressionParser', '_parse_term', 0, 4, 4).
python_method('DSLExpressionParser', '_parse_factor', 0, 3, 5).
python_class('sumd/dsl/parser_primary.py', 'DSLPrimaryParser').
python_method('DSLPrimaryParser', '_parse_paren_or_collection', 0, 4, 5).
python_method('DSLPrimaryParser', '_parse_identifier_command', 1, 6, 3).
python_method('DSLPrimaryParser', '_parse_identifier_forms', 0, 7, 8).
python_method('DSLPrimaryParser', '_parse_literal_value', 0, 6, 5).
python_method('DSLPrimaryParser', '_parse_primary', 0, 5, 7).
python_method('DSLPrimaryParser', '_parse_command', 0, 6, 6).
python_method('DSLPrimaryParser', '_parse_function_call', 0, 3, 7).
python_method('DSLPrimaryParser', '_parse_property_access', 0, 1, 2).
python_method('DSLPrimaryParser', '_parse_list', 0, 3, 6).
python_method('DSLPrimaryParser', '_parse_dict', 0, 3, 7).
python_class('sumd/dsl/schema.py', 'DSLDataType').
python_class('sumd/dsl/schema.py', 'DSLCommandType').
python_class('sumd/dsl/schema.py', 'DSLActionType').
python_class('sumd/dsl/schema.py', 'DSLParameter').
python_class('sumd/dsl/schema.py', 'DSLCommandSchema').
python_class('sumd/dsl/schema.py', 'DSLProjectSchema').
python_class('sumd/dsl/schema.py', 'DSLExpression').
python_class('sumd/dsl/schema.py', 'DSLStatement').
python_class('sumd/dsl/schema.py', 'DSLScript').
python_class('sumd/dsl/schema.py', 'NLPIntent').
python_class('sumd/dsl/schema.py', 'NLPEntity').
python_class('sumd/dsl/schema.py', 'NLPModel').
python_class('sumd/dsl/schema.py', 'DSLContext').
python_method('DSLContext', 'register_function', 2, 1, 0).
python_class('sumd/dsl/schema.py', 'DSLCommandResult').
python_class('sumd/dsl/schema_commands.py', 'SchemaCommandRegistry').
python_method('SchemaCommandRegistry', '__init__', 1, 1, 2).
python_method('SchemaCommandRegistry', '_register_commands', 0, 3, 0).
python_method('SchemaCommandRegistry', 'get_command', 1, 3, 0).
python_method('SchemaCommandRegistry', 'list_commands', 1, 4, 2).
python_method('SchemaCommandRegistry', 'validate_command_call', 2, 8, 3).
python_method('SchemaCommandRegistry', '_validate_parameter_type', 2, 2, 2).
python_method('SchemaCommandRegistry', 'process_natural_language', 1, 1, 1).
python_method('SchemaCommandRegistry', 'get_suggestions', 1, 1, 1).
python_class('sumd/dsl/schema_commands.py', 'SchemaBasedCommands').
python_method('SchemaBasedCommands', '__init__', 2, 1, 1).
python_method('SchemaBasedCommands', 'execute_command', 2, 10, 11).
python_method('SchemaBasedCommands', '_execute_sumd_command', 2, 4, 3).
python_method('SchemaBasedCommands', '_execute_file_command', 2, 4, 3).
python_method('SchemaBasedCommands', '_execute_search_command', 2, 3, 2).
python_method('SchemaBasedCommands', '_execute_utility_command', 2, 4, 3).
python_method('SchemaBasedCommands', '_execute_nlp_command', 2, 4, 3).
python_method('SchemaBasedCommands', '_execute_schema_command', 2, 4, 3).
python_method('SchemaBasedCommands', '_cmd_sumd_scan', 1, 2, 3).
python_method('SchemaBasedCommands', '_cmd_sumd_validate', 1, 2, 5).
python_method('SchemaBasedCommands', '_cmd_sumd_info', 1, 3, 2).
python_method('SchemaBasedCommands', '_cmd_cat', 1, 2, 2).
python_method('SchemaBasedCommands', '_cmd_ls', 1, 3, 5).
python_method('SchemaBasedCommands', '_cmd_edit', 1, 2, 3).
python_method('SchemaBasedCommands', '_cmd_find', 1, 4, 6).
python_method('SchemaBasedCommands', '_cmd_grep', 1, 7, 8).
python_method('SchemaBasedCommands', '_cmd_echo', 1, 1, 1).
python_method('SchemaBasedCommands', '_cmd_pwd', 1, 1, 1).
python_method('SchemaBasedCommands', '_cmd_cd', 1, 2, 4).
python_method('SchemaBasedCommands', '_cmd_ask', 1, 5, 3).
python_method('SchemaBasedCommands', '_cmd_summarize', 1, 2, 2).
python_method('SchemaBasedCommands', '_cmd_analyze_sentiment', 1, 8, 6).
python_method('SchemaBasedCommands', '_cmd_schema_info', 1, 1, 1).
python_method('SchemaBasedCommands', '_cmd_list_commands', 1, 4, 5).
python_method('SchemaBasedCommands', '_cmd_command_help', 1, 4, 2).
python_class('sumd/dsl/shell.py', 'DSLShell').
python_method('DSLShell', '__init__', 3, 2, 6).
python_method('DSLShell', '_setup_readline', 0, 3, 6).
python_method('DSLShell', '_completer', 2, 10, 5).
python_method('DSLShell', '_register_commands', 0, 3, 2).
python_method('DSLShell', 'run', 0, 9, 8).
python_method('DSLShell', '_get_prompt', 0, 1, 0).
python_method('DSLShell', '_handle_shell_command', 1, 14, 8).
python_method('DSLShell', '_execute_line', 1, 9, 6).
python_method('DSLShell', 'execute_script', 1, 9, 12).
python_method('DSLShell', 'execute_command', 1, 2, 3).
python_class('sumd/dsl/shell.py', 'DSLShellServer').
python_method('DSLShellServer', '__init__', 1, 2, 2).
python_method('DSLShellServer', 'execute_dsl', 2, 4, 5).
python_method('DSLShellServer', 'get_shell_info', 0, 2, 4).
python_class('sumd/models.py', 'SectionType').
python_class('sumd/models.py', 'Section').
python_class('sumd/models.py', 'SUMDDocument').
python_class('sumd/parser.py', 'SUMDParser').
python_method('SUMDParser', '__init__', 0, 1, 0).
python_method('SUMDParser', 'parse', 1, 1, 4).
python_method('SUMDParser', 'parse_file', 1, 1, 2).
python_method('SUMDParser', '_parse_header', 1, 9, 7).
python_method('SUMDParser', '_parse_sections', 1, 6, 7).
python_method('SUMDParser', 'validate', 1, 6, 1).
python_class('sumd/pipeline.py', 'RenderPipeline').
python_method('RenderPipeline', '__init__', 2, 1, 1).
python_method('RenderPipeline', '_collect', 0, 3, 23).
python_method('RenderPipeline', '_build_registered_sections', 2, 4, 6).
python_method('RenderPipeline', '_render_legacy_sections', 1, 1, 0).
python_method('RenderPipeline', '_assemble', 2, 4, 5).
python_method('RenderPipeline', 'run', 2, 2, 3).
python_class('sumd/sections/api_stubs.py', 'ApiStubsSection').
python_method('ApiStubsSection', 'should_render', 1, 1, 2).
python_class('sumd/sections/architecture.py', 'ArchitectureSection').
python_class('sumd/sections/base.py', 'RenderContext').
python_class('sumd/sections/base.py', 'Section').
python_method('Section', 'should_render', 1, 1, 0).
python_method('Section', 'render', 1, 1, 0).
python_class('sumd/sections/call_graph.py', 'CallGraphSection').
python_method('CallGraphSection', 'should_render', 1, 2, 2).
python_class('sumd/sections/code_analysis.py', 'CodeAnalysisSection').
python_method('CodeAnalysisSection', 'should_render', 1, 3, 2).
python_method('CodeAnalysisSection', 'render', 1, 1, 1).
python_class('sumd/sections/configuration.py', 'ConfigurationSection').
python_class('sumd/sections/dependencies.py', 'DependenciesSection').
python_method('DependenciesSection', 'should_render', 1, 4, 2).
python_class('sumd/sections/deployment.py', 'DeploymentSection').
python_class('sumd/sections/environment.py', 'EnvironmentSection').
python_method('EnvironmentSection', 'should_render', 1, 2, 2).
python_method('EnvironmentSection', 'render', 1, 1, 3).
python_class('sumd/sections/extras.py', 'ExtrasSection').
python_method('ExtrasSection', 'should_render', 1, 2, 2).
python_class('sumd/sections/interfaces.py', 'InterfacesSection').
python_method('InterfacesSection', 'should_render', 1, 3, 2).
python_class('sumd/sections/metadata.py', 'MetadataSection').
python_method('MetadataSection', 'render', 1, 5, 3).
python_class('sumd/sections/quality.py', 'QualitySection').
python_class('sumd/sections/refactor_analysis.py', 'RefactorAnalysisSection').
python_method('RefactorAnalysisSection', 'render', 1, 3, 2).
python_class('sumd/sections/source_snippets.py', 'SourceSnippetsSection').
python_class('sumd/sections/swop.py', 'SwopSection').
python_method('SwopSection', 'should_render', 1, 1, 2).
python_class('sumd/sections/test_contracts.py', 'TestContractsSection').
python_class('sumd/sections/workflows.py', 'WorkflowsSection').
python_method('WorkflowsSection', 'should_render', 1, 2, 2).
python_class('sumd/utils/prolog_core.py', 'Variable').
python_method('Variable', '__init__', 1, 2, 0).
python_method('Variable', '__repr__', 0, 2, 0).
python_method('Variable', '__eq__', 1, 3, 1).
python_method('Variable', '__hash__', 0, 1, 1).
python_class('sumd/utils/prolog_core.py', 'Term').
python_method('Term', '__init__', 1, 2, 1).
python_method('Term', '__repr__', 0, 2, 2).
python_method('Term', '__eq__', 1, 3, 1).
python_class('sumd/utils/prolog_core.py', 'Rule').
python_method('Rule', '__init__', 2, 2, 0).
python_method('Rule', '__repr__', 0, 2, 2).
python_class('sumd/utils/prolog_core.py', 'PythonPrologDB').
python_method('PythonPrologDB', '__init__', 0, 2, 0).
python_method('PythonPrologDB', 'add_fact', 1, 2, 4).
python_method('PythonPrologDB', 'add_rule', 2, 1, 2).
python_method('PythonPrologDB', 'parse_and_load', 1, 7, 8).
python_class('sumd/utils/prolog_core.py', 'PythonPrologEngine').
python_method('PythonPrologEngine', '__init__', 1, 2, 0).
python_method('PythonPrologEngine', 'query', 1, 5, 7).
python_method('PythonPrologEngine', '_find_vars', 1, 1, 5).
python_method('PythonPrologEngine', '_resolve', 2, 12, 7).
python_class('sumd/utils/prolog_core.py', 'HybridPrologEngine').
python_method('HybridPrologEngine', '__init__', 1, 2, 8).
python_method('HybridPrologEngine', 'query', 1, 5, 6).
python_method('HybridPrologEngine', '_query_pyswip', 1, 4, 8).
python_method('HybridPrologEngine', '_query_subprocess', 1, 9, 10).
python_method('HybridPrologEngine', '_query_python', 1, 1, 1).
python_method('HybridPrologEngine', '_swipl_executable_exists', 0, 2, 1).
python_class('sumd/validator.py', 'CodeBlockIssue').
python_class('tests/test_cli.py', 'TestValidateCommand').
python_method('TestValidateCommand', 'test_valid_file_exits_zero', 1, 2, 3).
python_method('TestValidateCommand', 'test_valid_file_prints_ok', 1, 2, 4).
python_method('TestValidateCommand', 'test_missing_file_exits_nonzero', 1, 2, 3).
python_class('tests/test_cli.py', 'TestInfoCommand').
python_method('TestInfoCommand', 'test_info_runs', 1, 2, 3).
python_class('tests/test_cli.py', 'TestExportCommand').
python_method('TestExportCommand', 'test_export_json', 1, 4, 6).
python_method('TestExportCommand', 'test_export_to_output_file', 2, 3, 4).
python_method('TestExportCommand', 'test_export_markdown', 1, 2, 3).
python_class('tests/test_cli.py', 'TestCliVersion').
python_method('TestCliVersion', 'test_version_option', 0, 3, 2).
python_class('tests/test_cli.py', 'TestCliHelp').
python_method('TestCliHelp', 'test_help', 0, 3, 3).
python_method('TestCliHelp', 'test_validate_help', 0, 2, 2).
python_method('TestCliHelp', 'test_export_help', 0, 2, 2).
python_method('TestCliHelp', 'test_scan_help', 0, 2, 2).
python_class('tests/test_cli.py', 'TestProjectDetection').
python_method('TestProjectDetection', 'test_is_project_dir_accepts_language_marker', 3, 3, 4).
python_method('TestProjectDetection', 'test_is_project_dir_accepts_glob_markers', 3, 3, 4).
python_method('TestProjectDetection', 'test_empty_dir_is_not_project', 1, 3, 2).
python_method('TestProjectDetection', 'test_detect_projects_finds_mixed_languages', 1, 3, 3).
python_method('TestProjectDetection', 'test_detect_projects_non_recursive_skips_nested', 1, 3, 3).
python_method('TestProjectDetection', 'test_detect_projects_recursive_finds_nested', 1, 3, 3).
python_class('tests/test_cli.py', 'TestNodeSpecFromPackageJson').
python_method('TestNodeSpecFromPackageJson', 'test_framework_detection', 2, 2, 3).
python_method('TestNodeSpecFromPackageJson', 'test_spec_uses_real_scripts_and_extras', 0, 8, 1).
python_method('TestNodeSpecFromPackageJson', 'test_spec_falls_back_without_scripts', 0, 6, 1).
python_class('tests/test_cli.py', 'TestGenerateDoqlLess').
python_method('TestGenerateDoqlLess', '_pkg', 1, 1, 3).
python_method('TestGenerateDoqlLess', 'test_fresh_generation_for_node_uses_real_scripts', 1, 6, 4).
python_method('TestGenerateDoqlLess', 'test_force_regenerates_autogen_file_without_duplicating', 1, 4, 4).
python_method('TestGenerateDoqlLess', 'test_force_preserves_user_authored_file', 1, 5, 5).
python_method('TestGenerateDoqlLess', 'test_no_force_skips_existing', 1, 3, 4).
python_class('tests/test_cqrs_es.py', 'TestEventStore').
python_method('TestEventStore', 'test_save_and_get_events', 0, 4, 7).
python_method('TestEventStore', 'test_persistence', 0, 3, 7).
python_method('TestEventStore', 'test_get_events_from_version', 0, 4, 8).
python_class('tests/test_cqrs_es.py', 'TestSumdAggregate').
python_method('TestSumdAggregate', 'test_create_document', 0, 9, 4).
python_method('TestSumdAggregate', 'test_add_section', 0, 6, 5).
python_method('TestSumdAggregate', 'test_remove_section', 0, 3, 6).
python_method('TestSumdAggregate', 'test_load_from_history', 0, 5, 11).
python_class('tests/test_cqrs_es.py', 'TestCommandBus').
python_method('TestCommandBus', 'test_dispatch_command', 0, 5, 10).
python_class('tests/test_cqrs_es.py', 'TestQueryBus').
python_method('TestQueryBus', 'test_dispatch_query', 0, 4, 11).
python_class('tests/test_cqrs_es.py', 'TestEventSourcedRepository').
python_method('TestEventSourcedRepository', 'test_save_and_get_aggregate', 0, 5, 8).
python_class('tests/test_cqrs_es.py', 'TestIntegration').
python_method('TestIntegration', 'test_full_workflow', 0, 9, 18).
python_class('tests/test_dsl.py', 'TestDSLLexer').
python_method('TestDSLLexer', 'test_tokenize_simple_command', 0, 7, 3).
python_method('TestDSLLexer', 'test_tokenize_function_call', 0, 6, 3).
python_method('TestDSLLexer', 'test_tokenize_arithmetic', 0, 7, 3).
python_method('TestDSLLexer', 'test_tokenize_string_literals', 0, 4, 3).
python_method('TestDSLLexer', 'test_tokenize_comments', 0, 4, 3).
python_class('tests/test_dsl.py', 'TestDSLParser').
python_method('TestDSLParser', 'test_parse_simple_command', 0, 5, 2).
python_method('TestDSLParser', 'test_parse_function_call', 0, 6, 2).
python_method('TestDSLParser', 'test_parse_arithmetic', 0, 7, 2).
python_method('TestDSLParser', 'test_parse_assignment', 0, 6, 2).
python_method('TestDSLParser', 'test_parse_pipeline', 0, 5, 2).
python_method('TestDSLParser', 'test_parse_comparison', 0, 6, 2).
python_method('TestDSLParser', 'test_parse_logical', 0, 6, 2).
python_class('tests/test_dsl.py', 'TestDSLEngine').
python_method('TestDSLEngine', 'test_execute_literal', 0, 4, 4).
python_method('TestDSLEngine', 'test_execute_arithmetic', 0, 4, 4).
python_method('TestDSLEngine', 'test_execute_comparison', 0, 4, 4).
python_method('TestDSLEngine', 'test_execute_logical', 0, 4, 4).
python_method('TestDSLEngine', 'test_execute_assignment', 0, 3, 5).
python_method('TestDSLEngine', 'test_execute_function_call', 0, 3, 4).
python_method('TestDSLEngine', 'test_execute_pipeline', 0, 3, 5).
python_class('tests/test_dsl.py', 'TestDSLCommandRegistry').
python_method('TestDSLCommandRegistry', 'test_builtin_registry', 0, 7, 4).
python_method('TestDSLCommandRegistry', 'test_command_categories', 0, 5, 4).
python_method('TestDSLCommandRegistry', 'test_help_system', 0, 5, 2).
python_class('tests/test_dsl.py', 'TestDSLShell').
python_method('TestDSLShell', 'test_shell_initialization', 0, 4, 3).
python_method('TestDSLShell', 'test_execute_command', 0, 5, 5).
python_method('TestDSLShell', 'test_execute_script', 0, 3, 6).
python_class('tests/test_dsl.py', 'TestDSLIntegration').
python_method('TestDSLIntegration', 'test_dsl_with_sumd_commands', 0, 4, 6).
python_method('TestDSLIntegration', 'test_complex_dsl_expressions', 0, 4, 4).
python_method('TestDSLIntegration', 'test_error_handling', 0, 2, 6).
python_class('tests/test_extractor.py', 'TestExtractPyproject').
python_method('TestExtractPyproject', 'test_missing_file_returns_empty', 1, 2, 1).
python_method('TestExtractPyproject', 'test_basic_fields', 1, 4, 2).
python_method('TestExtractPyproject', 'test_dependencies_parsed', 1, 3, 2).
python_method('TestExtractPyproject', 'test_dev_dependencies_from_optional', 1, 2, 2).
python_method('TestExtractPyproject', 'test_fallback_name_is_dir_name', 1, 2, 2).
python_method('TestExtractPyproject', 'test_corrupt_toml_returns_empty', 1, 2, 2).
python_class('tests/test_extractor.py', 'TestExtractTaskfile').
python_method('TestExtractTaskfile', 'test_missing_returns_empty', 1, 2, 1).
python_method('TestExtractTaskfile', 'test_parses_tasks', 1, 5, 3).
python_method('TestExtractTaskfile', 'test_task_without_desc', 1, 2, 2).
python_method('TestExtractTaskfile', 'test_multiple_tasks', 1, 4, 2).
python_class('tests/test_extractor.py', 'TestExtractPyqual').
python_method('TestExtractPyqual', 'test_missing_returns_empty', 1, 2, 1).
python_method('TestExtractPyqual', 'test_parses_pipeline', 1, 4, 2).
python_method('TestExtractPyqual', 'test_flat_format', 1, 2, 2).
python_class('tests/test_extractor.py', 'TestExtractPythonModules').
python_method('TestExtractPythonModules', 'test_missing_pkg_dir_returns_empty', 1, 2, 1).
python_method('TestExtractPythonModules', 'test_lists_modules', 1, 4, 3).
python_method('TestExtractPythonModules', 'test_excludes_dunder_files', 1, 2, 3).
python_class('tests/test_extractor.py', 'TestExtractReadmeTitle').
python_method('TestExtractReadmeTitle', 'test_missing_returns_empty', 1, 2, 1).
python_method('TestExtractReadmeTitle', 'test_extracts_h1', 1, 2, 2).
python_method('TestExtractReadmeTitle', 'test_no_h1_returns_empty', 1, 2, 2).
python_method('TestExtractReadmeTitle', 'test_first_h1_only', 1, 2, 2).
python_class('tests/test_extractor.py', 'TestExtractEnv').
python_method('TestExtractEnv', 'test_missing_returns_empty', 1, 2, 1).
python_method('TestExtractEnv', 'test_parses_key_value', 1, 4, 2).
python_method('TestExtractEnv', 'test_captures_preceding_comment', 1, 2, 2).
python_method('TestExtractEnv', 'test_captures_inline_comment', 1, 3, 2).
python_method('TestExtractEnv', 'test_empty_value_becomes_not_set', 1, 2, 2).
python_class('tests/test_extractor.py', 'TestExtractGoal').
python_method('TestExtractGoal', 'test_missing_returns_empty', 1, 2, 1).
python_method('TestExtractGoal', 'test_parses_project_and_versioning', 1, 4, 2).
python_class('tests/test_extractor.py', 'TestExtractProjectAnalysis').
python_method('TestExtractProjectAnalysis', 'test_missing_project_dir_returns_empty', 1, 2, 1).
python_method('TestExtractProjectAnalysis', 'test_loads_calls_toon_yaml', 1, 4, 4).
python_method('TestExtractProjectAnalysis', 'test_refactor_mode_loads_extra_files', 1, 6, 3).
python_method('TestExtractProjectAnalysis', 'test_missing_files_skipped', 1, 2, 2).
python_class('tests/test_extractor.py', 'TestExtractRequirements').
python_method('TestExtractRequirements', 'test_no_requirements_returns_empty', 1, 2, 1).
python_method('TestExtractRequirements', 'test_parses_requirements_txt', 1, 3, 3).
python_method('TestExtractRequirements', 'test_ignores_comments_and_flags', 1, 2, 2).
python_class('tests/test_extractor.py', 'TestExtractMakefile').
python_method('TestExtractMakefile', 'test_missing_returns_empty', 1, 2, 1).
python_method('TestExtractMakefile', 'test_parses_targets', 1, 4, 2).
python_method('TestExtractMakefile', 'test_comment_captured', 1, 2, 2).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPCQRSCommands').
python_method('TestMCPCQRSCommands', 'test_execute_command', 0, 6, 6).
python_method('TestMCPCQRSCommands', 'test_execute_command_error', 0, 3, 4).
python_method('TestMCPCQRSCommands', 'test_execute_query', 0, 4, 5).
python_method('TestMCPCQRSCommands', 'test_get_events', 0, 7, 4).
python_method('TestMCPCQRSCommands', 'test_get_aggregate', 0, 5, 5).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPDSLCommands').
python_method('TestMCPDSLCommands', 'test_execute_dsl', 0, 5, 5).
python_method('TestMCPDSLCommands', 'test_dsl_shell_info', 0, 7, 4).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPIntegration').
python_method('TestMCPIntegration', 'test_full_cqrs_workflow_via_mcp', 0, 5, 17).
python_method('TestMCPIntegration', 'test_dsl_integration_via_mcp', 0, 6, 7).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPErrorHandling').
python_method('TestMCPErrorHandling', 'test_unknown_command_type', 0, 3, 2).
python_method('TestMCPErrorHandling', 'test_unknown_query_type', 0, 3, 2).
python_method('TestMCPErrorHandling', 'test_aggregate_not_found', 0, 3, 3).
python_class('tests/test_mcp_server.py', 'TestDocToDict').
python_method('TestDocToDict', 'test_has_required_keys', 1, 5, 3).
python_method('TestDocToDict', 'test_section_has_fields', 1, 6, 2).
python_class('tests/test_mcp_server.py', 'TestResolvePath').
python_method('TestResolvePath', 'test_absolute_path_unchanged', 1, 2, 2).
python_method('TestResolvePath', 'test_relative_resolves_from_cwd', 0, 3, 2).
python_class('tests/test_mcp_server.py', 'TestListTools').
python_method('TestListTools', 'test_returns_thirteen_tools', 0, 2, 3).
python_method('TestListTools', 'test_tool_names', 0, 3, 2).
python_method('TestListTools', 'test_each_tool_has_input_schema', 0, 3, 2).
python_class('tests/test_mcp_server.py', 'TestParseSumd').
python_method('TestParseSumd', 'test_returns_json', 1, 3, 4).
python_method('TestParseSumd', 'test_missing_file_returns_error', 1, 2, 3).
python_class('tests/test_mcp_server.py', 'TestValidateSumd').
python_method('TestValidateSumd', 'test_valid_file', 1, 3, 4).
python_method('TestValidateSumd', 'test_missing_file_returns_error', 1, 2, 3).
python_class('tests/test_mcp_server.py', 'TestExportSumd').
python_method('TestExportSumd', 'test_export_json', 1, 2, 3).
python_method('TestExportSumd', 'test_export_markdown', 1, 2, 2).
python_method('TestExportSumd', 'test_export_to_file', 2, 3, 3).
python_class('tests/test_mcp_server.py', 'TestListSections').
python_method('TestListSections', 'test_returns_list', 1, 3, 5).
python_method('TestListSections', 'test_section_has_name', 1, 2, 4).
python_class('tests/test_mcp_server.py', 'TestGetSection').
python_method('TestGetSection', 'test_found_section', 1, 2, 4).
python_method('TestGetSection', 'test_missing_section', 1, 2, 3).
python_class('tests/test_mcp_server.py', 'TestInfoSumd').
python_method('TestInfoSumd', 'test_returns_info', 1, 4, 4).
python_class('tests/test_mcp_server.py', 'TestGenerateSumd').
python_method('TestGenerateSumd', 'test_generate_content', 0, 3, 1).
python_method('TestGenerateSumd', 'test_generate_to_file', 1, 3, 3).
python_class('tests/test_mcp_server.py', 'TestUnknownTool').
python_method('TestUnknownTool', 'test_unknown_returns_error', 0, 2, 2).
python_class('tests/test_sections.py', 'TestMetadataSection').
python_method('TestMetadataSection', 'test_always_renders', 0, 2, 3).
python_method('TestMetadataSection', 'test_contains_name_and_version', 0, 3, 4).
python_method('TestMetadataSection', 'test_contains_metadata_header', 0, 2, 3).
python_method('TestMetadataSection', 'test_optional_fields_omitted_when_empty', 0, 2, 4).
python_class('tests/test_sections.py', 'TestArchitectureSection').
python_method('TestArchitectureSection', 'test_always_renders', 0, 2, 3).
python_method('TestArchitectureSection', 'test_header_present', 0, 2, 4).
python_method('TestArchitectureSection', 'test_modules_listed', 0, 3, 4).
python_method('TestArchitectureSection', 'test_no_modules_no_source_modules_section', 0, 2, 4).
python_class('tests/test_sections.py', 'TestDependenciesSection').
python_method('TestDependenciesSection', 'test_renders_when_deps_present', 0, 2, 3).
python_method('TestDependenciesSection', 'test_runtime_deps_listed', 0, 3, 4).
python_method('TestDependenciesSection', 'test_no_deps_shows_fallback', 0, 2, 4).
python_method('TestDependenciesSection', 'test_dev_deps_section', 0, 3, 4).
python_class('tests/test_sections.py', 'TestWorkflowsSection').
python_method('TestWorkflowsSection', 'test_no_render_when_empty', 0, 2, 3).
python_method('TestWorkflowsSection', 'test_renders_with_tasks', 0, 3, 5).
python_method('TestWorkflowsSection', 'test_header_present', 0, 2, 3).
python_class('tests/test_sections.py', 'TestQualitySection').
python_method('TestQualitySection', 'test_no_render_when_empty', 0, 2, 3).
python_method('TestQualitySection', 'test_renders_with_pyqual', 0, 2, 3).
python_method('TestQualitySection', 'test_pipeline_name_in_output', 0, 2, 4).
python_class('tests/test_sections.py', 'TestEnvironmentSection').
python_method('TestEnvironmentSection', 'test_no_render_when_empty', 0, 2, 3).
python_method('TestEnvironmentSection', 'test_renders_with_vars', 0, 3, 5).
python_class('tests/test_sections.py', 'TestCallGraphSection').
python_method('TestCallGraphSection', 'test_no_render_without_calls', 0, 2, 3).
python_method('TestCallGraphSection', 'test_no_render_without_calls_file', 0, 2, 3).
python_method('TestCallGraphSection', 'test_renders_with_calls_file', 0, 3, 5).
python_class('tests/test_sections.py', 'TestCodeAnalysisSection').
python_method('TestCodeAnalysisSection', 'test_no_render_when_only_calls', 0, 2, 3).
python_method('TestCodeAnalysisSection', 'test_renders_with_map', 0, 2, 3).
python_class('tests/test_sections.py', 'TestRefactorAnalysisSection').
python_method('TestRefactorAnalysisSection', 'test_no_render_when_empty', 0, 2, 3).
python_method('TestRefactorAnalysisSection', 'test_renders_with_analysis_files', 0, 5, 5).
python_method('TestRefactorAnalysisSection', 'test_map_toon_excluded', 0, 2, 4).
python_class('tests/test_sections.py', 'TestSourceSnippetsSection').
python_method('TestSourceSnippetsSection', 'test_no_render_when_empty', 0, 2, 3).
python_method('TestSourceSnippetsSection', 'test_renders_with_snippets', 0, 4, 5).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('help', 'Default target').
makefile_target('install', 'Installation').
makefile_target('install-dev', '').
makefile_target('test', 'Testing').
makefile_target('test-cov', '').
makefile_target('lint', 'Code quality').
makefile_target('format', '').
makefile_target('clean', 'Utilities').
makefile_target('publish', 'Release helpers').
makefile_target('publish-confirm', '').
makefile_target('publish-test', '').
makefile_target('version', '').

% ── Taskfile Tasks ───────────────────────────────────────
taskfile_task('', 'Install Python dependencies (editable)').
taskfile_task('', 'Upgrade all outdated Python packages in the project venv').
taskfile_task('', 'Run pyqual quality pipeline (uses pyqual.yaml from cwd)').
taskfile_task('', 'Run pyqual with auto-fix (uses pyqual.yaml from cwd)').
taskfile_task('', 'Generate pyqual quality report (uses pyqual.yaml from cwd)').
taskfile_task('', 'Run pytest suite').
taskfile_task('', 'Run pytest suite and generate HTML report').
taskfile_task('', 'Generate example testql HTML report').
taskfile_task('', 'Run ruff lint check').
taskfile_task('', 'Auto-format with ruff').
taskfile_task('', 'Build wheel + sdist').
taskfile_task('', 'Remove build artefacts').
taskfile_task('', 'Install, full check, generate SUMD docs').
taskfile_task('', 'Generate project structure (app.doql.less)').
taskfile_task('', 'Reverse-engineer sumd project structure (LESS format)').
taskfile_task('', 'Export app.doql.less to other formats').
taskfile_task('', 'Validate app.doql.less syntax').
taskfile_task('', 'Run doql health checks').
taskfile_task('', 'Generate code from app.doql.less').
taskfile_task('', 'Full doql analysis (structure + validate + doctor)').
taskfile_task('', 'Build documentation').
taskfile_task('', 'Generate SUMD.md (full project documentation)').
taskfile_task('', 'Generate SUMR.md (pre-refactoring analysis report)').
taskfile_task('', 'Bump patch version (hatch)').
taskfile_task('', 'Build and publish to PyPI').
taskfile_task('', 'Full pre-commit check (lint + test + quality)').
taskfile_task('', 'Smoke-test all external CLI tools used by this project').
taskfile_task('', 'Show available tasks').

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', '*(not set)*', 'Required: OpenRouter API key (https://openrouter.ai/keys)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Model (default: openrouter/qwen/qwen3-coder-next)').
env_variable('PFIX_AUTO_APPLY', 'true', 'true = apply fixes without asking').
env_variable('PFIX_AUTO_INSTALL_DEPS', 'true', 'true = auto pip/uv install').
env_variable('PFIX_AUTO_RESTART', 'false', 'true = os.execv restart after fix').
env_variable('PFIX_MAX_RETRIES', '3', '').
env_variable('PFIX_DRY_RUN', 'false', '').
env_variable('PFIX_ENABLED', 'true', '').
env_variable('PFIX_GIT_COMMIT', 'false', 'true = auto-commit fixes').
env_variable('PFIX_GIT_PREFIX', 'pfix:', 'commit message prefix').
env_variable('PFIX_CREATE_BACKUPS', 'false', 'false = disable .pfix_backups/ directory').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').
testql_scenario('generated-from-pytests.testql.toon.yaml', 'integration').
testql_scenario('sumd-cli.testql.toon.yaml', 'cli').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('sumd/rules.pl', 'file').
sumd_declared_file('.swop/manifests/core/commands.yml', 'swop').
sumd_declared_file('.swop/manifests/core/queries.yml', 'swop').
sumd_declared_file('.swop/manifests/core/events.yml', 'swop').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('testql-scenarios/generated-from-pytests.testql.toon.yaml', 'testql').
sumd_declared_file('testql-scenarios/sumd-cli.testql.toon.yaml', 'testql').
sumd_declared_file('Taskfile.yml', 'taskfile').
sumd_declared_file('pyqual.yaml', 'pyqual').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'click').
sumd_interface('cli', '').
sumd_workflow('install', 'manual').
sumd_workflow_step('install', 1, 'echo "📦 Installing sumd..."').
sumd_workflow_step('install', 2, 'if command -v uv > /dev/null 2>&1').
sumd_workflow_step('install', 3, 'uv pip install -e .').
sumd_workflow_step('install', 4, 'else \').
sumd_workflow_step('install', 5, 'pip install -e .').
sumd_workflow_step('install', 6, 'fi').
sumd_workflow_step('install', 7, 'echo "✅ Installation completed!"').
sumd_workflow('install-dev', 'manual').
sumd_workflow_step('install-dev', 1, 'echo "📦 Installing sumd with dev dependencies..."').
sumd_workflow_step('install-dev', 2, 'if command -v uv > /dev/null 2>&1').
sumd_workflow_step('install-dev', 3, 'uv pip install -e ".[dev]"').
sumd_workflow_step('install-dev', 4, 'else \').
sumd_workflow_step('install-dev', 5, 'pip install -e ".[dev]"').
sumd_workflow_step('install-dev', 6, 'fi').
sumd_workflow_step('install-dev', 7, 'echo "✅ Dev installation completed!"').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'echo "🧪 Running tests..."').
sumd_workflow_step('test', 2, '.venv/bin/python -m pytest tests/ -v --tb=short').
sumd_workflow('test-cov', 'manual').
sumd_workflow_step('test-cov', 1, 'echo "🧪 Running tests with coverage..."').
sumd_workflow_step('test-cov', 2, '.venv/bin/python -m pytest tests/ -v --cov=sumd --cov-report=term-missing --cov-report=json').
sumd_workflow('lint', 'manual').
sumd_workflow_step('lint', 1, 'echo "🔍 Running linting with ruff..."').
sumd_workflow_step('lint', 2, '.venv/bin/python -m ruff check sumd/').
sumd_workflow_step('lint', 3, '.venv/bin/python -m ruff check tests/').
sumd_workflow('format', 'manual').
sumd_workflow_step('format', 1, 'echo "📝 Formatting code with ruff..."').
sumd_workflow_step('format', 2, '.venv/bin/python -m ruff format sumd/').
sumd_workflow_step('format', 3, '.venv/bin/python -m ruff format tests/').
sumd_workflow('clean', 'manual').
sumd_workflow_step('clean', 1, 'echo "🧹 Cleaning temporary files..."').
sumd_workflow_step('clean', 2, 'find . -type f -name "*.pyc" -delete').
sumd_workflow_step('clean', 3, 'find . -type d -name "__pycache__" -delete').
sumd_workflow('publish', 'manual').
sumd_workflow_step('publish', 1, 'echo "📦 Publishing to PyPI..."').
sumd_workflow_step('publish', 2, 'command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build)').
sumd_workflow_step('publish', 3, 'rm -rf dist/ build/ *.egg-info/').
sumd_workflow_step('publish', 4, '.venv/bin/python -m build').
sumd_workflow_step('publish', 5, '.venv/bin/twine check dist/*').
sumd_workflow_step('publish', 6, 'echo "⚡ Ready to upload. Run: make publish-confirm to upload to PyPI"').
sumd_workflow('publish-confirm', 'manual').
sumd_workflow_step('publish-confirm', 1, 'echo "🚀 Uploading to PyPI..."').
sumd_workflow_step('publish-confirm', 2, '.venv/bin/twine upload dist/*').
sumd_workflow('publish-test', 'manual').
sumd_workflow_step('publish-test', 1, 'echo "📦 Publishing to TestPyPI..."').
sumd_workflow_step('publish-test', 2, 'command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build)').
sumd_workflow_step('publish-test', 3, 'rm -rf dist/ build/ *.egg-info/').
sumd_workflow_step('publish-test', 4, '.venv/bin/python -m build').
sumd_workflow_step('publish-test', 5, '.venv/bin/twine upload --repository testpypi dist/*').
sumd_workflow('version', 'manual').
sumd_workflow_step('version', 1, 'echo "📦 Version information..."').
sumd_workflow_step('version', 2, 'cat VERSION').
sumd_workflow_step('version', 3, '.venv/bin/python -c "from importlib.metadata import version').
sumd_workflow('deps:update', 'manual').
sumd_workflow('quality', 'manual').
sumd_workflow('quality:fix', 'manual').
sumd_quality_workflow('quality:fix', 'fix').
sumd_workflow('quality:report', 'manual').
sumd_quality_workflow('quality:report', 'report').
sumd_workflow('test:report', 'manual').
sumd_workflow('test:report:example', 'manual').
sumd_workflow('fmt', 'manual').
sumd_workflow_step('fmt', 1, 'ruff format .').
sumd_workflow('build', 'manual').
sumd_workflow('structure', 'manual').
sumd_workflow('doql:adopt', 'manual').
sumd_workflow('doql:export', 'manual').
sumd_workflow_step('doql:export', 1, 'if [ ! -f "app.doql.less" ]').
sumd_workflow('doql:validate', 'manual').
sumd_workflow('doql:doctor', 'manual').
sumd_workflow('doql:build', 'manual').
sumd_workflow('docs:build', 'manual').
sumd_workflow_step('docs:build', 1, 'echo "Building SUMD documentation..."').
sumd_workflow('sumd', 'manual').
sumd_workflow('sumr', 'manual').
sumd_workflow('version:bump', 'manual').
sumd_workflow_step('version:bump', 1, 'hatch version patch').
sumd_workflow_step('version:bump', 2, 'echo "✅ Version bumped:"').
sumd_workflow_step('version:bump', 3, 'hatch version').
sumd_workflow('doctor', 'manual').
sumd_workflow('help', 'manual').
sumd_workflow_step('help', 1, 'task --list').
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
def validate_codeblocks(content, source)  # CC=9, fan=11
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

*234 nodes · 224 edges · 33 modules · CC̄=3.6*

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
| `_handle_shell_command` *(in sumd.dsl.shell.DSLShell)* | 14 ⚠ | 0 | 24 | **24** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/oqlos/sumd
# generated in 0.12s
# nodes: 234 | edges: 224 | modules: 33
# CC̄=3.6

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
  sumd.dsl.shell.DSLShell._handle_shell_command
    CC=14  in:0  out:24  total:24
  sumd.extractor.generate_project_logic
    CC=2  in:2  out:22  total:24
  sumd.parser.SUMDParser.parse_file
    CC=1  in:20  out:2  total:22
  sumd.extractor.extract_pyproject
    CC=3  in:5  out:17  total:22
  sumd.sections.quality._render_quality_parsed
    CC=9  in:1  out:21  total:22
  sumd.cli.lint
    CC=6  in:0  out:21  total:21
  sumd.sections.dependencies._render_deps_runtime
    CC=6  in:1  out:19  total:20
  sumd.cli.analyze
    CC=7  in:0  out:20  total:20
  sumd.sections.interfaces._render_interfaces_openapi
    CC=6  in:1  out:19  total:20
  sumd.extractor._parse_doql_content
    CC=6  in:1  out:19  total:20
  sumd.cli.map_cmd
    CC=7  in:0  out:20  total:20
  sumd.extractor.extract_package_json
    CC=3  in:4  out:15  total:19
  sumd.extractor._parse_doql_workflows
    CC=7  in:1  out:18  total:19

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
    validate_codeblocks  CC=9  out:17
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
  sumd.cli.validate → sumd.parser.SUMDParser.parse_file
  sumd.cli.export → sumd.parser.SUMDParser.parse_file
  sumd.cli.info → sumd.parser.SUMDParser.parse_file
  sumd.cli.extract → sumd.parser.SUMDParser.parse_file
  sumd.cli.lint → sumd.cli._lint_collect_paths
  sumd.cli.lint → sumd.validator.validate_sumd_file
  sumd.cli._lint_print_result → sumd.cli._lint_classify_issues
  sumd.cli._run_analyze_tool → sumd.cli._run_code2llm_formats
  sumd.cli._run_analyze_tool → sumd.cli._run_tool_subprocess
  sumd.cli.analyze → sumd.cli._setup_tools_venv
  sumd.cli._scaffold_smoke_scenario → sumd.cli._scaffold_write
  sumd.cli._scaffold_smoke_scenario → sumd.cli._api_scenario_template
  sumd.cli._scaffold_crud_scenarios → sumd.cli._scaffold_write
  sumd.cli._scaffold_crud_scenarios → sumd.cli._api_scenario_template
  sumd.cli._scaffold_from_openapi → sumd.cli._scaffold_smoke_scenario
  sumd.cli._scaffold_from_openapi → sumd.cli._scaffold_crud_scenarios
  sumd.cli._scaffold_generic → sumd.cli._api_scenario_template
  sumd.cli._scaffold_generic → sumd.cli._scaffold_write
  sumd.cli.map_cmd → sumd.extractor.generate_map_toon
  sumd.cli.main → sumd.cli.cli
  sumd.cli.main_sumr → sumd.cli.cli
  sumd.extractor.extract_pyproject → sumd.extractor._read_toml
  sumd.extractor.extract_taskfile → sumd.extractor._first_task_cmd
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

## Intent

SUMD - Structured Unified Markdown Descriptor for AI-aware project documentation
