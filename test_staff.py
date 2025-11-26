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
    def cobra1(self) -> Reptile:
        cobra1 = Reptile("Shai-Hulud", "King Cobra", "Hiss", "Smooth", True,
                         4, habitat=EnvironmentalType.DESERT)
        cobra1.add_to_diet("Raw Chicken", "200g", time(10))
        cobra1.add_to_diet("Raw Lamb", "100g", time(18, 30))
        return cobra1

    @pytest.fixture
    def cobra2(self) -> Reptile:
        cobra2 = Reptile("LittleMaker", "King Cobra", "Hiss", "Smooth", True,
                         0, habitat=EnvironmentalType.DESERT)
        cobra2.add_to_diet("Raw Chicken", "50g", time(10))
        cobra2.add_to_diet("Raw Chicken", "50g", time(15))
        cobra2.add_to_diet("Raw Lamb", "25g", time(18, 30))
        return cobra2

    @pytest.fixture
    def desert_mouse(self) -> Mammal:
        desert_mouse = Mammal("Muad'Dib", "Brown Desert Mouse", "Squeak", "Brown", True,
                              habitat=EnvironmentalType.DESERT)
        desert_mouse.add_to_diet("Spinach", "2x leaves", time(20, 15))
        desert_mouse.add_to_diet("Blueberries", "3x berries", time(20, 15))
        desert_mouse.add_to_diet("Grasshopper", "2x whole", time(6))
        desert_mouse.add_to_diet("Seeds", "5g", time(6))
        return desert_mouse

    @pytest.fixture
    def desert1(self, cobra1, cobra2) -> Enclosure:
        desert1 = Enclosure("Dune", EnvironmentalType.DESERT, 10)
        desert1.add_animal(cobra1)
        desert1.add_animal(cobra2)
        return desert1

    @pytest.fixture
    def desert2(self, desert_mouse) -> Enclosure:
        desert2 = Enclosure("DesertHideout", EnvironmentalType.DESERT, 10)
        desert2.add_animal(desert_mouse)
        return desert2

    @pytest.fixture
    def zookeeper(self) -> Zookeeper:
        return Zookeeper("Daniel")

    @pytest.fixture
    def veterinarian(self) -> Veterinarian:
        return Veterinarian("Ethan")

    def test_assignment(self, zookeeper: Zookeeper, desert1: Enclosure, desert_mouse: Mammal, capsys):
        zookeeper.assign(desert1, datetime(2004, 11, 10))
        assert desert1 in zookeeper.enclosure_assignments

        zookeeper.assign(desert1, datetime(2004, 11, 10))
        assert len(zookeeper.enclosure_assignments) == 1  # nothing should change

        zookeeper.assign(desert_mouse, datetime(2004, 11, 10))
        assert desert_mouse in zookeeper.animal_assignments
        assert len(zookeeper.animal_assignments) == 1

        zookeeper.assign("book", datetime(2004, 11, 10))
        actual = capsys.readouterr().out.strip()
        expected = f"[ERROR] Staff members cannot be assigned to str objects. No change made."
        assert expected == actual
        assert len(zookeeper.enclosure_assignments) == 1  # nothing should change

        actual = str(zookeeper)
        expected = (f"\n<ZOOKEEPER> ID: {zookeeper.id} | NAME: Daniel\n"
                    f" > Assigned Animals: 1\n"
                    f"   > Muad'Dib_{desert_mouse.id}\n"
                    f" > Assigned Enclosures: 1\n"
                    f"   > Dune_{desert1.id}\n")
        assert actual == expected

        assert len(zookeeper.log.data) == 2

    def test_unassignment(self, veterinarian: Veterinarian, desert1: Enclosure, desert_mouse: Mammal):
        veterinarian.assign(desert1, datetime(2004, 11, 10))
        veterinarian.unassign(desert1)
        assert desert1 not in veterinarian.enclosure_assignments

        veterinarian.unassign(desert_mouse)
        assert len(veterinarian.enclosure_assignments) == 0 == len(veterinarian.animal_assignments)  # nothing changes
        assert len(veterinarian.log.data) == 2

    def test_generate_schedule_zookeeper(self, zookeeper: Zookeeper, desert1: Enclosure, desert2: Enclosure):
        zookeeper.assign(desert1)
        zookeeper.assign(desert2)

        k = zookeeper
        d1 = desert1
        d2 = desert2
        c1 = desert1.inhabitants[0]
        c2 = desert1.inhabitants[1]
        m = desert2.inhabitants[0]

        actual = str(zookeeper.generate_schedule())
        expected = (
            "----------------------------------------------------------------------------------------------\n"
            f"DANIEL_{k.id} DAILY TASK SCHEDULE:\n\n"
            f"EVENT 1 @ 06:00:00\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (2x whole Grasshopper)\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (5g Seeds)\n\n"
            f"EVENT 2 @ 07:00:00\n"
            f" - Daniel_{k.id} to clean Dune_{d1.id} (standard)\n"
            f" - Daniel_{k.id} to clean DesertHideout_{d2.id} (standard)\n\n"
            f"EVENT 3 @ 10:00:00\n"
            f" - Daniel_{k.id} to feed Shai-Hulud_{c1.id} (200g Raw Chicken)\n"
            f" - Daniel_{k.id} to feed LittleMaker_{c2.id} (50g Raw Chicken)\n\n"
            f"EVENT 4 @ 15:00:00\n"
            f" - Daniel_{k.id} to feed LittleMaker_{c2.id} (50g Raw Chicken)\n\n"
            f"EVENT 5 @ 18:30:00\n"
            f" - Daniel_{k.id} to feed Shai-Hulud_{c1.id} (100g Raw Lamb)\n"
            f" - Daniel_{k.id} to feed LittleMaker_{c2.id} (25g Raw Lamb)\n\n"
            f"EVENT 6 @ 20:15:00\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (2x leaves Spinach)\n"
            f" - Daniel_{k.id} to feed Muad'Dib_{m.id} (3x berries Blueberries)\n"
            f"----------------------------------------------------------------------------------------------\n")
        assert actual == expected

    def test_generate_schedule_vet(self, veterinarian: Veterinarian, desert1: Enclosure, desert2: Enclosure):
        veterinarian.assign(desert1)
        veterinarian.assign(desert2)

        vet = veterinarian
        d1 = desert1
        d2 = desert2
        c1 = desert1.inhabitants[0]
        c2 = desert1.inhabitants[1]
        m = desert2.inhabitants[0]

        # Extra special task (non-routine) added directly to vet's special_tasks
        vet.special_tasks.new({
            "Time": time(22, 20),
            "SubjectID": vet.id,
            "SubjectName": vet.name,
            "ObjectID": m.id,
            "ObjectName": m.name,
            "Action": Action.CHECK_HEALTH,
            "Details": "Behavioural Review", })

        # Diagnosis
        vet.diagnose(m, "Psychological illness - anxiety", Severity.LOW, "Get 5 min of cuddles 2x per day.",
                     [[time(11), "5 min cuddles"], [time(19), "5 min cuddles"]],
                     datetime(2004, 11, 12, 10, 30))

        actual = str(veterinarian.generate_schedule())
        expected = (
            f"----------------------------------------------------------------------------------------------\n"
            f"ETHAN_{vet.id} DAILY TASK SCHEDULE:\n"
            f"\n"
            f"EVENT 1 @ 08:00:00\n"
            f" - Ethan_{vet.id} to perform health checkup on Shai-Hulud_{c1.id} (standard)\n"
            f" - Ethan_{vet.id} to perform health checkup on LittleMaker_{c2.id} (standard)\n"
            f" - Ethan_{vet.id} to perform health checkup on Muad'Dib_{m.id} (standard)\n"
            f"\n"
            f"EVENT 2 @ 11:00:00\n"
            f" - Ethan_{vet.id} to treat Muad'Dib_{m.id} (5 min cuddles)\n"
            f"\n"
            f"EVENT 3 @ 19:00:00\n"
            f" - Ethan_{vet.id} to treat Muad'Dib_{m.id} (5 min cuddles)\n"
            f"\n"
            "EVENT 4 @ 22:20:00\n"
            f" - Ethan_{vet.id} to perform health checkup on Muad'Dib_{m.id} (Behavioural Review)\n"
            f"----------------------------------------------------------------------------------------------\n")
        assert expected == actual

    def test_zookeeper_feed_and_clean(self, zookeeper: Zookeeper, desert1: Enclosure):
        k = zookeeper
        d1 = desert1
        c1 = desert1.inhabitants[0]

        d1.become_dirtier(datetime(2004, 11, 12), 3)
        k.clean(d1, datetime(2004, 11, 12, 7))
        c1.become_dirtier(datetime(2004, 11, 12), 2)
        k.clean(c1, datetime(2004, 11, 12, 14))
        k.feed(c1, "Raw Chicken", "200g", datetime(2004, 11, 12, 10))
        k.feed(c1, "Raw Lamb", "100g", datetime(2004, 11, 12, 18, 30))

        # Enclosure log
        assert str(d1.log) == (
            f"----------------------------------------------------------------------------------------------\n"
            f"DUNE_{d1.id} MAINTENANCE LOG:\n\n"
            f"[2004-11-12 00:00:00] Dune_{d1.id} becomes dirtier (cleanliness is now 'Low').\n"
            f"[2004-11-12 07:00:00] Dune_{d1.id} is cleaned by Daniel_{k.id} (cleanliness is now 'Moderate').\n"
            f"----------------------------------------------------------------------------------------------\n")

        # Cobra log
        assert str(c1.log) == (
            f"----------------------------------------------------------------------------------------------\n"
            f"SHAI-HULUD_{c1.id} GENERAL ACTIVITY LOG:\n\n"
            f"[2004-11-12 00:00:00] Shai-Hulud_{c1.id} becomes dirtier (cleanliness is now 'Moderate').\n"
            f"[2004-11-12 10:00:00] Shai-Hulud_{c1.id} eats (200g Raw Chicken).\n"
            f"[2004-11-12 14:00:00] Shai-Hulud_{c1.id} is cleaned by Daniel_{k.id} (cleanliness is now 'High').\n"
            f"[2004-11-12 18:30:00] Shai-Hulud_{c1.id} eats (100g Raw Lamb).\n"
            f"----------------------------------------------------------------------------------------------\n")

        # Zookeeper log
        assert str(k.log) == (
            f"----------------------------------------------------------------------------------------------\n"
            f"DANIEL_{k.id} GENERAL ACTIVITY LOG:\n\n"
            f"[2004-11-12 07:00:00] Daniel_{k.id} cleans Dune_{d1.id} (standard).\n"
            f"[2004-11-12 10:00:00] Daniel_{k.id} feeds Shai-Hulud_{c1.id} (200g Raw Chicken).\n"
            f"[2004-11-12 14:00:00] Daniel_{k.id} cleans Shai-Hulud_{c1.id} (standard).\n"
            f"[2004-11-12 18:30:00] Daniel_{k.id} feeds Shai-Hulud_{c1.id} (100g Raw Lamb).\n"
            f"----------------------------------------------------------------------------------------------\n")

    def test_vet_full_medical(self, veterinarian: Veterinarian, desert1: Enclosure, desert2: Enclosure):
        vet = veterinarian
        m = desert2.inhabitants[0]

        # Health Check
        vet.check_health(m, "Behavioral assessment", Severity.LOW,
                         datetime(2004, 11, 12, 10, 20))

        # Diagnosis
        vet.diagnose(m, "Psychological illness - anxiety", Severity.LOW, "Get 5 min of cuddles 2x per day.",
                     [[time(7), "5 min cuddles"], [time(19), "5 min cuddles"]],
                     datetime(2004, 11, 12, 10, 30))

        # Two treatments
        vet.treat(m, "5 min cuddles", Severity.LOW,
                  datetime(2004, 11, 12, 11, 0))
        vet.treat(m, "5 min cuddles", Severity.LOW,
                  datetime(2004, 11, 12, 19, 0))

        # Follow-up check + recovery
        vet.check_health(m, "Behavioral review.", Severity.LOW,
                         datetime(2004, 11, 13, 22, 20), )
        vet.declare_recovery(m, "Anxiety cured.",
                             datetime(2004, 11, 13, 22, 35))

        # Medical log of the mouse
        med_str = str(m.medical_log)

        block1 = (
            f"[2004-11-12 10:20:00] Muad'Dib_{m.id} receives health check from Ethan_{vet.id};\n"
            f" > Description: Behavioral assessment\n"
            f" > Severity: Low\n"
            f" > Treatment: NA\n")
        block2 = (
            f"[2004-11-12 10:30:00] Muad'Dib_{m.id} is diagnosed by Ethan_{vet.id};\n"
            f" > Description: Psychological illness - anxiety\n"
            f" > Severity: Low\n"
            f" > Treatment: Get 5 min of cuddles 2x per day.\n")
        block3 = (
            f"[2004-11-12 11:00:00] Muad'Dib_{m.id} receives treatment from Ethan_{vet.id};\n"
            f" > Description: 5 min cuddles\n"
            f" > Severity: Low\n"
            f" > Treatment: NA\n")
        block4 = (
            f"[2004-11-12 19:00:00] Muad'Dib_{m.id} receives treatment from Ethan_{vet.id};\n"
            f" > Description: 5 min cuddles\n"
            f" > Severity: Low\n"
            f" > Treatment: NA\n")
        block5 = (
            f"[2004-11-13 22:20:00] Muad'Dib_{m.id} receives health check from Ethan_{vet.id};\n"
            f" > Description: Behavioral review.\n"
            f" > Severity: Low\n"
            f" > Treatment: NA\n")
        block6 = (
            f"[2004-11-13 22:35:00] Muad'Dib_{m.id} is declared recovered by Ethan_{vet.id};\n"
            f" > Description: Anxiety cured.\n"
            f" > Severity: Very Low\n"
            f" > Treatment: NA\n")

        for block in (block1, block2, block3, block4, block5, block6):
            assert block in med_str

        med_ref_lines = [line for line in med_str.splitlines() if line.startswith("log ref number: ")]
        assert len(med_ref_lines) == 6  # 6 medical events with log ref numbers

        # Vet's general activity log
        staff_str = str(vet.log)

        # Action lines (log ref numbers dynamic)
        assert (f"[2004-11-12 10:20:00] Ethan_{vet.id} checks health of Muad'Dib_{m.id} (log ref:" in staff_str)
        assert (f"[2004-11-12 10:30:00] Ethan_{vet.id} diagnoses Muad'Dib_{m.id} (log ref:" in staff_str)
        assert (f"[2004-11-12 11:00:00] Ethan_{vet.id} treats Muad'Dib_{m.id} (log ref:" in staff_str)
        assert (f"[2004-11-12 19:00:00] Ethan_{vet.id} treats Muad'Dib_{m.id} (log ref:" in staff_str)
        assert (f"[2004-11-13 22:20:00] Ethan_{vet.id} checks health of Muad'Dib_{m.id} (log ref:" in staff_str)
        assert (f"[2004-11-13 22:35:00] Ethan_{vet.id} declares recovery of Muad'Dib_{m.id} (log ref:" in staff_str)

        # Exactly 6 log-ref mentions in staff log:
        assert staff_str.count("log ref:") == 6
