"""
File: requires_cleaning.py
Description: Contains the abstract RequiresCleaning class which is inherited by zoo objects that have a cleanliness
status and require cleaning (primarily Animals and Enclosures).
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from abc import ABC, abstractmethod
from datetime import datetime

from action import Action
from log import Log
from severity import Severity


class RequiresCleaning(ABC):
    def __init__(self):
        """
        Create a new RequiresCleaning instance.
        """
        self.__cleanliness: Severity = Severity.VERY_HIGH

    def get_cleanliness(self) -> Severity:
        """Get how clean the object is represented as an enumeration (Severity)."""
        return self.__cleanliness

    cleanliness = property(get_cleanliness)

    @abstractmethod
    def get_name(self) -> str:
        """Return a string representing the object's name."""

    @abstractmethod
    def get_id(self) -> str:
        """Return a string representing the object's unique identifier."""

    @abstractmethod
    def get_log(self) -> Log:
        """ Returns the log of the object's activities."""

    def become_dirtier(self, num_levels: int = 1):
        """
        Reduce cleanliness by a number of severity levels if possible. Log Event
        :param num_levels: The number of levels cleanliness is decreasing (default = 1).
        :return: None
        """
        if num_levels <= 0:
            raise ValueError("Cleanliness can only decrease by a positive number of levels.")

        # num_levels needs to be made negative so that the increase_decrease() method knows a decrease is occurring:
        self.__cleanliness = self.__cleanliness.increase_decrease(num_levels * -1)

        # log event:
        self.get_log().new({"DateTime": datetime.now(),  # date is when method is called.
                            "SubjectID": self.get_id(),
                            "SubjectName": self.get_name(),
                            "ObjectID": self.get_id(),
                            "ObjectName": self.get_name(),
                            "Action": Action.BECOME_DIRTIER,
                            "Details": f"cleanliness is now {self.cleanliness.description}"})

    def receive_cleaning(self, object_id: str, object_name: str, num_levels: int = 1, ):
        """
        Increase cleanliness by a number of severity levels if possible. Log event.
        :param object_name: The name of the object that the RequiresCleaning object is being cleaned by.
        :param object_id: The id of the object that the RequiresCleaning object is being cleaned by.
        :param num_levels: The number of levels cleanliness is increasing (default = 1).
        :return: None
        """
        if num_levels <= 0:
            raise ValueError("Cleanliness can only increase by a positive number of levels.")

        self.__cleanliness = self.__cleanliness.increase_decrease(num_levels)

        # log event:
        self.get_log().new({"DateTime": datetime.now(),  # date is when method is called.
                            "SubjectID": self.get_id(),
                            "SubjectName": self.get_name(),
                            "ObjectID": object_id,
                            "ObjectName": object_name,
                            "Action": Action.RECEIVE_CLEANING,
                            "Details": f"cleanliness is now {self.cleanliness.description}"})
