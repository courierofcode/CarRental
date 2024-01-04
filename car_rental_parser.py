import os
import sys
import json
import datetime

def validate_file(events_file):
    # Validate file location
    if os.path.isfile(events_file) == False:
        print("Error: File does not exist")
        exit()
    # Validate file name format
    if events_file.endswith(".json") == False:
        print("Error: Input file format - <events>.json")
        exit()

    else:
        # Validate file syntax (JSON file for best practice)
        with open(events_file, 'r') as events_data:
            try: 
                events = json.load(events_data)
            except json.JSONDecodeError as e:
                print(f"Error: JSON decoding error {e}")
                exit()
        return events


""" List of dictionaries
        records = [{
            "session_id": 
            "session_start":
            "session_end":
            "session_duration":
            "returned_late": 
            "car_damaged": 
            }]
"""   
def parse_json():
    # Search records for event
    """
        If record does NOT exist -> Create Record
        If record exists -> Validate event
            If event is valid add new event data to record
                Update Time Entry
                Calculate Duration
                Calculate if car was late
                Calculate if car was damaged
    """

def main():
    # Validate command line arguments
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print("Error: Wrong number of arguments")
        print("Usage: py car_rental_parser.py <events>.json")
        exit()

    if len(sys.argv) == 2:
        # Validate input file
        events_file = str(sys.argv[1])
        events = validate_file(events_file)

        """ List of dictionaries
            events = [{
                "id": 
                "type":
                "timestamp":
                "comments":
                }]
        """
        # Parse Input JSON file
        records = parse_json(events)

        # Write Output JSON file
        with open('output.json', 'w') as f:
            json.dump(records, f)
        

if __name__ == '__main__':
    main()