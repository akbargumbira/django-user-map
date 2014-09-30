# coding=utf-8
"""Utilities module."""


def wrap_number(number, range):
    """Wrap number to lie on the range.

    :param number: Number to be wrapped.
    :type number: int

    :param range: Min and max range in the form of [min, max]
    :type range: list
    """
    minimum = range[0]
    maximum = range[1]
    delta = maximum - minimum
    if number == maximum:
        return maximum
    else:
        return ((number - minimum) % delta + delta) % delta + minimum
