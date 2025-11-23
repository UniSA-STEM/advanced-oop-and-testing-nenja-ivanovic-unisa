"""
File: action.py
Description: Contains the enumeration class for all actions that can be logged.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from enum import Enum


class Action(Enum):
    EAT = ("eat", "eats")
    FEED = ("feed", "feeds")
    DRINK = ("drink", "drinks")
    GIVE_WATER = ("give water to", "gives water to")
    SLEEP = ("sleep", "sleeps")
    AGE = ("age", "ages")
    SPEAK = ("speak", "says")

    FLY = ("attempt to fly", "attempts to fly")  # for birds
    GROOM = ("groom self", "grooms self")  # for mammals
    BASK = ("bask in sun", "basks in sun")  # for reptiles

    CLEAN = ("clean", "cleans")
    RECEIVE_CLEANING = ("receive cleaning", "is cleaned by")
    BECOME_DIRTIER = ("become dirtier", "becomes dirtier")

    TREAT = ("treat", "treats")
    RECEIVE_TREATMENT = ("receive treatment", "receives treatment from")
    CHECK_HEALTH = ("perform health checkup on", "checks health of")
    RECEIVE_HEALTH_CHECK = ("receive health check", "receives health check from")
    DIAGNOSE = ("diagnose", "diagnoses")
    RECEIVE_DIAGNOSIS = ("receive diagnosis", "is diagnosed by")
    RECOVER = ("recover", "is declared recovered by")
    DECLARE_RECOVERY = ("declare recovery of", "declares recovery of")

    ASSIGN = ("be assigned to", "is assigned to")
    UNASSIGN = ("be unassigned from", "is unassigned from")

    def __init__(self, imperative: str, present_tense: str):
        self.__imperative = imperative
        self.__present_tense = present_tense

    def get_imperative(self) -> str:
        """Returns a string that is used when referring to the action as an imperative. E.g. '[Eat] lunch at 1pm.'"""
        return self.__imperative

    def get_present_tense(self) -> str:
        """Returns a string that is used when referring to the action being performed in the present.
        E.g. 'Bill [eats] lunch at 1pm.'"""
        return self.__present_tense

    imperative = property(get_imperative)
    present_tense = property(get_present_tense)
