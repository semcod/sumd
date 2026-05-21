"""DSL Lexer — token types and tokenizer for the SUMD DSL."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import List


class DSLTokenType(Enum):
    """Token types for DSL parsing."""
    COMMAND = "COMMAND"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    OPERATOR = "OPERATOR"
    COMPARATOR = "COMPARATOR"
    LOGICAL = "LOGICAL"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COMMA = "COMMA"
    DOT = "DOT"
    COLON = "COLON"
    PIPE = "PIPE"
    SEMICOLON = "SEMICOLON"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"


@dataclass
class DSLToken:
    """Token in DSL."""
    type: DSLTokenType
    value: str
    position: int = 0
    line: int = 1
    column: int = 1


class DSLLexer:
    """Lexer for tokenizing DSL expressions."""

    # Token patterns
    TOKEN_PATTERNS = [
        (DSLTokenType.COMMENT, r'#.*'),
        (DSLTokenType.STRING, r'"[^"]*"|\'[^\']*\''),
        (DSLTokenType.NUMBER, r'\d+\.?\d*'),
        (DSLTokenType.BOOLEAN, r'true|false'),
        (DSLTokenType.COMPARATOR, r'==|!=|<=|>=|<|>|contains|matches|startswith|endswith'),
        (DSLTokenType.LOGICAL, r'and|or|not'),
        (DSLTokenType.OPERATOR, r'\+|\-|\*|\/|\%|\*\*|\='),
        (DSLTokenType.LPAREN, r'\('),
        (DSLTokenType.RPAREN, r'\)'),
        (DSLTokenType.LBRACE, r'\{'),
        (DSLTokenType.RBRACE, r'\}'),
        (DSLTokenType.LBRACKET, r'\['),
        (DSLTokenType.RBRACKET, r'\]'),
        (DSLTokenType.COMMA, r','),
        (DSLTokenType.DOT, r'\.'),
        (DSLTokenType.COLON, r':'),
        (DSLTokenType.PIPE, r'\|'),
        (DSLTokenType.SEMICOLON, r';'),
        (DSLTokenType.NEWLINE, r'\n'),
        (DSLTokenType.WHITESPACE, r'[ \t\r]+'),
        (DSLTokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_\-]*'),
    ]

    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[DSLToken] = []

    def tokenize(self) -> List[DSLToken]:
        """Tokenize the input text."""
        while self.position < len(self.text):
            matched = False

            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.position)

                if match:
                    value = match.group(0)

                    # Skip whitespace and comments
                    if token_type not in [DSLTokenType.WHITESPACE, DSLTokenType.COMMENT]:
                        token = DSLToken(
                            type=token_type,
                            value=value,
                            position=self.position,
                            line=self.line,
                            column=self.column,
                        )
                        self.tokens.append(token)

                    # Update position
                    self.position = match.end()
                    self.column += len(value)

                    if token_type == DSLTokenType.NEWLINE:
                        self.line += 1
                        self.column = 1

                    matched = True
                    break

            if not matched:
                raise ValueError(
                    f"Unexpected character at line {self.line}, column {self.column}: "
                    f"{self.text[self.position]}"
                )

        # Add EOF token
        self.tokens.append(DSLToken(
            type=DSLTokenType.EOF,
            value="",
            position=self.position,
            line=self.line,
            column=self.column,
        ))

        return self.tokens
