"""
File: zoo_system.py
Description: Contains the concrete ZooSystem class which holds all information about a zoo, including animals,
enclosures,and staff. The ZooSystem class is responsible for administrative report generation and handling major
interactions between the classes it holds.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

import pandas as pd

from animal import Animal
from enclosure import Enclosure
from log import Log
from schedule import Schedule
from staff import Staff


class ZooSystem:
    def __init__(self, zoo_name: str):
        """
        Create a new instance of a ZooSystem.
        :param zoo_name: The name of the Zoo administrated by the system.
        """
        self.__enclosures = []
        self.__animals = []
        self.__staff = []
        self.__name = zoo_name

    def __str__(self) -> str:
        """Return the Zoo's key attributes as a formatted string."""

        animals_string = f"\n\nANIMALS ({len(self.animals)}) -----------------------------------------\n"
        for animal in self.animals:
            animals_string += "\n" + str(animal)

        enclosures_string = f"\n\nENCLOSURES ({len(self.enclosures)}) -----------------------------------------\n"
        for enclosure in self.enclosures:
            enclosures_string += "\n" + str(enclosure)

        staff_string = f"\n\nSTAFF ({len(self.staff)}) -----------------------------------------\n"
        for staff in self.staff:
            staff_string += str(staff)

        return ("----------------------------------------------------------------------------------------------\n"
                f"~~~~~ {self.name.upper()} ~~~~~ "
                + animals_string + enclosures_string + staff_string +
                "\n----------------------------------------------------------------------------------------------\n")

    def get_name(self) -> str:
        """Return a string representing the Zoo's name."""
        return self.__name

    def get_animals(self) -> list[Animal]:
        """ Returns the Animals that live in the zoo."""
        return self.__animals

    def get_enclosures(self) -> list[Enclosure]:
        """ Returns the Enclosures that exist in the zoo."""
        return self.__enclosures

    def get_staff(self) -> list[Staff]:
        """ Returns the Staff members that work in the zoo."""
        return self.__staff

    def set_name(self, name: str) -> None:
        """Set the Zoo's name."""
        if not isinstance(name, str):
            raise TypeError("Zoo name must be a string.")
        self.__name = name

    def set_animals(self, animals: list[Animal]) -> None:
        """Set the Animals that live in the zoo."""
        if not all(isinstance(a, Animal) for a in animals):
            raise TypeError("animals must be a list of Animal objects.")
        self.__animals = animals

    def set_enclosures(self, enclosures: list[Enclosure]) -> None:
        """Set the Enclosures that exist in the zoo."""
        if not all(isinstance(e, Enclosure) for e in enclosures):
            raise TypeError("enclosures must be a list of Enclosure objects.")
        self.__enclosures = enclosures

    def set_staff(self, staff: list[Staff]) -> None:
        """Set the Staff members that work in the zoo."""
        if not all(isinstance(s, Staff) for s in staff):
            raise TypeError("staff must be a list of Staff objects.")
        self.__staff = staff

    name = property(get_name, set_name)
    animals = property(get_animals, set_animals)
    enclosures = property(get_enclosures, set_enclosures)
    staff = property(get_staff, set_staff)

    # adding, removing, moving and assignment ---------------------------------------------------------------

    def add_animal(self, animal: Animal) -> None:
        """
        Add an Animal to the zoo.
        :param animal: The Animal to add to the zoo.
        :return: None
        """
        if not isinstance(animal, Animal):
            raise TypeError("Only Animal instances can be added to the zoo.")
        if animal not in self.__animals:
            self.__animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        """
        Remove an Animal from the zoo that is not under treatment.
        :param animal: The Animal to remove from the zoo.
        :return: None
        """
        if animal in self.__animals:  # can only remove animals from the zoo that already live there.
            # Remove from any enclosures first
            for enclosure in self.__enclosures:
                if animal in enclosure.inhabitants:
                    enclosure.remove_animal(animal)  # internally checks that animal is not sick.

            self.__animals.remove(animal)

    def add_enclosure(self, enclosure: Enclosure) -> None:
        """
        Add an Enclosure from the zoo - enclosures must be empty before adding.
        :param enclosure: The enclosure to remove from the zoo (must be empty).
        :return: None
        """
        if not isinstance(enclosure, Enclosure):
            raise TypeError("Only Enclosure instances can be added to the zoo.")
        if len(enclosure.inhabitants) > 0:
            raise ValueError(f"{enclosure.name}_{enclosure.id} cannot be added as it is not empty.")
        if enclosure not in self.__enclosures:
            self.__enclosures.append(enclosure)

    def remove_enclosure(self, enclosure: Enclosure) -> None:
        """
        Remove an Enclosure from the zoo - enclosures must be empty before removal.
        :param enclosure: The enclosure to remove from the zoo (must be empty).
        :return: None
        """
        if not isinstance(enclosure, Enclosure):
            raise TypeError("Only Enclosure instances can be removed from the zoo.")
        if len(enclosure.inhabitants) > 0:
            raise ValueError(f"{enclosure.name}_{enclosure.id} cannot be removed as it is not empty.")
        if enclosure in self.__enclosures:
            self.__enclosures.remove(enclosure)

    def add_staff_member(self, staff_member: Staff) -> None:
        """Add a Staff member to the zoo.
        :param staff_member: The staff member to add to the zoo.
        """
        if not isinstance(staff_member, Staff):
            raise TypeError("Only Staff instances can be added to the zoo.")
        if staff_member not in self.__staff:
            self.__staff.append(staff_member)

    def remove_staff_member(self, staff_member: Staff) -> None:
        """
        Remove a Staff member from the zoo.
        :param staff_member: The staff member to remove from the zoo.
        """
        if not isinstance(staff_member, Staff):
            raise TypeError("Only Staff instances can be removed from the zoo.")

        if staff_member in self.__staff:
            self.__staff.remove(staff_member)

    def assign_staff_to_enclosure(self, staff_member: Staff, enclosure: Enclosure,
                                  at_datetime: datetime) -> None:
        """
        Assign a member of staff to an enclosure.
        :param staff_member: The staff member to assign to the enclosure.
        :param enclosure: The enclosure the staff member is being assigned to.
        :param at_datetime: The date and time at which the assignment was made (default is when method is called).
        :return: None
        """
        if staff_member not in self.__staff:
            raise ValueError("Staff member must belong to this zoo before assignment.")
        if enclosure not in self.__enclosures:
            raise ValueError("Enclosure must belong to this zoo before assignment.")

        staff_member.assign(enclosure, at_datetime)

    def assign_animal_to_enclosure(self, animal: Animal, enclosure: Enclosure) -> None:
        """
        Assign a member of staff to an enclosure.
        :param animal: The animal to assign to the enclosure.
        :param enclosure: The enclosure the animal is being assigned to.
        :return: None
        """
        if animal not in self.__animals:
            raise ValueError(f"Animal must belong to {self.name} before it can be assigned to an enclosure.")
        if enclosure not in self.__enclosures:
            raise ValueError(f"Enclosure must belong to {self.name} before it can receive animals.")

        enclosure.add_animal(animal)  # checks that animal is not under treatment internally

    def move_animal(self, animal: Animal, from_enclosure: Enclosure, to_enclosure: Enclosure) -> None:
        """
        Move an animal from one enclosure to another. This will respect all existing rules in
        Enclosure (habitat, species, treatment status).
        :param animal: The animal being relocated.
        :param from_enclosure: Where the animal is currently located.
        :param to_enclosure: Where the animal is to be relocated.
        :return: None
        """
        if from_enclosure not in self.__enclosures or to_enclosure not in self.__enclosures:
            raise ValueError("Both enclosures must belong to this zoo.")

        if animal not in from_enclosure.inhabitants:
            raise ValueError(f"{animal.name}_{animal.id} does not live in {from_enclosure.name}_{from_enclosure.id}.")

        from_enclosure.remove_animal(animal)
        to_enclosure.add_animal(animal)

    # reporting  ------------------------------------------------------------------------------------------------

    def report_species(self) -> str:
        """
        Generate a text report listing animals grouped by species.
        :return: Report of animals grouped by species as a string.
        """
        species = [animal.species for animal in self.animals]
        species = list(set(species))  # remove duplicates
        output = f"\nANIMALS BY SPECIES ({len(self.__animals)} total):"

        for name in species:
            animals = [animal for animal in self.animals if animal.species == name]
            output += f"\n\n{species} ({len(animals)}):"
            for animal in animals:
                output += f"\n - {animal.name}_{animal.id}"
            output += "\n"

        return output

    def report_enclosure_status(self) -> str:
        """
        Generate a text report describing the status of each enclosure: environment, cleanliness, and occupancy.
        :return: Report of enclosure information as a string.
        """
        output = "\nENCLOSURE STATUS REPORT:"
        for enclosure in self.__enclosures:
            output += (str(enclosure) + "\n")

        return output

    def report_animals_on_display(self) -> str:
        """
        Generate a report of animals currently on display (not under treatment).
        :return: Report of animals not under treatment as a string.
        """
        display_animals = [a for a in self.__animals if not a.under_treatment]
        output = f"\nANIMALS CURRENTLY ON DISPLAY ({len(display_animals)}):"
        for animal in display_animals:
            output += f"\n - {animal.name}_{animal.id} ({animal.species})"
        output += "\n"
        return output

    def report_animal_medical_history(self, animal: Animal) -> str:
        """
        :param animal: The animal whose medical history is to be reported.
        Generate a health report for a single animal by delegating to its MedicalLog.
        :return: The animal's medical log as a string.
        """
        if animal not in self.__animals:
            raise ValueError("Animal must belong to this zoo.")
        return str(animal.medical_log)

    def report_zoo_medical_history(self) -> str:
        """
        Generate a combined health report for all animals in the zoo.
        :return: A report of all zoo animals' medical logs combined as a string.
        """
        animal_medical_log = Log("Combined Animal Medical")
        for animal in self.__animals:
            animal_medical_log.data = pd.concat([animal_medical_log.data, animal.medical_log.data])
        return str(animal_medical_log)

    def report_zoo_daily_staff_schedules(self) -> str:
        """
        Generate a combined daily schedule for all Staff in the zoo.
        :return: A Schedule with all daily schedules of zoo staff combined as a String
        """
        staff_schedule = Schedule("Combined Staff Daily")
        for member in self.__staff:
            staff_schedule.data = pd.concat([staff_schedule.data, member.generate_schedule().data])
        return str(staff_schedule)

    def report_zoo_staff_activity(self) -> str:
        """
        Generate a combined general activity log for all Staff in the zoo.
        :return: A log with all daily activity logs of zoo staff combined as a String
        """
        staff_log = Log("Combined Staff General Activity")
        for member in self.__staff:
            staff_log.data = pd.concat([staff_log.data, member.log.data])
        return str(staff_log)

    def report_zoo_enclosure_maintenance(self) -> str:
        """
        Generate a combined maintenance log for all Enclosures in the zoo.
        :return: A log with all maintenance logs of zoo enclosures combined as a String
        """
        enclosure_log = Log("Combined Enclosure Maintenance")
        for enclosure in self.__enclosures:
            enclosure_log.data = pd.concat([enclosure_log.data, enclosure.log.data])
        return str(enclosure_log)
