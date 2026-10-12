"""
RoboScript Compiler Backend
Grammar-driven compiler with detailed phase logging
"""

import sys
import io
from contextlib import redirect_stdout
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from grammar.grammar_parser import load_grammar
from phases.phase1_lexer import tokenize, LexerError
from phases.phase2_parser import parse, ParserError
from phases.phase3_semantic import analyze, SemanticError
from phases.phase4_ir_generator import generate_ir_objects
from phases.phase5_optimizer import optimize
from phases.phase6_code_generator import generate_code


app = FastAPI(
    title="RoboScript Compiler",
    description="Grammar-driven compiler for RoboScript robot programming language",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load grammar at startup
GRAMMAR_FILE = "grammar/roboscript_grammar.txt"
grammar = None

@app.on_event("startup")
async def startup_event():
    global grammar
    print("=" * 60)
    print("ROBO SCRIPT COMPILER - GRAMMAR-DRIVEN")
    print("=" * 60)
    grammar = load_grammar(GRAMMAR_FILE)
    print(f"✓ Grammar loaded from {GRAMMAR_FILE}")
    print(f"  Start symbol: {grammar.start_symbol}")
    print(f"  Terminals: {len(grammar.terminals)}")
    print(f"  Non-terminals: {len(grammar.non_terminals)}")
    print(f"  Production rules: {len(grammar.production_rules)}")
    print("=" * 60)
    print()


class CompileRequest(BaseModel):
    code: str = Field(..., description="RoboScript source code")


class CompileError(BaseModel):
    phase: str
    message: str
    line: int
    column: int


class CompileResponse(BaseModel):
    success: bool
    instructions: Optional[List[Dict[str, Any]]] = None
    error: Optional[CompileError] = None
    compilation_log: Optional[str] = None


@app.get("/")
async def root():
    return {
        "message": "RoboScript Grammar-Driven Compiler",
        "version": "2.0.0",
        "grammar_file": GRAMMAR_FILE,
        "endpoints": {
            "compile": "/compile",
            "grammar": "/grammar"
        }
    }


@app.get("/grammar")
async def get_grammar():
    """Return the current grammar configuration"""
    return {
        "start_symbol": grammar.start_symbol,
        "terminals": list(grammar.terminals.keys()),
        "non_terminals": list(grammar.non_terminals.keys()),
        "production_rules": [str(rule) for rule in grammar.production_rules],
        "semantic_rules": grammar.semantic_rules
    }


@app.post("/compile", response_model=CompileResponse)
async def compile_code(request: CompileRequest):
    """
    Compile RoboScript through all 6 phases with detailed logging
    """
    
    # Capture all print output
    log_buffer = io.StringIO()
    
    try:
        with redirect_stdout(log_buffer):
            print("\n" + "=" * 60)
            print("COMPILATION STARTED")
            print("=" * 60)
            print(f"Source code length: {len(request.code)} characters")
            print()
            
            # Phase 1: Lexical Analysis
            tokens = tokenize(request.code, grammar)
            
            # Phase 2: Syntax Analysis
            ast = parse(tokens, grammar)
            
            # Phase 3: Semantic Analysis
            analyze(ast, grammar)
            
            # Phase 4: IR Generation
            ir_instructions = generate_ir_objects(ast, grammar)
            
            # Phase 5: Optimization
            optimized_instructions = optimize(ir_instructions)
            
            # Phase 6: Code Generation
            target_code = generate_code(optimized_instructions)
            
            print("=" * 60)
            print("COMPILATION SUCCESSFUL")
            print("=" * 60)
            print(f"Final instruction count: {len(target_code)}")
            print("=" * 60)
        
        compilation_log = log_buffer.getvalue()
        
        return CompileResponse(
            success=True,
            instructions=target_code,
            error=None,
            compilation_log=compilation_log
        )
    
    except LexerError as e:
        compilation_log = log_buffer.getvalue()
        return CompileResponse(
            success=False,
            instructions=None,
            error=CompileError(
                phase="lexical_analysis",
                message=e.message,
                line=e.line,
                column=e.column
            ),
            compilation_log=compilation_log
        )
    
    except ParserError as e:
        compilation_log = log_buffer.getvalue()
        return CompileResponse(
            success=False,
            instructions=None,
            error=CompileError(
                phase="syntax_analysis",
                message=e.message,
                line=e.line,
                column=e.column
            ),
            compilation_log=compilation_log
        )
    
    except SemanticError as e:
        compilation_log = log_buffer.getvalue()
        return CompileResponse(
            success=False,
            instructions=None,
            error=CompileError(
                phase="semantic_analysis",
                message=e.message,
                line=e.line,
                column=e.column
            ),
            compilation_log=compilation_log
        )
    
    except Exception as e:
        compilation_log = log_buffer.getvalue()
        return CompileResponse(
            success=False,
            instructions=None,
            error=CompileError(
                phase="unknown",
                message=f"Unexpected error: {str(e)}",
                line=0,
                column=0
            ),
            compilation_log=compilation_log
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
