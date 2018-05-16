#!/usr/bin/env python2.7

"""
command example: python convert-to-cart.py -i /home/anas/Python/final_product/selected_traces_100 processed_traces_100 new

python script.py -i directory-of-traces-dataset directory-to-place-cartesian-traces keyword-to-identify-traces-in-source-directory

script = convert-to-cart.py
directory of traces dataset = /home/anas/Python/final_product/selected_traces_100
directory to place cartesian trace inside = processed_traces_100
keyword for identification of trace files inside source directory = new
"""

import sys, os, os.path, math
from __main__ import *


#######################################################################################################
''' Function to convert GPS coordinates i.e. 
    latitudes and longitudes to cartesian
    coordinates i.e. x,y,z
    Returnable Value: Cartesian Coordinates i.e. x,y,z'''
def gps_to_cartesian(latitude, longitude):
    
    x = round(6371000.0 * math.cos(math.radians(latitude)) * math.cos(math.radians(longitude)))
    y = round(6371000.0 * math.cos(math.radians(latitude)) * math.sin(math.radians(longitude)))
    z = 0.000                 # If 3D simulation is needed then use following formula for z-coordinate
                              # z = round(6371000.0 * math.sin(math.radians(latitude)))
    return (x,y,z)
#######################################################################################################


#######################################################################################################
def main():
    
    traces_directory = sys.argv[2]
    processed_traces_directory = sys.argv[3]
    trace_file_keyword = sys.argv[4]
    
    if not os.path.exists(traces_directory):
        print "Given directory does not exists"
        quit()
    
    trace_files = os.listdir(traces_directory)
    
    if len(trace_files) == 0:
        print "No trace files are present in mentioned directory"
        quit()
    
    if not os.path.exists(processed_traces_directory):
        os.makedirs(processed_traces_directory)
    
    list_of_files = os.listdir(traces_directory)
    
    for each_file in list_of_files:
        if "-cartesian" in each_file:
            print each_file , "exists already :: deleting"
            os.remove(each_file)
    
    list_of_files = os.listdir(traces_directory)
    list_of_files.sort()
    
    count = 1
    min_cartesian_data = []
    trace_names = []
    all_cartesian_data = []
    
    for trace_file in list_of_files:
        if trace_file_keyword in trace_file:
            count += 1
            converted_and_normalized_trace = processed_traces_directory + "/" + trace_file.replace(".txt","") + "-cartesian.txt"
            trace_names.append(converted_and_normalized_trace)
            
            print count, "of", len(list_of_files), " :: Reading GPS Trace :: ", trace_file
            
            with open (traces_directory + "/" + trace_file) as open_trace:
                trace_data = open_trace.readlines()
            open_trace.close()
            
            temp_cartesian_data = []
            for each in trace_data:
                gps_row = tuple(each.strip().split())
                x,y,z = gps_to_cartesian(float(gps_row[0]), float(gps_row[1]))
                cartesian_row = (x, y, z, int(gps_row[3].replace("'","").replace(")","")))
                temp_cartesian_data.append(cartesian_row)
                
            outfile = open(converted_and_normalized_trace, "w+")
            for each in temp_cartesian_data:
                outfile.write(str(each[0]))
                outfile.write(" ")
                outfile.write(str(each[1]))
                outfile.write(" ")
                outfile.write(str(each[2]))
                outfile.write(" ")
                outfile.write(str(each[3]))
                outfile.write("\n")
            outfile.close()
#######################################################################################################

    
if __name__ == "__main__":
    main()