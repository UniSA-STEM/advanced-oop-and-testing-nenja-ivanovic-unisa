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
        """Returns an integer that represents the severity level numerically (min=1, max=5)."""
        return self.__level

    description = property(get_description)
    level = property(get_level)

    def increase_decrease(self, num_levels: int):
        """
        Return a Severity a certain number of levels above or below own level.
        :param num_levels: The number of levels to go up.
        :return: Severity
        """
        try:
            current_level = self.level
            lookup_level = current_level + int(num_levels)  # convert to int if float was provided.
            if num_levels < 0:  # level is decreasing
                min_possible_level = min([severity.level for severity in Severity])
                lookup_level = max(lookup_level, min_possible_level)  # ensure level to look up is not lower than min
            if num_levels < 0:  # level is decreasing
                max_possible_level = max([severity.level for severity in Severity])
                lookup_level = min(lookup_level, max_possible_level)  # ensure level to look up is not higher than max

            # get first result if multiple matches:
            new_severity = [severity for severity in Severity if severity.level == lookup_level][0]
            return new_severity

        except TypeError:
            print("[ERROR] Could not determine change in Severity as the number of levels to "
                  "change provided is not numeric.\n")
            return self
