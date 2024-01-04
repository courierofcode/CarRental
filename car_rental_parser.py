import sys
import json
import logging
import parse_utils as utils

def parse_json(events):
    records = []

    for event in events:
        e_id = event["id"]
        e_type = event["type"]
        e_tstamp = event["timestamp"]
        e_comments = event["comments"]

        # Search records for event
        record = utils.find_record(records, "session_id", e_id)
        if record == -1:    # Record does not exist
            if e_type == "START":
                st_tstamp = e_tstamp
                end_tstamp = -1
            elif e_type == "END":
                st_tstamp = -1
                end_tstamp = e_tstamp
            else: # Record type undefined
                print("Error: Car Event type undefined")
            
            records.append({\
                "session_id": e_id,
                "session_start": st_tstamp, 
                "session_end": end_tstamp, 
                "session_duration": 0, 
                "returned_late": False,
                "car_damaged": False })

        else:
            if e_type == "START":
                st_tstamp = e_tstamp
                print(record)
                records[record]["session_start"] = e_tstamp
            elif e_type == "END":
                end_tstamp = e_tstamp
                records[record]["session_end"] = e_tstamp
            
            # Calculate Duration
            st_tstamp = records[record]["session_start"]
            end_tstamp = records[record]["session_end"]
            duration = utils.ride_duration(st_tstamp, end_tstamp)
            records[record]["session_duration"] = duration
            
            # Determine if arrival was on time
            records[record]["returned_late"] = utils.is_return_late(duration)
            
            # Determine if car was returned damaged
            if e_type == "END":
                records[record]["car_damaged"] = utils.is_car_damaged(e_comments)

    return records

def main():
    
    # Validate command line arguments
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print("Error: Wrong number of arguments")
        print("Usage: py car_rental_parser.py <events>.json")
        exit()

    if len(sys.argv) == 2:
        # Validate input file
        events_file = str(sys.argv[1])
        events = utils.validate_file(events_file)

        # Parse Input JSON file
        records = parse_json(events)

        # Write Output JSON file
        with open('output.json', 'w') as f:
            json.dump(records, f)
        

if __name__ == '__main__':
    main()