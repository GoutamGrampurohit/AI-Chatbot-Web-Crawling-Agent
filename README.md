Collaboratively developed using Tavily and Google's Gemini, this initiative brings together live web search, reranking, summarization, and automated critique, all housed in a straightforward and interactive frontend through Streamlit. At the core of the app, users can enter any prompt and receive the answer a professionally fact-checked summary based on relevant portions of the original document from the web.

🚀 Overview

The app seeks to automate answers to complicated or current-event based questions by taking the following steps:

1. Search for the web via the Tavily API;
2. Reranks the search result in respect to text length as a heuristic for richness of information;
3. Summarizes the top reranked results with Google’s Gemini Pro (gemini-2.5-flash);
4. Criticizes the answer based on the second Gemini prompt;
5. If the answer is criticized, it reruns the generation step automatically;
6. Keeps a history of each search and summary in the Streamlit session.

This is a simple and lightweight (but powerful) demonstration of how self-criticism can help ensure retrieval-augmented generation (RAG) produces high-quality outcomes.

🧠 Key Features

🔎 Live Web Search: Just uses the Tavily API to pull live search results.
 
📊 Reranking: A simple rerank of the search results based on the length of text (a simple easy heuristic).
 
📝 Summarization: Takes advantage of Gemini's generative capability to create clean and reasonably professional outcomes.
 
🧑‍⚖️ AI Critique Agent: Critiques each output against descriptors for completeness/clarity,649 factual consistency, and relevancy.
 
🔁 Auto-Retry logic: It attempts to automatically repeat the generation step if the human critique fails.

🧾 Search History: Keeps a session-based record of all queries and responses
