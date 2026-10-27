import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv, find_dotenv

# Resolve .env from this source file, independent of the directory Streamlit
# was launched from. An explicit process environment variable still wins.
load_dotenv(find_dotenv(usecwd=True) or os.path.join(os.path.dirname(__file__), ".env"))

def _build_llm():
    """Create Gemini when configured; keep the UI importable without credentials."""
    api_key = os.getenv("GOOGLE_API_KEY", "").strip().strip('"').strip("'")
    if not api_key:
        return None

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        temperature=0.2,
        max_output_tokens=1500,
        max_retries=2,
    )


llm = _build_llm()

# ── Search: call tool directly, no agent loop needed ──
def run_search(topic: str) -> str:
    """Directly search the web — no agent overhead."""
    return web_search.invoke(topic)

# ── Reader: call tool directly ──
def run_reader(search_results: str, topic: str) -> str:
    """Extract first URL from search results and scrape it."""
    # Find first URL in search results
    import re
    urls = re.findall(r'URL:\s*(https?://\S+)', search_results)
    if not urls:
        return "No URLs found to scrape."

    # Scrape the first relevant URL
    scraped = scrape_url.invoke(urls[0])
    return scraped

# ── Writer chain ──
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser() if llm else None

# ── Critic chain ──
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser() if llm else None


def require_llm() -> None:
    if llm is None:
        raise RuntimeError(
            "Gemini isn't configured yet. Add GOOGLE_API_KEY to the project's .env file."
        )
