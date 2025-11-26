"""
File: main.py
Description: Demonstration script for the Zoo Management System.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime, time

from bird import Bird
from enclosure import Enclosure
from environmental_type import EnvironmentalType
from mammal import Mammal
from reptile import Reptile
from severity import Severity
from veterinarian import Veterinarian
from zoo_system import ZooSystem
from zookeeper import Zookeeper

# 1. Create the zoo system ---------------------------------------------------
zoo = ZooSystem("The Royal Zoo")

# 2. Create empty enclosures and add them to the zoo ---------------------------
blue_lagoon = Enclosure("BlueLagoon", EnvironmentalType.AQUATIC, 5)
dune = Enclosure("Dune", EnvironmentalType.DESERT, 10)
cactus_land = Enclosure("CactusLand", EnvironmentalType.DESERT, 10)
desert_hideout = Enclosure("DesertHideout", EnvironmentalType.DESERT, 10)
mouse_retreat = Enclosure("MouseRetreat", EnvironmentalType.DESERT, 8)

for enclosure in (blue_lagoon, dune, cactus_land, desert_hideout, mouse_retreat):
    zoo.add_enclosure(enclosure)

# 3. Create animals and add them to the zoo ----------------------------------------
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

# Example of invalid animal input -----------------------------------------
zoo.add_animal("not an animal")

# 4. Set up diets ------------------------------------------------------------
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

# 5. Assign animals to enclosures via ZooSystem ----------------------------
zoo.assign_animal_to_enclosure(cobra1, dune)
zoo.assign_animal_to_enclosure(cobra2, dune)
zoo.assign_animal_to_enclosure(rattlesnake, cactus_land)
zoo.assign_animal_to_enclosure(desert_mouse, desert_hideout)
zoo.assign_animal_to_enclosure(penguin, blue_lagoon)

# Invalid assignment: wrong habitat (mouse into aquatic enclosure) -------
zoo.assign_animal_to_enclosure(desert_mouse, blue_lagoon)

# 6. Add staff (Zookeeper + Veterinarian) and assign enclosures ---------------
keeper1 = Zookeeper("Daniel")
keeper2 = Zookeeper("Nenja")
vet1 = Veterinarian("Ethan")
vet2 = Veterinarian("Cece")

for staff_member in (keeper1, keeper2, vet1, vet2):
    zoo.add_staff_member(staff_member)

assign_date = datetime(2004, 11, 10)

for enclosure in (dune, cactus_land, desert_hideout):
    zoo.assign_staff_to_enclosure(keeper1, enclosure, assign_date)
    zoo.assign_staff_to_enclosure(vet1, enclosure, assign_date)

zoo.assign_staff_to_enclosure(keeper2, blue_lagoon, assign_date)
zoo.assign_staff_to_enclosure(vet2, blue_lagoon, assign_date)

# Invalid staff assignment: staff not in this zoo -----------------------------
temp_keeper = Zookeeper("Temp")
zoo.assign_staff_to_enclosure(temp_keeper, dune, assign_date)

# 7. Zookeeper: cleaning + feeding ----------------------------------------
dune.become_dirtier(datetime(2004, 11, 12), 3)
keeper1.clean(dune, datetime(2004, 11, 12, 7))

cobra1.become_dirtier(datetime(2004, 11, 12), 2)
keeper1.clean(cobra1, datetime(2004, 11, 12, 14))

keeper1.feed(cobra1, "Raw Chicken", "200g", datetime(2004, 11, 12, 10))
keeper1.feed(cobra1, "Raw Lamb", "100g", datetime(2004, 11, 12, 18, 30))

# 8a. Veterinarian: full health process for mouse ---------------------------
vet1.check_health(desert_mouse, "Behavioral assessment", Severity.LOW,
                  datetime(2004, 11, 12, 10, 20))

vet1.diagnose(desert_mouse, "Psychological illness - anxiety", Severity.LOW,
              "Get 5 min of cuddles 2x per day.",
              [[time(11), "5 min cuddles"], [time(19), "5 min cuddles"]],
              datetime(2004, 11, 12, 10, 30))

# Mouse is under treatment, cannot be moved ----------------------
zoo.move_animal(desert_mouse, desert_hideout, dune)

vet1.treat(desert_mouse, "5 min cuddles", Severity.LOW,
           datetime(2004, 11, 12, 11, 0))

vet1.treat(desert_mouse, "5 min cuddles", Severity.LOW,
           datetime(2004, 11, 12, 19, 0))

vet1.check_health(desert_mouse, "Behavioral review.", Severity.LOW,
                  datetime(2004, 11, 13, 22, 20))

vet1.declare_recovery(desert_mouse, "Anxiety cured.",
                      datetime(2004, 11, 13, 22, 35))

# Now that mouse is healthy, moving and removing are allowed ---------
zoo.move_animal(desert_mouse, desert_hideout, mouse_retreat)
zoo.remove_enclosure(desert_hideout)  # now empty

# 8b. Veterinarian: medical events for Penguin  -------------------------
vet2.check_health(penguin, "Wing inspection", Severity.LOW,
                  datetime(2004, 11, 14, 9, 0))

vet2.diagnose(penguin, "Minor wing strain", Severity.VERY_LOW,
              "No swims for 1 day.", [[time(10), "Apply ice pack"], [time(18), "Recheck flexibility"]],
              datetime(2004, 11, 14, 9, 15))

vet2.treat(penguin, "Apply ice pack", Severity.VERY_LOW,
           datetime(2004, 11, 14, 10, 0))

vet2.check_health(penguin, "Wing follow-up check.", Severity.VERY_LOW,
                  datetime(2004, 11, 15, 9, 0))

vet2.declare_recovery(penguin, "Wing fully recovered.", datetime(2004, 11, 15, 9, 30))

# 9. Bird: activity + ageing + cleanliness  -------------------------------------
penguin.fly(datetime(2004, 11, 12, 6, 45))
penguin.eat("fish", "3x whole", datetime(2004, 11, 12, 9, 0))
penguin.drink("water", "500mL", datetime(2004, 11, 12, 12, 10))
penguin.sleep(datetime(2004, 11, 12, 12, 40))
penguin.eat("squid", "200g", datetime(2004, 11, 12, 18, 50))
penguin.become_older(datetime(2004, 11, 13, 10, 35))
penguin.become_dirtier(datetime(2004, 11, 13, 11, 0), 7)
penguin.receive_cleaning("S2", "Chloe", datetime(2004, 11, 13, 12, 0), 2)

# 10. Remove a staff member to show staff management ------------------------
zoo.remove_staff_member(keeper2)

# 11. Reports -------------------------------------------------------------------
print(zoo)
print(zoo.report_species())
print(zoo.report_enclosure_status())
print(zoo.report_animals_on_display())
print(zoo.report_animal_medical_history(desert_mouse))
print(zoo.report_zoo_medical_history())
print(zoo.report_zoo_daily_staff_schedules())
print(zoo.report_zoo_staff_activity())
print(zoo.report_zoo_enclosure_maintenance())
