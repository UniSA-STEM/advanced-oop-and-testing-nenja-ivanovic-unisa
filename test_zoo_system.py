"""
File: test_zoo_system.py
Description: Suite of tests for the ZooSystem class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime, time

import pytest

from bird import Bird
from enclosure import Enclosure
from environmental_type import EnvironmentalType
from mammal import Mammal
from reptile import Reptile
from severity import Severity
from veterinarian import Veterinarian
from zoo_system import ZooSystem
from zookeeper import Zookeeper


class TestZooSystem:

    @pytest.fixture
    def zoo1(self) -> dict:
        zoo = ZooSystem("The Royal Zoo")

        # Enclosures
        blue_lagoon = Enclosure("BlueLagoon", EnvironmentalType.AQUATIC, 5)
        dune = Enclosure("Dune", EnvironmentalType.DESERT, 10)
        cactus_land = Enclosure("CactusLand", EnvironmentalType.DESERT, 10)
        desert_hideout = Enclosure("DesertHideout", EnvironmentalType.DESERT, 10)

        for enclosure in (blue_lagoon, dune, cactus_land, desert_hideout):
            zoo.add_enclosure(enclosure)

        # Animals
        cobra1 = Reptile("Shai-Hulud", "King Cobra", "Hiss", "Smooth", True, 4,
                         habitat=EnvironmentalType.DESERT)
        cobra2 = Reptile("LittleMaker", "King Cobra", "Hiss", "Smooth", True, 0,
                         habitat=EnvironmentalType.DESERT)
        rattlesnake = Reptile("Sally", "Horned Rattlesnake", "Hiss", "Keeled",
                              True, 4, habitat=EnvironmentalType.DESERT)
        desert_mouse = Mammal("Muad'Dib", "Brown Desert Mouse", "Squeak", "Brown",
                              True, habitat=EnvironmentalType.DESERT)
        penguin = Bird("Pinky", "Emperor Penguin", 76, False, 2,
                       habitat=EnvironmentalType.AQUATIC)

        for animal in (cobra1, cobra2, rattlesnake, desert_mouse, penguin):
            zoo.add_animal(animal)

        # Diets
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

        penguin.add_to_diet("fish", "3x whole", time(9))
        penguin.add_to_diet("squid", "200g", time(19))

        # Assign animals to enclosures via ZooSystem
        zoo.assign_animal_to_enclosure(cobra1, dune)
        zoo.assign_animal_to_enclosure(cobra2, dune)
        zoo.assign_animal_to_enclosure(rattlesnake, cactus_land)
        zoo.assign_animal_to_enclosure(desert_mouse, desert_hideout)
        zoo.assign_animal_to_enclosure(penguin, blue_lagoon)

        # Staff
        keeper1 = Zookeeper("Daniel")
        keeper2 = Zookeeper("Nenja")
        vet1 = Veterinarian("Ethan")
        vet2 = Veterinarian("Cece")

        for staff in (keeper1, keeper2, vet1, vet2):
            zoo.add_staff_member(staff)

        assign_date = datetime(2004, 11, 10)
        for enclosure in (dune, cactus_land, desert_hideout):
            zoo.assign_staff_to_enclosure(keeper1, enclosure, assign_date)
            zoo.assign_staff_to_enclosure(vet1, enclosure, assign_date)

        zoo.assign_staff_to_enclosure(keeper2, blue_lagoon, assign_date)
        zoo.assign_staff_to_enclosure(vet2, blue_lagoon, assign_date)

        # Zookeeper actions (cleaning + feeding)
        dune.become_dirtier(datetime(2004, 11, 12), 3)
        keeper1.clean(dune, datetime(2004, 11, 12, 7))

        cobra1.become_dirtier(datetime(2004, 11, 12), 2)
        keeper1.clean(cobra1, datetime(2004, 11, 12, 14))

        keeper1.feed(cobra1, "Raw Chicken", "200g", datetime(2004, 11, 12, 10))
        keeper1.feed(cobra1, "Raw Lamb", "100g", datetime(2004, 11, 12, 18, 30))

        # Veterinarian: full health process for desert_mouse
        vet1.check_health(
            desert_mouse,
            "Behavioral assessment",
            Severity.LOW,
            datetime(2004, 11, 12, 10, 20),
        )
        vet1.diagnose(
            desert_mouse,
            "Psychological illness - anxiety",
            Severity.LOW,
            "Get 5 min of cuddles 2x per day.",
            [[time(11), "5 min cuddles"], [time(19), "5 min cuddles"]],
            datetime(2004, 11, 12, 10, 30),
        )
        vet1.treat(
            desert_mouse,
            "5 min cuddles",
            Severity.LOW,
            datetime(2004, 11, 12, 11, 0),
        )
        vet1.treat(
            desert_mouse,
            "5 min cuddles",
            Severity.LOW,
            datetime(2004, 11, 12, 19, 0),
        )
        vet1.check_health(
            desert_mouse,
            "Behavioral review.",
            Severity.LOW,
            datetime(2004, 11, 13, 22, 20),
        )
        vet1.declare_recovery(
            desert_mouse,
            "Anxiety cured.",
            datetime(2004, 11, 13, 22, 35),
        )

        # Penguin activity + ageing + cleanliness
        penguin.fly(datetime(2004, 11, 12, 6, 45))
        penguin.eat("fish", "3x whole", datetime(2004, 11, 12, 9, 0))
        penguin.drink("water", "500mL", datetime(2004, 11, 12, 12, 10))
        penguin.sleep(datetime(2004, 11, 12, 12, 40))
        penguin.eat("squid", "200g", datetime(2004, 11, 12, 18, 50))
        penguin.become_older(datetime(2004, 11, 13, 10, 35))
        penguin.become_dirtier(datetime(2004, 11, 13, 11, 0), 7)
        penguin.receive_cleaning("S2", "Chloe", datetime(2004, 11, 13, 12, 0), 2)

        # Additional: Veterinarian (vet2) medical events for penguin
        vet2.check_health(
            penguin,
            "Leg injury assessment",
            Severity.LOW,
            datetime(2004, 11, 14, 9, 45),
        )
        vet2.diagnose(
            penguin,
            "Mild leg sprain",
            Severity.LOW,
            "Rest and limit walking for 3 days.",
            [[time(10), "Check bandage"], [time(18), "Apply ice pack"]],
            datetime(2004, 11, 14, 10, 0),
        )

        return {
            "zoo": zoo,
            "blue_lagoon": blue_lagoon,
            "dune": dune,
            "cactus_land": cactus_land,
            "desert_hideout": desert_hideout,
            "cobra1": cobra1,
            "cobra2": cobra2,
            "rattlesnake": rattlesnake,
            "desert_mouse": desert_mouse,
            "penguin": penguin,
            "keeper1": keeper1,
            "keeper2": keeper2,
            "vet1": vet1,
            "vet2": vet2,
        }

    def test_zoo_overview_str(self, zoo1) -> None:
        zoo = zoo1["zoo"]
        cobra1 = zoo1["cobra1"]
        cobra2 = zoo1["cobra2"]
        rattlesnake = zoo1["rattlesnake"]
        desert_mouse = zoo1["desert_mouse"]
        penguin = zoo1["penguin"]
        blue_lagoon = zoo1["blue_lagoon"]
        dune = zoo1["dune"]
        cactus_land = zoo1["cactus_land"]
        desert_hideout = zoo1["desert_hideout"]
        keeper1 = zoo1["keeper1"]
        keeper2 = zoo1["keeper2"]
        vet1 = zoo1["vet1"]
        vet2 = zoo1["vet2"]

        s = str(zoo)

        # Header and footer
        assert s.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "~~~~~ THE ROYAL ZOO ~~~~~ "
        )
        assert s.endswith(
            "\n----------------------------------------------------------------------------------------------\n"
        )

        # Animals block
        animals_block = (
            "\n\nANIMALS (5) -----------------------------------------\n"
            "\n"
            f"ID: {cobra1.id} | NAME: Shai-Hulud | SPECIES: King Cobra\n"
            " > Age: 4 year(s) old.\n"
            " > Health Status: [HEALTHY]\n"
            " > Cleanliness: High\n"
            " > Scale type: Smooth\n"
            " > Venomous: True\n"
            "\n"
            f"ID: {cobra2.id} | NAME: LittleMaker | SPECIES: King Cobra\n"
            " > Age: 0 year(s) old.\n"
            " > Health Status: [HEALTHY]\n"
            " > Cleanliness: Very High\n"
            " > Scale type: Smooth\n"
            " > Venomous: True\n"
            "\n"
            f"ID: {rattlesnake.id} | NAME: Sally | SPECIES: Horned Rattlesnake\n"
            " > Age: 4 year(s) old.\n"
            " > Health Status: [HEALTHY]\n"
            " > Cleanliness: Very High\n"
            " > Scale type: Keeled\n"
            " > Venomous: True\n"
            "\n"
            f"ID: {desert_mouse.id} | NAME: Muad'Dib | SPECIES: Brown Desert Mouse\n"
            " > Age: 0 year(s) old.\n"
            " > Health Status: [HEALTHY]\n"
            " > Cleanliness: Very High\n"
            " > Fur colour: Brown\n"
            " > Nocturnal: True\n"
            "\n"
            f"ID: {penguin.id} | NAME: Pinky | SPECIES: Emperor Penguin\n"
            " > Age: 3 year(s) old.\n"
            " > Health Status: [UNDER TREATMENT]\n"
            " > Cleanliness: Moderate\n"
            " > Wingspan: 76cm\n"
            " > Can fly: False\n"
        )
        assert animals_block in s

        # Enclosures block
        enclosures_block = (
            "\n\nENCLOSURES (4) -----------------------------------------\n"
            "\n"
            f"ID: {blue_lagoon.id} | NAME: BlueLagoon | ENVIRONMENTAL TYPE: Aquatic\n"
            " > Species: Emperor Penguin\n"
            " > Size: 5 squared centimeters\n"
            " > Cleanliness: Very High\n"
            f" > Inhabitants: 1\n"
            f"   > Pinky_{penguin.id}\n"
            "\n"
            f"ID: {dune.id} | NAME: Dune | ENVIRONMENTAL TYPE: Desert\n"
            " > Species: King Cobra\n"
            " > Size: 10 squared centimeters\n"
            " > Cleanliness: Moderate\n"
            f" > Inhabitants: 2\n"
            f"   > Shai-Hulud_{cobra1.id}\n"
            f"   > LittleMaker_{cobra2.id}\n"
            "\n"
            f"ID: {cactus_land.id} | NAME: CactusLand | ENVIRONMENTAL TYPE: Desert\n"
            " > Species: Horned Rattlesnake\n"
            " > Size: 10 squared centimeters\n"
            " > Cleanliness: Very High\n"
            f" > Inhabitants: 1\n"
            f"   > Sally_{rattlesnake.id}\n"
            "\n"
            f"ID: {desert_hideout.id} | NAME: DesertHideout | ENVIRONMENTAL TYPE: Desert\n"
            " > Species: Brown Desert Mouse\n"
            " > Size: 10 squared centimeters\n"
            " > Cleanliness: Very High\n"
            f" > Inhabitants: 1\n"
            f"   > Muad'Dib_{desert_mouse.id}\n"
        )
        assert enclosures_block in s

        # Staff block
        staff_block = (
            "\n\nSTAFF (4) -----------------------------------------\n"
            f"\n<ZOOKEEPER> ID: {keeper1.id} | NAME: Daniel\n"
            " > Assigned Animals: 0\n"
            " > Assigned Enclosures: 3\n"
            f"   > Dune_{dune.id}\n"
            f"   > CactusLand_{cactus_land.id}\n"
            f"   > DesertHideout_{desert_hideout.id}\n"
            f"\n<ZOOKEEPER> ID: {keeper2.id} | NAME: Nenja\n"
            " > Assigned Animals: 0\n"
            " > Assigned Enclosures: 1\n"
            f"   > BlueLagoon_{blue_lagoon.id}\n"
            f"\n<VETERINARIAN> ID: {vet1.id} | NAME: Ethan\n"
            " > Assigned Animals: 0\n"
            " > Assigned Enclosures: 3\n"
            f"   > Dune_{dune.id}\n"
            f"   > CactusLand_{cactus_land.id}\n"
            f"   > DesertHideout_{desert_hideout.id}\n"
            f"\n<VETERINARIAN> ID: {vet2.id} | NAME: Cece\n"
            " > Assigned Animals: 0\n"
            " > Assigned Enclosures: 1\n"
            f"   > BlueLagoon_{blue_lagoon.id}\n"
        )
        assert staff_block in s

    def test_report_species_and_display(self, zoo1) -> None:
        zoo = zoo1["zoo"]
        cobra1 = zoo1["cobra1"]
        cobra2 = zoo1["cobra2"]
        rattlesnake = zoo1["rattlesnake"]
        desert_mouse = zoo1["desert_mouse"]
        penguin = zoo1["penguin"]

        species_report = zoo.report_species()

        # Header + footer
        assert species_report.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "ANIMALS BY SPECIES (5 total):\n"
        )
        assert species_report.endswith(
            "\n----------------------------------------------------------------------------------------------\n"
        )

        # Each species block
        king_cobra_block = (
            "\nKing Cobra (2):"
            f"\n - Shai-Hulud_{cobra1.id}"
            f"\n - LittleMaker_{cobra2.id}\n"
        )
        assert king_cobra_block in species_report

        rattler_block = (
            "\nHorned Rattlesnake (1):"
            f"\n - Sally_{rattlesnake.id}\n"
        )
        assert rattler_block in species_report

        penguin_block = (
            "\nEmperor Penguin (1):"
            f"\n - Pinky_{penguin.id}\n"
        )
        assert penguin_block in species_report

        mouse_block = (
            "\nBrown Desert Mouse (1):"
            f"\n - Muad'Dib_{desert_mouse.id}\n"
        )
        assert mouse_block in species_report

        # Animals on display
        display_report = zoo.report_animals_on_display()
        assert display_report.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "ANIMALS CURRENTLY ON DISPLAY (4): \n"  # penguin is under treatment
        )
        assert display_report.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        # Order is insertion order of animals
        for name, obj in [
            ("Shai-Hulud", cobra1),
            ("LittleMaker", cobra2),
            ("Sally", rattlesnake),
            ("Muad'Dib", desert_mouse)
        ]:
            assert f" - {name}_{obj.id} (" in display_report

        assert f" - Pinky_{penguin.id} (" not in display_report  # penguin is under treatment

    def test_medical_history_and_zoo_medical(self, zoo1) -> None:
        zoo = zoo1["zoo"]
        desert_mouse = zoo1["desert_mouse"]
        penguin = zoo1["penguin"]
        vet1 = zoo1["vet1"]
        vet2 = zoo1["vet2"]

        # Individual medical history for Mouse
        hist = zoo.report_animal_medical_history(desert_mouse)

        header = (
            "----------------------------------------------------------------------------------------------\n"
            f"MUAD'DIB_{desert_mouse.id} MEDICAL LOG:\n"
            "\n"
        )
        assert hist.startswith(header)
        assert hist.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        block1 = (
            f"[2004-11-12 10:20:00] Muad'Dib_{desert_mouse.id} receives health check from Ethan_{vet1.id};\n"
            " > Description: Behavioral assessment\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block2 = (
            f"[2004-11-12 10:30:00] Muad'Dib_{desert_mouse.id} is diagnosed by Ethan_{vet1.id};\n"
            " > Description: Psychological illness - anxiety\n"
            " > Severity: Low\n"
            " > Treatment: Get 5 min of cuddles 2x per day.\n"
        )
        block3 = (
            f"[2004-11-12 11:00:00] Muad'Dib_{desert_mouse.id} receives treatment from Ethan_{vet1.id};\n"
            " > Description: 5 min cuddles\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block4 = (
            f"[2004-11-12 19:00:00] Muad'Dib_{desert_mouse.id} receives treatment from Ethan_{vet1.id};\n"
            " > Description: 5 min cuddles\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block5 = (
            f"[2004-11-13 22:20:00] Muad'Dib_{desert_mouse.id} receives health check from Ethan_{vet1.id};\n"
            " > Description: Behavioral review.\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        block6 = (
            f"[2004-11-13 22:35:00] Muad'Dib_{desert_mouse.id} is declared recovered by Ethan_{vet1.id};\n"
            " > Description: Anxiety cured.\n"
            " > Severity: Very Low\n"
            " > Treatment: NA\n"
        )

        for block in (block1, block2, block3, block4, block5, block6):
            assert block in hist

        #  log-ref numbers check count = 6 for Mouse
        hist_log_ref_lines = [
            line for line in hist.splitlines()
            if line.startswith("log ref number: ")
        ]
        assert len(hist_log_ref_lines) == 6

        # Combined zoo medical history
        combined = zoo.report_zoo_medical_history()
        assert combined.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "COMBINED ANIMAL MEDICAL LOG:\n"
            "\n"
        )
        assert combined.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        # All mouse blocks present
        for block in (block1, block2, block3, block4, block5, block6):
            assert block in combined

        # penguin medical blocks
        p_block1 = (
            f"[2004-11-14 09:45:00] Pinky_{penguin.id} receives health check from Cece_{vet2.id};\n"
            " > Description: Leg injury assessment\n"
            " > Severity: Low\n"
            " > Treatment: NA\n"
        )
        p_block2 = (
            f"[2004-11-14 10:00:00] Pinky_{penguin.id} is diagnosed by Cece_{vet2.id};\n"
            " > Description: Mild leg sprain\n"
            " > Severity: Low\n"
            " > Treatment: Rest and limit walking for 3 days.\n"
        )

        assert p_block1 in combined
        assert p_block2 in combined

        log_ref_lines_combined = [
            line for line in combined.splitlines()
            if line.startswith("log ref number: ")
        ]
        assert len(log_ref_lines_combined) == 8

    def test_combined_staff_and_maintenance_reports(self, zoo1) -> None:
        zoo = zoo1["zoo"]
        dune = zoo1["dune"]
        desert_mouse = zoo1["desert_mouse"]
        cobra1 = zoo1["cobra1"]
        rattlesnake = zoo1["rattlesnake"]
        penguin = zoo1["penguin"]
        keeper1 = zoo1["keeper1"]
        keeper2 = zoo1["keeper2"]
        vet1 = zoo1["vet1"]
        vet2 = zoo1["vet2"]
        blue_lagoon = zoo1["blue_lagoon"]
        cactus_land = zoo1["cactus_land"]
        desert_hideout = zoo1["desert_hideout"]

        # Combined staff daily schedule
        schedule_str = zoo.report_zoo_daily_staff_schedules()
        assert schedule_str.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "COMBINED STAFF DAILY SCHEDULE:\n"
            "\n"
        )
        assert schedule_str.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        # Key schedule lines
        assert (
                f" - Daniel_{keeper1.id} to clean Dune_{dune.id} (standard)"
                in schedule_str
        )
        assert (
                f" - Daniel_{keeper1.id} to feed Sally_{rattlesnake.id} (2x whole Mouse)"
                in schedule_str
        )
        assert (
                f" - Daniel_{keeper1.id} to feed Shai-Hulud_{cobra1.id} (200g Raw Chicken)"
                in schedule_str
        )
        assert (
                f" - Nenja_{keeper2.id} to feed Pinky_{penguin.id} (3x whole fish)"
                in schedule_str
        )
        assert (
                f" - Cece_{vet2.id} to treat Pinky_{penguin.id} (Apply ice pack)"
                in schedule_str
        )
        assert (
                f" - Cece_{vet2.id} to perform health checkup on Pinky_{penguin.id} (standard)"
                in schedule_str
        )

        # Combined staff general activity log
        staff_log = zoo.report_zoo_staff_activity()
        assert staff_log.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "COMBINED STAFF GENERAL ACTIVITY LOG:\n"
            "\n"
        )
        assert staff_log.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        # Assignment lines
        assert (
                f"[2004-11-10 00:00:00] Daniel_{keeper1.id} is assigned to Dune_{dune.id} (Enclosure)."
                in staff_log
        )
        assert (
                f"[2004-11-10 00:00:00] Daniel_{keeper1.id} is assigned to CactusLand_{cactus_land.id} (Enclosure)."
                in staff_log
        )
        assert (
                f"[2004-11-10 00:00:00] Daniel_{keeper1.id} is assigned to DesertHideout_{desert_hideout.id} (Enclosure)."
                in staff_log
        )
        assert (
                f"[2004-11-10 00:00:00] Nenja_{keeper2.id} is assigned to BlueLagoon_{blue_lagoon.id} (Enclosure)."
                in staff_log
        )
        assert (
                f"[2004-11-10 00:00:00] Ethan_{vet1.id} is assigned to Dune_{dune.id} (Enclosure)."
                in staff_log
        )
        assert (
                f"[2004-11-10 00:00:00] Ethan_{vet1.id} is assigned to CactusLand_{cactus_land.id} (Enclosure)."
                in staff_log
        )
        assert (
                f"[2004-11-10 00:00:00] Ethan_{vet1.id} is assigned to DesertHideout_{desert_hideout.id} (Enclosure)."
                in staff_log
        )
        assert (
                f"[2004-11-10 00:00:00] Cece_{vet2.id} is assigned to BlueLagoon_{blue_lagoon.id} (Enclosure)."
                in staff_log
        )

        # Vet1 actions for Mouse
        assert (
                f"[2004-11-12 10:20:00] Ethan_{vet1.id} checks health of Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_log
        )
        assert (
                f"[2004-11-12 10:30:00] Ethan_{vet1.id} diagnoses Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_log
        )
        assert (
                f"[2004-11-12 11:00:00] Ethan_{vet1.id} treats Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_log
        )
        assert (
                f"[2004-11-12 19:00:00] Ethan_{vet1.id} treats Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_log
        )
        assert (
                f"[2004-11-13 22:20:00] Ethan_{vet1.id} checks health of Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_log
        )
        assert (
                f"[2004-11-13 22:35:00] Ethan_{vet1.id} declares recovery of Muad'Dib_{desert_mouse.id} (log ref:"
                in staff_log
        )

        # Vet2 actions for penguin
        assert (
                f"[2004-11-14 09:45:00] Cece_{vet2.id} checks health of Pinky_{penguin.id} (log ref:"
                in staff_log
        )
        assert (
                f"[2004-11-14 10:00:00] Cece_{vet2.id} diagnoses Pinky_{penguin.id} (log ref:"
                in staff_log
        )

        # 8 "log ref:"  in staff log (6 for Mouse + 2 for Penguin)
        assert staff_log.count("log ref:") == 8

        # Combined enclosure maintenance log
        enclosure_log = zoo.report_zoo_enclosure_maintenance()
        assert enclosure_log.startswith(
            "----------------------------------------------------------------------------------------------\n"
            "COMBINED ENCLOSURE MAINTENANCE LOG:\n"
            "\n"
        )
        assert enclosure_log.endswith(
            "----------------------------------------------------------------------------------------------\n"
        )

        assert (
                f"[2004-11-12 00:00:00] Dune_{dune.id} becomes dirtier (cleanliness is now 'Low')."
                in enclosure_log
        )
        assert (
                f"[2004-11-12 07:00:00] Dune_{dune.id} is cleaned by Daniel_{keeper1.id} (cleanliness is now 'Moderate')."
                in enclosure_log
        )

    def test_add_invalid_animal_raises_type_error(self):
        zoo = ZooSystem("Test Zoo")
        with pytest.raises(TypeError, match="Only Animal instances can be added to the zoo."):
            zoo.add_animal("not-an-animal")

    def test_add_invalid_enclosure_raises_type_error(self):
        zoo = ZooSystem("Test Zoo")
        with pytest.raises(TypeError, match="Only Enclosure instances can be added to the zoo."):
            zoo.add_enclosure("not-an-enclosure")

    def test_add_invalid_staff_member_raises_type_error(self):
        zoo = ZooSystem("Test Zoo")
        with pytest.raises(TypeError, match="Only Staff instances can be added to the zoo."):
            zoo.add_staff_member("not-a-staff")

    def test_assign_animal_not_in_zoo_raises_value_error(self, zoo1):
        zoo = zoo1["zoo"]
        dune = zoo1["dune"]
        # Reptile that is not part of this zoo
        stray_snake = Reptile("Stray", "Random Snake", "Hiss", "Smooth", True, 1,
                              habitat=EnvironmentalType.DESERT)
        with pytest.raises(
                ValueError,
                match="Animal must belong to The Royal Zoo before it can be assigned to an enclosure.",
        ):
            zoo.assign_animal_to_enclosure(stray_snake, dune)

    def test_assign_staff_not_in_zoo_raises_value_error(self, zoo1):
        zoo = zoo1["zoo"]
        dune = zoo1["dune"]
        stranger = Zookeeper("Stranger")
        with pytest.raises(
                ValueError,
                match="Staff member must belong to this zoo before assignment.",
        ):
            zoo.assign_staff_to_enclosure(stranger, dune, datetime(2004, 1, 1))

    def test_assign_enclosure_not_in_zoo_raises_value_error(self, zoo1):
        zoo = zoo1["zoo"]
        keeper1 = zoo1["keeper1"]
        new_enclosure = Enclosure("Outside", EnvironmentalType.DESERT, 5)
        with pytest.raises(
                ValueError,
                match="Enclosure must belong to this zoo before assignment.",
        ):
            zoo.assign_staff_to_enclosure(keeper1, new_enclosure, datetime(2004, 1, 1))

    def test_report_animal_medical_history_invalid_animal_raises_value_error(self, zoo1):
        zoo = zoo1["zoo"]
        # New animal not added to zoo
        outsider_mouse = Mammal("Outsider", "Brown Desert Mouse", "Squeak", "Brown",
                                True, habitat=EnvironmentalType.DESERT)
        with pytest.raises(
                ValueError,
                match="Animal must belong to this zoo.",
        ):
            zoo.report_animal_medical_history(outsider_mouse)
