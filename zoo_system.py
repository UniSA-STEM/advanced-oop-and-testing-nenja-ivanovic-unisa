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
from medical_log import MedicalLog
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

    name = property(get_name)
    animals = property(get_animals)
    enclosures = property(get_enclosures)
    staff = property(get_staff)

    # adding, removing, moving and assignment -----------------------------------------------------------------

    def add_animal(self, animal: Animal) -> None:
        """
        Add an Animal to the zoo.
        :param animal: The Animal to add to the zoo.
        :return: None
        """
        try:
            if not isinstance(animal, Animal):
                raise TypeError("Only Animal instances can be added to the zoo animals.")
            if animal not in self.__animals:
                self.__animals.append(animal)
        except TypeError as e:
            print(f"[ERROR] {e} No change made.\n")

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
        try:
            if not isinstance(enclosure, Enclosure):
                raise TypeError("Only Enclosure instances can be added to the zoo enclosures.")
            if len(enclosure.inhabitants) > 0:
                raise ValueError(f"{enclosure.name}_{enclosure.id} cannot be added as it is not empty.")
            if enclosure not in self.__enclosures:
                self.__enclosures.append(enclosure)
        except (TypeError, ValueError) as e:
            print(f"[ERROR] {e} No change made.\n")

    def remove_enclosure(self, enclosure: Enclosure) -> None:
        """
        Remove an Enclosure from the zoo - enclosures must be empty before removal.
        :param enclosure: The enclosure to remove from the zoo (must be empty).
        :return: None
        """
        try:
            if not isinstance(enclosure, Enclosure):
                raise TypeError("Only Enclosure instances can be removed from the zoo enclosures.")
            if len(enclosure.inhabitants) > 0:
                raise ValueError(f"{enclosure.name}_{enclosure.id} cannot be removed as it is not empty.")
            if enclosure in self.__enclosures:
                self.__enclosures.remove(enclosure)
        except (TypeError, ValueError) as e:
            print(f"[ERROR] {e} No change made.\n")

    def add_staff_member(self, staff_member: Staff) -> None:
        """Add a Staff member to the zoo.
        :param staff_member: The staff member to add to the zoo.
        """
        try:
            if not isinstance(staff_member, Staff):
                raise TypeError("Only Staff instances can be added to the zoo staff.")
            if staff_member not in self.__staff:
                self.__staff.append(staff_member)
        except TypeError as e:
            print(f"[ERROR] {e} No change made.\n")

    def remove_staff_member(self, staff_member: Staff) -> None:
        """
        Remove a Staff member from the zoo.
        :param staff_member: The staff member to remove from the zoo.
        """
        try:
            if not isinstance(staff_member, Staff):
                raise TypeError("Only Staff instances can be removed from the zoo staff.")

            if staff_member in self.__staff:
                self.__staff.remove(staff_member)
        except TypeError as e:
            print(f"[ERROR] {e} No change made.\n")

    def assign_staff_to_enclosure(self, staff_member: Staff, enclosure: Enclosure,
                                  at_datetime: datetime) -> None:
        """
        Assign a member of staff to an enclosure.
        :param staff_member: The staff member to assign to the enclosure.
        :param enclosure: The enclosure the staff member is being assigned to.
        :param at_datetime: The date and time at which the assignment was made (default is when method is called).
        :return: None
        """
        try:
            if staff_member not in self.__staff:
                raise ValueError("Staff member must belong to this zoo before assignment.")
            if enclosure not in self.__enclosures:
                raise ValueError("Enclosure must belong to this zoo before assignment.")

            staff_member.assign(enclosure, at_datetime)
        except ValueError as e:
            print(f"[ERROR] {e} No change made.\n")

    def assign_animal_to_enclosure(self, animal: Animal, enclosure: Enclosure) -> None:
        """
        Assign a member of staff to an enclosure.
        :param animal: The animal to assign to the enclosure.
        :param enclosure: The enclosure the animal is being assigned to.
        :return: None
        """
        try:
            if animal not in self.__animals:
                raise ValueError(f"Animal must belong to {self.name} before it can be assigned to an enclosure.")
            if enclosure not in self.__enclosures:
                raise ValueError(f"Enclosure must belong to {self.name} before it can receive animals.")
            enclosure.add_animal(animal)  # checks that animal is not under treatment internally

        except ValueError as e:
            print(f"[ERROR] {e} No change made.\n")

    def move_animal(self, animal: Animal, from_enclosure: Enclosure, to_enclosure: Enclosure) -> None:
        """
        Move an animal from one enclosure to another. This will respect all existing rules in
        Enclosure (habitat, species, treatment status).
        :param animal: The animal being relocated.
        :param from_enclosure: Where the animal is currently located.
        :param to_enclosure: Where the animal is to be relocated.
        :return: None
        """
        try:
            if from_enclosure not in self.__enclosures or to_enclosure not in self.__enclosures:
                raise ValueError("Both enclosures must belong to this zoo.")

            if animal not in from_enclosure.inhabitants:
                raise ValueError(
                    f"{animal.name}_{animal.id} does not live in {from_enclosure.name}_{from_enclosure.id}.")

            from_enclosure.remove_animal(animal)
            to_enclosure.add_animal(animal)

        except ValueError as e:
            print(f"[ERROR] {e} No change made.\n")

    # reporting  ------------------------------------------------------------------------------------------------

    def report_species(self) -> str:
        """
        Generate a text report listing animals grouped by species.
        :return: Report of animals grouped by species as a string.
        """
        species = [animal.species for animal in self.animals]
        species = list(set(species))  # remove duplicates
        output = (f"----------------------------------------------------------------------------------------------\n"
                  f"ANIMALS BY SPECIES ({len(self.__animals)} total):\n")

        for name in species:
            animals = [animal for animal in self.animals if animal.species == name]
            output += f"\n{name} ({len(animals)}):"
            for animal in animals:
                output += f"\n - {animal.name}_{animal.id}"
            output += "\n"
        output += "\n----------------------------------------------------------------------------------------------\n"
        return output

    def report_enclosure_status(self) -> str:
        """
        Generate a text report describing the status of each enclosure: environment, cleanliness, and occupancy.
        :return: Report of enclosure information as a string.
        """
        output = f"----------------------------------------------------------------------------------------------\n" \
                 "ENCLOSURE STATUS REPORT:\n"
        for enclosure in self.__enclosures:
            output += ("\n" + str(enclosure))

        output += "\n----------------------------------------------------------------------------------------------\n"
        return output

    def report_animals_on_display(self) -> str:
        """
        Generate a report of animals currently on display (not under treatment).
        :return: Report of animals not under treatment as a string.
        """
        display_animals = [a for a in self.__animals if not a.under_treatment]
        output = (
            f"----------------------------------------------------------------------------------------------\n"
            f"ANIMALS CURRENTLY ON DISPLAY ({len(display_animals)}): \n")
        for animal in display_animals:
            output += f"\n - {animal.name}_{animal.id} ({animal.species})"
        output += "\n----------------------------------------------------------------------------------------------\n"
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
        animal_medical_log = MedicalLog("Combined Animal Medical")
        medical_logs = [animal.medical_log.data for animal in self.__animals if not animal.medical_log.data.empty]

        if len(medical_logs):
            animal_medical_log.data = pd.concat(medical_logs)

        return str(animal_medical_log)

    def report_zoo_daily_staff_schedules(self) -> str:
        """
        Generate a combined daily schedule for all Staff in the zoo.
        :return: A Schedule with all daily schedules of zoo staff combined as a String
        """
        staff_schedule = Schedule("Combined Staff Daily")

        daily_schedules = []
        for member in self.__staff:
            member_schedule = member.generate_schedule()
            if not member_schedule.data.empty:
                daily_schedules.append(member_schedule.data)

        if len(daily_schedules) > 0:
            staff_schedule.data = pd.concat(daily_schedules)

        return str(staff_schedule)

    def report_zoo_staff_activity(self) -> str:
        """
        Generate a combined general activity log for all Staff in the zoo.
        :return: A log with all daily activity logs of zoo staff combined as a String
        """
        staff_log = Log("Combined Staff General Activity")
        activity_logs = [member.log.data for member in self.__staff if not member.log.data.empty]

        if len(activity_logs) > 0:
            staff_log.data = pd.concat(activity_logs)

        return str(staff_log)

    def report_zoo_enclosure_maintenance(self) -> str:
        """
        Generate a combined maintenance log for all Enclosures in the zoo.
        :return: A log with all maintenance logs of zoo enclosures combined as a String
        """
        enclosure_log = Log("Combined Enclosure Maintenance")
        maintenance_logs = [enclosure.log.data for enclosure in self.__enclosures if not enclosure.log.data.empty]

        if len(maintenance_logs) > 0:
            enclosure_log.data = pd.concat(maintenance_logs)

        return str(enclosure_log)
