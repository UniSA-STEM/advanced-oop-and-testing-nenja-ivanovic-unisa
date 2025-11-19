"""
File: medical_log.py
Description: Contains the MedicalLog class which is used to keep track of historical information about health status of
animal objects over time. MedicalLog is a subclass of Log.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from data_record import DataRecord
from log import Log
from severity import Severity


class MedicalLog(Log):
    def __init__(self, log_name: str):
        """
        Create a new Log instance.
        :param log_name: The name of the log.
        """
        super().__init__(log_name)

        # create a dataframe to store medical history (base columns with new columns added):
        cols_to_add = DataFrame({
            "Severity": pd.Series(dtype="object"),  # Severity enumeration
            "Treatment": pd.Series(dtype="string")})
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
            - 'Severity' (Severity): The importance of the action or action outcome.
            - 'Treatment' (str): Any medical action prescribed to be taken as a result of the current action.
        :return: int
        """

        if not isinstance(new_row.get("DateTime"),
                          datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime or time object.")

        if not isinstance(new_row.get("Severity"), Severity):
            raise TypeError("The logged record severity must be from the Severity enumeration.")

        return super().new(new_row)

    def __str__(self) -> str:
        """
        Display the contents of the log in a readable format.
        :return: A formatted string representing the log.
        """
        output = DataRecord.__str__(self) + " LOG:"

        if len(self.data) == 0:
            output += "\nNo medical history recorded."
        else:
            self.data.sort_values(by=['DateTime'], ascending=True, inplace=True)
            # iterate through log records and add each as a formatted line:
            for row in self.data.itertuples():
                subject_desc = f"{row.SubjectName}_{row.SubjectID}"
                object_desc = f"{row.ObjectName}_{row.ObjectID}"
                # if the subject of the scheduled action only relates to the performer, do not describe
                # the ObjectName and ObjectID of the event:
                object_desc = "" if object_desc == subject_desc else " " + object_desc
                output += (f"\n\n[{row.DateTime}] {subject_desc} {row.Action.present_tense}{object_desc};"
                           f"\n > Description: {row.Details}"
                           f"\n > Severity: {row.Severity.description}"
                           f"\n > Treatment: {row.Treatment}"
                           f"\nlog ref number: {row.Index}")
                # present_tense gets the descriptive verb associated with performing that Action (e.g. eats)
        output += f"\n----------------------------------------------------------------------------------------------\n"
        return output
