import React, { useState, useEffect } from "react";
import "./RobotSimulator.css";

const GRID_SIZE = 10;
const CELL_SIZE = 50;

const DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"];
const DIRECTION_ARROWS = {
  NORTH: "▲",
  EAST: "▶",
  SOUTH: "▼",
  WEST: "◀",
};

function RobotSimulator({ instructions }) {
  const [robotPos, setRobotPos] = useState({ x: 5, y: 5 });
  const [robotDir, setRobotDir] = useState("NORTH");
  const [currentStep, setCurrentStep] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [executionLog, setExecutionLog] = useState([]);
  const [speed, setSpeed] = useState(500);

  const initialState = { x: 5, y: 5, dir: "NORTH" };

  // Auto-execute next step when running
  useEffect(() => {
    if (!isRunning || !instructions || currentStep >= instructions.length) {
      if (isRunning && currentStep >= instructions.length) {
        setIsRunning(false);
      }
      return;
    }

    const timer = setTimeout(() => {
      executeStep();
    }, speed);

    return () => clearTimeout(timer);
  }, [isRunning, currentStep]);

  const reset = () => {
    setRobotPos({ x: initialState.x, y: initialState.y });
    setRobotDir(initialState.dir);
    setCurrentStep(0);
    setIsRunning(false);
    setExecutionLog([]);
  };

  const executeStep = () => {
    if (!instructions || currentStep >= instructions.length) {
      setIsRunning(false);
      return;
    }

    const instruction = instructions[currentStep];
    const log = `[${currentStep}] ${instruction.opcode} ${instruction.operand || ""}`;

    if (instruction.opcode === "MOVE") {
      const distance = instruction.operand;
      const newPos = move(robotPos, robotDir, distance);

      if (newPos.outOfBounds) {
        setExecutionLog((prev) => [
          ...prev,
          `${log} - OUT OF BOUNDS! Stopped.`,
        ]);
        setIsRunning(false);
        return;
      }

      setRobotPos(newPos);
      setExecutionLog((prev) => [...prev, log]);
    } else if (instruction.opcode === "TURN") {
      const direction = instruction.operand;
      const newDir = turn(robotDir, direction);
      setRobotDir(newDir);
      setExecutionLog((prev) => [...prev, log]);
    }

    setCurrentStep((prev) => prev + 1);
  };

  const move = (pos, dir, distance) => {
    let newX = pos.x;
    let newY = pos.y;

    switch (dir) {
      case "NORTH":
        newY -= distance;
        break;
      case "EAST":
        newX += distance;
        break;
      case "SOUTH":
        newY += distance;
        break;
      case "WEST":
        newX -= distance;
        break;
    }

    if (newX < 0 || newX >= GRID_SIZE || newY < 0 || newY >= GRID_SIZE) {
      return { x: pos.x, y: pos.y, outOfBounds: true };
    }

    return { x: newX, y: newY };
  };

  const turn = (currentDir, turnDir) => {
    const currentIndex = DIRECTIONS.indexOf(currentDir);
    let newIndex;

    if (turnDir === "LEFT") {
      newIndex = (currentIndex - 1 + DIRECTIONS.length) % DIRECTIONS.length;
    } else {
      newIndex = (currentIndex + 1) % DIRECTIONS.length;
    }

    return DIRECTIONS[newIndex];
  };

  const handleRun = () => {
    if (!instructions || instructions.length === 0) {
      return;
    }

    if (currentStep >= instructions.length) {
      reset();
      return;
    }

    setIsRunning(true);
  };

  const handlePause = () => {
    setIsRunning(false);
  };

  const handleStep = () => {
    if (!isRunning) {
      executeStep();
    }
  };

  return (
    <div className="robot-simulator-panel">
      <div className="panel-header">
        <h2>🤖 Robot Simulator</h2>
      </div>

      <div className="simulator-content">
        <div className="grid-container">
          <svg width={GRID_SIZE * CELL_SIZE} height={GRID_SIZE * CELL_SIZE}>
            {/* Grid lines */}
            {Array.from({ length: GRID_SIZE + 1 }).map((_, i) => (
              <g key={i}>
                <line
                  x1={0}
                  y1={i * CELL_SIZE}
                  x2={GRID_SIZE * CELL_SIZE}
                  y2={i * CELL_SIZE}
                  stroke="#ddd"
                  strokeWidth="1"
                />
                <line
                  x1={i * CELL_SIZE}
                  y1={0}
                  x2={i * CELL_SIZE}
                  y2={GRID_SIZE * CELL_SIZE}
                  stroke="#ddd"
                  strokeWidth="1"
                />
              </g>
            ))}

            {/* Robot */}
            <g
              transform={`translate(${robotPos.x * CELL_SIZE + CELL_SIZE / 2}, ${robotPos.y * CELL_SIZE + CELL_SIZE / 2})`}
            >
              <circle r="18" fill="#667eea" />
              <text textAnchor="middle" dy="7" fontSize="24" fill="white">
                {DIRECTION_ARROWS[robotDir]}
              </text>
            </g>
          </svg>
        </div>

        <div className="robot-info">
          <div className="info-item">
            <strong>Position:</strong> ({robotPos.x}, {robotPos.y})
          </div>
          <div className="info-item">
            <strong>Direction:</strong> {robotDir}
          </div>
          <div className="info-item">
            <strong>Step:</strong> {currentStep} / {instructions?.length || 0}
          </div>
        </div>

        <div className="simulator-controls">
          <button
            onClick={handleRun}
            disabled={!instructions || instructions.length === 0 || isRunning}
            className="btn btn-primary"
          >
            ▶ Run
          </button>
          <button
            onClick={handlePause}
            disabled={!isRunning}
            className="btn btn-secondary"
          >
            ⏸ Pause
          </button>
          <button
            onClick={handleStep}
            disabled={
              !instructions ||
              instructions.length === 0 ||
              isRunning ||
              currentStep >= instructions.length
            }
            className="btn btn-secondary"
          >
            ⏭ Step
          </button>
          <button onClick={reset} className="btn btn-secondary">
            🔄 Reset
          </button>
          <div className="speed-control">
            <label>Speed:</label>
            <input
              type="range"
              min="100"
              max="1000"
              step="100"
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
              disabled={isRunning}
            />
            <span>{speed}ms</span>
          </div>
        </div>

        <div className="execution-log">
          <h3>Execution Log</h3>
          <div className="log-content">
            {executionLog.length === 0 ? (
              <div className="log-empty">
                No execution yet. Compile code and press Run.
              </div>
            ) : (
              executionLog.map((log, i) => (
                <div key={i} className="log-item">
                  {log}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default RobotSimulator;
