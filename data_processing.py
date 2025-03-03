import os
import glob
import csv
from datetime import datetime, timedelta

import random
import json

import math

import logging

DATE_FORMAT = "%d-%m-%Y"
NULL_FIELD_VALUES = ['nan', 'nat', 'null', 'none']
STOCK_FILES_DIR = 'stock_price_data_files'
OUTPUT_DIR = 'outputs'

CONSECUTIVE_TIMESTAMPS = 10

# csv_files = glob.glob(f'{STOCK_FILES_DIR}/**/*.csv')

csv_files = {
    p.name: sorted(
        [f.path for f in os.scandir(p.path) if os.path.splitext(f.name)[-1] == ".csv"]
    ) for p in os.scandir('stock_price_data_files/') if os.path.isdir(p.path)
}

def read_csv(file_path, has_header=False):
    """
    Reads a CSV file and returns its content as a list of rows.

    Args:
        file_path (str): The path to the CSV file.
        has_header (bool): Whether the CSV file has a header row.

    Returns:
        list: A list of rows from the CSV file.
    """
    data = list()

    with open(file_path, 'r') as f:
        x = csv.reader(f)
        
        for (_, _row) in enumerate(x):
            data.append(_row)
    
    if not data:
        logging.warning(f"{file_path} is empty.")    
        
    if has_header:
        return data[1:]
    else:
        return data       
    
def to_datetime(date_str, date_format=DATE_FORMAT):
    """
    Converts a date string to a datetime object.

    Args:
        date_str (str): The date string to convert.
        date_format (str): The format of the date string.

    Returns:
        datetime: The corresponding datetime object.
    """
    return datetime.strptime(date_str, date_format)

def from_datetime(date, date_format=DATE_FORMAT):
    """
    Converts a datetime object to a date string.

    Args:
        date (datetime): The datetime object to convert.
        date_format (str): The format of the date string.

    Returns:
        str: The corresponding date string.
    """
    return datetime.strftime(date, date_format)

# lambda functions that will be used to preprocess and postprocess row data
preprocess_row = lambda x: [x[0], to_datetime(x[1]), float(x[2])]
postprocess_row = lambda x: [x[0], from_datetime(x[1]), str(x[2])]
    
def is_valid_date(date_str, date_format=DATE_FORMAT):
    """
    Validates if a date string is in the correct format.

    Args:
        date_str (str): The date string to validate.
        date_format (str): The expected format of the date string.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        to_datetime(date_str, date_format)
        return True
    except ValueError:
        if date_str.lower() in NULL_FIELD_VALUES:
            return True
        else:
            return False
    
def is_valid_value(value_str):
    """
    Validates if a string can be converted to a float.

    Args:
        value_str (str): The string to validate.

    Returns:
        bool: True if the string can be converted to a float, 
        False otherwise.
    """
    try:
        float(value_str)
        return True
    except ValueError:
        if value_str.lower() in NULL_FIELD_VALUES:
            return True
        else:
            return False

def validate_data(data, filename):
    """
    Validates the data from a CSV file.

    Args:
        data (list): The data to validate.
        filename (str): The name of the CSV file.

    Returns:
        bool: True if the data is valid, raises an exception otherwise.
    """
    # validate length of rows
    if not all([len(_d) == 3 for _d in data]):
        raise Exception(
            f"{filename}: Invalid file format! Some rows contain more than 3 columns."
        )

    # validate datetime format
    if not all([is_valid_date(_d[1]) for _d in data]):
        raise Exception(
            f"{filename}: Invalid file data! Second column is not in the right datetime format: {DATE_FORMAT}"
        )

    # validate values
    if not all([is_valid_value(_d[2]) for _d in data]):
        raise Exception(
            f"{filename}: Invalid file data! Third column values cannot be converted to float."
        )

    # validate uniqueness of ticker (first column)
    if len(set([_d[0] for _d in data])) > 1:
        raise Exception(
            f"{filename}: Invalid file data! First column contains more than one ticker."
        )
    
    return True

def preprocess_data(data, drop_nulls=True, sort_by_date=True):
    """
    Preprocesses the data by dropping null values, converting types, 
    and sorting ascending by datetime.

    Args:
        data (list): The data to preprocess.
        drop_nulls (bool): Whether to drop rows with null values.
        sort_by_date (bool): Whether to sort the data by date.

    Returns:
        list: The preprocessed data.
    """
    # drop null values
    if drop_nulls:
        data = [v for v in data if not any([d in NULL_FIELD_VALUES for d in v])]

    # convert to float and datetime
    data = list(map(preprocess_row, data))
    # data = [[v[0], to_datetime(v[1]), float(v[2])] for v in data]

    # sort by date
    if sort_by_date:
        data = sorted(data, key=lambda v: v[1])
    
    return data