#!/bin/bash

#---------------------------

./run-MobilityModelCheck.sh ./MobilityModelCheck/ini-files/omnetpp-n50-s123456789-rwp.ini
./run-MobilityModelCheck.sh ./MobilityModelCheck/ini-files/omnetpp-n50-s123456789-swim.ini
cp ./Traces/SFO-Taxi-Cabs/50-traces-seed-123456789/bonnmotion_50_cabs.movements ./MobilityModelCheck/
./run-MobilityModelCheck.sh ./MobilityModelCheck/ini-files/omnetpp-n50-s123456789-bonnmotion.ini
rm ./MobilityModelCheck/bonnmotion_50_cabs.movements
cp ./Traces/SFO-Taxi-Cabs/50-traces-seed-123456789/map.db ./MobilityModelCheck/
./run-MobilityModelCheck.sh ./MobilityModelCheck/ini-files/omnetpp-n50-s123456789-trails.ini
rm ./MobilityModelCheck/map.db

#----------------------------
