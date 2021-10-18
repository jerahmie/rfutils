#!/bin/env python
"""Construct a dictionary of materials from a materials file.
"""

import os
import sys

import csv
import re

class MaterialsDB(object):
    """Construct a materials data base from materials.
    """
    def __init__(self):
        self._material_dict = []
        self._material_count = 0

    def add_material(self, material):
        """Add a material to the database.
        """
        