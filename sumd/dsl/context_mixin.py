"""Shared DSL context helpers used by both engine and schema DSLContext classes."""

from typing import Any


class VariableMixin:
    """Mixin providing set_variable / get_variable helpers."""

    variables: dict[str, Any]

    def set_variable(self, name: str, value: Any) -> None:
        """Set a variable in the context."""
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """Get a variable from the context."""
        return self.variables.get(name)
