"""Analysis-tool helpers — extracted from cli.py to reduce god-module size."""

import subprocess
import sys
from pathlib import Path

import click


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
