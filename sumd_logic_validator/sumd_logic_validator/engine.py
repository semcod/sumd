"""Prolog engine — re-exports from sumd.utils.prolog_core for backward compatibility."""

from sumd.utils.prolog_core import (
    Variable,
    Term,
    Rule,
    is_variable,
    to_term,
    _split_body_terms,
    PythonPrologDB,
    unify,
    resolve_val,
    deep_resolve,
    extend_subst,
    occurs_check,
    rename_variables,
    PythonPrologEngine,
    HybridPrologEngine,
    PYSWIP_AVAILABLE,
)

__all__ = [
    "Variable",
    "Term",
    "Rule",
    "is_variable",
    "to_term",
    "_split_body_terms",
    "PythonPrologDB",
    "unify",
    "resolve_val",
    "deep_resolve",
    "extend_subst",
    "occurs_check",
    "rename_variables",
    "PythonPrologEngine",
    "HybridPrologEngine",
    "PYSWIP_AVAILABLE",
]
