"""
File: veterinarian.py
Description: Contains the concrete Veterinarian class which is a subclass of the Staff class that is responsible for
providing health checks, giving diagnoses, administering treatments and declaring recoveries.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import time, datetime  # automatically handles formatting issues with dates and times.

import pandas as pd

from action import Action
from animal import Animal
from enclosure import Enclosure
from environmental_type import EnvironmentalType
from mammal import Mammal
from reptile import Reptile
from schedule import Schedule
from severity import Severity
from staff import Staff


class Veterinarian(Staff):
    def __str__(self) -> str:
        """Return the Veterinarian's key attributes as a formatted string."""
        return "\n<VETERINARIAN> " + super().__str__()

    def generate_schedule(self) -> Schedule:
        """Return the full daily schedule of responsibilities of the Veterinarian"""
        # schedule is recreated from scratch every time it is required to ensure all changes are incorporated.
        schedule = Schedule(f"{self.name}_{self.id} Daily Task")

        schedule.data = pd.concat([schedule.data, self.special_tasks.data])  # add all special (non-routine) tasks first

        for enclosure in self.enclosure_assignments:
            for animal in enclosure.inhabitants:
                # perform a health checkup on each animal in the vet's assigned enclosures:
                schedule.new({"Time": time(8),  # conduct all routine checkups each morning at 8am
                              "SubjectID": self.id,
                              "SubjectName": self.name,
                              "ObjectID": animal.id,
                              "ObjectName": animal.name,
                              "Action": Action.CHECK_HEALTH,
                              "Details": "standard"}  # no specific details for a routine (standard) checkup.
                             )
                # administer each animal's prescribed treatment(s) in the vet's assigned enclosures:
                animal_treatments = animal.treatments
                for entry in animal_treatments.data.itertuples():  # add each entry in the animal's treatment schedule.
                    schedule.new(
                        {"Time": entry.Time,
                         "SubjectID": self.id,
                         "SubjectName": self.name,
                         "ObjectID": animal.id,
                         "ObjectName": animal.name,
                         "Action": Action.TREAT,
                         "Details": entry.Details}  # get treatment details from the animal's treatment schedule.
                    )
        return schedule

    def check_health(self, animal: Animal, details: str, severity: Severity,
                     at_datetime: datetime = datetime.now()):
        """
        Check the health of an animal.
        :param at_datetime: The date and time the health check occurred (default is when method is called).
        :param animal: The animal having their health checked.
        :param details: The agenda/type of the checkup.
        :param severity: How urgent the checkup is represented as a Severity enum.
        :return: None
        """
        if not isinstance(animal, Animal):
            raise TypeError("Veterinarians can only perform a health check on Animals.")

        # record that the animal received a health check in its own logs (returns a ref number):
        log_ref_num = animal.receive_health_check(self.id, self.name, details, severity, at_datetime)

        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.id,
                      "SubjectName": self.name,
                      "ObjectID": animal.id,
                      "ObjectName": animal.name,
                      "Action": Action.CHECK_HEALTH,
                      "Details": f"log ref: {log_ref_num}"})

    def diagnose(self, animal: Animal, details: str, severity: Severity, treatment_desc: str,
                 treatment_list: list, at_datetime=datetime.now()):
        """
        Diagnose an animal with a medical condition and prescribe treatment.
        :param animal: The animal receiving the diagnosis.
        :param treatment_list: A nested list containing treatments to schedule and the time to schedule them. Format:
        [[treatment1 time (time), treatment1 desc (str)], [treatment2 time (time), treatment2 desc (str)], ...]
        :param treatment_desc: the overall description of the treatment prescribed to treat the condition.
        :param severity: How severe the condition is represented as a Severity enum.
        :param details: A description of the condition.
        :param at_datetime: The date and time at which the diagnosis was given (default is when the method is called).
        :return: None
        """

        if not isinstance(animal, Animal):
            raise TypeError("Veterinarians can only diagnose Animals.")

        # record that the animal received a diagnosis in its own logs (returns a ref number):
        log_ref_num = animal.receive_diagnosis(self.id, self.name, details, severity, treatment_desc,
                                               treatment_list, at_datetime)

        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.id,
                      "SubjectName": self.name,
                      "ObjectID": animal.id,
                      "ObjectName": animal.name,
                      "Action": Action.DIAGNOSE,
                      "Details": f"log ref: {log_ref_num}"})

    def treat(self, animal: Animal, details: str, severity: Severity, at_datetime=datetime.now()):
        """
        Administer a prescribed treatment for an animal with a medical condition.
        :param animal: The animal receiving the treatment.
        :param severity: How urgent the treatment was represented as a Severity enum.
        :param details: What the treatment involved.
        :param at_datetime: The date and time at which the treatment was given (default is when the method is called).
        :return: None
        """
        if not isinstance(animal, Animal):
            raise TypeError("Veterinarians can only treat Animals.")

        # record that the animal received a diagnosis in its own logs (returns a ref number):
        log_ref_num = animal.receive_treatment(self.id, self.name, details, severity, at_datetime)

        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.id,
                      "SubjectName": self.name,
                      "ObjectID": animal.id,
                      "ObjectName": animal.name,
                      "Action": Action.TREAT,
                      "Details": f"log ref: {log_ref_num}"})

    def declare_recovery(self, animal: Animal, details: str, at_datetime=datetime.now()):
        """
        Declare that an animal that was under treatment is now recovered and cease treatment.
        :param animal: The animal that is being declared healthy.
        :param details: Any further details of the recovery.
        :param at_datetime: The date and time at which the declaration was made (default is when the method is called).
        :return: None
        """
        if not isinstance(animal, Animal):
            raise TypeError("Veterinarians can only treat Animals")

        # record that the animal received a diagnosis in its own logs (returns a ref number):
        log_ref_num = animal.recover(self.id, self.name, details, at_datetime)

        self.log.new({"DateTime": at_datetime,
                      "SubjectID": self.id,
                      "SubjectName": self.name,
                      "ObjectID": animal.id,
                      "ObjectName": animal.name,
                      "Action": Action.DECLARE_RECOVERY,
                      "Details": f"log ref: {log_ref_num}"})


