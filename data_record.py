"""
File: data_record.py
Description: Contains the DataRecord class which is used to keep track of information about zoo activities.
Author: Nenja Ivanovic
ID: 110462390
Username: ivany005
This is my own work as defined by the University's Academic Integrity Policy.
"""
from abc import ABC, abstractmethod

import pandas as pd
from pandas import DataFrame


class DataRecord(ABC):
    def __init__(self, record_name: str):
        """
        Create a new DataRecord instance
        :param record_name: The name of the DataRecord.
        """
        self.__name = record_name
        self.__data = pd.DataFrame()

    def get_data(self) -> DataFrame:
        """Return the data stored in the DataRecord instance.
        :return DataFrame"""
        return self.__data

    def set_data(self, new_data: DataFrame):
        """
        Replace the data stored in the DataRecord instance with another DataFrame that has matching columns.
        :param new_data: The new data to store (a DataFrame).
        :return: None
        """
        if not isinstance(new_data, DataFrame):
            raise TypeError("The data attribute of a DataRecord object can only be set to a pandas DataFrame.")
        # check that the new dataframe contains at minimum all columns of the existing dataframe it is replacing:
        if not (all(cols in new_data.columns.values for cols in self.data.columns.values)):
            raise ValueError("The new data must contain the columns of the existing data.")
        self.__data = new_data

    def get_name(self) -> str:
        """Return the name (string) of the DataRecord."""
        return self.__name

    data = property(get_data, set_data)
    name = property(get_name)

    @abstractmethod
    def new(self, new_row: dict):
        """
        Add a new row of information to the DataRecord.
        :param new_row: The new row of information to be added, represented as a dictionary.
        :return: None
        """
        if not isinstance(new_row, dict):
            raise TypeError("The new row of data must be provided as a Dictionary object.")
        if not set(self.data.columns.values) == set(new_row.keys()):
            raise ValueError(f"The dictionary keys must match the existing columns of the DataRecord data attribute. "
                             f"\nExpected: {set(self.data.columns.values)}"
                             f"\nGot: {set(new_row.keys())}")
        next_empty_row = len(self.data)
        self.data.loc[next_empty_row] = new_row

    @abstractmethod  # every concrete subclass must have a special string method for displaying records.
    def __str__(self) -> str:
        """Return a formatted string representation of the DataRecord's contents."""
        output = (f"----------------------------------------------------------------------------------------------"
                  f"\n{self.name.upper()}")
        return output
        # the abstract __string__() method returns the start of every subclass string output which can be added to.
