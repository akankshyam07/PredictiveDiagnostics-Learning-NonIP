"""
Author: Akankshya Mohanty
Mentor & Reviewer: Rajani Vanarse
#*******************************************************************
#Copyright (C) 2023 Adino Labs
#*******************************************************************
"""
import enum


class Recommendation(enum.Enum):
    PROBABLE_DISEASE = 0
    TESTS = 1
    MEDICINES = 2