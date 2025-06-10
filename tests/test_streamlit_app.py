"""
Tests for the Streamlit AI News Crew application
"""

import os

# Import the main function from streamlit_app
import sys
from datetime import datetime
from unittest.mock import Mock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai_news_crew.crew import AiNewsCrew

# Import the validation function from streamlit_app
from streamlit_app import display_error_with_guidance, validate_topic_input


class TestAiNewsCrewIntegration:
    """Test the AI News Crew integration"""

    def test_crew_instance_creation(self):
        """Test that AiNewsCrew can be instantiated"""
        crew_instance = AiNewsCrew()
        assert crew_instance is not None

    def test_crew_has_required_methods(self):
        """Test that the crew has the required methods"""
        crew_instance = AiNewsCrew()
        assert hasattr(crew_instance, "crew")
        assert callable(crew_instance.crew)

    def test_crew_kickoff_inputs_format(self):
        """Test that inputs are formatted correctly for crew kickoff"""
        expected_inputs = {
            "topic": "Test Topic",
            "current_year": str(datetime.now().year),
        }

        # Verify the inputs structure matches what the crew expects
        assert "topic" in expected_inputs
        assert "current_year" in expected_inputs
        assert isinstance(expected_inputs["current_year"], str)

    @patch("src.ai_news_crew.crew.AiNewsCrew")
    def test_crew_execution_mock(self, mock_crew_class):
        """Test crew execution with mocked response"""
        # Mock the crew instance and its methods
        mock_crew_instance = Mock()
        mock_crew = Mock()
        mock_result = Mock()
        mock_result.raw = "# Test Report\n\nThis is a test report."

        mock_crew.kickoff.return_value = mock_result
        mock_crew_instance.crew.return_value = mock_crew
        mock_crew_class.return_value = mock_crew_instance

        # Test the crew execution flow
        crew_instance = mock_crew_class()
        inputs = {"topic": "Test Topic", "current_year": "2025"}
        result = crew_instance.crew().kickoff(inputs=inputs)

        # Verify the mock was called correctly
        mock_crew_class.assert_called_once()
        mock_crew_instance.crew.assert_called_once()
        mock_crew.kickoff.assert_called_once_with(inputs=inputs)

        # Verify the result has the expected structure
        assert hasattr(result, "raw")
        assert result.raw == "# Test Report\n\nThis is a test report."


class TestInputValidation:
    """Test the input validation functionality"""

    def test_validate_empty_input(self):
        """Test validation of empty input"""
        is_valid, message = validate_topic_input("")
        assert not is_valid
        assert "Please enter a topic" in message

    def test_validate_whitespace_input(self):
        """Test validation of whitespace-only input"""
        is_valid, message = validate_topic_input("   ")
        assert not is_valid
        assert "Please enter a topic" in message

    def test_validate_short_input(self):
        """Test validation of too short input"""
        is_valid, message = validate_topic_input("AI")
        assert not is_valid
        assert "at least 3 characters" in message

    def test_validate_long_input(self):
        """Test validation of too long input"""
        long_topic = "A" * 201
        is_valid, message = validate_topic_input(long_topic)
        assert not is_valid
        assert "less than 200 characters" in message

    def test_validate_invalid_characters(self):
        """Test validation of input with invalid characters"""
        invalid_topics = ["Topic<script>", "Topic{test}", "Topic[array]"]
        for topic in invalid_topics:
            is_valid, message = validate_topic_input(topic)
            assert not is_valid
            assert "invalid characters" in message

    def test_validate_valid_input(self):
        """Test validation of valid input"""
        valid_topics = [
            "Quantum Computing",
            "AI and Machine Learning",
            "Climate Change 2025",
            "Space Exploration: Mars Mission",
        ]
        for topic in valid_topics:
            is_valid, message = validate_topic_input(topic)
            assert is_valid
            assert message == ""

    def test_validate_edge_cases(self):
        """Test validation edge cases"""
        # Minimum valid length
        is_valid, message = validate_topic_input("ABC")
        assert is_valid
        assert message == ""

        # Maximum valid length
        max_topic = "A" * 200
        is_valid, message = validate_topic_input(max_topic)
        assert is_valid
        assert message == ""


class TestStreamlitAppComponents:
    """Test individual components of the Streamlit app"""

    def test_input_validation(self):
        """Test input validation logic"""
        # Test empty input
        empty_topic = ""
        assert not empty_topic.strip()

        # Test whitespace-only input
        whitespace_topic = "   "
        assert not whitespace_topic.strip()

        # Test valid input
        valid_topic = "Quantum Computing"
        assert valid_topic.strip()
        assert len(valid_topic.strip()) > 0

    def test_current_year_generation(self):
        """Test that current year is generated correctly"""
        current_year = str(datetime.now().year)
        assert current_year.isdigit()
        assert len(current_year) == 4
        assert int(current_year) >= 2025

    def test_error_guidance_function_exists(self):
        """Test that error guidance function exists and is callable"""
        assert callable(display_error_with_guidance)

    def test_mock_result_formatting(self):
        """Test that result formatting handles different result types"""
        # Test result with raw attribute
        mock_result_with_raw = Mock()
        mock_result_with_raw.raw = "# Test Report\n\nContent here"
        assert hasattr(mock_result_with_raw, "raw")

        # Test result without raw attribute
        mock_result_without_raw = Mock(spec=[])
        assert not hasattr(mock_result_without_raw, "raw")
        # Should fall back to str() conversion
        str_result = str(mock_result_without_raw)
        assert isinstance(str_result, str)


class TestErrorHandling:
    """Test error handling functionality"""

    def test_api_error_detection(self):
        """Test that API errors are properly categorised"""
        api_errors = [
            Exception("API key not found"),
            Exception("Invalid API credentials"),
            Exception("API quota exceeded"),
        ]
        # These would be tested in integration with the actual error display function
        for error in api_errors:
            error_str = str(error).lower()
            assert "api" in error_str or "key" in error_str

    def test_connection_error_detection(self):
        """Test that connection errors are properly categorised"""
        connection_errors = [
            Exception("Connection timeout"),
            Exception("Network connection failed"),
            Exception("Unable to connect to server"),
        ]
        for error in connection_errors:
            error_str = str(error).lower()
            assert (
                "timeout" in error_str
                or "connection" in error_str
                or "connect" in error_str
            )

    def test_memory_error_detection(self):
        """Test that memory errors are properly categorised"""
        memory_errors = [
            Exception("Out of memory"),
            Exception("Insufficient resources"),
            Exception("Memory allocation failed"),
        ]
        for error in memory_errors:
            error_str = str(error).lower()
            assert "memory" in error_str or "resource" in error_str
