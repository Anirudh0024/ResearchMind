import os
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

# ==========================================
# ENVIRONMENT SETUP
# ==========================================

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing from environment variables.")

tavily = TavilyClient(api_key=TAVILY_API_KEY)


# ==========================================
# NORMAL PYTHON SEARCH FUNCTION
# ==========================================


def search_web(query: str, max_results: int = 3) -> list:
    """
    Search the web using Tavily.
    Returns a list of search result dictionaries.
    """

    response = tavily.search(
        query=query,
        max_results=max_results,
        search_depth="basic",
    )

    return response.get("results", [])


# ==========================================
# NORMAL PYTHON SCRAPING FUNCTION
# ==========================================


def scrape_webpage(url: str) -> str:
    """
    Scrape webpage content using Requests and BeautifulSoup.
    No LLM required.
    """

    try:
        if not url.startswith(("http://", "https://")):
            return "Invalid URL."

        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 ResearchMind/1.0"},
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary HTML elements
        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "noscript",
            ]
        ):
            tag.decompose()

        # Extract readable content
        text = soup.get_text(separator=" ", strip=True)

        return text[:6000] if text else "No readable content found."

    except requests.RequestException as error:
        return f"Could not scrape webpage: {error}"

    except Exception as error:
        return f"Scraping failed: {error}"


# ==========================================
# LANGCHAIN TOOL WRAPPERS
# Keep these for agent compatibility
# ==========================================


@tool
def web_search(query: str) -> str:
    """Search the web for recent and relevant information."""

    results = search_web(query)

    output = []

    for result in results:

        output.append(
            f"Title: {result.get('title', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Snippet: {result.get('content', 'N/A')[:500]}\n"
        )

    return "\n--------------------\n".join(output)


@tool
def web_scrape(url: str) -> str:
    """Scrape a webpage and return its text content."""

    return scrape_webpage(url)
