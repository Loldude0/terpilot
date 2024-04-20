import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatPage from './components/ChatPage';
import ScheduleBuilding from './pages/ScheduleBuilding';
import TaskBar from './components/taskBar';
import './App.css';

function App() {
  return (
    <Router>
      <TaskBar />
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/schedulebuilding" element={<ScheduleBuilding />} />
      </Routes>
    </Router>
  );
}

export default App;