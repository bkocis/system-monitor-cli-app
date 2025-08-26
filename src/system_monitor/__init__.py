"""
System Monitor CLI Dashboard

A beautiful, real-time system monitoring dashboard for the terminal that provides 
comprehensive insights into your system's performance with live temperature graphs, 
resource usage, and hardware information.
"""

__version__ = "1.0.0"


from .dashboard import SystemDashboard

__all__ = ["SystemDashboard"]
