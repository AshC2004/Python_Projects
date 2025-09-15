
import React from 'react';
import { Message } from '../types';
import BotIcon from './icons/BotIcon';
import UserIcon from './icons/UserIcon';

interface MessageProps {
  message: Message;
}

const MessageBubble: React.FC<MessageProps> = ({ message }) => {
  const isModel = message.role === 'model';
  const isLoading = isModel && !message.content;

  return (
    <div className={`flex items-start gap-3 ${isModel ? 'justify-start' : 'justify-end'}`}>
      {isModel && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
          <BotIcon className="w-5 h-5 text-gray-600 dark:text-gray-300"/>
        </div>
      )}
      <div
        className={`max-w-md lg:max-w-lg px-4 py-3 rounded-2xl ${
          isModel
            ? 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-tl-none'
            : 'bg-blue-600 text-white rounded-br-none'
        }`}
      >
        {isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
          </div>
        ) : (
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        )}
      </div>
      {!isModel && (
         <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center">
          <UserIcon className="w-5 h-5 text-blue-600 dark:text-blue-400" />
        </div>
      )}
    </div>
  );
};

export default MessageBubble;