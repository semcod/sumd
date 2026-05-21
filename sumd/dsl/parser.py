"""DSL Parser for SUMD Domain Specific Language.

Backward-compatibility shim — re-exports all public names.
"""

from __future__ import annotations

from typing import List, Optional

from .lexer import DSLToken, DSLTokenType, DSLLexer
from .ast_nodes import DSLExpression, DSLExpressionType


class DSLParser:
    """Parser for DSL expressions."""
    
    def __init__(self, tokens: List[DSLToken]):
        self.tokens = tokens
        self.current = 0
    
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

    def _try_parse_command(self) -> Optional[DSLExpression]:
        """Try to parse a command with optional pipe; rewind and return None on failure."""
        saved_pos = self.current
        self._advance()  # consume identifier

        args: list[DSLExpression] = []
        has_pipe = False
        while (not self._is_at_end() and
               not self._check(DSLTokenType.NEWLINE) and
               not self._check(DSLTokenType.EOF) and
               not self._check(DSLTokenType.SEMICOLON)):
            if self._check(DSLTokenType.PIPE):
                has_pipe = True
                break
            arg = self._parse_primary()
            if arg:
                args.append(arg)

        valid = args or self._check(DSLTokenType.NEWLINE) or self._check(DSLTokenType.EOF) or self._check(DSLTokenType.SEMICOLON) or has_pipe
        if not valid:
            self.current = saved_pos
            return None

        cmd = DSLExpression(
            type=DSLExpressionType.COMMAND,
            value=self.tokens[saved_pos].value,
            children=args,
        )
        if has_pipe and self._match(DSLTokenType.PIPE):
            right = self._parse_statement()
            if right:
                return DSLExpression(
                    type=DSLExpressionType.PIPELINE,
                    value="|",
                    children=[cmd, right],
                )
        return cmd

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

    def _parse_identifier_forms(self) -> Optional[DSLExpression]:
        """Parse function call, property access, command, or plain identifier."""
        if not self._check(DSLTokenType.IDENTIFIER):
            return None

        # Function call: id(
        if self._check_next(DSLTokenType.LPAREN):
            return self._parse_function_call()

        # Property access: id.id
        if (self._check_next(DSLTokenType.DOT) and
                self.current + 2 < len(self.tokens) and
                self.tokens[self.current + 2].type == DSLTokenType.IDENTIFIER):
            return self._parse_property_access()

        identifier = self._advance()

        # Standalone command when at expression boundary
        if (self._is_at_end() or
                self._check(DSLTokenType.NEWLINE) or
                self._check(DSLTokenType.EOF) or
                self._check(DSLTokenType.SEMICOLON) or
                self._check(DSLTokenType.PIPE)):
            return DSLExpression(
                type=DSLExpressionType.COMMAND,
                value=identifier.value,
                children=[],
            )

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
    
    # Helper methods
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


def parse_dsl(text: str) -> DSLExpression:
    """Parse DSL text into expression."""
    lexer = DSLLexer(text)
    tokens = lexer.tokenize()
    parser = DSLParser(tokens)
    return parser.parse()
