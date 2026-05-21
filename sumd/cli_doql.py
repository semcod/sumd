"""DOQL generation helpers — extracted from cli.py to reduce god-module size."""

import re
from pathlib import Path

from sumd.extractor import extract_package_json, extract_pyproject


# Language-specific boilerplate for app.doql.less generation.
# Each entry defines a minimal DOQL skeleton for a project type so that
# `sumd <dir>` produces sensible defaults for any supported language.
_DOQL_SPECS: dict[str, dict[str, str]] = {
    "python": {
        "interface": 'interface[type="cli"] {\n  framework: click;\n}',
        "install": "pip install -e .",
        "dev":     'pip install -e ".[dev]"',
        "build":   "python -m build",
        "test":    "pytest -q",
        "lint":    "ruff check .",
        "fmt":     "ruff format .",
        "clean":   "rm -rf build/ dist/ *.egg-info",
        "deploy":  "pip",
        "runtime": "python",
    },
    "node": {
        "interface": 'interface[type="web"] {\n  framework: node;\n}',
        "install": "npm install",
        "dev":     "npm run dev",
        "build":   "npm run build",
        "test":    "npm test",
        "lint":    "npm run lint",
        "fmt":     "npm run format",
        "clean":   "rm -rf node_modules dist build .cache",
        "deploy":  "npm",
        "runtime": "node",
    },
    "rust": {
        "interface": 'interface[type="cli"] {\n  framework: clap;\n}',
        "install": "cargo fetch",
        "dev":     "cargo run",
        "build":   "cargo build --release",
        "test":    "cargo test",
        "lint":    "cargo clippy --all-targets --all-features -- -D warnings",
        "fmt":     "cargo fmt",
        "clean":   "cargo clean",
        "deploy":  "cargo",
        "runtime": "rust",
    },
    "go": {
        "interface": 'interface[type="cli"] {\n  framework: cobra;\n}',
        "install": "go mod download",
        "dev":     "go run ./...",
        "build":   "go build ./...",
        "test":    "go test ./...",
        "lint":    "golangci-lint run",
        "fmt":     "gofmt -w .",
        "clean":   "go clean ./...",
        "deploy":  "go",
        "runtime": "go",
    },
    "java": {
        "interface": 'interface[type="service"] {\n  framework: spring;\n}',
        "install": "mvn install -DskipTests",
        "dev":     "mvn compile",
        "build":   "mvn package",
        "test":    "mvn test",
        "lint":    "mvn verify",
        "fmt":     "mvn spotless:apply",
        "clean":   "mvn clean",
        "deploy":  "maven",
        "runtime": "jvm",
    },
    "ruby": {
        "interface": 'interface[type="cli"] {\n  framework: thor;\n}',
        "install": "bundle install",
        "dev":     "bundle exec rake",
        "build":   "gem build *.gemspec",
        "test":    "bundle exec rspec",
        "lint":    "bundle exec rubocop",
        "fmt":     "bundle exec rubocop -a",
        "clean":   "rm -rf pkg/",
        "deploy":  "rubygems",
        "runtime": "ruby",
    },
    "php": {
        "interface": 'interface[type="web"] {\n  framework: php;\n}',
        "install": "composer install",
        "dev":     "composer dev",
        "build":   "composer build",
        "test":    "vendor/bin/phpunit",
        "lint":    "vendor/bin/phpstan analyse",
        "fmt":     "vendor/bin/php-cs-fixer fix",
        "clean":   "rm -rf vendor/",
        "deploy":  "composer",
        "runtime": "php",
    },
    "dotnet": {
        "interface": 'interface[type="cli"] {\n  framework: dotnet;\n}',
        "install": "dotnet restore",
        "dev":     "dotnet run",
        "build":   "dotnet build -c Release",
        "test":    "dotnet test",
        "lint":    "dotnet format --verify-no-changes",
        "fmt":     "dotnet format",
        "clean":   "dotnet clean",
        "deploy":  "nuget",
        "runtime": "dotnet",
    },
    "swift": {
        "interface": 'interface[type="cli"] {\n  framework: swiftpm;\n}',
        "install": "swift package resolve",
        "dev":     "swift run",
        "build":   "swift build -c release",
        "test":    "swift test",
        "lint":    "swiftlint",
        "fmt":     "swiftformat .",
        "clean":   "swift package clean",
        "deploy":  "swiftpm",
        "runtime": "swift",
    },
    "dart": {
        "interface": 'interface[type="app"] {\n  framework: flutter;\n}',
        "install": "flutter pub get",
        "dev":     "flutter run",
        "build":   "flutter build",
        "test":    "flutter test",
        "lint":    "flutter analyze",
        "fmt":     "dart format .",
        "clean":   "flutter clean",
        "deploy":  "pub",
        "runtime": "dart",
    },
    "elixir": {
        "interface": 'interface[type="service"] {\n  framework: phoenix;\n}',
        "install": "mix deps.get",
        "dev":     "iex -S mix",
        "build":   "mix compile",
        "test":    "mix test",
        "lint":    "mix credo",
        "fmt":     "mix format",
        "clean":   "mix clean",
        "deploy":  "hex",
        "runtime": "beam",
    },
    "haskell": {
        "interface": 'interface[type="cli"] {\n  framework: optparse-applicative;\n}',
        "install": "cabal build --only-dependencies",
        "dev":     "cabal run",
        "build":   "cabal build",
        "test":    "cabal test",
        "lint":    "hlint .",
        "fmt":     "ormolu --mode=inplace .",
        "clean":   "cabal clean",
        "deploy":  "hackage",
        "runtime": "haskell",
    },
    "clojure": {
        "interface": 'interface[type="cli"] {\n  framework: tools.cli;\n}',
        "install": "clj -P",
        "dev":     "clj -M:dev",
        "build":   "clj -T:build",
        "test":    "clj -M:test",
        "lint":    "clj-kondo --lint src",
        "fmt":     "cljstyle fix",
        "clean":   "rm -rf target/",
        "deploy":  "clojars",
        "runtime": "jvm",
    },
    "cpp": {
        "interface": 'interface[type="cli"] {\n  framework: native;\n}',
        "install": "cmake -S . -B build",
        "dev":     "cmake --build build",
        "build":   "cmake --build build --config Release",
        "test":    "ctest --test-dir build",
        "lint":    "clang-tidy src/*.cpp",
        "fmt":     "clang-format -i src/*",
        "clean":   "rm -rf build/",
        "deploy":  "binary",
        "runtime": "native",
    },
    "generic": {
        "interface": 'interface[type="cli"] {\n  framework: shell;\n}',
        "install": "make install",
        "dev":     "make",
        "build":   "make build",
        "test":    "make test",
        "lint":    "make lint",
        "fmt":     "make fmt",
        "clean":   "make clean",
        "deploy":  "binary",
        "runtime": "shell",
    },
}


