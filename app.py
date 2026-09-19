import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from serp_search import gather_resources
from summarizer import build_digest

st.set_page_config(page_title="PrepRadar", page_icon="📚")
st.title("📚 PrepRadar")
st.caption(
    "An AI research agent that turns a weak topic into a curated study digest, "
    "built on SerpApi's Google Search, YouTube Search, and Google Scholar engines."
)

topic = st.text_input(
    "What topic are you struggling with?",
    placeholder="e.g. Deadlock handling in Operating Systems",
)

if st.button("Build my study digest") and topic:
    with st.spinner("Searching the web, YouTube, and Scholar..."):
        resources = gather_resources(topic)

    if not resources:
        st.warning("No results found — try a different phrasing of the topic.")
    else:
        with st.spinner("Summarizing and ranking results..."):
            digest = build_digest(topic, resources)
        st.markdown(digest)

        with st.expander(f"Raw sources found ({len(resources)})"):
            for r in resources:
                st.write(f"**[{r['source']}]** [{r['title']}]({r['link']})")
