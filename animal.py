"""
File: animal.py
Description: Contains the abstract Animal class which is the root class of all animal objects that live in the zoo.
have a name and age.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from abc import ABC


class Animal(ABC):
    _next_id = 1  # unique identifier of the animal which is incremented by one each time a animal is created.

    def __init__(self, name: str, species: str, age: int = 0, sound: str = None):
        """
        Initialise new Animal instances.
        :param name: The name of the animal.
        :param species: The specific species name of the Animal.
        :param age:  The age of the animal in years (default is 0).
        :param sound: The sound that the animal makes (if any; default is None).
        """
        self.__name = name
        self.__species = species
        self.__age = age
        self.__sound = sound

        self.__id = Animal._next_id
        Animal._next_id += 1

    def get_name(self) -> str:
        """Return a string representing the animal's name."""
        return self.__name

    def get_age(self) -> int:
        """Return an integer representing the animal's age in years."""
        return self.__age

    name = property(get_name)
    age = property(get_age)

    def become_older(self, years: int = 1):
        pass

    def sleep(self):
        pass

    def make_sound(self):
        pass
