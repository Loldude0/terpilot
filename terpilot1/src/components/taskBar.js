import React from 'react';
import { useNavigate } from 'react-router-dom';
import './TaskBar.css'; // Import CSS for styling

function TaskBar() {
  const navigate = useNavigate();

  return (
    <div className="task-bar">
      <div className="logo">TerpPilot</div>
      <div>
        <button className="task-bar-button" onClick={() => navigate("/schedulebuilding")}>Schedule Building</button>
        <span>Welcome Pranav</span>
        <button className="task-bar-button"><i className="icon-settings"></i></button>
      </div>
    </div>
  );
}

export default TaskBar;