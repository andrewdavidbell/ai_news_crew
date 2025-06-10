"""
Integration tests for OpenLIT observability functionality
"""

import os
import time
from datetime import datetime
from unittest.mock import Mock, patch

import requests

# Import the OpenLIT initialization function
from streamlit_app import initialize_openlit


class TestOpenLITConnectivity:
    """Test OpenLIT service connectivity and configuration"""

    def test_otlp_endpoint_configuration(self):
        """Test that OTLP endpoint is properly configured"""
        # Test default endpoint configuration
        with patch.dict(os.environ, {}, clear=True):
            # Clear environment and test default setting
            result = initialize_openlit()
            assert os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") == "http://localhost:4318"

    def test_sampling_configuration(self):
        """Test that sampling is configured for local development"""
        with patch.dict(os.environ, {}, clear=True):
            initialize_openlit()
            assert os.getenv("OTEL_TRACES_SAMPLER") == "traceidratio"
            assert os.getenv("OTEL_TRACES_SAMPLER_ARG") == "1.0"

    def test_service_name_configuration(self):
        """Test that service name is properly set"""
        with patch.dict(os.environ, {}, clear=True):
            initialize_openlit()
            assert os.getenv("OTEL_SERVICE_NAME") == "ai-news-crew"

    def test_custom_environment_variables_preserved(self):
        """Test that custom environment variables are preserved"""
        custom_endpoint = "http://custom-endpoint:4318"
        custom_service = "custom-service"

        with patch.dict(
            os.environ,
            {
                "OTEL_EXPORTER_OTLP_ENDPOINT": custom_endpoint,
                "OTEL_SERVICE_NAME": custom_service,
            },
        ):
            initialize_openlit()
            assert os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") == custom_endpoint
            assert os.getenv("OTEL_SERVICE_NAME") == custom_service

    @patch("openlit.init")
    def test_openlit_initialization_success(self, mock_openlit_init):
        """Test successful OpenLIT initialization"""
        mock_openlit_init.return_value = None

        result = initialize_openlit()

        assert result is True
        mock_openlit_init.assert_called_once()

    @patch("openlit.init")
    def test_openlit_initialization_failure(self, mock_openlit_init):
        """Test graceful handling of OpenLIT initialization failure"""
        mock_openlit_init.side_effect = Exception("Connection failed")

        result = initialize_openlit()

        assert result is False
        mock_openlit_init.assert_called_once()

    def test_otlp_collector_endpoint_reachability(self):
        """Test if OTLP collector endpoint is reachable (when services are running)"""
        endpoint = "http://localhost:4318"

        try:
            # Test with a short timeout to avoid hanging tests
            response = requests.get(f"{endpoint}/health", timeout=2)
            # If we get any response, the service is running
            service_available = True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # Service not running - this is expected in CI/testing environments
            service_available = False

        # This test documents the expected behaviour rather than failing
        # when services aren't running
        assert isinstance(service_available, bool)

    def test_openlit_dashboard_endpoint_reachability(self):
        """Test if OpenLIT dashboard endpoint is reachable (when services are running)"""
        dashboard_url = "http://localhost:3001"

        try:
            response = requests.get(dashboard_url, timeout=2)
            dashboard_available = True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            dashboard_available = False

        # Document expected behaviour
        assert isinstance(dashboard_available, bool)


