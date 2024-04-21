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
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false); // Define the loading state
  const [mapLocations, setMapLocations] = useState([]);
  const [scheduleData, setScheduleData] = useState([]);
  const {isLoaded, loadError} = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
  });
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessageToBackend = async (messageContent) => {
    // Uncomment the following lines and replace with your backend endpoint
    console.log("sending to backend")
    const response = await fetch('http://104.131.173.76:5000/getresponse', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: messageContent })
    });
    console.log(messages)
    const user_message = { content: messageContent, direction: "outgoing" };
    let new_messages = [...messages, user_message];
    setMessages(new_messages);
    
    if (response.ok) {
      const data = await response.json();
      console.log(data);
      if (data.type === "text-data"){
        setMessages([...new_messages, { content: data.message, direction: "incoming" }]);
      } else if (data.type === "geo-data") {
        setMessages([...new_messages, { content: "geo-data", direction: "incoming" }]);
        // data.message = [{"name":"251 North", "lng": -76.9496090325357, "lat": 38.99274005}, {"name": "94th Aero Squadron", "lng": -76.9210122711411, "lat": 38.9781702}]
        setMapLocations(data.message);  
      } else if (data.type === "schedule-data") {
        setMessages([...new_messages, { content: "schedule-data", direction: "incoming" }]);
        setScheduleData(data.message)

      } else {
        console.log("error");
      }
      // Handle the response data as needed...
    } else {
      // Handle errors...
      setMessages([...messages, { content: "Error sending message", direction: "incoming" }]);
    }
  };
  
  const sendMessage = () => {
    if (!inputValue.trim()) return;
    setLoading(true); // You would turn this true when sending starts
    
    setMessages(prevMessages => [...prevMessages, { content: inputValue, direction: "outgoing" }]);
    setInputValue(""); // Clear the input after sending
    sendMessageToBackend(inputValue); // Call the function to send the message to the backend
    setLoading(false); // You would turn this true when sending starts and then back to false when done
  };
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { // Added check for shiftKey
      e.preventDefault(); // Prevents the default action of Enter key (new line)
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => 
          msg.direction === "incoming" ? (
            <div key={index} className={`message-bubble incoming`}>
              {msg.content === "geo-data" ? <MapComponent locations={mapLocations} /> :
              msg.content === "schedule-data" ? <Calendar schedule={scheduleData} />: msg.content}
            </div>
          ) : (
            <div key={index} className={`message-bubble outgoing`}>
              {msg.content}
            </div>
          )
        )}
        <div className="bottom-ref" ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown} // Added onKeyDown event handler
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