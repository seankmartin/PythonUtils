"""Array manipulation."""
import numpy as np


def non_zero_divide(numerator, denominator):
    """Divide numerator / denominator, but if denominator is zero result is zero"""
    result = np.divide(
        numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0
    )
    return result
