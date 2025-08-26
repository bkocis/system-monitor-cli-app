#!/usr/bin/env python3
"""
Main entry point for the System Monitor CLI Dashboard.
"""

import sys

from .dashboard import SystemDashboard


def main():
    """Main entry point for the system monitor dashboard."""
    try:
        dashboard = SystemDashboard()
        dashboard.run()
    except KeyboardInterrupt:
        print("\n[bold red]Dashboard stopped.[/bold red]")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
