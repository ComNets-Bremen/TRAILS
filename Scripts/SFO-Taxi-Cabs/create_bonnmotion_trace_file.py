#!/usr/bin/env python2.7

"""
command example: python create_bonnmotion_trace_file.py -i selected_traces_100 2

python script.py -i directory-of-traces-dataset Cartesian-coordinates-dimensions-to-be-created

script = create_bonnmotion_trace_file.py
directory of traces dataset = selected_traces_100
dimensions of cartesian coordinates to be used for bonn motion movement file = 2 or 3
"""

import sys, os, math
import math

from __main__ import *

''' Function to convert GPS coordinates i.e. 
    latitudes and longitudes to cartesian
    coordinates i.e. x,y,z'''
def latlong_to_xyz(latitude, longitude):
   
    global dimensions
    
    x = round(6371000.0 * math.cos(math.radians(latitude)) * math.cos(math.radians(longitude)))
    y = round(6371000.0 * math.cos(math.radians(latitude)) * math.sin(math.radians(longitude)))
    z = 0.000            #round(6371000.0 * math.sin(math.radians(latitude)))
    
    if dimensions == 3:
        z = round(6371000.0 * math.sin(math.radians(latitude)))
    
    return (x,y,z)

''' Function to find minimum and maximum values
    present in the columns of "data" to normalize
    the data'''
def find_min(data):
    
    x_coord = []
    y_coord = []
    z_coord = []
    s_time = []
    
    for each in data:
        x_coord.append(each[0])
        y_coord.append(each[1])
        z_coord.append(each[2])
        s_time.append(each[3])
        
    return (min(x_coord), min(y_coord), min(z_coord), min(s_time))
    

def main():
    
    global dimensions
    
    files_directory = sys.argv[2]
    dimensions = int(sys.argv[3])
    
    if not os.path.exists(files_directory):
        print "Given directory does not exists"
        quit()
    
    trace_files = os.listdir(files_directory)
    
    if len(trace_files) == 0:
        print "No trace files are present in mentioned directory"
        quit()
    
    bonn_motion = []
    
    print "Processing : "
    
    for trace in trace_files:
        print trace
        with open(files_directory + "/" + trace) as filedata:
            content = filedata.readlines()
        filedata.close()
                
        tmp_list = []
        for each in content:
            temp = tuple(each.strip().split())                                # Stores the data in tuple form
            x,y,z = latlong_to_xyz(float(temp[0]), float(temp[1]))
            
            #if dimensions == 2:
            #    tup = (x, y, int(temp[3].replace("'","").replace(")","")))
            #elif dimensions == 3:
            #    tup = (x, y, z, int(temp[3].replace("'","").replace(")","")))
            
            tup = (x, y, z, int(temp[3].replace("'","").replace(")","")))
            
            tmp_list.append(tup)
                
        min_x, min_y, min_z, min_time = find_min(tmp_list)
                
        tmp_lst2 = []
        for each in tmp_list:
            t = (each[0]-min_x, each[1]-min_y, each[2]-min_z, each[3]-min_time)
            tmp_lst2.append(t)
                    
        tmp_lst2.sort(key=lambda tup: tup[3])
                
        bm = ()
        for each in tmp_lst2:                    
            if dimensions == 2:
                bm = bm + (each[3], each[0], each[1],)
            elif dimensions == 3:
                bm = bm + (each[3], each[0], each[1], each[2])
            
                    
        bonn_motion.append(bm)
            
            
    outfile = open ("bonnmotion_" + str(len(trace_files)) + "_cabs.movements", 'w')
    for every in bonn_motion:
        for each in every:
            outfile.write(str(each))
            outfile.write(' ')
        outfile.write('\n')

    outfile.close()
    
    
if __name__ == "__main__":
    main()