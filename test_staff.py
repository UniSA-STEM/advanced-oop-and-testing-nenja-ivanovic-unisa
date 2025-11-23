from datetime import datetime, time

import pytest

from enclosure import Enclosure
from environmental_type import EnvironmentalType
from mammal import Mammal
from reptile import Reptile
from zookeeper import Zookeeper


class TestStaff:
    @pytest.fixture
    def staff_setup(self):
        keeper = Zookeeper("Daniel")

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

        keeper.assign(desert1, datetime(2004, 11, 10))
        keeper.assign(desert2, datetime(2004, 11, 10))
        keeper.assign(desert3, datetime(2004, 11, 10))

        return {
            "keeper": keeper,
            "desert1": desert1,
            "desert2": desert2,
            "desert3": desert3,
            "cobra1": cobra1,
            "cobra2": cobra2,
            "rattlesnake": rattlesnake,
            "desert_mouse": desert_mouse,
        }

    def test_zookeeper_str(self, staff_setup):
        k = staff_setup["keeper"]
        d1 = staff_setup["desert1"]
        d2 = staff_setup["desert2"]
        d3 = staff_setup["desert3"]

        expected = (
            f"\n<ZOOKEEPER> ID: {k.id} | NAME: Daniel\n"
            f" > Assigned Animals: 0\n"
            f" > Assigned Enclosures: 3\n"
            f"   > Dune_{d1.id}\n"
            f"   > CactusLand_{d2.id}\n"
            f"   > DesertHideout_{d3.id}\n"
        )
        assert str(k) == expected

    def test_generate_schedule(self, staff_setup):
        k = staff_setup["keeper"]
        c1 = staff_setup["cobra1"]
        c2 = staff_setup["cobra2"]
        r = staff_setup["rattlesnake"]
        m = staff_setup["desert_mouse"]
        d1 = staff_setup["desert1"]
        d2 = staff_setup["desert2"]
        d3 = staff_setup["desert3"]

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

    def test_cleaning_and_logs(self, staff_setup):
        k = staff_setup["keeper"]
        d1 = staff_setup["desert1"]
        c1 = staff_setup["cobra1"]
        c2 = staff_setup["cobra2"]

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
            f"[2004-11-10 00:00:00] Daniel_{k.id} is assigned to CactusLand_{staff_setup['desert2'].id} (Enclosure).\n"
            f"[2004-11-10 00:00:00] Daniel_{k.id} is assigned to DesertHideout_{staff_setup['desert3'].id} (Enclosure).\n"
            f"[2004-11-12 07:00:00] Daniel_{k.id} cleans Dune_{d1.id} (standard).\n"
            f"[2004-11-12 10:00:00] Daniel_{k.id} feeds Shai-Hulud_{c1.id} (200g Raw Chicken).\n"
            f"[2004-11-12 14:00:00] Daniel_{k.id} cleans Shai-Hulud_{c1.id} (standard).\n"
            f"[2004-11-12 18:30:00] Daniel_{k.id} feeds Shai-Hulud_{c1.id} (100g Raw Lamb).\n"
            "----------------------------------------------------------------------------------------------\n"
        )
