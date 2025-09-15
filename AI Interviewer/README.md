# Automated Excel Mock Interviewer

This project is a Proof-of-Concept for an automated system designed to automate the initial screening of a candidate's Microsoft Excel skills through a simulated, conversational interview.

## 1. The Business Context (The 'Why')

Our company is rapidly expanding its Finance, Operations, and Data Analytics divisions. A key skill for all new hires is advanced proficiency in Microsoft Excel. However, our current screening process is a major bottleneck. Manual technical interviews for Excel are time-consuming for our senior analysts and lead to inconsistent evaluations. This slows down our hiring pipeline and impacts our growth targets.

We believe an automated solution can solve this problem by providing a consistent, scalable, and efficient way to conduct initial technical screenings.

## 2. Our Solution: A Conversational Interviewer

This application is a web-based chat interface that simulates a real-time Excel interview. A candidate can interact with an interviewer that asks a series of relevant questions, evaluates their responses, and provides a comprehensive feedback report at the end.

This approach allows candidates to practice their skills in a low-pressure environment while providing the hiring team with a structured and consistent evaluation of their Excel knowledge.

## 3. Core Features

-   **Structured Interview Flow:** The agent guides the user through a series of predefined questions, simulating a real screening call from introduction to conclusion.
-   **Intelligent Answer Evaluation:** Powered by a local Large Language Model via Ollama, the agent provides immediate, brief feedback on the user's answer before proceeding to the next question.
-   **Automated Behavior:** The system is designed to be a professional and encouraging interviewer, creating a realistic and supportive environment for the candidate.
-   **Constructive Feedback Report:** At the conclusion of the interview, a detailed performance summary is generated. It includes an overall summary, a bulleted list of strengths, actionable areas for improvement, and a final proficiency rating.

## 4. Technology Stack

-   **Frontend:** React, TypeScript, Tailwind CSS
    -   **Justification:** This combination was chosen for its modern, component-based architecture, which allows for rapid development and a scalable, maintainable codebase. TypeScript adds type safety, reducing bugs, while Tailwind CSS enables the creation of a polished, responsive UI with minimal custom CSS.
-   **AI / Language Model:** [Ollama](https://ollama.com/) with the `deepseek-coder` model.
    -   **Justification:** Using Ollama to run models locally provides maximum privacy, removes dependency on cloud APIs, eliminates API costs, and allows for deep customization. The `deepseek-coder` model is a powerful, open-source model well-suited for this task due to its strong reasoning and instruction-following capabilities.
-   **Platform:** The application is a pure front-end web app that runs in any modern browser. It communicates with the local Ollama server, which acts as its backend.

## 5. How to Run Locally

To run this application, you must have Ollama installed and running on your machine.

1.  **Install Ollama:** If you haven't already, download and install Ollama from the [official website](https://ollama.com/).

2.  **Pull the Deepseek Coder Model:** Open your terminal and run the following command to download and set up the `deepseek-coder` model:
    ```bash
    ollama run deepseek-coder
    ```
    This may take a few minutes depending on your internet connection. Once complete, you can exit the Ollama chat prompt. Ollama will continue running in the background.

3.  **Clone the project repository.**

4.  **Install Dependencies & Run:** Open your terminal in the project root directory and run your development server. The specific commands may vary based on your setup (e.g., `npm install && npm run dev` or `yarn && yarn dev`).

5.  Open your browser and navigate to the local development server address. The application will now connect to your local Ollama instance for the interview.

## 6. The "Cold Start" Problem & Future Improvements

The project brief correctly identifies the "cold start" problem—how to build an effective system without a pre-existing dataset of interview transcripts. Our strategy addresses this in two phases:

**Phase 1: Bootstrapping with Prompt Engineering (Current Implementation)**

The current system relies on a set of high-quality, general Excel questions and sophisticated prompt engineering. By providing the model with a clear persona, detailed instructions, and a structured format for its responses, we can achieve high-quality results without any initial training data.

**Phase 2: Iterative Improvement (Future Strategy)**

-   **Prompt Refinement:** We can continuously update the system prompts based on observed system behavior and user feedback to improve evaluation quality and conversational flow.
-   **Question Bank Expansion:** The `INTERVIEW_QUESTIONS` array can be expanded and categorized by difficulty or topic (e.g., Formulas, Data Visualization, Macros). The system could then be programmed to dynamically select questions, creating a more adaptive interview experience.
-   **Transcript Analysis:** In a production environment, we could collect anonymized interview transcripts. Analyzing this data would help us identify common candidate mistakes, confusing questions, and areas where the AI's evaluation could be improved. This data provides an invaluable feedback loop for enhancing the entire system.


## 7. This is a working demo of the project

https://github.com/user-attachments/assets/48ac54cf-fa09-4c19-89c5-b21f965c0e3f

