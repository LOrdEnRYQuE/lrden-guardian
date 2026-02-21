#!/usr/bin/env python3
"""
LRDEnE Guardian - Setup Script
=============================

Copyright (c) 2026 LRDEnE. All rights reserved.

Install the LRDEnE Guardian AI safety system for use in any project.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lrden-guardian",
    version="1.0.0",
    author="LRDEnE Technology Team",
    author_email="tech@lrden.com",
    description="LRDEnE Guardian - Advanced AI Safety & Hallucination Detection System",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/LRDEnE/lrden-guardian",
    project_urls={
        "Bug Tracker": "https://github.com/LRDEnE/lrden-guardian/issues",
        "Documentation": "https://github.com/LRDEnE/lrden-guardian/wiki",
        "Source Code": "https://github.com/LRDEnE/lrden-guardian",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lrden-guardian=lrden_guardian.cli:main",
            "lrden-init=lrden_guardian.init:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lrden_guardian": [
            "data/*.json",
            "templates/*.txt",
            "config/*.yaml",
        ],
    },
    keywords="AI safety hallucination detection content validation LRDEnE guardian",
    zip_safe=False,
)
