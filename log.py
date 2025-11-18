"""
File: log.py
Description: Contains the Log class which is used to keep track of historical information about the actions of zoo
entities over time.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from action import Action
from data_record import DataRecord


class Log(DataRecord):
    def __init__(self, log_name: str):
        """
        Create a new Log instance.
        :param log_name: The name of the log.
        """
        super().__init__(log_name)

        # create a dataframe to store action history
        self.data = DataFrame({
            "DateTime": pd.Series(dtype="object"),  # datetime object
            "Id": pd.Series(dtype="int"),
            "Name": pd.Series(dtype="string"),
            "Action": pd.Series(dtype="object"),  # Action enumeration
            "Details": pd.Series(dtype="string")
        })

    def new(self, new_row: dict):
        """
        Add a new row of information to the log.

        :param new_row: New row of information to be added, represented as a dictionary.
                        The dictionary must contain:
                        - 'DateTime' (datetime): When the action was performed.
                        - 'Id' (int): ID of the object performing the action.
                        - 'Name' (str): Name of the object performing the action.
                        - 'Action' (Action): The action being performed.
                        - 'Details' (str): Further description of the action.
        :return: None
        """

        if not isinstance(new_row.get("DateTime"),
                          datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime or time object.")

        if not isinstance(new_row.get("Action"), Action):
            raise TypeError("The logged action must be from the Action enumeration.")

        super().new(new_row)

    def __str__(self) -> str:
        """
        Display the contents of the log in a readable format.
        :return: A formatted string representing the log.
        """
        output = super().__str__() + " LOG:"

        if len(self.data) == 0:
            output += "\nNo data recorded."
        else:
            # iterate through log records and add each as a formatted line:
            for row in self.data.itertuples():
                output += (f"\n[{row.DateTime}] {row.Name}_{row.Id} "
                           f"{row.Action.present_tense} {row.Details}.")
        output += f"\n----------------------------------------------------------------------------------------------\n"
        return output
