"""
File: severity.py
Description: Contains the enumeration class for the spectrum of severity levels to be used as a descriptive qualifier.

Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from enum import Enum


class Severity(Enum):
    VERY_LOW = ("Very Low", 1)
    LOW = ("Low", 2)
    MODERATE = ("Moderate", 3)
    HIGH = ("High", 4)
    VERY_HIGH = ("Very High", 5)

    def __init__(self, description: str, level: int):
        self.__description = description
        self.__level = level

    def get_description(self) -> str:
        """Returns a string that represents the severity level verbally."""
        return self.__description

    def get_level(self) -> int:
        """Returns an integer that represents the severity level numerically (min=1, max=5).."""
        return self.__level

    description = property(get_description)
    level = property(get_level)
