import os
import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()

tavily_api = os.getenv("TAVILY_API_KEY")
gemini_api = os.getenv("GEMINI_API_KEY")

# Fail-safe if keys missing
if not tavily_api or not gemini_api:
    st.error("❌ API keys are missing! Please set them in a .env file.")
    st.stop()

# Initialize Tavily + Gemini
tavily_client = TavilyClient(api_key=tavily_api)
genai.configure(api_key=gemini_api)
llm = genai.GenerativeModel("gemini-2.5-flash")

# --- Functions ---
def search(query, n_results=3):
    results = tavily_client.search(query, max_results=n_results)
    return results['results']

def rerank(query, results, topk=3):
    sorted_results = sorted(results, key=lambda x: len(x.get('content', '')), reverse=True)
    return sorted_results[:topk]

def format_results(reranked_results):
    formatted_input = "\n\n".join(
        f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}"
        for r in reranked_results
    )
    prompt = (
        "Format the following search results in a professional, clear tone with summarized key points:\n\n"
        f"{formatted_input}"
    )
    response = llm.generate_content(prompt)
    return response.text

def critic_agent(formatted_text, query):
    critic_prompt = (
        "Act as a critic. Does the following meet these rules:\n"
        "- Clear and professional?\n"
        "- Factually consistent?\n"
        "- Relevant to this query: '{}'\n"
        "Reply 'PASS' if all good, otherwise 'FAIL' with reason.\n"
        "Response:\n{}".format(query, formatted_text)
    )
    critique = llm.generate_content(critic_prompt)
    return critique.text

def pipeline(query):
    results = search(query)
    reranked = rerank(query, results)
    formatted = format_results(reranked)
    critique = critic_agent(formatted, query)
    if "FAIL" in critique:
        return pipeline(query)  # retry with next best
    else:
        return formatted

# --- Streamlit Frontend ---
st.title("🔍 AI Chatbot + Web-Crawling Agent")
st.write("Ask anything, I'll fetch, rerank, summarize, and critique results for you!")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []  # list of {"query": ..., "answer": ...}

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query.strip():
        with st.spinner("Searching and formatting results..."):
            final_output = pipeline(query)

        # Save to history
        st.session_state.history.append({"query": query, "answer": final_output})

        st.success("✅ Critic Agent: PASS")
        st.subheader("📌 Final Answer")
        st.write(final_output)
    else:
        st.warning("⚠️ Please enter a valid query.")

# --- Display History ---
if st.session_state.history:
    st.sidebar.header("📜 Search History")
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        with st.sidebar.expander(f"{i}. {entry['query']}"):
            st.write(entry['answer'])
