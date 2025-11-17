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
from datetime import datetime  # automatically handles formatting issues with dates and times.

import pandas as pd  # for easier storage and manipulation of data such as activity logs and dietary info.

from action import Action


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
        self.__sound = sound

        if age < 0:
            raise ValueError("Animal age must be positive.")
        self.__age = age

        self.__id = Animal._next_id
        Animal._next_id += 1

        # create a dataframe to store activities
        self.__log = pd.DataFrame({
            "Time": pd.Series(dtype="object"),  # datetime object
            "Id": pd.Series(dtype="int"),
            "Name": pd.Series(dtype="string"),
            "Action": pd.Series(dtype="object"),  # Action enumeration
            "Details": pd.Series(dtype="string")

        })

    def get_name(self) -> str:
        """Return a string representing the animal's name."""
        return self.__name

    def get_age(self) -> int:
        """Return an integer representing the animal's age in years."""
        return self.__age

    def get_id(self) -> int:
        """Return an integer representing the animal's unique identifier."""
        return self.__id

    def get_log(self):
        return self.__log

    name = property(get_name)
    age = property(get_age)
    id = property(get_id)
    log = property(get_log)

    def become_older(self, years: float = 1, at_datetime: datetime = datetime.now()):
        """
        Increase the animal's age by a certain number of years and log event.
        :param years: The number of years that the animal has gotten older (default 1 year).
        :param at_datetime: The date and time at which the animal got older (default is when the method is called).
        :return: None
        """
        if not isinstance(years, float | int):
            raise TypeError("Number of years must be a numeric value.")
        if years <= 0:
            raise ValueError("The number of years to age must be greater than zero.")
        if not isinstance(at_datetime, datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime object.")

        self.__age += years
        # add event to log:
        self.__log[len(self.__log)] = [at_datetime, self.id, self.name, Action.AGE,
                                       f"(by {years} years to become {self.__age} years old)"]

    def sleep(self, at_datetime: datetime = datetime.now()):
        """
        Log that the animal is sleeping.
        :param at_datetime: The date and time at which the animal slept (default is when the method is called).
        :return: None
        """
        if not isinstance(at_datetime, datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime object.")

        # add event to log:
        self.__log[len(self.__log)] = [at_datetime, self.id, self.name, Action.SLEEP,
                                       f"(Zzz...)"]

    def make_sound(self, at_datetime: datetime = datetime.now()):
        """
        Log that the animal made a sound.
        :param at_datetime: The date and time at which the animal made a sound (default is when the method is called).
        :return: None
        """
        if not isinstance(at_datetime, datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime object.")

        # add event to log:
        self.__log[len(self.__log)] = [at_datetime, self.id, self.name, Action.SPEAK,
                                       f"('{self.__sound}')"]

    def eat(self, food: str, quantity: int, at_datetime=datetime.now()):
        """

        :param food: Name of the food eaten.
        :param quantity: Quantity of the food eaten.
        :param at_datetime: The date and time at which the animal ate food (default is when the method is called).
        :return: None
        """
        if not isinstance(quantity, float | int):
            raise TypeError("Number of years must be a numeric value.")
        if quantity <= 0:
            raise ValueError("The quantity of food eaten must be greater than zero.")

        if not isinstance(at_datetime, datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime object.")

        # add event to log:
        self.__log[len(self.__log)] = [at_datetime, self.id, self.name, Action.AGE,
                                       f"({quantity}x {food})"]
