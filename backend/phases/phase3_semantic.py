"""
Phase 3: Semantic Analysis
Validates the AST for semantic correctness using rules from grammar
"""

from typing import Dict


class SemanticError(Exception):
    """Exception raised during semantic analysis"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Semantic error at {line}:{column}: {message}")


class SemanticAnalyzer:
    """Grammar-driven semantic analyzer"""
    
    def __init__(self, ast, grammar):
        self.ast = ast
        self.grammar = grammar
        self.semantic_rules = grammar.semantic_rules
        self.errors = []
        self.warnings = []
        
        print("=" * 60)
        print("PHASE 3: SEMANTIC ANALYSIS")
        print("=" * 60)
        print("Input AST:")
        print("-" * 60)
        print(ast)
        print("-" * 60)
        print(f"\n[Semantic] Loaded semantic rules from grammar:")
        for key, value in self.semantic_rules.items():
            print(f"  {key} = {value}")
    
    def analyze(self):
        """Perform semantic analysis on the AST"""
        print(f"\n[Semantic] Starting analysis...")
        
        self.visit_node(self.ast)
        
        if self.warnings:
            print(f"\n[Semantic] Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print(f"\n[Semantic] Errors found: {len(self.errors)}")
            for error in self.errors:
                print(f"  {error}")
            raise SemanticError(
                self.errors[0],
                self.ast.line,
                self.ast.column
            )
        
        # Estimate instruction count
        instruction_count = self.estimate_instructions(self.ast)
        print(f"\n[Semantic] Estimated instruction count: {instruction_count}")
        
        max_instructions = self.semantic_rules.get('MAX_TOTAL_INSTRUCTIONS', 10000)
        if instruction_count > max_instructions:
            raise SemanticError(
                f"Program would generate {instruction_count} instructions, exceeding limit of {max_instructions}",
                self.ast.line,
                self.ast.column
            )
        
        print(f"[Semantic] Analysis passed!")
        print("=" * 60)
        print()
    
    def visit_node(self, node, depth=0):
        """Visit a node and perform semantic checks"""
        indent = "  " * depth
        print(f"{indent}[Semantic] Checking {node.node_type}")
        
        # Check based on node type
        if node.node_type == "M":  # Move command
            self.check_move_command(node, depth)
        elif node.node_type == "T":  # Turn command
            self.check_turn_command(node, depth)
        elif node.node_type == "R":  # Repeat command
            self.check_repeat_command(node, depth)
        
        # Recursively visit children
        for child in node.children:
            self.visit_node(child, depth + 1)
    
    def check_move_command(self, node, depth):
        """Validate MOVE command"""
        indent = "  " * depth
        
        # Find the INT child
        int_node = None
        for child in node.children:
            if child.node_type == "INT":
                int_node = child
                break
        
        if int_node:
            distance = int(int_node.value)
            print(f"{indent}  MOVE distance: {distance}")
            
            max_distance = self.semantic_rules.get('MAX_MOVE_DISTANCE', 100)
            if distance > max_distance:
                error = f"MOVE distance {distance} exceeds maximum {max_distance}"
                self.errors.append(error)
                print(f"{indent}  ERROR: {error}")
            elif distance == 0:
                warning = f"MOVE distance is 0 (no-op)"
                self.warnings.append(warning)
                print(f"{indent}  WARNING: {warning}")
    
    def check_turn_command(self, node, depth):
        """Validate TURN command"""
        indent = "  " * depth
        
        # Find direction
        direction = None
        for child in node.children:
            if child.node_type in ["LEFT", "RIGHT"]:
                direction = child.node_type
                break
        
        if direction:
            print(f"{indent}  TURN direction: {direction}")
    
    def check_repeat_command(self, node, depth):
        """Validate REPEAT command"""
        indent = "  " * depth
        
        # Find the INT child
        int_node = None
        for child in node.children:
            if child.node_type == "INT":
                int_node = child
                break
        
        if int_node:
            count = int(int_node.value)
            print(f"{indent}  REPEAT count: {count}")
            
            max_repeat = self.semantic_rules.get('MAX_REPEAT_COUNT', 50)
            if count > max_repeat:
                error = f"REPEAT count {count} exceeds maximum {max_repeat}"
                self.errors.append(error)
                print(f"{indent}  ERROR: {error}")
            elif count == 0:
                warning = f"REPEAT count is 0 (block will not execute)"
                self.warnings.append(warning)
                print(f"{indent}  WARNING: {warning}")
    
    def estimate_instructions(self, node, multiplier=1):
        """Estimate total instructions after expansion"""
        if node.node_type == "M":  # Move
            return multiplier
        elif node.node_type == "T":  # Turn
            return multiplier
        elif node.node_type == "R":  # Repeat
            # Find repeat count
            count = 1
            for child in node.children:
                if child.node_type == "INT":
                    count = int(child.value)
                    break
            
            # Count instructions inside repeat
            total = 0
            for child in node.children:
                total += self.estimate_instructions(child, multiplier * count)
            return total
        else:
            # Recurse into children
            total = 0
            for child in node.children:
                total += self.estimate_instructions(child, multiplier)
            return total


def analyze(ast, grammar):
    """Convenience function to perform semantic analysis"""
    analyzer = SemanticAnalyzer(ast, grammar)
    analyzer.analyze()
