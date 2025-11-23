"""
File: animal.py
Description: Contains the abstract Animal class which is the root class of all animal objects that live in the zoo.
have a name and age.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime  # automatically handles formatting issues with dates and times.
from datetime import time

from action import Action
from environmental_type import EnvironmentalType
from has_health import HasHealth
from log import Log
from requires_cleaning import RequiresCleaning
from schedule import Schedule


class Animal(RequiresCleaning, HasHealth):
    _next_id = 1  # unique identifier of the animal which is incremented by one each time an animal is created.

    def __init__(self, name: str, species: str, habitat: EnvironmentalType = EnvironmentalType.GRASS, age: int = 0,
                 sound: str = None):
        """
        Initialise new Animal instances.
        :param name: The name of the animal.
        :param species: The specific species name of the Animal.
        :param habitat: The environmental type the animal lives in (default is GRASS).
        :param age:  The age of the animal in years (default is 0).
        :param sound: The sound that the animal makes (if any; default is None).
        """
        self.__name = name
        self.__species = species
        self.__sound = sound

        if age < 0:
            raise ValueError("Animal age must be positive.")
        self.__age = age

        if not isinstance(habitat, EnvironmentalType):
            raise TypeError("Animal habitat must be an EnvironmentalType enumeration.")
        self.__habitat = habitat

        self.__id = "A" + str(Animal._next_id)  # A to represent 'Animal'
        Animal._next_id += 1

        self.__log = Log(f"{self.__name}_{self.id} General Activity")  # new Log to store records of general activities.
        self.__diet = Schedule(f"{self.__name}_{self.id} Dietary")  # create a new schedule to store daily feeding plan.

        RequiresCleaning.__init__(self)
        HasHealth.__init__(self)

    def __str__(self) -> str:
        """Return the Animal's key attributes as a formatted string."""
        health_status = "UNDER TREATMENT" if self.under_treatment else "HEALTHY"
        return (f"ID: {self.id} | NAME: {self.__name} | SPECIES: {self.species}"
                f"\n > Age: {self.age} year(s) old."
                f"\n > Health Status: [{health_status}]"
                f"\n > Cleanliness: {self.cleanliness.description}"
                f"\n")

    def __eq__(self, other) -> bool:
        """Determine whether one Animal is equal to another."""
        if isinstance(other, Animal) & (other.id == self.__id):
            return True
        else:
            return False

    def get_name(self) -> str:
        """Return a string representing the animal's name."""
        return self.__name

    def get_age(self) -> int:
        """Return an integer representing the animal's age in years."""
        return self.__age

    def get_id(self) -> str:
        """Return a string representing the animal's unique identifier."""
        return self.__id

    def get_species(self) -> str:
        """Return a string representing the animal's species."""
        return self.__species

    def get_habitat(self) -> EnvironmentalType:
        """Return an enumeration representing the habitat the animal lives in."""
        return self.__habitat

    def get_log(self) -> Log:
        """ Returns the log of the animal's activities."""
        return self.__log

    def get_diet(self) -> Schedule:
        """ Returns the animal's daily feeding schedule."""
        return self.__diet

    name = property(get_name)
    age = property(get_age)
    id = property(get_id)
    species = property(get_species)
    log = property(get_log)
    diet = property(get_diet)
    habitat = property(get_habitat)

    def become_older(self, at_datetime: datetime = datetime.now(), years: float = 1):
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

        self.__age += years
        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.__id,
                      "SubjectName": self.__name,
                      "ObjectID": self.__id,
                      "ObjectName": self.__name,
                      "Action": Action.AGE,
                      "Details": f"by {years} year(s) to become {self.__age} year(s) old"})

    def sleep(self, at_datetime: datetime = datetime.now()):
        """
        Log that the animal is sleeping.
        :param at_datetime: The date and time at which the animal slept (default is when the method is called).
        :return: None
        """
        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.__id,
                      "SubjectName": self.__name,
                      "ObjectID": self.__id,
                      "ObjectName": self.__name,
                      "Action": Action.SLEEP,
                      "Details": f"Zzz..."})

    def make_sound(self, at_datetime: datetime = datetime.now()):
        """
        Log that the animal made a sound.
        :param at_datetime: The date and time at which the animal made a sound (default is when the method is called).
        :return: None
        """
        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.__id,
                      "SubjectName": self.__name,
                      "ObjectID": self.__id,
                      "ObjectName": self.__name,
                      "Action": Action.SPEAK,
                      "Details": f"'{self.__sound}'"})

    def eat(self, food: str, quantity: str, at_datetime=datetime.now()):
        """
        Log that the animal ate food.
        :param food: Name of the food eaten.
        :param quantity: Quantity of the food eaten.
        :param at_datetime: The date and time at which the animal ate food (default is when the method is called).
        :return: None
        """
        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.__id,
                      "SubjectName": self.__name,
                      "ObjectID": self.__id,
                      "ObjectName": self.__name,
                      "Action": Action.EAT,
                      "Details": f"{quantity} {food}"})

    def drink(self, liquid: str, quantity: str, at_datetime=datetime.now()):
        """
        Log that the animal drank a liquid.
        :param liquid: Name of the liquid drank.
        :param quantity: Quantity of the liquid drank.
        :param at_datetime: The date and time at which the animal drank (default is when the method is called).
        :return: None
        """
        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.__id,
                      "SubjectName": self.__name,
                      "ObjectID": self.__id,
                      "ObjectName": self.__name,
                      "Action": Action.DRINK,
                      "Details": f"{quantity} {liquid}"})

    def add_to_diet(self, food: str, quantity: str, at_time: time):
        """
        Add food to the animal's diet.
        :param food: Name of the food to be eaten.
        :param quantity: Quantity of the food to be eaten.
        :param at_time: The time at which the animal should eat the food.
        :return: None
        """
        self.diet.new({"Time": at_time,
                       "SubjectID": self.id,
                       "SubjectName": self.name,
                       "ObjectID": self.id,
                       "ObjectName": self.name,
                       "Action": Action.EAT,
                       "Details": f"{quantity} {food}"})

    def remove_food_from_diet(self, after_time: time = time(0, 0, 0),
                              before_time: time = time(23, 59, 59)):
        """
        Remove meal(s) from diet which occur in the provided time range.
        :param after_time: The start of the time range associated with the meal(s) to be removed.
        :param before_time: The end of the time range associated with the meal(s) to be removed.
        :return: None
        """
        self.diet.remove(after_time, before_time)
