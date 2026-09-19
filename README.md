# PrepRadar 📚

PrepRadar is an AI research agent for exam prep. Give it a topic you're
struggling with, and it searches the web, YouTube, and academic sources via
SerpApi, then uses an LLM to summarize and rank the results into a single,
curated study digest with links — saving hours of manual searching across
scattered resources.

Built for the [SerpApi India Hackathon 2026](https://serpapi.github.io/serpapi-india-hackathon-2026/) — Track: **AI Agents**.

## How it uses SerpApi

PrepRadar's core functionality depends entirely on SerpApi:

- **Google Search** (`engine=google`) — finds explainer articles and written references
- **YouTube Search** (`engine=youtube`) — finds lecture and tutorial videos
- **Google Scholar** (`engine=google_scholar`) — finds academic papers and references

Without live SerpApi results, the agent has nothing to summarize or rank —
search is the primary data source, not an add-on.

## Setup

1. Clone this repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```
   - Get a free SerpApi key: https://serpapi.com/manage-api-key (250 free searches/month)
   - Get a free Groq API key: https://console.groq.com/keys (no cost, generous free-tier limits)
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL Streamlit prints (usually `http://localhost:8501`).

## Usage

1. Type in a topic you're struggling with (e.g. "Deadlock handling in Operating Systems").
2. Click **Build my study digest**.
3. PrepRadar searches Google, YouTube, and Scholar, then returns a ranked,
   summarized digest of the best resources for that topic.

## Tech stack

- Python
- Streamlit (UI)
- SerpApi (`google-search-results` package) — search
- Groq API (Llama 3.3 70B) — summarization and ranking, free tier

## Project structure

```
prepradar/
├── app.py            # Streamlit UI
├── serp_search.py    # SerpApi search calls
├── summarizer.py      # Groq-based summarization/ranking
├── requirements.txt
├── .env.example
└── README.md
```
