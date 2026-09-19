import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from serp_search import gather_resources
from summarizer import build_digest

st.set_page_config(page_title="PrepRadar", page_icon="📚", layout="centered")

CATEGORY_META = {
    "Web": {"icon": "🌐", "badge": "badge-web"},
    "YouTube": {"icon": "▶️", "badge": "badge-youtube"},
    "Scholar": {"icon": "🎓", "badge": "badge-scholar"},
}
CATEGORY_ORDER = ["Web", "YouTube", "Scholar"]

st.markdown(
    """
    <style>
    .block-container { max-width: 760px; padding-top: 2.5rem; }

    .pr-hero-title { font-size: 2.1rem; font-weight: 800; margin-bottom: 0.2rem; }
    .pr-hero-sub { color: #9a9aa5; font-size: 0.95rem; margin-bottom: 1.8rem; line-height: 1.5; }

    .pr-overview {
        border-left: 4px solid #8b5cf6;
        background: rgba(139, 92, 246, 0.08);
        border-radius: 0.5rem;
        padding: 1rem 1.25rem;
        margin: 1.4rem 0 2rem 0;
        line-height: 1.55;
    }

    .pr-section-header {
        font-size: 1.05rem;
        font-weight: 700;
        margin: 1.6rem 0 0.6rem 0;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .pr-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 0.6rem;
        padding: 0.85rem 1.05rem;
        margin-bottom: 0.6rem;
        transition: border-color 0.15s ease;
    }
    .pr-card:hover { border-color: rgba(139, 92, 246, 0.55); }

    .pr-card-title a {
        text-decoration: none;
        font-weight: 600;
        font-size: 0.98rem;
    }
    .pr-card-title a:hover { color: #a78bfa; }

    .pr-card-note {
        color: #9a9aa5;
        font-size: 0.85rem;
        margin-top: 0.25rem;
        line-height: 1.4;
    }

    .pr-badge {
        display: inline-block;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 0.15rem 0.5rem;
        border-radius: 999px;
        margin-bottom: 0.4rem;
    }
    .badge-web { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
    .badge-youtube { background: rgba(239, 68, 68, 0.15); color: #f87171; }
    .badge-scholar { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="pr-hero-title">📚 PrepRadar</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="pr-hero-sub">Turn a weak topic into a curated study digest — '
    "powered by live search across the web, YouTube, and Google Scholar.</div>",
    unsafe_allow_html=True,
)

topic = st.text_input(
    "What topic are you struggling with?",
    placeholder="e.g. Deadlock handling in Operating Systems",
)

if st.button("Build my study digest", type="primary") and topic:
    with st.spinner("Searching the web, YouTube, and Scholar..."):
        resources = gather_resources(topic)

    if not resources:
        st.warning("No results found — try a different phrasing of the topic.")
    else:
        with st.spinner("Summarizing and ranking results..."):
            digest = build_digest(topic, resources)

        overview = digest.get("overview", "")
        ranked = digest.get("resources", [])

        if overview:
            st.markdown(f'<div class="pr-overview">{overview}</div>', unsafe_allow_html=True)

        if ranked:
            grouped: dict[str, list[dict]] = {}
            for item in ranked:
                grouped.setdefault(item.get("category", "Web"), []).append(item)

            for category in CATEGORY_ORDER:
                items = grouped.get(category)
                if not items:
                    continue
                meta = CATEGORY_META[category]
                st.markdown(
                    f'<div class="pr-section-header">{meta["icon"]} {category}</div>',
                    unsafe_allow_html=True,
                )
                for item in items:
                    st.markdown(
                        f"""
                        <div class="pr-card">
                            <span class="pr-badge {meta['badge']}">{category}</span>
                            <div class="pr-card-title"><a href="{item.get('link', '#')}" target="_blank">{item.get('title', 'Untitled')}</a></div>
                            <div class="pr-card-note">{item.get('note', '')}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(overview)

        with st.expander(f"Raw sources found ({len(resources)})"):
            for r in resources:
                st.write(f"**[{r['source']}]** [{r['title']}]({r['link']})")
