#!/usr/bin/env python
"""
Streamlit UI for AI News Crew
A lightweight chat interface for local interaction with the CrewAI framework.
"""

import warnings
from datetime import datetime

import streamlit as st

from src.ai_news_crew.crew import AiNewsCrew

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def main():
    """Main Streamlit application"""

    # Page configuration
    st.set_page_config(
        page_title="AI News Crew",
        page_icon="📰",
        layout="centered",
        initial_sidebar_state="auto",
    )

    # Main title and description
    st.title("📰 AI News Crew")
    st.markdown("""
    Welcome to AI News Crew - your intelligent research and reporting assistant.
    Enter a topic below and our AI crew will conduct thorough research and generate a comprehensive report.
    """)

    # Input section
    st.subheader("Research Topic")
    topic = st.text_input(
        "What would you like to research?",
        placeholder="e.g., AI LLMs, Climate Change, Quantum Computing",
        help="Enter any topic you'd like our AI crew to research and report on",
    )

    # Submit button
    if st.button("🚀 Start Research", type="primary", use_container_width=True):
        if not topic.strip():
            st.error("Please enter a topic to research.")
            return

        # Show loading state
        with st.spinner(
            "🔍 AI crew is researching your topic... This may take a few minutes."
        ):
            try:
                # Prepare inputs for the crew
                inputs = {
                    "topic": topic.strip(),
                    "current_year": str(datetime.now().year),
                }

                # Execute the crew
                crew_instance = AiNewsCrew()
                result = crew_instance.crew().kickoff(inputs=inputs)

                # Display success message
                st.success("✅ Research completed successfully!")

                # Display the result
                st.subheader("📋 Research Report")
                st.markdown("---")

                # Format and display the crew output
                if hasattr(result, "raw"):
                    st.markdown(result.raw)
                else:
                    st.markdown(str(result))

            except Exception as e:
                st.error(f"❌ An error occurred during research: {str(e)}")
                st.info("Please try again or check your configuration.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Powered by CrewAI • Built with Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
