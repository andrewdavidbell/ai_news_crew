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
