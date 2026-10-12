"""
Grammar Parser - Reads and parses the grammar configuration file
This allows the compiler to be grammar-driven and adaptable
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Set, Optional, Tuple


@dataclass
class ProductionRule:
    """Represents a single production rule: LHS -> RHS"""
    lhs: str
    rhs: List[str]  # List of symbols on right-hand side
    
    def __repr__(self):
        return f"{self.lhs} -> {' '.join(self.rhs)}"


@dataclass
class Grammar:
    """Represents the complete grammar configuration"""
    terminals: Dict[str, Optional[str]]  # terminal name -> regex pattern (if any)
    non_terminals: Dict[str, str]  # symbol -> description
    production_rules: List[ProductionRule]
    start_symbol: str
    semantic_rules: Dict[str, int]
    
    def is_terminal(self, symbol: str) -> bool:
        """Check if a symbol is a terminal"""
        return symbol in self.terminals
    
    def is_non_terminal(self, symbol: str) -> bool:
        """Check if a symbol is a non-terminal"""
        return symbol in self.non_terminals
    
    def get_productions_for(self, non_terminal: str) -> List[ProductionRule]:
        """Get all production rules for a given non-terminal"""
        return [rule for rule in self.production_rules if rule.lhs == non_terminal]
    
    def get_terminal_pattern(self, terminal: str) -> Optional[str]:
        """Get the regex pattern for a terminal, if it has one"""
        return self.terminals.get(terminal)


class GrammarParser:
    """Parses the grammar configuration file"""
    
    def __init__(self, grammar_file_path: str):
        self.grammar_file_path = grammar_file_path
    
    def parse(self) -> Grammar:
        """Parse the grammar file and return Grammar object"""
        with open(self.grammar_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        terminals = self._parse_terminals(content)
        non_terminals = self._parse_non_terminals(content)
        production_rules = self._parse_production_rules(content)
        start_symbol = self._parse_start_symbol(content)
        semantic_rules = self._parse_semantic_rules(content)
        
        return Grammar(
            terminals=terminals,
            non_terminals=non_terminals,
            production_rules=production_rules,
            start_symbol=start_symbol,
            semantic_rules=semantic_rules
        )
    
    def _parse_terminals(self, content: str) -> Dict[str, Optional[str]]:
        """Parse [TERMINALS] section"""
        terminals = {}
        section = self._extract_section(content, "TERMINALS")
        
        for line in section.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split(maxsplit=1)
            if len(parts) == 1:
                # Terminal without pattern
                terminals[parts[0]] = None
            elif len(parts) == 2:
                # Terminal with regex pattern
                terminals[parts[0]] = parts[1]
        
        return terminals
    
    def _parse_non_terminals(self, content: str) -> Dict[str, str]:
        """Parse [NON_TERMINALS] section"""
        non_terminals = {}
        section = self._extract_section(content, "NON_TERMINALS")
        
        for line in section.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                non_terminals[parts[0]] = parts[1]
            elif len(parts) == 1:
                non_terminals[parts[0]] = parts[0]
        
        return non_terminals
    
    def _parse_production_rules(self, content: str) -> List[ProductionRule]:
        """Parse [PRODUCTION_RULES] section"""
        rules = []
        section = self._extract_section(content, "PRODUCTION_RULES")
        
        for line in section.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse rule: LHS -> RHS
            if '->' in line:
                lhs, rhs = line.split('->', 1)
                lhs = lhs.strip()
                rhs_symbols = rhs.strip().split()
                
                rules.append(ProductionRule(lhs=lhs, rhs=rhs_symbols))
        
        return rules
    
    def _parse_start_symbol(self, content: str) -> str:
        """Parse [START_SYMBOL] section"""
        section = self._extract_section(content, "START_SYMBOL")
        
        for line in section.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                return line
        
        return "S"  # Default start symbol
    
    def _parse_semantic_rules(self, content: str) -> Dict[str, int]:
        """Parse [SEMANTIC_RULES] section"""
        rules = {}
        section = self._extract_section(content, "SEMANTIC_RULES")
        
        for line in section.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse: KEY = VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                try:
                    rules[key] = int(value)
                except ValueError:
                    rules[key] = value
        
        return rules
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a section from the grammar file"""
        pattern = rf'\[{section_name}\](.*?)(?=\[|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""


def load_grammar(grammar_file_path: str) -> Grammar:
    """Convenience function to load grammar from file"""
    parser = GrammarParser(grammar_file_path)
    return parser.parse()


if __name__ == "__main__":
    # Test the grammar parser
    grammar = load_grammar("roboscript_grammar.txt")
    print("=== GRAMMAR LOADED ===")
    print(f"Start Symbol: {grammar.start_symbol}")
    print(f"\nTerminals: {list(grammar.terminals.keys())}")
    print(f"\nNon-terminals: {list(grammar.non_terminals.keys())}")
    print(f"\nProduction Rules:")
    for rule in grammar.production_rules:
        print(f"  {rule}")
    print(f"\nSemantic Rules: {grammar.semantic_rules}")
