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


def validate_topic_input(topic: str) -> tuple[bool, str]:
    """
    Validate the topic input and return validation result with message.

    Args:
        topic: The topic string to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not topic or not topic.strip():
        return False, "Please enter a topic to research."

    topic = topic.strip()

    if len(topic) < 3:
        return False, "Topic must be at least 3 characters long."

    if len(topic) > 200:
        return False, "Topic must be less than 200 characters long."

    # Check for potentially problematic characters
    if any(char in topic for char in ["<", ">", "{", "}", "[", "]"]):
        return (
            False,
            "Topic contains invalid characters. Please use only letters, numbers, and basic punctuation.",
        )

    return True, ""


def display_research_output(result) -> None:
    """
    Display the research output with proper formatting.

    Args:
        result: The crew execution result
    """
    st.success("✅ Research completed successfully!")

    # Display the result
    st.subheader("📋 Research Report")
    st.markdown("---")

    # Format and display the crew output
    if hasattr(result, "raw"):
        content = result.raw
    else:
        content = str(result)

    # Display the markdown content
    st.markdown(content)

    # Add download button for the report
    st.download_button(
        label="📥 Download Report",
        data=content,
        file_name=f"ai_news_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown",
        use_container_width=True,
    )


def display_error_with_guidance(error: Exception) -> None:
    """
    Display error message with troubleshooting guidance.

    Args:
        error: The exception that occurred
    """
    st.error(f"❌ An error occurred during research: {str(error)}")

    # Provide specific guidance based on error type
    error_str = str(error).lower()

    if "api" in error_str or "key" in error_str:
        st.warning("🔑 **API Configuration Issue**")
        st.info("""
        This appears to be an API configuration issue. Please check:
        - Your API keys are properly set in environment variables
        - You have sufficient API credits/quota
        - Your internet connection is stable
        """)
    elif "timeout" in error_str or "connection" in error_str:
        st.warning("🌐 **Connection Issue**")
        st.info("""
        This appears to be a connection issue. Please:
        - Check your internet connection
        - Try again in a few moments
        - Consider using a simpler topic if the issue persists
        """)
    elif "memory" in error_str or "resource" in error_str:
        st.warning("💾 **Resource Issue**")
        st.info("""
        This appears to be a resource issue. Please:
        - Try a more specific or simpler topic
        - Restart the application if the issue persists
        - Ensure your system has sufficient memory available
        """)
    else:
        st.warning("🔧 **General Troubleshooting**")
        st.info("""
        Please try the following:
        - Ensure your topic is clear and specific
        - Check that all dependencies are properly installed
        - Restart the application if issues persist
        - Contact support if the problem continues
        """)


def main():
    """Main Streamlit application"""

    # Page configuration
    st.set_page_config(
        page_title="AI News Crew",
        page_icon="📰",
        layout="centered",
        initial_sidebar_state="auto",
    )

    # Initialize session state for managing UI state
    if "research_completed" not in st.session_state:
        st.session_state.research_completed = False
    if "last_topic" not in st.session_state:
        st.session_state.last_topic = ""

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
        value=""
        if st.session_state.research_completed
        else st.session_state.last_topic,
    )

    # Create two columns for buttons
    col1, col2 = st.columns([3, 1])

    with col1:
        submit_button = st.button(
            "🚀 Start Research", type="primary", use_container_width=True
        )

    with col2:
        if st.session_state.research_completed:
            if st.button("🔄 New Research", use_container_width=True):
                st.session_state.research_completed = False
                st.session_state.last_topic = ""
                st.rerun()

    # Handle form submission
    if submit_button:
        # Validate input
        is_valid, error_message = validate_topic_input(topic)

        if not is_valid:
            st.error(error_message)
            return

        # Store the topic for potential reuse
        st.session_state.last_topic = topic.strip()

        # Show processing status
        status_container = st.container()
        with status_container:
            st.info("🔄 **Processing Status**")
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("Initialising AI crew...")
            progress_bar.progress(10)

        # Show loading state
        with st.spinner(
            "🔍 AI crew is researching your topic... This may take a few minutes."
        ):
            try:
                # Update status
                status_text.text("Preparing research parameters...")
                progress_bar.progress(20)

                # Prepare inputs for the crew
                inputs = {
                    "topic": topic.strip(),
                    "current_year": str(datetime.now().year),
                }

                # Update status
                status_text.text("Starting research phase...")
                progress_bar.progress(40)

                # Execute the crew
                crew_instance = AiNewsCrew()

                # Update status
                status_text.text("Conducting research and analysis...")
                progress_bar.progress(70)

                result = crew_instance.crew().kickoff(inputs=inputs)

                # Update status
                status_text.text("Finalising report...")
                progress_bar.progress(100)

                # Clear status container
                status_container.empty()

                # Display the result
                display_research_output(result)

                # Mark research as completed
                st.session_state.research_completed = True

            except Exception as e:
                # Clear status container
                status_container.empty()

                # Display error with guidance
                display_error_with_guidance(e)

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
