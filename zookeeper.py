"""
File: zookeeper.py
Description: Contains the concrete Zookeeper class which is a subclass of the Staff class that is responsible for
feeding, cleaning and providing water to animals, and cleaning enclosures.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import time  # automatically handles formatting issues with dates and times.

import pandas as pd

from action import Action
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
