# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains all the information of a star
"""

class Star:
    """
    Contain all the information we need from a star to decide witch is the best
    """
    def __init__(self, name: str, neb_depth_vs_rms: float, line: str):
        self.name: str = name
        self.neb_depth_vs_rms: float = neb_depth_vs_rms
        self.line: str = line