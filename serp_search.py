"""SerpApi search helpers for PrepRadar.

Runs three parallel-style searches (web, YouTube, Google Scholar) for a
given study topic and returns a normalized list of results.
"""
import os
from serpapi import GoogleSearch

SERPAPI_KEY = os.environ.get("SERPAPI_API_KEY")


def _run_search(params: dict) -> dict:
    if not SERPAPI_KEY:
        raise RuntimeError(
            "SERPAPI_API_KEY environment variable is not set. "
            "Copy .env.example to .env and add your key."
        )
    params["api_key"] = SERPAPI_KEY
    search = GoogleSearch(params)
    return search.get_dict()


def search_web(topic: str, num_results: int = 5) -> list[dict]:
    """Search Google for articles/explainers on a topic."""
    results = _run_search({
        "engine": "google",
        "q": f'"{topic}" tutorial',
        "num": num_results,
    })
    items = results.get("organic_results", [])[:num_results]
    return [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet", ""),
            "source": "Web",
        }
        for item in items
    ]


def search_youtube(topic: str, num_results: int = 5) -> list[dict]:
    """Search YouTube for lecture/explainer videos on a topic."""
    results = _run_search({
        "engine": "youtube",
        "search_query": f"{topic} lecture",
    })
    items = results.get("video_results", [])[:num_results]
    return [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("description", ""),
            "source": "YouTube",
        }
        for item in items
    ]


def search_scholar(topic: str, num_results: int = 5) -> list[dict]:
    """Search Google Scholar for academic references on a topic."""
    results = _run_search({
        "engine": "google_scholar",
        "q": topic,
    })
    items = results.get("organic_results", [])[:num_results]
    return [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet", ""),
            "source": "Scholar",
        }
        for item in items
    ]


def gather_resources(topic: str) -> list[dict]:
    """Run all three searches and combine the results into one list."""
    resources: list[dict] = []
    resources.extend(search_web(topic))
    resources.extend(search_youtube(topic))
    resources.extend(search_scholar(topic))
    return resources
