#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="system-monitor-cli",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A beautiful, real-time system monitoring dashboard for the terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/system-monitor-cli-app",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "system-monitor=src.system_monitor.main:main",
        ],
    },
    scripts=[
        "scripts/run_dashboard.sh",
        "scripts/monitoring_terms.sh",
    ],
    keywords="system monitoring, CLI, dashboard, temperature, GPU, CPU, memory, disk",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/system-monitor-cli-app/issues",
        "Source": "https://github.com/yourusername/system-monitor-cli-app",
        "Documentation": "https://github.com/yourusername/system-monitor-cli-app#readme",
    },
)
