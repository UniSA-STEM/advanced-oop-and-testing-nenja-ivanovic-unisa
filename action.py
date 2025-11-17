"""
File: action.py
Description: Contains the enumeration class for all actions that can be logged.
have a name and age.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from enum import Enum


class Action(Enum):
    EAT = ("eat", "eats")
    SLEEP = ("sleep", "sleeps")
    AGE = ("age", "ages")
    SPEAk = ("speak", "says")

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
