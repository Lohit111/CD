import React, { useState } from 'react'
import './CodeEditor.css'

const SAMPLE_PROGRAM = `MOVE 3;
TURN RIGHT;
REPEAT 2 {
    MOVE 1;
    TURN LEFT;
}
MOVE 2;`;

function CodeEditor({ onCompile, isCompiling, compiledInstructions, compilationError }) {
  const [code, setCode] = useState(SAMPLE_PROGRAM)
  const [showLog, setShowLog] = useState(false)
  const [compilationLog, setCompilationLog] = useState('')

  const handleCompile = async () => {
    const log = await onCompile(code)
    if (log) {
      setCompilationLog(log)
      setShowLog(true)
    }
  }

  return (
    <div className="code-editor-panel">
      <div className="panel-header">
        <h2>📝 Code Editor</h2>
      </div>

      <div className="editor-controls">
        <button
          onClick={() => setCode(SAMPLE_PROGRAM)}
          className="btn btn-secondary"
          disabled={isCompiling}
        >
          Load Sample
        </button>
        <button
          onClick={() => setCode('')}
          className="btn btn-secondary"
          disabled={isCompiling}
        >
          Clear
        </button>
        <button
          onClick={handleCompile}
          className="btn btn-primary"
          disabled={isCompiling}
        >
          {isCompiling ? 'Compiling...' : '⚙️ Compile'}
        </button>
        {compilationLog && (
          <button
            onClick={() => setShowLog(!showLog)}
            className="btn btn-secondary"
          >
            {showLog ? 'Hide Log' : 'Show Compilation Log'}
          </button>
        )}
      </div>

      <textarea
        className="code-textarea"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Write your RoboScript code here..."
        spellCheck={false}
      />

      <div className="compilation-output">
        <h3>Compilation Output</h3>

        {isCompiling && (
          <div className="status-message info">
            Compiling through all 6 phases...
          </div>
        )}

        {compilationError && (
          <div className="status-message error">
            <strong>❌ Compilation Failed</strong>
            <p><strong>Phase:</strong> {compilationError.phase}</p>
            <p><strong>Error:</strong> {compilationError.message}</p>
            <p><strong>Location:</strong> Line {compilationError.line}, Column {compilationError.column}</p>
          </div>
        )}

        {compiledInstructions && !compilationError && (
          <div className="status-message success">
            <strong>✅ Compilation Successful</strong>
            <p><strong>Instructions Generated:</strong> {compiledInstructions.length}</p>
            <div className="instructions-list">
              <h4>Target Instructions:</h4>
              {compiledInstructions.map((instr, i) => (
                <div key={i} className="instruction-item">
                  [{i.toString().padStart(3, '0')}] {instr.opcode} {instr.operand}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {showLog && compilationLog && (
        <div className="compilation-log-modal" onClick={() => setShowLog(false)}>
          <div className="compilation-log-content" onClick={(e) => e.stopPropagation()}>
            <div className="log-header">
              <h3>📋 Compilation Log (All 6 Phases)</h3>
              <button onClick={() => setShowLog(false)} className="close-btn">✕</button>
            </div>
            <pre className="compilation-log">{compilationLog}</pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default CodeEditor
