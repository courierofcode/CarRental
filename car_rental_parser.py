import os
import sys
import json
import logging
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
def find_record(records, key, value):
    return next((i for i in range(len(records)) if records[i][key] == value), -1)

def ride_duration(start_tstamp, end_tstamp):
    start_dt = datetime.datetime.utcfromtimestamp(int(start_tstamp))  
    end_dt = datetime.datetime.utcfromtimestamp(int(end_tstamp))

    duration = end_dt - start_dt 
    hrs, rem = divmod(duration.total_seconds(), 3600)
    mins, secs = divmod(rem, 60)

    return f"{int(hrs):02d}:{int(mins):02d}:{int(secs):02d}"

def is_car_damaged(comments):
    if comments == "":
        is_damaged = False
    else:
        is_damaged = True
    return is_damaged

def is_return_ontime(duration):
    time_split = [int(split) for split in duration.split(":")]
    time_diff = datetime.timedelta(hours=time_split[0], minutes=time_split[1], seconds=time_split[2])
    total_hrs = time_diff.total_seconds() / 3600

    if total_hrs <= 24:
        is_ontime = True
    else:
        is_ontime = False
    return is_ontime

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
def parse_json(events):
    records = []

    for event in events:
        e_id = event["id"]
        e_type = event["type"]
        e_tstamp = event["timestamp"]
        e_comments = event["comments"]

        # Search records for event
        record = find_record(records, "session_id", e_id)
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
            duration = ride_duration(st_tstamp, end_tstamp)
            records[record]["session_duration"] = duration
            
            # Determine if arrival was on time
            records[record]["returned_late"] = is_return_ontime(duration)
            
            # Determine if car was returned damaged
            if e_type == "END":
                records[record]["car_damaged"] = is_car_damaged(e_comments)

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