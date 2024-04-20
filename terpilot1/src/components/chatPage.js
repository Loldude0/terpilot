import React, { useState } from 'react';
import './ChatPage.css'; // Make sure your CSS is correctly linked
import sendIcon from '../pages/sendButton.png'; // Check the path is correct

function ChatPage() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return; // Prevent sending empty messages
    setLoading(true);

    // Simulate a backend call
    try {
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate a delay
      setMessage(''); // Clear the message after successful sending
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false); // Ensure loading is set to false after operation
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {/* Messages will be displayed here */}
      </div>
      {loading ? (
        <div className="loader">...</div>
      ) : (
        <div className="input-container">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type something ..."
            disabled={loading}
          />
          <button className="send-button" onClick={sendMessage} disabled={loading}>
            <img src={sendIcon} alt="Send" className="send-button-icon"/>
          </button>
        </div>
      )}
    </div>
  );
}

export default ChatPage;
