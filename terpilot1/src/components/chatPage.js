import React, { useState, useEffect, useRef} from 'react';
import {useLoadScript} from '@react-google-maps/api'; // Import the useLoadScript hook
import { 
  MainContainer, 
  ChatContainer, 
  MessageList, 
  Message, 
  MessageInput,
  ConversationHeader 
} from '@chatscope/chat-ui-kit-react';
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import '../App.css'; 
import './ChatPage.css';
import sendIcon from "../pages/sendIcon.png"; // Import the send icon
import MapComponent from './MapComponents';
import Calendar from './Calendar';


function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false); // Define the loading state
  const [mapLocations, setMapLocations] = useState([]);
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: "AIzaSyA0Rb9lOy66_3hIcrfcduzGzqC2ajlQc6k"
  });
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessageToBackend = async (messageContent) => {
    // Immediately update the outgoing message
    setMessages(prevMessages => [...prevMessages, { content: messageContent, direction: "outgoing" }]);
  
    // Fetch data from backend
    const response = await fetch('http://104.131.173.76:5000/getresponse', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: messageContent })
    });
  
    // Check if response is OK and then process data
    if (response.ok) {
      const data = await response.json();
      setMessages(prevMessages => {
        // Copy previous messages and handle new data
        let newMessages = [...prevMessages];
        if (data.type === "text-data") {
          newMessages.push({ content: data.message, direction: "incoming" });
        } else if (data.type === "geo-data") {
          newMessages.push({ content: "geo-data", direction: "incoming" });
          setMapLocations(data.message);
        } else if (data.type === "schedule-data") {
          newMessages.push({ content: "schedule-data", direction: "incoming" });
          setScheduleData(data.schedule);
        }
        return newMessages;
      });
    } else {
      // Handle errors by adding an error message to chat
      setMessages(prevMessages => [...prevMessages, { content: "Error sending message", direction: "incoming" }]);
    }
  };
  

  const sendMessage = () => {
    if (!inputValue.trim()) return;
    setLoading(true);
    sendMessageToBackend(inputValue);
    setInputValue(""); // Clear the input after sending
    setLoading(false); // Turn this false when done
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevents the default action of Enter key
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message-bubble ${msg.direction === "outgoing" ? "outgoing" : "incoming"}`}>
            {msg.content === "geo-data" ? <MapComponent locations={mapLocations} /> :
             msg.content === "schedule-data" ? <Calendar schedule={scheduleData} /> : msg.content}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type something..."
          className="message-input"
          rows={1}
        />
        <button onClick={sendMessage} disabled={loading}>
          <img src={sendIcon} alt="Send" className="send-button-icon" />
        </button>
      </div>
    </div>
  );
}

export default ChatPage;