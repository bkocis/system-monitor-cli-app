# 🖥️ System Monitor CLI Dashboard

A beautiful, real-time system monitoring dashboard for the terminal that provides comprehensive insights into your system's performance with live temperature graphs, resource usage, and hardware information.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## ✨ Features

### 🌡️ **Temperature Monitoring & History**
- **Real-time temperature tracking** for CPU and GPU
- **Visual temperature graphs** with configurable history points
- **Color-coded alerts** (green/yellow/red based on configurable thresholds)
- **Historical trends** showing temperature patterns over time

### 💻 **System Resource Monitoring**
- **CPU usage** with percentage and core count
- **Memory usage** with detailed used/total breakdown
- **Real-time updates** with configurable refresh rate
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

### ⚙️ **Configuration System**
- **JSON-based configuration** with user-friendly defaults
- **Customizable refresh rates** and temperature thresholds
- **Configurable display options** and color schemes
- **Per-user configuration** stored in `~/.config/system-monitor/`

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

### Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install lm-sensors nvidia-utils-* python3.12 python3.12-venv

# Initialize sensors (run once)
sudo sensors-detect --auto
```

## 🚀 Installation & Quick Start

### Option 1: Install as Python Package (Recommended)
```bash
# Clone the repository
git clone https://github.com/bkocis/system-monitor-cli-app.git
cd system-monitor-cli-app

# Install the package
pip install -e .

# Run the dashboard
system-monitor
```

### Option 2: Development Installation
```bash
# Clone the repository
git clone https://github.com/bkocis/system-monitor-cli-app.git
cd system-monitor-cli-app

# Set up development environment
make dev-setup
source venv/bin/activate

# Run the dashboard
make run
```

### Option 3: Script-based Setup
```bash
# Clone the repository
git clone https://github.com/bkocis/system-monitor-cli-app.git
cd system-monitor-cli-app

# Run using the setup script
./scripts/run_dashboard.sh

# Or launch in dedicated terminal window
./scripts/monitoring_terms.sh
```

### Option 4: Manual Setup
```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
python -m src.system_monitor.main
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

## ⚙️ Configuration

### Configuration File
The dashboard uses a JSON configuration file located at `~/.config/system-monitor/config.json`. 

**Create custom configuration:**
```bash
# Copy default configuration
mkdir -p ~/.config/system-monitor
cp config/default.json ~/.config/system-monitor/config.json

# Edit configuration
nano ~/.config/system-monitor/config.json
```

### Configuration Options
```json
{
  "refresh_rate": 1.0,
  "max_history_points": 100,
  "temperature_thresholds": {
    "warning": 70,
    "critical": 80
  },
  "display": {
    "show_gpu": true,
    "show_network": false,
    "graph_height": 8,
    "graph_length": 100
  },
  "colors": {
    "normal": "green",
    "warning": "yellow", 
    "critical": "red"
  }
}
```

For detailed configuration options, see [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## 🔨 Development

### Development Setup
```bash
# Clone repository
git clone https://github.com/bkocis/system-monitor-cli-app.git
cd system-monitor-cli-app

# Set up development environment
make dev-setup
source venv/bin/activate

# Install development dependencies
make install-dev
```

### Available Make Commands
```bash
make help              # Show available commands
make install          # Install package in development mode
make install-dev      # Install with development dependencies
make test             # Run test suite
make test-coverage    # Run tests with coverage report
make lint             # Run linting tools (ruff)
make format           # Format code (ruff)
make clean            # Clean build artifacts
make run              # Run the dashboard
make build            # Build distribution packages
```

### Running Tests
```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test file
pytest tests/test_dashboard.py
```

### Code Quality
```bash
# Format code
make format

# Check code quality (linting and type checking)
make lint

# Check formatting without making changes
make format-check
```

## 📁 Project Structure

```
system-monitor-cli-app/
├── src/system_monitor/        # Main package
│   ├── __init__.py           # Package initialization
│   ├── main.py               # CLI entry point
│   ├── dashboard.py          # Core dashboard logic
│   └── config.py             # Configuration management
├── tests/                    # Test suite
│   ├── test_dashboard.py     # Dashboard tests
│   └── test_config.py        # Configuration tests
├── scripts/                  # Shell scripts
│   ├── run_dashboard.sh      # Main launcher
│   └── monitoring_terms.sh   # Terminal launcher
├── config/                   # Configuration files
│   └── default.json          # Default configuration
├── docs/                     # Documentation
│   ├── CONFIGURATION.md      # Configuration guide
│   └── DEVELOPMENT.md        # Development guide
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── pyproject.toml           # Modern packaging config
├── setup.py                 # Package setup
├── Makefile                 # Development automation
└── CHANGELOG.md             # Version history
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
- **Green**: Normal operation (< 50% usage, configurable temperature)
- **Yellow**: Moderate load (50-75% usage, warning temperature)  
- **Red**: High load/temperature (> 75% usage, critical temperature)

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

### Configuration Issues
```bash
# Reset to default configuration
rm ~/.config/system-monitor/config.json
# Will recreate on next run

# Validate JSON configuration
python -c "import json; json.load(open('~/.config/system-monitor/config.json'))"
```

### Installation Issues
```bash
# Clean installation
make clean
pip uninstall system-monitor-cli
pip install -e .

# Development environment reset
rm -rf venv
make dev-setup
```

### Permission Issues
```bash
# Make scripts executable
chmod +x scripts/run_dashboard.sh scripts/monitoring_terms.sh
```

## 🔍 Technical Details

### Architecture
- **Python 3.12** with modern packaging standards
- **Rich library** for terminal UI rendering
- **psutil** for cross-platform system metrics
- **JSON configuration** with user-friendly defaults
- **Modular design** with separate concerns

### Performance
- **Minimal CPU overhead** (~1-2% CPU usage)
- **Memory efficient** (~10-20MB RAM usage)
- **Configurable refresh rate** (default: 1 second)
- **Adaptive terminal sizing** for different screen sizes

### Data Collection
- **CPU**: `psutil.cpu_percent()` and `sensors` command
- **GPU**: `nvidia-smi` and `nvidia-settings` integration
- **Memory**: `psutil.virtual_memory()` and `psutil.swap_memory()`
- **Disk**: `psutil.disk_usage()` with intelligent filtering
- **Temperature**: Hardware sensor integration with configurable history

### Testing
- **Comprehensive test suite** with >90% coverage
- **Unit tests** for all major components
- **Mocked external dependencies** for reliable testing
- **Continuous integration ready**

## 📦 Distribution

### Building Packages
```bash
# Build wheel and source distribution
make build

# Files created in dist/
ls dist/
# system_monitor_cli-1.0.0-py3-none-any.whl
# system_monitor_cli-1.0.0.tar.gz
```

### Installing from Source
```bash
# Install from local directory
pip install .

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## 📝 License

This project is open source under the MIT License. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Please see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed development guidelines.

### Areas for Improvement
- Support for AMD GPUs
- Additional sensor types
- Network monitoring features
- Export/logging capabilities
- Windows/macOS support

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure code quality (`make lint`)
5. Submit a pull request

### Reporting Issues
Please report bugs and feature requests on [GitHub Issues](https://github.com/bkocis/system-monitor-cli-app/issues).

## 🔗 Links

- **Repository**: https://github.com/bkocis/system-monitor-cli-app
- **Issues**: https://github.com/bkocis/system-monitor-cli-app/issues
- **Documentation**: [docs/](docs/)

---

**Created by Balaz Kocis** | **Professional System Monitoring for the Terminal**