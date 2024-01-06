import os
import sys
import json
import logging
import datetime
import parse_utils as utils

# Initialize logger
datetime_str = datetime.datetime.now().strftime("%Y-%M-%d-%H-%M-%S")
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"logfile_{datetime_str}.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create Logger file handler
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def parse_json(events, records):
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
                logger.error(f"Car event type ({e_type}) undefined on: {event}")
                exit(-2)
            
            records.append({\
                "session_id": e_id,
                "session_start": st_tstamp, 
                "session_end": end_tstamp, 
                "session_duration": 0, 
                "returned_late": False,
                "car_damaged": False })

        else:
            if e_type == "START":
                records[record]["session_start"] = e_tstamp
            elif e_type == "END":
                records[record]["session_end"] = e_tstamp
            else: # Record type undefined
                logger.error(f"Car event type ({e_type}) undefined on: {event}")
                exit(-2)
            
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

def main():
    # Validate command line arguments
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        logger.error("Wrong number of arguments")
        logger.error("Usage: py car_rental_parser.py <events>.json")
        exit(-1)

    if len(sys.argv) == 2:
        # Validate input file
        events_file = str(sys.argv[1])
        logger.debug(f"Command Run: python car_rental_parser.py {events_file}")
        events = utils.validate_file(events_file, logger)
        logger.info(f"Input file ({events_file}) JSON syntax validated")


        # Parse Input JSON file
        records = []
        logger.debug("Attempting to parse JSON file...")
        parse_json(events, records)
        logger.info("Event records parsed successfully")

        # Write Output JSON file
        with open('output.json', 'w') as f:
            logger.debug("Attempting to create (output.json) file")
            json.dump(records, f, indent=4)
            logger.info("Output records file (outputs.json) created")
    exit(0)        

if __name__ == '__main__':
    main()