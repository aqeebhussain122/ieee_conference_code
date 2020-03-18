#!/usr/bin/python3

import time
import subprocess
import os
import multiprocessing
import sys
import argparse
import ports

def main():
    # Argparser description
    desc = 'Ping sweeping script designed to perform slow pings to the network to capture the active hosts'

    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument("ip_address", help="Target IP address to port sweep", type=str)
    parser.add_argument("sleep_time", help="Quantity of time to sleep before probing the next port", type=int)
    # Variable of the args parser
    args = parser.parse_args()
    print("Target IP address: {}".format(args.ip_address))
    print("Selected sleep time: {}".format(args.sleep_time))
    # Scans a class C range by default
    for port in range(1, 65565):
        target = args.ip_address
        ip_check = validate_ip(target)
         
        # If the IP validation function comes out as incorrect then quit
        if ip_check != True:
            print("Error: The IP address is not correct")
            sys.exit(-1)

        # Using fping to print out the active IP addresses from a /24 subnet mask
        #result = subprocess.call(['fping', '-q', address])
        result = ports.TCPportCheck(target, port)
        sleep = time.sleep(args.sleep_time)
        if result == 0:
            sleep
            print("{} is active".format(port))
            
def timer(value):
    for remaining in range(value, 0 -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rIP address scanned!       \n")

# TO VALIDATE A GIVEN IP ADDRESS TO ENSURE THE ADDRESS REMAINS WITHIN IP FORMATTING
def validate_ip(ip_address):
    split_address = ip_address.split('.')
    # If there are not 4 octects in the given address then the boolean logic is false
    if len(split_address) != 4:
        return False
    # For the values within the split address, validate for any non-integer values
    for num in split_address:
        if not num.isdigit():
            return False
        # Values in the actual split addressing assigned to integer values for checks
        value = int(num)
        # If the IP address contains a value which is not in range of 0 to 255 then it's invalid
        if value < 0 or value > 255:
            return False
    # Return the function as true if all checks pass
    return True

main()
