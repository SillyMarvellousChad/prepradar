"""Uses Groq (free-tier LLM) to rank and summarize search results into a study digest."""
import json
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

GROQ_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "You are a study assistant that turns raw search results into a structured "
    "study digest for a student. You will be given a topic and a list of search "
    "results tagged by category (Web, YouTube, Scholar).\n\n"
    "Return ONLY valid JSON, no markdown fences, no commentary, matching exactly "
    "this schema:\n"
    '{"overview": "<2-3 sentence plain-text overview of the topic>", '
    '"resources": [{"category": "Web"|"YouTube"|"Scholar", '
    '"title": "<short resource title, max ~12 words>", "link": "<url>", '
    '"note": "<one-sentence note on what this resource covers and why it helps>"}]}\n\n'
    "Rules: pick the best 5-8 resources overall, drop irrelevant or low-quality "
    "ones, keep each category's original label, and only use links given in the "
    "input — never invent one."
)


def build_digest(topic: str, resources: list[dict]) -> dict:
    """Send the topic and gathered resources to Groq and return structured digest data.

    Returns a dict: {"overview": str, "resources": [{"category", "title", "link", "note"}]}.
    Falls back to {"overview": <raw text>, "resources": []} if the model doesn't
    return valid JSON.
    """
    resource_text = "\n".join(
        f"- [{r['source']}] {r['title']} — {r['link']}\n  {r.get('snippet', '')}"
        for r in resources
    )
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=1200,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nSearch results:\n{resource_text}",
            },
        ],
    )
    raw = completion.choices[0].message.content
    try:
        data = json.loads(raw)
        data.setdefault("overview", "")
        data.setdefault("resources", [])
        return data
    except (json.JSONDecodeError, AttributeError):
        return {"overview": raw, "resources": []}
