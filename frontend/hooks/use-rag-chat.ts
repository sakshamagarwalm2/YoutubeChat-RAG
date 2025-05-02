"use client";

import { useState, useEffect } from 'react';
import { useToast } from './use-toast';
import { Message } from '@/types/message';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';

export const useRagChat = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isInitializing, setIsInitializing] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [initializationError, setInitializationError] = useState<string | null>(null);
  const { toast } = useToast();

  // Set up beforeunload event to clear session data when window is closed
  useEffect(() => {
    const handleBeforeUnload = async () => {
      if (isInitialized) {
        try {
          // Send a non-blocking request to clear the session
          navigator.sendBeacon(`${API_BASE_URL}/clear`);
        } catch (error) {
          console.error('Error clearing session on page unload:', error);
        }
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, [isInitialized]);

  const handleInitialize = async () => {
    if (!youtubeUrl || !apiKey) {
      setInitializationError('YouTube URL and API key are required');
      return;
    }

    setIsInitializing(true);
    setInitializationError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/initialize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          youtube_url: youtubeUrl,
          api_key: apiKey,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to initialize RAG pipeline');
      }

      setIsInitialized(true);
      // Add a system message to indicate successful initialization
      setMessages([
        {
          role: 'assistant',
          content: 'RAG pipeline initialized successfully. You can now ask questions about the video.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      console.error('Error initializing RAG pipeline:', error);
      setInitializationError(error instanceof Error ? error.message : 'Failed to initialize RAG pipeline');
    } finally {
      setIsInitializing(false);
    }
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || !isInitialized) return;

    // Add user message to chat
    const userMessage: Message = {
      role: 'user',
      content: currentMessage,
      timestamp: new Date().toISOString(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setCurrentMessage('');
    setIsProcessing(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userMessage.content,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get response');
      }

      // Add assistant message to chat
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
        timestamp: new Date().toISOString(),
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to chat
      const errorMessage: Message = {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to get response'}`,
        timestamp: new Date().toISOString(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
      
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : 'Failed to get response',
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClearSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/clear`, {
        method: 'POST',
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to clear session');
      }

      // Reset state
      setMessages([]);
      setCurrentMessage('');
      setIsInitialized(false);
      setYoutubeUrl('');
      setApiKey('');
      
      toast({
        title: "Success",
        description: "Session cleared successfully",
        variant: "success",
      });
    } catch (error) {
      console.error('Error clearing session:', error);
      
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : 'Failed to clear session',
        variant: "destructive",
      });
    }
  };

  return {
    youtubeUrl,
    apiKey,
    messages,
    currentMessage,
    isInitializing,
    isInitialized,
    isProcessing,
    initializationError,
    setYoutubeUrl,
    setApiKey,
    setCurrentMessage,
    handleInitialize,
    handleSendMessage,
    handleClearSession,
  };
};