# -------------------------------------------------------------------------------
# Input validations
# Joseph Egan
# 2026-03-18
# Sources: https://github.com/MachineCreation/TMDb_listing_function/blob/main/UI/input_validations.py
# -------------------------------------------------------------------------------
# Description: simple input validations

# Local imports
import app.Logic.processing.exceptions as ie

# python imports
from typing import Callable

def input_port(
    prompt: str = "Enter a valid port number:",
    e_message: str = "Invalid port. Please enter a valid port number. (0 - 65535)"
        ) -> int:
    '''
    Prompts user for a whole number input with optional specified bounds.
    :param prompt: Prompt string shown to the user
    :param e_message: Error message to show on invalid input
    :return: The entered integer value
    '''
    while True:
        try:
            value = input(prompt + " ")    # get input
            # check for float value; don't assume truncated value is
            # acceptable
            
            if "." in value:
                raise ValueError
            value = int(value)  # convert value to int
            if 0 > value > 65535:
                raise ValueError
            return value

        except ValueError:
            print(e_message)
        except ie.RangeError as e:
            print_error(e, e_message)

# -------------------
def input_string(prompt: str = "Please enter a word or phrase",
                 e_message: str = "String value can not be outside "
                 "provided conditions.",
                 valid_func: Callable[[str], None] | None = None):
    while True:
        value = input(prompt + " ").strip()

        try:
            if valid_func:
                valid_func(value)
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")

        

# -------------------
def print_error(error: Exception,
                message: str):
    '''
    Prints an error message along with details from an exception if they
    exist.
    :param error: The exception object containing error details.
    :param message: The error message to be printed.
    :return: None
    '''
    print(message)
    if error.args and error.args[0]:
        print(error.args[0])


