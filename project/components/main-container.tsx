"use client";

import React from 'react';
import Header from './header';
import InputSection from './input-section';
import ChatSection from './chat-section';
import { useRagChat } from '@/hooks/use-rag-chat';

const MainContainer: React.FC = () => {
  const {
    youtubeUrl,
    apiKey,
    isInitializing,
    isInitialized,
    initializationError,
    messages,
    currentMessage,
    isProcessing,
    setYoutubeUrl,
    setApiKey,
    setCurrentMessage,
    handleInitialize,
    handleSendMessage,
    handleClearSession,
  } = useRagChat();

  return (
    <div className="max-w-3xl mx-auto">
      <Header />
      
      <InputSection 
        youtubeUrl={youtubeUrl}
        apiKey={apiKey}
        isInitializing={isInitializing}
        isInitialized={isInitialized}
        initializationError={initializationError}
        setYoutubeUrl={setYoutubeUrl}
        setApiKey={setApiKey}
        handleInitialize={handleInitialize}
      />
      
      <ChatSection 
        messages={messages}
        currentMessage={currentMessage}
        isProcessing={isProcessing}
        isInitialized={isInitialized}
        setCurrentMessage={setCurrentMessage}
        handleSendMessage={handleSendMessage}
        handleClearSession={handleClearSession}
      />
    </div>
  );
};

export default MainContainer;