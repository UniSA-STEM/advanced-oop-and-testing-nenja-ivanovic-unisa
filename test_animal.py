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

from bird import Bird
from mammal import Mammal
from severity import Severity


class TestAnimal:
    @pytest.fixture
    def bird(self) -> Bird:
        return Bird("Pinky", "Emperor Penguin", 76, False, 2)

    # Basic printing / initial state -----------------------------------------------------------------------

    def test_initial_str(self, bird: Bird) -> None:
        expected = (
            "ID: A1 | NAME: Pinky | SPECIES: Emperor Penguin\n"
            " > Age: 2 year(s) old.\n"
            " > Health Status: [HEALTHY]\n"
            " > Cleanliness: Very High\n"
            " > Wingspan: 76cm\n"
            " > Can fly: False\n"
        )
        assert str(bird) == expected

    # Health status after diagnosis ------------------------------------------------------------------------

    def test_health_status_and_medical_log_after_diagnosis(self, bird: Bird) -> None:
        bird.receive_health_check(
            "S34",
            "Dr.John",
            "Behavioral assessment",
            Severity.LOW,
            datetime(2004, 11, 12, 10, 20),
        )
        bird.receive_diagnosis(
            "S34",
            "Dr.John",
            "Psychological illness - anxiety",
            Severity.LOW,
            "Get 5 min of cuddles every 12 hours.",
            [[time(7), "5 min cuddles"], [time(19), "5 min cuddles"]],
            datetime(2004, 11, 12, 10, 30),
        )

        expected_str = (
            "ID: A2 | NAME: Pinky | SPECIES: Emperor Penguin\n"
            " > Age: 2 year(s) old.\n"
            " > Health Status: [UNDER TREATMENT]\n"
            " > Cleanliness: Very High\n"
            " > Wingspan: 76cm\n"
            " > Can fly: False\n"
        )
        assert str(bird) == expected_str

    # Full medical timeline (after treatments + recovery) --------------------------------------------------

    def test_medical_log_after_treatments_and_recovery(self, bird: Bird) -> None:
        bird.receive_health_check(
            "S34",
            "Dr.John",
            "Behavioral assessment",
            Severity.LOW,
            datetime(2004, 11, 12, 10, 20),
        )
        bird.receive_diagnosis(
            "S34",
            "Dr.John",
            "Psychological illness - anxiety",
            Severity.LOW,
            "Get 5 min of cuddles every 12 hours.",
            [[time(7), "5 min cuddles"], [time(19), "5 min cuddles"]],
            datetime(2004, 11, 12, 10, 30),
        )
        bird.receive_treatment(
            "S34",
            "Dr.John",
            "5 min cuddles",
            Severity.LOW,
            datetime(2004, 11, 12, 10, 35),
        )
        bird.receive_treatment(
            "S2",
            "Chloe",
            "5 min cuddles",
            Severity.LOW,
            datetime(2004, 11, 12, 19, 0),
        )
        bird.receive_health_check(
            "S34",
            "Dr.John",
            "Behavioral review.",
            Severity.LOW,
            datetime(2004, 11, 13, 10, 20),
        )
        bird.recover(
            "S34",
            "Dr.John",
            "Anxiety cured.",
            datetime(2004, 11, 13, 10, 35),
        )

        expected_med_log = (
            "----------------------------------------------------------------------------------------------\n"
            "PINKY_A3 MEDICAL LOG:\n"
            "\n"
            "[2004-11-12 10:20:00] Pinky_A3 receives health check from Dr.John_S34;\n"
            " > Description: Behavioral assessment\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
            "log ref number: 4\n"
            "\n"
            "[2004-11-12 10:30:00] Pinky_A3 is diagnosed by Dr.John_S34;\n"
            " > Description: Psychological illness - anxiety\n"
            " > Severity: Low\n"
            " > Treatment: Get 5 min of cuddles every 12 hours.\n"
            "log ref number: 7\n"
            "\n"
            "[2004-11-12 10:35:00] Pinky_A3 receives treatment from Dr.John_S34;\n"
            " > Description: 5 min cuddles\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
            "log ref number: 8\n"
            "\n"
            "[2004-11-12 19:00:00] Pinky_A3 receives treatment from Chloe_S2;\n"
            " > Description: 5 min cuddles\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
            "log ref number: 9\n"
            "\n"
            "[2004-11-13 10:20:00] Pinky_A3 receives health check from Dr.John_S34;\n"
            " > Description: Behavioral review.\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
            "log ref number: 10\n"
            "\n"
            "[2004-11-13 10:35:00] Pinky_A3 is declared recovered by Dr.John_S34;\n"
            " > Description: Anxiety cured.\n"
            " > Severity: Very Low\n"
            " > Treatment: NA\n"
            "log ref number: 11\n"
            "----------------------------------------------------------------------------------------------\n"
        )
        assert str(bird.medical_log) == expected_med_log

    # General activity log + age / cleanliness changes -----------------------------------------------------

    def test_general_activity_log_and_cleanliness(self, bird: Bird) -> None:
        bird.fly(datetime(2004, 11, 12, 6, 0))
        bird.fly(datetime(2004, 11, 12, 6, 20))
        bird.fly(datetime(2004, 11, 12, 6, 45))
        bird.eat("fish", "3x whole", datetime(2004, 11, 12, 9, 0))
        bird.drink("water", "500mL", datetime(2004, 11, 12, 12, 10))
        bird.sleep(datetime(2004, 11, 12, 12, 40))
        bird.eat("squid", "200g", datetime(2004, 11, 12, 18, 50))
        bird.become_older(datetime(2004, 11, 13, 10, 35))
        bird.become_dirtier(datetime(2004, 11, 13, 11, 0), 7)
        bird.receive_cleaning("S2", "Chloe", datetime(2004, 11, 13, 12, 0), 2)

        expected_str = (
            "ID: A4 | NAME: Pinky | SPECIES: Emperor Penguin\n"
            " > Age: 3 year(s) old.\n"
            " > Health Status: [HEALTHY]\n"
            " > Cleanliness: Moderate\n"
            " > Wingspan: 76cm\n"
            " > Can fly: False\n"
        )
        assert str(bird) == expected_str

    # Diet schedule ----------------------------------------------------------------------------------------

    def test_diet_schedule_add_and_remove(self, bird: Bird) -> None:
        bird.add_to_diet("fish", "3x whole", time(9, 0))
        bird.add_to_diet("squid", "200g", time(19, 0))

        expected_diet_full = (
            "----------------------------------------------------------------------------------------------\n"
            "PINKY_A5 DIETARY SCHEDULE:\n"
            "\n"
            "EVENT 1 @ 09:00:00\n"
            " - Pinky_A5 to eat (3x whole fish)\n"
            "\n"
            "EVENT 2 @ 19:00:00\n"
            " - Pinky_A5 to eat (200g squid)\n"
            "----------------------------------------------------------------------------------------------\n"
        )
        assert str(bird.diet) == expected_diet_full

    # Mammal -----------------------------------------------------------------------------------------------------
    @pytest.fixture
    def mammal(self) -> Mammal:
        return Mammal("Momo", "Monkey", "Oooh-ooh-ah", "Yellow-brown", False, 3)

    def test_mammal_str_and_groom_log(self, mammal: Mammal) -> None:
        assert (str(mammal) ==
                'ID: A6 | NAME: Momo | SPECIES: Monkey\n'
                ' > Age: 3 year(s) old.\n'
                ' > Health Status: [HEALTHY]\n'
                ' > Cleanliness: Very High\n'
                ' > Fur colour: Yellow-brown\n'
                ' > Nocturnal: False\n'
                )
        mammal.groom(datetime(2004, 11, 12, 15, 0))
        assert (str(mammal.log) ==
                '----------------------------------------------------------------------------------------------\n'
                'MOMO_A6 GENERAL ACTIVITY LOG:\n'
                '\n'
                '[2004-11-12 15:00:00] Momo_A6 grooms self (picks at its yellow-brown fur).\n'
                '----------------------------------------------------------------------------------------------\n'
                )
