# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains all the information of a check
"""
from typing import Dict

from src.model.star import Star


class Check:
    """
    Model that contains all the information we need for a check
    """
    def __init__(self,
                 table_path: str,
                 directory_path: str,
                 base_file_name: str,
                 header: str,
                 footer: str,
                 stars: Dict[str, Star]) -> None:
        self.table_path: str = table_path
        self.directory_path: str = directory_path
        self.base_file_name: str = base_file_name
        self.header: str = header
        self.footer: str = footer
        self.stars: Dict[str, Star] = stars