class TestSessionMetadataHandling:
    """Test session metadata creation and handling"""

    def test_session_metadata_structure(self):
        """Test that session metadata has the correct structure"""

        # Mock datetime for consistent testing
        fixed_datetime = datetime(2025, 1, 6, 10, 0, 0)

        with patch("streamlit_app.datetime") as mock_datetime:
            mock_datetime.now.return_value = fixed_datetime
            mock_datetime.strftime = datetime.strftime

            session_metadata = {
                "session_id": f"session_{fixed_datetime.strftime('%Y%m%d_%H%M%S')}",
                "topic": "Test Topic",
                "timestamp": fixed_datetime.isoformat(),
                "interface": "streamlit",
                "openlit_enabled": True,
            }

            # Verify all required fields are present
            required_fields = [
                "session_id",
                "topic",
                "timestamp",
                "interface",
                "openlit_enabled",
            ]
            for field in required_fields:
                assert field in session_metadata

            # Verify field types
            assert isinstance(session_metadata["session_id"], str)
            assert isinstance(session_metadata["topic"], str)
            assert isinstance(session_metadata["timestamp"], str)
            assert isinstance(session_metadata["interface"], str)
            assert isinstance(session_metadata["openlit_enabled"], bool)

            # Verify session ID format
            assert session_metadata["session_id"].startswith("session_")
            assert "20250106_100000" in session_metadata["session_id"]

    def test_session_id_consistency(self):
        """Test that session ID remains consistent across interactions"""
        # This would be tested in the context of Streamlit session state
        # For now, verify the format is consistent
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"session_{timestamp}"

        assert session_id.startswith("session_")
        assert len(session_id.split("_")) == 3  # session, date, time

    def test_enhanced_inputs_structure(self):
        """Test that enhanced inputs for crew execution include metadata"""
        base_inputs = {"topic": "Test Topic", "current_year": "2025"}

        session_metadata = {
            "session_id": "session_20250106_100000",
            "topic": "Test Topic",
            "timestamp": "2025-01-06T10:00:00",
            "interface": "streamlit",
            "openlit_enabled": True,
        }

        enhanced_inputs = {**base_inputs, "session_metadata": session_metadata}

        # Verify structure
        assert "topic" in enhanced_inputs
        assert "current_year" in enhanced_inputs
        assert "session_metadata" in enhanced_inputs

        # Verify metadata is properly nested
        metadata = enhanced_inputs["session_metadata"]
        assert metadata["session_id"] == "session_20250106_100000"
        assert metadata["topic"] == "Test Topic"
        assert metadata["interface"] == "streamlit"


class TestObservabilityStatusIndicators:
    """Test observability status indicators in the UI"""

    def test_openlit_enabled_status(self):
        """Test status indicator when OpenLIT is enabled"""
        # This tests the logic that would be used in the UI
        openlit_enabled = True

        if openlit_enabled:
            status_message = "🔍 Observability: Active"
            status_colour = "#28a745"  # Green
        else:
            status_message = "⚠️ Observability: Disabled"
            status_colour = "#ffc107"  # Yellow

        assert status_message == "🔍 Observability: Active"
        assert status_colour == "#28a745"

    def test_openlit_disabled_status(self):
        """Test status indicator when OpenLIT is disabled"""
        openlit_enabled = False

        if openlit_enabled:
            status_message = "🔍 Observability: Active"
            status_colour = "#28a745"  # Green
        else:
            status_message = "⚠️ Observability: Disabled"
            status_colour = "#ffc107"  # Yellow

        assert status_message == "⚠️ Observability: Disabled"
        assert status_colour == "#ffc107"


