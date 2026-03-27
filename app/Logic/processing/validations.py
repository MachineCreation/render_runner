# -------------------------------------------------------------------------------
# Input validations
# Joseph Egan
# 2026-03-18
# Sources:
# https://github.com/MachineCreation/TMDb_listing_function/blob/main/UI/input_validations.py
# -------------------------------------------------------------------------------
# Description: simple input validations

# Local imports
import app.Logic.processing.exceptions as ie

# python imports
from typing import Callable
import re


def input_port(
    prompt: str = "Enter a valid port number:",
    e_message: str = "Please enter a valid port number. (0 - 65535)"
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

            if 0 > value or value > 65535:
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


# -------------------
def input_y_or_n(
    prompt: str = "Please enter y(Yes) or n(No)",
    e_message: str = "Value must be Y, N, Yes, or No"
        ) -> bool:
    '''
    Prompts user for Y or N.
    :param prompt: Prompt string shown to the user
    :param e_message: Error message shown on invalid input
    :return: True if user answered yes, False if no
    '''
    accepted = ['y', 'yes', 'n', 'no']
    while True:
        value = input(prompt + ' ').lower()
        if value in accepted:
            return value in ['y', 'yes']
        print(f'Invalid Entry: {e_message}')


# -------------------
def input_int(
    ge: int | None = None,
    gt: int | None = None,
    le: int | None = None,
    lt: int | None = None,
    prompt: str = "Enter whole number:",
    e_message: str = "Invalid input. Please enter a whole number."
        ) -> int:
    '''
    Prompts user for a whole number input with optional specified bounds.
    :param ge: lower inclusive bound
    :param gt: lower exclusive bound
    :param le: upper inclusive bound
    :param lt: upper exclusive bound
    :param prompt: Prompt string shown to the user
    :param e_message: Error message to show on invalid input
    :return: The entered integer value
    '''
    # print(f'ge:{ge}, gt:{gt}, le:{le}, lt:{lt}')
    # validate bound configuration
    validate_bounds(ge=ge, gt=gt, le=le, lt=lt)

    while True:
        try:
            value = input(prompt + " ")    # get input
            # check for float value; don't assume truncated value is
            # acceptable
            if "." in value:
                raise ValueError
            value = int(value)  # convert value to int
            validate_number_against_bounds(
                value, ge=ge, gt=gt, le=le, lt=lt)
            return value

        except ValueError:
            print(e_message)
        except ie.RangeError as e:
            print_error(e, e_message)


# -------------------
def validate_bounds(
    ge=None,
    gt=None,
    le=None,
    lt=None
        ):
    '''
    Validates that the provided bound keywords are not contradictory and
    that the lower bound is strictly less than the upper bound unless both
    are equal and inclusive.
    :param ge: lower inclusive
    :param gt: lower exclusive
    :param le: upper inclusive
    :param lt: upper exclusive
    :return: None
    '''
    # Only one lower-bound allowed
    if ge is not None and gt is not None:
        raise ie.RangeError("Specify at most one of ge or gt.")

    # Only one upper-bound allowed
    if le is not None and lt is not None:
        raise ie.RangeError("Specify at most one of le or lt.")

    # Determine lower and upper bounds (value, inclusive:bool)
    lower = None
    if gt is not None:
        lower = (gt, False)
    elif ge is not None:
        lower = (ge, True)

    upper = None
    if lt is not None:
        upper = (lt, False)
    elif le is not None:
        upper = (le, True)

    # If both provided, ensure the interval is not empty
    if lower is not None and upper is not None:
        lv, lincl = lower
        uv, uincl = upper

        if lv < uv:
            return
        if lv > uv:
            raise ie.RangeError(
                "Lower bound must be less than upper bound.")
        # lower value == upper value
        if not (lincl and uincl):
            raise ie.RangeError("Bounds define an empty range (equal"
                                " endpoints but exclusive).")


# -------------------
def validate_number_against_bounds(
    value,
    *,
    ge=None,
    gt=None,
    le=None,
    lt=None
        ):
    '''
    Validates that a number satisfies the specified bound keywords.
    :param value: The number to validate.
    :param ge: lower inclusive
    :param gt: lower exclusive
    :param le: upper inclusive
    :param lt: upper exclusive
    :return: None
    '''
    if ge is not None and value < ge:
        raise ie.RangeError(
            f'Input must be greater than or equal to {ge}.')
    if gt is not None and value <= gt:
        raise ie.RangeError(
            f'Input must be greater than {gt}.')
    if le is not None and value > le:
        raise ie.RangeError(
            f'Input must be less than or equal to {le}.')
    if lt is not None and value >= lt:
        raise ie.RangeError(
            f'Input must be less than {lt}.')


# -------------------
def print_delineator():
    '''
    prints simple delineation line
    :return: None
    '''
    print('-' * 79 + '\n')


# -------------------
def python_safe_prompt(prompt: str) -> str:
    """
    Validate and sanitize a prompt string for safe storage and API usage.
    """

    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string")

    # Strip leading/trailing whitespace
    cleaned_prompt = prompt.strip()

    # Increased max length for real-world AI prompts
    MAX_LENGTH = 12000
    if len(cleaned_prompt) > MAX_LENGTH:
        raise ValueError(f"Prompt exceeds max length of {MAX_LENGTH}")

    # Remove non-printable control characters (except newline/tab)
    cleaned_prompt = re.sub(r"[^\x20-\x7E\n\t]", "", cleaned_prompt)

    # Normalize excessive whitespace (but preserve intent)
    cleaned_prompt = re.sub(r"[ \t]+", " ", cleaned_prompt)

    if not cleaned_prompt:
        raise ValueError("Prompt cannot be empty after cleaning")

    return cleaned_prompt


# -------------------
def select_item(
    static_options: list[str],
    map: dict[str, str | Callable] | None = None,
    prompt='Please type an option from the list',
    e_message='Typed option not found'
        ) -> str | bool | Callable:
    '''
    Prompts a user to type an option from a provided list or dict.
    :param static_options: List of display options
    :param map: Optional mapping from user-entered key to return value
    :param prompt: Prompt string shown to the user
    :param e_message: Error message for invalid selection
    :return: The selected value (original list item, mapped value, or callable)
    '''
    options_list = [opt.lower() for opt in static_options]
    display_options = static_options

    while True:
        for idx, option in enumerate(display_options):
            print(f'{idx + 1}. {option}')
        value = input_string(prompt + " \n").lower().strip()

        # return original value for key if map
        if map is not None:
            for key, val in map.items():
                if value == key.lower():
                    return val

        # return for list only
        if value in options_list:
            return value

        print(e_message)