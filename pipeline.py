from agents import built_reader_agent, built_search_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:

    state = {}

    try:
        # ==========================================
        # STEP 1: SEARCH AGENT
        # ==========================================

        print("\n" + " =" * 50)
        print("STEP 1: Search agent is working...")
        print("=" * 50)

        search_agent = built_search_agent()

        search_result = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Find recent, reliable and detailed information about: {topic}",
                    )
                ]
            }
        )

        state["search_result"] = search_result["messages"][-1].content

        print("\nSearch result:\n", state["search_result"])

        # ==========================================
        # STEP 2: READER AGENT
        # ==========================================

        print("\n" + " =" * 50)
        print("STEP 2: Reader agent is scraping top resources...")
        print("=" * 50)

        reader_agent = built_reader_agent()

        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_result'][:800]}",
                    )
                ]
            }
        )

        state["scraped_content"] = reader_result["messages"][-1].content

        print("\nScraped content:\n", state["scraped_content"])

        # ==========================================
        # STEP 3: WRITER CHAIN
        # ==========================================

        print("\n" + " =" * 50)
        print("STEP 3: Writer is drafting the report...")
        print("=" * 50)

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_result']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )

        state["report"] = writer_chain.invoke(
            {"topic": topic, "research": research_combined}
        )

        print("\nFINAL RESEARCH REPORT:\n", state["report"])

        # ==========================================
        # STEP 4: CRITIC CHAIN
        # ==========================================

        print("\n" + " =" * 50)
        print("STEP 4: Critic is reviewing the report...")
        print("=" * 50)

        state["feedback"] = critic_chain.invoke({"report": state["report"]})

        print("\nCRITIC REVIEW:\n", state["feedback"])

        return state

    except Exception as error:
        print(f"\nResearch pipeline failed: {error}")
        raise


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    topic = input("\nEnter a research topic: ").strip()

    if topic:
        result = run_research_pipeline(topic)
    else:
        print("Please enter a valid research topic.")
