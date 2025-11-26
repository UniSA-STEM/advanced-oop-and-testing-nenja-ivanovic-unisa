"""
File: test_data_record.py
Description: Suite of unit tests for the subclasses of the DataRecord class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime, time

import pytest

from action import Action
from log import Log
from medical_log import MedicalLog
from schedule import Schedule
from severity import Severity


class TestLog:
    @pytest.fixture
    def log1(self) -> Log:
        return Log("Jane's Activity")

    @pytest.fixture
    def medical_log1(self) -> MedicalLog:
        medical_log1 = MedicalLog("Jane's Medical")
        medical_log1.new({"DateTime": datetime(2025, 11, 18, 13), "SubjectID": "1", "SubjectName": "Jane",
                          "ObjectID": "34", "ObjectName": "John", "Action": Action.RECEIVE_HEALTH_CHECK,
                          "Details": "Standard checkup - measure weight, inspect teeth, listen to heart.",
                          "Severity": Severity.VERY_LOW, "Treatment": "NA"})
        medical_log1.new({"DateTime": datetime(2025, 11, 18, 13, 30), "SubjectID": "1", "SubjectName": "Jane",
                          "ObjectID": "34", "ObjectName": "Dr.John", "Action": Action.RECEIVE_DIAGNOSIS,
                          "Details": "Illness - Significant tooth decay from plaque on back teeth.",
                          "Severity": Severity.HIGH,
                          "Treatment": "Take pain killers every 10 hours, tooth extraction surgery ASAP."})

        medical_log1.new({"DateTime": datetime(2025, 11, 18, 13, 35), "SubjectID": "1", "SubjectName": "Jane",
                          "ObjectID": "34", "ObjectName": "Dr.John", "Action": Action.RECEIVE_TREATMENT,
                          "Details": "Medication taken - prescription pain killers.",
                          "Severity": Severity.LOW, "Treatment": "NA"})
        medical_log1.new({"DateTime": datetime(2025, 11, 18, 22, 00), "SubjectID": "1", "SubjectName": "Jane",
                          "ObjectID": "12", "ObjectName": "Zookeeper.Billy", "Action": Action.RECEIVE_TREATMENT,
                          "Details": "Medication taken - prescription pain killers.",
                          "Severity": Severity.LOW, "Treatment": "NA"})
        medical_log1.new({"DateTime": datetime(2025, 11, 19, 7, 00), "SubjectID": "1", "SubjectName": "Jane",
                          "ObjectID": "12", "ObjectName": "Surgeon.Charlie", "Action": Action.RECEIVE_TREATMENT,
                          "Details": "Extraction of teeth under anaesthesia.",
                          "Severity": Severity.VERY_HIGH, "Treatment": "Eat soft foods only for 1 week."})
        medical_log1.new({"DateTime": datetime(2025, 11, 26, 9, 00), "SubjectID": "1", "SubjectName": "Jane",
                          "ObjectID": "12", "ObjectName": "Surgeon.Charlie", "Action": Action.RECEIVE_HEALTH_CHECK,
                          "Details": "Post-op checkup",
                          "Severity": Severity.VERY_LOW, "Treatment": "NA"})
        medical_log1.new({"DateTime": datetime(2025, 11, 26, 9, 30), "SubjectID": "1", "SubjectName": "Jane",
                          "ObjectID": "34", "ObjectName": "Dr.John", "Action": Action.RECOVER,
                          "Details": "Oral disease successfully treated.",
                          "Severity": Severity.VERY_LOW,
                          "Treatment": "Cease pain killers."})
        return medical_log1

    def test_new(self, log1):
        assert len(log1.data) == 0
        assert (log1.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nJANE'S ACTIVITY LOG:"
                "\nNo data recorded."
                "\n----------------------------------------------------------------------------------------------\n")

        log1.new({"DateTime": datetime(2004, 11, 12, 13, 50),
                  "SubjectID": "1",
                  "SubjectName": "Jane",
                  "ObjectID": "1",
                  "ObjectName": "Jane",
                  "Action": Action.EAT,
                  "Details": "1x apple"})

        assert (log1.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nJANE'S ACTIVITY LOG:"
                "\n"
                "\n[2004-11-12 13:50:00] Jane_1 eats (1x apple)."
                "\n----------------------------------------------------------------------------------------------\n")
        assert len(log1.data) == 1

    def test_medical_log(self, medical_log1):
        output = medical_log1.__str__()

        # Header and footer
        assert output.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "JANE'S MEDICAL LOG:\n"
        )
        assert output.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        # Check each medical event str block
        block1 = (
            "[2025-11-18 13:00:00] Jane_1 receives health check from John_34;\n"
            " > Description: Standard checkup - measure weight, inspect teeth, listen to heart.\n"
            " > Severity: Very Low\n"
            " > Treatment: NA\n"
            "log ref number: ")
        block2 = (
            "[2025-11-18 13:30:00] Jane_1 is diagnosed by Dr.John_34;\n"
            " > Description: Illness - Significant tooth decay from plaque on back teeth.\n"
            " > Severity: High\n"
            " > Treatment: Take pain killers every 10 hours, tooth extraction surgery ASAP.\n"
            "log ref number: ")
        block3 = (
            "[2025-11-18 13:35:00] Jane_1 receives treatment from Dr.John_34;\n"
            " > Description: Medication taken - prescription pain killers.\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
            "log ref number: ")
        block4 = (
            "[2025-11-18 22:00:00] Jane_1 receives treatment from Zookeeper.Billy_12;\n"
            " > Description: Medication taken - prescription pain killers.\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
            "log ref number: ")
        block5 = (
            "[2025-11-19 07:00:00] Jane_1 receives treatment from Surgeon.Charlie_12;\n"
            " > Description: Extraction of teeth under anaesthesia.\n"
            " > Severity: Very High\n"
            " > Treatment: Eat soft foods only for 1 week.\n"
            "log ref number: ")
        block6 = (
            "[2025-11-26 09:00:00] Jane_1 receives health check from Surgeon.Charlie_12;\n"
            " > Description: Post-op checkup\n"
            " > Severity: Very Low\n"
            " > Treatment: NA\n"
            "log ref number: ")
        block7 = (
            "[2025-11-26 09:30:00] Jane_1 is declared recovered by Dr.John_34;\n"
            " > Description: Oral disease successfully treated.\n"
            " > Severity: Very Low\n"
            " > Treatment: Cease pain killers.\n"
            "log ref number: ")

        for block in (block1, block2, block3, block4, block5, block6, block7):
            assert block in output


class TestSchedule:
    @pytest.fixture
    def schedule1(self) -> Schedule:
        return Schedule("Jane's Dietary")

    @pytest.fixture
    def schedule2(self) -> Schedule:
        schedule2 = Schedule("Zookeepers' Daily")
        schedule2.new({"Time": time(9, 30), "SubjectID": "34", "SubjectName": "John", "ObjectID": "1",
                       "ObjectName": "Jane",
                       "Action": Action.FEED, "Details": "1x apple"})
        schedule2.new(
            {"Time": time(9, 30), "SubjectID": "5", "SubjectName": "Mary", "ObjectID": "1", "ObjectName": "Jane",
             "Action": Action.GIVE_WATER, "Details": "fill water tray 500mLs"})
        schedule2.new(
            {"Time": time(9, 30), "SubjectID": "34", "SubjectName": "John", "ObjectID": "1", "ObjectName": "Jane",
             "Action": Action.CHECK_HEALTH, "Details": "review burn on stomach"})
        return schedule2

    @pytest.fixture
    def schedule3(self, schedule2) -> Schedule:
        schedule3 = schedule2
        schedule3.new(
            {"Time": time(14, 00), "SubjectID": "5", "SubjectName": "Mary", "ObjectID": "1", "ObjectName": "Jane",
             "Action": Action.FEED, "Details": "3 cups milk"})
        schedule3.new({"Time": time(14, 30), "SubjectID": "5", "SubjectName": "Mary", "ObjectID": "3", "ObjectName":
            "Blue Lagoon Enclosure", "Action": Action.CLEAN, "Details": "sweep only"})
        schedule3.new(
            {"Time": time(9, 30), "SubjectID": "34", "SubjectName": "John", "ObjectID": "1", "ObjectName": "Jane",
             "Action": Action.TREAT, "Details": "apply ointment"})
        return schedule3

    def test_subject_only_record(self, schedule1):
        # subject and object of the action are the same:
        schedule1.new({"Time": time(9, 30), "SubjectID": "1", "SubjectName": "Jane", "ObjectID": "1",
                       "ObjectName": "Jane", "Action": Action.EAT, "Details": "1x apple"})
        assert (schedule1.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nJANE'S DIETARY SCHEDULE:"
                "\n\nEVENT 1 @ 09:30:00"
                "\n - Jane_1 to eat (1x apple)"
                "\n----------------------------------------------------------------------------------------------\n")

        schedule1.new({"Time": time(9, 30), "SubjectID": "1", "SubjectName": "Jane", "ObjectID": "1",
                       "ObjectName": "Jane", "Action": Action.DRINK, "Details": "3 cups milk"})
        assert (schedule1.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nJANE'S DIETARY SCHEDULE:"
                "\n\nEVENT 1 @ 09:30:00"
                "\n - Jane_1 to eat (1x apple)"
                "\n - Jane_1 to drink (3 cups milk)"
                "\n----------------------------------------------------------------------------------------------\n")

    def test_subject_object_record(self, schedule2):
        # recorded events have both a subject and object
        assert (schedule2.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nZOOKEEPERS' DAILY SCHEDULE:"
                "\n\nEVENT 1 @ 09:30:00"
                "\n - John_34 to feed Jane_1 (1x apple)"
                "\n - Mary_5 to give water to Jane_1 (fill water tray 500mLs)"
                "\n - John_34 to perform health checkup on Jane_1 (review burn on stomach)"
                "\n----------------------------------------------------------------------------------------------\n")

    def test_event_grouping(self, schedule3):
        # when events are added out of order, check that they are still grouped correctly upon display
        assert (schedule3.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nZOOKEEPERS' DAILY SCHEDULE:"
                "\n\nEVENT 1 @ 09:30:00"
                "\n - John_34 to feed Jane_1 (1x apple)"
                "\n - Mary_5 to give water to Jane_1 (fill water tray 500mLs)"
                "\n - John_34 to perform health checkup on Jane_1 (review burn on stomach)"
                "\n - John_34 to treat Jane_1 (apply ointment)"
                "\n\nEVENT 2 @ 14:00:00"
                "\n - Mary_5 to feed Jane_1 (3 cups milk)"
                "\n\nEVENT 3 @ 14:30:00"
                "\n - Mary_5 to clean Blue Lagoon Enclosure_3 (sweep only)"
                "\n----------------------------------------------------------------------------------------------\n")

    def test_remove(self, schedule3):
        schedule3.remove(time(14, 0), time(14, 15))
        assert (schedule3.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nZOOKEEPERS' DAILY SCHEDULE:"
                "\n\nEVENT 1 @ 09:30:00"
                "\n - John_34 to feed Jane_1 (1x apple)"
                "\n - Mary_5 to give water to Jane_1 (fill water tray 500mLs)"
                "\n - John_34 to perform health checkup on Jane_1 (review burn on stomach)"
                "\n - John_34 to treat Jane_1 (apply ointment)"
                "\n\nEVENT 2 @ 14:30:00"
                "\n - Mary_5 to clean Blue Lagoon Enclosure_3 (sweep only)"
                "\n----------------------------------------------------------------------------------------------\n")

        schedule3.remove()
        assert (schedule3.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nZOOKEEPERS' DAILY SCHEDULE:"
                "\nNo events scheduled."
                "\n----------------------------------------------------------------------------------------------\n")

        schedule3.remove()  # try remove when schedule is already empty
        assert (schedule3.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nZOOKEEPERS' DAILY SCHEDULE:"
                "\nNo events scheduled."
                "\n----------------------------------------------------------------------------------------------\n")
