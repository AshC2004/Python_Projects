
export enum InterviewState {
  NOT_STARTED = 'NOT_STARTED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
}

export type MessageRole = 'user' | 'model';

export interface Message {
  role: MessageRole;
  content: string;
}

export interface InterviewTranscript {
    question: string;
    answer: string;
}
