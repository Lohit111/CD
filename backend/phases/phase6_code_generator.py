"""
Phase 6: Target Code Generation
Generates final executable code for the robot simulator
"""

from typing import List, Dict, Any
from .phase4_ir_generator import IRInstruction


class CodeGenerator:
    """Generates target code from optimized IR"""
    
    def __init__(self, instructions: List[IRInstruction]):
        self.instructions = instructions
        
        print("=" * 60)
        print("PHASE 6: TARGET CODE GENERATION")
        print("=" * 60)
        print(f"Input: {len(instructions)} optimized IR instructions")
        print("-" * 60)
        for i, instr in enumerate(instructions):
            print(f"  [{i:3d}] {instr}")
        print("-" * 60)
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate target code for robot simulator"""
        print(f"\n[Code Gen] Generating target code...")
        
        target_code = []
        
        for i, instr in enumerate(self.instructions):
            target_instr = {
                "opcode": instr.opcode,
                "operand": instr.operand
            }
            target_code.append(target_instr)
            print(f"  [{i:3d}] {instr.opcode} {instr.operand}")
        
        print(f"\n[Code Gen] Generated {len(target_code)} target instructions")
        print("=" * 60)
        print()
        
        return target_code


def generate_code(instructions: List[IRInstruction]) -> List[Dict[str, Any]]:
    """Convenience function to generate target code"""
    generator = CodeGenerator(instructions)
    return generator.generate()
