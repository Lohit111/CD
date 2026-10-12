import React, { useState } from "react";
import CodeEditor from "./components/CodeEditor";
import RobotSimulator from "./components/RobotSimulator";
import "./App.css";

const BACKEND_URL = "http://localhost:8000";

function App() {
  const [compiledInstructions, setCompiledInstructions] = useState(null);
  const [compilationError, setCompilationError] = useState(null);
  const [isCompiling, setIsCompiling] = useState(false);

  const handleCompile = async (code) => {
    setIsCompiling(true);
    setCompilationError(null);
    setCompiledInstructions(null);

    try {
      const response = await fetch(`${BACKEND_URL}/compile`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code }),
      });

      const data = await response.json();

      if (data.success) {
        setCompiledInstructions(data.instructions);
        setCompilationError(null);
        return data.compilation_log;
      } else {
        setCompilationError(data.error);
        setCompiledInstructions(null);
        return data.compilation_log;
      }
    } catch (error) {
      setCompilationError({
        phase: "network",
        message: `Failed to connect to backend: ${error.message}. Make sure backend is running on ${BACKEND_URL}`,
        line: 0,
        column: 0,
      });
      setCompiledInstructions(null);
      return null;
    } finally {
      setIsCompiling(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 RoboScript Compiler</h1>
        <p>
          Grammar-Driven Compiler Design Project - 6 Phases with Detailed
          Logging
        </p>
      </header>

      <div className="app-content">
        <CodeEditor
          onCompile={handleCompile}
          isCompiling={isCompiling}
          compiledInstructions={compiledInstructions}
          compilationError={compilationError}
        />

        <RobotSimulator instructions={compiledInstructions} />
      </div>
    </div>
  );
}

export default App;
