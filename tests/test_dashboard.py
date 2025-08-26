"""
Unit tests for the SystemDashboard class.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.system_monitor.dashboard import SystemDashboard


class TestSystemDashboard(unittest.TestCase):
    """Test cases for SystemDashboard class."""

    def setUp(self):
        """Set up test fixtures."""
        self.dashboard = SystemDashboard()

    def test_init(self):
        """Test dashboard initialization."""
        self.assertIsNotNone(self.dashboard.console)
        self.assertIn("gpu", self.dashboard.temp_history)
        self.assertIn("cpu", self.dashboard.temp_history)
        self.assertEqual(self.dashboard.temp_history["gpu"], [])
        self.assertEqual(self.dashboard.temp_history["cpu"], [])

    @patch("subprocess.check_output")
    def test_get_gpu_temp_success(self, mock_subprocess):
        """Test successful GPU temperature retrieval."""
        mock_subprocess.return_value = "GPU Core Temperature: 65.0 C"
        temp = self.dashboard.get_gpu_temp()
        self.assertEqual(temp, 65)

    @patch("subprocess.check_output")
    def test_get_gpu_temp_failure(self, mock_subprocess):
        """Test GPU temperature retrieval failure."""
        mock_subprocess.side_effect = Exception("Command failed")
        temp = self.dashboard.get_gpu_temp()
        self.assertIsNone(temp)

    @patch("subprocess.check_output")
    def test_get_cpu_temp_success(self, mock_subprocess):
        """Test successful CPU temperature retrieval."""
        mock_subprocess.return_value = """
        coretemp-isa-0000
        Core 0:       +45.0°C  (high = +100.0°C, crit = +100.0°C)
        Core 1:       +47.0°C  (high = +100.0°C, crit = +100.0°C)
        """
        temp = self.dashboard.get_cpu_temp()
        self.assertEqual(temp, 46)  # Average of 45 and 47

    @patch("subprocess.check_output")
    def test_get_cpu_temp_failure(self, mock_subprocess):
        """Test CPU temperature retrieval failure."""
        mock_subprocess.side_effect = Exception("sensors not found")
        temp = self.dashboard.get_cpu_temp()
        self.assertIsNone(temp)

    def test_update_temperature_history(self):
        """Test temperature history update."""
        self.dashboard.update_temperature_history(65, 45)

        self.assertEqual(len(self.dashboard.temp_history["gpu"]), 1)
        self.assertEqual(len(self.dashboard.temp_history["cpu"]), 1)

        self.assertEqual(self.dashboard.temp_history["gpu"][0][1], 65)
        self.assertEqual(self.dashboard.temp_history["cpu"][0][1], 45)

    def test_update_temperature_history_none_values(self):
        """Test temperature history update with None values."""
        self.dashboard.update_temperature_history(None, None)

        self.assertEqual(len(self.dashboard.temp_history["gpu"]), 0)
        self.assertEqual(len(self.dashboard.temp_history["cpu"]), 0)

    def test_temperature_history_max_points(self):
        """Test that temperature history respects max points limit."""
        # Set a small limit for testing
        original_max = self.dashboard.max_history_points
        self.dashboard.max_history_points = 3

        # Add more points than the limit
        for i in range(5):
            self.dashboard.update_temperature_history(60 + i, 40 + i)

        # Should only keep the last 3 points
        self.assertEqual(len(self.dashboard.temp_history["gpu"]), 3)
        self.assertEqual(len(self.dashboard.temp_history["cpu"]), 3)

        # Check that it kept the latest values
        self.assertEqual(self.dashboard.temp_history["gpu"][-1][1], 64)
        self.assertEqual(self.dashboard.temp_history["cpu"][-1][1], 44)

        # Restore original max
        self.dashboard.max_history_points = original_max

    def test_format_bytes(self):
        """Test byte formatting."""
        self.assertEqual(self.dashboard.format_bytes(1024), "1.0 KB")
        self.assertEqual(self.dashboard.format_bytes(1048576), "1.0 MB")
        self.assertEqual(self.dashboard.format_bytes(1073741824), "1.0 GB")

    def test_format_bytes_exact(self):
        """Test exact byte formatting with commas."""
        self.assertEqual(self.dashboard.format_bytes_exact(1024), "1,024")
        self.assertEqual(self.dashboard.format_bytes_exact(1048576), "1,048,576")

    def test_format_bytes_gb(self):
        """Test GB formatting."""
        self.assertEqual(self.dashboard.format_bytes_gb(1073741824), "1G")
        self.assertEqual(self.dashboard.format_bytes_gb(2147483648), "2G")

    def test_get_color_for_percentage(self):
        """Test color selection based on percentage."""
        self.assertEqual(self.dashboard.get_color_for_percentage(30), "green")
        self.assertEqual(self.dashboard.get_color_for_percentage(60), "yellow")
        self.assertEqual(self.dashboard.get_color_for_percentage(80), "red")

    @patch("psutil.cpu_percent")
    @patch("psutil.cpu_count")
    @patch("psutil.cpu_freq")
    def test_get_cpu_info(self, mock_freq, mock_count, mock_percent):
        """Test CPU information retrieval."""
        mock_percent.return_value = 45.0
        mock_count.return_value = 8
        mock_freq.return_value = MagicMock()
        mock_freq.return_value._asdict.return_value = {"current": 2400.0}

        cpu_info = self.dashboard.get_cpu_info()

        self.assertEqual(cpu_info["percent"], 45.0)
        self.assertEqual(cpu_info["count"], 8)
        self.assertIsNotNone(cpu_info["freq"])

    @patch("psutil.virtual_memory")
    @patch("psutil.swap_memory")
    def test_get_memory_info(self, mock_swap, mock_virtual):
        """Test memory information retrieval."""
        mock_virtual.return_value = MagicMock(
            total=8589934592,  # 8GB
            available=4294967296,  # 4GB
            percent=50.0,
            used=4294967296,  # 4GB
        )
        mock_swap.return_value = MagicMock(
            total=2147483648,  # 2GB
            used=1073741824,  # 1GB
            percent=50.0,
        )

        mem_info = self.dashboard.get_memory_info()

        self.assertEqual(mem_info["total"], 8589934592)
        self.assertEqual(mem_info["percent"], 50.0)
        self.assertEqual(mem_info["swap_total"], 2147483648)

    def test_create_temperature_graph_no_data(self):
        """Test temperature graph creation with no data."""
        graph = self.dashboard.create_temperature_graph("cpu")
        # Should return a Text object indicating no data
        self.assertIsNotNone(graph)

    def test_create_temperature_graph_with_data(self):
        """Test temperature graph creation with data."""
        # Add some test data
        self.dashboard.update_temperature_history(65, 45)
        self.dashboard.update_temperature_history(67, 47)
        self.dashboard.update_temperature_history(70, 50)

        graph = self.dashboard.create_temperature_graph("cpu")
        self.assertIsNotNone(graph)


if __name__ == "__main__":
    unittest.main()
