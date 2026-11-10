import streamlit as st

from agents import writer_chain, critic_chain
from tools import search_web, scrape_webpage

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ResearchMind | AI Research Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
<style>

:root {
    --bg: #F5F7F5;
    --surface: #FFFFFF;
    --primary: #174D3D;
    --primary-hover: #23664F;
    --text: #173B32;
    --muted: #77857D;
    --border: #DCE5DF;
    --soft: #EAF1EC;
}

/* GLOBAL LIGHT THEME */

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* HEADER */

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    background-color: var(--bg) !important;
}

/* TYPOGRAPHY */

h1, h2, h3, h4 {
    color: var(--text) !important;
    letter-spacing: -0.5px;
}

p, label {
    color: var(--muted);
}

/* SIDEBAR */

[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background-color: #FFFFFF !important;
}

[data-testid="stSidebar"] {
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text) !important;
}

/* HERO */

.hero {
    padding: 35px;
    background: var(--primary);
    border-radius: 16px;
    margin-bottom: 30px;
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 36px;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #D4E5DA;
    font-size: 15px;
    margin-top: 12px;
    margin-bottom: 0;
    line-height: 1.7;
}

/* INPUT */

.stTextInput input {
    background-color: #FFFFFF !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
    min-height: 46px;
}

.stTextInput input::placeholder {
    color: #9AA9A0 !important;
    opacity: 1 !important;
}

.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 1px var(--primary) !important;
}

/* PRIMARY BUTTONS */

.stFormSubmitButton button,
button[kind="primary"] {
    background-color: var(--primary) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--primary) !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 44px;
}

.stFormSubmitButton button:hover,
button[kind="primary"]:hover {
    background-color: var(--primary-hover) !important;
    border-color: var(--primary-hover) !important;
    color: #FFFFFF !important;
}

/* SECONDARY BUTTONS */

[data-testid="stSidebar"] button,
.stButton button[kind="secondary"] {
    background-color: var(--soft) !important;
    color: var(--primary) !important;
    border: 1px solid #C9D9CE !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 42px;
}

[data-testid="stSidebar"] button:hover,
.stButton button[kind="secondary"]:hover {
    background-color: #DCE9E1 !important;
    color: #123D32 !important;
    border-color: var(--primary) !important;
}

/* DOWNLOAD BUTTON */

.stDownloadButton button {
    background-color: var(--primary) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--primary) !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 44px;
}

/* AGENT CARDS */

.agent-card {
    background-color: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    min-height: 115px;
    transition: 0.2s ease;
}

.agent-card:hover {
    border-color: #9ABBA6;
    transform: translateY(-2px);
}

.agent-icon {
    font-size: 23px;
    margin-bottom: 10px;
}

.agent-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
}

.agent-description {
    color: var(--muted);
    font-size: 12px;
    margin-top: 5px;
}

/* TABS */

.stTabs [data-baseweb="tab-list"] {
    gap: 18px;
    border-bottom: 1px solid var(--border);
    background-color: transparent !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
}

/* STATUS */

