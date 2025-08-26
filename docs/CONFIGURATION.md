# Configuration Guide

The System Monitor CLI Dashboard can be customized through a configuration file. This guide explains all available configuration options.

## Configuration File Location

The configuration file is automatically created at:
- `~/.config/system-monitor/config.json` (Linux)

You can also specify a custom configuration file path when initializing the Config class.

## Configuration Options

### Basic Settings

```json
{
  "refresh_rate": 1.0,
  "max_history_points": 100
}
```

- **refresh_rate**: Update frequency in seconds (default: 1.0)
- **max_history_points**: Number of temperature history points to keep (default: 100)

### Temperature Thresholds

```json
{
  "temperature_thresholds": {
    "warning": 70,
    "critical": 80
  }
}
```

- **warning**: Temperature in Celsius for yellow alerts (default: 70)
- **critical**: Temperature in Celsius for red alerts (default: 80)

### Display Settings

```json
{
  "display": {
    "show_gpu": true,
    "show_network": false,
    "graph_height": 8,
    "graph_length": 100
  }
}
```

- **show_gpu**: Enable/disable GPU monitoring (default: true)
- **show_network**: Enable/disable network monitoring (default: false)
- **graph_height**: Height of temperature graphs in lines (default: 8)
- **graph_length**: Width of temperature graphs in characters (default: 100)

### Color Scheme

```json
{
  "colors": {
    "normal": "green",
    "warning": "yellow", 
    "critical": "red"
  }
}
```

- **normal**: Color for normal status (default: "green")
- **warning**: Color for warning status (default: "yellow")
- **critical**: Color for critical status (default: "red")

### Filesystem Filters

```json
{
  "filters": {
    "exclude_virtual_filesystems": true,
    "exclude_loop_devices": true,
    "exclude_snap_mounts": true
  }
}
```

- **exclude_virtual_filesystems**: Hide virtual/temporary filesystems (default: true)
- **exclude_loop_devices**: Hide loop devices (default: true)
- **exclude_snap_mounts**: Hide snap package mounts (default: true)

## Example Configuration

Here's a complete example configuration file:

```json
{
  "refresh_rate": 2.0,
  "max_history_points": 150,
  "temperature_thresholds": {
    "warning": 75,
    "critical": 85
  },
  "display": {
    "show_gpu": true,
    "show_network": true,
    "graph_height": 10,
    "graph_length": 120
  },
  "colors": {
    "normal": "bright_green",
    "warning": "bright_yellow", 
    "critical": "bright_red"
  },
  "filters": {
    "exclude_virtual_filesystems": true,
    "exclude_loop_devices": true,
    "exclude_snap_mounts": true
  }
}
```

## Creating a Custom Configuration

1. Copy the default configuration:
   ```bash
   mkdir -p ~/.config/system-monitor
   cp config/default.json ~/.config/system-monitor/config.json
   ```

2. Edit the configuration file:
   ```bash
   nano ~/.config/system-monitor/config.json
   ```

3. Restart the dashboard to apply changes

## Available Colors

The dashboard supports these Rich library colors:
- Basic: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- Bright: `bright_black`, `bright_red`, `bright_green`, etc.
- RGB: `rgb(255,0,0)` for custom colors
- Hex: `#ff0000` for custom colors

## Troubleshooting

### Configuration Not Loading
- Check that the JSON syntax is valid
- Ensure the file has proper permissions
- Check the terminal for warning messages

### Invalid Values
- The dashboard will fall back to defaults for invalid values
- Check the logs for configuration warnings
- Refer to this guide for valid value ranges

### Performance Issues
- Lower `refresh_rate` for faster updates (e.g., 0.5 for 2Hz)
- Reduce `max_history_points` to use less memory
- Disable `show_network` if not needed
