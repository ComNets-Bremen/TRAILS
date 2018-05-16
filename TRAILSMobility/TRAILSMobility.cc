//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

/**
 * The C++ file of the TRAILS Mobility Model for the INET Framework
 * in OMNeT++.
 *
 * @author : Anas bin Muslim (anas1@uni-bremen.de)
 *
 */

#include "TraceBasedProbabilisticMobility.h"

namespace inet {

Define_Module(TRAILSMobility);

// Constructor
TRAILSMobility::TRAILSMobility() {
    nextMoveIsWait = false;
    destPOIReached = false;
    destPOISet = false;
    firstMove = true;
    movementOnEdge = false;
    edgeExists = true;
    indexPoint = 0;
    noOfPOIS = 0;
    waitT = 0;
}

void TRAILSMobility::initialize(int stage){
    LineSegmentsMobilityBase::initialize(stage);

    // Open the connection to mobility map database
    if (stage == 0){
        if (sqlWrapper::open == false){
            rc = sqlWrapper::openDB();
        }

        // Boolean indicating if mobility speed is to be used from actual trace files
        speedFromMap = par("speedFromMap");
    }
    else if (stage == 1){

        // Count the total POIs in mobility map
        rc = sqlWrapper::countPOIS(this);

        EV << simTime().dbl() << " :: " << this->getParentModule()->getFullName()<< " :: " << noOfPOIS << endl;

        //For logging destination points
        outfile.open("record.txt",std::ios::out|std::ios::app);
    }
    else if (stage == 2){

    }
}

void TRAILSMobility::setInitialPosition(){
    sql = "SELECT * from POIS where ID = " + std::to_string(intuniform(1,noOfPOIS));

    rc = sqlWrapper::getInitialPOI(strdup(sql.c_str()), this);

    startPOIID = tempPOIID;
    lastPosition = previousPOI;

    recordScalar("x", lastPosition.x);
    recordScalar("y", lastPosition.y);
    recordScalar("z", lastPosition.z);

    //std::cout << simTime().dbl() << " :: " << this->getParentModule()->getFullName()<< " :: Start POI ID " << startPOIID << " :: Coord " << lastPosition << endl;
}

void TRAILSMobility::setTargetPosition(){

    if (nextMoveIsWait) {
        simtime_t waitTime = 0;

        // If destination is reached; select a waiting time from pool for this location
        if (targetPosition == finalPOI){
            rc = sqlWrapper::getWaitTime(endPOIID, this);

            if (waitT > 0){
                waitTime = waitT;
            }
            else{
                waitTime = par("waitTime");
            }

            destPOISet = false;
            movementOnEdge = false;

            //For logging destination points
            outfile<< this->getParentModule()->getFullName() << " :: " << targetPosition.x << " " << targetPosition.y << " At dest" << endl;
        }
        else{
            //For logging destination points
            outfile<< this->getParentModule()->getFullName() << " :: " << targetPosition.x << " " << targetPosition.y << endl;
        }

        nextChange = simTime() + waitTime;

    }
    else {
        targetPosition = setTargetPoint(this);

        speed = par("speed");
        if(speedFromMap == true){
            if(speedAtEdge >= 1 && speedAtEdge < 10000){
                speed = speedAtEdge;
            }
        }

        double distance = lastPosition.distance(targetPosition);
        simtime_t travelTime = distance / speed;
        nextChange = simTime() + travelTime;
    }

    nextMoveIsWait = !nextMoveIsWait;
}

void TRAILSMobility::move(){
    LineSegmentsMobilityBase::move();
    raiseErrorIfOutside();
}

void TRAILSMobility::getEdge(TRAILSMobility * tbm){

    // If node has just decided the destination POI and haven't started to move on edge
    // It must decide which path to be taken before starting movement
    // There could be multiple edges from one POI to the other; choosing one of them

    if(movementOnEdge == false){
        rc = sqlWrapper::getFirstLastID((void*) tbm, startPOIID, endPOIID);

        // Edges has been decided; Now retrieving it from map for mobility
        if(firstID != 0 && lastID != 0){

            indexPoint = firstID;

            rc = sqlWrapper::getEdge((void*) tbm, startPOIID, endPOIID, indexPoint);

            movementOnEdge = true;
            indexPoint ++;
        }
        else{
            // For only 1 POI in map; select it as next destination; No other option available
            if (noOfPOIS < 2)
                target = previousPOI;
        }
    }

    // Node has already starting moving on the edge; continue to move until destination POI is reached
    else{

        if(indexPoint <= lastID){
            rc = sqlWrapper::getEdge((void*) tbm, startPOIID, endPOIID, indexPoint);
            indexPoint ++;
        }
        else{
            destPOISet = false;
            movementOnEdge = false;
        }

    }

}

Coord TRAILSMobility::setTargetPoint(TRAILSMobility * tbm){
    if (destPOISet == false){

        // Repeatedly retrieve a POI until standing point and destination POI are different
        //  do{
        // If node is already at POI, then select a next destination POI

        sql = "Select DISTINCT(END_POI_ID) from EDGES where START_POI_ID = " + std::to_string(startPOIID);
        //std::cout << simTime().dbl() << " :: " << this->getParentModule()->getFullName() << " :: start POI ID :: " << startPOIID << " :: final POI ID  " << endPOIID << " :: Coord " << finalPOI << endl;
        rc = sqlWrapper::getDestination(strdup(sql.c_str()), (void*) tbm);

        if(tempPOIID >= 0){
            endPOIID = tempPOIID;
        }
        else{
            endPOIID = startPOIID;
            finalPOI = previousPOI;
        }
        //std::cout << simTime().dbl() << " :: " << this->getParentModule()->getFullName() << " :: start POI ID :: " << startPOIID << " :: final POI ID  " << endPOIID << " :: Coord " << finalPOI << endl;

        /*if(noOfPOIS == 1){
            break;
        }*/

        //}while(finalPOI == previousPOI );

        // Destination POI has been selected; now get an edge to this POI
        destPOISet = true;

        getEdge(this);

        return target;
    }
    else {
        //Dest POI is set and edge is also retrieved; get the next point on edge (path) after indexPoint
        //and move there

        if (indexPoint <= lastID){
            getEdge(this);

            return target;
        }
        else if(indexPoint > lastID){
            destPOIReached = true;
            destPOISet = false;
            previousPOI = finalPOI;
            movementOnEdge = false;
            startPOIID = endPOIID;
            return finalPOI;
        }
    }
}

TRAILSMobility::~TRAILSMobility() {
    // TODO Auto-generated destructor stub
    outfile.close();
}

} /* namespace inet */
