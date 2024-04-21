import React from 'react';
import { useNavigate } from 'react-router-dom';
import './taskBar.css'; // Import CSS for styling
import turtleLogo from './turtle-svgrepo-com.png'; // Import Turtle Logo image

function TaskBar() {
  const navigate = useNavigate();

  return (
    <div className="task-bar">
      <div className="logo">
        TerPilot
        <img src={turtleLogo} alt="Turtle Logo" style={{ marginLeft: '10px', width: '45px', height: '45px' }} />
      </div>
      <div>
        <button className="task-bar-button" onClick={() => navigate("/schedulebuilding")}>View Schedules</button>
        <span>Welcome Pranav</span>
        <button className="task-bar-button"><i className="icon-settings"></i></button>
      </div>
    </div>
  );
}

export default TaskBar;