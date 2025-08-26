# 🖥️ System Monitor CLI Dashboard

A beautiful, real-time system monitoring dashboard for the terminal that provides comprehensive insights into your system's performance with live temperature graphs, resource usage, and hardware information.

## ✨ Features

### 🌡️ **Temperature Monitoring & History**
- **Real-time temperature tracking** for CPU and GPU
- **Visual temperature graphs** with 100-point history
- **Color-coded alerts** (green/yellow/red based on temperature thresholds)
- **Historical trends** showing temperature patterns over time

### 💻 **System Resource Monitoring**
- **CPU usage** with percentage and core count
- **Memory usage** with detailed used/total breakdown
- **Real-time updates** every second
- **Percentage-based color coding** for quick status assessment

### 🎮 **GPU Information**
- **NVIDIA GPU support** with detailed metrics
- **GPU utilization** and temperature monitoring
- **VRAM usage** (used/total memory)
- **Power consumption** tracking
- **GPU model identification**

### 💿 **Disk Usage Analysis**
- **Multiple filesystem support** with smart filtering
- **Dual view modes**: exact bytes and GB format
- **Mounted drive information** with usage percentages
- **Automatic filtering** of virtual/temporary filesystems

### 🎨 **Beautiful Terminal UI**
- **Rich formatting** with colors, emojis, and proper alignment
- **Live dashboard** with smooth updates
- **Responsive layout** that adapts to terminal size
- **Professional panels** with clear section organization

## 🔧 Requirements

### System Requirements
- **Linux** (tested on Ubuntu/Debian-based systems)
- **Python 3.12+**
- **NVIDIA GPU** (optional, for GPU monitoring features)

### Software Dependencies
- `nvidia-settings` and `nvidia-smi` (for GPU monitoring)
- `sensors` command (for CPU temperature - usually from `lm-sensors` package)
- `psutil` Python library
- `rich` Python library

### Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install lm-sensors nvidia-utils-* python3.12 python3.12-venv

# Initialize sensors (run once)
sudo sensors-detect --auto
```

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
# Clone or download the project
git clone <your-repo-url>
cd system-monitor-cli-app

# Run the dashboard (automatically sets up everything)
./run_dashboard.sh
```

### Option 2: Terminal Window Launch
```bash
# Launch in a dedicated terminal window
./monitoring_terms.sh
```

### Option 3: Manual Setup
```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install "rich>=13.0.0" "psutil>=5.8.0"

# Run dashboard
python system_dashboard.py
```

## 📊 Dashboard Layout

The dashboard displays information in the following order:

```
🖥️  SYSTEM DASHBOARD  |  2024-01-15 14:30:25
┌─────────────────────────────────────────────┐

🌡️  Temperatures & History
┌─────────────────────────────────────────────┐
│ 🏭 CPU:    72°C    [Temperature Graph]     │
│ 🎮 GPU:    65°C    [Temperature Graph]     │
└─────────────────────────────────────────────┘

💾 System Info                🎮 GPU Info
┌─────────────────┐          ┌─────────────────┐
│ 💻 CPU Usage: 45%│          │ 🎮 GPU: RTX 4090│
│ 🔢 CPU Cores: 16│          │ ⚡ Usage: 23%   │
│ 🧠 Memory: 67%  │          │ 🧠 VRAM: 2.1GB  │
│ 📦 Used: 32GB   │          │ ⚡ Power: 180W  │
└─────────────────┘          └─────────────────┘

💿 Disk Usage
┌─────────────────────────────────────────────┐
│ Filesystem    Size      Used      Avail  Use%│
│ /dev/sda1     500GB     350GB     150GB   70%│
│ /dev/sdb1     1TB       200GB     800GB   20%│
└─────────────────────────────────────────────┘

Press Ctrl+C to exit
```

## 🎯 Use Cases

### 🔥 **System Performance Monitoring**
- Monitor system health during intensive tasks
- Track temperature trends during gaming or rendering
- Identify resource bottlenecks in real-time

### 🎮 **Gaming & Content Creation**
- Keep eye on GPU temperatures during gaming sessions
- Monitor VRAM usage for optimal game settings
- Track power consumption for efficiency optimization

### 🖥️ **Server Administration**
- Monitor headless servers via SSH
- Track resource usage trends over time
- Quick system health checks

### 🔧 **Development & Testing**
- Monitor resource usage during builds/tests
- Profile application performance impact
- Debug memory leaks and CPU spikes

### ⚡ **Overclocking & Tuning**
- Monitor temperatures during stress testing
- Track performance metrics after hardware changes
- Validate cooling solutions effectiveness

## 🎨 Visual Features

### Temperature Graphs
- **Real-time ASCII graphs** showing temperature trends
- **Color coding**: Green (cool), Yellow (warm), Red (hot)
- **Historical data** with min/max temperature display
- **Adaptive scaling** based on temperature range

### Color-Coded Metrics
- **Green**: Normal operation (< 50% usage, < 70°C)
- **Yellow**: Moderate load (50-75% usage, 70-80°C)  
- **Red**: High load/temperature (> 75% usage, > 80°C)

## ⚙️ Configuration

### Customizing Update Frequency
Edit `system_dashboard.py` line 404:
```python
with Live(self.create_dashboard(), refresh_per_second=2):  # 2Hz instead of 1Hz
```

### Adjusting Temperature History
Edit `system_dashboard.py` line 25:
```python
self.max_history_points = 200  # Keep 200 points instead of 100
```

### Terminal Window Settings
Edit `monitoring_terms.sh` to customize terminal appearance:
```bash
xfce4-terminal --command "bash $SCRIPT_DIR/run_dashboard.sh" \
  --hide-borders \
  --geometry 220x48+200+50 \  # Width x Height + X + Y position
  --hide-scrollbar
```

## 🛠️ Troubleshooting

### GPU Not Detected
```bash
# Check NVIDIA drivers
nvidia-smi

# Install nvidia-utils if missing
sudo apt install nvidia-utils-*
```

### Temperature Sensors Not Working
```bash
# Detect sensors
sudo sensors-detect --auto

# Test sensors
sensors
```

### Permission Issues
```bash
# Make scripts executable
chmod +x run_dashboard.sh monitoring_terms.sh system_dashboard.py
```

### Virtual Environment Issues
```bash
# Remove and recreate venv
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install rich psutil
```

## 🔍 Technical Details

### Architecture
- **Python 3.12** with modern async-friendly design
- **Rich library** for terminal UI rendering
- **psutil** for cross-platform system metrics
- **subprocess** calls for hardware-specific tools

### Performance
- **Minimal CPU overhead** (~1-2% CPU usage)
- **Memory efficient** (~10-20MB RAM usage)
- **Non-blocking updates** with 1-second refresh rate
- **Adaptive terminal sizing** for different screen sizes

### Data Collection
- **CPU**: `psutil.cpu_percent()` and `sensors` command
- **GPU**: `nvidia-smi` and `nvidia-settings` integration
- **Memory**: `psutil.virtual_memory()` and `psutil.swap_memory()`
- **Disk**: `psutil.disk_usage()` with intelligent filtering
- **Temperature**: Hardware sensor integration with history tracking

## 📝 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Support for AMD GPUs
- Additional sensor types
- Network monitoring features
- Export/logging capabilities
- Configuration file support

---
