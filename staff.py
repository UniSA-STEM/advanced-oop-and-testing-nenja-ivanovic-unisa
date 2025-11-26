"""
File: staff.py
Description: Contains the abstract Staff class which is the root class of all staff objects that work the zoo.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from abc import abstractmethod, ABC
from datetime import datetime  # automatically handles formatting issues with dates and times.

from action import Action
from animal import Animal
from enclosure import Enclosure
from log import Log
from schedule import Schedule


class Staff(ABC):
    _next_id = 1  # unique identifier of the staff which is incremented by one each time a staff object is created.

    def __init__(self, name: str):
        """
        Initialise new Staff instances.
        :param name: The name of the staff member.
        """
        self.__name = name

        self.__id = "S" + str(Staff._next_id)  # S to represent "Staff".
        Staff._next_id += 1

        self.__animal_assignments = []
        self.__enclosure_assignments = []
        self.__special_tasks = Schedule(f"{self.__name} Special Task")

        self.__log = Log(f"{self.__name}_{self.id} General Activity")  # new Log to store records of general activities.

    @abstractmethod
    def __str__(self) -> str:
        """Return the Staff's key attributes as a formatted string."""
        animals_string = f"\n > Assigned Animals: {len(self.animal_assignments)}"
        for animal in self.animal_assignments:
            animals_string += f"\n   > {animal.name}_{animal.id}"

        enclosures_string = f"\n > Assigned Enclosures: {len(self.enclosure_assignments)}"
        for enclosure in self.enclosure_assignments:
            enclosures_string += f"\n   > {enclosure.name}_{enclosure.id}"
        return f"ID: {self.id} | NAME: {self.__name}" + animals_string + enclosures_string + "\n"

    def __eq__(self, other) -> bool:
        """Determine whether one Staff is equal to another."""
        if isinstance(other, Staff) & (other.id == self.__id):
            return True
        else:
            return False

    def get_name(self) -> str:
        """Return a string representing the Staff's name."""
        return self.__name

    def get_id(self) -> str:
        """Return a string representing the staff's unique identifier."""
        return self.__id

    def get_log(self) -> Log:
        """ Returns the log of the Staff's activities."""
        return self.__log

    def get_animal_assignments(self) -> list[Animal]:
        """ Returns the Animals that the Staff member is responsible for."""
        return self.__animal_assignments

    def get_enclosure_assignments(self) -> list[Enclosure]:
        """ Returns the Enclosures that the Staff member is responsible for."""
        return self.__enclosure_assignments

    def get_special_tasks(self) -> Schedule:
        """ Returns the Schedule containing special (non-routine) tasks that the Staff member is
        responsible for doing."""
        return self.__special_tasks

    name = property(get_name)
    id = property(get_id)
    log = property(get_log)
    animal_assignments = property(get_animal_assignments)
    enclosure_assignments = property(get_enclosure_assignments)
    special_tasks = property(get_special_tasks)

    @abstractmethod
    def generate_schedule(self) -> Schedule:
        """Return the full daily schedule of responsibilities of the Staff member"""
        pass

    def assign(self, assignment: Animal | Enclosure, at_datetime: datetime = datetime.now()):
        """
        Assign a new object to the responsibilities of the staff member.
        :param at_datetime: the datetime at which the assignment was made (default is when method is called).
        :param assignment: The object requiring actions to assign to the Staff.
        :return: None
        """
        try:
            if isinstance(assignment, Animal):
                if assignment not in self.animal_assignments:  # duplicates not allowed
                    self.animal_assignments.append(assignment)
                else:
                    return None
            elif isinstance(assignment, Enclosure):
                if assignment not in self.enclosure_assignments:  # duplicates not allowed
                    self.enclosure_assignments.append(assignment)
                else:
                    return None
            else:
                raise TypeError(f"Staff members cannot be assigned to {assignment.__class__.__name__} objects.")

            self.log.new({"DateTime": at_datetime,
                          "SubjectID": self.__id,
                          "SubjectName": self.__name,
                          "ObjectID": assignment.id,
                          "ObjectName": assignment.name,
                          "Action": Action.ASSIGN,
                          "Details": f"{assignment.__class__.__name__}"})
        except TypeError as e:
            print(f"[ERROR] {e} No change made.\n")

    def unassign(self, assignment: Animal | Enclosure, at_datetime: datetime = datetime.now()):
        """
        Unassign an assigned object from the responsibilities of the staff member.
        :param assignment: The object requiring actions to unassign from the Staff member.
        :param at_datetime: the datetime at which the unassignment occurred (default is when method is called).
        :return: None
        """
        if assignment in self.animal_assignments:
            self.animal_assignments.remove(assignment)
        elif assignment in self.enclosure_assignments:
            self.enclosure_assignments.remove(assignment)
        else:
            return None  # skip adding a log entry if nothing was changed.

        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.__id,
                      "SubjectName": self.__name,
                      "ObjectID": assignment.id,
                      "ObjectName": assignment.name,
                      "Action": Action.UNASSIGN,
                      "Details": f"{assignment.__class__.__name__}"})

        return None
