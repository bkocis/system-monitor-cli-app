"""
Unit tests for the Config class.
"""

import glob
import json
import os
import tempfile
import unittest
import uuid

from src.system_monitor.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        # Use unique filename for each test to avoid cross-contamination
        unique_id = str(uuid.uuid4())[:8]
        self.config_file = os.path.join(self.temp_dir, f"test_config_{unique_id}.json")
        # Ensure clean state - remove any existing config file
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up any config files created during testing
        for config_file in glob.glob(os.path.join(self.temp_dir, "*.json")):
            if os.path.exists(config_file):
                os.remove(config_file)
        if os.path.exists(self.temp_dir):
            try:
                os.rmdir(self.temp_dir)
            except OSError:
                pass  # Directory not empty, that's okay

    def test_default_config_initialization(self):
        """Test initialization with default configuration."""
        config = Config(self.config_file)

        self.assertEqual(config.refresh_rate, 1.0)
        self.assertEqual(config.max_history_points, 100)
        self.assertEqual(config.temperature_warning_threshold, 70)
        self.assertEqual(config.temperature_critical_threshold, 80)

    def test_config_file_creation(self):
        """Test that config file is created if it doesn't exist."""
        config = Config(self.config_file)
        config.save_config()

        self.assertTrue(os.path.exists(self.config_file))

    def test_config_file_loading(self):
        """Test loading configuration from existing file."""
        # Create a test config file
        test_config = {
            "refresh_rate": 2.0,
            "max_history_points": 150,
            "temperature_thresholds": {"warning": 75, "critical": 85},
        }

        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        config = Config(self.config_file)

        self.assertEqual(config.refresh_rate, 2.0)
        self.assertEqual(config.max_history_points, 150)
        self.assertEqual(config.temperature_warning_threshold, 75)
        self.assertEqual(config.temperature_critical_threshold, 85)

    def test_config_get_set(self):
        """Test get and set methods with dot notation."""
        config = Config(self.config_file)

        # Test getting existing values
        self.assertEqual(config.get("refresh_rate"), 1.0)
        self.assertEqual(config.get("temperature_thresholds.warning"), 70)

        # Test getting non-existent values
        self.assertIsNone(config.get("non_existent_key"))
        self.assertEqual(config.get("non_existent_key", "default"), "default")

        # Test setting values
        config.set("refresh_rate", 2.5)
        config.set("temperature_thresholds.warning", 75)

        self.assertEqual(config.get("refresh_rate"), 2.5)
        self.assertEqual(config.get("temperature_thresholds.warning"), 75)

    def test_config_merge_with_defaults(self):
        """Test that loaded config merges with defaults."""
        # Create partial config file
        test_config = {"refresh_rate": 3.0, "display": {"show_gpu": False}}

        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        config = Config(self.config_file)

        # Should have the custom value
        self.assertEqual(config.refresh_rate, 3.0)
        self.assertEqual(config.get("display.show_gpu"), False)

        # Should still have default values for missing keys
        self.assertEqual(config.max_history_points, 100)
        self.assertEqual(config.temperature_warning_threshold, 70)
        self.assertEqual(config.get("display.show_network"), False)

    def test_invalid_config_file(self):
        """Test handling of invalid JSON config file."""
        # Create invalid JSON file
        with open(self.config_file, "w") as f:
            f.write("invalid json content")

        config = Config(self.config_file)

        # Should fall back to defaults
        self.assertEqual(config.refresh_rate, 1.0)
        self.assertEqual(config.max_history_points, 100)

    def test_properties(self):
        """Test configuration properties."""
        config = Config(self.config_file)

        self.assertIsInstance(config.refresh_rate, float)
        self.assertIsInstance(config.max_history_points, int)
        self.assertIsInstance(config.temperature_warning_threshold, int)
        self.assertIsInstance(config.temperature_critical_threshold, int)

        # Test that properties match get() method
        self.assertEqual(config.refresh_rate, config.get("refresh_rate"))
        self.assertEqual(config.max_history_points, config.get("max_history_points"))


if __name__ == "__main__":
    unittest.main()
