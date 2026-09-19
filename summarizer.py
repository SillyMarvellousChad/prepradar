"""Uses Groq (free-tier LLM) to rank and summarize search results into a study digest."""
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

GROQ_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "You are a study assistant. You will be given a topic and a list of "
    "search results (web articles, YouTube videos, and scholarly sources). "
    "Rank them by usefulness for a student trying to learn the topic, drop "
    "anything irrelevant or low-quality, and write a short study digest. "
    "Respond in Markdown with a 2-3 sentence overview of the topic, then a "
    "'Recommended Resources' section listing the best 5-8 sources grouped by "
    "type (Web, YouTube, Scholar), each with the title as a link and a "
    "one-line note on what it covers."
)


def build_digest(topic: str, resources: list[dict]) -> str:
    """Send the topic and gathered resources to Groq and return a Markdown digest."""
    resource_text = "\n".join(
        f"- [{r['source']}] {r['title']} — {r['link']}\n  {r.get('snippet', '')}"
        for r in resources
    )
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=1200,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nSearch results:\n{resource_text}",
            },
        ],
    )
    return completion.choices[0].message.content
