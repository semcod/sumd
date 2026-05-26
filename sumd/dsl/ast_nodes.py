"""DSL AST Nodes — expression types and nodes for the SUMD DSL."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class DSLExpressionType(Enum):
    """Types of DSL expressions."""
    COMMAND = "COMMAND"
    ASSIGNMENT = "ASSIGNMENT"
    COMPARISON = "COMPARISON"
    LOGICAL = "LOGICAL"
    ARITHMETIC = "ARITHMETIC"
    FUNCTION_CALL = "FUNCTION_CALL"
    PROPERTY_ACCESS = "PROPERTY_ACCESS"
    LITERAL = "LITERAL"
    IDENTIFIER = "IDENTIFIER"
    PIPELINE = "PIPELINE"
    BLOCK = "BLOCK"
    LIST = "LIST"
    DICT = "DICT"


@dataclass
class DSLExpression:
    """Expression in DSL."""
    type: DSLExpressionType
    value: Any
    children: List[DSLExpression] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """String representation of the expression."""
        if self.type == DSLExpressionType.COMMAND:
            args = " ".join(str(child) for child in self.children)
            return f"{self.value} {args}"
        if self.type == DSLExpressionType.FUNCTION_CALL:
            args = ", ".join(str(child) for child in self.children)
            return f"{self.value}({args})"
        if self.type == DSLExpressionType.PROPERTY_ACCESS:
            if self.children:
                return f"{self.value}.{str(self.children[0])}"
            return str(self.value)
        if self.type == DSLExpressionType.PIPELINE:
            return " | ".join(str(child) for child in self.children)
        return str(self.value)
