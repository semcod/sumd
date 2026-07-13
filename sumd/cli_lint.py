"""Lint helpers — extracted from cli.py to reduce god-module size."""

from pathlib import Path
from typing import Optional

import click


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
