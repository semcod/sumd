% ── AUTO-GENERATED ARCHITECTURAL FACTS ────────────────────
% ── Project Metadata ─────────────────────────────────────
project_metadata('sumd', '0.3.46', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 261, 'less').
project_file('examples/app.doql.less', 60, 'less').
project_file('examples/basic/demo.sh', 50, 'shell').
project_file('examples/llm/anthropic_example.py', 61, 'python').
project_file('examples/llm/llm_cli_example.sh', 37, 'shell').
project_file('examples/llm/ollama_example.sh', 38, 'shell').
project_file('examples/llm/openai_example.py', 89, 'python').
project_file('examples/mcp/mcp_client.py', 139, 'python').
project_file('print_errors.py', 7, 'python').
project_file('project.sh', 41, 'shell').
project_file('scripts/bootstrap.sh', 70, 'shell').
project_file('scripts/install_testql_autoloop.sh', 157, 'shell').
project_file('sumd/__init__.py', 36, 'python').
project_file('sumd/__main__.py', 6, 'python').
project_file('sumd/cli.py', 2000, 'python').
project_file('sumd/cqrs/__init__.py', 19, 'python').
project_file('sumd/cqrs/aggregates.py', 221, 'python').
project_file('sumd/cqrs/commands.py', 266, 'python').
project_file('sumd/cqrs/events.py', 185, 'python').
project_file('sumd/cqrs/queries.py', 420, 'python').
project_file('sumd/cqrs/sumd_aggregate.py', 345, 'python').
project_file('sumd/dsl/__init__.py', 15, 'python').
project_file('sumd/dsl/commands.py', 657, 'python').
project_file('sumd/dsl/engine.py', 595, 'python').
project_file('sumd/dsl/nlp.py', 448, 'python').
project_file('sumd/dsl/parser.py', 667, 'python').
project_file('sumd/dsl/schema.py', 352, 'python').
project_file('sumd/dsl/schema_commands.py', 518, 'python').
project_file('sumd/dsl/shell.py', 360, 'python').
project_file('sumd/extractor.py', 1283, 'python').
project_file('sumd/generator.py', 16, 'python').
project_file('sumd/mcp_server.py', 715, 'python').
project_file('sumd/models.py', 46, 'python').
project_file('sumd/parser.py', 196, 'python').
project_file('sumd/pipeline.py', 452, 'python').
project_file('sumd/prolog_engine.py', 431, 'python').
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
project_file('sumd/toon_parser.py', 174, 'python').
project_file('sumd/validator.py', 384, 'python').
project_file('sumd_logic_validator/logic/__init__.py', 2, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/__init__.py', 4, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/cli.py', 115, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/engine.py', 435, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/logic/__init__.py', 2, 'python').
project_file('sumd_logic_validator/sumd_logic_validator/main.py', 5, 'python').
project_file('sumd_logic_validator/tests/__init__.py', 1, 'python').
project_file('sumd_logic_validator/tests/test_engine.py', 52, 'python').
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

