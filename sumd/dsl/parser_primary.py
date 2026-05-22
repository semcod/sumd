"""Primary and literal expression parsing logic for the SUMD DSL Parser."""

from __future__ import annotations

from typing import Optional

from .parser_expr import DSLExpressionParser
from .lexer import DSLTokenType
from .ast_nodes import DSLExpression, DSLExpressionType


class DSLPrimaryParser(DSLExpressionParser):
    """Primary expression parsing methods for literals, identifiers, lists, dicts."""

    def _parse_paren_or_collection(self) -> Optional[DSLExpression]:
        """Parse parenthesized, list, or dict expression."""
        if self._match(DSLTokenType.LPAREN):
            expr = self._parse_pipeline()
            self._consume(DSLTokenType.RPAREN, "Expected ')' after expression.")
            return expr
        if self._match(DSLTokenType.LBRACKET):
            return self._parse_list()
        if self._match(DSLTokenType.LBRACE):
            return self._parse_dict()
        return None

    def _parse_identifier_command(self, identifier_token) -> Optional[DSLExpression]:
        """Return a standalone COMMAND node if at an expression boundary, else None."""
        if (
            self._is_at_end()
            or self._check(DSLTokenType.NEWLINE)
            or self._check(DSLTokenType.EOF)
            or self._check(DSLTokenType.SEMICOLON)
            or self._check(DSLTokenType.PIPE)
        ):
            return DSLExpression(
                type=DSLExpressionType.COMMAND,
                value=identifier_token.value,
                children=[],
            )
        return None

    def _parse_identifier_forms(self) -> Optional[DSLExpression]:
        """Parse function call, property access, command, or plain identifier."""
        if not self._check(DSLTokenType.IDENTIFIER):
            return None

        # Function call: id(
        if self._check_next(DSLTokenType.LPAREN):
            return self._parse_function_call()

        # Property access: id.id
        if (
            self._check_next(DSLTokenType.DOT)
            and self.current + 2 < len(self.tokens)
            and self.tokens[self.current + 2].type == DSLTokenType.IDENTIFIER
        ):
            return self._parse_property_access()

        identifier = self._advance()
        cmd = self._parse_identifier_command(identifier)
        if cmd is not None:
            return cmd

        return DSLExpression(
            type=DSLExpressionType.IDENTIFIER,
            value=identifier.value,
        )

    def _parse_literal_value(self) -> Optional[DSLExpression]:
        """Parse string, number, or boolean literal."""
        if self._match(DSLTokenType.STRING):
            value = self._previous().value
            return DSLExpression(
                type=DSLExpressionType.LITERAL,
                value=value[1:-1],
                metadata={"type": "string"},
            )
        if self._match(DSLTokenType.NUMBER):
            value = self._previous().value
            return DSLExpression(
                type=DSLExpressionType.LITERAL,
                value=float(value) if "." in value else int(value),
                metadata={"type": "float" if "." in value else "int"},
            )
        if self._match(DSLTokenType.BOOLEAN):
            value = self._previous().value
            return DSLExpression(
                type=DSLExpressionType.LITERAL,
                value=value == "true",
                metadata={"type": "bool"},
            )
        return None

    def _parse_primary(self) -> DSLExpression:
        """Parse primary expression."""
        if expr := self._parse_paren_or_collection():
            return expr

        # Dot as literal
        if self._match(DSLTokenType.DOT):
            return DSLExpression(
                type=DSLExpressionType.LITERAL,
                value=".",
                metadata={"type": "string"},
            )

        if expr := self._parse_identifier_forms():
            return expr

        if expr := self._parse_literal_value():
            return expr

        raise ValueError(f"Unexpected token: {self._peek().value}")

    def _parse_command(self) -> DSLExpression:
        """Parse command expression."""
        command = self._advance()
        args = []

        while not self._is_at_end() and not self._check(DSLTokenType.NEWLINE) and not self._check(DSLTokenType.SEMICOLON) and not self._check(DSLTokenType.PIPE):
            if self._check(DSLTokenType.EOF):
                break

            arg = self._parse_primary()
            args.append(arg)

        return DSLExpression(
            type=DSLExpressionType.COMMAND,
            value=command.value,
            children=args,
        )

    def _parse_function_call(self) -> DSLExpression:
        """Parse function call expression."""
        identifier = self._advance()
        self._consume(DSLTokenType.LPAREN, "Expected '(' after function name.")

        args = []
        if not self._check(DSLTokenType.RPAREN):
            args.append(self._parse_pipeline())
            while self._match(DSLTokenType.COMMA):
                args.append(self._parse_pipeline())

        self._consume(DSLTokenType.RPAREN, "Expected ')' after arguments.")

        return DSLExpression(
            type=DSLExpressionType.FUNCTION_CALL,
            value=identifier.value,
            children=args,
        )

    def _parse_property_access(self) -> DSLExpression:
        """Parse property access expression."""
        identifier = self._advance()
        self._advance()  # Skip '.'
        property_name = self._advance()

        return DSLExpression(
            type=DSLExpressionType.PROPERTY_ACCESS,
            value=identifier.value,
            children=[
                DSLExpression(type=DSLExpressionType.IDENTIFIER, value=property_name.value)
            ],
        )

    def _parse_list(self) -> DSLExpression:
        """Parse list literal."""
        items = []

        if not self._check(DSLTokenType.RBRACKET):
            items.append(self._parse_pipeline())
            while self._match(DSLTokenType.COMMA):
                items.append(self._parse_pipeline())

        self._consume(DSLTokenType.RBRACKET, "Expected ']' after list items.")

        return DSLExpression(
            type=DSLExpressionType.LIST,
            value="list",
            children=items,
        )

    def _parse_dict(self) -> DSLExpression:
        """Parse dictionary literal."""
        items = []

        if not self._check(DSLTokenType.RBRACE):
            # Parse key: value pairs
            key = self._parse_primary()
            self._consume(DSLTokenType.COLON, "Expected ':' after dictionary key.")
            value = self._parse_pipeline()
            items.append((key, value))

            while self._match(DSLTokenType.COMMA):
                key = self._parse_primary()
                self._consume(DSLTokenType.COLON, "Expected ':' after dictionary key.")
                value = self._parse_pipeline()
                items.append((key, value))

        self._consume(DSLTokenType.RBRACE, "Expected '}' after dictionary items.")

        return DSLExpression(
            type=DSLExpressionType.DICT,
            value="dict",
            metadata={"items": items},
        )
