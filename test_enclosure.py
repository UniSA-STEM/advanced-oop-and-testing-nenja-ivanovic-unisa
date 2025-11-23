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
        return Reptile(
            "Shai-Hulud", "King Cobra", "Hiss", "Smooth", True, 4,
            habitat=EnvironmentalType.DESERT
        )

    @pytest.fixture
    def cobra2(self) -> Reptile:
        return Reptile(
            "LittleMaker", "King Cobra", "Hiss", "Smooth", True, 0,
            habitat=EnvironmentalType.DESERT
        )

    @pytest.fixture
    def rattlesnake(self) -> Reptile:
        return Reptile(
            "Sally", "Horned Rattlesnake", "Hiss", "Keeled", True, 4,
            habitat=EnvironmentalType.DESERT
        )

    @pytest.fixture
    def desert_mouse(self) -> Mammal:
        return Mammal(
            "Muad'Dib", "Brown Desert Mouse", "Squeak", "Brown", True,
            habitat=EnvironmentalType.DESERT
        )

    def test_initial_str_empty_desert(self, desert1: Enclosure) -> None:
        s = str(desert1)
        expected = (
            f"ID: {desert1.id} | NAME: {desert1.name} | ENVIRONMENTAL TYPE: {desert1.environmental_type.value}\n"
            f" > Species: {desert1.species}\n"
            f" > Size: {desert1.size} squared centimeters\n"
            f" > Cleanliness: {desert1.cleanliness.description}\n"
            f" > Inhabitants: 0\n"
        )
        assert s == expected

    def test_cannot_add_wrong_habitat(self, aquatic1: Enclosure, cobra1: Reptile) -> None:
        with pytest.raises(ValueError) as excinfo:
            aquatic1.add_animal(cobra1)
        expected_msg = (
            f"{cobra1.name}_{cobra1.id} requires a(n) "
            f"{cobra1.habitat.value.upper()} habitat and cannot live in "
            f"a(n) {aquatic1.environmental_type.value.upper()} enclosure."
        )
        assert str(excinfo.value) == expected_msg

    def test_add_animals_and_species_rules(
            self,
            desert1: Enclosure,
            cobra1: Reptile,
            cobra2: Reptile,
            desert_mouse: Mammal,
            rattlesnake: Reptile,
    ) -> None:
        desert1.add_animal(cobra1)

        s1 = str(desert1)
        expected1 = (
            f"ID: {desert1.id} | NAME: {desert1.name} | ENVIRONMENTAL TYPE: {desert1.environmental_type.value}\n"
            f" > Species: {cobra1.species}\n"
            f" > Size: {desert1.size} squared centimeters\n"
            f" > Cleanliness: {desert1.cleanliness.description}\n"
            f" > Inhabitants: 1\n"
            f"   > {cobra1.name}_{cobra1.id}\n"
        )
        assert s1 == expected1

        desert1.add_animal(cobra1)
        assert len(desert1.inhabitants) == 1

        desert1.add_animal(cobra2)
        s2 = str(desert1)
        expected2 = (
            f"ID: {desert1.id} | NAME: {desert1.name} | ENVIRONMENTAL TYPE: {desert1.environmental_type.value}\n"
            f" > Species: {cobra1.species}\n"
            f" > Size: {desert1.size} squared centimeters\n"
            f" > Cleanliness: {desert1.cleanliness.description}\n"
            f" > Inhabitants: 2\n"
            f"   > {cobra1.name}_{cobra1.id}\n"
            f"   > {cobra2.name}_{cobra2.id}\n"
        )
        assert s2 == expected2

        with pytest.raises(ValueError) as exc_mouse:
            desert1.add_animal(desert_mouse)
        expected_mouse_msg = (
            f"{desert_mouse.name}_{desert_mouse.id} cannot live in "
            f"{desert1.name}_{desert1.id} as animals of a different species already live there "
            f"({desert1.species})."
        )
        assert str(exc_mouse.value) == expected_mouse_msg

        with pytest.raises(ValueError) as exc_rattle:
            desert1.add_animal(rattlesnake)
        expected_rattle_msg = (
            f"{rattlesnake.name}_{rattlesnake.id} cannot live in "
            f"{desert1.name}_{desert1.id} as animals of a different species already live there "
            f"({desert1.species})."
        )
        assert str(exc_rattle.value) == expected_rattle_msg

    def test_remove_animals_and_errors(
            self,
            desert1: Enclosure,
            cobra1: Reptile,
            cobra2: Reptile,
    ) -> None:
        desert1.add_animal(cobra1)
        desert1.add_animal(cobra2)

        desert1.remove_animal(cobra2)
        s = str(desert1)
        expected = (
            f"ID: {desert1.id} | NAME: {desert1.name} | ENVIRONMENTAL TYPE: {desert1.environmental_type.value}\n"
            f" > Species: {cobra1.species}\n"
            f" > Size: {desert1.size} squared centimeters\n"
            f" > Cleanliness: {desert1.cleanliness.description}\n"
            f" > Inhabitants: 1\n"
            f"   > {cobra1.name}_{cobra1.id}\n"
        )
        assert s == expected

        with pytest.raises(AssertionError) as excinfo:
            desert1.remove_animal(cobra2)
        assert (
                f"{cobra2.name}_{cobra2.id} does not live in {desert1.name}_{desert1.id}"
                in str(excinfo.value)
        )

    def test_cannot_remove_under_treatment_and_final_state(
            self,
            desert1: Enclosure,
            cobra1: Reptile,
            desert_mouse: Mammal,
    ) -> None:
        desert1.add_animal(cobra1)

        cobra1.receive_diagnosis(
            "S34",
            "Dr.John",
            "Illness - food poisoning.",
            Severity.MODERATE,
            "Take antidote",
            [[time(9), "Take antidote"]],
            datetime(2004, 11, 12, 10, 30),
        )

        with pytest.raises(ValueError) as excinfo:
            desert1.remove_animal(cobra1)
        expected_msg = (
            f"{cobra1.name}_{cobra1.id} is under treatment so they cannot be relocated at this time."
        )
        assert str(excinfo.value) == expected_msg

        cobra1.recover("S34", "Dr.John", "Full recovery of food poisoning.")
        desert1.remove_animal(cobra1)

        s_empty = str(desert1)
        expected_empty = (
            f"ID: {desert1.id} | NAME: {desert1.name} | ENVIRONMENTAL TYPE: {desert1.environmental_type.value}\n"
            f" > Species: {desert1.species}\n"
            f" > Size: {desert1.size} squared centimeters\n"
            f" > Cleanliness: {desert1.cleanliness.description}\n"
            f" > Inhabitants: 0\n"
        )
        assert s_empty == expected_empty

        desert1.add_animal(desert_mouse)
        s_mouse = str(desert1)
        expected_mouse = (
            f"ID: {desert1.id} | NAME: {desert1.name} | ENVIRONMENTAL TYPE: {desert1.environmental_type.value}\n"
            f" > Species: {desert_mouse.species}\n"
            f" > Size: {desert1.size} squared centimeters\n"
            f" > Cleanliness: {desert1.cleanliness.description}\n"
            f" > Inhabitants: 1\n"
            f"   > {desert_mouse.name}_{desert_mouse.id}\n"
        )
        assert s_mouse == expected_mouse