# Ordered list of (type, markers) used to detect the dominant project type.
# First match wins — pyproject.toml before requirements.txt, etc.
_PROJECT_TYPE_MARKERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("python",   ("pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "requirements.txt")),
    ("node",     ("package.json", "deno.json", "deno.jsonc", "bun.lockb")),
    ("rust",     ("Cargo.toml",)),
    ("go",       ("go.mod",)),
    ("java",     ("pom.xml", "build.gradle", "build.gradle.kts",
                  "settings.gradle", "settings.gradle.kts", "build.sbt")),
    ("ruby",     ("Gemfile",)),
    ("php",      ("composer.json",)),
    ("swift",    ("Package.swift",)),
    ("dart",     ("pubspec.yaml",)),
    ("elixir",   ("mix.exs",)),
    ("haskell",  ("stack.yaml", "cabal.project")),
    ("clojure",  ("project.clj", "deps.edn")),
    ("cpp",      ("CMakeLists.txt", "meson.build", "configure.ac")),
)

_PROJECT_TYPE_GLOBS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("dotnet",  ("*.csproj", "*.fsproj", "*.vbproj", "*.sln")),
    ("ruby",    ("*.gemspec",)),
    ("haskell", ("*.cabal",)),
)


def _detect_project_type(proj_dir: Path) -> str:
    """Return a coarse project-type tag (python, node, rust, …) or 'generic'."""
    for type_, markers in _PROJECT_TYPE_MARKERS:
        if any((proj_dir / m).exists() for m in markers):
            return type_
    for type_, patterns in _PROJECT_TYPE_GLOBS:
        for pattern in patterns:
            try:
                if next(proj_dir.glob(pattern), None) is not None:
                    return type_
            except (PermissionError, OSError):
                continue
    return "generic"


