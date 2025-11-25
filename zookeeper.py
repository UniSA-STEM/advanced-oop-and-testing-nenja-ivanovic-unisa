"""
File: zookeeper.py
Description: Contains the concrete Zookeeper class which is a subclass of the Staff class that is responsible for
feeding, cleaning and providing water to animals, and cleaning enclosures.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import time, datetime  # automatically handles formatting issues with dates and times.

import pandas as pd

from action import Action
from animal import Animal
from requires_cleaning import RequiresCleaning
from schedule import Schedule
from staff import Staff


class Zookeeper(Staff):
    def __str__(self) -> str:
        """Return the Zookeeper's key attributes as a formatted string."""
        return "\n<ZOOKEEPER> " + super().__str__()

    def generate_schedule(self) -> Schedule:
        """Return the full daily schedule of responsibilities of the Zookeeper"""
        # schedule is recreated from scratch every time it is required to ensure all changes are incorporated.
        schedule = Schedule(f"{self.name}_{self.id} Daily Task")

        schedule.data = pd.concat([schedule.data, self.special_tasks.data])  # add all special (non-routine) tasks first

        for enclosure in self.enclosure_assignments:
            schedule.new({"Time": time(7),  # clean all the assigned enclosures at 7am each morning
                          "SubjectID": self.id,
                          "SubjectName": self.name,
                          "ObjectID": enclosure.id,
                          "ObjectName": enclosure.name,
                          "Action": Action.CLEAN,
                          "Details": f"standard"})

            for animal in enclosure.inhabitants:
                animal_diet = animal.diet  # feed every animal in the enclosure
                for entry in animal_diet.data.itertuples():  # add each entry in the animal's diet as a separate task
                    schedule.new({"Time": entry.Time,  # get what time to feed from the animal's diet
                                  "SubjectID": self.id,
                                  "SubjectName": self.name,
                                  "ObjectID": animal.id,
                                  "ObjectName": animal.name,
                                  "Action": Action.FEED,
                                  "Details": entry.Details}  # get what food to feed from the animal's diet
                                 )
        return schedule

    def feed(self, animal: Animal, food: str, quantity: str, at_datetime: datetime = datetime.now()):
        """
        Log that the Zookeeper fed an animal.
        :param at_datetime: The date and time the feeding occurred (default is when method is called).
        :param animal: The animal being fed.
        :param food: Name of the food given.
        :param quantity: Quantity of the food given.
        :return: None
        """
        try:
            if not isinstance(animal, Animal):
                raise TypeError("Zookeepers can only feed Animal objects.")

            self.log.new({"DateTime": at_datetime,
                          "SubjectID": self.id,
                          "SubjectName": self.name,
                          "ObjectID": animal.id,
                          "ObjectName": animal.name,
                          "Action": Action.FEED,
                          "Details": f"{quantity} {food}"})

            # record that the object ate in its own logs:
            animal.eat(food, quantity, at_datetime)


        except TypeError as e:
            print(f"[ERROR] {e} No change made.\n")

    def clean(self, object_cleaned: RequiresCleaning, at_datetime: datetime = datetime.now(),
              details: str = "standard"):
        """
        Log that the Zookeeper cleaned an object which requires cleaning.
        :param at_datetime: The date and time the cleaning occurred (default is when method is called).
        :param object_cleaned: The object being cleaned (of type RequiresCleaning).
        :param details: The details of the cleaning (default is "standard")
        :return: None
        """
        try:
            if not isinstance(object_cleaned, RequiresCleaning):
                raise TypeError("Zookeepers can only clean instances of the RequiresCleaning class.")

            self.log.new({"DateTime": at_datetime,
                          "SubjectID": self.id,
                          "SubjectName": self.name,
                          "ObjectID": object_cleaned.get_id(),
                          "ObjectName": object_cleaned.get_name(),
                          "Action": Action.CLEAN,
                          "Details": f"{details}"})

            # record that the object was cleaned in its own logs:
            object_cleaned.receive_cleaning(self.id, self.name, at_datetime, 1)
        except TypeError as e:
            print(f"[ERROR] {e} No change made.\n")
