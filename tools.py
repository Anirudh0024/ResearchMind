from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()


tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web fro recent and reliable information on a topic. Returns Titles,URLs and small snippits."""
    results = tavily.search(query=query, max_results=1)
    out = []

    for r in results["results"]:
        out.append(
            f"Title:{r['title']}\nUrl:{r['url']}\nSnippit:{r['content'][:300]}\n"
        )
    return "\n----\n".join(out)


@tool
def web_scrape(url: str) -> str:
    """Scrape the web page at the given URL and return its text content."""
    try:
        response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:2000]
    except Exception as e:
        return f"Could not scrape URL:{str(e)}"


# print(
#     web_scrape.invoke(
#         "https://www.indiatoday.in/cities/delhi/story/delhi-air-pollution-aqi-311-no-rain-forecast-till-november-15-3035730-2026-11-10"
#     )
# )
