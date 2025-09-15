
import React, { useState, useCallback } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import ChatWindow from './components/ChatWindow';
import FeedbackReport from './components/FeedbackReport';
import { InterviewState, Message } from './types';
import { evaluateAnswerAndGetNextPrompt, generateFinalFeedback } from './services/ollamaService';
import { INTERVIEW_QUESTIONS } from './constants';

const App: React.FC = () => {
  const [interviewState, setInterviewState] = useState<InterviewState>(InterviewState.NOT_STARTED);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const handleStartInterview = useCallback(() => {
    setMessages([
      { role: 'model', content: "Hello! I'm your automated Excel mock interviewer. I'll ask you a series of questions to assess your Excel proficiency. Let's begin with the first question." },
      { role: 'model', content: INTERVIEW_QUESTIONS[0] }
    ]);
    setInterviewState(InterviewState.IN_PROGRESS);
    setCurrentQuestionIndex(0);
    setUserAnswers([]);
    setFeedback('');
    setError(null);
  }, []);

  const handleSendMessage = async (userMessage: string) => {
    if (isLoading || !userMessage.trim()) return;

    const newMessages: Message[] = [...messages, { role: 'user', content: userMessage }];
    setMessages(newMessages);
    setUserAnswers(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      if (currentQuestionIndex < INTERVIEW_QUESTIONS.length - 1) {
        const nextQuestionIndex = currentQuestionIndex + 1;
        const responseText = await evaluateAnswerAndGetNextPrompt(
          INTERVIEW_QUESTIONS[currentQuestionIndex],
          userMessage,
          INTERVIEW_QUESTIONS[nextQuestionIndex]
        );
        setMessages(prev => [...prev, { role: 'model', content: responseText }]);
        setCurrentQuestionIndex(nextQuestionIndex);
      } else {
        // Last question
        const concludingMessage = "Thank you, that concludes the interview. I am now generating your feedback report. Please wait a moment.";
        setMessages(prev => [...prev, { role: 'model', content: concludingMessage }]);
        
        const transcript = INTERVIEW_QUESTIONS.map((q, i) => ({ question: q, answer: userAnswers[i] || "" }));
        transcript[INTERVIEW_QUESTIONS.length-1].answer = userMessage;

        const finalFeedback = await generateFinalFeedback(transcript);
        setFeedback(finalFeedback);
        setInterviewState(InterviewState.COMPLETED);
      }
    } catch (err) {
      console.error(err);
      const errorMessage = err instanceof Error ? err.message : "An unknown error occurred.";
      setError(errorMessage);
      setMessages(prev => [...prev, { role: 'model', content: `Sorry, I encountered an error: ${errorMessage}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    setInterviewState(InterviewState.NOT_STARTED);
    setMessages([]);
  };

  const renderContent = () => {
    switch (interviewState) {
      case InterviewState.NOT_STARTED:
        return <WelcomeScreen onStart={handleStartInterview} />;
      case InterviewState.IN_PROGRESS:
        return <ChatWindow messages={messages} onSendMessage={handleSendMessage} isLoading={isLoading} error={error} />;
      case InterviewState.COMPLETED:
        return <FeedbackReport feedback={feedback} onRestart={handleRestart} />;
      default:
        return <WelcomeScreen onStart={handleStartInterview} />;
    }
  };

  return (
    <div className="flex flex-col h-screen items-center justify-center bg-gray-100 dark:bg-gray-900 font-sans p-4">
      <div className="w-full max-w-2xl h-full max-h-[700px] flex flex-col bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden">
        {renderContent()}
      </div>
       <footer className="text-center text-sm text-gray-500 dark:text-gray-400 mt-4">
          Made By Ashish Chhabra.
        </footer>
    </div>
  );
};

export default App;
