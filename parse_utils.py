import os
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