"""
File: mammal.py
Description: Contains the concrete Mammal class which is a subclass of the Animal class that has fur and may or
may not be nocturnal.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

from action import Action
from animal import Animal
from environmental_type import EnvironmentalType


class Mammal(Animal):
    def __init__(self, name: str, species: str, sound: str, fur_colour: str,
                 is_nocturnal: bool = False, age: int = 0, habitat: EnvironmentalType = EnvironmentalType.GRASS):
        """
        Initialise new Mammal instances.
        :param name: The name of the mammal.
        :param species: The specific species of mammal that the instance is.
        :param sound: The sound that the animal makes.
        :param fur_colour: The primary colour of the mammal's fur.
        :param is_nocturnal: Whether the mammal is primarily active at night (False by default).
        :param age: The age of the mammal in years (default is 0).
        :param habitat: The environmental type the Mammal lives in (default is GRASS).
        """
        super().__init__(name, species, sound, habitat, age)

        try:
            if not isinstance(is_nocturnal, bool):
                raise TypeError
        except TypeError:
            if is_nocturnal == "True":
                is_nocturnal = True
            elif is_nocturnal == "False":
                is_nocturnal = False
            else:
                is_nocturnal = False  # revert to default
                print(f"[WARNING] Provided is_nocturnal value for Mammal is not boolean, so default value of "
                      f"False has been assumed.\n")

        self.__fur_colour = fur_colour
        self.__is_nocturnal = is_nocturnal

    def __str__(self) -> str:
        """Return the Mammal's key attributes as a formatted string."""
        return super().__str__() + (
            f" > Fur colour: {self.__fur_colour}\n"
            f" > Nocturnal: {self.__is_nocturnal}\n"
        )

    def groom(self, at_datetime: datetime = datetime.now()):
        """
        Log that the Mammal grooms its fur.
        :param at_datetime: The date and time at which the mammal groomed itself (default is when the method was called)
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
