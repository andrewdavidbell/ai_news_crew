# Development Plan for AI News Crew Streamlit UI

## Project Purpose and Goals

Create a lightweight Streamlit-based chat interface for the AI News Crew application that enables single-user local interaction with the existing CrewAI framework. The interface should maintain simplicity whilst providing full access to the crew's research and reporting capabilities without requiring heavy JavaScript frameworks or complex deployment infrastructure.

## Context and Background

The existing AI News Crew application utilises CrewAI framework with:
- Two agents: researcher and reporting_analyst configured via YAML
- Sequential task processing: research_task followed by reporting_task
- Current CLI interface via main.py with hardcoded topic inputs
- Output currently writes to report.md file
- Local development environment using uv for dependency management

The crew takes a topic input and produces detailed research reports through a two-stage process where the researcher gathers information and the analyst creates comprehensive markdown reports.

## Hard Requirements

- Single-user local deployment only
- No session management complexity required
- Maintain existing crew functionality without modification
- Use Streamlit for UI framework
- Preserve markdown output formatting
- No file-based output in UI mode

## Development Phases

### Phase 1: Core Streamlit Implementation ✅ COMPLETED
- [x] Create `streamlit_app.py` in project root
  - [x] Import AiNewsCrew class
  - [x] Implement basic page layout with title
  - [x] Add text input field for topic entry
  - [x] Create submit button for crew execution
  - [x] Display loading state during processing
- [x] Add streamlit dependency to pyproject.toml
  - [x] Include streamlit in project dependencies
  - [x] Ensure compatibility with existing dependencies

### Phase 2: Crew Integration ✅ COMPLETED
- [x] Modify task configuration in `src/ai_news_crew/crew.py`
  - [x] Remove `output_file: "report.md"` from reporting_task
  - [x] Ensure expected_output remains markdown formatted
  - [x] Verify task dependencies remain intact
- [x] Implement crew execution in Streamlit
  - [x] Create inputs dictionary with topic and current_year
  - [x] Handle crew.kickoff() method call
  - [x] Capture and display crew output
  - [x] Format output for web display

### Phase 3: User Experience Enhancement ✅ COMPLETED
- [x] Add input validation
  - [x] Ensure topic field is not empty
  - [x] Provide helpful error messages
  - [x] Handle invalid input gracefully
  - [x] Validate topic length (3-200 characters)
  - [x] Check for potentially problematic characters
- [x] Implement output display
  - [x] Use st.markdown() for proper formatting
  - [x] Add clear/reset functionality with "New Research" button
  - [x] Display processing status updates with progress bar
  - [x] Add download button for reports
- [x] Add basic error handling
  - [x] Catch crew execution exceptions
  - [x] Display user-friendly error messages
  - [x] Provide troubleshooting guidance based on error type
  - [x] Categorise errors (API, connection, memory, general)

### Phase 4: Documentation and Testing ✅ COMPLETED
- [x] Update README.md
  - [x] Add UI usage instructions
  - [x] Include streamlit run command
  - [x] Document local setup requirements
- [x] Test core functionality
  - [x] Verify crew output displays correctly
  - [x] Test error conditions
  - [x] Validate markdown rendering
  - [x] Confirm no file outputs created

## Assumptions

- Streamlit can handle the crew's processing time without timeout issues
- Crew output format is suitable for direct display in Streamlit
- No authentication or user management required for local use
- Current crew configuration will work without modification
- uv package manager will handle streamlit dependency correctly

## QA Checklist

- [x] All user instructions followed
- [x] Streamlit interface functional and intuitive
- [x] Existing crew functionality preserved
- [x] No critical code smell warnings
- [x] Code follows PEP-8 standards
- [x] Documentation updated with UI instructions
- [x] Input validation prevents common errors
- [x] Error handling provides clear feedback
- [x] Local deployment tested and verified
- [x] No residual files created during UI operation
- [x] Markdown formatting displays correctly
- [x] Processing time acceptable for local use
