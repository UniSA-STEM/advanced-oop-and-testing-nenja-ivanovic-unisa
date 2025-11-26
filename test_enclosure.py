"""
File: test_enclosure.py
Description: Suite of unit tests for the Enclosure class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime, time

import pytest

from enclosure import Enclosure
from environmental_type import EnvironmentalType
from mammal import Mammal
from reptile import Reptile
from severity import Severity


class TestEnclosure:
    @pytest.fixture
    def aquatic1(self) -> Enclosure:
        return Enclosure("BlueLagoon", EnvironmentalType.AQUATIC, 5)

    @pytest.fixture
    def desert1(self) -> Enclosure:
        return Enclosure("Dune", EnvironmentalType.DESERT, 10)

    @pytest.fixture
    def cobra1(self) -> Reptile:
        return Reptile("Shai-Hulud", "King Cobra", "Hiss", "Smooth", True,
                       4, habitat=EnvironmentalType.DESERT)

    @pytest.fixture
    def cobra2(self) -> Reptile:
        return Reptile("LittleMaker", "King Cobra", "Hiss", "Smooth", True,
                       0, habitat=EnvironmentalType.DESERT)

    @pytest.fixture
    def rattlesnake(self) -> Reptile:
        return Reptile("Sally", "Horned Rattlesnake", "Hiss", "Keeled", True,
                       4, habitat=EnvironmentalType.DESERT)

    @pytest.fixture
    def desert_mouse(self) -> Mammal:
        return Mammal("Muad'Dib", "Brown Desert Mouse", "Squeak", "Brown", True,
                      habitat=EnvironmentalType.DESERT)

    def test_initial_str_empty_desert(self, desert1: Enclosure) -> None:
        expected = (f"ID: {desert1.id} | NAME: Dune | ENVIRONMENTAL TYPE: Desert\n"
                    f" > Species: None\n"
                    f" > Size: 10 squared meters\n"
                    f" > Cleanliness: Very High\n"
                    f" > Inhabitants: 0\n")
        actual = str(desert1)
        assert actual == expected

    def test_cannot_add_wrong_habitat(self, aquatic1: Enclosure, cobra1: Reptile, capsys) -> None:
        aquatic1.add_animal(cobra1)
        expected = (f"[ERROR] Shai-Hulud_{cobra1.id} requires a(n) DESERT habitat and cannot live in a(n) AQUATIC "
                    f"enclosure. No change made.")
        actual = capsys.readouterr().out.strip()
        assert cobra1 not in aquatic1.inhabitants
        assert expected == actual

    def test_add_animals_and_species_rules(self, desert1: Enclosure, cobra1: Reptile, cobra2: Reptile,
                                           desert_mouse: Mammal, rattlesnake: Reptile, capsys) -> None:
        desert1.add_animal(cobra1)
        assert len(desert1.inhabitants) == 1
        assert desert1.inhabitants[0] == cobra1

        desert1.add_animal(cobra1)
        assert len(desert1.inhabitants) == 1  # there should not be duplicate of cobra1.

        desert1.add_animal(cobra2)
        assert desert1.inhabitants == [cobra1, cobra2]

        expected = (
            f"ID: {desert1.id} | NAME: Dune | ENVIRONMENTAL TYPE: Desert\n"
            f" > Species: King Cobra\n"
            f" > Size: 10 squared meters\n"
            f" > Cleanliness: Very High\n"
            f" > Inhabitants: 2\n"
            f"   > Shai-Hulud_{cobra1.id}\n"
            f"   > LittleMaker_{cobra2.id}\n"
        )
        actual = str(desert1)
        assert expected == actual

        desert1.add_animal(desert_mouse)
        expected = (
            f"[ERROR] Muad'Dib_{desert_mouse.id} cannot live in Dune_E3 as animals of a different species already live there"
            f" (King Cobra). No change made.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert desert_mouse not in desert1.inhabitants

    def test_remove_animals(self, desert1: Enclosure, cobra1: Reptile, cobra2: Reptile) -> None:
        desert1.add_animal(cobra1)
        desert1.add_animal(cobra2)

        desert1.remove_animal(cobra2)
        assert desert1.inhabitants == [cobra1]

        desert1.remove_animal(cobra2)  # try remove again
        assert desert1.inhabitants == [cobra1]  # there should be no change

        desert1.remove_animal(cobra1)
        assert cobra1 not in desert1.inhabitants
        assert desert1.species is None  # species should be reset as enclosure is now empty

    def test_cannot_remove_under_treatment(self, desert1: Enclosure, cobra1: Reptile, desert_mouse: Mammal,
                                           capsys) -> None:
        desert1.add_animal(cobra1)
        cobra1.receive_diagnosis("S34", "Dr.John", "Illness - food poisoning.",
                                 Severity.MODERATE, "Take antidote", [[time(9), "Take antidote"]],
                                 datetime(2004, 11, 12, 10, 30))

        desert1.remove_animal(cobra1)
        assert cobra1 in desert1.inhabitants  # should not have been removed
        expected = f"[ERROR] Shai-Hulud_{cobra1.id} is under treatment so they cannot be relocated at this time. No change made."
        actual = capsys.readouterr().out.strip()
        assert expected == actual

        cobra1.recover("S34", "Dr.John", "Full recovery of food poisoning.")
        desert1.remove_animal(cobra1)  # should now succeed that cobra is recovered.
