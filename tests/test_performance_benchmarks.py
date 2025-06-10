"""
Performance benchmarks for OpenLIT integration
"""

import time
from datetime import datetime
from unittest.mock import Mock, patch

from streamlit_app import initialize_openlit, validate_topic_input


class TestPerformanceBenchmarks:
    """Performance benchmarks to ensure OpenLIT integration doesn't degrade performance"""

    def test_baseline_app_startup_time(self):
        """Benchmark baseline app startup time without OpenLIT"""
        start_time = time.time()

        # Simulate basic app initialization without OpenLIT
        with patch("openlit.init") as mock_init:
            mock_init.side_effect = Exception("Disabled for benchmark")

            # Basic validation function (core app functionality)
            is_valid, message = validate_topic_input("Test Topic")
            assert is_valid is True

        end_time = time.time()
        baseline_time = end_time - start_time

        # Should be very fast (under 10ms)
        assert baseline_time < 0.01

    def test_openlit_startup_overhead(self):
        """Benchmark OpenLIT initialization overhead"""
        start_time = time.time()

        with patch("openlit.init") as mock_init:
            mock_init.return_value = None
            result = initialize_openlit()

        end_time = time.time()
        openlit_time = end_time - start_time

        # OpenLIT initialization should be fast (under 100ms)
        assert openlit_time < 0.1
        assert result is True

    def test_session_metadata_creation_performance(self):
        """Benchmark session metadata creation performance"""
        iterations = 1000
        start_time = time.time()

        for i in range(iterations):
            session_metadata = {
                "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}",
                "topic": f"Test Topic {i}",
                "timestamp": datetime.now().isoformat(),
                "interface": "streamlit",
                "openlit_enabled": True,
            }

        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_creation = total_time / iterations

        # Should be very fast per creation (under 1ms each)
        assert avg_time_per_creation < 0.001
        assert total_time < 1.0  # Total time under 1 second for 1000 iterations

    def test_input_validation_performance(self):
        """Benchmark input validation performance"""
        test_topics = [
            "AI and Machine Learning",
            "Quantum Computing Advances",
            "Climate Change Solutions",
            "Space Exploration Technologies",
            "Renewable Energy Systems",
        ]

        iterations = 100
        start_time = time.time()

        for _ in range(iterations):
            for topic in test_topics:
                is_valid, message = validate_topic_input(topic)
                assert is_valid is True

        end_time = time.time()
        total_time = end_time - start_time
        total_validations = iterations * len(test_topics)
        avg_time_per_validation = total_time / total_validations

        # Should be very fast per validation (under 0.1ms each)
        assert avg_time_per_validation < 0.0001

    def test_mock_crew_execution_performance(self):
        """Benchmark mock crew execution with observability metadata"""
        from src.ai_news_crew.crew import AiNewsCrew

        with patch.object(AiNewsCrew, "crew") as mock_crew_method:
            mock_crew = Mock()
            mock_result = Mock()
            mock_result.raw = "# Test Report\n\nThis is a test report."
            mock_crew.kickoff.return_value = mock_result
            mock_crew_method.return_value = mock_crew

            # Prepare inputs with metadata
            base_inputs = {"topic": "Test Topic", "current_year": "2025"}
            session_metadata = {
                "session_id": "session_20250106_100000",
                "topic": "Test Topic",
                "timestamp": "2025-01-06T10:00:00",
                "interface": "streamlit",
                "openlit_enabled": True,
            }
            enhanced_inputs = {**base_inputs, "session_metadata": session_metadata}

            # Benchmark execution
            start_time = time.time()

            crew_instance = AiNewsCrew()
            result = crew_instance.crew().kickoff(inputs=enhanced_inputs)

            end_time = time.time()
            execution_time = end_time - start_time

            # Mock execution should be very fast (under 10ms)
            assert execution_time < 0.01
            assert hasattr(result, "raw")

    def test_memory_usage_estimation(self):
        """Estimate memory usage of session metadata"""
        import sys

        # Create session metadata
        session_metadata = {
            "session_id": "session_20250106_100000",
            "topic": "Test Topic for Memory Usage Testing",
            "timestamp": "2025-01-06T10:00:00.123456",
            "interface": "streamlit",
            "openlit_enabled": True,
        }

        # Estimate memory usage (rough approximation)
        metadata_size = sys.getsizeof(session_metadata)
        for key, value in session_metadata.items():
            metadata_size += sys.getsizeof(key) + sys.getsizeof(value)

        # Should be reasonable memory usage (under 1KB per session)
        assert metadata_size < 1024  # Less than 1KB

    def test_concurrent_session_simulation(self):
        """Simulate multiple concurrent sessions for performance testing"""
        import queue
        import threading

        num_sessions = 10
        results_queue = queue.Queue()

        def simulate_session(session_id):
            start_time = time.time()

            # Simulate session metadata creation
            session_metadata = {
                "session_id": f"session_{session_id}",
                "topic": f"Test Topic {session_id}",
                "timestamp": datetime.now().isoformat(),
                "interface": "streamlit",
                "openlit_enabled": True,
            }

            # Simulate input validation
            is_valid, message = validate_topic_input(session_metadata["topic"])

            end_time = time.time()
            session_time = end_time - start_time

            results_queue.put(
                {
                    "session_id": session_id,
                    "execution_time": session_time,
                    "validation_result": is_valid,
                }
            )

        # Create and start threads
        threads = []
        start_time = time.time()

        for i in range(num_sessions):
            thread = threading.Thread(target=simulate_session, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        end_time = time.time()
        total_time = end_time - start_time

        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Verify all sessions completed successfully
        assert len(results) == num_sessions
        for result in results:
            assert result["validation_result"] is True
            assert result["execution_time"] < 0.01  # Each session under 10ms

        # Total time should be reasonable (under 1 second for 10 concurrent sessions)
        assert total_time < 1.0

    def test_performance_regression_detection(self):
        """Test to detect performance regressions in future changes"""
        # This test establishes performance baselines by running other tests

        # Run baseline measurements (these will assert their own performance thresholds)
        self.test_baseline_app_startup_time()
        self.test_openlit_startup_overhead()
        self.test_session_metadata_creation_performance()
        self.test_input_validation_performance()

        # If we reach here, all performance tests passed
        assert True


class TestResourceUsageBenchmarks:
    """Test resource usage patterns with OpenLIT integration"""

    def test_environment_variable_impact(self):
        """Test impact of environment variable configuration"""
        import os

        # Count initial environment variables
        initial_env_count = len(os.environ)

        # Initialize OpenLIT (which sets environment variables)
        with patch("openlit.init") as mock_init:
            mock_init.return_value = None
            initialize_openlit()

        # Count environment variables after initialization
        final_env_count = len(os.environ)

        # Should only add a few environment variables
        added_vars = final_env_count - initial_env_count
        assert added_vars <= 5  # Should add at most 5 environment variables

        # Verify expected variables are set
        expected_vars = [
            "OTEL_EXPORTER_OTLP_ENDPOINT",
            "OTEL_TRACES_SAMPLER",
            "OTEL_TRACES_SAMPLER_ARG",
            "OTEL_SERVICE_NAME",
        ]

        for var in expected_vars:
            assert os.getenv(var) is not None

        # Environment variable impact is acceptable
        assert True

    def test_string_processing_performance(self):
        """Test string processing performance for topics and metadata"""
        import random
        import string

        # Generate test topics of various lengths
        test_cases = []
        for length in [10, 50, 100, 200]:  # Different topic lengths
            topic = "".join(
                random.choices(string.ascii_letters + string.digits + " ", k=length)
            )
            test_cases.append(topic.strip())

        start_time = time.time()

        # Test validation performance across different topic lengths
        for topic in test_cases:
            is_valid, message = validate_topic_input(topic)
            # All should be valid (within length limits and no special characters)

        end_time = time.time()
        total_time = end_time - start_time

        # Should handle various string lengths efficiently
        assert total_time < 0.01  # Under 10ms for all test cases

        # String processing performance is acceptable
        assert True
