
import React, { useState, useRef, useEffect } from 'react';
import SendIcon from './icons/SendIcon';

interface InputBarProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const InputBar: React.FC<InputBarProps> = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-3">
      <textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
          }
        }}
        placeholder="Type your answer here..."
        className="flex-1 bg-gray-100 dark:bg-gray-900 border border-gray-300 dark:border-gray-600 rounded-lg py-2 px-4 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800 dark:text-gray-200 max-h-40 overflow-y-auto"
        rows={1}
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading || !input.trim()}
        className="p-2 rounded-full bg-blue-600 text-white disabled:bg-gray-400 disabled:cursor-not-allowed hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75 transition-colors self-end"
      >
        <SendIcon className="w-5 h-5" />
      </button>
    </form>
  );
};

export default InputBar;