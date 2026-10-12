"""
Phase 1: Lexical Analysis (Lexer)
Grammar-driven lexer that reads token definitions from grammar file
"""

import re
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto


@dataclass
class Token:
    """Represents a token with type, value, and source location"""
    type: str  # Token type name (e.g., "MOVE", "INT", "SEMICOLON")
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"


class LexerError(Exception):
    """Exception raised during lexical analysis"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at {line}:{column}: {message}")


class Lexer:
    """Grammar-driven lexical analyzer"""
    
    def __init__(self, source: str, grammar):
        self.source = source
        self.grammar = grammar
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Build token specifications from grammar
        self._build_token_specs()
        
        print("=" * 60)
        print("PHASE 1: LEXICAL ANALYSIS")
        print("=" * 60)
        print(f"Input source code ({len(source)} characters):")
        print("-" * 60)
        print(source)
        print("-" * 60)
    
    def _build_token_specs(self):
        """Build token specifications from grammar terminals"""
        self.keyword_tokens = {}
        self.symbol_tokens = {}
        self.pattern_tokens = {}
        
        for terminal, pattern in self.grammar.terminals.items():
            if pattern is None:
                # It's a keyword (exact match required)
                self.keyword_tokens[terminal] = terminal
            elif pattern.startswith('\\'):
                # It's a regex pattern (like \d+ for integers)
                self.pattern_tokens[terminal] = pattern
            else:
                # It's a symbol (like ; or { or })
                self.symbol_tokens[terminal] = pattern
        
        print(f"\n[Lexer] Loaded from grammar:")
        print(f"  Keywords: {list(self.keyword_tokens.keys())}")
        print(f"  Symbols: {self.symbol_tokens}")
        print(f"  Patterns: {self.pattern_tokens}")
    
    def current_char(self) -> Optional[str]:
        """Get current character without advancing"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Look ahead at character without advancing"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Move to next character and return current"""
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace and comments"""
        while self.current_char() is not None:
            char = self.current_char()
            
            if char in ' \t\n\r':
                self.advance()
                continue
            
            # Skip comments (// style)
            if char == '/' and self.peek_char() == '/':
                while self.current_char() is not None and self.current_char() != '\n':
                    self.advance()
                continue
            
            break
    
    def try_match_pattern(self) -> Optional[Token]:
        """Try to match a pattern-based token (like INT)"""
        for token_type, pattern in self.pattern_tokens.items():
            # Try to match pattern at current position
            remaining = self.source[self.pos:]
            match = re.match(pattern, remaining)
            
            if match:
                value = match.group(0)
                start_line = self.line
                start_column = self.column
                
                # Advance position
                for _ in value:
                    self.advance()
                
                return Token(token_type, value, start_line, start_column)
        
        return None
    
    def try_match_keyword(self) -> Optional[Token]:
        """Try to match a keyword"""
        for token_type, keyword in self.keyword_tokens.items():
            if self.source[self.pos:].startswith(keyword):
                # Check that it's not part of a longer word
                next_pos = self.pos + len(keyword)
                if next_pos < len(self.source):
                    next_char = self.source[next_pos]
                    if next_char.isalnum():
                        continue  # Part of a longer identifier
                
                start_line = self.line
                start_column = self.column
                
                # Consume the keyword
                for _ in keyword:
                    self.advance()
                
                return Token(token_type, keyword, start_line, start_column)
        
        return None
    
    def try_match_symbol(self) -> Optional[Token]:
        """Try to match a symbol"""
        for token_type, symbol in self.symbol_tokens.items():
            if self.source[self.pos:].startswith(symbol):
                start_line = self.line
                start_column = self.column
                
                # Consume the symbol
                for _ in symbol:
                    self.advance()
                
                return Token(token_type, symbol, start_line, start_column)
        
        return None
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code"""
        print(f"\n[Lexer] Starting tokenization...")
        
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            start_pos = self.pos
            
            # Try to match token types in order of priority:
            # 1. Symbols (highest priority - exact match)
            # 2. Keywords (must match completely)
            # 3. Patterns (like numbers)
            
            token = self.try_match_symbol()
            if token is None:
                token = self.try_match_keyword()
            if token is None:
                token = self.try_match_pattern()
            
            if token is None:
                # No match found
                char = self.current_char()
                raise LexerError(
                    f"Unexpected character '{char}'",
                    self.line,
                    self.column
                )
            
            self.tokens.append(token)
            print(f"  {token}")
        
        # Add EOF token
        eof_token = Token("EOF", "", self.line, self.column)
        self.tokens.append(eof_token)
        
        print(f"\n[Lexer] Tokenization complete: {len(self.tokens)} tokens generated")
        print("=" * 60)
        print()
        
        return self.tokens


def tokenize(source: str, grammar) -> List[Token]:
    """Convenience function to tokenize source code"""
    lexer = Lexer(source, grammar)
    return lexer.tokenize()
