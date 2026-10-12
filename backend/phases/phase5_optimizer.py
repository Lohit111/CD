"""
Phase 5: Code Optimization
Applies optimizations to intermediate representation
"""

from typing import List
from .phase4_ir_generator import IRInstruction


class Optimizer:
    """IR optimizer"""
    
    def __init__(self, instructions: List[IRInstruction]):
        self.instructions = instructions
        
        print("=" * 60)
        print("PHASE 5: CODE OPTIMIZATION")
        print("=" * 60)
        print(f"Input: {len(instructions)} IR instructions")
        print("-" * 60)
        for i, instr in enumerate(instructions):
            print(f"  [{i:3d}] {instr}")
        print("-" * 60)
    
    def optimize(self) -> List[IRInstruction]:
        """Apply optimization passes"""
        optimized = self.instructions[:]
        
        print(f"\n[Optimizer] Applying optimization passes...")
        
        # Pass 1: Merge consecutive moves
        print(f"\n[Optimizer] Pass 1: Merge consecutive MOVE instructions")
        before_count = len(optimized)
        optimized = self.merge_consecutive_moves(optimized)
        after_count = len(optimized)
        print(f"  Instructions: {before_count} -> {after_count} (saved {before_count - after_count})")
        
        # Pass 2: Cancel opposite turns
        print(f"\n[Optimizer] Pass 2: Cancel opposite turns")
        before_count = len(optimized)
        optimized = self.cancel_opposite_turns(optimized)
        after_count = len(optimized)
        print(f"  Instructions: {before_count} -> {after_count} (saved {before_count - after_count})")
        
        # Pass 3: Remove full rotations
        print(f"\n[Optimizer] Pass 3: Remove full rotations (4 identical turns)")
        before_count = len(optimized)
        optimized = self.remove_full_rotations(optimized)
        after_count = len(optimized)
        print(f"  Instructions: {before_count} -> {after_count} (saved {before_count - after_count})")
        
        print(f"\n[Optimizer] Optimization complete!")
        print(f"  Original: {len(self.instructions)} instructions")
        print(f"  Optimized: {len(optimized)} instructions")
        print(f"  Reduction: {len(self.instructions) - len(optimized)} instructions ({100 * (len(self.instructions) - len(optimized)) / max(1, len(self.instructions)):.1f}%)")
        
        print("\nOptimized IR:")
        print("-" * 60)
        for i, instr in enumerate(optimized):
            print(f"  [{i:3d}] {instr}")
        print("-" * 60)
        print("=" * 60)
        print()
        
        return optimized
    
    def merge_consecutive_moves(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Merge consecutive MOVE instructions"""
        if not instructions:
            return instructions
        
        optimized = []
        i = 0
        
        while i < len(instructions):
            current = instructions[i]
            
            if current.opcode == "MOVE":
                # Accumulate consecutive moves
                total_distance = current.operand
                j = i + 1
                
                while j < len(instructions) and instructions[j].opcode == "MOVE":
                    print(f"    Merging MOVE {instructions[j].operand} into MOVE {total_distance}")
                    total_distance += instructions[j].operand
                    j += 1
                
                if total_distance > 0:
                    optimized.append(IRInstruction("MOVE", total_distance))
                    if j - i > 1:
                        print(f"    Result: MOVE {total_distance} (merged {j - i} instructions)")
                
                i = j
            else:
                optimized.append(current)
                i += 1
        
        return optimized
    
    def cancel_opposite_turns(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Cancel adjacent opposite turns"""
        if len(instructions) < 2:
            return instructions
        
        optimized = []
        i = 0
        
        while i < len(instructions):
            current = instructions[i]
            
            if i + 1 < len(instructions):
                next_instr = instructions[i + 1]
                
                if (current.opcode == "TURN" and next_instr.opcode == "TURN"):
                    if ((current.operand == "LEFT" and next_instr.operand == "RIGHT") or
                        (current.operand == "RIGHT" and next_instr.operand == "LEFT")):
                        print(f"    Canceling TURN {current.operand} + TURN {next_instr.operand}")
                        i += 2
                        continue
            
            optimized.append(current)
            i += 1
        
        return optimized
    
    def remove_full_rotations(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Remove four consecutive identical turns (360-degree rotation)"""
        if len(instructions) < 4:
            return instructions
        
        optimized = []
        i = 0
        
        while i < len(instructions):
            current = instructions[i]
            
            if current.opcode == "TURN" and i + 3 < len(instructions):
                # Check if next 3 are identical turns
                if all(
                    instructions[i + j].opcode == "TURN" and 
                    instructions[i + j].operand == current.operand
                    for j in range(1, 4)
                ):
                    print(f"    Removing full rotation: 4x TURN {current.operand}")
                    i += 4
                    continue
            
            optimized.append(current)
            i += 1
        
        return optimized


def optimize(instructions: List[IRInstruction]) -> List[IRInstruction]:
    """Convenience function to optimize IR"""
    optimizer = Optimizer(instructions)
    return optimizer.optimize()
