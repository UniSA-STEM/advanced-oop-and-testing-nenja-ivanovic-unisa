"""
File: data_record.py
Description: Contains the abstract DataRecord class which is inherited by classes that represent objects which
keep track of information about zoo activities.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from abc import ABC, abstractmethod

import pandas as pd
from pandas import DataFrame

from action import Action


class DataRecord(ABC):
    _next_empty_row = 0  # use to index records, increment by +1 each time a new row is added to a record.

    # Id is stored as a class attribute so that every row in the zoo's records has an absolutely unique
    # reference number and can be tracked down if required.

    def __init__(self, record_name: str):
        """
        Create a new DataRecord instance
        :param record_name: The name of the DataRecord.
        """
        self.__name = record_name
        self.__data = pd.DataFrame({
            "SubjectID": pd.Series(dtype="string"),
            "SubjectName": pd.Series(dtype="string"),
            "Action": pd.Series(dtype="object"),  # Action enumeration
            "ObjectID": pd.Series(dtype="string"),  # receiver of the action (if applicable)
            "ObjectName": pd.Series(dtype="string"),  # receiver of the action (if applicable)
            "Details": pd.Series(dtype="string")})

    def get_data(self) -> DataFrame:
        """Return the data stored in the DataRecord instance.
        :return: DataFrame"""
        return self.__data

    def set_data(self, new_data: DataFrame):
        """
        Replace the data stored in the DataRecord instance with another DataFrame that has matching columns.
        :param new_data: The new data to store (a DataFrame).
        :return: None
        """

        try:
            # check that the new dataframe contains at minimum all columns of the existing dataframe it is replacing:
            if not (all(cols in new_data.columns.values for cols in self.data.columns.values)):
                raise ValueError("The new data must contain the columns of the existing data.")
            self.__data = new_data
        except TypeError:
            print(f"[ERROR] The data attribute of a DataRecord object can only be set to a pandas DataFrame."
                  f" No change made.\n")
        except ValueError as e:
            print(f"[ERROR] {e} No change made.\n")

    def get_name(self) -> str:
        """Return the name (string) of the DataRecord."""
        return self.__name

    def set_name(self, name: str):
        """Set the name of the DataRecord to a new string value."""
        self.__name = name

    data = property(get_data, set_data)
    name = property(get_name, set_name)

    @abstractmethod
    def new(self, new_row: dict) -> int | None:
        """
        Add a new row of information to the DataRecord.
        :param new_row: The new row of information to be added, represented as a dictionary.
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
        try:
            if not isinstance(new_row, dict):
                raise TypeError("The new row of data must be provided as a Dictionary object.")

            if not isinstance(new_row.get("Action"), Action):
                raise TypeError("The action of a new log record must be from the Action enumeration.")

            assert set(self.data.columns.values) == set(new_row.keys()), (
                f"The dictionary keys must match the existing columns of the DataRecord data attribute. "
                f"\nExpected: {set(self.__data.columns.values)}"
                f"\nGot: {set(new_row.keys())}")

            self.__data.loc[DataRecord._next_empty_row] = new_row
            DataRecord._next_empty_row += 1
            return DataRecord._next_empty_row - 1  # reduce by one as incrementing by +1 has already occurred.

        except TypeError as e:
            print(f"[ERROR] {e} No change made.\n")
            return None
        except AssertionError as e:
            print(f"[ERROR] {e}\nNo change made.\n")
            return None

    @abstractmethod  # every concrete subclass must have a special string method for displaying records.
    def __str__(self) -> str:
        """Return a formatted string representation of the DataRecord's contents."""
        output = (f"----------------------------------------------------------------------------------------------"
                  f"\n{self.name.upper()}")
        return output
        # the abstract __string__() method returns the start of every subclass string output which can be added to.