_DOQL_AUTOGEN_MARKER = "// Generated by sumd"


def _render_doql_boilerplate(
    project_name: str,
    spec: dict[str, str],
    extra_workflows: "dict[str, str] | None" = None,
) -> str:
    """Render a full app.doql.less boilerplate from a language spec.

    extra_workflows: additional {name: cmd} pairs rendered after the canonical
                     install/dev/build/test/lint/fmt/clean set — used to surface
                     project-specific scripts (e.g. npm scripts like
                     ``icons:generate``) so the file reflects the real project.
    """
    canonical = ("install", "dev", "build", "test", "lint", "fmt", "clean")
    blocks = [
        f'workflow[name="{wf}"] {{\n  trigger: manual;\n  step-1: run cmd={spec[wf]};\n}}'
        for wf in canonical
    ]
    for name, cmd in (extra_workflows or {}).items():
        blocks.append(
            f'workflow[name="{name}"] {{\n  trigger: manual;\n  step-1: run cmd={cmd};\n}}'
        )
    workflows = "\n\n".join(blocks)
    return f'''// LESS format — define @variables here as needed
{_DOQL_AUTOGEN_MARKER} for {project_name}

{{APP_BLOCK}}

{spec["interface"]}

{workflows}

workflow[name="help"] {{
  trigger: manual;
  step-1: run cmd=task --list;
}}

deploy {{
  target: {spec["deploy"]};
}}

environment[name="local"] {{
  runtime: {spec["runtime"]};
}}
'''


# Ordered framework detectors for Node projects — first match wins.
# Entries earlier in the list are more specific (Next before React, etc.).
_NODE_FRAMEWORKS: tuple[tuple[str, frozenset[str]], ...] = (
    ("next",      frozenset({"next"})),
    ("nuxt",      frozenset({"nuxt", "nuxt3"})),
    ("astro",     frozenset({"astro"})),
    ("remix",     frozenset({"@remix-run/react", "@remix-run/node"})),
    ("sveltekit", frozenset({"@sveltejs/kit"})),
    ("svelte",    frozenset({"svelte"})),
    ("vue",       frozenset({"vue", "nuxt"})),
    ("react",     frozenset({"react"})),
    ("angular",   frozenset({"@angular/core"})),
    ("solid",     frozenset({"solid-js"})),
    ("vite",      frozenset({"vite"})),
    ("webpack",   frozenset({"webpack"})),
    ("nestjs",    frozenset({"@nestjs/core"})),
    ("fastify",   frozenset({"fastify"})),
    ("express",   frozenset({"express"})),
)


def _node_framework(deps: set[str]) -> str:
    """Derive a framework label for a Node project from its dep set."""
    base = "node"
    for fw, markers in _NODE_FRAMEWORKS:
        if deps & markers:
            base = fw
            break
    if "typescript" in deps:
        return f"{base}+typescript" if base != "node" else "typescript"
    return base


# Script names consumed by the canonical install/dev/build/test/lint/fmt/clean
# workflows — these must NOT also appear as extra workflows (would duplicate).
_NODE_CANONICAL_SCRIPTS: frozenset[str] = frozenset({
    "install", "dev", "start", "serve",
    "build", "test",
    "lint", "fmt", "format", "lint:fix",
    "clean",
})


