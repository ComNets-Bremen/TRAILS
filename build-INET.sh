#!/bin/bash

echo "Make sure INET is downloaded and untared here"
echo "Get INET from https://inet.omnetpp.org/Download.html"

cd inet
cp ../SWIMMobility/* src/inet/mobility/single/
cp ../TRAILSMobility/* src/inet/mobility/single/
make makefiles
make MODE=release
cd ..
