"""
File: test_animal.py
Description: Suite of unit tests for the subclasses of the Animal class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime, time

import pytest

from action import Action
from bird import Bird
from environmental_type import EnvironmentalType
from mammal import Mammal
from reptile import Reptile


class TestAnimal:
    @pytest.fixture
    def bird(self) -> Bird:
        return Bird("Pinky", "Emperor Penguin", 76, False, 2)

    @pytest.fixture
    def mammal(self) -> Mammal:
        return Mammal("Momo", "Monkey", "Oooh-ooh-ah", "Yellow-brown", False, 3)

    @pytest.fixture
    def reptile(self) -> Reptile:
        return Reptile("Lizzy", "Komodo Dragon", "Hiss", "rough", True, 5)

    @pytest.fixture
    def datetime1(self) -> datetime:
        return datetime(2004, 11, 12)

    def test_animal_initialization_error_handling(self, capsys):
        # incorrect value type provided for habitat:
        animal = Bird("Pinky", "Emperor Penguin", 76, False, 2, 34)
        expected = ("[WARNING] Provided animal age was not an EnvironmentalType, so default value "
                    "of EnvironmentalType.GRASS years was assumed.")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.habitat == EnvironmentalType.GRASS

        # incorrect negative number provided for age:
        animal = Bird("Pinky", "Emperor Penguin", 76, False, -4)
        expected = ("[WARNING] Provided animal age was negative, so absolute value was used (4 "
                    "years).")
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.age == 4

        # incorrect value type provided for age:
        animal = Bird("Pinky", "Emperor Penguin", 76, False, "three")
        expected = f"[WARNING] Provided animal age was not numeric, so default value of 0 years was assumed."
        actual = capsys.readouterr().out.strip()
        assert expected == actual
        assert animal.age == 0

    def test_bird(self, bird: Bird) -> None:
        # incorrect value type provided for can_fly:
        bird2 = Bird("Eloise", "Eagle", 30)

        bird.fly()

        assert bird.log.data['Action'].iloc[0] == Action.FLY
        assert bird.log.data['Details'].iloc[0] == "fails"  # penguin cannot fly

        bird2.fly()
        assert bird2.log.data['Details'].iloc[0] == "succeeds"  # can_fly is True by default

        actual = str(bird)
        expected = (f"ID: {bird.id} | NAME: Pinky | SPECIES: Emperor Penguin\n"
                    f" > Age: 2 year(s) old.\n"
                    f" > Health Status: [HEALTHY]\n"
                    f" > Cleanliness: Very High\n"
                    f" > Wingspan: 76cm\n"
                    f" > Can fly: False\n")
        assert expected == actual

    def test_mammal(self, mammal: Mammal) -> None:
        mammal.groom()
        assert mammal.log.data['Action'].iloc[0] == Action.GROOM
        assert mammal.log.data['Details'].iloc[0] == "picks at its yellow-brown fur"

        actual = str(mammal)
        expected = (f"ID: {mammal.id} | NAME: Momo | SPECIES: Monkey\n"
                    f" > Age: 3 year(s) old.\n"
                    f" > Health Status: [HEALTHY]\n"
                    f" > Cleanliness: Very High\n"
                    f" > Fur colour: Yellow-brown\n"
                    f" > Nocturnal: False\n")
        assert expected == actual

    def test_reptile(self, reptile: Reptile) -> None:
        reptile.bask()
        assert reptile.log.data['Action'].iloc[0] == Action.BASK
        assert reptile.log.data['Details'].iloc[0] == "to regulate body temperature"

        actual = str(reptile)
        expected = (f"ID: {reptile.id} | NAME: Lizzy | SPECIES: Komodo Dragon\n"
                    f" > Age: 5 year(s) old.\n"
                    f" > Health Status: [HEALTHY]\n"
                    f" > Cleanliness: Very High\n"
                    f" > Scale type: rough\n"
                    f" > Venomous: True\n")
        assert expected == actual

    def test_general_animal_behaviours(self, bird: Bird, datetime1):
        bird.eat("apple", "2x whole", datetime1)
        bird.drink("water", "1 cup", datetime1)
        bird.sleep(datetime1)
        bird.make_sound(datetime1)

        bird.become_older(datetime1)
        assert bird.age == 3

        actual = str(bird.log)
        expected = (
            f'----------------------------------------------------------------------------------------------\n'
            f'PINKY_{bird.id} GENERAL ACTIVITY LOG:\n'
            f'\n'
            f'[2004-11-12 00:00:00] Pinky_{bird.id} eats (2x whole apple).\n'
            f'[2004-11-12 00:00:00] Pinky_{bird.id} drinks (1 cup water).\n'
            f'[2004-11-12 00:00:00] Pinky_{bird.id} sleeps (Zzz...).\n'
            f"[2004-11-12 00:00:00] Pinky_{bird.id} says ('Squawk').\n"
            f'[2004-11-12 00:00:00] Pinky_{bird.id} ages (by 1 year(s) to become 3 year(s) old).\n'
            f'----------------------------------------------------------------------------------------------\n')
        assert actual == expected

    def test_diet_schedule_add_and_remove(self, bird: Bird) -> None:
        bird.add_to_diet("fish", "3x whole", time(9, 0))
        bird.add_to_diet("squid", "200g", time(19, 0))

        actual = str(bird.diet)
        expected = (
            f"----------------------------------------------------------------------------------------------\n"
            f"PINKY_{bird.id} DIETARY SCHEDULE:\n"
            f"\n"
            f"EVENT 1 @ 09:00:00\n"
            f" - Pinky_{bird.id} to eat (3x whole fish)\n"
            f"\n"
            f"EVENT 2 @ 19:00:00\n"
            f" - Pinky_{bird.id} to eat (200g squid)\n"
            f"----------------------------------------------------------------------------------------------\n")
        assert expected == actual
