
import React from 'react';
import BotIcon from './icons/BotIcon';

interface WelcomeScreenProps {
  onStart: () => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onStart }) => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-8 bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200">
      <div className="w-20 h-20 mb-6 bg-blue-100 dark:bg-blue-900/50 rounded-full flex items-center justify-center">
        <BotIcon className="w-12 h-12 text-blue-600 dark:text-blue-400" />
      </div>
      <h1 className="text-3xl font-bold mb-2">Excel Mock Interview</h1>
      <p className="max-w-md mb-8 text-gray-600 dark:text-gray-400">
        Test your Microsoft Excel knowledge with our automated interviewer. Get instant feedback and identify areas for improvement.
      </p>
      <button
        onClick={onStart}
        className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75 transition-transform transform hover:scale-105"
      >
        Start Interview
      </button>
    </div>
  );
};

export default WelcomeScreen;
