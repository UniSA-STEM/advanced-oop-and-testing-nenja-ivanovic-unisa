"""
File: bird.py
Description: Contains the concrete Bird class which is a subclass of the Animal class that has a wingspan and may or
may not be able to fly.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

from action import Action
from animal import Animal
from environmental_type import EnvironmentalType


class Bird(Animal):
    def __init__(self, name: str, species: str, wingspan: float, can_fly: bool = True, age: int = 0,
                 habitat: EnvironmentalType = EnvironmentalType.RAINFOREST):
        """
        Initialise new Bird instances.
        :param name: The name of the bird.
        :param species: The specific species of bird that the instance is.
        :param age:  The age of the bird in years (default is 0).
        :param habitat: The environmental type the bird lives in (default is RAINFOREST).
        :param can_fly: Whether the bird can fly (True by default).
        :param wingspan: The wingspan of the bird in cm.
        """
        super().__init__(name, species, "Squawk", habitat, age, )  # all birds say squawk

        try:
            if not isinstance(can_fly, bool):
                raise TypeError
        except TypeError:
            if can_fly == "True":
                can_fly = True
            elif can_fly == "False":
                can_fly = False
            else:
                can_fly = True  # revert to default
                print(f"[WARNING] Provided can_fly value for Bird is not boolean, so default value of "
                      f"True has been assumed.\n")

        try:
            assert wingspan >= 0
        except AssertionError:
            wingspan = abs(wingspan)  # assume wingspan provided was meant to be positive
            print(
                f"[WARNING] Provided Bird wingspan is negative, so absolute value has been assumed ({wingspan} cm).\n")
        except TypeError:
            wingspan = None  # set to None
            print(f"[ERROR] Provided Bird's wingspan in cm number is not numeric, so 0 has been assigned.\n")

        self.__can_fly = can_fly
        self.__wingspan = wingspan

    def __str__(self) -> str:
        """Return the Bird's key attributes as a formatted string."""
        return super().__str__() + (f" > Wingspan: {self.__wingspan}cm"
                                    f"\n > Can fly: {self.__can_fly}"
                                    f"\n")

    def fly(self, at_datetime: datetime = datetime.now()):
        """Log that the Bird flies, or tries and fails to fly depending on the Bird's can_fly attribute.
        :param at_datetime: The date and time at which the bird attempted to fly (default is when the method is called).
        :return: None
        """
        details = "succeeds" if self.__can_fly else "fails"
        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.id,
                      "SubjectName": self.name,
                      "ObjectID": self.id,
                      "ObjectName": self.name,
                      "Action": Action.FLY,
                      "Details": f"{details}"})
