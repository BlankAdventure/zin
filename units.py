# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 18:16:40 2025

@author: BlankAdventure
"""

import re
from typing import TypeAlias

Unit: TypeAlias = str|float|int

suffixes = {'G': 1e9,
            'M': 1e6,
            'k': 1e3,
            'h': 1e2,
            'c': 1e-2,
            'm': 1e-3,
            'u': 1e-6,
            'n': 1e-9,
            'p': 1e-12}

valid_units = "".join(suffixes.keys())
regex = rf"^(?:(\d+\.\d+|\d+|\.\d+))([{valid_units}])$"

def decode_unit(text: str) -> float:
    '''Takes a string and checks it contains a valid float followed by a single
    suffix character. If it does, it returns the numerical interpretaion. If 
    not, ValueError is raised.
    '''
    
    # The regex with capturing groups for the float and the character
    # Group 1: (\d+(?:\.\d+)?) - Matches the float part
    # Group 2: ([a-zA-Z]) - Matches the single trailing character
    #regex = r"^(?:(\d+\.\d+|\d+|\.\d+))([a-zA-Z])$"

    
    match = re.match(regex, text)

    if match:
        float_str = match.group(1) # Get the string matched by the first capturing group
        character = match.group(2) # Get the string matched by the second capturing group        
        return float(float_str)*suffixes[character]
    else:
        raise ValueError(f'{text} <--invalid component specification!')


def handle_units(unit: Unit) -> float:
    '''
    The main function for dealing with units. If a numeric value is passed in
    it simply returns this value. If a string is passed in, it calls
    decode_unit to obtain a numeric value.

    Parameters
    ----------
    str_or_num : str|float|int
        String with units to decode, or numeric value.

    Raises
    ------
    TypeError
        Triggered if input is neither string nor numeric (float or int)

    Returns
    -------
    float
        The numeric value (either decoded or passed through)

    '''
    match unit:
        case float() | int():
            return unit
        case str():
            return decode_unit(unit)
        case _:
            raise TypeError('Must be a a float or string')



