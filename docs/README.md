<!-- code2docs:start --># sumd

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.10-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-553-green)
> **553** functions | **104** classes | **126** files | CC̄ = 3.7

> Auto-generated project documentation from source code analysis.

**Author:** Tom Sapletta  
**License:** Apache-2.0[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/oqlos/statement](https://github.com/oqlos/statement)

## Installation

### From PyPI

```bash
pip install sumd
```

### From Source

```bash
git clone https://github.com/oqlos/statement
cd sumd
pip install -e .
```

### Optional Extras

```bash
pip install sumd[mcp]    # mcp features
pip install sumd[dev]    # development tools
```

## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
sumd ./my-project

# Only regenerate README
sumd ./my-project --readme-only

# Preview what would be generated (no file writes)
sumd ./my-project --dry-run

# Check documentation health
sumd check ./my-project

# Sync — regenerate only changed modules
sumd sync ./my-project
```

### Python API

```python
from sumd import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```




## Architecture

```
sumd/
├── swop
├── goal
├── test
├── TODO
├── Makefile
├── working_script
├── koru
    ├── pre-commit-config
    ├── guards
├── script
├── pyqual
├── pyproject
├── tree
├── print_errors
├── mcp
├── CHANGELOG
├── Taskfile
├── simple_script
├── project
├── SPEC
├── README
    ├── USAGE
    ├── TESTQL_AUTOLOOP_ONBOARDING
    ├── README
    ├── sumd
    ├── README
        ├── anthropic_example
        ├── ollama_example
        ├── llm_cli_example
        ├── context_injection
        ├── openai_example
        ├── README
        ├── mcp_client
        ├── claude_desktop_config
        ├── continue_config
        ├── cursor_mcp
        ├── README
        ├── demo
        ├── README
            ├── goal
            ├── sumd
            ├── pyproject
            ├── Taskfile
            ├── openapi
            ├── README
        ├── makefile
        ├── taskfile
        ├── vscode-tasks
        ├── docker-compose
        ├── pre-commit-config
        ├── github-actions
        ├── Dockerfile
        ├── README
    ├── toon_parser
    ├── validator
    ├── cli
    ├── generator
    ├── prolog_engine
├── sumd/
    ├── __main__
    ├── extractor
    ├── parser
    ├── rules
    ├── cli_scan
    ├── models
    ├── cli_doql
    ├── renderer
    ├── pipeline
    ├── mcp_server
        ├── base
        ├── interfaces
        ├── refactor_analysis
        ├── quality
        ├── deployment
        ├── code_analysis
        ├── metadata
    ├── sections/
        ├── dependencies
        ├── call_graph
        ├── architecture
        ├── source_snippets
        ├── workflows
        ├── swop
        ├── extras
        ├── api_stubs
        ├── environment
        ├── configuration
            ├── render
        ├── utils/
            ├── should_render
        ├── prolog_core
    ├── utils/
        ├── aggregates
        ├── commands
        ├── events
        ├── sumd_aggregate
    ├── cqrs/
        ├── queries
        ├── engine
        ├── schema
        ├── lexer
        ├── commands
    ├── dsl/
        ├── parser
        ├── context_mixin
        ├── shell
        ├── schema_commands
        ├── ast_nodes
        ├── nlp
    ├── install_testql_autoloop
    ├── bootstrap
            ├── toon
            ├── toon
            ├── toon
    ├── requirements
    ├── pyproject
    ├── README
        ├── cli
    ├── sumd_logic_validator/
        ├── main
        ├── logic/
            ├── rules
```

## API Overview

### Classes

- **`CodeBlockIssue`** — —
- **`SUMDParser`** — Parser for SUMD markdown documents.
- **`SectionType`** — SUMD section types.
- **`Section`** — Represents a SUMD section.
- **`SUMDDocument`** — Represents a parsed SUMD document.
- **`RenderPipeline`** — Collect project data → build sections → render → inject TOC.
- **`RenderContext`** — All extracted data for a project, passed to every Section.render().
- **`Section`** — Protocol for all SUMD section renderers.
- **`InterfacesSection`** — —
- **`RefactorAnalysisSection`** — —
- **`QualitySection`** — —
- **`DeploymentSection`** — —
- **`CodeAnalysisSection`** — —
- **`MetadataSection`** — Render ## Metadata — always present, all profiles.
- **`DependenciesSection`** — —
- **`CallGraphSection`** — —
- **`ArchitectureSection`** — —
- **`SourceSnippetsSection`** — —
- **`WorkflowsSection`** — —
- **`SwopSection`** — —
- **`ExtrasSection`** — —
- **`ApiStubsSection`** — —
- **`EnvironmentSection`** — —
- **`ConfigurationSection`** — —
- **`Variable`** — Represents a logical variable in our pure Python engine.
- **`Term`** — Represents a Prolog term (e.g. parent(john, mary)).
- **`Rule`** — Represents a Prolog rule Head :- Body.
- **`PythonPrologDB`** — In-memory Prolog database for pure Python execution.
- **`PythonPrologEngine`** — SLD Resolution Logic Interpreter.
- **`HybridPrologEngine`** — Hybrid Logic Engine delegating queries based on backend availability.
- **`AggregateRoot`** — Base aggregate root for event sourcing.
- **`EntityState`** — Base entity state for aggregates.
- **`Entity`** — Base entity for domain objects.
- **`ValueObject`** — Base value object.
- **`Repository`** — Base repository for aggregates.
- **`EventSourcedRepository`** — Event-sourced repository implementation.
- **`Command`** — Base command class for CQRS pattern.
- **`CommandHandler`** — Base command handler interface.
- **`CommandBus`** — Command bus for dispatching commands to appropriate handlers.
- **`CreateSumdDocument`** — Command to create a new SUMD document.
- **`UpdateSumdDocument`** — Command to update an existing SUMD document.
- **`AddSumdSection`** — Command to add a section to a SUMD document.
- **`RemoveSumdSection`** — Command to remove a section from a SUMD document.
- **`ValidateSumdDocument`** — Command to validate a SUMD document.
- **`ScanProject`** — Command to scan a project and generate SUMD.
- **`GenerateMap`** — Command to generate project map.
- **`ExecuteDslCommand`** — Command to execute DSL command.
- **`SumdCommandHandler`** — Base handler for SUMD commands.
- **`Event`** — Base event class for event sourcing.
- **`EventStore`** — In-memory event store with optional file persistence.
- **`SumdDocumentCreated`** — Event fired when a SUMD document is created.
- **`SumdDocumentUpdated`** — Event fired when a SUMD document is updated.
- **`SumdSectionAdded`** — Event fired when a section is added to SUMD document.
- **`SumdSectionRemoved`** — Event fired when a section is removed from SUMD document.
- **`SumdDocumentValidated`** — Event fired when a SUMD document is validated.
- **`SumdCommandExecuted`** — Event fired when a SUMD command is executed.
- **`SumdSection`** — Represents a section in a SUMD document.
- **`SumdDocumentState`** — State of a SUMD document aggregate.
- **`SumdAggregate`** — SUMD document aggregate root.
- **`Query`** — Base query class for CQRS pattern.
- **`QueryHandler`** — Base query handler interface.
- **`QueryBus`** — Query bus for dispatching queries to appropriate handlers.
- **`GetSumdDocument`** — Query to get a SUMD document.
- **`ListSumdSections`** — Query to list sections in a SUMD document.
- **`GetSumdSection`** — Query to get a specific section from a SUMD document.
- **`GetProjectInfo`** — Query to get project information.
- **`GetEventHistory`** — Query to get event history for an aggregate.
- **`GetAllEvents`** — Query to get all events from the event store.
- **`SearchDocuments`** — Query to search SUMD documents.
- **`GetValidationResults`** — Query to get validation results for a document.
- **`ExecuteDslQuery`** — Query to execute DSL query.
- **`SumdQueryHandler`** — Handler for SUMD queries.
- **`DSLContext`** — Execution context for DSL expressions.
- **`DSLEngine`** — Engine for executing DSL expressions.
- **`DSLDataType`** — Supported data types in DSL.
- **`DSLCommandType`** — Supported command types in DSL.
- **`DSLActionType`** — Supported action types in DSL.
- **`DSLParameter`** — DSL parameter definition.
- **`DSLCommandSchema`** — DSL command schema definition.
- **`DSLProjectSchema`** — DSL project schema definition.
- **`DSLExpression`** — DSL expression model.
- **`DSLStatement`** — DSL statement model.
- **`DSLScript`** — DSL script model.
- **`NLPIntent`** — NLP intent model.
- **`NLPEntity`** — NLP entity model.
- **`NLPModel`** — NLP model configuration.
- **`DSLContext`** — DSL execution context model.
- **`DSLCommandResult`** — DSL command execution result.
- **`DSLTokenType`** — Token types for DSL parsing.
- **`DSLToken`** — Token in DSL.
- **`DSLLexer`** — Lexer for tokenizing DSL expressions.
- **`DSLCommand`** — DSL command definition.
- **`DSLCommandRegistry`** — Registry for DSL commands.
- **`DSLParser`** — Parser for DSL expressions.
- **`VariableMixin`** — Mixin providing set_variable / get_variable helpers.
- **`DSLShell`** — Interactive shell for SUMD DSL.
- **`DSLShellServer`** — Server for DSL shell operations (for MCP integration).
- **`SchemaCommandRegistry`** — Registry for schema-based DSL commands.
- **`SchemaBasedCommands`** — Implementation of schema-based DSL commands.
- **`DSLExpressionType`** — Types of DSL expressions.
- **`DSLExpression`** — Expression in DSL.
- **`NLPProcessor`** — Natural Language Processor for DSL commands.
- **`NLPIntegration`** — NLP integration for DSL engine.
- **`SimpleNLPModel`** — Simple NLP model implementation for basic functionality.

### Functions

- `print()` — —
- `print()` — —
- `print()` — —
- `write_file()` — —
- `print()` — —
- `write_file()` — —
- `print()` — —
- `scan()` — —
- `validate()` — —
- `ask(sumd_path, question, model)` — —
- `main()` — —
- `build_context(sumd_path)` — Return a focused context string from SUMD.md.
- `ask(sumd_path, question, model)` — —
- `main()` — —
- `run(sumd_file, single_tool, tool_args)` — —
- `main()` — —
- `extract_testql_scenarios(proj_dir)` — Scan all *.testql.toon.yaml and testql-scenarios/*.yaml files in project.
- `validate_codeblocks(content, source)` — Validate all fenced code blocks in *content*.
- `validate_markdown(content, source, profile)` — Validate SUMD markdown structure.
- `validate_project_architecture(proj_dir)` — Run Prolog-based architectural consistency checks on the project.
- `validate_sumd_file(path, profile)` — Run all validators on a SUMD.md file.
- `cli()` — SUMD - Structured Unified Markdown Descriptor CLI.
- `validate(file)` — Validate a SUMD document.
- `export(file, format, output)` — Export a SUMD document to structured format.
- `info(file)` — Display information about a SUMD document.
- `generate(file, format, output)` — Generate a SUMD document from structured format.
- `extract(file, section)` — Extract content from a SUMD document.
- `scan(workspace, export_json, report, fix)` — Scan a workspace directory and generate SUMD.md for every project found.
- `lint(files, workspace, as_json, strict)` — Validate SUMD.md files — check markdown structure and codeblock formats.
- `analyze(project, tools, force)` — Run analysis tools (code2llm, redup, vallm) on a project.
- `scaffold(project, output, force, scenario_type)` — Generate testql scenario scaffolds from OpenAPI spec or SUMD.md.
- `map_cmd(project, output, force, stdout)` — Generate project/map.toon.yaml — static code map in toon format.
- `dsl(directory, command, script, interactive)` — SUMD DSL Shell - Domain Specific Language for SUMD operations.
- `cqrs_command(directory, command_type, aggregate_id, data)` — Execute CQRS command on SUMD aggregate.
- `nlp_command(text, directory, execute, verbose)` — Process natural language text and convert to DSL commands.
- `main()` — Main entry point — if first arg is a path, run 'scan <path> --fix'.
- `main_sumr()` — Entry point for `sumr` command — generates SUMR.md (refactor profile).
- `extract_pyproject(proj_dir)` — —
- `extract_taskfile(proj_dir)` — —
- `extract_openapi(proj_dir)` — —
- `extract_doql(proj_dir)` — Read app.doql.less (preferred) or app.doql.css as fallback.
- `extract_pyqual(proj_dir)` — —
- `extract_python_modules(proj_dir, pkg_name)` — —
- `extract_readme_title(proj_dir)` — —
- `extract_requirements(proj_dir)` — Parse requirements*.txt files — return list of {file, deps[]}.
- `extract_makefile(proj_dir)` — Parse Makefile — return list of {target, comment}.
- `extract_goal(proj_dir)` — Parse goal.yaml — versioning strategy, git conventions, build strategies.
- `extract_env(proj_dir)` — Parse .env.example — return list of {key, default, comment}.
- `extract_dockerfile(proj_dir)` — Parse Dockerfile — base image, exposed ports, entrypoint, labels.
- `extract_docker_compose(proj_dir)` — Parse docker-compose*.yml — services with images, ports, environment.
- `extract_package_json(proj_dir)` — Parse package.json — name, version, scripts, dependencies.
- `generate_map_toon(proj_dir)` — Generate project/map.toon.yaml content for proj_dir.
- `generate_project_logic(proj_dir)` — Generate project/logic.pl containing Prolog facts representing the project structure.
- `required_tools_for_profile(profile)` — Return the set of external tools needed to refresh analysis files for *profile*.
- `extract_source_snippets(proj_dir, pkg_name)` — Return per-module AST summary for source_snippets section.
- `extract_swop(proj_dir)` — Extract SWOP manifest files from .swop/manifests/<context>/ directory.
- `extract_project_analysis(proj_dir, refactor)` — Return list of {file, lang, content} for files present in project/ subdir.
- `parse(content)` — Parse a SUMD markdown document.
- `parse_file(path)` — Parse a SUMD file — delegates to parse for DRY.
- `validate(document)` — Validate a SUMD document.
- `generate_sumd_content(proj_dir, return_sources, raw_sources, profile)` — Generate SUMD.md content from a project directory.
- `list_tools()` — —
- `call_tool(name, arguments)` — —
- `main()` — —
- `call_with_ctx(render_fn)` — Return a ``render`` method that calls *render_fn* with ctx attributes.
- `always(_self, _ctx)` — Always render the section.
- `has_attr(attr)` — Return a ``should_render`` that checks ``bool(ctx.<attr>)``.
- `is_variable(x)` — —
- `to_term(x)` — —
- `unify(x, y, subst)` — Logical unification of x and y under substitution subst.
- `resolve_val(x, subst)` — —
- `deep_resolve(x, subst)` — —
- `extend_subst(v, val, subst)` — —
- `occurs_check(v, val, subst)` — —
- `rename_variables(rule, suffix)` — Rename variables in rule to avoid collisions in resolution.
- `create_builtin_registry()` — Create registry with built-in commands.
- `parse_dsl(text)` — Parse DSL text into expression.
- `main()` — Main entry point for DSL shell.
- `log()` — —
- `write_if_missing()` — —
- `get_engine()` — —
- `main()` — 🧠 Hybrid Python-Prolog logic runner CLI.
- `info()` — Display information about the available Prolog backends.
- `query(query_str)` — Query the logic rules.
- `shell()` — Start interactive logic query shell.


## Project Structure

📄 `.pre-commit-config`
📄 `CHANGELOG`
📄 `Makefile`
📄 `README` (4 functions)
📄 `SPEC`
📄 `TODO`
📄 `Taskfile`
📄 `Taskfile.guards`
📄 `docs.README`
📄 `docs.TESTQL_AUTOLOOP_ONBOARDING`
📄 `docs.USAGE`
📄 `examples.README`
📄 `examples.basic.README`
📄 `examples.basic.demo`
📄 `examples.basic.sample-project.README`
📄 `examples.basic.sample-project.Taskfile`
📄 `examples.basic.sample-project.goal`
📄 `examples.basic.sample-project.openapi`
📄 `examples.basic.sample-project.pyproject`
📄 `examples.basic.sample-project.sumd`
📄 `examples.integrations.Dockerfile`
📄 `examples.integrations.README`
📄 `examples.integrations.docker-compose`
📄 `examples.integrations.github-actions`
📄 `examples.integrations.makefile`
📄 `examples.integrations.pre-commit-config`
📄 `examples.integrations.taskfile`
📄 `examples.integrations.vscode-tasks`
📄 `examples.llm.README`
📄 `examples.llm.anthropic_example` (2 functions)
📄 `examples.llm.context_injection`
📄 `examples.llm.llm_cli_example`
📄 `examples.llm.ollama_example`
📄 `examples.llm.openai_example` (3 functions)
📄 `examples.mcp.README`
📄 `examples.mcp.claude_desktop_config`
📄 `examples.mcp.continue_config`
📄 `examples.mcp.cursor_mcp`
📄 `examples.mcp.mcp_client` (2 functions)
📄 `examples.sumd`
📄 `goal`
📄 `koru`
📄 `mcp`
📄 `print_errors`
📄 `project`
📄 `pyproject`
📄 `pyqual`
📄 `script` (19 functions)
📄 `scripts.bootstrap`
📄 `scripts.install_testql_autoloop` (2 functions)
📄 `simple_script` (17 functions)
📦 `sumd`
📄 `sumd.__main__`
📄 `sumd.cli` (29 functions)
📄 `sumd.cli_doql` (6 functions)
📄 `sumd.cli_scan` (14 functions)
📦 `sumd.cqrs`
📄 `sumd.cqrs.aggregates` (23 functions, 6 classes)
📄 `sumd.cqrs.commands` (8 functions, 12 classes)
📄 `sumd.cqrs.events` (8 functions, 8 classes)
📄 `sumd.cqrs.queries` (17 functions, 13 classes)
📄 `sumd.cqrs.sumd_aggregate` (18 functions, 3 classes)
📦 `sumd.dsl`
📄 `sumd.dsl.ast_nodes` (1 functions, 2 classes)
📄 `sumd.dsl.commands` (30 functions, 2 classes)
📄 `sumd.dsl.context_mixin` (2 functions, 1 classes)
📄 `sumd.dsl.engine` (39 functions, 2 classes)
📄 `sumd.dsl.lexer` (2 functions, 3 classes)
📄 `sumd.dsl.nlp` (21 functions, 3 classes)
📄 `sumd.dsl.parser` (36 functions, 1 classes)
📄 `sumd.dsl.schema` (1 functions, 14 classes)
📄 `sumd.dsl.schema_commands` (33 functions, 2 classes)
📄 `sumd.dsl.shell` (14 functions, 2 classes)
📄 `sumd.extractor` (63 functions)
📄 `sumd.generator`
📄 `sumd.mcp_server` (18 functions)
📄 `sumd.models` (3 classes)
📄 `sumd.parser` (9 functions, 1 classes)
📄 `sumd.pipeline` (16 functions, 1 classes)
📄 `sumd.prolog_engine`
📄 `sumd.renderer` (1 functions)
📄 `sumd.rules`
📦 `sumd.sections`
📄 `sumd.sections.api_stubs` (2 functions, 1 classes)
📄 `sumd.sections.architecture` (9 functions, 1 classes)
📄 `sumd.sections.base` (2 functions, 2 classes)
📄 `sumd.sections.call_graph` (7 functions, 1 classes)
📄 `sumd.sections.code_analysis` (3 functions, 1 classes)
📄 `sumd.sections.configuration` (1 functions, 1 classes)
📄 `sumd.sections.dependencies` (4 functions, 1 classes)
📄 `sumd.sections.deployment` (5 functions, 1 classes)
📄 `sumd.sections.environment` (4 functions, 1 classes)
📄 `sumd.sections.extras` (4 functions, 1 classes)
📄 `sumd.sections.interfaces` (8 functions, 1 classes)
📄 `sumd.sections.metadata` (1 functions, 1 classes)
📄 `sumd.sections.quality` (3 functions, 1 classes)
📄 `sumd.sections.refactor_analysis` (1 functions, 1 classes)
📄 `sumd.sections.source_snippets` (1 functions, 1 classes)
📄 `sumd.sections.swop` (2 functions, 1 classes)
📦 `sumd.sections.utils`
📄 `sumd.sections.utils.render` (1 functions)
📄 `sumd.sections.utils.should_render` (2 functions)
📄 `sumd.sections.workflows` (4 functions, 1 classes)
📄 `sumd.toon_parser` (9 functions)
📦 `sumd.utils`
📄 `sumd.utils.prolog_core` (32 functions, 6 classes)
📄 `sumd.validator` (16 functions, 1 classes)
📄 `sumd_logic_validator.README`
📄 `sumd_logic_validator.pyproject`
📄 `sumd_logic_validator.requirements`
📦 `sumd_logic_validator.sumd_logic_validator`
📄 `sumd_logic_validator.sumd_logic_validator.cli` (5 functions)
📦 `sumd_logic_validator.sumd_logic_validator.logic`
📄 `sumd_logic_validator.sumd_logic_validator.logic.rules`
📄 `sumd_logic_validator.sumd_logic_validator.main`
📄 `swop`
📄 `test` (1 functions)
📄 `testql-scenarios.generated-cli-tests.testql.toon`
📄 `testql-scenarios.generated-from-pytests.testql.toon`
📄 `testql-scenarios.sumd-cli.testql.toon`
📄 `tree`
📄 `working_script` (12 functions)

## Requirements

- Python >= >=3.10
- click >=8.4.0- pyyaml >=6.0.3- toml >=0.10.2- goal >=2.1.190- costs >=0.1.51- pfix >=0.1.73- mcp >=1.27.1

## Contributing

**Contributors:**
- Tom Softreck <tom@sapletta.com>
- Tom Sapletta <tom-sapletta-com@users.noreply.github.com>

We welcome contributions! Open an issue or pull request to get started.
### Development Setup

```bash
# Clone the repository
git clone https://github.com/oqlos/statement
cd sumd

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `examples` | Usage examples and code samples | [View](./examples) |

<!-- code2docs:end -->