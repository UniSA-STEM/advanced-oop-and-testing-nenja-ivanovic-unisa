"""
File: requires_cleaning.py
Description: Contains the abstract RequiresCleaning class which is inherited by zoo objects that have a cleanliness
status and require cleaning (primarily Animals and Enclosures).
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from abc import ABC

from severity import Severity


class RequiresCleaning(ABC):
    # create a new RequiresCleaning instance
    def __init__(self):
        self.__cleanliness = Severity.VERY_HIGH

    def get_cleanliness(self) -> Severity:
        """Get how clean the object is represented as an enumeration (Severity)."""
        return self.__cleanliness

    cleanliness = property(get_cleanliness)

    def become_dirtier(self, num_levels: int = 1):
        """
        Reduce cleanliness by a number of severity levels if possible.
        :param num_levels: The number of levels cleanliness is decreasing (default = 1).
        :return: None
        """
        if num_levels <= 0:
            raise ValueError("Cleanliness can only decrease by")
        current_cleanliness = self.cleanliness.level
        new_cleanliness = current_cleanliness
