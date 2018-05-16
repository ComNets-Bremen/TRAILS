#!/usr/bin/env python2.7

"""
command example: area_and_speed_stats.py -i selected_traces_100

python script.py -i directory-of-traces-dataset

script = area_and_speed_stats.py
directory of traces dataset = selected_traces_100
output will be displayed on terminal after script has ended
"""

import sys, os, math, numpy

from __main__ import *

''' Function to convert GPS coordinates i.e. 
    latitudes and longitudes to cartesian
    coordinates i.e. x,y,z'''
def latlong_to_xyz(latitude, longitude):
   
    global dimensions
    
    x = round(6371000.0 * math.cos(math.radians(latitude)) * math.cos(math.radians(longitude)))
    y = round(6371000.0 * math.cos(math.radians(latitude)) * math.sin(math.radians(longitude)))
    z = 0.000            #round(6371000.0 * math.sin(math.radians(latitude)))
    
    return (x,y,z)

''' Function to find minimum and maximum values
    present in the columns of "data" to normalize
    the data'''
def find_min_max(data):
    
    x_coord = []
    y_coord = []
    z_coord = []
    s_time = []
    
    for each in data:
        x_coord.append(each[0])
        y_coord.append(each[1])
        z_coord.append(each[2])
        s_time.append(each[3])
        
    return (min(x_coord), min(y_coord), min(z_coord), min(s_time), max(x_coord), max(y_coord), max(z_coord))
    
    
def main():
    
    files_directory = sys.argv[2]
    
    min_coords = []
    max_coords = []
    speed = []
    
    if not os.path.exists(files_directory):
        print("Given directory does not exists")
        quit()
    
    trace_files = os.listdir(files_directory)
    
    if len(trace_files) == 0:
        print("No trace files are present in mentioned directory")
        quit()
    
    print("Processing : ")
    
    for trace in trace_files:
        print(trace)
        with open(files_directory + "/" + trace) as filedata:
            content = filedata.readlines()
        filedata.close()
        
        tmp_list2 = []
        for each in content:
            temp = tuple(each.strip().split())
            x,y,z = latlong_to_xyz(float(temp[0]), float(temp[1]))
            tup = (x, y, z, int(temp[3].replace("'","").replace(")","")))
            
            tmp_list2.append(tup)
                
        min_x, min_y, min_z, min_time, max_x, max_y, max_z = find_min_max(tmp_list2)
        
        tmp_list = []
        for each in tmp_list2:
            t = (each[0]-min_x, each[1]-min_y, each[2]-min_z, each[3]-min_time)
            tmp_list.append(t)
        
        min_x, min_y, min_z, min_time, max_x, max_y, max_z = find_min_max(tmp_list)
        
        min_coords.append((min_x, min_y, min_z))
        max_coords.append((max_x, max_y, max_z))
        
        i = 1
        
        while i < len(tmp_list):
            del_t = tmp_list[i-1][3] - tmp_list[i][3]
            del_d = math.hypot(tmp_list[i][0]-tmp_list[i-1][0], tmp_list[i][1]-tmp_list[i-1][1])
            speed.append(del_d / del_t)
            i = i + 1

    global_min_area = map(min, zip(*min_coords))
    global_max_area = map(max, zip(*max_coords))
    
    print()
    print("*" * 25)
    print()
    print("Minimum (x,y,z) : ", global_min_area, "m")
    print("Maximum (x,y,z) : ", global_max_area, "m")
    print("Minimum Speed   : ", min(speed), "mps")
    print("Maximum Speed   : ", max(speed), "mps")
    
    print("Average Speed   : ", numpy.mean(speed), "mps")
    print()
    print("*" * 25)
    print()
if __name__ == "__main__":
    main()