staff1 = Veterinarian("Ethan")

desert1 = Enclosure("Dune", EnvironmentalType.DESERT, 10)
desert2 = Enclosure("CactusLand", EnvironmentalType.DESERT, 10)
desert3 = Enclosure("DesertHideout", EnvironmentalType.DESERT, 10)

cobra1 = Reptile("Shai-Hulud", "King Cobra", "Hiss", "Smooth", True,
                 4, habitat=EnvironmentalType.DESERT)
cobra2 = Reptile("LittleMaker", "King Cobra", "Hiss", "Smooth", True,
                 0, habitat=EnvironmentalType.DESERT)
rattlesnake = Reptile("Sally", "Horned Rattlesnake", "Hiss", "Keeled", True,
                      4, habitat=EnvironmentalType.DESERT)
desert_mouse = Mammal("Muad'Dib", "Brown Desert Mouse", "Squeak", "Brown", True,
                      habitat=EnvironmentalType.DESERT)

desert1.add_animal(cobra1)
desert1.add_animal(cobra2)
desert2.add_animal(rattlesnake)
desert3.add_animal(desert_mouse)

staff1.assign(desert1, datetime(2004, 11, 10))
staff1.assign(desert2, datetime(2004, 11, 10))
staff1.assign(desert3, datetime(2004, 11, 10))

staff1.check_health(
    desert_mouse,
    "Behavioral assessment",
    Severity.LOW,
    datetime(2004, 11, 12, 10, 20)
)
staff1.diagnose(
    desert_mouse,
    "Psychological illness - anxiety",
    Severity.LOW,
    "Get 5 min of cuddles 2x per day.",
    [[time(11), "5 min cuddles"], [time(19), "5 min cuddles"]],
    datetime(2004, 11, 12, 10, 30)
)
staff1.special_tasks.new({"Time": time(22, 20),
                          "SubjectID": staff1.id,
                          "SubjectName": staff1.name,
                          "ObjectID": desert_mouse.id,
                          "ObjectName": desert_mouse.name,
                          "Action": Action.CHECK_HEALTH,
                          "Details": "Behavioural Review"}
                         )
print(staff1.generate_schedule())

staff1.treat(
    desert_mouse,
    "5 min cuddles",
    Severity.LOW,
    datetime(2004, 11, 12, 11, )
)
staff1.treat(
    desert_mouse,
    "5 min cuddles",
    Severity.LOW,
    datetime(2004, 11, 12, 19)
)
staff1.check_health(
    desert_mouse,
    "Behavioral review.",
    Severity.LOW,
    datetime(2004, 11, 13, 22, 20)
)
staff1.declare_recovery(
    desert_mouse,
    "Anxiety cured.",
    datetime(2004, 11, 13, 22, 35),
)

print(desert_mouse.medical_log)
print(staff1.log)
print(staff1)
