"""
File: log.py
Description: Contains the Log class which is used to keep track of historical information about the actions of zoo
entities over time. Log is a subclass of DataRecord.
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

        # create a dataframe to store action history (base columns with new columns added):
        cols_to_add = DataFrame({"DateTime": pd.Series(dtype="object")})  # datetime object
        self.data = pd.concat([self.data, cols_to_add])

    def new(self, new_row: dict) -> int:
        """
        Add a new row of information to the log.

        :param new_row: New row of information to be added, represented as a dictionary.
            The dictionary must contain:
            - 'DateTime' (datetime): When the action was performed.
            - 'SubjectID' (str): ID of the performer of the action.
            - 'SubjectName' (str): Name of the performer of the action.
            - 'ObjectID' (str): ID of the receiver of the action.
            - 'ObjectName' (str): Name of the receiver of the action.
            - 'Action' (Action): The action being performed.
            - 'Details' (str): Further description of the action.
        :return: The reference number of the new row added.
        """

        if not isinstance(new_row.get("DateTime"),
                          datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime or time object.")

        if not isinstance(new_row.get("Action"), Action):
            raise TypeError("The logged action must be from the Action enumeration.")

        return super().new(new_row)

    def __str__(self) -> str:
        """
        Display the contents of the log in a readable format.
        :return: A formatted string representing the log.
        """
        output = super().__str__() + " LOG:"

        if len(self.data) == 0:
            output += "\nNo data recorded."
        else:
            self.data.sort_values(by=['DateTime'], ascending=True, inplace=True)
            # iterate through log records and add each as a formatted line:
            for row in self.data.itertuples():
                subject_desc = f"{row.SubjectName}_{row.SubjectID}"
                object_desc = f"{row.ObjectName}_{row.ObjectID}"
                # if the subject of the scheduled action only relates to the performer, do not describe
                # the ObjectName and ObjectID of the event:
                object_desc = "" if object_desc == subject_desc else object_desc + " "
                output += (f"\n[{row.DateTime}] {subject_desc} {row.Action.present_tense} "
                           f"{object_desc}({row.Details}).")
                # present_tense gets the descriptive verb associated with performing that Action (e.g. eats)
        output += f"\n----------------------------------------------------------------------------------------------\n"
        return output
