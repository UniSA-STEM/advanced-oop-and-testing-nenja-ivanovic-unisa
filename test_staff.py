"""
File: test_staff.py
Description: Suite of unit tests for the subclasses of the Staff class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime, time

import pytest

from action import Action
from enclosure import Enclosure
from environmental_type import EnvironmentalType
from mammal import Mammal
from reptile import Reptile
from severity import Severity
from veterinarian import Veterinarian
from zookeeper import Zookeeper


class TestStaff:
    @pytest.fixture
    def animals_and_enclosures_setup(self):
        """Create animal instances, add to the animals' diets. Create enclosure instances and
        add animals to enclosures"""
        desert1 = Enclosure("Dune", EnvironmentalType.DESERT, 10)
        desert2 = Enclosure("CactusLand", EnvironmentalType.DESERT, 10)
        desert3 = Enclosure("DesertHideout", EnvironmentalType.DESERT, 10)

        cobra1 = Reptile("Shai-Hulud", "King Cobra", "Hiss", "Smooth", True, 4,
                         habitat=EnvironmentalType.DESERT)
        cobra2 = Reptile("LittleMaker", "King Cobra", "Hiss", "Smooth", True, 0,
                         habitat=EnvironmentalType.DESERT)
        rattlesnake = Reptile("Sally", "Horned Rattlesnake", "Hiss", "Keeled", True, 4,
                              habitat=EnvironmentalType.DESERT)
        desert_mouse = Mammal("Muad'Dib", "Brown Desert Mouse", "Squeak", "Brown", True,
                              habitat=EnvironmentalType.DESERT)

        # diets
        cobra1.add_to_diet("Raw Chicken", "200g", time(10))
        cobra1.add_to_diet("Raw Lamb", "100g", time(18, 30))

        cobra2.add_to_diet("Raw Chicken", "50g", time(10))
        cobra2.add_to_diet("Raw Chicken", "50g", time(15))
        cobra2.add_to_diet("Raw Lamb", "25g", time(18, 30))

        rattlesnake.add_to_diet("Mouse", "2x whole", time(9))
        rattlesnake.add_to_diet("Mouse", "2x whole", time(19))

        desert_mouse.add_to_diet("Spinach", "2x leaves", time(20, 15))
        desert_mouse.add_to_diet("Blueberries", "3x berries", time(20, 15))
        desert_mouse.add_to_diet("Grasshopper", "2x whole", time(6))
        desert_mouse.add_to_diet("Seeds", "5g", time(6))

        desert1.add_animal(cobra1)
        desert1.add_animal(cobra2)
        desert2.add_animal(rattlesnake)
        desert3.add_animal(desert_mouse)

        return {
            "desert1": desert1,
            "desert2": desert2,
            "desert3": desert3,
            "cobra1": cobra1,
            "cobra2": cobra2,
            "rattlesnake": rattlesnake,
            "desert_mouse": desert_mouse,
        }

    @pytest.fixture
    def zookeeper_setup(self, animals_and_enclosures_setup):
        """Create a Zookeeper and assign enclosures to them."""
        c1 = animals_and_enclosures_setup["cobra1"]
        c2 = animals_and_enclosures_setup["cobra2"]
        r = animals_and_enclosures_setup["rattlesnake"]
        m = animals_and_enclosures_setup["desert_mouse"]
        d1 = animals_and_enclosures_setup["desert1"]
        d2 = animals_and_enclosures_setup["desert2"]
        d3 = animals_and_enclosures_setup["desert3"]

        keeper = Zookeeper("Daniel")

        keeper.assign(d1, datetime(2004, 11, 10))
        keeper.assign(d2, datetime(2004, 11, 10))
        keeper.assign(d3, datetime(2004, 11, 10))

        return {
            "keeper": keeper,
            "desert1": d1,
            "desert2": d2,
            "desert3": d3,
            "cobra1": c1,
            "cobra2": c2,
            "rattlesnake": r,
            "desert_mouse": m,
        }

    def test_zookeeper_str(self, zookeeper_setup):
        k = zookeeper_setup["keeper"]
        d1 = zookeeper_setup["desert1"]
        d2 = zookeeper_setup["desert2"]
        d3 = zookeeper_setup["desert3"]

        expected = (
            f"\n<ZOOKEEPER> ID: {k.id} | NAME: Daniel\n"
            f" > Assigned Animals: 0\n"
            f" > Assigned Enclosures: 3\n"
            f"   > Dune_{d1.id}\n"
            f"   > CactusLand_{d2.id}\n"
            f"   > DesertHideout_{d3.id}\n"
        )
        assert str(k) == expected

    def test_generate_schedule(self, zookeeper_setup):
        k = zookeeper_setup["keeper"]
        c1 = zookeeper_setup["cobra1"]
        c2 = zookeeper_setup["cobra2"]
        r = zookeeper_setup["rattlesnake"]
        m = zookeeper_setup["desert_mouse"]
        d1 = zookeeper_setup["desert1"]
        d2 = zookeeper_setup["desert2"]
        d3 = zookeeper_setup["desert3"]

        s = str(k.generate_schedule())
        expected = (
            "----------------------------------------------------------------------------------------------\n"
            f"DANIEL_{k.id} DAILY TASK SCHEDULE:\n\n"
            "EVENT 1 @ 06:00:00\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (2x whole Grasshopper)\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (5g Seeds)\n\n"
            "EVENT 2 @ 07:00:00\n"
            f" - Daniel_{k.id} to clean Dune_{d1.id} (standard)\n"
            f" - Daniel_{k.id} to clean CactusLand_{d2.id} (standard)\n"
            f" - Daniel_{k.id} to clean DesertHideout_{d3.id} (standard)\n\n"
            "EVENT 3 @ 09:00:00\n"
            f" - Daniel_{k.id} to feed Sally_{r.id} (2x whole Mouse)\n\n"
            "EVENT 4 @ 10:00:00\n"
            f" - Daniel_{k.id} to feed Shai-Hulud_{c1.id} (200g Raw Chicken)\n"
            f" - Daniel_{k.id} to feed LittleMaker_{c2.id} (50g Raw Chicken)\n\n"
            "EVENT 5 @ 15:00:00\n"
            f" - Daniel_{k.id} to feed LittleMaker_{c2.id} (50g Raw Chicken)\n\n"
            "EVENT 6 @ 18:30:00\n"
            f" - Daniel_{k.id} to feed Shai-Hulud_{c1.id} (100g Raw Lamb)\n"
            f" - Daniel_{k.id} to feed LittleMaker_{c2.id} (25g Raw Lamb)\n\n"
            "EVENT 7 @ 19:00:00\n"
            f" - Daniel_{k.id} to feed Sally_{r.id} (2x whole Mouse)\n\n"
            "EVENT 8 @ 20:15:00\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (2x leaves Spinach)\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (3x berries Blueberries)\n"
            "----------------------------------------------------------------------------------------------\n"
        )
        assert s == expected

    def test_cleaning_and_logs(self, zookeeper_setup):
        k = zookeeper_setup["keeper"]
        d1 = zookeeper_setup["desert1"]
        d2 = zookeeper_setup["desert2"]
        d3 = zookeeper_setup["desert3"]
        c1 = zookeeper_setup["cobra1"]

        d1.become_dirtier(datetime(2004, 11, 12), 3)
        k.clean(d1, datetime(2004, 11, 12, 7))
        c1.become_dirtier(datetime(2004, 11, 12), 2)
        k.clean(c1, datetime(2004, 11, 12, 14))
        k.feed(c1, "Raw Chicken", "200g", datetime(2004, 11, 12, 10))
        k.feed(c1, "Raw Lamb", "100g", datetime(2004, 11, 12, 18, 30))

        # Enclosure log
        assert str(d1.log) == (
            "----------------------------------------------------------------------------------------------\n"
            f"DUNE_{d1.id} MAINTENANCE LOG:\n\n"
            f"[2004-11-12 00:00:00] Dune_{d1.id} becomes dirtier (cleanliness is now 'Low').\n"
            f"[2004-11-12 07:00:00] Dune_{d1.id} is cleaned by Daniel_{k.id} (cleanliness is now 'Moderate').\n"
            "----------------------------------------------------------------------------------------------\n"
        )

        # Cobra log
        assert str(c1.log) == (
            "----------------------------------------------------------------------------------------------\n"
            f"SHAI-HULUD_{c1.id} GENERAL ACTIVITY LOG:\n\n"
            f"[2004-11-12 00:00:00] Shai-Hulud_{c1.id} becomes dirtier (cleanliness is now 'Moderate').\n"
            f"[2004-11-12 10:00:00] Shai-Hulud_{c1.id} eats (200g Raw Chicken).\n"
            f"[2004-11-12 14:00:00] Shai-Hulud_{c1.id} is cleaned by Daniel_{k.id} (cleanliness is now 'High').\n"
            f"[2004-11-12 18:30:00] Shai-Hulud_{c1.id} eats (100g Raw Lamb).\n"
            "----------------------------------------------------------------------------------------------\n"
        )

        # Zookeeper log
        assert str(k.log) == (
            "----------------------------------------------------------------------------------------------\n"
            f"DANIEL_{k.id} GENERAL ACTIVITY LOG:\n\n"
            f"[2004-11-10 00:00:00] Daniel_{k.id} is assigned to Dune_{d1.id} (Enclosure).\n"
            f"[2004-11-10 00:00:00] Daniel_{k.id} is assigned to CactusLand_{d2.id} (Enclosure).\n"
            f"[2004-11-10 00:00:00] Daniel_{k.id} is assigned to DesertHideout_{d3.id} (Enclosure).\n"
            f"[2004-11-12 07:00:00] Daniel_{k.id} cleans Dune_{d1.id} (standard).\n"
            f"[2004-11-12 10:00:00] Daniel_{k.id} feeds Shai-Hulud_{c1.id} (200g Raw Chicken).\n"
            f"[2004-11-12 14:00:00] Daniel_{k.id} cleans Shai-Hulud_{c1.id} (standard).\n"
            f"[2004-11-12 18:30:00] Daniel_{k.id} feeds Shai-Hulud_{c1.id} (100g Raw Lamb).\n"
            "----------------------------------------------------------------------------------------------\n"
        )

    @pytest.fixture
    def veterinarian_setup(self, animals_and_enclosures_setup):
        """Create a Veterinarian and assign enclosures to them."""
        c1 = animals_and_enclosures_setup["cobra1"]
        c2 = animals_and_enclosures_setup["cobra2"]
        r = animals_and_enclosures_setup["rattlesnake"]
        m = animals_and_enclosures_setup["desert_mouse"]
        d1 = animals_and_enclosures_setup["desert1"]
        d2 = animals_and_enclosures_setup["desert2"]
        d3 = animals_and_enclosures_setup["desert3"]

        vet = Veterinarian("Ethan")

        vet.assign(d1, datetime(2004, 11, 10))
        vet.assign(d2, datetime(2004, 11, 10))
        vet.assign(d3, datetime(2004, 11, 10))

        return {
            "vet": vet,
            "desert1": d1,
            "desert2": d2,
            "desert3": d3,
            "cobra1": c1,
            "cobra2": c2,
            "rattlesnake": r,
            "desert_mouse": m,
        }

    @pytest.fixture
    def vet_for_schedule(self, veterinarian_setup) -> dict:
        """Used to test Veterinarian.generate_schedule (up to diagnosis + special task)."""
        vet = veterinarian_setup["vet"]
        c1 = veterinarian_setup["cobra1"]
        c2 = veterinarian_setup["cobra2"]
        r = veterinarian_setup["rattlesnake"]
        desert_mouse = veterinarian_setup["desert_mouse"]
        d1 = veterinarian_setup["desert1"]
        d2 = veterinarian_setup["desert2"]
        d3 = veterinarian_setup["desert3"]

        # Health check + diagnosis for the mouse (creates treatments schedule)
        vet.check_health(
            desert_mouse,
            "Behavioral assessment",
            Severity.LOW,
            datetime(2004, 11, 12, 10, 20),
        )
        vet.diagnose(
            desert_mouse,
            "Psychological illness - anxiety",
            Severity.LOW,
            "Get 5 min of cuddles 2x per day.",
            [[time(11), "5 min cuddles"], [time(19), "5 min cuddles"]],
            datetime(2004, 11, 12, 10, 30),
        )

        # Extra special task (non-routine) added directly to vet's special_tasks
        vet.special_tasks.new({
            "Time": time(22, 20),
            "SubjectID": vet.id,
            "SubjectName": vet.name,
            "ObjectID": desert_mouse.id,
            "ObjectName": desert_mouse.name,
            "Action": Action.CHECK_HEALTH,
            "Details": "Behavioural Review",
        })

        return {
            "vet": vet,
            "desert1": d1,
            "desert2": d2,
            "desert3": d3,
            "cobra1": c1,
            "cobra2": c2,
            "rattlesnake": r,
            "desert_mouse": desert_mouse,
        }

    @pytest.fixture
    def vet_for_full_medical(self, vet_for_schedule) -> dict:
        """
        Used to test medical + staff logs, including treatments and recovery.
        Starts from vet_for_schedule and adds treatment + recovery actions.
        """
        vet = vet_for_schedule["vet"]
        c1 = vet_for_schedule["cobra1"]
        c2 = vet_for_schedule["cobra2"]
        r = vet_for_schedule["rattlesnake"]
        desert_mouse = vet_for_schedule["desert_mouse"]
        d1 = vet_for_schedule["desert1"]
        d2 = vet_for_schedule["desert2"]
        d3 = vet_for_schedule["desert3"]

        # Two treatments
        vet.treat(
            desert_mouse,
            "5 min cuddles",
            Severity.LOW,
            datetime(2004, 11, 12, 11, 0),
        )
        vet.treat(
            desert_mouse,
            "5 min cuddles",
            Severity.LOW,
            datetime(2004, 11, 12, 19, 0),
        )

        # Follow-up check + recovery
        vet.check_health(
            desert_mouse,
            "Behavioral review.",
            Severity.LOW,
            datetime(2004, 11, 13, 22, 20),
        )
        vet.declare_recovery(
            desert_mouse,
            "Anxiety cured.",
            datetime(2004, 11, 13, 22, 35),
        )

        return {
            "vet": vet,
            "desert1": d1,
            "desert2": d2,
            "desert3": d3,
            "cobra1": c1,
            "cobra2": c2,
            "rattlesnake": r,
            "desert_mouse": desert_mouse,
        }

    def test_veterinarian_generate_schedule(self, vet_for_schedule) -> None:
        vet = vet_for_schedule["vet"]
        desert_mouse = vet_for_schedule["desert_mouse"]
        cobra1 = vet_for_schedule["cobra1"]
        cobra2 = vet_for_schedule["cobra2"]
        rattlesnake = vet_for_schedule["rattlesnake"]

        schedule = vet.generate_schedule()
        s = str(schedule)

        expected = (
            "----------------------------------------------------------------------------------------------\n"
            f"ETHAN_{vet.id} DAILY TASK SCHEDULE:\n"
            "\n"
            "EVENT 1 @ 08:00:00\n"
            f" - Ethan_{vet.id} to perform health checkup on Shai-Hulud_{cobra1.id} (standard)\n"
            f" - Ethan_{vet.id} to perform health checkup on LittleMaker_{cobra2.id} (standard)\n"
            f" - Ethan_{vet.id} to perform health checkup on Sally_{rattlesnake.id} (standard)\n"
            f" - Ethan_{vet.id} to perform health checkup on Muad'Dib_{desert_mouse.id} (standard)\n"
            "\n"
            "EVENT 2 @ 11:00:00\n"
            f" - Ethan_{vet.id} to treat Muad'Dib_{desert_mouse.id} (5 min cuddles)\n"
            "\n"
            "EVENT 3 @ 19:00:00\n"
            f" - Ethan_{vet.id} to treat Muad'Dib_{desert_mouse.id} (5 min cuddles)\n"
            "\n"
            "EVENT 4 @ 22:20:00\n"
            f" - Ethan_{vet.id} to perform health checkup on Muad'Dib_{desert_mouse.id} (Behavioural Review)\n"
            "----------------------------------------------------------------------------------------------\n"
        )

        assert s == expected

    def test_veterinarian_str(self, vet_for_schedule) -> None:
        vet = vet_for_schedule["vet"]
        desert1 = vet_for_schedule["desert1"]
        desert2 = vet_for_schedule["desert2"]
        desert3 = vet_for_schedule["desert3"]

        expected = (
            f"\n<VETERINARIAN> ID: {vet.id} | NAME: Ethan\n"
            " > Assigned Animals: 0\n"
            " > Assigned Enclosures: 3\n"
            f"   > Dune_{desert1.id}\n"
            f"   > CactusLand_{desert2.id}\n"
            f"   > DesertHideout_{desert3.id}\n"
        )
        assert str(vet) == expected

    def test_veterinarian_medical_and_staff_logs(self, vet_for_full_medical) -> None:
        vet = vet_for_full_medical["vet"]
        desert1 = vet_for_full_medical["desert1"]
        desert2 = vet_for_full_medical["desert2"]
        desert3 = vet_for_full_medical["desert3"]
        desert_mouse = vet_for_full_medical["desert_mouse"]

        # Medical log of the mouse
        med_str = str(desert_mouse.medical_log)

        med_header = (
            "----------------------------------------------------------------------------------------------\n"
            f"MUAD'DIB_{desert_mouse.id} MEDICAL LOG:\n"
            "\n"
        )
        assert med_str.startswith(med_header)
        assert med_str.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        block1 = (
            f"[2004-11-12 10:20:00] Muad'Dib_{desert_mouse.id} receives health check from Ethan_{vet.id};\n"
            " > Description: Behavioral assessment\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block2 = (
            f"[2004-11-12 10:30:00] Muad'Dib_{desert_mouse.id} is diagnosed by Ethan_{vet.id};\n"
            " > Description: Psychological illness - anxiety\n"
            " > Severity: Low\n"
            " > Treatment: Get 5 min of cuddles 2x per day.\n"
        )
        block3 = (
            f"[2004-11-12 11:00:00] Muad'Dib_{desert_mouse.id} receives treatment from Ethan_{vet.id};\n"
            " > Description: 5 min cuddles\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block4 = (
            f"[2004-11-12 19:00:00] Muad'Dib_{desert_mouse.id} receives treatment from Ethan_{vet.id};\n"
            " > Description: 5 min cuddles\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block5 = (
            f"[2004-11-13 22:20:00] Muad'Dib_{desert_mouse.id} receives health check from Ethan_{vet.id};\n"
            " > Description: Behavioral review.\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block6 = (
            f"[2004-11-13 22:35:00] Muad'Dib_{desert_mouse.id} is declared recovered by Ethan_{vet.id};\n"
            " > Description: Anxiety cured.\n"
            " > Severity: Very Low\n"
            " > Treatment: NA\n"
        )

        for block in (block1, block2, block3, block4, block5, block6):
            assert block in med_str

        med_ref_lines = [line for line in med_str.splitlines() if line.startswith("log ref number: ")]
        assert len(med_ref_lines) == 6  # 6 medical events with log ref numbers

        # Vet's general activity log
        staff_str = str(vet.log)

        staff_header = (
            "----------------------------------------------------------------------------------------------\n"
            f"ETHAN_{vet.id} GENERAL ACTIVITY LOG:\n"
            "\n"
        )
        assert staff_str.startswith(staff_header)
        assert staff_str.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        # Assignment lines
        assign1 = (
            f"[2004-11-10 00:00:00] Ethan_{vet.id} is assigned to Dune_{desert1.id} (Enclosure)."
        )
        assign2 = (
            f"[2004-11-10 00:00:00] Ethan_{vet.id} is assigned to CactusLand_{desert2.id} (Enclosure)."
        )
        assign3 = (
            f"[2004-11-10 00:00:00] Ethan_{vet.id} is assigned to DesertHideout_{desert3.id} (Enclosure)."
        )
        assert assign1 in staff_str
        assert assign2 in staff_str
        assert assign3 in staff_str

        # Action lines (log ref numbers dynamic)
        assert (
                f"[2004-11-12 10:20:00] Ethan_{vet.id} checks health of Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_str
        )
        assert (
                f"[2004-11-12 10:30:00] Ethan_{vet.id} diagnoses Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_str
        )
        assert (
                f"[2004-11-12 11:00:00] Ethan_{vet.id} treats Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_str
        )
        assert (
                f"[2004-11-12 19:00:00] Ethan_{vet.id} treats Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_str
        )
        assert (
                f"[2004-11-13 22:20:00] Ethan_{vet.id} checks health of Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_str
        )
        assert (
                f"[2004-11-13 22:35:00] Ethan_{vet.id} declares recovery of Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_str
        )

        # Exactly 6 log-ref mentions in staff log:
        assert staff_str.count("log ref:") == 6
