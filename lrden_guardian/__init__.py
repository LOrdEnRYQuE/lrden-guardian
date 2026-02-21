#!/usr/bin/env python3
"""
LRDEnE Guardian - Advanced AI Safety & Hallucination Detection System
======================================================================

Copyright (c) 2026 LRDEnE. All rights reserved.

This is the main package for LRDEnE Guardian, providing enterprise-grade
AI safety and hallucination detection capabilities.

Author: LRDEnE Technology Team
Version: 1.0.0
License: Proprietary - LRDEnE Internal Use
"""

__version__ = "1.0.0"
__author__ = "LRDEnE Technology Team"
__email__ = "tech@lrden.com"
__license__ = "Proprietary"
__copyright__ = "Copyright (c) 2026 LRDEnE. All rights reserved."

# Import core Guardian class
from .guardian import LRDEnEGuardian, create_lrden_guardian

# Export main components
__all__ = [
    "LRDEnEGuardian",
    "create_lrden_guardian",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__"
]

# Package metadata
PACKAGE_INFO = {
    "name": "lrden-guardian",
    "version": __version__,
    "description": "LRDEnE Guardian - Advanced AI Safety & Hallucination Detection System",
    "author": __author__,
    "email": __email__,
    "license": __license__,
    "copyright": __copyright__,
    "url": "https://github.com/LRDEnE/lrden-guardian",
    "documentation": "https://lrden-guardian.readthedocs.io/",
    "support": "tech@lrden.com"
}

def get_package_info():
    """Get LRDEnE Guardian package information"""
    return PACKAGE_INFO

def get_version():
    """Get LRDEnE Guardian version"""
    return __version__
