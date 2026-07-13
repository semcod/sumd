"""Focused regression tests for cli.py helper groups.

These helpers are slated for extraction into cohesive submodules
(cli_lint, cli_scaffold, cli_analyze, cli_dsl). They are imported from
``sumd.cli`` here so the same tests pin behaviour *before* and *after* the
extraction — proving the move preserves behaviour exactly.
"""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

# Imported from sumd.cli (re-exported post-extraction) so tests are stable
# across the refactor.
from sumd.cli import (
    _api_scenario_template,
    _lint_classify_issues,
    _lint_collect_paths,
    _lint_print_result,
    _print_scaffold_summary,
    _run_analyze_tool,
    _scaffold_from_openapi,
    _scaffold_write,
    _should_run_interactive,
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _codeblock(message: str, kind: str = "error", line: int = 1, lang: str = "yaml"):
    """Build a minimal codeblock object as returned by validate_sumd_file."""
    return SimpleNamespace(message=message, kind=kind, line=line, lang=lang)


def _lint_result(*, ok=True, markdown=(), codeblocks=(), logic=()):
    """Build a minimal lint result dict understood by the lint helpers."""
    return {"ok": ok, "markdown": list(markdown), "codeblocks": list(codeblocks), "logic": list(logic)}


# ===========================================================================
# cli_dsl: interactive-shell gating
# ===========================================================================

class TestShouldRunInteractive:
    """The DSL command's decision to drop into the interactive REPL."""

    def test_explicit_interactive_flag_wins(self):
        assert _should_run_interactive(True, command="scan('.')", script=None) is True

    def test_command_runs_and_exits(self):
        assert _should_run_interactive(False, command="scan('.')", script=None) is False

    def test_script_runs_and_exits(self):
        assert _should_run_interactive(False, command=None, script=Path("x.dsl")) is False

    def test_default_is_interactive(self):
        assert _should_run_interactive(False, command=None, script=None) is True


# ===========================================================================
# cli_lint: issue classification, path collection, printing
# ===========================================================================

class TestLintClassifyIssues:
    def test_non_strict_logic_issues_are_warnings(self):
        r = _lint_result(
            markdown=["bad H1"],
            codeblocks=[_codeblock("yaml err", "error"), _codeblock("warn me", "warning")],
            logic=["logic inconsistency"],
        )
        errors, warnings = _lint_classify_issues(r, strict=False)
        assert errors == ["bad H1", "yaml err"]
        assert warnings == ["warn me", "logic inconsistency"]

    def test_strict_promotes_logic_to_errors(self):
        r = _lint_result(logic=["logic inconsistency"])
        errors, warnings = _lint_classify_issues(r, strict=True)
        assert errors == ["logic inconsistency"]
        assert warnings == []

    def test_missing_logic_key_defaults_to_empty(self):
        r = {"ok": True, "markdown": ["m"], "codeblocks": []}
        errors, warnings = _lint_classify_issues(r, strict=False)
        assert errors == ["m"]
        assert warnings == []


class TestLintCollectPaths:
    def test_explicit_files_returned_verbatim(self, tmp_path: Path):
        f1, f2 = tmp_path / "a.md", tmp_path / "b.md"
        f1.write_text("x")
        f2.write_text("x")
        assert _lint_collect_paths((f1, f2), workspace=None) == [f1, f2]

    def test_workspace_finds_sumd_in_subdirs(self, tmp_path: Path):
        (tmp_path / "proj-a").mkdir()
        (tmp_path / "proj-a" / "SUMD.md").write_text("x")
        (tmp_path / "proj-b").mkdir()  # no SUMD.md → skipped
        (tmp_path / ".hidden").mkdir()
        (tmp_path / ".hidden" / "SUMD.md").write_text("x")  # dotdir → skipped

        paths = _lint_collect_paths((), workspace=tmp_path)
        assert [p.name for p in paths] == ["SUMD.md"]
        assert paths[0].parent.name == "proj-a"

    def test_combines_explicit_files_and_workspace(self, tmp_path: Path):
        explicit = tmp_path / "extra.md"
        explicit.write_text("x")
        (tmp_path / "proj").mkdir()
        (tmp_path / "proj" / "SUMD.md").write_text("x")
        paths = _lint_collect_paths((explicit,), workspace=tmp_path)
        assert explicit in paths
        assert any(p.parent.name == "proj" for p in paths)


class TestLintPrintResult:
    def test_prints_status_and_blocks(self, capsys):
        r = _lint_result(
            ok=False,
            markdown=["bad H1"],
            codeblocks=[_codeblock("yaml err", "error", line=4, lang="yaml")],
            logic=["logic x"],
        )
        _lint_print_result(Path("SUMD.md"), r, strict=False)
        out = capsys.readouterr().out
        assert "❌" in out  # not ok → cross
        assert "SUMD.md" in out
        assert "[markdown]" in out
        assert "[codeblock L4 yaml]" in out
        assert "[logic]" in out

    def test_strict_shows_logic_as_error(self, capsys):
        r = _lint_result(ok=True, logic=["logic x"])
        _lint_print_result(Path("SUMD.md"), r, strict=True)
        out = capsys.readouterr().out
        assert "[logic]" in out


# ===========================================================================
# cli_scaffold: OpenAPI → testql scenario generation
# ===========================================================================

class TestApiScenarioTemplate:
    def test_contains_metadata_and_endpoint_count(self):
        block = "  GET,  /users,  200\n  POST, /users,  201"
        out = _api_scenario_template("users", "api", block, base_path="/api/v1")
        assert "# SCENARIO: users" in out
        assert "# TYPE: api" in out
        assert "API[2]" in out  # two endpoints
        assert "base_path,  /api/v1" in out

    def test_default_base_path(self):
        out = _api_scenario_template("s", "smoke", "  GET, /health, 200")
        assert "base_path,  /api/v1" in out


class TestScaffoldWrite:
    def test_new_file_is_written_and_recorded(self, tmp_path: Path):
        generated, skipped = [], []
        path = tmp_path / "f.testql.toon.yaml"
        _scaffold_write(path, "body", force=False, generated=generated, skipped=skipped)
        assert path.read_text() == "body"
        assert generated == [path.name]
        assert skipped == []

    def test_existing_without_force_is_skipped(self, tmp_path: Path):
        path = tmp_path / "f.testql.toon.yaml"
        path.write_text("original")
        generated, skipped = [], []
        _scaffold_write(path, "new", force=False, generated=generated, skipped=skipped)
        assert path.read_text() == "original"  # untouched
        assert generated == []
        assert skipped == [path.name]

    def test_force_overwrites_existing(self, tmp_path: Path):
        path = tmp_path / "f.testql.toon.yaml"
        path.write_text("original")
        generated, skipped = [], []
        _scaffold_write(path, "new", force=True, generated=generated, skipped=skipped)
        assert path.read_text() == "new"
        assert generated == [path.name]
        assert skipped == []


class TestScaffoldFromOpenapi:
    def _spec(self, base_url="https://api.example.com/v2"):
        return {
            "openapi": "3.0.0",
            "servers": [{"url": base_url}],
            "paths": {
                "/health": {"get": {}},
                "/users": {"get": {}, "post": {}},
            },
        }

    def test_all_generates_smoke_and_crud(self, tmp_path: Path):
        generated, skipped = [], []
        n = _scaffold_from_openapi(
            self._spec(), tmp_path, "all", force=False, generated=generated, skipped=skipped
        )
        assert n == 2  # two paths
        assert (tmp_path / "smoke-health.testql.toon.yaml").exists()
        assert (tmp_path / "api-users.testql.toon.yaml").exists()
        # health is a well-known health path → not emitted as a crud resource
        assert not (tmp_path / "api-health.testql.toon.yaml").exists()

    def test_base_path_from_servers(self, tmp_path: Path):
        generated, skipped = [], []
        _scaffold_from_openapi(
            self._spec("https://api.example.com/v2/"), tmp_path, "all", False, generated, skipped
        )
        smoke = (tmp_path / "smoke-health.testql.toon.yaml").read_text()
        assert "api.example.com/v2" in smoke

    def test_smoke_only_skips_crud(self, tmp_path: Path):
        generated, skipped = [], []
        _scaffold_from_openapi(self._spec(), tmp_path, "smoke", False, generated, skipped)
        assert (tmp_path / "smoke-health.testql.toon.yaml").exists()
        assert not (tmp_path / "api-users.testql.toon.yaml").exists()


class TestPrintScaffoldSummary:
    def test_lists_generated_and_skipped(self, capsys, tmp_path: Path):
        _print_scaffold_summary(["a.testql.toon.yaml"], ["b.testql.toon.yaml"], tmp_path)
        out = capsys.readouterr().out
        assert "1 generated" in out
        assert "1 skipped" in out
        assert "a.testql.toon.yaml" in out
        assert "already exists" in out  # next to skipped entry

    def test_next_steps_only_when_something_generated(self, capsys, tmp_path: Path):
        _print_scaffold_summary([], [], tmp_path)
        out = capsys.readouterr().out
        assert "Next steps" not in out


# ===========================================================================
# cli_analyze: analysis-tool routing
# ===========================================================================

class TestRunAnalyzeTool:
    """Routing of code2llm/redup/vallm to the correct tool invocation."""

    def _make_bin(self, tmp_path: Path, *tools: str) -> Path:
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        for t in tools:
            (bin_dir / t).write_text("#!/bin/sh\nexit 0\n")
        return bin_dir

    def test_unknown_tool_returns_false(self, tmp_path: Path):
        bin_dir = self._make_bin(tmp_path)
        with patch("subprocess.run") as mock_run:
            assert _run_analyze_tool("nope", bin_dir, tmp_path, tmp_path) is False
        mock_run.assert_not_called()

    def test_redup_invokes_scan_with_toon_format(self, tmp_path: Path):
        project = tmp_path / "proj"
        project.mkdir()
        out = tmp_path / "out"
        bin_dir = self._make_bin(tmp_path, "redup")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = SimpleNamespace(returncode=0)
            assert _run_analyze_tool("redup", bin_dir, project, out) is True

        cmd = mock_run.call_args[0][0]
        assert cmd[0].endswith("redup")
        assert "scan" in cmd
        assert "--format" in cmd and "toon" in cmd

    def test_vallm_invokes_batch_recursive(self, tmp_path: Path):
        project = tmp_path / "proj"
        project.mkdir()
        out = tmp_path / "out"
        bin_dir = self._make_bin(tmp_path, "vallm")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = SimpleNamespace(returncode=0)
            assert _run_analyze_tool("vallm", bin_dir, project, out) is True

        cmd = mock_run.call_args[0][0]
        assert cmd[0].endswith("vallm")
        assert "batch" in cmd and "--recursive" in cmd

    def test_code2llm_runs_all_formats_and_reports_failure(self, tmp_path: Path):
        project = tmp_path / "proj"
        project.mkdir()
        out = tmp_path / "out"
        bin_dir = self._make_bin(tmp_path, "code2llm")
        # 5 formats expected; one fails → overall False.
        return_codes = [SimpleNamespace(returncode=0)] * 4 + [SimpleNamespace(returncode=1)]
        with patch("subprocess.run", side_effect=return_codes) as mock_run:
            assert _run_analyze_tool("code2llm", bin_dir, project, out) is False
        assert mock_run.call_count == 5
