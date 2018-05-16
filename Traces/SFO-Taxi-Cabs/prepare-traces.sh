#!/usr/bin/env bash

# trace selection parameters
TRACE_NUM="50"
RANDOM_SEED="123456789"

# working folder
TRACE_CREATION_FOLDER="./${TRACE_NUM}-traces-seed-${RANDOM_SEED}"
mkdir "${TRACE_CREATION_FOLDER}"
cd "${TRACE_CREATION_FOLDER}"

# untaring parameters 
RAW_TRACE_FILE_ARCHIVE="../cabspottingdata.tar.gz"
RAW_TRACES_LOCATION="./cabspottingdata/"

# untar the SFO taxi cab traces original
echo "Untaring ${RAW_TRACE_FILE_ARCHIVE} file"
tar -xzf "${RAW_TRACE_FILE_ARCHIVE}"

# script paths
SCRIPT_PATH="../../../Scripts/SFO-Taxi-Cabs/"

# BonnMotion trace creation parameters
COORD_DIMENSIONS="2"

# Mobility database creation parameters
MIN_POI_DETECTION_TIME="600"
NUM_NEIGHBORS="75"
POI_RADIUS="30"
DIJKSTRA_STATUS="dijkstras=off"

# common parameters
RAW_SELECTED_TRACE_LOCATION="./${TRACE_NUM}-selected-traces/"
PROCESSED_TRACE_LOCATION="./${TRACE_NUM}-processed-traces/"
SELECT_PREFIX="new"

echo "" > ./trace-creation-output.txt
echo "Processing Traces" >> ./trace-creation-output.txt
echo "Parameters: " >> ./trace-creation-output.txt
echo "SCRIPT_PATH ${SCRIPT_PATH}" >> ./trace-creation-output.txt
echo "RAW_SELECTED_TRACE_LOCATION ${RAW_SELECTED_TRACE_LOCATION}" >> ./trace-creation-output.txt
echo "PROCESSED_TRACE_LOCATION ${PROCESSED_TRACE_LOCATION}" >> ./trace-creation-output.txt
echo "SELECT_PREFIX ${SELECT_PREFIX}" >> ./trace-creation-output.txt
echo "TRACE_NUM ${TRACE_NUM}" >> ./trace-creation-output.txt
echo "RAW_TRACE_LOCATION ${RAW_TRACES_LOCATION}" >> ./trace-creation-output.txt
echo "RANDOM_SEED ${RANDOM_SEED}" >> ./trace-creation-output.txt
echo "COORD_DIMENSIONS ${COORD_DIMENSIONS}" >> ./trace-creation-output.txt
echo "MIN_POI_DETECTION_TIME ${MIN_POI_DETECTION_TIME}" >> ./trace-creation-output.txt
echo "NUM_NEIGHBORS ${NUM_NEIGHBORS}" >> ./trace-creation-output.txt
echo "POI_RADIUS ${POI_RADIUS}" >> ./trace-creation-output.txt
echo "DIJKSTRA_STATUS ${DIJKSTRA_STATUS}" >> ./trace-creation-output.txt
echo "" >> ./trace-creation-output.txt

echo "Preparing traces for ${TRACE_NUM} nodes"

echo "Selecting trace files ..."
echo "Selecting trace files ..." >> ./trace-creation-output.txt
"$SCRIPT_PATH"/select_n_files.py -i $TRACE_NUM $SELECT_PREFIX $RAW_TRACES_LOCATION $RAW_SELECTED_TRACE_LOCATION $RANDOM_SEED >> ./trace-creation-output.txt

echo "Finding area and speed  ..."
echo "Finding area and speed  ..." >> ./trace-creation-output.txt
"$SCRIPT_PATH"/area_and_speed_stats.py -i $RAW_SELECTED_TRACE_LOCATION >> ./trace-creation-output.txt

echo "Creating BonnMotion mobility trace ..."
echo "Creating BonnMotion mobility trace ..." >> ./trace-creation-output.txt
"$SCRIPT_PATH"/create_bonnmotion_trace_file.py -i $RAW_SELECTED_TRACE_LOCATION 2 $COORD_DIMENSIONS >> ./trace-creation-output.txt

echo "Convert to cartesian format ..."
echo "Convert to cartesian format ..." >> ./trace-creation-output.txt
"$SCRIPT_PATH"/convert-to-cart.py -i $RAW_SELECTED_TRACE_LOCATION $PROCESSED_TRACE_LOCATION $SELECT_PREFIX >> ./trace-creation-output.txt

echo "Create database for mobility ..."
echo "Create database for mobility ..." >> ./trace-creation-output.txt
"$SCRIPT_PATH"/traces_processing.py -i $PROCESSED_TRACE_LOCATION $MIN_POI_DETECTION_TIME $NUM_NEIGHBORS $POI_RADIUS $DIJKSTRA_STATUS >> ./trace-creation-output.txt

echo "Completed" 
echo "Completed" >> ./trace-creation-output.txt
echo ""

echo "Check the ./trace-creation-output.txt for all the trace creation script output"
echo ""
