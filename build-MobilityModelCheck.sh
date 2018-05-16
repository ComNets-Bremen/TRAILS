#!/bin/bash

cd MobilityModelCheck
make clean
INET_PATH=$(pwd)/../inet/src/
opp_makemake -r --deep -I$INET_PATH -L$INET_PATH -lINET --mode release -f
make
cd ..

