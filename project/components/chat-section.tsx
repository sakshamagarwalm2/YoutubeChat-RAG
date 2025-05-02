"use client";

import React, { useEffect, useRef } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { MessageSquare, Send, Loader2, Trash2 } from 'lucide-react';
import { Message } from '@/types/message';
import ChatMessage from './chat-message';

interface ChatSectionProps {
  messages: Message[];
  currentMessage: string;
  isProcessing: boolean;
  isInitialized: boolean;
  setCurrentMessage: (message: string) => void;
  handleSendMessage: () => Promise<void>;
  handleClearSession: () => Promise<void>;
}

const ChatSection: React.FC<ChatSectionProps> = ({
  messages,
  currentMessage,
  isProcessing,
  isInitialized,
  setCurrentMessage,
  handleSendMessage,
  handleClearSession,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentMessage.trim() || isProcessing || !isInitialized) return;
    await handleSendMessage();
    inputRef.current?.focus();
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden flex flex-col transition-all duration-300">
      <div className="p-4 bg-gray-50 border-b border-gray-100 flex justify-between items-center">
        <div className="flex items-center">
          <MessageSquare className="h-5 w-5 text-gray-500 mr-2" />
          <h2 className="font-medium text-gray-800">Chat</h2>
        </div>
        <Button
          variant="ghost"
          size="sm"
          className="text-gray-500 hover:text-red-500"
          onClick={handleClearSession}
          disabled={!isInitialized || messages.length === 0}
        >
          <Trash2 className="h-4 w-4 mr-1" />
          Clear Session
        </Button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[400px] max-h-[500px]">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-400">
            <MessageSquare className="h-12 w-12 mb-2 opacity-20" />
            <p className="text-center">
              {isInitialized 
                ? "Ask a question about the video" 
                : "Initialize the RAG pipeline to start chatting"}
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={onSubmit} className="p-4 border-t border-gray-100 flex gap-2">
        <Input
          ref={inputRef}
          type="text"
          placeholder={isInitialized ? "Ask a question about the video..." : "Initialize the RAG pipeline first..."}
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          className="flex-1 border-gray-200 focus:border-amber-400"
          disabled={!isInitialized || isProcessing}
        />
        <Button 
          type="submit" 
          disabled={!isInitialized || isProcessing || !currentMessage.trim()}
          className="bg-blue-500 hover:bg-blue-600 text-white"
        >
          {isProcessing ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </Button>
      </form>
    </div>
  );
};

export default ChatSection;