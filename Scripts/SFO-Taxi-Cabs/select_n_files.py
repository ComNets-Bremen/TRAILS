#!/usr/bin/env python2.7

"""
command example: python select_n_files.py -i 4 new cabspottingdata select_files/selected 123456789

python script.py -i N-files-to-be-selected keyword-for-tracefile-identification directory-of-dataset directory-to-place-selected-files

script = select_n_files.py
number of files to be selected = 4
keyword for identification of trace files = new
directory of traces dataset = cabspottingdata
directory to place selected files  = select_files/selected
123456789 = seed for random number generator
"""



import sys, os, os.path, random, shutil

def main():
    
    N = int(sys.argv[2])
    trace_files_keyword = sys.argv[3]
    traces_directory = sys.argv[4]
    selected_traces_directory = sys.argv[5]
    rand_seed = sys.argv[6]
    
    random.seed(rand_seed)
    
    if not os.path.exists(traces_directory):
        print(traces_directory, "directory donot exists")
        quit()
        
    files_list = os.listdir(traces_directory)
    
    if not os.path.exists(selected_traces_directory):
        os.makedirs(selected_traces_directory)
    else:
        selected = os.listdir(selected_traces_directory)
        for each in selected:
            os.remove(selected_traces_directory + "/" + each)
            
    i = 0
    trace_files_name_list = []
    
    for each in files_list:
        if trace_files_keyword in each:
            trace_files_name_list.append(each)
    
    if len(trace_files_name_list) < N:
        print("Number of traces to be selected are more than the traces in directory")
        print("Number of traces in directory = ", len(trace_files_name_list))
        print("Number of traces to be selected = ", N)
        quit()
    
    print("Selected files :")
    while i < N:
        rand = random.randint(0,len(trace_files_name_list)-1)
        trace_file = trace_files_name_list[rand]
        trace_files_name_list.remove(trace_file)
        trace_file = traces_directory + "/" + trace_file
        print(i, trace_file)
        shutil.copy(trace_file, selected_traces_directory)
        i += 1

if __name__ == "__main__":
    main()