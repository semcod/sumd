"""Expression parsing logic for the SUMD DSL Parser."""

from __future__ import annotations

from .parser_base import DSLParserBase
from .lexer import DSLTokenType
from .ast_nodes import DSLExpression, DSLExpressionType


class DSLExpressionParser(DSLParserBase):
    """Expression parsing methods for math and logic operations."""

    def _parse_logical_or(self) -> DSLExpression:
        """Parse logical OR expression."""
        left = self._parse_logical_and()

        while self._match(DSLTokenType.LOGICAL, "or"):
            operator = self._previous()
            right = self._parse_logical_and()

            left = DSLExpression(
                type=DSLExpressionType.LOGICAL,
                value=operator.value,
                children=[left, right],
            )

        return left

    def _parse_logical_and(self) -> DSLExpression:
        """Parse logical AND expression."""
        left = self._parse_comparison()

        while self._match(DSLTokenType.LOGICAL, "and"):
            operator = self._previous()
            right = self._parse_comparison()

            left = DSLExpression(
                type=DSLExpressionType.LOGICAL,
                value=operator.value,
                children=[left, right],
            )

        return left

    def _parse_comparison(self) -> DSLExpression:
        """Parse comparison expression."""
        left = self._parse_arithmetic()

        if self._match(DSLTokenType.COMPARATOR):
            operator = self._previous()
            right = self._parse_arithmetic()

            return DSLExpression(
                type=DSLExpressionType.COMPARISON,
                value=operator.value,
                children=[left, right],
            )

        return left

    def _parse_arithmetic(self) -> DSLExpression:
        """Parse arithmetic expression."""
        left = self._parse_term()

        while self._match(DSLTokenType.OPERATOR, "+") or self._match(DSLTokenType.OPERATOR, "-"):
            operator = self._previous()
            right = self._parse_term()

            left = DSLExpression(
                type=DSLExpressionType.ARITHMETIC,
                value=operator.value,
                children=[left, right],
            )

        return left

    def _parse_term(self) -> DSLExpression:
        """Parse term expression."""
        left = self._parse_factor()

        while self._match(DSLTokenType.OPERATOR, "*") or self._match(DSLTokenType.OPERATOR, "/") or self._match(DSLTokenType.OPERATOR, "%"):
            operator = self._previous()
            right = self._parse_factor()

            left = DSLExpression(
                type=DSLExpressionType.ARITHMETIC,
                value=operator.value,
                children=[left, right],
            )

        return left

    def _parse_factor(self) -> DSLExpression:
        """Parse factor expression."""
        if self._match(DSLTokenType.OPERATOR, "-"):
            operator = self._previous()
            right = self._parse_factor()

            return DSLExpression(
                type=DSLExpressionType.ARITHMETIC,
                value=operator.value,
                children=[right],
            )

        if self._match(DSLTokenType.LOGICAL, "not"):
            operator = self._previous()
            right = self._parse_factor()

            return DSLExpression(
                type=DSLExpressionType.LOGICAL,
                value=operator.value,
                children=[right],
            )

        return self._parse_primary()
