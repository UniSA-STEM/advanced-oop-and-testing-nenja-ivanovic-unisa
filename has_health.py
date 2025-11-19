"""
File: has_health.py
Description: Contains the abstract HasHealth class which is inherited by objects that can acquire medical conditions
and require treatment (primarily Animals).
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from abc import ABC, abstractmethod
from datetime import datetime

from action import Action
from log import Log
from medical_log import MedicalLog
from schedule import Schedule
from severity import Severity


class HasHealth(ABC):
    def __init__(self):
        """
        Create a new HasHealth instance.
        """
        self.__under_treatment = False  # healthy upon initiation
        self.__medical_log = MedicalLog(
            f"{self.get_name()} Medical")  # new MedicalLog to store records of medical events.
        self.__treatments = Schedule(
            f"{self.get_name()} Treatment")  # create a new schedule to store daily treatment plan.

    def get_under_treatment(self) -> bool:
        """Get whether the object is currently receiving medical treatment: true or false. ."""
        return self.__under_treatment

    def get_medical_log(self) -> MedicalLog:
        """ Returns the log of the object's medical history."""
        return self.__medical_log

    def get_treatments(self) -> Schedule:
        """ Returns the object's daily medical treatment schedule."""
        return self.__treatments

    cleanliness = property(get_under_treatment)
    medical_log = property(get_medical_log)
    treatments = property(get_treatments)

    @abstractmethod
    def get_name(self) -> str:
        """Return a string representing the object's name."""

    @abstractmethod
    def get_id(self) -> str:
        """Return a string representing the object's unique identifier."""

    @abstractmethod
    def get_log(self) -> Log:
        """ Returns the log of the object's activities."""

    def schedule_treatments(self, treatments: list):
        """
        Add one or more treatments to the object's daily treatment schedule.
        :param treatments: A nested list containing treatments to schedule and the time to schedule them. Format:
        [[treatment1 time (time), treatment1 desc (str)], [treatment2 time (time), treatment2 desc (str)], ...]
        :return: None
        """
        for treatment in treatments:
            self.__treatments.new({"Time": treatment[0],
                                   "SubjectID": self.get_id(),
                                   "SubjectName": self.get_name(),
                                   "ObjectID": self.get_id(),
                                   "ObjectName": self.get_name(),
                                   "Action": Action.RECEIVE_TREATMENT,
                                   "Details": treatment[1],
                                   })

    def receive_health_check(self, doctor_id: str, doctor_name: str, details: str, severity: Severity,
                             at_datetime=datetime.now()) -> int:
        """
        Log that the object received a health check.
        :param severity: How urgent the checkup is represented as a Severity enum.
        :param details: The agenda of the checkup.
        :param doctor_name: The name of the object conducting the checkup.
        :param doctor_id: The id of the object conducting the checkup.
        :param at_datetime: The date and time at which the checkup occurred (default is when the method is called).
        :return: The reference number of the new row added.
        """
        return self.medical_log.new({"DateTime": at_datetime,
                                     "SubjectID": self.get_id(),
                                     "SubjectName": self.get_name(),
                                     "ObjectID": doctor_id,
                                     "ObjectName": doctor_name,
                                     "Action": Action.RECEIVE_HEALTH_CHECK,
                                     "Details": f"{details}",
                                     "Severity": severity,
                                     "Treatment": "NA"  # treatment should only be described when a diagnosis is made.
                                     })

    def receive_diagnosis(self, doctor_id: str, doctor_name: str, details: str, severity: Severity, treatment_desc: str,
                          treatment_list: list, at_datetime=datetime.now()):
        """
        Log that the object was diagnosed with a condition and the details of the condition. Add prescribed treatments
        to daily treatment schedule and change object's under_treatment status.
        :param treatment_list: A nested list containing treatments to schedule and the time to schedule them. Format:
        [[treatment1 time (time), treatment1 desc (str)], [treatment2 time (time), treatment2 desc (str)], ...]
        :param treatment_desc: the overall description of the treatment prescribed to treat the condition.
        :param severity: How severe the condition is represented as a Severity enum.
        :param details: A description of the condition.
        :param doctor_name: The name of the object giving the diagnosis.
        :param doctor_id: The id of the object giving the diagnosis.
        :param at_datetime: The date and time at which the diagnosis was given (default is when the method is called).
        :return: The reference number of the new row added.
        """
        self.schedule_treatments(treatment_list)
        self.__under_treatment = True

        return self.medical_log.new({"DateTime": at_datetime,
                                     "SubjectID": self.get_id(),
                                     "SubjectName": self.get_name(),
                                     "ObjectID": doctor_id,
                                     "ObjectName": doctor_name,
                                     "Action": Action.RECEIVE_HEALTH_CHECK,
                                     "Details": f"{details}",
                                     "Severity": severity,
                                     "Treatment": f"{treatment_desc}"
                                     })

    def receive_treatment(self, treater_id: str, treater_name: str, details: str, severity: Severity,
                          at_datetime=datetime.now()) -> int:
        """
        Log that the object received a treatment.
        :param severity: How urgent the treatment was represented as a Severity enum.
        :param details: What the treatment involved.
        :param treater_name: The name of the object giving the treatment.
        :param treater_id: The id of the object giving the treatment.
        :param at_datetime: The date and time at which the treatment was given (default is when the method is called).
        :return: The reference number of the new row added.
        """
        return self.medical_log.new({"DateTime": at_datetime,
                                     "SubjectID": self.get_id(),
                                     "SubjectName": self.get_name(),
                                     "ObjectID": treater_id,
                                     "ObjectName": treater_name,
                                     "Action": Action.RECEIVE_TREATMENT,
                                     "Details": f"{details}",
                                     "Severity": severity,
                                     "Treatment": "NA"  # treatment should only be described when a diagnosis is made.
                                     })

    def recover(self, doctor_id: str, doctor_name: str, details: str, at_datetime=datetime.now()) -> int:
        """
        Log that the object has been declared recovered, clear scheduled treatments and change under_treatment status.
        :param details: What the treatment involved.
        :param doctor_name: The name of the object declaring recovery.
        :param doctor_id: The id of the object declaring recovery.
        :param at_datetime: The date and time at which the treatment was given (default is when the method is called).
        :return: The reference number of the new row added.
        """
        self.__under_treatment = False
        self.treatments.remove()  # remove all treatments

        return self.medical_log.new({"DateTime": at_datetime,
                                     "SubjectID": self.get_id(),
                                     "SubjectName": self.get_name(),
                                     "ObjectID": doctor_id,
                                     "ObjectName": doctor_name,
                                     "Action": Action.RECOVER,
                                     "Details": f"{details}",
                                     "Severity": Severity.VERY_LOW,  # all recovery declarations are low urgency.
                                     "Treatment": "NA"  # treatment should only be described when a diagnosis is made.
                                     })
