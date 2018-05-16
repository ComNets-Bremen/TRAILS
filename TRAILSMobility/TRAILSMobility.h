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
* The C++ include file of the TRAILS Mobility Model for the INET Framework
* in OMNeT++.
*
* @author : Anas bin Muslim (anas1@uni-bremen.de)
*
*/

#ifndef INET_MOBILITY_SINGLE_TRAILSMOBILITY_H_
#define INET_MOBILITY_SINGLE_TRAILSMOBILITY_H_

#include "inet/mobility/single/sqlWrapper.h"
#include <fstream>


namespace inet {

class TRAILSMobility : public LineSegmentsMobilityBase {
protected:

    std::ofstream outfile;

    bool nextMoveIsWait;
    bool destPOIReached;
    bool destPOISet;
    bool movementOnEdge;
    bool firstMove;

    int rc;
    int indexPoint;
    int startPOIID;
    int endPOIID;

    double speed;

    std::string sql;

public:
    bool speedFromMap;
    bool edgeExists;

    int firstID, lastID;
    int noOfPOIS, noNodes;
    int speedAtEdge;
    int waitT;
    int tempPOIID;

    char * edge;

    Coord previousPOI;
    Coord target;
    Coord finalPOI;

protected:
    virtual int numInitStages() const override { return NUM_INIT_STAGES; }

    virtual void initialize(int stage) override;

    virtual void setInitialPosition() override;

    virtual void setTargetPosition() override;

    virtual void move() override;

    /* Gets the edge (path) from source to destination POI */
    virtual void getEdge(TRAILSMobility *);

    /* Sets the next target point to move to */
    virtual Coord setTargetPoint(TRAILSMobility *);

public:
    TRAILSMobility();
    virtual ~TRAILSMobility();
};

} /* namespace inet */

#endif /* INET_MOBILITY_SINGLE_TRAILSMOBILITY_H_ */
