import React, { useState } from 'react';
import './ChatPage.css'; // Make sure your CSS is correctly linked
import sendIcon from '../pages/sendButton.png'; // Check the path is correct

function ChatPage() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return; // Prevent sending empty messages
    setLoading(true);

    // Prepare the data to send in the request
    const dataToSend = {
      message: message
    };

    try {
      // HTTP request to the backend
      const response = await fetch('http://127.0.0.1:5000/getresponse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      } else {
        // Optionally handle the response data
        const responseData = await response.json();
        console.log('Message sent successfully:', responseData);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setMessage(''); // Clear the message after attempt to send (success or fail)
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

export default ChatPage;