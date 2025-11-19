"""
File: reptile.py
Description: Contains the concrete Reptile class which is a subclass of the Animal class that has scales and may or
may not be venomous.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""

from action import Action
from animal import Animal


class Reptile(Animal):
    def __init__(self, name: str, species: str, sound: str, scale_type: str,
                 is_venomous: bool = False, age: int = 0):
        """
        Initialise new Reptile instances.
        :param name: The name of the reptile.
        :param species: The specific species of reptile that the instance is.
        :param sound: The sound that the animal makes (if any; default is None).
        :param scale_type: The primary type/description of the reptile's scales (e.g. 'smooth', 'keeled').
        :param is_venomous: Whether the reptile is venomous (False by default).
        :param age: The age of the reptile in years (default is 0).
        """
        super().__init__(name, species, age, sound)

        if not isinstance(is_venomous, bool):
            raise TypeError("A reptile's 'is_venomous' attribute must be boolean.")

        self.__scale_type = scale_type
        self.__is_venomous = is_venomous

    def __str__(self) -> str:
        """Return the Reptile's key attributes as a formatted string."""
        return super().__str__() + (
            f" > Scale type: {self.__scale_type}\n"
            f" > Venomous: {self.__is_venomous}\n"
        )

    def bask(self, at_datetime):
        """
        Log that the Reptile basks to regulate its body temperature.
        :param at_datetime: The date and time at which the reptile basked.
        :return: None
        """
        self.log.new({
            "DateTime": at_datetime,
            "SubjectID": self.id,
            "SubjectName": self.name,
            "ObjectID": self.id,
            "ObjectName": self.name,
            "Action": Action.BASK,
            "Details": "to regulate body temperature"
        })
