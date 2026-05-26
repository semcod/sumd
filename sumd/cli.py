"""SUMD CLI - Command-line interface for SUMD operations."""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click

from sumd.parser import SUMDParser, parse_file
from sumd.parser import validate_sumd_file
from sumd.generator import generate_map_toon
from sumd.pipeline import RenderPipeline
from sumd.extractor import extract_package_json, extract_pyproject
from sumd import __version__

from sumd.cli_doql import (
    _DOQL_SPECS,
    _DOQL_AUTOGEN_MARKER,
    _detect_project_type,
    _render_doql_boilerplate,
    _node_framework,
    _node_spec_from_package_json,
    _build_doql_spec,
    _generate_doql_less,
)

from sumd.cli_scan import (
    _is_project_dir,
    _detect_projects,
    _ensure_venv,
    _tool_bin,
    _run_one_tool,
    _run_analysis_tools,
    _export_sumd_json,
    _render_write_validate,
    _echo_scan_result,
    _maybe_generate_doql,
    _maybe_generate_testql,
    _finalize_scan,
    _scan_one_project,
)



@click.group()
@click.version_option(version=__version__)
def cli():
    """SUMD - Structured Unified Markdown Descriptor CLI."""
    pass


@cli.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
def validate(file: Path):
    """Validate a SUMD document.

    FILE: Path to the SUMD markdown file
    """
    try:
        document = parse_file(file)
        parser = SUMDParser()
        errors = parser.validate(document)

        if errors:
            click.echo("❌ Validation failed:", err=True)
            for error in errors:
                click.echo(f"  - {error}", err=True)
            sys.exit(1)
        else:
            click.echo("✅ SUMD document is valid")
            sys.exit(0)
    except Exception as e:
        click.echo(f"❌ Error parsing file: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    type=click.Choice(["markdown", "json", "yaml", "toml"]),
    default="json",
    help="Output format",
)
@click.option("--output", type=click.Path(path_type=Path), help="Output file path")
def export(file: Path, format: str, output: Optional[Path]):
    """Export a SUMD document to structured format.

    FILE: Path to the SUMD markdown file
    """
    try:
        document = parse_file(file)

        data = {
            "project_name": document.project_name,
            "description": document.description,
            "sections": [
                {
                    "name": section.name,
                    "type": section.type.value,
                    "content": section.content,
                    "level": section.level,
                }
                for section in document.sections
            ],
        }

        result = ""
        if format == "markdown":
            result = document.raw_content
        elif format == "json":
            import json

            result = json.dumps(data, indent=2)
        elif format == "yaml":
            import yaml

            result = yaml.dump(data, default_flow_style=False)
        elif format == "toml":
            import toml

            result = toml.dumps(data)

        if output:
            output.write_text(result, encoding="utf-8")
            click.echo(f"✅ Exported to {output}")
        else:
            click.echo(result)
    except Exception as e:
        click.echo(f"❌ Error exporting file: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
def info(file: Path):
    """Display information about a SUMD document.

    FILE: Path to the SUMD markdown file
    """
    try:
        document = parse_file(file)

        click.echo(f"📦 Project: {document.project_name}")
        click.echo(f"📝 Description: {document.description}")
        click.echo(f"📑 Sections: {len(document.sections)}")

        for section in document.sections:
            click.echo(f"  - {section.name} ({section.type.value})")
    except Exception as e:
        click.echo(f"❌ Error reading file: {e}", err=True)
        sys.exit(1)


def _parse_structured_data(content: str, format_type: str) -> dict:
    """Parse structured data string based on format type."""
    if format_type == "json":
        import json
        return json.loads(content)
    if format_type == "yaml":
        import yaml
        return yaml.safe_load(content)
    if format_type == "toml":
        import toml
        return toml.loads(content)
    return {}


@cli.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    type=click.Choice(["json", "yaml", "toml"]),
    default="json",
    help="Input format",
)
@click.option("--output", type=click.Path(path_type=Path), help="Output SUMD file path")
def generate(file: Path, format: str, output: Optional[Path]):
    """Generate a SUMD document from structured format.

    FILE: Path to the structured format file (json/yaml/toml)
    """
    try:
        content = file.read_text(encoding="utf-8")
        data = _parse_structured_data(content, format)

        # Generate SUMD markdown
        lines = []
        lines.append(f"# {data.get('project_name', 'Untitled')}")
        if data.get("description"):
            lines.append(f"{data['description']}")
        lines.append("")

        for section in data.get("sections", []):
            level_prefix = "#" * section.get("level", 2)
            lines.append(f"{level_prefix} {section['name'].title()}")
            lines.append("")
            lines.append(section.get("content", ""))
            lines.append("")

        result = "\n".join(lines)

        if output:
            output.write_text(result, encoding="utf-8")
            click.echo(f"✅ Generated SUMD at {output}")
        else:
            click.echo(result)
    except Exception as e:
        click.echo(f"❌ Error generating SUMD: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
@click.option("--section", type=str, help="Extract specific section")
def extract(file: Path, section: str):
    """Extract content from a SUMD document.

    FILE: Path to the SUMD markdown file
    """
    try:
        document = parse_file(file)

        if section:
            for sec in document.sections:
                if sec.name.lower() == section.lower():
                    click.echo(sec.content)
                    return
            click.echo(f"❌ Section '{section}' not found", err=True)
            sys.exit(1)
        else:
            click.echo(document.raw_content)
    except Exception as e:
        click.echo(f"❌ Error extracting content: {e}", err=True)
        sys.exit(1)


# Files whose presence marks a directory as a "project" root.
# Covers a broad range of languages and project/tooling ecosystems so that
# `sumd <dir>` works on Python, Node/JS/TS, Rust, Go, Java/Kotlin, Ruby, PHP,
# .NET, Swift, Dart/Flutter, Elixir, Haskell, Clojure, C/C++ and generic
# tool-driven repos (Taskfile, Makefile, Dockerfile, docker-compose, …).
# Glob patterns for project markers (extensions that vary per project).
def _collect_project_dirs(workspace: Path, workspace_mode: bool, effective_depth: Optional[int]) -> list[Path]:
    """Determine the list of project directories to scan."""
    if workspace_mode:
        return [workspace] if _is_project_dir(workspace) else []
    project_dirs = _detect_projects(workspace, max_depth=effective_depth)
    if _is_project_dir(workspace):
        project_dirs.insert(0, workspace)
    return project_dirs


def _scan_projects_loop(
    project_dirs: list[Path],
    fix: bool,
    raw: bool,
    export_json: bool,
    analyze: bool,
    tool_list: list[str],
    parser_inst,
    profile: str,
    generate_doql: bool,
    doql_sync: bool,
    generate_testql: bool,
) -> tuple[int, int, int, dict]:
    """Execute scan over multiple projects and accumulate results."""
    results = {}
    ok_count = skip_count = fail_count = 0
    for proj_dir in project_dirs:
        result = _scan_one_project(
            proj_dir, fix, raw, export_json, analyze, tool_list, parser_inst, profile, generate_doql, doql_sync, generate_testql
        )
        results[proj_dir.name] = result
        if result["status"] == "SKIP":
            skip_count += 1
        elif result["status"] == "OK":
            ok_count += 1
        else:
            fail_count += 1
    return ok_count, skip_count, fail_count, results


@cli.command("scan")
@click.argument("workspace", type=click.Path(exists=True, path_type=Path), default=".")
@click.option(
    "--export-json/--no-export-json",
    default=False,
    help="Also export sumd.json per project",
)
@click.option(
    "--report",
    type=click.Path(path_type=Path),
    default=None,
    help="Save JSON summary report to file",
)
@click.option(
    "--fix/--no-fix",
    default=True,
    help="Overwrite existing SUMD.md (default). Use --no-fix to skip if already present.",
)
@click.option(
    "--raw/--no-raw",
    default=True,
    help="Embed source files as raw code blocks (default). Use --no-raw for structured Markdown.",
)
@click.option(
    "--analyze/--no-analyze",
    default=False,
    help="Run analysis tools (code2llm, redup, vallm) on each project after scan",
)
@click.option(
    "--tools",
    type=str,
    default="code2llm,redup,vallm",
    help="Tools to run with --analyze",
)
@click.option(
    "--profile",
    type=click.Choice(["minimal", "light", "rich", "refactor"]),
    default="rich",
    help="Section profile to use when rendering SUMD.md. Use 'refactor' for pre-refactoring analysis report.",
)
@click.option(
    "--depth",
    type=int,
    default=None,
    help="Max directory depth to scan for projects (default: 0 unless --recursive)",
)
@click.option(
    "--recursive/--no-recursive",
    default=False,
    help="Recursively scan subdirectories for projects (default: scan immediate children only)",
)
@click.option(
    "--generate-doql/--no-generate-doql",
    default=True,
    help="Generate app.doql.less file for each project if it doesn't exist (default: enabled)",
)
@click.option(
    "--doql-sync/--no-doql-sync",
    default=False,
    help="Run 'doql sync' after generating SUMD.md (only in projects with app.doql.less/css)",
)
@click.option(
    "--generate-testql/--no-generate-testql",
    default=True,
    help="Generate testql scenarios via 'testql generate' if none exist (default: enabled)",
)
@click.option(
    "--workspace-mode/--no-workspace-mode",
    default=True,
    help="Treat the workspace root as a single project; skip scanning subdirectories for separate projects (default: enabled)",
)
def scan(
    workspace: Path,
    export_json: bool,
    report: Optional[Path],
    fix: bool,
    raw: bool,
    analyze: bool,
    tools: str,
    profile: str,
    depth: Optional[int],
    recursive: bool,
    generate_doql: bool,
    doql_sync: bool,
    generate_testql: bool,
    workspace_mode: bool,
):
    """Scan a workspace directory and generate SUMD.md for every project found.

    Detects projects by the presence of a known marker file (pyproject.toml,
    package.json, Cargo.toml, go.mod, pom.xml, build.gradle, Gemfile,
    composer.json, Package.swift, pubspec.yaml, mix.exs, CMakeLists.txt,
    Makefile, Dockerfile, Taskfile.yml, SUMD.md, …) — see _PROJECT_MARKER_FILES
    for the full list. Language-agnostic: works on Python, JS/TS, Rust, Go,
    Java/Kotlin, Ruby, PHP, .NET, Swift, Dart, Elixir, Haskell, Clojure, C/C++
    and generic tool-driven repos.

    Extracts metadata from: pyproject.toml, package.json, Taskfile.yml,
    Makefile, testql-scenarios/, openapi.yaml, app.doql.less, pyqual.yaml,
    Dockerfile, docker-compose.yml, requirements*.txt, .env.example, goal.yaml
    and any Python source modules in the package directory.

    WORKSPACE: Root directory containing project subdirectories (default: current dir)
    """
    workspace = workspace.resolve()
    parser_inst = SUMDParser()
    tool_list = [t.strip() for t in tools.split(",") if t.strip()]

    # Default non-recursive: only immediate children (max_depth=0).
    # --recursive or --depth overrides this default.
    effective_depth = depth if depth is not None else (None if recursive else 0)

    project_dirs = _collect_project_dirs(workspace, workspace_mode, effective_depth)

    if not project_dirs:
        click.echo(
            f"⚠️  No projects found in {workspace} "
            "(looked for pyproject.toml, package.json, Cargo.toml, go.mod, "
            "pom.xml, Gemfile, composer.json, Dockerfile, Taskfile.yml, "
            "Makefile, SUMD.md, …)"
        )
        sys.exit(1)

    click.echo(f"\n🔍 Scanning {len(project_dirs)} projects in {workspace}\n")
    click.echo(f"{'Project':<20} {'Status':<10} {'Sections':<10} {'Sources'}")
    click.echo("─" * 70)

    ok_count, skip_count, fail_count, results = _scan_projects_loop(
        project_dirs, fix, raw, export_json, analyze, tool_list, parser_inst, profile, generate_doql, doql_sync, generate_testql
    )

    click.echo("─" * 70)
    click.echo(
        f"\n📊 Summary: {len(project_dirs)} projects | ✅ {ok_count} ok | ⏭ {skip_count} skipped | ❌ {fail_count} failed\n"
    )

    if report:
        report.write_text(
            json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        click.echo(f"📄 Report saved to {report}")

    sys.exit(0 if fail_count == 0 else 1)


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--workspace",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Validate all SUMD.md files in workspace subdirectories",
)
@click.option(
    "--json", "as_json", is_flag=True, default=False, help="Output results as JSON"
)
@click.option(
    "--strict", is_flag=True, default=False, help="Treat logic inconsistencies as fatal errors"
)
def lint(files: tuple[Path, ...], workspace: Optional[Path], as_json: bool, strict: bool):
    """Validate SUMD.md files — check markdown structure and codeblock formats.

    Validates:
      - Markdown structure (H1, required H2 sections, metadata fields)
      - Codeblock formats (YAML parseable, Less/CSS braces balanced, Mermaid diagram type)
      - markpact annotations (valid kind, required path= attr for markpact:file)
      - Empty or broken blocks

    Examples:
      sumd lint SUMD.md
      sumd lint --workspace .
    """
    paths = _lint_collect_paths(files, workspace)

    if not paths:
        click.echo(
            "⚠️  No SUMD.md files specified. Use sumd lint SUMD.md or --workspace .",
            err=True,
        )
        sys.exit(1)

    all_results = []
    total_errors = 0
    total_warnings = 0

    for path in paths:
        r = validate_sumd_file(path)
        all_results.append(r)

        errors, warnings = _lint_classify_issues(r, strict)
        total_errors += len(errors)
        total_warnings += len(warnings)

        if as_json:
            continue

        _lint_print_result(path, r, strict)

    if as_json:
        import json as _json

        click.echo(_json.dumps(all_results, indent=2, default=str))
    else:
        click.echo(
            f"\n📊 {len(paths)} files | ❌ {total_errors} errors | ⚠ {total_warnings} warnings"
        )

    sys.exit(0 if total_errors == 0 else 1)


def _lint_classify_issues(r: dict, strict: bool) -> tuple[list[str], list[str]]:
    """Classify issues into (errors, warnings) based on strict mode."""
    errors: list[str] = r["markdown"] + [
        c.message for c in r["codeblocks"] if c.kind == "error"
    ]
    warnings: list[str] = [c.message for c in r["codeblocks"] if c.kind == "warning"]
    logic = r.get("logic", [])
    if strict:
        errors += logic
    else:
        warnings += logic
    return errors, warnings


def _lint_collect_paths(
    files: tuple[Path, ...], workspace: Optional[Path]
) -> list[Path]:
    """Collect SUMD.md paths from explicit files and/or workspace."""
    paths: list[Path] = list(files)
    if workspace:
        ws = workspace.resolve()
        paths += sorted(
            d / "SUMD.md"
            for d in ws.iterdir()
            if d.is_dir() and not d.name.startswith(".") and (d / "SUMD.md").exists()
        )
    return paths


def _lint_print_result(path: Path, r: dict, strict: bool) -> None:
    """Print lint result for a single file."""
    errors, warnings = _lint_classify_issues(r, strict)
    status = "✅" if r["ok"] else "❌"
    cb_count = len(r["codeblocks"])
    click.echo(
        f"{status} {path}  ({cb_count} blocks, {len(errors)} errors, {len(warnings)} warnings)"
    )
    for issue in r["markdown"]:
        click.echo(f"    [markdown] ❌ {issue}")
    for issue in r.get("logic", []):
        click.echo(f"    [logic] ❌ {issue}")
    for cb in r["codeblocks"]:
        icon = "❌" if cb.kind == "error" else "⚠"
        click.echo(f"    [codeblock L{cb.line} {cb.lang}] {icon} {cb.message}")


def _setup_tools_venv(venv_dir: Path, tool_list: list[str], force: bool) -> Path:
    """Create .sumd-tools venv and install tools if needed. Returns bin_dir."""
    tools_dir = venv_dir.parent
    if not venv_dir.exists() or force:
        click.echo("📁 Setting up tools environment...")
        tools_dir.mkdir(exist_ok=True)
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            click.echo(f"❌ Failed to create venv: {result.stderr}", err=True)
            sys.exit(1)
        pip_path = venv_dir / "bin" / "pip"
        if not pip_path.exists():
            pip_path = venv_dir / "Scripts" / "pip.exe"
        for pkg in tool_list:
            click.echo(f"   📥 Installing {pkg}...")
            subprocess.run([str(pip_path), "install", "-q", pkg], capture_output=True)
    else:
        click.echo(f"📁 Using existing venv: {venv_dir}")
    bin_dir = venv_dir / "bin"
    return bin_dir if bin_dir.exists() else venv_dir / "Scripts"


def _run_code2llm_formats(bin_dir: Path, project: Path, project_output: Path) -> bool:
    """Run code2llm for each format. Returns True if all succeeded."""
    code2llm = bin_dir / "code2llm"
    if not code2llm.exists():
        code2llm = bin_dir / "code2llm.exe"
    formats = [
        ("toon", "analysis.toon.yaml"),
        ("evolution", "evolution.toon.yaml"),
        ("context", "context.md"),
        ("calls_toon", "calls.toon.yaml"),
        ("mermaid", "flow.mmd, compact_flow.mmd"),
    ]
    all_ok = True
    for fmt, output_files in formats:
        extra = ["--no-png"] if fmt in ("mermaid", "calls") else []
        r = subprocess.run(
            [str(code2llm), "./", "-f", fmt, "-o", str(project_output)] + extra,
            capture_output=True,
            text=True,
            cwd=str(project),
        )
        if r.returncode != 0:
            click.echo(f"   ⚠️  code2llm -f {fmt} failed", err=True)
            all_ok = False
        else:
            click.echo(f"   ✅ code2llm -f {fmt} → {output_files}")
    return all_ok


def _run_tool_subprocess(bin_dir: Path, tool: str, cmd_args: list[str]) -> bool:
    """Run a single analysis tool subprocess. Returns True on success."""
    exe = bin_dir / tool
    if not exe.exists():
        exe = bin_dir / f"{tool}.exe"
    r = subprocess.run([str(exe)] + cmd_args, capture_output=True, text=True)
    if r.returncode == 0:
        click.echo(f"   ✅ {tool} complete")
        return True
    click.echo(f"   ⚠️  {tool} failed", err=True)
    return False


_TOOL_LABELS: dict[str, str] = {
    "code2llm": "🔬 Running code2llm...",
    "redup": "🔍 Running redup...",
    "vallm": "✅ Running vallm...",
}


def _run_analyze_tool(
    tool: str, bin_dir: Path, project: Path, project_output: Path
) -> bool:
    """Run a single analysis tool. Returns True on success."""
    if tool == "code2llm":
        return _run_code2llm_formats(bin_dir, project, project_output)
    if tool == "redup":
        return _run_tool_subprocess(
            bin_dir,
            "redup",
            ["scan", str(project), "--format", "toon", "--output", str(project_output)],
        )
    if tool == "vallm":
        return _run_tool_subprocess(
            bin_dir,
            "vallm",
            [
                "batch",
                str(project),
                "--recursive",
                "--format",
                "toon",
                "--output",
                str(project_output),
            ],
        )
    return False


def analyze(project: Path, tools: str, force: bool):
    """Run analysis tools (code2llm, redup, vallm) on a project.

    Installs tools to .sumd-tools/venv and generates analysis files in project/.

    PROJECT: Path to the project directory to analyze
    """
    import subprocess as _sp  # noqa: F401 (already imported at top)

    project = project.resolve()
    venv_dir = project / ".sumd-tools" / "venv"
    project_output = project / "project"

    tool_list = [t.strip() for t in tools.split(",") if t.strip()]
    valid_tools = {"code2llm", "redup", "vallm"}
    invalid = set(tool_list) - valid_tools
    if invalid:
        click.echo(f"❌ Unknown tools: {', '.join(invalid)}", err=True)
        sys.exit(1)

    click.echo(f"🔍 Analyzing project: {project.name}")
    click.echo(f"📦 Tools: {', '.join(tool_list)}")

    bin_dir = _setup_tools_venv(venv_dir, tool_list, force)
    project_output.mkdir(exist_ok=True)
    success_count = 0

    for tool in tool_list:
        click.echo(_TOOL_LABELS[tool])
        if _run_analyze_tool(tool, bin_dir, project, project_output):
            success_count += 1

    click.echo(
        f"\n📊 Analysis complete: {success_count}/{len(tool_list)} tools succeeded"
    )
    click.echo(f"📁 Output: {project_output}/")
    sys.exit(0 if success_count == len(tool_list) else 1)


def _api_scenario_template(
    name: str, scenario_type: str, endpoints_block: str, base_path: str = "/api/v1"
) -> str:
    n_ep = endpoints_block.strip().count("\n  ") + 1
    return (
        f"# SCENARIO: {name}.testql.toon.yaml — {name.replace('-', ' ')}\n"
        f"# TYPE: {scenario_type}\n"
        f"# VERSION: 1.0\n"
        f"# GENERATED: true\n"
        f"\n"
        f"# ── Konfiguracja ──────────────────────────────────────\n"
        f"CONFIG[1]{{key, value}}:\n"
        f"  base_path,  {base_path}\n"
        f"\n"
        f"# ── Wywołania API ─────────────────────────────────────\n"
        f"API[{n_ep}]{{method, endpoint, status}}:\n"
        f"{endpoints_block}\n"
        f"# ── Asercje ───────────────────────────────────────────\n"
        f"# ASSERT[0]{{field, op, expected}}:\n"
        f"#   NOTE: fill in assertions\n"
    )


def _scaffold_write(
    path: Path, content: str, force: bool, generated: list[str], skipped: list[str]
) -> None:
    if path.exists() and not force:
        skipped.append(path.name)
    else:
        path.write_text(content, encoding="utf-8")
        generated.append(path.name)


def _scaffold_smoke_scenario(
    paths: dict,
    base: str,
    out_dir: Path,
    force: bool,
    generated: list[str],
    skipped: list[str],
) -> None:
    health_paths = [
        p for p in paths if any(k in p.lower() for k in ("health", "ping", "status"))
    ]
    ep_block = (
        "\n".join(f"  GET,  {p},  200" for p in health_paths[:5])
        if health_paths
        else "  GET,  /health,  200  # NOTE: adjust path"
    )
    _scaffold_write(
        out_dir / "smoke-health.testql.toon.yaml",
        _api_scenario_template("smoke-health", "smoke", ep_block, base),
        force,
        generated,
        skipped,
    )


def _scaffold_crud_scenarios(
    groups: dict,
    base: str,
    out_dir: Path,
    force: bool,
    generated: list[str],
    skipped: list[str],
) -> None:
    for resource, eps in sorted(groups.items()):
        if resource in ("health", "ping", "status"):
            continue
        safe_resource = re.sub(r"[^\w\-]", "_", resource).strip("_")
        ep_lines = [f"  {method},  {path},  200" for method, path in eps[:8]]
        if not ep_lines:
            continue
        _scaffold_write(
            out_dir / f"api-{safe_resource}.testql.toon.yaml",
            _api_scenario_template(
                f"api-{safe_resource}", "api", "\n".join(ep_lines), base
            ),
            force,
            generated,
            skipped,
        )


def _scaffold_from_openapi(
    spec: dict,
    out_dir: Path,
    scenario_type: str,
    force: bool,
    generated: list[str],
    skipped: list[str],
) -> int:
    """Generate scenarios from OpenAPI spec into out_dir. Returns number of path entries."""
    paths = spec.get("paths", {})
    groups: dict[str, list[tuple[str, str]]] = {}
    for path, methods in paths.items():
        segment = path.strip("/").split("/")[0] or "root"
        for method in methods:
            if method.lower() in ("get", "post", "put", "delete", "patch"):
                groups.setdefault(segment, []).append((method.upper(), path))

    base = spec.get("servers", [{}])[0].get("url", "/api/v1").rstrip("/")

    if scenario_type in ("smoke", "all"):
        _scaffold_smoke_scenario(paths, base, out_dir, force, generated, skipped)

    if scenario_type in ("crud", "api", "all"):
        _scaffold_crud_scenarios(groups, base, out_dir, force, generated, skipped)

    return len(paths)


def _scaffold_generic(
    out_dir: Path, force: bool, generated: list[str], skipped: list[str]
) -> None:
    click.echo("⚠️  No openapi.yaml found — generating generic smoke scaffold")
    content = _api_scenario_template(
        "smoke-generic",
        "smoke",
        "  GET,  /health,  200  # NOTE: adjust\n  GET,  /,  200       # NOTE: adjust",
        "/api/v1  # NOTE: adjust base_path",
    )
    _scaffold_write(
        out_dir / "smoke-generic.testql.toon.yaml", content, force, generated, skipped
    )


def _scaffold_openapi_flow(
    openapi_path: Path, out_dir: Path, scenario_type: str, force: bool, generated: list[str], skipped: list[str]
) -> None:
    """Parse openapi.yaml and generate scaffolded scenarios."""
    import yaml as _yaml
    click.echo(f"📖 Reading {openapi_path.name}...")
    try:
        spec = _yaml.safe_load(openapi_path.read_text(encoding="utf-8"))
    except Exception as e:
        click.echo(f"❌ Failed to parse openapi.yaml: {e}", err=True)
        sys.exit(1)
    n_paths = _scaffold_from_openapi(
        spec, out_dir, scenario_type, force, generated, skipped
    )
    groups_count = len(
        {
            (path.strip("/").split("/")[0] or "root")
            for path in spec.get("paths", {})
        }
    )
    click.echo(f"   📋 {n_paths} paths → {groups_count} resource groups")


def _print_scaffold_summary(generated: list[str], skipped: list[str], out_dir: Path) -> None:
    """Print the final summary of scaffolded files."""
    click.echo(
        f"\n📊 scaffold: {len(generated)} generated | {len(skipped)} skipped (use --force to overwrite)"
    )
    for f in generated:
        click.echo(f"   ✅ {out_dir / f}")
    for f in skipped:
        click.echo(f"   ⏭  {out_dir / f} (already exists)")
    if generated:
        click.echo("\n💡 Next steps:")
        click.echo("   1. Fill in ASSERTs in generated files")
        click.echo("   2. Run: sumd scan . --fix   (to embed scenarios in SUMD.md)")
        click.echo(f"   3. Run: testql run {out_dir}/")


@cli.command()
@click.argument("project", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output directory for generated files (default: <project>/testql-scenarios/)",
)
@click.option(
    "--force/--no-force", default=False, help="Overwrite existing scenario files"
)
@click.option(
    "--type",
    "scenario_type",
    type=click.Choice(["api", "smoke", "crud", "all"]),
    default="all",
    help="Type of scenarios to generate",
)
def scaffold(project: Path, output: Optional[Path], force: bool, scenario_type: str):
    """Generate testql scenario scaffolds from OpenAPI spec or SUMD.md.

    Reads openapi.yaml (if present) and generates .testql.toon.yaml scenario files
    for each endpoint group. Without OpenAPI, generates a generic smoke test scaffold.

    Why scaffold exists: sumd scan only READS existing testql files — it cannot
    generate them because testql scenarios encode expected business behaviour that
    only a human (or LLM with domain context) can define. scaffold generates the
    structural skeleton; the assertions must be filled in manually or via LLM.

    PROJECT: Path to the project directory
    """
    project = project.resolve()
    out_dir = (output or (project / "testql-scenarios")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    generated: list[str] = []
    skipped: list[str] = []

    openapi_path = project / "openapi.yaml"
    if openapi_path.exists():
        _scaffold_openapi_flow(openapi_path, out_dir, scenario_type, force, generated, skipped)
    else:
        _scaffold_generic(out_dir, force, generated, skipped)
    _print_scaffold_summary(generated, skipped, out_dir)


@cli.command(name="map")
@click.argument("project", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output file path (default: <project>/project/map.toon.yaml)",
)
@click.option(
    "--force/--no-force", default=False, help="Overwrite existing map.toon.yaml"
)
@click.option(
    "--stdout",
    is_flag=True,
    default=False,
    help="Print to stdout instead of writing file",
)
def map_cmd(project: Path, output: Optional[Path], force: bool, stdout: bool):
    """Generate project/map.toon.yaml — static code map in toon format.

    Analyses all source files in the project and produces a map.toon.yaml
    with module inventory, function signatures, CC estimates, and fan-out
    metrics. The file is automatically included in SUMD.md by 'sumd scan'.

    Equivalent to the 'code2llm map' output but generated without external tools.
    """
    project = project.resolve()
    out_path = output or (project / "project" / "map.toon.yaml")

    if not stdout and out_path.exists() and not force:
        click.echo(f"⏭  {out_path} already exists (use --force to overwrite)")
        sys.exit(0)

    click.echo(f"🗺  Generating map for {project.name}...")
    content = generate_map_toon(project)

    if stdout:
        click.echo(content, nl=False)
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")

    # Quick summary from the header line
    header = content.splitlines()[0] if content else ""
    click.echo(f"✅ Written {out_path}")
    click.echo(f"   {header}")
    click.echo("\n💡 Next: sumd scan . --fix  (to embed map in SUMD.md)")


async def _execute_dsl_command(shell, command: str) -> None:
    """Execute a single DSL command and print the result."""
    result = await shell.execute_command(command)
    if result is not None:
        if isinstance(result, (list, dict)):
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(result)


def _should_run_interactive(interactive: bool, command: Optional[str], script: Optional[Path]) -> bool:
    """Determine if the interactive shell should be started."""
    if interactive:
        return True
    if command:
        return False
    if script:
        return False
    return True


async def _run_dsl_async(
    directory: Path,
    command: Optional[str],
    script: Optional[Path],
    interactive: bool,
) -> None:
    """Async implementation of the 'dsl' command."""
    from sumd.dsl.shell import DSLShell

    shell = DSLShell(working_directory=directory)
    try:
        if command:
            await _execute_dsl_command(shell, command)
        elif script:
            await shell.execute_script(script)
        
        if _should_run_interactive(interactive, command, script):
            await shell.run()
    except KeyboardInterrupt:
        click.echo("\nInterrupted.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help="Working directory for DSL shell",
)
@click.option(
    "--command",
    "-c",
    help="Execute single DSL command",
)
@click.option(
    "--script",
    "-s",
    type=click.Path(exists=True, path_type=Path),
    help="Execute DSL script file",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Run interactively after script/command",
)
def dsl(directory: Path, command: Optional[str], script: Optional[Path], interactive: bool):
    """SUMD DSL Shell - Domain Specific Language for SUMD operations.

    Provides an interactive shell and scripting interface for SUMD operations
    with CQRS ES architecture support.

    Examples:
        sumd dsl                           # Start interactive shell
        sumd dsl -c "scan('.')"            # Execute single command
        sumd dsl -s script.dsl             # Execute script file
        sumd dsl -d /path/to/project       # Set working directory
    """
    import asyncio
    asyncio.run(_run_dsl_async(directory, command, script, interactive))


@cli.command("cqrs")
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help="Working directory for CQRS ES operations",
)
@click.argument("command_type")
@click.argument("aggregate_id")
@click.option(
    "--data",
    help="Command data as JSON string",
)
def cqrs_command(directory: Path, command_type: str, aggregate_id: str, data: Optional[str]):
    """Execute CQRS command on SUMD aggregate.
    
    COMMAND_TYPE: Type of command to execute
    AGGREGATE_ID: ID of the aggregate (usually file path)
    
    Examples:
        sumd cqrs-cmd create_sumd_document ./SUMD.md --data '{"project_name":"MyProject"}'
        sumd cqrs-cmd add_section ./SUMD.md --data '{"section_name":"Architecture","content":"..."}'
    """
    import asyncio
    from sumd.cqrs.events import EventStore
    from sumd.cqrs.commands import CommandBus, SumdCommandHandler
    from pathlib import Path
    
    async def run_command():
        try:
            # Initialize CQRS ES components
            event_store = EventStore(Path.home() / ".sumd" / "events")
            command_bus = CommandBus(event_store)
            command_handler = SumdCommandHandler(event_store)
            
            # Register handler
            command_bus.register_handler(command_type, command_handler)
            
            # Parse data
            command_data = {}
            if data:
                try:
                    command_data = json.loads(data)
                except json.JSONDecodeError:
                    click.echo(f"Invalid JSON data: {data}", err=True)
                    sys.exit(1)
            
            # Create and execute command
            from sumd.cqrs.commands import (
                CreateSumdDocument,
                UpdateSumdDocument,
                AddSumdSection,
                RemoveSumdSection,
                ValidateSumdDocument,
                ScanProject,
                GenerateMap,
                ExecuteDslCommand,
            )
            
            command_classes = {
                "create_sumd_document": CreateSumdDocument,
                "update_sumd_document": UpdateSumdDocument,
                "add_sumd_section": AddSumdSection,
                "remove_sumd_section": RemoveSumdSection,
                "validate_sumd_document": ValidateSumdDocument,
                "scan_project": ScanProject,
                "generate_map": GenerateMap,
                "execute_dsl_command": ExecuteDslCommand,
            }
            
            command_class = command_classes.get(command_type)
            if not command_class:
                click.echo(f"Unknown command type: {command_type}", err=True)
                sys.exit(1)
            
            command = command_class(aggregate_id=aggregate_id, data=command_data)
            events = await command_bus.dispatch(command)
            
            click.echo(f"✅ Command executed: {command_type}")
            click.echo(f"   Aggregate ID: {aggregate_id}")
            click.echo(f"   Events generated: {len(events)}")
            
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    
    asyncio.run(run_command())


async def _execute_nlp_result(engine, result: dict, context, verbose: bool) -> None:
    """Execute the DSL command resulting from NLP analysis."""
    if verbose:
        click.echo("⚡ Executing generated DSL command...")
    exec_result = await engine.execute_text(result['dsl_command'], context)
    if exec_result.success:
        click.echo("✅ Command executed successfully!")
        if exec_result.result:
            click.echo(f"   Result: {exec_result.result}")
    else:
        click.echo(f"❌ Command execution failed: {exec_result.error}", err=True)
        sys.exit(1)


async def _run_nlp_async(
    text: str, directory: Path, execute: bool, verbose: bool
) -> None:
    """Async implementation of the 'nlp' command."""
    from .dsl.engine import DSLEngine, DSLContext
    from .dsl.schema import DEFAULT_PROJECT_SCHEMA

    try:
        engine = DSLEngine(project_schema=DEFAULT_PROJECT_SCHEMA)
        context = DSLContext(directory)

        if verbose:
            click.echo(f'🤖 Processing: "{text}"')
            click.echo(f"📁 Directory: {directory}")
            click.echo()

        nlp_result = await engine.process_natural_language(text)

        if not nlp_result.success:
            click.echo(f"❌ NLP processing failed: {nlp_result.error}", err=True)
            sys.exit(1)

        result = nlp_result.result
        click.echo("🧠 NLP Analysis:")
        click.echo(f"   Original: \"{result['original_text']}\"")
        click.echo(f"   Intent: {result['intent']}")
        click.echo(f"   Entities: {result['entities']}")
        click.echo(f"   Generated DSL: {result['dsl_command']}")
        click.echo()

        if execute:
            await _execute_nlp_result(engine, result, context, verbose)
        else:
            click.echo('💡 To execute this command, use:')
            click.echo(f'   sumd nlp "{text}" --execute')
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command("nlp")
@click.argument("text", type=str)
@click.option(
    "-d", "--directory",
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help="Working directory for NLP processing"
)
@click.option(
    "-e", "--execute",
    is_flag=True,
    help="Execute the generated DSL command"
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Show verbose output"
)
def nlp_command(text: str, directory: Path, execute: bool, verbose: bool):
    """Process natural language text and convert to DSL commands."""
    import asyncio
    asyncio.run(_run_nlp_async(text, directory, execute, verbose))


def main():
    """Main entry point — if first arg is a path, run 'scan <path> --fix'."""
    import sys as _sys

    args = _sys.argv[1:]
    # If first arg looks like a path (not a known command), treat as `scan <path> --fix`
    known_commands = {
        "scan",
        "lint",
        "analyze",
        "map",
        "scaffold",
        "generate",
        "validate",
        "export",
        "extract",
        "info",
        "reload",
        "dsl",
        "cqrs",
        "nlp",
        "--help",
        "--version",
    }
    # reload <path>  →  scan <path> --fix --doql-sync
    if args and args[0] == "reload":
        path = args[1] if len(args) > 1 and not args[1].startswith("-") else "."
        extra = [a for a in args[1:] if a != path]
        _sys.argv = [_sys.argv[0], "scan", path, "--fix", "--doql-sync"] + extra
    elif args and args[0] not in known_commands and not args[0].startswith("-"):
        _sys.argv = [_sys.argv[0], "scan", args[0], "--fix"] + args[1:]
    cli()


def main_sumr():
    """Entry point for `sumr` command — generates SUMR.md (refactor profile).

    Usage:
        sumr .                  # generate SUMR.md in current project
        sumr /path/to/project   # generate SUMR.md in specified project
    """
    import sys as _sys

    args = _sys.argv[1:]
    # Default to current dir if no path given
    path = "."
    extra = []
    if args and not args[0].startswith("-"):
        path = args[0]
        extra = args[1:]
    else:
        extra = args
    _sys.argv = [_sys.argv[0], "scan", path, "--fix", "--profile", "refactor"] + extra
    cli()


if __name__ == "__main__":
    main()
