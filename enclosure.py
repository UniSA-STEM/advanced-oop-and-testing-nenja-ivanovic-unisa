"""
File: enclosure.py
Description: Contains the Enclosure class which represents the enclosed areas that Animals can live in within the zoo.
Enclosures have an EnvironmentalType and can only house one species of Animal.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""

from animal import Animal
from environmental_type import EnvironmentalType
from log import Log
from requires_cleaning import RequiresCleaning


class Enclosure(RequiresCleaning):
    _next_id = 1  # unique identifier of the enclosure which is incremented by one each time an enclosure is created.

    def __init__(self, name: str, environmental_type: EnvironmentalType, size: int):
        """
        Initialise new Enclosure instances.
        :param name: The name of the enclosure.
        :param environmental_type: The environmental type the animal lives in.
        :param size: the area contained by the enclosure in square meters.
        """
        self.__name = name
        self.__size = size
        self.__species = None  # The species of animal housed by the enclosure (default is None).
        self.__inhabitants = []  # list containing the animals living in the enclosure.

        try:
            if not isinstance(environmental_type, EnvironmentalType):
                raise TypeError("Enclosure environmental_type must be an EnvironmentalType enumeration.\n")
        except TypeError as e:
            environmental_type = EnvironmentalType.GRASS  # revert to default
            print(f"[WARNING] {e} Default value of EnvironmentalType.GRASS years has been assumed.\n")

        self.__environmental_type = environmental_type

        self.__id = "E" + str(Enclosure._next_id)  # E to represent 'Enclosure'
        Enclosure._next_id += 1

        # new Log to store records of enclosure cleaning and other maintenance actions.
        self.__log = Log(f"{self.__name}_{self.id} Maintenance")
        RequiresCleaning.__init__(self)

    def __str__(self) -> str:
        """Return the Enclosure's key attributes as a formatted string."""
        inhabitants_string = f"\n > Inhabitants: {len(self.inhabitants)}"
        for inhabitant in self.inhabitants:
            inhabitants_string += f"\n   > {inhabitant.name}_{inhabitant.id}"
        return (f"ID: {self.id} | NAME: {self.__name} | ENVIRONMENTAL TYPE: {self.__environmental_type.value}"
                f"\n > Species: {self.species}"
                f"\n > Size: {self.size} squared meters"
                f"\n > Cleanliness: {self.cleanliness.description}"
                + inhabitants_string + f"\n")

    def __eq__(self, other) -> bool:
        """Determine whether one Enclosure is equal to another."""
        if isinstance(other, Enclosure) & (other.id == self.__id):
            return True
        else:
            return False

    def get_name(self) -> str:
        """Return a string representing the enclosure's name."""
        return self.__name

    def get_id(self) -> str:
        """Return a string representing the enclosure's unique identifier."""
        return self.__id

    def get_size(self) -> int:
        """Return an integer representing the enclosure's area in square meters."""
        return self.__size

    def get_species(self) -> str:
        """Return a string representing the animal's species which is living in the enclosure."""
        return self.__species

    def get_environmental_type(self) -> EnvironmentalType:
        """Get the environmental type of the enclosure represented as an enumeration (EnvironmentalType)."""
        return self.__environmental_type

    def get_inhabitants(self) -> list[Animal]:
        """Return a list containing the animals that live in the enclosure."""
        return self.__inhabitants

    def get_log(self) -> Log:
        """ Returns the log of the enclosure's maintenance."""
        return self.__log

    name = property(get_name)
    size = property(get_size)
    id = property(get_id)
    species = property(get_species)
    inhabitants = property(get_inhabitants)
    environmental_type = property(get_environmental_type)
    log = property(get_log)

    def add_animal(self, animal: Animal):
        """
        House a new animal in the enclosure if the enclosure matches its habitat and species requirements and is not
        under treatment.
        :param animal: The animal to add to the enclosure.
        :return: None
        """
        try:
            if not isinstance(animal, Animal):
                raise TypeError("Only Animal objects can live in the enclosure.")
            if animal.under_treatment:
                raise ValueError(
                    f"{animal.name}_{animal.id} is under treatment so they cannot be relocated at this time.")
            if animal.habitat != self.environmental_type:
                raise ValueError(
                    f"{animal.name}_{animal.id} requires a(n) {animal.habitat.value.upper()} habitat and cannot live in "
                    f"a(n) {self.environmental_type.value.upper()} enclosure.")
            if (len(self.inhabitants) > 0) & (self.__species != animal.species):
                raise ValueError(
                    f"{animal.name}_{animal.id} cannot live in {self.__name}_{self.id} as animals of a different"
                    f" species already live there ({self.species}).")
            if animal not in self.inhabitants:  # unnecessary if animal already is in enclosure.
                self.__inhabitants.append(animal)
                self.__species = animal.species  # update species attribute in case the enclosure was previously empty.
        except (TypeError, ValueError) as e:
            print(f"[ERROR] {e} No change made.\n")

    def remove_animal(self, animal: Animal):
        """
        Remove an animal from the enclosure if it is not under treatment.
        :param animal: The animal to remove from the enclosure.
        :return: None
        """
        try:
            if not isinstance(animal, Animal):
                raise TypeError("Only Animal objects can be removed from enclosure.")
            if animal.under_treatment:
                raise ValueError(
                    f"{animal.name}_{animal.id} is under treatment so they cannot be relocated at this time.")

            if animal in self.inhabitants:
                self.inhabitants.remove(animal)
                if len(self.inhabitants) == 0:
                    self.__species = None
        except (TypeError, ValueError) as e:
            print(f"[ERROR] {e} No change made.\n")
