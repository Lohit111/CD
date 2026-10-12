"""
Phase 4: Intermediate Representation (IR) Generation
Converts AST into intermediate code
"""

from dataclasses import dataclass
from typing import List, Any, Dict


@dataclass
class IRInstruction:
    """IR instruction"""
    opcode: str
    operand: Any = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {"opcode": self.opcode, "operand": self.operand}
    
    def __repr__(self):
        if self.operand is not None:
            return f"{self.opcode} {self.operand}"
        return self.opcode


class IRGenerator:
    """Generates intermediate representation from AST"""
    
    def __init__(self, ast, grammar):
        self.ast = ast
        self.grammar = grammar
        self.instructions: List[IRInstruction] = []
        
        print("=" * 60)
        print("PHASE 4: INTERMEDIATE CODE GENERATION")
        print("=" * 60)
        print("Input AST:")
        print("-" * 60)
        print(ast)
        print("-" * 60)
    
    def generate(self) -> List[IRInstruction]:
        """Generate IR from AST"""
        print(f"\n[IR Gen] Starting IR generation...")
        
        self.visit_node(self.ast)
        
        print(f"\n[IR Gen] Generated {len(self.instructions)} instructions:")
        print("-" * 60)
        for i, instr in enumerate(self.instructions):
            print(f"  [{i:3d}] {instr}")
        print("-" * 60)
        print("=" * 60)
        print()
        
        return self.instructions
    
    def visit_node(self, node, depth=0):
        """Visit AST node and generate IR"""
        indent = "  " * depth
        
        if node.node_type == "M":  # Move command
            self.generate_move(node, depth)
        elif node.node_type == "T":  # Turn command
            self.generate_turn(node, depth)
        elif node.node_type == "R":  # Repeat command
            self.generate_repeat(node, depth)
        else:
            # Recurse into children for other nodes
            for child in node.children:
                self.visit_node(child, depth)
    
    def generate_move(self, node, depth):
        """Generate IR for MOVE command"""
        indent = "  " * depth
        
        # Find INT child
        distance = None
        for child in node.children:
            if child.node_type == "INT":
                distance = int(child.value)
                break
        
        if distance is not None:
            instr = IRInstruction("MOVE", distance)
            self.instructions.append(instr)
            print(f"{indent}[IR Gen] Generated: {instr}")
    
    def generate_turn(self, node, depth):
        """Generate IR for TURN command"""
        indent = "  " * depth
        
        # Find direction child
        direction = None
        for child in node.children:
            if child.node_type in ["LEFT", "RIGHT"]:
                direction = child.node_type
                break
        
        if direction:
            instr = IRInstruction("TURN", direction)
            self.instructions.append(instr)
            print(f"{indent}[IR Gen] Generated: {instr}")
    
    def generate_repeat(self, node, depth):
        """Generate IR for REPEAT - expands the loop"""
        indent = "  " * depth
        
        # Find repeat count
        count = None
        for child in node.children:
            if child.node_type == "INT":
                count = int(child.value)
                break
        
        if count is not None:
            print(f"{indent}[IR Gen] Expanding REPEAT {count} times...")
            
            # Find the statement list inside repeat
            for child in node.children:
                if child.node_type == "L":  # Statement list
                    # Expand loop by repeating the statements
                    for iteration in range(count):
                        print(f"{indent}  [IR Gen] Iteration {iteration + 1}/{count}")
                        for stmt_child in child.children:
                            self.visit_node(stmt_child, depth + 1)


def generate_ir_objects(ast, grammar) -> List[IRInstruction]:
    """Generate IR and return as list of IRInstruction objects"""
    generator = IRGenerator(ast, grammar)
    return generator.generate()


def generate_ir(ast, grammar) -> List[Dict[str, Any]]:
    """Generate IR and return as list of dicts"""
    instructions = generate_ir_objects(ast, grammar)
    return [instr.to_dict() for instr in instructions]
