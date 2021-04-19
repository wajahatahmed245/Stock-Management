from random import randint
from django.dispatch import Signal


def getImei(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)