[data-testid="stStatusWidget"] {
    background-color: #FFFFFF !important;
    color: var(--text) !important;
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* DIVIDERS */

hr {
    border-color: var(--border) !important;
}

footer {
    background-color: var(--bg) !important;
}

#MainMenu {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# HELPER FUNCTIONS
# ==========================================


def to_text(content):
    """Convert LangChain output into readable text."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for block in content:

            if isinstance(block, str):
                parts.append(block)

            elif isinstance(block, dict) and "text" in block:
                parts.append(block["text"])

        return "\n".join(parts)

    if isinstance(content, dict):
        parts = []

        for key, value in content.items():

            title = key.replace("_", " ").title()

            if isinstance(value, list):
                value = "\n".join(f"- {item}" for item in value)

            parts.append(f"### {title}\n{value}")

        return "\n\n".join(parts)

    return str(content)


# ==========================================
# RESEARCH PIPELINE
# ==========================================


def run_pipeline_with_progress(topic):

    state = {}

    with st.status("ResearchMind is working...", expanded=True) as status:

        # ==================================
        # STEP 1: SEARCH
        # ==================================

        st.write("🔎 **Step 1/4 — Searching the web**")

        search_results = search_web(topic, max_results=3)

        if not search_results:
            raise ValueError("No search results found. Try another topic.")

        search_text = []

        for index, result in enumerate(search_results, start=1):

            title = result.get("title", "Untitled")
            url = result.get("url", "")
            snippet = result.get("content", "")

            search_text.append(
                f"### Source {index}: {title}\n" f"URL: {url}\n" f"Snippet: {snippet}\n"
            )

        state["search_result"] = "\n".join(search_text)

        st.write(f"✓ Found {len(search_results)} search results")

        # ==================================
        # STEP 2: READER
        # ==================================

        st.write("📖 **Step 2/4 — Reading webpages**")

        scraped_text = []
        valid_sources = []

        for index, result in enumerate(search_results, start=1):

            url = result.get("url", "")
            title = result.get("title", "Untitled")

            if not url:
                continue

            with st.spinner(f"Reading source {index}/{len(search_results)}..."):

                content = scrape_webpage(url)

            if (
                content
                and not content.startswith(
                    (
                        "Could not scrape",
                        "Scraping failed",
                        "Invalid URL",
                    )
                )
                and content != "No readable content found."
            ):

                valid_sources.append(url)

                scraped_text.append(
                    f"### {title}\n"
                    f"Source URL: {url}\n"
                    f"Extracted Content:\n{content[:3500]}\n"
                )

                st.write(f"✓ Source {index} extracted")

            else:

                st.warning(f"Could not extract content from source {index}.")

        if not scraped_text:

            raise ValueError(
                "Could not scrape any webpages. " "Try another research topic."
            )

        state["scraped_content"] = "\n\n".join(scraped_text)

        state["sources"] = valid_sources

        st.write(f"✓ Successfully read {len(valid_sources)} webpages")

        # ==================================
        # STEP 3: WRITER
        # ==================================

        st.write("✍️ **Step 3/4 — Writing research report**")

        research_combined = (
            f"SEARCH RESULTS:\n"
            f"{state['search_result']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n"
            f"{state['scraped_content']}"
        )

        with st.spinner("Writer is generating your research report..."):

            report_result = writer_chain.invoke(
                {
                    "topic": topic,
                    "research": research_combined,
                }
            )

        state["report"] = to_text(report_result)

        st.write("✓ Research report generated")

        # ==================================
        # STEP 4: CRITIC
        # ==================================

        st.write("🧐 **Step 4/4 — Reviewing report quality**")

        with st.spinner("Critic is evaluating your report..."):

            feedback_result = critic_chain.invoke({"report": state["report"]})

        state["feedback"] = to_text(feedback_result)

        st.write("✓ Critic review completed")

        # ==================================
        # COMPLETION
        # ==================================

        status.update(
            label="Research completed successfully!",
            state="complete",
            expanded=False,
        )

    return state


# ==========================================
# SESSION STATE
# ==========================================

if "result" not in st.session_state:
    st.session_state.result = None

if "topic" not in st.session_state:
    st.session_state.topic = ""


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🔎 ResearchMind")

    st.caption("AI Research Workspace")

    st.divider()

    st.markdown("### WORKFLOW")

    st.markdown("""
    🔎 **Search Agent**

    📖 **Reader Agent**

    ✍️ **Writer Agent**

    🧐 **Critic Agent**
    """)

    st.divider()

    st.markdown("### BUILT WITH")

    st.caption("Python · LangChain · Groq · Tavily · Streamlit")

    st.divider()

    if st.button(
        "🗑️ Clear results",
        use_container_width=True,
        type="secondary",
    ):

        st.session_state.result = None
        st.session_state.topic = ""

        st.rerun()

    st.divider()

    st.caption("ResearchMind · Version 1.0")


# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
    """
<div class="hero">

    <h1>Research, with clarity.</h1>

    <p>
        Discover information, explore sources, and create
        structured research reports with your AI team.
    </p>

</div>
""",
    unsafe_allow_html=True,
)


# ==========================================
# RESEARCH INPUT
# ==========================================

st.markdown("### Start your research")

with st.form("research_form"):

    topic_input = st.text_input(
        "Research topic",
        placeholder="e.g. The future of Generative AI in healthcare",
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(
        "✦  Generate research report",
        type="primary",
        use_container_width=True,
    )


# ==========================================
# RUN RESEARCH
# ==========================================

if submitted:

    topic = topic_input.strip()

    if not topic:

        st.warning("Please enter a research topic.")

    else:

        try:

            st.session_state.result = None
            st.session_state.topic = topic

            st.session_state.result = run_pipeline_with_progress(topic)

            st.success("Your research report is ready!")

        except Exception as error:

            error_message = str(error).lower()

            st.error("Research pipeline failed.")

            if (
                "429" in error_message
                or "rate_limit" in error_message
                or "rate limit" in error_message
            ):

                st.warning(
                    "Groq API rate limit reached. "
                    "Your research pipeline uses two LLM stages: "
                    "Writer and Critic. Please wait for your "
                    "token limit to reset or reduce the report size."
                )

            else:

                st.error(str(error))


# ==========================================
# WORKFLOW OVERVIEW
# ==========================================

if not st.session_state.result:

    st.markdown("### Your research team")

    col1, col2, col3, col4 = st.columns(4)

    agents = [
        (col1, "🔎", "Search", "Find relevant sources"),
        (col2, "📖", "Reader", "Extract useful content"),
        (col3, "✍️", "Writer", "Generate structured reports"),
        (col4, "🧐", "Critic", "Evaluate report quality"),
    ]

    for col, icon, name, description in agents:

        with col:

            st.markdown(
                f"""
                <div class="agent-card">

                    <div class="agent-icon">{icon}</div>

                    <div class="agent-title">{name}</div>

                    <div class="agent-description">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ==========================================
# RESULTS DASHBOARD
# ==========================================

result = st.session_state.result

if result:

    st.divider()

    st.markdown("## Research results")

    st.caption(f"Research topic: {st.session_state.topic}")

    # RESULTS TABS

    tab_report, tab_critic, tab_search, tab_reader = st.tabs(
        [
            "📄 Research Report",
            "🧐 Critic Review",
            "🔎 Search Results",
            "📖 Scraped Content",
        ]
    )

    # REPORT

    with tab_report:

        st.markdown(result["report"])

        st.divider()

        st.download_button(
            label="⬇ Download research report",
            data=result["report"],
            file_name="ResearchMind_Report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # CRITIC

    with tab_critic:

        st.markdown(result["feedback"])

    # SEARCH

    with tab_search:

        st.markdown(result["search_result"])

    # SCRAPED CONTENT

    with tab_reader:

        st.markdown(result["scraped_content"])

        if result.get("sources"):

            st.divider()

            st.markdown("### Sources")

            for index, url in enumerate(result["sources"], start=1):

                st.markdown(f"{index}. [{url}]({url})")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption("ResearchMind · Built with Python and LangChain")
