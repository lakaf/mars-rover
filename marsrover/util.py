"""Module for util functions"""

from typing import List


def strip_str_list(str_list: List[str]) -> List[str]:
    """Strips all str elements in a list.

    Args:
        str_list (List[str]): List of string elements

    Returns:
        List[str]: List of stripped string elements
    """
    return [s.strip() for s in str_list]
