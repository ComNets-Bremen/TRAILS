#!/usr/bin/env python3

import argparse
from file_read_backwards import FileReadBackwards
import glob
import sys

# Main function
def main():
    parser = argparse.ArgumentParser(description='Dump simulation data')
    parser.add_argument('logfolders', type=str, nargs="+", help="Log Folder")
    args = parser.parse_args()
    
    print("# events  ANS TNRT ACD TNC")

    for inputfolder in args.logfolders:
        file_wildcard = inputfolder + "/General-*.txt"
        for filename in glob.glob(file_wildcard):
            frb = FileReadBackwards(filename, encoding="utf-8")
            events_found = False
            ANS_found = False
            ACD_found = False
            events = 0
            ANS_val = 0    
            TNRT_val = 0
            ACD_val = 0    
            TNC_val = 0

            for line in frb:
                if not events_found and "event #" in line:
                    words = line.split("event #")
                    events = int(words[1].strip())
                    events_found = True
                elif not ANS_found and "ANS" in line:
                    words = line.split(" ")
                    ANS_val = int(words[4].strip())    
                    TNRT_val = int(words[6].strip())
                    ANS_found = True
                elif not ACD_found and "ACD" in line:
                    words = line.split(" ")
                    ACD_val = int(float(words[4].strip()))
                    TNC_val = int(words[6].strip())
                    ACD_found = True
                if events_found and ANS_found and ACD_found:
                    break
            print(events, ANS_val, TNRT_val, ACD_val, TNC_val)

if __name__ == "__main__":
    main()