% ── Python Functions ─────────────────────────────────────
python_function('examples/llm/anthropic_example.py', 'ask', 3, 1, 3).
python_function('examples/llm/anthropic_example.py', 'main', 0, 2, 8).
python_function('examples/llm/openai_example.py', 'build_context', 1, 5, 5).
python_function('examples/llm/openai_example.py', 'ask', 3, 1, 3).
python_function('examples/llm/openai_example.py', 'main', 0, 2, 8).
python_function('examples/mcp/mcp_client.py', 'run', 3, 12, 12).
python_function('examples/mcp/mcp_client.py', 'main', 0, 2, 9).
python_function('sumd/cli.py', '_detect_project_type', 1, 7, 4).
python_function('sumd/cli.py', '_render_doql_boilerplate', 3, 3, 3).
python_function('sumd/cli.py', '_node_framework', 1, 4, 0).
python_function('sumd/cli.py', '_node_spec_from_package_json', 1, 6, 5).
python_function('sumd/cli.py', '_build_doql_spec', 2, 3, 4).
python_function('sumd/cli.py', '_generate_doql_less', 5, 7, 8).
python_function('sumd/cli.py', 'cli', 0, 1, 2).
python_function('sumd/cli.py', 'validate', 1, 4, 8).
python_function('sumd/cli.py', 'export', 3, 7, 11).
python_function('sumd/cli.py', 'info', 1, 3, 7).
python_function('sumd/cli.py', 'generate', 3, 8, 15).
python_function('sumd/cli.py', 'extract', 2, 5, 8).
python_function('sumd/cli.py', '_is_project_dir', 1, 6, 4).
python_function('sumd/cli.py', '_walk_projects', 4, 10, 7).
python_function('sumd/cli.py', '_detect_projects', 2, 1, 1).
python_function('sumd/cli.py', '_ensure_venv', 3, 4, 4).
python_function('sumd/cli.py', '_tool_bin', 2, 1, 1).
python_function('sumd/cli.py', '_run_one_tool', 4, 2, 5).
python_function('sumd/cli.py', '_run_analysis_tools', 3, 5, 5).
python_function('sumd/cli.py', '_export_sumd_json', 2, 1, 2).
python_function('sumd/cli.py', '_render_write_validate', 4, 1, 5).
python_function('sumd/cli.py', '_echo_scan_result', 4, 1, 3).
python_function('sumd/cli.py', '_maybe_generate_doql', 2, 6, 6).
python_function('sumd/cli.py', '_maybe_generate_testql', 1, 5, 5).
python_function('sumd/cli.py', '_finalize_scan', 9, 8, 9).
python_function('sumd/cli.py', '_scan_one_project', 11, 8, 9).
python_function('sumd/cli.py', 'scan', 14, 9, 18).
python_function('sumd/cli.py', 'lint', 4, 7, 13).
python_function('sumd/cli.py', '_lint_collect_paths', 2, 4, 7).
python_function('sumd/cli.py', '_lint_print_result', 2, 4, 3).
python_function('sumd/cli.py', '_setup_tools_venv', 3, 6, 6).
python_function('sumd/cli.py', '_run_code2llm_formats', 3, 4, 4).
python_function('sumd/cli.py', '_run_tool_subprocess', 3, 3, 4).
python_function('sumd/cli.py', 'analyze', 3, 8, 17).
python_function('sumd/cli.py', '_api_scenario_template', 4, 1, 3).
python_function('sumd/cli.py', '_scaffold_write', 5, 3, 3).
python_function('sumd/cli.py', '_scaffold_smoke_scenario', 6, 1, 5).
python_function('sumd/cli.py', '_scaffold_crud_scenarios', 6, 4, 7).
python_function('sumd/cli.py', '_scaffold_from_openapi', 6, 7, 12).
python_function('sumd/cli.py', '_scaffold_generic', 4, 1, 3).
python_function('sumd/cli.py', 'scaffold', 4, 8, 18).
python_function('sumd/cli.py', 'map_cmd', 4, 6, 12).
python_function('sumd/cli.py', 'dsl', 4, 10, 13).
python_function('sumd/cli.py', 'cqrs_command', 4, 5, 19).
python_function('sumd/cli.py', 'nlp_command', 4, 8, 13).
python_function('sumd/cli.py', 'main', 0, 7, 3).
python_function('sumd/cli.py', 'main_sumr', 0, 3, 2).
python_function('sumd/dsl/commands.py', 'create_builtin_registry', 0, 1, 3).
python_function('sumd/dsl/commands.py', '_cmd_cat', 2, 3, 3).
python_function('sumd/dsl/commands.py', '_cmd_ls', 2, 9, 9).
python_function('sumd/dsl/commands.py', '_cmd_edit', 2, 2, 5).
python_function('sumd/dsl/commands.py', '_cmd_mkdir', 2, 2, 2).
python_function('sumd/dsl/commands.py', '_cmd_rm', 2, 4, 5).
python_function('sumd/dsl/commands.py', '_cmd_sumd_scan', 2, 6, 6).
python_function('sumd/dsl/commands.py', '_cmd_sumd_map', 2, 6, 6).
python_function('sumd/dsl/commands.py', '_cmd_sumd_validate', 2, 2, 5).
python_function('sumd/dsl/commands.py', '_cmd_sumd_info', 2, 2, 3).
python_function('sumd/dsl/commands.py', '_cmd_find', 2, 6, 9).
python_function('sumd/dsl/commands.py', '_cmd_grep', 2, 8, 11).
python_function('sumd/dsl/commands.py', '_cmd_echo', 2, 1, 1).
python_function('sumd/dsl/commands.py', '_cmd_pwd', 2, 1, 1).
python_function('sumd/dsl/commands.py', '_cmd_cd', 2, 4, 5).
python_function('sumd/dsl/commands.py', '_cmd_help', 2, 2, 2).
python_function('sumd/dsl/commands.py', '_cmd_clear', 2, 1, 1).
python_function('sumd/dsl/commands.py', '_cmd_set', 2, 3, 5).
python_function('sumd/dsl/commands.py', '_cmd_get', 2, 3, 2).
python_function('sumd/dsl/commands.py', '_cmd_unset', 2, 3, 1).
python_function('sumd/dsl/commands.py', '_cmd_vars', 2, 2, 3).
python_function('sumd/dsl/commands.py', '_cmd_exists', 2, 2, 2).
python_function('sumd/dsl/commands.py', '_cmd_read_file', 2, 3, 3).
python_function('sumd/dsl/parser.py', 'parse_dsl', 1, 1, 4).
python_function('sumd/dsl/shell.py', 'main', 0, 10, 12).
python_function('sumd/extractor.py', '_read_toml', 1, 2, 2).
python_function('sumd/extractor.py', 'extract_pyproject', 1, 3, 5).
python_function('sumd/extractor.py', '_first_task_cmd', 1, 4, 2).
python_function('sumd/extractor.py', 'extract_taskfile', 1, 6, 8).
python_function('sumd/extractor.py', '_parse_openapi_endpoints', 1, 8, 7).
python_function('sumd/extractor.py', 'extract_openapi', 1, 5, 7).
python_function('sumd/extractor.py', '_parse_doql_entities', 1, 4, 5).
python_function('sumd/extractor.py', '_parse_doql_interfaces', 1, 3, 7).
python_function('sumd/extractor.py', '_parse_doql_workflows', 1, 3, 10).
python_function('sumd/extractor.py', '_parse_doql_content', 1, 5, 14).
python_function('sumd/extractor.py', 'extract_doql', 1, 3, 3).
python_function('sumd/extractor.py', 'extract_pyqual', 1, 3, 5).
python_function('sumd/extractor.py', 'extract_python_modules', 2, 2, 4).
python_function('sumd/extractor.py', 'extract_readme_title', 1, 4, 5).
python_function('sumd/extractor.py', 'extract_requirements', 1, 7, 7).
python_function('sumd/extractor.py', 'extract_makefile', 1, 7, 9).
python_function('sumd/extractor.py', 'extract_goal', 1, 3, 7).
python_function('sumd/extractor.py', 'extract_env', 1, 8, 9).
python_function('sumd/extractor.py', '_parse_dockerfile_line', 2, 8, 6).
python_function('sumd/extractor.py', 'extract_dockerfile', 1, 5, 5).
python_function('sumd/extractor.py', 'extract_docker_compose', 1, 9, 12).
python_function('sumd/extractor.py', 'extract_package_json', 1, 3, 6).
python_function('sumd/extractor.py', '_lang_of', 1, 1, 2).
python_function('sumd/extractor.py', '_fan_out', 1, 5, 5).
python_function('sumd/extractor.py', '_cc_estimate', 1, 4, 4).
python_function('sumd/extractor.py', '_try_radon_cc', 1, 2, 1).
python_function('sumd/extractor.py', '_analyse_py_top_funcs', 2, 4, 6).
python_function('sumd/extractor.py', '_analyse_class_methods', 2, 4, 6).
python_function('sumd/extractor.py', '_analyse_py_top_classes', 2, 4, 7).
python_function('sumd/extractor.py', '_analyse_py_module', 1, 2, 6).
python_function('sumd/extractor.py', '_parse_ignore_file', 1, 6, 7).
python_function('sumd/extractor.py', '_path_matches_pattern', 2, 18, 4).
python_function('sumd/extractor.py', '_is_path_ignored', 3, 7, 3).
python_function('sumd/extractor.py', '_is_map_ignored_path', 1, 4, 1).
python_function('sumd/extractor.py', '_collect_map_files', 1, 8, 12).
python_function('sumd/extractor.py', '_render_map_detail', 2, 5, 3).
python_function('sumd/extractor.py', '_map_cc_stats', 1, 6, 8).
python_function('sumd/extractor.py', '_render_py_module_detail', 3, 5, 3).
python_function('sumd/extractor.py', 'generate_map_toon', 1, 3, 13).
python_function('sumd/extractor.py', 'generate_project_logic', 1, 20, 18).
python_function('sumd/extractor.py', '_extract_sumd_semantic_facts', 1, 14, 10).
python_function('sumd/extractor.py', 'required_tools_for_profile', 1, 1, 0).
python_function('sumd/extractor.py', 'extract_source_snippets', 2, 6, 11).
python_function('sumd/extractor.py', 'extract_swop', 1, 9, 8).
python_function('sumd/extractor.py', 'extract_project_analysis', 2, 5, 7).
python_function('sumd/mcp_server.py', '_doc_to_dict', 1, 1, 0).
python_function('sumd/mcp_server.py', '_resolve_path', 1, 2, 3).
python_function('sumd/mcp_server.py', 'list_tools', 0, 1, 2).
python_function('sumd/mcp_server.py', '_tool_parse_sumd', 1, 1, 5).
python_function('sumd/mcp_server.py', '_tool_validate_sumd', 1, 1, 7).
python_function('sumd/mcp_server.py', '_tool_export_sumd', 1, 5, 8).
python_function('sumd/mcp_server.py', '_tool_list_sections', 1, 1, 4).
python_function('sumd/mcp_server.py', '_tool_get_section', 1, 3, 6).
python_function('sumd/mcp_server.py', '_tool_info_sumd', 1, 1, 5).
python_function('sumd/mcp_server.py', '_tool_generate_sumd', 1, 5, 5).
python_function('sumd/mcp_server.py', '_tool_execute_command', 1, 3, 6).
python_function('sumd/mcp_server.py', '_tool_execute_query', 1, 3, 5).
python_function('sumd/mcp_server.py', '_tool_get_events', 1, 2, 6).
python_function('sumd/mcp_server.py', '_tool_get_aggregate', 1, 3, 4).
python_function('sumd/mcp_server.py', '_tool_execute_dsl', 1, 3, 5).
python_function('sumd/mcp_server.py', '_tool_dsl_shell_info', 1, 2, 3).
python_function('sumd/mcp_server.py', 'call_tool', 2, 3, 4).
python_function('sumd/mcp_server.py', 'main', 0, 2, 3).
python_function('sumd/parser.py', 'parse', 1, 1, 2).
python_function('sumd/parser.py', 'parse_file', 1, 1, 2).
python_function('sumd/parser.py', 'validate', 1, 1, 2).
python_function('sumd/pipeline.py', '_refresh_map_toon', 1, 5, 4).
python_function('sumd/pipeline.py', '_find_tools_bin_dir', 1, 3, 1).
python_function('sumd/pipeline.py', '_run_tool_if_present', 4, 3, 3).
python_function('sumd/pipeline.py', '_refresh_analysis_files', 2, 7, 5).
python_function('sumd/pipeline.py', '_collect_tool_sources', 5, 6, 3).
python_function('sumd/pipeline.py', '_doql_sources', 1, 4, 1).
python_function('sumd/pipeline.py', '_collect_pkg_sources', 10, 5, 6).
python_function('sumd/pipeline.py', '_collect_infra_sources', 5, 6, 3).
python_function('sumd/pipeline.py', '_collect_sources', 16, 2, 4).
python_function('sumd/pipeline.py', '_inject_toc', 1, 3, 6).
python_function('sumd/prolog_engine.py', 'is_variable', 1, 6, 4).
python_function('sumd/prolog_engine.py', 'to_term', 1, 10, 14).
python_function('sumd/prolog_engine.py', '_split_body_terms', 1, 11, 3).
python_function('sumd/prolog_engine.py', 'unify', 3, 10, 7).
python_function('sumd/prolog_engine.py', 'resolve_val', 2, 3, 1).
python_function('sumd/prolog_engine.py', 'deep_resolve', 2, 2, 4).
python_function('sumd/prolog_engine.py', 'extend_subst', 3, 2, 2).
python_function('sumd/prolog_engine.py', 'occurs_check', 3, 3, 4).
python_function('sumd/prolog_engine.py', 'rename_variables', 2, 4, 5).
python_function('sumd/renderer.py', 'generate_sumd_content', 4, 1, 2).
python_function('sumd/sections/api_stubs.py', '_render_api_stubs', 1, 8, 9).
python_function('sumd/sections/architecture.py', '_render_architecture_doql_section', 4, 4, 8).
python_function('sumd/sections/architecture.py', '_render_architecture_modules', 3, 2, 1).
python_function('sumd/sections/architecture.py', '_render_doql_app', 2, 3, 3).
python_function('sumd/sections/architecture.py', '_render_doql_entities', 2, 4, 4).
python_function('sumd/sections/architecture.py', '_render_doql_interfaces', 2, 3, 5).
python_function('sumd/sections/architecture.py', '_render_doql_integrations', 2, 3, 5).
python_function('sumd/sections/architecture.py', '_render_architecture_doql_parsed', 2, 1, 4).
python_function('sumd/sections/architecture.py', '_render_architecture_rules', 2, 3, 4).
python_function('sumd/sections/architecture.py', '_render_architecture', 5, 6, 5).
python_function('sumd/sections/call_graph.py', '_parse_calls_header', 1, 6, 5).
python_function('sumd/sections/call_graph.py', '_parse_hub_stat_line', 1, 2, 3).
python_function('sumd/sections/call_graph.py', '_process_in_hubs_line', 3, 6, 5).
python_function('sumd/sections/call_graph.py', '_parse_calls_hubs', 1, 8, 3).
python_function('sumd/sections/call_graph.py', '_parse_calls_toon', 1, 1, 3).
python_function('sumd/sections/call_graph.py', '_render_call_graph', 1, 4, 8).
python_function('sumd/sections/code_analysis.py', '_render_code_analysis', 2, 6, 4).
python_function('sumd/sections/configuration.py', '_render_configuration_section', 2, 1, 0).
python_function('sumd/sections/dependencies.py', '_render_deps_runtime', 3, 6, 2).
python_function('sumd/sections/dependencies.py', '_render_deps_dev', 3, 6, 2).
python_function('sumd/sections/dependencies.py', '_render_dependencies', 3, 2, 4).
python_function('sumd/sections/deployment.py', '_render_deployment_install', 3, 2, 2).
python_function('sumd/sections/deployment.py', '_render_deployment_reqs', 2, 5, 2).
python_function('sumd/sections/deployment.py', '_render_dockerfile_info', 2, 5, 3).
python_function('sumd/sections/deployment.py', '_render_deployment_docker', 3, 4, 4).
python_function('sumd/sections/deployment.py', '_render_deployment', 5, 1, 4).
python_function('sumd/sections/environment.py', '_render_env_section', 1, 3, 2).
python_function('sumd/sections/environment.py', '_render_goal_section', 1, 7, 3).
python_function('sumd/sections/extras.py', '_render_makefile_targets', 2, 2, 1).
python_function('sumd/sections/extras.py', '_render_pkg_json_scripts', 2, 6, 4).
python_function('sumd/sections/extras.py', '_render_extras', 2, 3, 3).
python_function('sumd/sections/interfaces.py', '_render_interfaces_openapi', 4, 5, 7).
python_function('sumd/sections/interfaces.py', '_render_testql_raw', 3, 4, 7).
python_function('sumd/sections/interfaces.py', '_render_testql_endpoint', 2, 1, 2).
python_function('sumd/sections/interfaces.py', '_render_testql_extras', 2, 6, 3).
python_function('sumd/sections/interfaces.py', '_render_testql_one_structured', 2, 7, 4).
python_function('sumd/sections/interfaces.py', '_render_interfaces_testql', 4, 3, 3).
python_function('sumd/sections/interfaces.py', '_render_interfaces', 5, 5, 4).
python_function('sumd/sections/quality.py', '_render_quality_raw', 2, 2, 4).
python_function('sumd/sections/quality.py', '_render_quality_parsed', 2, 8, 3).
python_function('sumd/sections/quality.py', '_render_quality', 3, 3, 3).
python_function('sumd/sections/source_snippets.py', '_render_source_snippets', 2, 6, 4).
python_function('sumd/sections/swop.py', '_render_swop_section', 2, 9, 5).
python_function('sumd/sections/test_contracts.py', '_render_scenario_contract', 2, 8, 2).
python_function('sumd/sections/test_contracts.py', '_render_test_contracts', 1, 5, 9).
python_function('sumd/sections/utils/render.py', 'call_with_ctx', 1, 1, 2).
python_function('sumd/sections/utils/should_render.py', 'always', 2, 1, 0).
python_function('sumd/sections/utils/should_render.py', 'has_attr', 1, 1, 2).
python_function('sumd/sections/workflows.py', '_render_workflows_doql', 2, 2, 3).
python_function('sumd/sections/workflows.py', '_render_workflows_taskfile', 4, 6, 4).
python_function('sumd/sections/workflows.py', '_render_workflows', 4, 4, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_config', 1, 9, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_api', 1, 6, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_assert', 1, 7, 5).
python_function('sumd/toon_parser.py', '_parse_toon_block_performance', 1, 7, 5).
python_function('sumd/toon_parser.py', '_parse_toon_block_navigate', 1, 7, 4).
python_function('sumd/toon_parser.py', '_parse_toon_block_gui', 1, 7, 5).
python_function('sumd/toon_parser.py', '_parse_toon_file', 1, 4, 13).
python_function('sumd/toon_parser.py', 'extract_testql_scenarios', 1, 7, 8).
python_function('sumd/validator.py', '_validate_yaml_body', 2, 2, 1).
python_function('sumd/validator.py', '_validate_less_css_body', 2, 2, 1).
python_function('sumd/validator.py', '_validate_mermaid_body', 2, 2, 4).
python_function('sumd/validator.py', '_validate_toon_body', 2, 2, 1).
python_function('sumd/validator.py', '_validate_bash_body', 2, 4, 1).
python_function('sumd/validator.py', '_validate_deps_body', 2, 5, 6).
python_function('sumd/validator.py', '_validate_markpact_meta', 5, 5, 6).
python_function('sumd/validator.py', 'validate_codeblocks', 2, 9, 11).
python_function('sumd/validator.py', '_check_h1', 2, 2, 2).
python_function('sumd/validator.py', '_check_required_sections', 3, 1, 6).
python_function('sumd/validator.py', '_check_metadata_fields', 2, 7, 6).
python_function('sumd/validator.py', '_check_unclosed_fences', 2, 2, 2).
python_function('sumd/validator.py', '_check_empty_links', 2, 1, 1).
python_function('sumd/validator.py', 'validate_markdown', 3, 1, 6).
python_function('sumd/validator.py', 'validate_project_architecture', 1, 8, 11).
python_function('sumd/validator.py', 'validate_sumd_file', 2, 3, 8).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'get_engine', 0, 4, 6).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'main', 0, 1, 1).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'info', 0, 1, 3).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'query', 1, 5, 11).
python_function('sumd_logic_validator/sumd_logic_validator/cli.py', 'shell', 0, 9, 11).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'is_variable', 1, 6, 3).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'to_term', 1, 10, 15).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', '_split_body_terms', 1, 12, 4).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'unify', 3, 10, 7).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'resolve_val', 2, 3, 1).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'deep_resolve', 2, 2, 4).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'extend_subst', 3, 2, 2).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'occurs_check', 3, 3, 4).
python_function('sumd_logic_validator/sumd_logic_validator/engine.py', 'rename_variables', 2, 4, 5).
python_function('sumd_logic_validator/tests/test_engine.py', 'rules_path', 1, 1, 1).
python_function('sumd_logic_validator/tests/test_engine.py', 'test_pure_python_parser', 1, 1, 4).
python_function('sumd_logic_validator/tests/test_engine.py', 'test_pure_python_queries', 1, 1, 6).
python_function('sumd_logic_validator/tests/test_engine.py', 'test_hybrid_engine_fallback', 1, 1, 3).
python_function('tests/test_architectural_logic.py', 'test_pure_python_prolog_basic', 0, 1, 6).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_missing_file', 1, 2, 5).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_aligned', 1, 1, 3).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_missing_automation', 1, 2, 5).
python_function('tests/test_architectural_logic.py', 'test_architectural_validation_missing_gate', 1, 2, 5).
python_function('tests/test_cli.py', 'sumd_file', 1, 1, 1).
python_function('tests/test_dogfood.py', '_run', 3, 1, 1).
python_function('tests/test_dogfood.py', 'project_copy', 1, 1, 5).
python_function('tests/test_dogfood.py', 'test_sumd_scans_itself', 1, 1, 5).
python_function('tests/test_dogfood.py', 'test_sumd_scans_all_profiles', 2, 1, 4).
python_function('tests/test_dogfood.py', 'test_sumr_generates_sumr_md', 1, 2, 5).
python_function('tests/test_dogfood.py', 'test_sumd_lint_passes_on_generated_output', 1, 1, 3).
python_function('tests/test_dogfood.py', 'test_sumd_version_flag', 0, 1, 4).
python_function('tests/test_dogfood.py', 'test_sumd_scan_produces_no_unhandled_exceptions', 1, 1, 2).
python_function('tests/test_mcp_server.py', 'sumd_file', 1, 1, 1).
python_function('tests/test_mcp_server.py', 'run', 1, 1, 2).
python_function('tests/test_parser.py', 'test_parse_basic', 0, 1, 2).
python_function('tests/test_parser.py', 'test_parse_sections', 0, 1, 1).
python_function('tests/test_parser.py', 'test_validate_valid_document', 0, 1, 3).
python_function('tests/test_parser.py', 'test_validate_missing_intent', 0, 1, 4).
python_function('tests/test_parser.py', 'test_parse_file', 1, 1, 2).
python_function('tests/test_parser.py', 'test_parser_class', 0, 1, 3).
python_function('tests/test_parser.py', 'test_markpact_semantic_kinds_valid', 0, 2, 2).
python_function('tests/test_parser.py', 'test_markpact_unknown_kind_error', 0, 2, 2).
python_function('tests/test_parser.py', 'test_markpact_missing_path_error', 0, 2, 2).
python_function('tests/test_pipeline.py', 'proj_dir', 1, 1, 1).
python_function('tests/test_pipeline.py', 'test_pipeline_run_returns_string', 1, 1, 4).
python_function('tests/test_pipeline.py', 'test_pipeline_output_has_h1', 1, 2, 4).
python_function('tests/test_pipeline.py', 'test_pipeline_output_has_metadata', 1, 1, 2).
python_function('tests/test_pipeline.py', 'test_pipeline_return_sources', 1, 1, 3).
python_function('tests/test_pipeline.py', 'test_pipeline_profile_minimal', 1, 1, 2).
python_function('tests/test_pipeline.py', 'test_pipeline_profile_refactor', 1, 1, 2).
python_function('tests/test_pipeline.py', 'test_pipeline_with_modules', 1, 1, 4).
python_function('tests/test_pipeline.py', 'test_pipeline_with_taskfile', 1, 1, 3).
python_function('tests/test_pipeline.py', 'test_pipeline_with_dependencies', 1, 1, 3).
python_function('tests/test_pipeline.py', 'test_pipeline_injects_toc', 1, 1, 2).
python_function('tests/test_pipeline.py', 'test_required_tools_rich', 0, 1, 1).
python_function('tests/test_pipeline.py', 'test_required_tools_refactor', 0, 1, 1).
python_function('tests/test_pipeline.py', 'test_required_tools_minimal', 0, 1, 1).
python_function('tests/test_pipeline.py', 'test_refresh_map_toon_writes_file', 1, 1, 2).
python_function('tests/test_pipeline.py', 'test_refresh_analysis_files_noop_without_tools', 1, 1, 1).
python_function('tests/test_sections.py', 'make_ctx', 0, 1, 4).
python_function('tests/test_statement.py', 'test_placeholder', 0, 1, 0).
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
python_method('Repository', 'get_by_id', 1, 1, 0).
python_method('Repository', 'save', 1, 1, 0).
python_method('Repository', 'delete', 1, 1, 0).
python_class('sumd/cqrs/aggregates.py', 'EventSourcedRepository').
python_method('EventSourcedRepository', '__init__', 2, 1, 0).
python_method('EventSourcedRepository', 'get_by_id', 1, 3, 4).
python_method('EventSourcedRepository', 'save', 1, 1, 2).
python_method('EventSourcedRepository', 'delete', 1, 2, 0).
python_method('EventSourcedRepository', 'clear_cache', 0, 1, 1).
python_class('sumd/cqrs/commands.py', 'Command').
python_class('sumd/cqrs/commands.py', 'CommandHandler').
python_method('CommandHandler', 'handle', 1, 1, 0).
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
python_method('SumdCommandHandler', 'handle', 1, 7, 10).
python_class('sumd/cqrs/events.py', 'Event').
python_method('Event', 'to_dict', 0, 1, 1).
python_method('Event', 'from_dict', 2, 1, 2).
python_class('sumd/cqrs/events.py', 'EventStore').
python_method('EventStore', '__init__', 1, 2, 1).
python_method('EventStore', 'save_event', 1, 5, 4).
python_method('EventStore', 'get_events', 2, 1, 1).
python_method('EventStore', 'get_all_events', 0, 2, 3).
python_method('EventStore', '_persist_event', 1, 3, 5).
python_method('EventStore', '_load_events', 0, 8, 7).
python_class('sumd/cqrs/events.py', 'SumdDocumentCreated').
python_class('sumd/cqrs/events.py', 'SumdDocumentUpdated').
python_class('sumd/cqrs/events.py', 'SumdSectionAdded').
python_class('sumd/cqrs/events.py', 'SumdSectionRemoved').
python_class('sumd/cqrs/events.py', 'SumdDocumentValidated').
python_class('sumd/cqrs/events.py', 'SumdCommandExecuted').
python_class('sumd/cqrs/queries.py', 'Query').
python_class('sumd/cqrs/queries.py', 'QueryHandler').
python_method('QueryHandler', 'handle', 1, 1, 0).
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
python_method('SumdQueryHandler', '_handle_get_sumd_document', 1, 2, 4).
python_method('SumdQueryHandler', '_handle_list_sumd_sections', 1, 2, 4).
python_method('SumdQueryHandler', '_handle_get_sumd_section', 1, 4, 5).
python_method('SumdQueryHandler', '_handle_get_project_info', 1, 3, 5).
python_method('SumdQueryHandler', '_handle_get_event_history', 1, 2, 4).
python_method('SumdQueryHandler', '_handle_get_all_events', 1, 2, 5).
python_method('SumdQueryHandler', '_handle_search_documents', 1, 6, 11).
python_method('SumdQueryHandler', '_handle_get_validation_results', 1, 2, 4).
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
python_method('SumdAggregate', '_when_section_added', 1, 1, 4).
python_method('SumdAggregate', '_when_section_removed', 1, 1, 2).
python_method('SumdAggregate', '_when_document_validated', 1, 1, 1).
python_method('SumdAggregate', 'create_document', 4, 2, 3).
python_method('SumdAggregate', 'update_document', 1, 2, 3).
python_method('SumdAggregate', 'add_section', 5, 3, 3).
python_method('SumdAggregate', 'remove_section', 1, 3, 5).
python_method('SumdAggregate', 'validate_document', 2, 2, 3).
python_method('SumdAggregate', 'get_section', 1, 3, 1).
python_method('SumdAggregate', 'has_section', 1, 1, 1).
python_method('SumdAggregate', 'get_state', 0, 1, 5).
python_method('SumdAggregate', 'create_from_file', 2, 6, 10).
python_class('sumd/dsl/commands.py', 'DSLCommand').
python_method('DSLCommand', '__post_init__', 0, 2, 0).
python_class('sumd/dsl/commands.py', 'DSLCommandRegistry').
python_method('DSLCommandRegistry', '__init__', 0, 1, 0).
python_method('DSLCommandRegistry', 'register', 1, 4, 1).
python_method('DSLCommandRegistry', 'get_command', 1, 1, 1).
python_method('DSLCommandRegistry', 'list_commands', 1, 4, 3).
python_method('DSLCommandRegistry', 'list_categories', 0, 1, 2).
python_method('DSLCommandRegistry', 'get_help', 1, 6, 4).
python_class('sumd/dsl/engine.py', 'DSLContext').
python_method('DSLContext', '__init__', 1, 2, 1).
python_method('DSLContext', 'set_variable', 2, 1, 0).
python_method('DSLContext', 'get_variable', 1, 1, 1).
python_method('DSLContext', 'register_function', 2, 1, 0).
python_method('DSLContext', 'get_function', 1, 1, 1).
python_class('sumd/dsl/engine.py', 'DSLEngine').
python_method('DSLEngine', '__init__', 3, 2, 4).
python_method('DSLEngine', 'execute', 2, 1, 1).
python_method('DSLEngine', 'execute_text', 2, 3, 5).
python_method('DSLEngine', '_is_natural_language', 1, 3, 4).
python_method('DSLEngine', 'process_natural_language', 1, 1, 1).
python_method('DSLEngine', 'get_suggestions', 1, 1, 1).
python_method('DSLEngine', '_execute_expression', 2, 15, 13).
python_method('DSLEngine', '_execute_assignment', 2, 3, 4).
python_method('DSLEngine', '_execute_command', 2, 9, 9).
python_method('DSLEngine', '_execute_function_call', 2, 7, 8).
python_method('DSLEngine', '_execute_property_access', 2, 5, 5).
python_method('DSLEngine', '_execute_comparison', 2, 12, 8).
python_method('DSLEngine', '_execute_logical', 2, 9, 3).
python_method('DSLEngine', '_execute_arithmetic', 2, 10, 3).
python_method('DSLEngine', '_execute_pipeline', 2, 6, 4).
python_method('DSLEngine', '_execute_list', 2, 2, 2).
python_method('DSLEngine', '_execute_dict', 2, 2, 3).
python_method('DSLEngine', '_execute_block', 2, 2, 1).
python_method('DSLEngine', '_execute_sumd_command', 3, 4, 6).
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
python_method('DSLEngine', '_builtin_list_files', 2, 1, 4).
python_method('DSLEngine', '_builtin_cwd', 1, 1, 1).
python_method('DSLEngine', '_builtin_cd', 2, 2, 3).
python_method('DSLEngine', '_builtin_help', 1, 1, 1).
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
python_method('SimpleNLPModel', 'predict_intent', 1, 3, 4).
python_method('SimpleNLPModel', 'extract_entities', 2, 4, 1).
python_class('sumd/dsl/parser.py', 'DSLTokenType').
python_class('sumd/dsl/parser.py', 'DSLToken').
python_class('sumd/dsl/parser.py', 'DSLLexer').
python_method('DSLLexer', '__init__', 1, 1, 0).
python_method('DSLLexer', 'tokenize', 0, 7, 8).
python_class('sumd/dsl/parser.py', 'DSLExpressionType').
python_class('sumd/dsl/parser.py', 'DSLExpression').
python_method('DSLExpression', '__str__', 0, 8, 2).
python_class('sumd/dsl/parser.py', 'DSLParser').
python_method('DSLParser', '__init__', 1, 1, 0).
python_method('DSLParser', 'parse', 0, 6, 7).
python_method('DSLParser', '_parse_statement', 0, 23, 10).
python_method('DSLParser', '_parse_pipeline', 0, 2, 4).
python_method('DSLParser', '_parse_assignment', 0, 3, 5).
python_method('DSLParser', '_parse_logical_or', 0, 2, 4).
python_method('DSLParser', '_parse_logical_and', 0, 2, 4).
python_method('DSLParser', '_parse_comparison', 0, 2, 4).
python_method('DSLParser', '_parse_arithmetic', 0, 3, 4).
python_method('DSLParser', '_parse_term', 0, 4, 4).
python_method('DSLParser', '_parse_factor', 0, 3, 5).
python_method('DSLParser', '_parse_primary', 0, 22, 18).
python_method('DSLParser', '_parse_command', 0, 6, 6).
python_method('DSLParser', '_parse_function_call', 0, 3, 7).
python_method('DSLParser', '_parse_property_access', 0, 1, 2).
python_method('DSLParser', '_parse_list', 0, 3, 6).
python_method('DSLParser', '_parse_dict', 0, 3, 7).
python_method('DSLParser', '_is_at_end', 0, 1, 1).
python_method('DSLParser', '_peek', 0, 1, 0).
python_method('DSLParser', '_previous', 0, 1, 0).
python_method('DSLParser', '_advance', 0, 2, 2).
python_method('DSLParser', '_check', 2, 5, 2).
python_method('DSLParser', '_check_next', 2, 5, 1).
python_method('DSLParser', '_match', 2, 2, 2).
python_method('DSLParser', '_consume', 2, 2, 4).
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
python_method('DSLContext', 'set_variable', 2, 1, 0).
python_method('DSLContext', 'get_variable', 1, 1, 1).
python_method('DSLContext', 'register_function', 2, 1, 0).
python_class('sumd/dsl/schema.py', 'DSLCommandResult').
python_class('sumd/dsl/schema_commands.py', 'SchemaCommandRegistry').
python_method('SchemaCommandRegistry', '__init__', 1, 1, 2).
python_method('SchemaCommandRegistry', '_register_commands', 0, 3, 0).
python_method('SchemaCommandRegistry', 'get_command', 1, 3, 0).
python_method('SchemaCommandRegistry', 'list_commands', 1, 2, 2).
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
python_method('SchemaBasedCommands', '_cmd_sumd_info', 1, 2, 2).
python_method('SchemaBasedCommands', '_cmd_cat', 1, 2, 2).
python_method('SchemaBasedCommands', '_cmd_ls', 1, 2, 5).
python_method('SchemaBasedCommands', '_cmd_edit', 1, 2, 3).
python_method('SchemaBasedCommands', '_cmd_find', 1, 2, 6).
python_method('SchemaBasedCommands', '_cmd_grep', 1, 7, 8).
python_method('SchemaBasedCommands', '_cmd_echo', 1, 1, 1).
python_method('SchemaBasedCommands', '_cmd_pwd', 1, 1, 1).
python_method('SchemaBasedCommands', '_cmd_cd', 1, 2, 4).
python_method('SchemaBasedCommands', '_cmd_ask', 1, 5, 3).
python_method('SchemaBasedCommands', '_cmd_summarize', 1, 2, 2).
python_method('SchemaBasedCommands', '_cmd_analyze_sentiment', 1, 3, 6).
python_method('SchemaBasedCommands', '_cmd_schema_info', 1, 1, 1).
python_method('SchemaBasedCommands', '_cmd_list_commands', 1, 3, 5).
python_method('SchemaBasedCommands', '_cmd_command_help', 1, 3, 2).
python_class('sumd/dsl/shell.py', 'DSLShell').
python_method('DSLShell', '__init__', 3, 4, 6).
python_method('DSLShell', '_setup_readline', 0, 3, 6).
python_method('DSLShell', '_completer', 2, 10, 5).
python_method('DSLShell', '_register_commands', 0, 3, 2).
python_method('DSLShell', 'run', 0, 9, 8).
python_method('DSLShell', '_get_prompt', 0, 1, 0).
python_method('DSLShell', '_handle_shell_command', 1, 13, 8).
python_method('DSLShell', '_execute_line', 1, 9, 6).
python_method('DSLShell', 'execute_script', 1, 9, 12).
python_method('DSLShell', 'execute_command', 1, 2, 3).
python_class('sumd/dsl/shell.py', 'DSLShellServer').
python_method('DSLShellServer', '__init__', 1, 2, 2).
python_method('DSLShellServer', 'execute_dsl', 2, 4, 5).
python_method('DSLShellServer', 'get_shell_info', 0, 1, 4).
python_class('sumd/models.py', 'SectionType').
python_class('sumd/models.py', 'Section').
python_class('sumd/models.py', 'SUMDDocument').
python_class('sumd/parser.py', 'SUMDParser').
python_method('SUMDParser', '__init__', 0, 1, 0).
python_method('SUMDParser', 'parse', 1, 1, 4).
python_method('SUMDParser', 'parse_file', 1, 1, 2).
python_method('SUMDParser', '_parse_header', 1, 9, 7).
python_method('SUMDParser', '_parse_sections', 1, 6, 7).
python_method('SUMDParser', 'validate', 1, 5, 1).
python_class('sumd/pipeline.py', 'RenderPipeline').
python_method('RenderPipeline', '__init__', 2, 1, 1).
python_method('RenderPipeline', '_collect', 0, 3, 23).
python_method('RenderPipeline', '_build_registered_sections', 2, 4, 6).
python_method('RenderPipeline', '_render_legacy_sections', 1, 1, 0).
python_method('RenderPipeline', '_assemble', 2, 4, 5).
python_method('RenderPipeline', 'run', 2, 2, 3).
python_class('sumd/prolog_engine.py', 'Variable').
python_method('Variable', '__init__', 1, 1, 0).
python_method('Variable', '__repr__', 0, 1, 0).
python_method('Variable', '__eq__', 1, 2, 1).
python_method('Variable', '__hash__', 0, 1, 1).
python_class('sumd/prolog_engine.py', 'Term').
python_method('Term', '__init__', 1, 1, 1).
python_method('Term', '__repr__', 0, 2, 2).
python_method('Term', '__eq__', 1, 3, 1).
python_class('sumd/prolog_engine.py', 'Rule').
python_method('Rule', '__init__', 2, 2, 0).
python_method('Rule', '__repr__', 0, 2, 2).
python_class('sumd/prolog_engine.py', 'PythonPrologDB').
python_method('PythonPrologDB', '__init__', 0, 1, 0).
python_method('PythonPrologDB', 'add_fact', 1, 1, 4).
python_method('PythonPrologDB', 'add_rule', 2, 1, 2).
python_method('PythonPrologDB', 'parse_and_load', 1, 4, 8).
python_class('sumd/prolog_engine.py', 'PythonPrologEngine').
python_method('PythonPrologEngine', '__init__', 1, 1, 0).
python_method('PythonPrologEngine', 'query', 1, 5, 7).
python_method('PythonPrologEngine', '_find_vars', 1, 4, 5).
python_method('PythonPrologEngine', '_resolve', 2, 10, 7).
python_class('sumd/prolog_engine.py', 'HybridPrologEngine').
python_method('HybridPrologEngine', '__init__', 1, 2, 8).
python_method('HybridPrologEngine', 'query', 1, 5, 6).
python_method('HybridPrologEngine', '_query_pyswip', 1, 4, 8).
python_method('HybridPrologEngine', '_query_subprocess', 1, 9, 10).
python_method('HybridPrologEngine', '_query_python', 1, 1, 1).
python_method('HybridPrologEngine', '_swipl_executable_exists', 0, 2, 1).
python_class('sumd/sections/api_stubs.py', 'ApiStubsSection').
python_method('ApiStubsSection', 'should_render', 1, 1, 2).
python_class('sumd/sections/architecture.py', 'ArchitectureSection').
python_class('sumd/sections/base.py', 'RenderContext').
python_class('sumd/sections/base.py', 'Section').
python_method('Section', 'should_render', 1, 1, 0).
python_method('Section', 'render', 1, 1, 0).
python_class('sumd/sections/call_graph.py', 'CallGraphSection').
python_method('CallGraphSection', 'should_render', 1, 1, 2).
python_class('sumd/sections/code_analysis.py', 'CodeAnalysisSection').
python_method('CodeAnalysisSection', 'should_render', 1, 1, 2).
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
python_class('sumd/validator.py', 'CodeBlockIssue').
python_class('sumd_logic_validator/sumd_logic_validator/engine.py', 'Variable').
python_method('Variable', '__init__', 1, 1, 0).
python_method('Variable', '__repr__', 0, 1, 0).
python_method('Variable', '__eq__', 1, 2, 1).
python_method('Variable', '__hash__', 0, 1, 1).
python_class('sumd_logic_validator/sumd_logic_validator/engine.py', 'Term').
python_method('Term', '__init__', 1, 1, 1).
python_method('Term', '__repr__', 0, 2, 2).
python_method('Term', '__eq__', 1, 3, 1).
python_class('sumd_logic_validator/sumd_logic_validator/engine.py', 'Rule').
python_method('Rule', '__init__', 2, 2, 0).
python_method('Rule', '__repr__', 0, 2, 2).
python_class('sumd_logic_validator/sumd_logic_validator/engine.py', 'PythonPrologDB').
python_method('PythonPrologDB', '__init__', 0, 1, 0).
python_method('PythonPrologDB', 'add_fact', 1, 1, 4).
python_method('PythonPrologDB', 'add_rule', 2, 1, 2).
python_method('PythonPrologDB', 'parse_and_load', 1, 3, 8).
python_class('sumd_logic_validator/sumd_logic_validator/engine.py', 'PythonPrologEngine').
python_method('PythonPrologEngine', '__init__', 1, 1, 0).
python_method('PythonPrologEngine', 'query', 1, 5, 7).
python_method('PythonPrologEngine', '_find_vars', 1, 4, 5).
python_method('PythonPrologEngine', '_resolve', 2, 10, 7).
python_class('sumd_logic_validator/sumd_logic_validator/engine.py', 'HybridPrologEngine').
python_method('HybridPrologEngine', '__init__', 1, 2, 8).
python_method('HybridPrologEngine', 'query', 1, 5, 6).
python_method('HybridPrologEngine', '_query_pyswip', 1, 4, 8).
python_method('HybridPrologEngine', '_query_subprocess', 1, 9, 10).
python_method('HybridPrologEngine', '_query_python', 1, 1, 1).
python_method('HybridPrologEngine', '_swipl_executable_exists', 0, 2, 1).
python_class('tests/test_cli.py', 'TestValidateCommand').
python_method('TestValidateCommand', 'test_valid_file_exits_zero', 1, 1, 3).
python_method('TestValidateCommand', 'test_valid_file_prints_ok', 1, 2, 4).
python_method('TestValidateCommand', 'test_missing_file_exits_nonzero', 1, 1, 3).
python_class('tests/test_cli.py', 'TestInfoCommand').
python_method('TestInfoCommand', 'test_info_runs', 1, 1, 3).
python_class('tests/test_cli.py', 'TestExportCommand').
python_method('TestExportCommand', 'test_export_json', 1, 2, 6).
python_method('TestExportCommand', 'test_export_to_output_file', 2, 1, 4).
python_method('TestExportCommand', 'test_export_markdown', 1, 1, 3).
python_class('tests/test_cli.py', 'TestCliVersion').
python_method('TestCliVersion', 'test_version_option', 0, 1, 2).
python_class('tests/test_cli.py', 'TestCliHelp').
python_method('TestCliHelp', 'test_help', 0, 2, 3).
python_method('TestCliHelp', 'test_validate_help', 0, 1, 2).
python_method('TestCliHelp', 'test_export_help', 0, 1, 2).
python_method('TestCliHelp', 'test_scan_help', 0, 1, 2).
python_class('tests/test_cli.py', 'TestProjectDetection').
python_method('TestProjectDetection', 'test_is_project_dir_accepts_language_marker', 3, 1, 4).
python_method('TestProjectDetection', 'test_is_project_dir_accepts_glob_markers', 3, 1, 4).
python_method('TestProjectDetection', 'test_empty_dir_is_not_project', 1, 1, 2).
python_method('TestProjectDetection', 'test_detect_projects_finds_mixed_languages', 1, 1, 3).
python_method('TestProjectDetection', 'test_detect_projects_non_recursive_skips_nested', 1, 1, 3).
python_method('TestProjectDetection', 'test_detect_projects_recursive_finds_nested', 1, 1, 3).
python_class('tests/test_cli.py', 'TestNodeSpecFromPackageJson').
python_method('TestNodeSpecFromPackageJson', 'test_framework_detection', 2, 1, 3).
python_method('TestNodeSpecFromPackageJson', 'test_spec_uses_real_scripts_and_extras', 0, 1, 1).
python_method('TestNodeSpecFromPackageJson', 'test_spec_falls_back_without_scripts', 0, 1, 1).
python_class('tests/test_cli.py', 'TestGenerateDoqlLess').
python_method('TestGenerateDoqlLess', '_pkg', 1, 1, 3).
python_method('TestGenerateDoqlLess', 'test_fresh_generation_for_node_uses_real_scripts', 1, 1, 4).
python_method('TestGenerateDoqlLess', 'test_force_regenerates_autogen_file_without_duplicating', 1, 1, 4).
python_method('TestGenerateDoqlLess', 'test_force_preserves_user_authored_file', 1, 1, 5).
python_method('TestGenerateDoqlLess', 'test_no_force_skips_existing', 1, 1, 4).
python_class('tests/test_cqrs_es.py', 'TestEventStore').
python_method('TestEventStore', 'test_save_and_get_events', 0, 2, 7).
python_method('TestEventStore', 'test_persistence', 0, 2, 7).
python_method('TestEventStore', 'test_get_events_from_version', 0, 3, 8).
python_class('tests/test_cqrs_es.py', 'TestSumdAggregate').
python_method('TestSumdAggregate', 'test_create_document', 0, 1, 4).
python_method('TestSumdAggregate', 'test_add_section', 0, 1, 5).
python_method('TestSumdAggregate', 'test_remove_section', 0, 1, 6).
python_method('TestSumdAggregate', 'test_load_from_history', 0, 3, 11).
python_class('tests/test_cqrs_es.py', 'TestCommandBus').
python_method('TestCommandBus', 'test_dispatch_command', 0, 2, 10).
python_class('tests/test_cqrs_es.py', 'TestQueryBus').
python_method('TestQueryBus', 'test_dispatch_query', 0, 2, 11).
python_class('tests/test_cqrs_es.py', 'TestEventSourcedRepository').
python_method('TestEventSourcedRepository', 'test_save_and_get_aggregate', 0, 2, 8).
python_class('tests/test_cqrs_es.py', 'TestIntegration').
python_method('TestIntegration', 'test_full_workflow', 0, 2, 18).
python_class('tests/test_dsl.py', 'TestDSLLexer').
python_method('TestDSLLexer', 'test_tokenize_simple_command', 0, 1, 3).
python_method('TestDSLLexer', 'test_tokenize_function_call', 0, 1, 3).
python_method('TestDSLLexer', 'test_tokenize_arithmetic', 0, 1, 3).
python_method('TestDSLLexer', 'test_tokenize_string_literals', 0, 1, 3).
python_method('TestDSLLexer', 'test_tokenize_comments', 0, 1, 3).
python_class('tests/test_dsl.py', 'TestDSLParser').
python_method('TestDSLParser', 'test_parse_simple_command', 0, 1, 2).
python_method('TestDSLParser', 'test_parse_function_call', 0, 1, 2).
python_method('TestDSLParser', 'test_parse_arithmetic', 0, 1, 2).
python_method('TestDSLParser', 'test_parse_assignment', 0, 1, 2).
python_method('TestDSLParser', 'test_parse_pipeline', 0, 1, 2).
python_method('TestDSLParser', 'test_parse_comparison', 0, 1, 2).
python_method('TestDSLParser', 'test_parse_logical', 0, 1, 2).
python_class('tests/test_dsl.py', 'TestDSLEngine').
python_method('TestDSLEngine', 'test_execute_literal', 0, 1, 4).
python_method('TestDSLEngine', 'test_execute_arithmetic', 0, 1, 4).
python_method('TestDSLEngine', 'test_execute_comparison', 0, 1, 4).
python_method('TestDSLEngine', 'test_execute_logical', 0, 1, 4).
python_method('TestDSLEngine', 'test_execute_assignment', 0, 1, 5).
python_method('TestDSLEngine', 'test_execute_function_call', 0, 1, 4).
python_method('TestDSLEngine', 'test_execute_pipeline', 0, 1, 5).
python_class('tests/test_dsl.py', 'TestDSLCommandRegistry').
python_method('TestDSLCommandRegistry', 'test_builtin_registry', 0, 1, 4).
python_method('TestDSLCommandRegistry', 'test_command_categories', 0, 1, 4).
python_method('TestDSLCommandRegistry', 'test_help_system', 0, 1, 2).
python_class('tests/test_dsl.py', 'TestDSLShell').
python_method('TestDSLShell', 'test_shell_initialization', 0, 2, 3).
python_method('TestDSLShell', 'test_execute_command', 0, 2, 5).
python_method('TestDSLShell', 'test_execute_script', 0, 2, 6).
python_class('tests/test_dsl.py', 'TestDSLIntegration').
python_method('TestDSLIntegration', 'test_dsl_with_sumd_commands', 0, 2, 6).
python_method('TestDSLIntegration', 'test_complex_dsl_expressions', 0, 1, 4).
python_method('TestDSLIntegration', 'test_error_handling', 0, 3, 6).
python_class('tests/test_extractor.py', 'TestExtractPyproject').
python_method('TestExtractPyproject', 'test_missing_file_returns_empty', 1, 1, 1).
python_method('TestExtractPyproject', 'test_basic_fields', 1, 1, 2).
python_method('TestExtractPyproject', 'test_dependencies_parsed', 1, 1, 2).
python_method('TestExtractPyproject', 'test_dev_dependencies_from_optional', 1, 1, 2).
python_method('TestExtractPyproject', 'test_fallback_name_is_dir_name', 1, 1, 2).
python_method('TestExtractPyproject', 'test_corrupt_toml_returns_empty', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractTaskfile').
python_method('TestExtractTaskfile', 'test_missing_returns_empty', 1, 1, 1).
python_method('TestExtractTaskfile', 'test_parses_tasks', 1, 1, 3).
python_method('TestExtractTaskfile', 'test_task_without_desc', 1, 1, 2).
python_method('TestExtractTaskfile', 'test_multiple_tasks', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractPyqual').
python_method('TestExtractPyqual', 'test_missing_returns_empty', 1, 1, 1).
python_method('TestExtractPyqual', 'test_parses_pipeline', 1, 1, 2).
python_method('TestExtractPyqual', 'test_flat_format', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractPythonModules').
python_method('TestExtractPythonModules', 'test_missing_pkg_dir_returns_empty', 1, 1, 1).
python_method('TestExtractPythonModules', 'test_lists_modules', 1, 1, 3).
python_method('TestExtractPythonModules', 'test_excludes_dunder_files', 1, 1, 3).
python_class('tests/test_extractor.py', 'TestExtractReadmeTitle').
python_method('TestExtractReadmeTitle', 'test_missing_returns_empty', 1, 1, 1).
python_method('TestExtractReadmeTitle', 'test_extracts_h1', 1, 1, 2).
python_method('TestExtractReadmeTitle', 'test_no_h1_returns_empty', 1, 1, 2).
python_method('TestExtractReadmeTitle', 'test_first_h1_only', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractEnv').
python_method('TestExtractEnv', 'test_missing_returns_empty', 1, 1, 1).
python_method('TestExtractEnv', 'test_parses_key_value', 1, 1, 2).
python_method('TestExtractEnv', 'test_captures_preceding_comment', 1, 1, 2).
python_method('TestExtractEnv', 'test_captures_inline_comment', 1, 1, 2).
python_method('TestExtractEnv', 'test_empty_value_becomes_not_set', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractGoal').
python_method('TestExtractGoal', 'test_missing_returns_empty', 1, 1, 1).
python_method('TestExtractGoal', 'test_parses_project_and_versioning', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractProjectAnalysis').
python_method('TestExtractProjectAnalysis', 'test_missing_project_dir_returns_empty', 1, 1, 1).
python_method('TestExtractProjectAnalysis', 'test_loads_calls_toon_yaml', 1, 1, 4).
python_method('TestExtractProjectAnalysis', 'test_refactor_mode_loads_extra_files', 1, 1, 3).
python_method('TestExtractProjectAnalysis', 'test_missing_files_skipped', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractRequirements').
python_method('TestExtractRequirements', 'test_no_requirements_returns_empty', 1, 1, 1).
python_method('TestExtractRequirements', 'test_parses_requirements_txt', 1, 1, 3).
python_method('TestExtractRequirements', 'test_ignores_comments_and_flags', 1, 1, 2).
python_class('tests/test_extractor.py', 'TestExtractMakefile').
python_method('TestExtractMakefile', 'test_missing_returns_empty', 1, 1, 1).
python_method('TestExtractMakefile', 'test_parses_targets', 1, 1, 2).
python_method('TestExtractMakefile', 'test_comment_captured', 1, 1, 2).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPCQRSCommands').
python_method('TestMCPCQRSCommands', 'test_execute_command', 0, 1, 6).
python_method('TestMCPCQRSCommands', 'test_execute_command_error', 0, 1, 4).
python_method('TestMCPCQRSCommands', 'test_execute_query', 0, 1, 5).
python_method('TestMCPCQRSCommands', 'test_get_events', 0, 1, 4).
python_method('TestMCPCQRSCommands', 'test_get_aggregate', 0, 1, 5).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPDSLCommands').
python_method('TestMCPDSLCommands', 'test_execute_dsl', 0, 1, 5).
python_method('TestMCPDSLCommands', 'test_dsl_shell_info', 0, 1, 4).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPIntegration').
python_method('TestMCPIntegration', 'test_full_cqrs_workflow_via_mcp', 0, 3, 17).
python_method('TestMCPIntegration', 'test_dsl_integration_via_mcp', 0, 2, 7).
python_class('tests/test_mcp_cqrs_dsl.py', 'TestMCPErrorHandling').
python_method('TestMCPErrorHandling', 'test_unknown_command_type', 0, 1, 2).
python_method('TestMCPErrorHandling', 'test_unknown_query_type', 0, 1, 2).
python_method('TestMCPErrorHandling', 'test_aggregate_not_found', 0, 1, 3).
python_class('tests/test_mcp_server.py', 'TestDocToDict').
python_method('TestDocToDict', 'test_has_required_keys', 1, 1, 3).
python_method('TestDocToDict', 'test_section_has_fields', 1, 2, 2).
python_class('tests/test_mcp_server.py', 'TestResolvePath').
python_method('TestResolvePath', 'test_absolute_path_unchanged', 1, 1, 2).
python_method('TestResolvePath', 'test_relative_resolves_from_cwd', 0, 1, 2).
python_class('tests/test_mcp_server.py', 'TestListTools').
python_method('TestListTools', 'test_returns_thirteen_tools', 0, 1, 3).
python_method('TestListTools', 'test_tool_names', 0, 1, 2).
python_method('TestListTools', 'test_each_tool_has_input_schema', 0, 2, 2).
python_class('tests/test_mcp_server.py', 'TestParseSumd').
python_method('TestParseSumd', 'test_returns_json', 1, 1, 4).
python_method('TestParseSumd', 'test_missing_file_returns_error', 1, 1, 3).
python_class('tests/test_mcp_server.py', 'TestValidateSumd').
python_method('TestValidateSumd', 'test_valid_file', 1, 1, 4).
python_method('TestValidateSumd', 'test_missing_file_returns_error', 1, 1, 3).
python_class('tests/test_mcp_server.py', 'TestExportSumd').
python_method('TestExportSumd', 'test_export_json', 1, 1, 3).
python_method('TestExportSumd', 'test_export_markdown', 1, 1, 2).
python_method('TestExportSumd', 'test_export_to_file', 2, 1, 3).
python_class('tests/test_mcp_server.py', 'TestListSections').
python_method('TestListSections', 'test_returns_list', 1, 1, 5).
python_method('TestListSections', 'test_section_has_name', 1, 1, 4).
python_class('tests/test_mcp_server.py', 'TestGetSection').
python_method('TestGetSection', 'test_found_section', 1, 1, 4).
python_method('TestGetSection', 'test_missing_section', 1, 1, 3).
python_class('tests/test_mcp_server.py', 'TestInfoSumd').
python_method('TestInfoSumd', 'test_returns_info', 1, 1, 4).
python_class('tests/test_mcp_server.py', 'TestGenerateSumd').
python_method('TestGenerateSumd', 'test_generate_content', 0, 1, 1).
python_method('TestGenerateSumd', 'test_generate_to_file', 1, 1, 3).
python_class('tests/test_mcp_server.py', 'TestUnknownTool').
python_method('TestUnknownTool', 'test_unknown_returns_error', 0, 1, 2).
python_class('tests/test_sections.py', 'TestMetadataSection').
python_method('TestMetadataSection', 'test_always_renders', 0, 1, 3).
python_method('TestMetadataSection', 'test_contains_name_and_version', 0, 1, 4).
python_method('TestMetadataSection', 'test_contains_metadata_header', 0, 1, 3).
python_method('TestMetadataSection', 'test_optional_fields_omitted_when_empty', 0, 1, 4).
python_class('tests/test_sections.py', 'TestArchitectureSection').
python_method('TestArchitectureSection', 'test_always_renders', 0, 1, 3).
python_method('TestArchitectureSection', 'test_header_present', 0, 1, 4).
python_method('TestArchitectureSection', 'test_modules_listed', 0, 1, 4).
python_method('TestArchitectureSection', 'test_no_modules_no_source_modules_section', 0, 1, 4).
python_class('tests/test_sections.py', 'TestDependenciesSection').
python_method('TestDependenciesSection', 'test_renders_when_deps_present', 0, 1, 3).
python_method('TestDependenciesSection', 'test_runtime_deps_listed', 0, 1, 4).
python_method('TestDependenciesSection', 'test_no_deps_shows_fallback', 0, 1, 4).
python_method('TestDependenciesSection', 'test_dev_deps_section', 0, 1, 4).
python_class('tests/test_sections.py', 'TestWorkflowsSection').
python_method('TestWorkflowsSection', 'test_no_render_when_empty', 0, 1, 3).
python_method('TestWorkflowsSection', 'test_renders_with_tasks', 0, 1, 5).
python_method('TestWorkflowsSection', 'test_header_present', 0, 1, 3).
python_class('tests/test_sections.py', 'TestQualitySection').
python_method('TestQualitySection', 'test_no_render_when_empty', 0, 1, 3).
python_method('TestQualitySection', 'test_renders_with_pyqual', 0, 1, 3).
python_method('TestQualitySection', 'test_pipeline_name_in_output', 0, 1, 4).
python_class('tests/test_sections.py', 'TestEnvironmentSection').
python_method('TestEnvironmentSection', 'test_no_render_when_empty', 0, 1, 3).
python_method('TestEnvironmentSection', 'test_renders_with_vars', 0, 1, 5).
python_class('tests/test_sections.py', 'TestCallGraphSection').
python_method('TestCallGraphSection', 'test_no_render_without_calls', 0, 1, 3).
python_method('TestCallGraphSection', 'test_no_render_without_calls_file', 0, 1, 3).
python_method('TestCallGraphSection', 'test_renders_with_calls_file', 0, 1, 5).
python_class('tests/test_sections.py', 'TestCodeAnalysisSection').
python_method('TestCodeAnalysisSection', 'test_no_render_when_only_calls', 0, 1, 3).
python_method('TestCodeAnalysisSection', 'test_renders_with_map', 0, 1, 3).
python_class('tests/test_sections.py', 'TestRefactorAnalysisSection').
python_method('TestRefactorAnalysisSection', 'test_no_render_when_empty', 0, 1, 3).
python_method('TestRefactorAnalysisSection', 'test_renders_with_analysis_files', 0, 1, 5).
python_method('TestRefactorAnalysisSection', 'test_map_toon_excluded', 0, 1, 4).
python_class('tests/test_sections.py', 'TestSourceSnippetsSection').
python_method('TestSourceSnippetsSection', 'test_no_render_when_empty', 0, 1, 3).
python_method('TestSourceSnippetsSection', 'test_renders_with_snippets', 0, 1, 5).

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
sumd_workflow('analyze', 'manual').
sumd_workflow_step('analyze', 1, 'echo "🔬 Running project analysis..."').
sumd_workflow_step('analyze', 2, 'sumd analyze . --tools code2llm,redup,vallm').



% ── ARCHITECTURAL CONSISTENCY RULES ───────────────────────
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

