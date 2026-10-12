"""
Quick test script to verify the compiler works correctly
Run: python test_compiler.py
"""

from grammar.grammar_parser import load_grammar
from phases.phase1_lexer import tokenize
from phases.phase2_parser import parse
from phases.phase3_semantic import analyze
from phases.phase4_ir_generator import generate_ir_objects
from phases.phase5_optimizer import optimize
from phases.phase6_code_generator import generate_code

# Test program
test_code = """MOVE 3;
TURN RIGHT;
REPEAT 2 {
    MOVE 1;
    TURN LEFT;
}
MOVE 2;"""

print("Testing RoboScript Compiler")
print("=" * 60)

# Load grammar
grammar = load_grammar("grammar/roboscript_grammar.txt")
print("[OK] Grammar loaded")

# Phase 1: Lexical Analysis
tokens = tokenize(test_code, grammar)
print(f"[OK] Phase 1 complete: {len(tokens)} tokens")

# Phase 2: Syntax Analysis
ast = parse(tokens, grammar)
print(f"[OK] Phase 2 complete: AST built")

# Phase 3: Semantic Analysis
analyze(ast, grammar)
print(f"[OK] Phase 3 complete: Semantics validated")

# Phase 4: IR Generation
ir_instructions = generate_ir_objects(ast, grammar)
print(f"[OK] Phase 4 complete: {len(ir_instructions)} IR instructions")

# Phase 5: Optimization
optimized = optimize(ir_instructions)
print(f"[OK] Phase 5 complete: {len(optimized)} optimized instructions")

# Phase 6: Code Generation
target_code = generate_code(optimized)
print(f"[OK] Phase 6 complete: {len(target_code)} target instructions")

print("\n" + "=" * 60)
print("FINAL OUTPUT:")
print("-" * 60)
for i, instr in enumerate(target_code):
    print(f"[{i}] {instr['opcode']} {instr['operand']}")
print("=" * 60)

# Verify expected output
print("\nVERIFICATION:")
if len(target_code) >= 5:  # At least MOVE, TURN, MOVE (merged), TURN, TURN, MOVE
    print(f"[OK] Generated {len(target_code)} instructions")
else:
    print(f"[FAIL] Expected at least 5 instructions, got {len(target_code)}")

if len(target_code) > 0 and target_code[0]['opcode'] == 'MOVE' and target_code[0]['operand'] == 3:
    print("[OK] First instruction correct: MOVE 3")
else:
    print("[FAIL] First instruction wrong")

if len(target_code) > 1 and target_code[1]['opcode'] == 'TURN' and target_code[1]['operand'] == 'RIGHT':
    print("[OK] Second instruction correct: TURN RIGHT")
else:
    print("[FAIL] Second instruction wrong or missing")

turn_left_count = sum(1 for instr in target_code if instr['opcode'] == 'TURN' and instr['operand'] == 'LEFT')
if turn_left_count >= 2:
    print(f"[OK] TURN LEFT instructions present ({turn_left_count} times)")
else:
    print(f"[FAIL] Expected at least 2 TURN LEFT, got {turn_left_count}")

print("\nTest complete!")
