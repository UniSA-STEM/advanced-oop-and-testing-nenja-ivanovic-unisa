"""
File: test_requires_cleaning.py
Description: Suite of unit tests for the RequiresCleaning class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""

import pytest

from action import Action
from bird import Bird
from enclosure import Enclosure
from environmental_type import EnvironmentalType
from severity import Severity


class TestRequiresCleaning:
    @pytest.fixture
    def animal(self) -> Bird:
        return Bird("Pinky", "Emperor Penguin", 76, False, 2)

    @pytest.fixture
    def enclosure(self) -> Enclosure:
        return Enclosure("Dune", EnvironmentalType.DESERT, 10)

    def test_initial_state(self, animal: Bird, enclosure: Enclosure) -> None:
        assert animal.cleanliness == Severity.VERY_HIGH
        assert enclosure.cleanliness == Severity.VERY_HIGH

    def test_become_dirtier(self, animal: Bird, enclosure: Enclosure, capsys) -> None:
        animal.become_dirtier(num_levels="five")
        expected = ("[WARNING] Provided number of levels to decrease severity is non-numeric. Default value of 1 has"
                    "been assumed.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.cleanliness == Severity.HIGH
        assert animal.log.data['Action'].iloc[0] == Action.BECOME_DIRTIER
        assert animal.log.data['Details'].iloc[0] == "cleanliness is now 'High'"

        animal.become_dirtier(num_levels=-2)
        expected = ("[WARNING] Cleanliness can only decrease by a positive number of levels. Absolute value (2 levels) "
                    "has been assumed.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.cleanliness == Severity.LOW

        animal.become_dirtier(num_levels=0)
        expected = ("[WARNING] Cleanliness can only decrease by a non-zero number of levels. "
                    "Default value of 1 has been assumed.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.cleanliness == Severity.VERY_LOW

        animal.become_dirtier(num_levels=3)
        assert animal.cleanliness == Severity.VERY_LOW  # should not change as it is already at minimum.

    def test_receive_cleaning(self, animal: Bird, enclosure: Enclosure, capsys) -> None:
        animal.become_dirtier(num_levels=5)  # set to the lowest level to start
        animal.receive_cleaning("S2", "Chloe", num_levels="five")
        expected = ("[WARNING] Provided number of levels to increase severity is non-numeric. Default value of 1 has"
                    "been assumed.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.cleanliness == Severity.LOW
        assert animal.log.data['Action'].iloc[1] == Action.RECEIVE_CLEANING
        assert animal.log.data['Details'].iloc[1] == "cleanliness is now 'Low'"

        animal.receive_cleaning("S2", "Chloe", num_levels=-2)
        expected = ("[WARNING] Cleanliness can only increase by a positive number of levels. Absolute value (2 levels) "
                    "has been assumed.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.cleanliness == Severity.HIGH

        animal.receive_cleaning("S2", "Chloe", num_levels=0)
        expected = ("[WARNING] Cleanliness can only increase by a non-zero number of levels. "
                    "Default value of 1 has been assumed.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.cleanliness == Severity.VERY_HIGH

        animal.receive_cleaning("S2", "Chloe", num_levels=3)
        assert animal.cleanliness == Severity.VERY_HIGH  # should not change as it is already at minimum.
