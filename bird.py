"""
File: bird.py
Description: Contains the concrete Bird class which is a subclass of the Animal class that has a wingspan and may or
may not be able to fly.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime, time

from action import Action
from animal import Animal
from severity import Severity


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

        if not isinstance(wingspan, (float, int)):
            raise TypeError("A bird's 'wingspan' attribute must be provided as a numeric value.")

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
                      "SubjectID": self.id,
                      "SubjectName": self.name,
                      "ObjectID": self.id,
                      "ObjectName": self.name,
                      "Action": Action.FLY,
                      "Details": f"{details}"})


bird1 = Bird("Pinky", "Emperor Penguin", 76, False, 2)
print(bird1)
bird1.fly(datetime(2004, 11, 12, 6))
bird1.fly(datetime(2004, 11, 12, 6, 20))
bird1.fly(datetime(2004, 11, 12, 6, 45))
bird1.eat("fish", "3x whole", datetime(2004, 11, 12, 9))
bird1.receive_health_check("S34", "Dr.John", "Behavioral assessment", Severity.LOW,
                           datetime(2004, 11, 12, 10, 20))
bird1.receive_diagnosis("S34", "Dr.John", "Psychological illness - anxiety", Severity.LOW,
                        "Get 5 min of cuddles every 12 hours.",
                        [[time(7), "5 min cuddles"], [time(19), "5 min cuddles"]],
                        datetime(2004, 11, 12, 10, 30)
                        )
print(bird1)
print(bird1.medical_log)
print(bird1.treatments)
bird1.receive_treatment("S34", "Dr.John", "5 min cuddles", Severity.LOW,
                        datetime(2004, 11, 12, 10, 35))
bird1.drink("water", "500mL", datetime(2004, 11, 12, 12, 10))
bird1.sleep(datetime(2004, 11, 12, 12, 40))
bird1.eat("squid", "200g", datetime(2004, 11, 12, 18, 50))
bird1.receive_treatment("S2", "Chloe", "5 min cuddles", Severity.LOW,
                        datetime(2004, 11, 12, 19, 00))
bird1.receive_health_check("S34", "Dr.John", "Behavioral review.", Severity.LOW,
                           datetime(2004, 11, 13, 10, 20))
bird1.recover("S34", "Dr.John", "Anxiety cured.",
              datetime(2004, 11, 13, 10, 35))

print(bird1.medical_log)
print(bird1)
print(bird1.log)

bird1.become_older(datetime(2004, 11, 13, 10, 35))
bird1.become_dirtier(datetime(2004, 11, 13, 11), 7)
print(bird1)
bird1.receive_cleaning("S2", "Chloe", datetime(2004, 11, 13, 12), 2)
print(bird1)
print(bird1.log)

bird1.add_to_diet("fish", "3x whole", time(9))
bird1.add_to_diet("squid", "200g", time(19))
print(bird1.diet)
bird1.remove_food_from_diet(time(17))
print(bird1.diet)