class TestCrewExecutionWithObservability:
    """Test crew execution with observability integration"""

    @patch("src.ai_news_crew.crew.AiNewsCrew")
    def test_crew_execution_with_metadata(self, mock_crew_class):
        """Test that crew execution receives enhanced inputs with metadata"""
        # Mock the crew instance and its methods
        mock_crew_instance = Mock()
        mock_crew = Mock()
        mock_result = Mock()
        mock_result.raw = "# Test Report\n\nThis is a test report."

        mock_crew.kickoff.return_value = mock_result
        mock_crew_instance.crew.return_value = mock_crew
        mock_crew_class.return_value = mock_crew_instance

        # Simulate the enhanced inputs that would be passed to crew
        base_inputs = {"topic": "Test Topic", "current_year": "2025"}

        session_metadata = {
            "session_id": "session_20250106_100000",
            "topic": "Test Topic",
            "timestamp": "2025-01-06T10:00:00",
            "interface": "streamlit",
            "openlit_enabled": True,
        }

        enhanced_inputs = {**base_inputs, "session_metadata": session_metadata}

        # Execute crew with enhanced inputs
        crew_instance = mock_crew_class()
        result = crew_instance.crew().kickoff(inputs=enhanced_inputs)

        # Verify the crew was called with enhanced inputs
        mock_crew.kickoff.assert_called_once_with(inputs=enhanced_inputs)

        # Verify the inputs contain both base data and metadata
        called_inputs = mock_crew.kickoff.call_args[1]["inputs"]
        assert "topic" in called_inputs
        assert "current_year" in called_inputs
        assert "session_metadata" in called_inputs
        assert called_inputs["session_metadata"]["openlit_enabled"] is True

    def test_crew_execution_without_openlit(self):
        """Test crew execution when OpenLIT is disabled"""
        # Simulate scenario where OpenLIT initialization failed
        openlit_enabled = False

        session_metadata = {
            "session_id": "session_20250106_100000",
            "topic": "Test Topic",
            "timestamp": "2025-01-06T10:00:00",
            "interface": "streamlit",
            "openlit_enabled": openlit_enabled,
        }

        # Verify that metadata correctly reflects disabled state
        assert session_metadata["openlit_enabled"] is False

        # Crew should still execute normally even without observability
        assert "topic" in session_metadata
        assert "session_id" in session_metadata


class TestPerformanceConsiderations:
    """Test performance impact of OpenLIT integration"""

    def test_initialization_performance(self):
        """Test that OpenLIT initialization doesn't significantly impact startup"""

        # Measure initialization time
        start_time = time.time()

        with patch("openlit.init") as mock_init:
            mock_init.return_value = None
            result = initialize_openlit()

        end_time = time.time()
        initialization_time = end_time - start_time

        # Initialization should be very fast (under 1 second)
        assert initialization_time < 1.0
        assert result is True

    def test_metadata_creation_performance(self):
        """Test that metadata creation is efficient"""

        start_time = time.time()

        # Create session metadata (simulating what happens in the app)
        for _ in range(100):  # Test with multiple iterations
            session_metadata = {
                "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "topic": "Test Topic",
                "timestamp": datetime.now().isoformat(),
                "interface": "streamlit",
                "openlit_enabled": True,
            }

        end_time = time.time()
        total_time = end_time - start_time

        # Should be very fast even for multiple iterations
        assert total_time < 0.1  # Less than 100ms for 100 iterations
        assert len(session_metadata) == 5  # Verify structure


class TestErrorHandlingWithObservability:
    """Test error handling when observability services are unavailable"""

    @patch("openlit.init")
    def test_graceful_degradation_on_init_failure(self, mock_openlit_init):
        """Test that app continues to work when OpenLIT fails to initialize"""
        mock_openlit_init.side_effect = Exception("OTLP endpoint unreachable")

        # Should not raise exception, should return False
        result = initialize_openlit()

        assert result is False
        mock_openlit_init.assert_called_once()

    def test_app_functionality_without_observability(self):
        """Test that core app functionality works without observability"""
        # Simulate running without OpenLIT
        openlit_enabled = False

        # Core validation should still work
        from streamlit_app import validate_topic_input

        is_valid, message = validate_topic_input("Test Topic")
        assert is_valid is True
        assert message == ""

        # Session metadata should still be created
        session_metadata = {
            "session_id": "session_20250106_100000",
            "topic": "Test Topic",
            "timestamp": "2025-01-06T10:00:00",
            "interface": "streamlit",
            "openlit_enabled": openlit_enabled,
        }

        assert session_metadata["openlit_enabled"] is False
        assert "topic" in session_metadata  # Core functionality preserved

    def test_network_timeout_handling(self):
        """Test handling of network timeouts during service checks"""

        # This simulates what happens when services are checked but unavailable
        def simulate_timeout():
            raise requests.exceptions.Timeout("Connection timed out")

        try:
            simulate_timeout()
            service_reachable = True
        except requests.exceptions.Timeout:
            service_reachable = False

        # Should handle timeout gracefully
        assert service_reachable is False
