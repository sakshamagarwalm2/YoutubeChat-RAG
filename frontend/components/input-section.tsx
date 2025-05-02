"use client";

import React from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface InputSectionProps {
  youtubeUrl: string;
  apiKey: string;
  isInitializing: boolean;
  isInitialized: boolean;
  initializationError: string | null;
  setYoutubeUrl: (url: string) => void;
  setApiKey: (key: string) => void;
  handleInitialize: () => Promise<void>;
}

const InputSection: React.FC<InputSectionProps> = ({
  youtubeUrl,
  apiKey,
  isInitializing,
  isInitialized,
  initializationError,
  setYoutubeUrl,
  setApiKey,
  handleInitialize,
}) => {
  const { toast } = useToast();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await handleInitialize();
      if (!initializationError) {
        toast({
          title: "Success!",
          description: "RAG pipeline initialized successfully.",
          variant: "success",
        });
      }
    } catch (error) {
      console.error("Initialization error:", error);
    }
  };

  return (
    <div className="bg-[#F5EFE1] rounded-lg p-6 mb-6 shadow-sm border border-amber-100 transition-all duration-300 ease-in-out">
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <Input
            type="text"
            placeholder="Enter YouTube URL (e.g., https://www.youtube.com/watch?v=DbgvDGtjkEA)"
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            className="bg-white border-gray-200 focus:border-amber-400 px-4 py-3 rounded-md"
            disabled={isInitializing || isInitialized}
            required
          />
        </div>
        
        <div>
          <Input
            type="password"
            placeholder="Enter your Groq API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="bg-white border-gray-200 focus:border-amber-400 px-4 py-3 rounded-md"
            disabled={isInitializing || isInitialized}
            required
          />
        </div>
        
        <div className="flex justify-center">
          <Button
            type="submit"
            disabled={isInitializing || isInitialized || !youtubeUrl || !apiKey}
            className={`bg-amber-500 hover:bg-amber-600 text-white px-6 py-2 rounded-md transition-colors duration-300
              ${isInitialized ? 'bg-green-500 hover:bg-green-500 cursor-default' : ''}`}
          >
            {isInitializing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Initializing...
              </>
            ) : isInitialized ? (
              'RAG Pipeline Initialized'
            ) : (
              'Initialize RAG Pipeline'
            )}
          </Button>
        </div>
        
        {initializationError && (
          <div className="text-red-500 text-sm text-center mt-2 animate-fadeIn">
            Error: {initializationError}
          </div>
        )}
      </form>
    </div>
  );
};

export default InputSection;