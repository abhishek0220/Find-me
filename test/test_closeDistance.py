import pytest
from FindMe.APIs.tasks import isClose

def test_isCloseEvaluatesTrue():
    # IIT Jammu Volleyball Court
    lat1 = 32.801327378634554
    long1 = 74.89640421112314
    # IIT Jammu BasketBall Court
    lat2 = 32.801328595317045
    long2  = 74.89622208882155

    assert isClose(lat1, long1, lat2, long2) == True

def test_isCloseEvaluatesFalse():
    # IIT Jammu Volleyball Court
    lat1 = 32.801327378634554
    long1 = 74.89640421112314
    # Maggi Point
    lat2 = 32.807139869187786
    long2 = 74.89683075592777

    assert isClose(lat1, long1, lat2, long2) == False