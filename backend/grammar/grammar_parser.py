"""
Grammar Parser - Reads production rules and deduces terminals/non-terminals
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Set, Optional


@dataclass
class ProductionRule:
    """Represents a single production rule: LHS -> RHS"""
    lhs: str
    rhs: List[str]
    
    def __repr__(self):
        return f"{self.lhs} -> {' '.join(self.rhs)}"


@dataclass
class Grammar:
    """Represents the complete grammar"""
    terminals: Dict[str, Optional[str]]
    non_terminals: Dict[str, str]
    production_rules: List[ProductionRule]
    start_symbol: str
    semantic_rules: Dict[str, int]
    
    def is_terminal(self, symbol: str) -> bool:
        return symbol in self.terminals
    
    def is_non_terminal(self, symbol: str) -> bool:
        return symbol in self.non_terminals
    
    def get_productions_for(self, non_terminal: str) -> List[ProductionRule]:
        return [rule for rule in self.production_rules if rule.lhs == non_terminal]
    
    def get_terminal_pattern(self, terminal: str) -> Optional[str]:
        return self.terminals.get(terminal)


class GrammarParser:
    """Parses pure production rules and deduces grammar structure"""
    
    # Hardcoded terminal patterns
    TERMINAL_PATTERNS = {
        'INT': r'\d+',
        'SEMICOLON': ';',
        'LBRACE': '{',
        'RBRACE': '}',
    }
    
    # Hardcoded keywords (terminals without patterns)
    KEYWORDS = ['MOVE', 'TURN', 'LEFT', 'RIGHT', 'REPEAT']
    
    # Hardcoded semantic constraints
    SEMANTIC_RULES = {
        'MAX_MOVE_DISTANCE': 100,
        'MAX_REPEAT_COUNT': 50,
        'MAX_TOTAL_INSTRUCTIONS': 10000,
    }
    
    def __init__(self, grammar_file_path: str):
        self.grammar_file_path = grammar_file_path
    
    def parse(self) -> Grammar:
        """Parse grammar file and deduce structure"""
        with open(self.grammar_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse production rules
        production_rules = self._parse_production_rules(content)
        
        # Deduce non-terminals (symbols on LHS of rules)
        non_terminals = self._deduce_non_terminals(production_rules)
        
        # Deduce terminals (symbols that appear in RHS but not in LHS)
        terminals = self._deduce_terminals(production_rules, non_terminals)
        
        # Start symbol is the first non-terminal (first LHS)
        start_symbol = production_rules[0].lhs if production_rules else 'S'
        
        return Grammar(
            terminals=terminals,
            non_terminals=non_terminals,
            production_rules=production_rules,
            start_symbol=start_symbol,
            semantic_rules=self.SEMANTIC_RULES
        )
    
    def _parse_production_rules(self, content: str) -> List[ProductionRule]:
        """Parse production rules from file"""
        rules = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse rule: LHS -> RHS
            if '->' in line:
                lhs, rhs = line.split('->', 1)
                lhs = lhs.strip()
                rhs_symbols = rhs.strip().split()
                
                rules.append(ProductionRule(lhs=lhs, rhs=rhs_symbols))
        
        return rules
    
    def _deduce_non_terminals(self, rules: List[ProductionRule]) -> Dict[str, str]:
        """Deduce non-terminals from LHS of production rules"""
        non_terminals = {}
        
        for rule in rules:
            if rule.lhs not in non_terminals:
                non_terminals[rule.lhs] = rule.lhs
        
        return non_terminals
    
    def _deduce_terminals(self, rules: List[ProductionRule], 
                          non_terminals: Dict[str, str]) -> Dict[str, Optional[str]]:
        """Deduce terminals from RHS symbols that are not non-terminals"""
        all_symbols = set()
        
        # Collect all symbols from RHS
        for rule in rules:
            for symbol in rule.rhs:
                if symbol != 'epsilon':  # epsilon is not a terminal
                    all_symbols.add(symbol)
        
        # Terminals are symbols that are not non-terminals
        terminals = {}
        
        for symbol in all_symbols:
            if symbol not in non_terminals:
                # Check if it's a known terminal with pattern
                if symbol in self.TERMINAL_PATTERNS:
                    terminals[symbol] = self.TERMINAL_PATTERNS[symbol]
                elif symbol in self.KEYWORDS:
                    terminals[symbol] = None  # Keyword without pattern
                else:
                    # Unknown terminal - treat as keyword
                    terminals[symbol] = None
        
        return terminals


def load_grammar(grammar_file_path: str) -> Grammar:
    """Load grammar from production rules file"""
    parser = GrammarParser(grammar_file_path)
    return parser.parse()


if __name__ == "__main__":
    # Test the grammar parser
    grammar = load_grammar("roboscript_grammar.txt")
    print("=== GRAMMAR LOADED ===")
    print(f"Start Symbol: {grammar.start_symbol}")
    print(f"\nNon-terminals: {list(grammar.non_terminals.keys())}")
    print(f"\nTerminals: {list(grammar.terminals.keys())}")
    print(f"\nProduction Rules:")
    for rule in grammar.production_rules:
        print(f"  {rule}")
    print(f"\nSemantic Rules: {grammar.semantic_rules}")
