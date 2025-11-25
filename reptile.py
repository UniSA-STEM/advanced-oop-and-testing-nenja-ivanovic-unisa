"""
File: reptile.py
Description: Contains the concrete Reptile class which is a subclass of the Animal class that has scales and may or
may not be venomous.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

from action import Action
from animal import Animal
from environmental_type import EnvironmentalType


class Reptile(Animal):
    def __init__(self, name: str, species: str, sound: str, scale_type: str,
                 is_venomous: bool = False, age: int = 0, habitat: EnvironmentalType = EnvironmentalType.RAINFOREST):
        """
        Initialise new Reptile instances.
        :param name: The name of the reptile.
        :param species: The specific species of reptile that the instance is.
        :param sound: The sound that the animal makes.
        :param scale_type: The primary type/description of the reptile's scales (e.g. 'smooth', 'keeled').
        :param is_venomous: Whether the reptile is venomous (False by default).
        :param age: The age of the reptile in years (default is 0).
        :param habitat: The environmental type the animal lives in (default is DESERT).
        """
        super().__init__(name, species, sound, habitat, age)

        try:
            if not isinstance(is_venomous, bool):
                raise TypeError
        except TypeError:
            if is_venomous == "True":
                is_venomous = True
            elif is_venomous == "False":
                is_venomous = False
            else:
                is_venomous = False  # revert to default
                print(f"[WARNING] Provided is_venomous value for Reptile is not boolean, so default value of "
                      f"False has been assumed.\n")

        self.__scale_type = scale_type
        self.__is_venomous = is_venomous

    def __str__(self) -> str:
        """Return the Reptile's key attributes as a formatted string."""
        return super().__str__() + (
            f" > Scale type: {self.__scale_type}\n"
            f" > Venomous: {self.__is_venomous}\n"
        )

    def bask(self, at_datetime: datetime = datetime.now()):
        """
        Log that the Reptile basks to regulate its body temperature.
        :param at_datetime: The date and time at which the reptile basked (default is when the method was called).
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
