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
