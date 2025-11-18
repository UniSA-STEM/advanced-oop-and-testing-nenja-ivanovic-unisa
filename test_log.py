"""
File: test_log.py
Description: Suite of unit tests for the Log class.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

import pytest

from action import Action
from log import Log


class TestLog:
    @pytest.fixture
    def log1(self) -> Log:
        return Log("Jane's Activity")

    def test_new(self, log1):
        assert len(log1.data) == 0
        assert (log1.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nJANE'S ACTIVITY LOG:"
                "\nNo data recorded."
                "\n----------------------------------------------------------------------------------------------\n")

        log1.new({"DateTime": datetime(2004, 11, 12, 13, 50),
                  "SubjectID": 1,
                  "SubjectName": "Jane",
                  "Action": Action.EAT,
                  "Details": "(1x apple)"})

        assert (log1.__str__() ==
                "----------------------------------------------------------------------------------------------"
                "\nJANE'S ACTIVITY LOG:"
                "\n[2004-11-12 13:50:00] Jane_1 eats (1x apple)."
                "\n----------------------------------------------------------------------------------------------\n")
        assert len(log1.data) == 1
