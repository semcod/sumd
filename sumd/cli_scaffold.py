"""Scaffold helpers — extracted from cli.py to reduce god-module size.

Generates testql scenario skeletons (``*.testql.toon.yaml``) from an OpenAPI
spec or a generic smoke fallback.
"""

import re
import sys
from pathlib import Path

import click


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
