import React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { cn } from '@/lib/utils';
import { Message } from '@/types/message';
import { User, Bot } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const formattedTime = formatDistanceToNow(new Date(message.timestamp), { 
    addSuffix: true,
    includeSeconds: true
  });

  return (
    <div
      className={cn(
        "flex w-full", 
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "flex max-w-[80%] gap-2 rounded-lg p-4",
          isUser 
            ? "bg-blue-500 text-white" 
            : "bg-gray-100 text-gray-800"
        )}
      >
        <div className={cn(
          "self-start mt-1", 
          isUser ? "order-last ml-2" : "mr-2"
        )}>
          {isUser ? (
            <User className="h-4 w-4" />
          ) : (
            <Bot className="h-4 w-4" />
          )}
        </div>
        
        <div className="flex flex-col gap-1">
          <div className="break-words">{message.content}</div>
          <div 
            className={cn(
              "text-xs",
              isUser ? "text-blue-100" : "text-gray-500"
            )}
          >
            {formattedTime}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;