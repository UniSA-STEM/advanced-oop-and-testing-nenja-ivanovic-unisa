"""
File: mammal.py
Description: Contains the concrete Mammal class which is a subclass of the Animal class that has fur and may or
may not be nocturnal.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""

from action import Action
from animal import Animal


class Mammal(Animal):
    def __init__(self, name: str, species: str, sound: str, fur_colour: str,
                 is_nocturnal: bool = False, age: int = 0):
        """
        Initialise new Mammal instances.
        :param name: The name of the mammal.
        :param species: The specific species of mammal that the instance is.
        :param sound: The sound that the animal makes (if any; default is None).
        :param fur_colour: The primary colour of the mammal's fur.
        :param is_nocturnal: Whether the mammal is primarily active at night (False by default).
        :param age: The age of the mammal in years (default is 0).
        """
        super().__init__(name, species, age, sound)

        if not isinstance(fur_colour, str):
            raise TypeError("A mammal's 'fur_colour' attribute must be provided as a string.")

        if not isinstance(is_nocturnal, bool):
            raise TypeError("A mammal's 'is_nocturnal' attribute must be boolean.")

        self.__fur_colour = fur_colour
        self.__is_nocturnal = is_nocturnal

    def __str__(self) -> str:
        """Return the Mammal's key attributes as a formatted string."""
        return super().__str__() + (
            f" > Fur colour: {self.__fur_colour}\n"
            f" > Nocturnal: {self.__is_nocturnal}\n"
        )

    def groom(self, at_datetime):
        """
        Log that the Mammal grooms its fur.
        :param at_datetime: The date and time at which the mammal groomed itself.
        :return: None
        """
        self.log.new({
            "DateTime": at_datetime,
            "SubjectID": self.id,
            "SubjectName": self.name,
            "ObjectID": self.id,
            "ObjectName": self.name,
            "Action": Action.GROOM,
            "Details": f"picks at its {self.__fur_colour.lower()} fur"
        })
