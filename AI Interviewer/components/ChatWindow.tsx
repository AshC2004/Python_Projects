
import React, { useEffect, useRef } from 'react';
import { Message } from '../types';
import MessageBubble from './Message';
import InputBar from './InputBar';

interface ChatWindowProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  error: string | null;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, onSendMessage, isLoading, error }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex flex-col h-full">
      <header className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h1 className="text-xl font-bold text-gray-800 dark:text-gray-200">Excel Interview</h1>
      </header>
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}
        {isLoading && (
           <MessageBubble message={{ role: 'model', content: '' }} />
        )}
        <div ref={messagesEndRef} />
      </div>
      {error && <p className="px-6 pb-2 text-sm text-red-500">{error}</p>}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <InputBar onSendMessage={onSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default ChatWindow;