
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface FeedbackReportProps {
  feedback: string;
  onRestart: () => void;
}

const FeedbackReport: React.FC<FeedbackReportProps> = ({ feedback, onRestart }) => {
  return (
    <div className="flex flex-col h-full">
        <header className="p-4 border-b border-gray-200 dark:border-gray-700">
            <h1 className="text-xl font-bold text-gray-800 dark:text-gray-200">Interview Feedback Report</h1>
        </header>
        <div className="flex-1 overflow-y-auto p-8 bg-white dark:bg-gray-800">
            {feedback ? (
                <div className="prose dark:prose-invert max-w-none prose-headings:text-gray-800 dark:prose-headings:text-gray-200 prose-p:text-gray-600 dark:prose-p:text-gray-400 prose-li:text-gray-600 dark:prose-li:text-gray-400">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{feedback}</ReactMarkdown>
                </div>
            ) : (
                <div className="flex items-center justify-center h-full text-gray-600 dark:text-gray-400">
                    <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                        <span className="ml-2">Generating your report...</span>
                    </div>
                </div>
            )}
        </div>
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-center">
            <button
                onClick={onRestart}
                className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75 transition-transform transform hover:scale-105"
            >
                Try Again
            </button>
        </div>
    </div>
  );
};

export default FeedbackReport;