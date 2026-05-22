"""Base class for DSL Parser containing core state and helper methods."""

from __future__ import annotations

from typing import List, Optional

from .lexer import DSLToken, DSLTokenType
from .ast_nodes import DSLExpression, DSLExpressionType


class DSLParserBase:
    """Base parser class with token traversal utilities."""

    def __init__(self, tokens: List[DSLToken]):
        self.tokens = tokens
        self.current = 0

    def _is_at_end(self) -> bool:
        """Check if we're at the end of tokens."""
        return self._peek().type == DSLTokenType.EOF

    def _peek(self) -> DSLToken:
        """Get current token without consuming it."""
        return self.tokens[self.current]

    def _previous(self) -> DSLToken:
        """Get previous token."""
        return self.tokens[self.current - 1]

    def _advance(self) -> DSLToken:
        """Consume and return current token."""
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _check(self, token_type: DSLTokenType, value: Optional[str] = None) -> bool:
        """Check current token type and optionally value."""
        if self._is_at_end():
            return False
        token = self._peek()
        if token.type != token_type:
            return False
        if value is not None and token.value != value:
            return False
        return True

    def _check_next(self, token_type: DSLTokenType, value: Optional[str] = None) -> bool:
        """Check next token type and optionally value."""
        if self.current + 1 >= len(self.tokens):
            return False
        token = self.tokens[self.current + 1]
        if token.type != token_type:
            return False
        if value is not None and token.value != value:
            return False
        return True

    def _match(self, token_type: DSLTokenType, value: Optional[str] = None) -> bool:
        """Match and consume token if it matches."""
        if self._check(token_type, value):
            self._advance()
            return True
        return False

    def _consume(self, token_type: DSLTokenType, message: str) -> DSLToken:
        """Consume token or raise error."""
        if self._check(token_type):
            return self._advance()
        raise ValueError(f"{message} Got {self._peek().value} instead.")
