"""
File: bird.py
Description: Contains the concrete Bird class which is a subclass of the Animal class that has a wingspan and may or
may not be able to fly.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from action import Action
from animal import Animal


class Bird(Animal):
    def __init__(self, name: str, species: str, wingspan: float, can_fly: bool = True, age: int = 0):
        """
        Initialise new Bird instances.
        :param name: The name of the bird.
        :param species: The specific species of bird that the instance is.
        :param age:  The age of the bird in years (default is 0).
        :param can_fly: Whether the bird can fly (True by default).
        :param wingspan: The wingspan of the bird in cm.
        """
        super().__init__(name, species, age, "Squawk")  # all birds say squawk

        if not isinstance(can_fly, bool):
            raise TypeError("A bird's 'can_fly' attribute must be boolean.")

        if not isinstance(wingspan, float):
            raise TypeError("A bird's 'wingspan' attribute must be provided as a float.")

        if wingspan <= 0:
            raise ValueError("Bird wingspan must be greater than zero.")

        self.__can_fly = can_fly
        self.__wingspan = wingspan

    def __str__(self) -> str:
        """Return the Bird's key attributes as a formatted string."""
        return super().__str__() + (f" > Wingspan: {self.__wingspan}cm"
                                    f"\n > Can fly: {self.__can_fly}"
                                    f"\n")

    def fly(self, at_datetime):
        """Log that the Bird flies, or tries and fails to fly depending on the Bird's can_fly attribute.
        :param at_datetime: The date and time at which the bird attempted to fly (default is when the method is called).
        :return: None
        """
        details = "succeeds" if self.__can_fly else "fails"
        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.__id,
                      "SubjectName": self.__name,
                      "ObjectID": self.__id,
                      "ObjectName": self.__name,
                      "Action": Action.FLY,
                      "Details": f"{details}"})
