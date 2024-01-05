import pytest
import sys
import os
# Navigate to upper directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parse_utils as utils
   
@pytest.fixture
def records():
    value = [{ 
    "type": "START",
    "id": "ABC123",
    "timestamp": "1681722000",
    "comments": "No issues - brand new and shiny!"
    },
    { 
    "type": "END",
    "id": "ABC123",
    "timestamp": "1681743600",
    "comments": "Car is missing both front wheels!"
    },
    { 
    "type": "START",
    "id": "ABC456",
    "timestamp": "1680343200",
    "comments": "Small dent on passenger door"
    },
    { 
    "type": "END",
    "id": "1680382800",
    "timestamp": "0123499",
    "comments": "" 
    }]
    return value

@pytest.fixture
def times():
    value = [["1672882240", "1672889440", "02:00:00"],
              ["1704425400", "1704511800", "24:00:00"],
              ["1704511800", "1705203000", "192:00:00"]]
    return value

@pytest.fixture
def comments():
    value = ["Small dent on passenger door", "Car is missing both front wheels!", ""]
    return value

def test_find_record(records):
    assert utils.find_record(records, "id", "ABC123") != -1
    assert utils.find_record(records, "id", "ABC456") != -1
    assert utils.find_record(records, "id", "XZY890") == -1

def test_ride_duration(times):
    assert utils.ride_duration(times[0][0], times[0][1]) == times[0][2]
    assert utils.ride_duration(times[1][0], times[1][1]) == times[1][2]
    assert utils.ride_duration(times[2][0], times[2][1]) == times[2][2]

def test_is_car_damaged(comments):
    assert utils.is_car_damaged(comments[0]) == True
    assert utils.is_car_damaged(comments[1]) == True
    assert utils.is_car_damaged(comments[2]) == False

def test_is_return_late(times):
    assert utils.is_return_late(times[0][2]) == False
    assert utils.is_return_late(times[1][2]) == False
    assert utils.is_return_late(times[2][2]) == True

    