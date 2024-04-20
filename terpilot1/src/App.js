import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatPage from './pages/ChatPage';
import ScheduleBuilding from './pages/ScheduleBuilding';
import TaskBar from './components/taskBar';

function App() {
  return (
    <Router>
      <div className="App">
        <TaskBar />
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/schedulebuilding" element={<ScheduleBuilding />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
