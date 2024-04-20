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

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");

  const sendMessage = (text) => {
    if (!text.trim()) return;
    const messageModel = { message: text, direction: "outgoing" };
    setMessages([...messages, messageModel]);
    setInputValue("");
    // Here you would also handle sending the message to your backend or chatbot service
  };

  return (
    <div style={{ height: "120vh", width: "100vw" }}>
      <MainContainer responsive className="my-chat-container">
        <ChatContainer>
          <MessageList>
            {messages.map((msg, index) => (
              <Message key={index} model={msg} />
            ))}
          </MessageList>
          <MessageInput 
            placeholder="Type message here..."
            value={inputValue} 
            onChange={setInputValue}
            onSend={() => sendMessage(inputValue)} 
            style={{ backgroundColor: '#fff', color: '#fff' }}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
}


export default ChatPage;