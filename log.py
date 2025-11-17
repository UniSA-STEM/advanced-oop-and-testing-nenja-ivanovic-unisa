"""
File: log.py
Description: Contains the Log class which is used to keep track of information about other zoo classes over time.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import datetime

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from action import Action


class Log:
    def __init__(self, log_name):
        """ Create a new Log instance. """
        self.__name = log_name
        # create a dataframe to store activities
        self.__log = pd.DataFrame({
            "Time": pd.Series(dtype="object"),  # datetime object
            "Id": pd.Series(dtype="int"),
            "Name": pd.Series(dtype="string"),
            "Action": pd.Series(dtype="object"),  # Action enumeration
            "Details": pd.Series(dtype="string")
        })

    def get_log(self) -> DataFrame:
        """ Returns the log dataframe."""
        return self.__log

    log = property(get_log)

    def new(self, actor_id: int, actor_name: str, action: Action, details: str, at_datetime: datetime = datetime.now()):
        """
        Add information about an action that was performed by an object to the log as a new row.
        :param actor_id: The id of the object performing the action.
        :param actor_name: The name of the object performing the action.
        :param action: The action being performed (from the Action enum).
        :param details: A further description of details relating to the action.
        :param at_datetime: The date and time at which the action was performed (default is when the method is called).
        :return: None
        """

        if not isinstance(at_datetime, datetime):  # the datetime class will internally handle formatting issues.
            raise TypeError("at_datetime must be a datetime object.")

        if not isinstance(action, Action):
            raise TypeError("The logged action must be from the Action enumeration.")

        # add new row to log:
        self.__log[len(self.__log)] = [at_datetime, actor_id, actor_name, action, details]

    def __str__(self) -> str:
        """
        Display the contents of the log in a readable format.
        :return: A formatted string representing the log.
        """
        output = f"----------------------------------------------------------------------------------------------" \
                 "\n{self.__name.capitalize()} LOG:"

        # iterate through log records and add each as a formatted line:
        for row in self.log.iterrows():
            output += (f"\n[{row['Time']}] {row['Name']} (id: {row['Id']}) "
                       f"{row['Action'].present_tense} {row['Details']}.")
        output += f"\n----------------------------------------------------------------------------------------------\n"
        return output