def _node_spec_from_package_json(
    pkg_json: dict,
) -> tuple[dict[str, str], dict[str, str]]:
    """Return (spec, extra_workflows) tailored to an actual package.json.

    - Workflows reuse real npm scripts when present (``npm run <name>``) and
      fall back to sensible defaults otherwise.
    - Framework label reflects detected deps (react, vite, next, …) plus a
      ``+typescript`` suffix when TS tooling is in use.
    - Every non-canonical script is exposed as an extra workflow so the file
      mirrors the real project surface (e.g. ``icons:generate``, ``test:e2e``).
    """
    scripts: dict[str, str] = pkg_json.get("scripts") or {}
    deps: set[str] = set(pkg_json.get("dependencies") or []) | set(
        pkg_json.get("dev_dependencies") or []
    )

    framework = _node_framework(deps)
    spec = dict(_DOQL_SPECS["node"])
    spec["interface"] = f'interface[type="web"] {{\n  framework: {framework};\n}}'

    def pick(*candidates: str, fallback: str) -> str:
        for n in candidates:
            if n in scripts:
                return f"npm run {n}"
        return fallback

    spec["install"] = "npm install"
    spec["dev"]     = pick("dev", "start", "serve", fallback="npm run dev")
    spec["build"]   = pick("build", fallback="npm run build")
    spec["test"]    = "npm test" if "test" in scripts else spec["test"]
    spec["lint"]    = pick("lint", fallback="npm run lint")
    spec["fmt"]     = pick("fmt", "format", "lint:fix", fallback="npm run format")
    spec["clean"]   = pick("clean", fallback="rm -rf node_modules dist build .cache")

    extras = {
        name: f"npm run {name}"
        for name in scripts
        if name not in _NODE_CANONICAL_SCRIPTS
    }
    return spec, extras


def _build_doql_spec(
    proj_dir: Path, project_type: str,
) -> tuple[dict[str, str], dict[str, str]]:
    """Return (spec, extra_workflows) for the given project type.

    For Node projects, the spec is derived from the actual package.json so
    the generated DOQL mirrors the real project. For every other type we
    use the static language defaults in ``_DOQL_SPECS``.
    """
    if project_type == "node":
        pkg_json = extract_package_json(proj_dir)
        if pkg_json:
            return _node_spec_from_package_json(pkg_json)
    spec = _DOQL_SPECS.get(project_type, _DOQL_SPECS["generic"])
    return dict(spec), {}


def _generate_doql_less(
    proj_dir: Path,
    project_name: str,
    version: str = "0.1.0",
    force: bool = False,
    project_type: str = "python",
) -> Path | None:
    """Generate or refresh app.doql.less file.

    - If file does not exist: create from language-appropriate boilerplate.
    - If file exists and force=False: skip (return None).
    - If file exists and force=True:
        * files originally emitted by sumd (identified by the auto-gen marker)
          are fully regenerated so they stay in sync with the project;
        * user-authored files keep all their content — only the ``app { }``
          metadata block is refreshed in place.

    Returns the path to the generated/updated file, or None if skipped.
    """
    doql_path = proj_dir / "app.doql.less"
    if doql_path.exists() and not force:
        return None

    app_block = f"""app {{\n  name: {project_name};\n  version: {version};\n}}"""

    if doql_path.exists() and force:
        content = doql_path.read_text(encoding="utf-8")
        if _DOQL_AUTOGEN_MARKER not in content:
            # User-authored: preserve body, refresh only the metadata block.
            if re.search(r"app\s*\{[^}]*\}", content, flags=re.DOTALL):
                new_content = re.sub(
                    r"app\s*\{[^}]*\}",
                    app_block,
                    content,
                    count=1,
                    flags=re.DOTALL,
                )
            else:
                new_content = app_block + "\n\n" + content
            doql_path.write_text(new_content, encoding="utf-8")
            return doql_path
        # Fall through: auto-generated → fully regenerate below.

    # Fresh boilerplate, tailored to the detected language AND project scripts.
    spec, extras = _build_doql_spec(proj_dir, project_type)
    content = _render_doql_boilerplate(project_name, spec, extras).replace(
        "{APP_BLOCK}", app_block
    )
    doql_path.write_text(content, encoding="utf-8")
    return doql_path

