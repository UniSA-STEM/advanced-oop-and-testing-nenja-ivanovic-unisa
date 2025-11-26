"""
File: test_has_health.py
Description: Suite of unit tests for the HasHealth class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""

from datetime import datetime, time

import pytest

from action import Action
from bird import Bird
from medical_log import MedicalLog
from severity import Severity


class TestHasHealth:
    @pytest.fixture
    def bird(self) -> Bird:
        return Bird("Pinky", "Emperor Penguin", 76, False, 2)

    def test_initial_state(self, bird: Bird) -> None:
        assert bird.under_treatment == False
        assert isinstance(bird.medical_log, MedicalLog) & (len(bird.medical_log.data) == 0)

        actual = str(bird.medical_log)
        expected = (
            f'----------------------------------------------------------------------------------------------\n'
            f'PINKY_{bird.id} MEDICAL LOG:\n'
            f'No medical history recorded.\n'
            f'----------------------------------------------------------------------------------------------\n')
        assert expected == actual

    def test_schedule_and_receive_treatments(self, bird: Bird) -> None:
        bird.schedule_treatments([[time(7), "treatment1"], [time(19), "treatment2"]])
        assert len(bird.treatments.data) == 2
        assert bird.treatments.data['Action'].iloc[0] == Action.RECEIVE_TREATMENT
        assert bird.treatments.data['Details'].iloc[0] == "treatment1"

        bird.receive_treatment("S34", "Dr.John", "treatment1", Severity.LOW,
                               datetime(2004, 11, 12, 7))
        assert bird.medical_log.data['Action'].iloc[0] == Action.RECEIVE_TREATMENT
        assert bird.medical_log.data['Details'].iloc[0] == "treatment1"

    def test_receive_health_check(self, bird: Bird) -> None:
        bird.receive_health_check("S34", "Dr.John", "Behavioral assessment",
                                  Severity.LOW, datetime(2004, 11, 12, 16, 20))
        assert bird.medical_log.data['Action'].iloc[0] == Action.RECEIVE_HEALTH_CHECK
        assert bird.medical_log.data['Details'].iloc[0] == "Behavioral assessment"

    def test_receive_diagnosis_and_recover(self, bird: Bird) -> None:
        bird.receive_diagnosis("S34", "Dr.John", "Psychological illness - anxiety",
                               Severity.LOW, "Get 5 min of cuddles every 12 hours.",
                               [[time(7), "5 min cuddles"], [time(19), "5 min cuddles"]],
                               datetime(2004, 11, 12, 10, 30))

        assert len(bird.treatments.data) == 2
        assert bird.under_treatment == True
        assert bird.medical_log.data['Action'].iloc[0] == Action.RECEIVE_DIAGNOSIS
        assert bird.medical_log.data['Details'].iloc[0] == "Psychological illness - anxiety"

        bird.recover("S34", "Dr.John", "Anxiety cured.",
                     datetime(2004, 11, 12, 13, 20))
        assert bird.under_treatment == False
        assert len(bird.treatments.data) == 0  # treatments wiped
        assert bird.medical_log.data['Action'].iloc[1] == Action.RECOVER
        assert bird.medical_log.data['Details'].iloc[1] == "Anxiety cured."
