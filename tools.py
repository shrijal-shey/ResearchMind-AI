from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    try:
        results = DDGS(timeout=8).text(query, max_results=5)
    except Exception as exc:
        return f"Web search failed: {exc}. Check your internet connection and try again."

    out = []
    for r in results:
        out.append(
            f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body'][:300]}\n"
        )

    return "\n----\n".join(out) if out else "No results found."

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(
            url,
            timeout=(3, 8),
            headers={"User-Agent": "Mozilla/5.0"},
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
