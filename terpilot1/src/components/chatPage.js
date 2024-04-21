import React, { useState } from 'react';
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

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false); // Define the loading state

  const sendMessageToBackend = async (messageContent) => {
    // Uncomment the following lines and replace with your backend endpoint
    console.log("sending to backend")
    const response = await fetch('http://127.0.0.1:5000/getresponse', {
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
      setMessages([...new_messages, { content: data.message, direction: "incoming" }]);
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
        {messages.map((msg, index) => (
          <div key={index} className={`message-bubble ${msg.direction === "outgoing" ? "outgoing" : "incoming"}`}>
            {msg.content}
          </div>
        ))}
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