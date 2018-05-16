#!/bin/bash

# INI_FILE=./ini-files/omnetpp-n50-s123456789-rwp.ini
TEMP_INI_FILE=$1
INI_FILE=$(realpath $TEMP_INI_FILE)
BASE_DIR=$(basename $INI_FILE)
RESULTS_DIR=./MobilityModelCheck/results/
RESULTS_DIR2=$(realpath $RESULTS_DIR)
RESULTS_DIR3="$RESULTS_DIR2/$(date +"%Y-%m-%d_%H-%M-%S")_${BASE_DIR%.*}"

mkdir $RESULTS_DIR3

cd MobilityModelCheck
# rm /home/adu/memlog-trails-simu.log
cp $INI_FILE $RESULTS_DIR3
START_TIME=$(date +%s)
./MobilityModelCheck -u Cmdenv -f $INI_FILE -n ./:../inet/src/ -l INET --result-dir=$RESULTS_DIR3
END_TIME=$(date +%s)
TIME_DIFF=$((END_TIME-START_TIME))
echo "Simulation Duration: ${TIME_DIFF} seconds" >> $RESULTS_DIR3/sim-time.txt
# cp /home/adu/memlog-trails-simu.log $RESULTS_DIR3/
cd ..

