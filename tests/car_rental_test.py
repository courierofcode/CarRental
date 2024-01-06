import pytest
import sys
import os
# Navigate to upper directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parse_utils as utils
import car_rental_parser as cr_parser
   
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

@pytest.fixture
def test_dir_path():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    return test_dir

@pytest.fixture
def cmd_line_args(monkeypatch, test_dir_path):
    input_path = os.path.join(test_dir_path, "valid_input.json")
    monkeypatch.setattr(sys, "argv", ["car_rental_parser.py", input_path])

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

"""Exit Codes
     0 - No Error
    -1 - Command line argv error
    -2 - JSON file data type error
"""
def test_cmd_line(monkeypatch, test_dir_path):
    input_path = os.path.join(test_dir_path, "invalid_input2.json")
    monkeypatch.setattr(sys, "argv", ["car_rental_parser.py", input_path, "not_allowed.json"])

    with pytest.raises(SystemExit) as exinfo:
        cr_parser.main()
    assert exinfo.value.code == -1

def test_json_dtype(monkeypatch, test_dir_path):
    input_path = os.path.join(test_dir_path, "invalid_input1.json")
    monkeypatch.setattr(sys, "argv", ["car_rental_parser.py", input_path])

    with pytest.raises(SystemExit) as exinfo:
        cr_parser.main()
    assert exinfo.value.code == -2


def test_integration(cmd_line_args):
    with pytest.raises(SystemExit) as exinfo:
        cr_parser.main()
    assert exinfo.value.code == 0   