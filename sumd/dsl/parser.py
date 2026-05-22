"""DSL Parser for SUMD Domain Specific Language.

This module re-exports all public names and implements the primary entry point
for statement, pipeline, and command parsing logic.
"""

from __future__ import annotations

from typing import List, Optional

from .lexer import DSLToken, DSLTokenType, DSLLexer
from .ast_nodes import DSLExpression, DSLExpressionType
from .parser_primary import DSLPrimaryParser


class DSLParser(DSLPrimaryParser):
    """Parser for DSL expressions."""

    def parse(self) -> DSLExpression:
        """Parse tokens into DSL expression."""
        if not self.tokens:
            raise ValueError("No tokens to parse")

        expressions = []

        while not self._is_at_end():
            expr = self._parse_statement()
            if expr:
                expressions.append(expr)

            # Skip semicolons
            if self._match(DSLTokenType.SEMICOLON):
                continue

        # If single expression, return it directly
        if len(expressions) == 1:
            return expressions[0]

        # Otherwise return a block
        return DSLExpression(
            type=DSLExpressionType.BLOCK,
            value="block",
            children=expressions,
        )

    def _looks_like_command(self) -> bool:
        """True if current IDENTIFIER starts a command (not func/assign/expr)."""
        if not self._check(DSLTokenType.IDENTIFIER):
            return False
        next_type = self._peek_next_type()
        return next_type not in (
            DSLTokenType.LPAREN,
            DSLTokenType.PIPE,
            DSLTokenType.COMPARATOR,
            DSLTokenType.LOGICAL,
        ) and not self._check_next(DSLTokenType.OPERATOR, "=")

    def _peek_next_type(self) -> Optional[DSLTokenType]:
        """Return type of next token, or None if at end."""
        if self.current + 1 >= len(self.tokens):
            return None
        return self.tokens[self.current + 1].type

    def _is_command_boundary(self) -> bool:
        """Return True if the current position marks a natural end of a command argument list."""
        return (
            self._is_at_end()
            or self._check(DSLTokenType.NEWLINE)
            or self._check(DSLTokenType.EOF)
            or self._check(DSLTokenType.SEMICOLON)
        )

    def _collect_command_args(self) -> tuple[list[DSLExpression], bool]:
        """Collect command argument expressions until a boundary or pipe. Returns (args, has_pipe)."""
        args: list[DSLExpression] = []
        has_pipe = False
        while not self._is_command_boundary() and not self._is_at_end():
            if self._check(DSLTokenType.PIPE):
                has_pipe = True
                break
            arg = self._parse_primary()
            if arg:
                args.append(arg)
        return args, has_pipe

    def _build_pipeline_or_cmd(
        self, cmd: DSLExpression, has_pipe: bool
    ) -> DSLExpression:
        """Wrap *cmd* in a PIPELINE node if a pipe token follows, otherwise return *cmd* as-is."""
        if has_pipe and self._match(DSLTokenType.PIPE):
            right = self._parse_statement()
            if right:
                return DSLExpression(
                    type=DSLExpressionType.PIPELINE,
                    value="|",
                    children=[cmd, right],
                )
        return cmd

    def _try_parse_command(self) -> Optional[DSLExpression]:
        """Try to parse a command with optional pipe; rewind and return None on failure."""
        saved_pos = self.current
        self._advance()  # consume identifier

        args, has_pipe = self._collect_command_args()

        if not (args or self._is_command_boundary() or has_pipe):
            self.current = saved_pos
            return None

        cmd = DSLExpression(
            type=DSLExpressionType.COMMAND,
            value=self.tokens[saved_pos].value,
            children=args,
        )
        return self._build_pipeline_or_cmd(cmd, has_pipe)

    def _parse_statement(self) -> Optional[DSLExpression]:
        """Parse a statement."""
        if self._match(DSLTokenType.NEWLINE):
            return None

        if self._looks_like_command():
            expr = self._try_parse_command()
            if expr is not None:
                self._match(DSLTokenType.NEWLINE)
                return expr

        expr = self._parse_pipeline()
        self._match(DSLTokenType.NEWLINE)
        return expr

    def _parse_pipeline(self) -> DSLExpression:
        """Parse a pipeline expression."""
        left = self._parse_assignment()

        if self._match(DSLTokenType.PIPE):
            right = self._parse_pipeline()
            return DSLExpression(
                type=DSLExpressionType.PIPELINE,
                value="|",
                children=[left, right],
            )

        return left

    def _parse_assignment(self) -> DSLExpression:
        """Parse assignment expression."""
        if self._check(DSLTokenType.IDENTIFIER) and self._check_next(DSLTokenType.OPERATOR, "="):
            identifier = self._advance()
            self._advance()  # Skip '='
            value = self._parse_logical_or()

            return DSLExpression(
                type=DSLExpressionType.ASSIGNMENT,
                value="=",
                children=[
                    DSLExpression(type=DSLExpressionType.IDENTIFIER, value=identifier.value),
                    value,
                ],
            )

        return self._parse_logical_or()


def parse_dsl(text: str) -> DSLExpression:
    """Parse DSL text into expression."""
    lexer = DSLLexer(text)
    tokens = lexer.tokenize()
    parser = DSLParser(tokens)
    return parser.parse()
