"""
File: schedule.py
Description: Contains the Schedule class which is used to plan daily tasks/routines for animals & staff in the zoo.
Log is a subclass of DataRecord.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from datetime import time

import pandas as pd
from pandas import DataFrame

from action import Action
from data_record import DataRecord


class Schedule(DataRecord):
    """Create a Schedule instance"""

    def __init__(self, schedule_name: str):
        """
        Create a new Schedule instance.
        :param schedule_name: The name of the Schedule.
        """
        super().__init__(schedule_name)

        # create a dataframe to store scheduled actions (base columns with new columns added):
        cols_to_add = DataFrame(
            {"Time": pd.Series(dtype="object")})  # time object - no date required as schedule is daily.
        self.data = pd.concat([self.data, cols_to_add])

    def new(self, new_row: dict):
        """
        Add a new row of information to the log.

        :param new_row: New row of information to be added, represented as a dictionary.
            The dictionary must contain:
            - 'Time' (time): When the action should be performed.
            - 'SubjectID' (int): ID of the performer of the action.
            - 'SubjectName' (str): Name of the performer of the action.
            - 'Action' (Action): The action that should be performed.
            - 'ObjectID' (int): ID of the receiver of the action.
            - 'ObjectName' (str): Name of the receiver of the action.
            - 'Details' (str): Further description of the action to be performed.
        :return: None
        """

        if not isinstance(new_row.get("Time"),
                          time):  # the time class will internally handle formatting issues.
            raise TypeError("The 'Time' value of the new row must be a time object.")

        if not isinstance(new_row.get("Action"), Action):
            raise TypeError("The logged action must be from the Action enumeration.")

        super().new(new_row)

    def __str__(self) -> str:
        """
        Display the schedule contents in a readable format.
        :return: A formatted string representing the diet.
        """
        output = super().__str__() + " SCHEDULE:"

        if len(self.data) == 0:
            output += "\nNo events scheduled."
        else:
            self.data.sort_values(by=['Time'], ascending=True, inplace=True)
            event_times = self.data['Time'].unique()
            event_number = 1

            # group components of diet by time they should be eaten (aka meals).
            for event_time in event_times:
                event = self.data[self.data['Time'] == event_time]
                output += f"\n\nEVENT {event_number} @ {event_time}"
                event_number += 1

                # iterate through diet entries for the meal_time and add each as a formatted line:
                for row in event.itertuples():
                    subject_desc = f"{row.SubjectName}_{row.SubjectID}"
                    object_desc = f"{row.ObjectName}_{row.ObjectID}"
                    # if the subject of the scheduled action only relates to the performer, do not describe
                    # the ObjectName and ObjectID of the event:
                    object_desc = "" if object_desc == subject_desc else object_desc + " "

                    output += f"\n - {subject_desc} to {row.Action.imperative} {object_desc}({row.Details})"
        output += f"\n----------------------------------------------------------------------------------------------\n"
        return output

    def remove(self, after_time: time = time(0, 0, 0),
               before_time: time = time(23, 59, 59)):
        """
        Remove record(s) from Schedule which occur in the provided time range.
        :param after_time: The start of the time range associated with the record(s) to be removed.
        :param before_time: The end of the time range associated with the record(s) to be removed.
        :return: None
        """
        # replace the existing schedule with a version where entries that match 'time' conditions are excluded:
        self.data = self.data[(after_time > self.data['Time']) | (self.data['Time'] > before_time)]
