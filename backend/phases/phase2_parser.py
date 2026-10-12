"""
Phase 2: Syntax Analysis (Parser)
Grammar-driven recursive descent parser
Builds an Abstract Syntax Tree (AST) using production rules from grammar
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ASTNode:
    """Base class for AST nodes"""
    node_type: str
    line: int
    column: int
    children: List['ASTNode']
    value: Optional[str] = None
    
    def __repr__(self, indent=0):
        spaces = "  " * indent
        result = f"{spaces}{self.node_type}"
        if self.value:
            result += f" [{self.value}]"
        result += "\n"
        for child in self.children:
            result += child.__repr__(indent + 1)
        return result


class ParserError(Exception):
    """Exception raised during syntax analysis"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Parser error at {line}:{column}: {message}")


class Parser:
    """Grammar-driven recursive descent parser"""
    
    def __init__(self, tokens: List, grammar):
        self.tokens = tokens
        self.grammar = grammar
        self.pos = 0
        
        print("=" * 60)
        print("PHASE 2: SYNTAX ANALYSIS (PARSING)")
        print("=" * 60)
        print(f"Input: {len(tokens)} tokens")
        print("-" * 60)
        for i, token in enumerate(tokens):
            print(f"  [{i}] {token}")
        print("-" * 60)
        print(f"\n[Parser] Using grammar with start symbol: {grammar.start_symbol}")
        print(f"[Parser] Production rules:")
        for rule in grammar.production_rules:
            print(f"  {rule}")
    
    def current_token(self):
        """Get current token"""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1):
        """Look ahead at token"""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self):
        """Move to next token and return current"""
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def expect(self, token_type: str):
        """Expect a specific token type and consume it"""
        token = self.current_token()
        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type}, got {token.type}",
                token.line,
                token.column
            )
        print(f"  [Parser] Matched: {token_type}")
        return self.advance()
    
    def parse(self) -> ASTNode:
        """Parse the token stream into an AST"""
        print(f"\n[Parser] Starting parse from '{self.grammar.start_symbol}'...")
        
        ast = self.parse_non_terminal(self.grammar.start_symbol)
        
        # Ensure we consumed all tokens
        if self.current_token().type != "EOF":
            token = self.current_token()
            raise ParserError(
                f"Unexpected token {token.type} after program end",
                token.line,
                token.column
            )
        
        print(f"\n[Parser] Parse successful!")
        print("\n[Parser] Generated AST:")
        print("-" * 60)
        print(ast)
        print("-" * 60)
        print("=" * 60)
        print()
        
        return ast
    
    def parse_non_terminal(self, non_terminal: str) -> ASTNode:
        """Parse a non-terminal using its production rules"""
        print(f"\n  [Parser] Parsing non-terminal: {non_terminal}")
        
        rules = self.grammar.get_productions_for(non_terminal)
        
        if not rules:
            raise ParserError(
                f"No production rules for non-terminal '{non_terminal}'",
                self.current_token().line,
                self.current_token().column
            )
        
        # Try each production rule
        for rule in rules:
            print(f"    [Parser] Trying rule: {rule}")
            
            # Check for epsilon production
            if rule.rhs == ["epsilon"]:
                print(f"    [Parser] Matched epsilon production")
                return ASTNode(
                    node_type=non_terminal,
                    line=self.current_token().line,
                    column=self.current_token().column,
                    children=[]
                )
            
            # Try to match the rule
            saved_pos = self.pos
            try:
                children = []
                for symbol in rule.rhs:
                    if self.grammar.is_terminal(symbol):
                        # Match terminal
                        token = self.expect(symbol)
                        child = ASTNode(
                            node_type=symbol,
                            line=token.line,
                            column=token.column,
                            children=[],
                            value=token.value
                        )
                        children.append(child)
                    elif self.grammar.is_non_terminal(symbol):
                        # Recursively parse non-terminal
                        child = self.parse_non_terminal(symbol)
                        children.append(child)
                    else:
                        raise ParserError(
                            f"Unknown symbol '{symbol}' in grammar",
                            self.current_token().line,
                            self.current_token().column
                        )
                
                # Success! Return the AST node
                print(f"    [Parser] Successfully matched rule: {rule}")
                return ASTNode(
                    node_type=non_terminal,
                    line=self.current_token().line,
                    column=self.current_token().column,
                    children=children
                )
            
            except ParserError:
                # This rule didn't match, try next one
                self.pos = saved_pos
                print(f"    [Parser] Rule didn't match, backtracking...")
                continue
        
        # No rule matched
        token = self.current_token()
        raise ParserError(
            f"No production rule for '{non_terminal}' matches at token {token.type}",
            token.line,
            token.column
        )


def parse(tokens: List, grammar) -> ASTNode:
    """Convenience function to parse tokens into AST"""
    parser = Parser(tokens, grammar)
    return parser.parse()
