#!/usr/bin/env python3

import re
import subprocess
import time
from datetime import datetime

import psutil
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import config


class SystemDashboard:
    def __init__(self):
        self.console = Console()
        # Temperature history storage (last 60 readings)
        self.temp_history = {
            "gpu": [],  # List of (timestamp, temperature) tuples
            "cpu": [],  # List of (timestamp, temperature) tuples
        }
        self.max_history_points = config.max_history_points

    def get_gpu_temp(self):
        """Get GPU temperature using nvidia-settings (same approach as gpu_temp_monitor.sh)"""
        try:
            output = subprocess.check_output(
                ["nvidia-settings", "-q", "[gpu:0]/GPUCoreTemp"],
                stderr=subprocess.STDOUT,
                text=True,
            )
            # Extract temperature after colon and before period
            temp_match = re.search(r":\s*(\d+)\.", output)
            return int(temp_match.group(1)) if temp_match else None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception):
            return None

    def get_gpu_info(self):
        """Get detailed GPU information using nvidia-smi"""
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw",
                    "--format=csv,noheader,nounits",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                data = result.stdout.strip().split(", ")
                if len(data) >= 6:
                    return {
                        "name": data[0],
                        "temperature": int(data[1]) if data[1].isdigit() else None,
                        "utilization": int(data[2]) if data[2].isdigit() else None,
                        "memory_used": int(data[3]) if data[3].isdigit() else None,
                        "memory_total": int(data[4]) if data[4].isdigit() else None,
                        "power_draw": float(data[5])
                        if data[5].replace(".", "").isdigit()
                        else None,
                    }
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception):
            pass
        return {}

    def get_cpu_temp(self):
        """Get CPU temperature using sensors (same approach as existing scripts)"""
        try:
            output = subprocess.check_output(["sensors"], text=True)
            temps = []
            for line in output.split("\n"):
                if "Core" in line and "+" in line:
                    temp_match = re.search(r"\+(\d+)", line)
                    if temp_match:
                        temps.append(int(temp_match.group(1)))
            return sum(temps) // len(temps) if temps else None
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception):
            return None

    def update_temperature_history(self, gpu_temp, cpu_temp):
        """Update temperature history with current readings"""
        current_time = time.time()

        # Update GPU temperature history
        if gpu_temp is not None:
            self.temp_history["gpu"].append((current_time, gpu_temp))
            # Keep only the last max_history_points readings
            if len(self.temp_history["gpu"]) > self.max_history_points:
                self.temp_history["gpu"] = self.temp_history["gpu"][
                    -self.max_history_points :
                ]

        # Update CPU temperature history
        if cpu_temp is not None:
            self.temp_history["cpu"].append((current_time, cpu_temp))
            # Keep only the last max_history_points readings
            if len(self.temp_history["cpu"]) > self.max_history_points:
                self.temp_history["cpu"] = self.temp_history["cpu"][
                    -self.max_history_points :
                ]

    def create_temperature_graph(self, temp_type, height=8, length=100):
        """Create a simple text-based temperature graph"""
        if temp_type not in self.temp_history or not self.temp_history[temp_type]:
            return Text("No data available", style="dim")

        history = self.temp_history[temp_type]
        if len(history) < 2:
            return Text("Collecting data...", style="dim")

        # Extract temperatures
        temps = [temp for _, temp in history]
        min_temp = min(temps)
        max_temp = max(temps)

        # Avoid division by zero
        if max_temp == min_temp:
            temp_range = 1
        else:
            temp_range = max_temp - min_temp

        # Create the graph using Text object with proper styling
        graph_text = Text()

        for i in range(height):
            threshold = min_temp + (temp_range * (height - i - 1) / height)

            # Add temperature scale on the left
            temp_label = f"{threshold:.0f}° "
            graph_text.append(temp_label, style="dim")

            # Build the line for this height level
            for _, temp in history[-length:]:  # Show last length points
                if temp >= threshold:
                    if temp >= config.temperature_critical_threshold:
                        graph_text.append("█", style="red")
                    elif temp >= config.temperature_warning_threshold:
                        graph_text.append("█", style="yellow")
                    else:
                        graph_text.append("█", style="green")
                else:
                    graph_text.append(" ")

            graph_text.append("\n")

        # Add timeline at bottom
        if len(history) >= 10:
            for i in range(min(length, len(history))):
                if i % 10 == 0:
                    graph_text.append("│", style="dim")
                else:
                    graph_text.append("─", style="dim")
            graph_text.append(f" {len(history)}s", style="dim")
            graph_text.append("\n")

        # Add current temp info
        current_temp = temps[-1]
        if current_temp < config.temperature_warning_threshold:
            temp_color = "green"
        elif current_temp < config.temperature_critical_threshold:
            temp_color = "yellow"
        else:
            temp_color = "red"

        graph_text.append("Current: ", style="dim")
        graph_text.append(f"{current_temp}°C", style=temp_color)
        graph_text.append(f" | Min: {min_temp}° | Max: {max_temp}°", style="dim")

        return graph_text

    def get_memory_info(self):
        """Get memory information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
            "used": mem.used,
            "swap_total": swap.total,
            "swap_used": swap.used,
            "swap_percent": swap.percent,
        }

    def get_disk_info(self):
        """Get disk information"""
        disks = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disks.append(
                    {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": partition_usage.total,
                        "used": partition_usage.used,
                        "free": partition_usage.free,
                        "percent": partition_usage.percent,
                    }
                )
            except PermissionError:
                continue
        return disks

    def get_cpu_info(self):
        """Get CPU information"""
        return {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        }

    def get_network_info(self):
        """Get network information"""
        stats = psutil.net_io_counters()
        return {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
        }

    def format_bytes(self, bytes_value):
        """Format bytes to human readable format"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def format_bytes_exact(self, bytes_value):
        """Format bytes as exact number with comma separators"""
        return f"{bytes_value:,}"

    def format_bytes_gb(self, bytes_value):
        """Format bytes to GB with one decimal place"""
        gb_value = bytes_value / (1024**3)
        return f"{gb_value:.0f}G"

    def get_color_for_percentage(self, percent):
        """Get color based on percentage"""
        if percent < 50:
            return "green"
        elif percent < 75:
            return "yellow"
        else:
            return "red"

    def create_dashboard(self):
        """Create the main dashboard"""

        # Get system information
        gpu_temp = self.get_gpu_temp()
        gpu_info = self.get_gpu_info()
        cpu_temp = self.get_cpu_temp()
        cpu_info = self.get_cpu_info()
        memory_info = self.get_memory_info()
        disk_info = self.get_disk_info()


        # Update temperature history
        self.update_temperature_history(gpu_temp, cpu_temp)

        # Header
        header_text = Text("🖥️  SYSTEM DASHBOARD", style="bold blue")
        header_text.append(
            f"  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="dim"
        )
        header_panel = Panel(header_text, style="blue")

        # Combined Temperature Panel with Current Values and History
        # Calculate available width for temperature graphs
        console_width = self.console.size.width
        # Account for panel borders (2), metric column (~12), current temp column (~12), and padding (~6)
        available_graph_width = max(50, console_width - 32)

        # Current temperature table
        temp_table = Table(show_header=False, box=None)
        temp_table.add_column("Metric", style="bold", width=12)
        temp_table.add_column("Current", justify="center", width=12)
        temp_table.add_column("History Graph", justify="left")

        # CPU row with current temp and history
        if cpu_temp is not None:
            cpu_color = self.get_color_for_percentage(
                cpu_temp * 100 / 90
            )  # assuming 90°C as max
            cpu_current = f"[{cpu_color}]{cpu_temp}°C[/{cpu_color}]"
        else:
            cpu_current = "[red]N/A[/red]"

        cpu_temp_graph = self.create_temperature_graph(
            "cpu", height=6, length=available_graph_width
        )
        temp_table.add_row("🏭 CPU:", cpu_current, cpu_temp_graph)

        # GPU row with current temp and history
        if gpu_temp is not None:
            gpu_color = self.get_color_for_percentage(
                gpu_temp * 100 / 90
            )  # assuming 90°C as max
            gpu_current = f"[{gpu_color}]{gpu_temp}°C[/{gpu_color}]"
        else:
            gpu_current = "[red]N/A[/red]"

        gpu_temp_graph = self.create_temperature_graph(
            "gpu", height=6, length=available_graph_width
        )
        temp_table.add_row("🎮 GPU:", gpu_current, gpu_temp_graph)

        temp_panel = Panel(temp_table, title="🌡️  Temperatures & History", style="cyan")

        # System Info Panel
        sys_table = Table(show_header=False, box=None)
        sys_table.add_column("Metric", style="bold")
        sys_table.add_column("Value")

        cpu_color = self.get_color_for_percentage(cpu_info["percent"])
        sys_table.add_row(
            "💻 CPU Usage:", f"[{cpu_color}]{cpu_info['percent']:.1f}%[/{cpu_color}]"
        )
        sys_table.add_row("🔢 CPU Cores:", f"{cpu_info['count']}")

        mem_color = self.get_color_for_percentage(memory_info["percent"])
        sys_table.add_row(
            "🧠 Memory:", f"[{mem_color}]{memory_info['percent']:.1f}%[/{mem_color}]"
        )
        sys_table.add_row(
            "📦 Used/Total:",
            f"{self.format_bytes(memory_info['used'])} / {self.format_bytes(memory_info['total'])}",
        )

        sys_panel = Panel(sys_table, title="💾 System Info", style="green")

        # GPU Info Panel
        gpu_table = Table(show_header=False, box=None)
        gpu_table.add_column("Metric", style="bold")
        gpu_table.add_column("Value")

        if gpu_info:
            gpu_table.add_row("🎮 GPU:", gpu_info.get("name", "Unknown"))
            if gpu_info.get("utilization") is not None:
                util_color = self.get_color_for_percentage(gpu_info["utilization"])
                gpu_table.add_row(
                    "⚡ Usage:",
                    f"[{util_color}]{gpu_info['utilization']}%[/{util_color}]",
                )
            if (
                gpu_info.get("memory_used") is not None
                and gpu_info.get("memory_total") is not None
            ):
                mem_percent = (gpu_info["memory_used"] / gpu_info["memory_total"]) * 100
                mem_color = self.get_color_for_percentage(mem_percent)
                gpu_table.add_row(
                    "🧠 VRAM:",
                    f"[{mem_color}]{gpu_info['memory_used']}MB / {gpu_info['memory_total']}MB[/{mem_color}]",
                )
            if gpu_info.get("power_draw") is not None:
                gpu_table.add_row("⚡ Power:", f"{gpu_info['power_draw']:.1f}W")
        else:
            gpu_table.add_row("🎮 GPU:", "[red]Not detected[/red]")

        gpu_panel = Panel(gpu_table, title="🎮 GPU Info", style="magenta")

        # Disk Info Panel - Exact Bytes
        disk_bytes_table = Table(show_header=True, box=None, title="Mem usage [%]")
        disk_bytes_table.add_column("Filesystem", style="bold")
        disk_bytes_table.add_column("Size", justify="right")
        disk_bytes_table.add_column("Used", justify="right")
        disk_bytes_table.add_column("Avail", justify="right")
        disk_bytes_table.add_column("Use%", justify="right")
        disk_bytes_table.add_column("Mounted on")

        # Disk Info Panel - GB Format
        disk_gb_table = Table(show_header=True, box=None, title="Mounted drives")
        disk_gb_table.add_column("Filesystem", style="bold")
        disk_gb_table.add_column("Size", justify="right")
        disk_gb_table.add_column("Used", justify="right")
        disk_gb_table.add_column("Avail", justify="right")
        disk_gb_table.add_column("Use%", justify="right")
        disk_gb_table.add_column("Mounted on")

        for disk in disk_info:  # Show real physical drives only
            # Filter out loop devices and virtual filesystems
            device_name = disk["device"]
            mountpoint = disk["mountpoint"]
            if (
                device_name.startswith("/dev/loop")
                or device_name.startswith("/dev/snap")
                or disk["fstype"]
                in [
                    "tmpfs",
                    "devtmpfs",
                    "sysfs",
                    "proc",
                    "cgroup",
                    "devpts",
                    "securityfs",
                    "pstore",
                    "efivarfs",
                    "bpf",
                    "cgroup2",
                    "configfs",
                    "debugfs",
                    "tracefs",
                    "fusectl",
                    "mqueue",
                    "hugetlbfs",
                ]
                or mountpoint.startswith("/sys")
                or mountpoint.startswith("/proc")
                or mountpoint.startswith("/dev")
                or mountpoint.startswith("/run")
                or mountpoint.startswith("/snap")
                or mountpoint.startswith("/var/snap/")
                or mountpoint == "/boot/efi"
                or mountpoint.startswith("/boot/efi")
            ):
                continue

            color = self.get_color_for_percentage(disk["percent"])

            # Add to exact bytes table
            disk_bytes_table.add_row(
                disk["device"],
                self.format_bytes_exact(disk["total"]),
                self.format_bytes_exact(disk["used"]),
                self.format_bytes_exact(disk["free"]),
                f"[{color}]{disk['percent']:.0f}%[/{color}]",
                disk["mountpoint"],
            )

            # Add to GB table
            disk_gb_table.add_row(
                disk["device"],
                self.format_bytes_gb(disk["total"]),
                self.format_bytes_gb(disk["used"]),
                self.format_bytes_gb(disk["free"]),
                f"[{color}]{disk['percent']:.0f}%[/{color}]",
                disk["mountpoint"],
            )

        # Combine both tables vertically
        disk_combined = Group(disk_bytes_table, "", disk_gb_table)
        disk_panel = Panel(disk_combined, title="💿 Disk Usage", style="yellow")

        # Footer
        footer_text = Text("Press Ctrl+C to exit", style="dim")
        footer_panel = Panel(footer_text, style="dim")

        # Combine everything vertically in the requested order:
        # 1. Combined temperature block with current values and history
        # 2. System information
        # 3. GPU information
        # 4. Disk usage at the bottom
        dashboard = Group(
            header_panel, temp_panel, sys_panel, gpu_panel, disk_panel, footer_panel
        )

        return dashboard

    def run(self):
        """Run the dashboard"""
        try:
            refresh_rate = 1.0 / config.refresh_rate if config.refresh_rate > 0 else 1.0
            with Live(
                self.create_dashboard(), refresh_per_second=refresh_rate, screen=True
            ) as live:
                while True:
                    time.sleep(config.refresh_rate)
                    live.update(self.create_dashboard())
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Dashboard stopped.[/bold red]")


if __name__ == "__main__":
    dashboard = SystemDashboard()
    dashboard.run()
