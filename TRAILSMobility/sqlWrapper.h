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
* The C++ include file for the database helper functions used by TRAILS Mobility Model
* in OMNeT++.
*
* @author : Anas bin Muslim (anas1@uni-bremen.de)
*
*/

#ifndef INET_MOBILITY_SINGLE_SQLWRAPPER_H_
#define INET_MOBILITY_SINGLE_SQLWRAPPER_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>
#include <vector>
#include "inet/common/INETDefs.h"
#include "inet/mobility/base/LineSegmentsMobilityBase.h"

namespace inet {

class TRAILSMobility;

class sqlWrapper {

private:
    static sqlite3 *DB;

    static int rc;
    static int timeFirstID;
    static int timeLastID;

    static char *zErrMsg;
    static std::string sql;

    static std::vector <int> IDs;
    static std::vector <float> times;
    static std::vector <int> targetPOIs;

public:
    static bool open;

public:
    /* Initialize a connection to SQLite database carrying mobility map information */
    static int openDB();

    /* *******************************************************************
        SPECIFIED FUNCTIONS: USE ONLY FOR Probabilistic TRACE BASED MODEL
       ******************************************************************* */

    /* Retrieves ID of POI desired by a node */
    static int getPOIID(char * sql, void * pntr);
    static int getPOIID_callback(void * pntr, int count, char ** data, char ** colName);

    /* Retrieves a point on edge desired by a node based on index point and ID */
    static int getEdge(void * pntr, int src, int dest, int idx);
    static int getEdge_callback(void* unused, int count, char ** data, char ** colName);

    /* Retrieves the start and ending ID of edge, based on which each edge
       is identified. This helps in deciding which path to be taken by node */
    static int getFirstLastID(void * pntr, int src, int dest);
    static int getEdgeID_callback(void * unused, int count, char ** data, char ** colName);

    /* Count the number of POIS identified in mobility map */
    static int countPOIS(void * pntr);
    static int countPOIS_callback(void* pntr, int count, char ** data, char ** colName);

    /* Retrieves the initial location of a node */
    static int getInitialPOI(char * sql, void * pntr);
    static int initialPOI_callback(void * pntr, int count, char ** data, char ** colName);

    /* Retrieves all accessible POIs from the given POI and returns a random POI as destination, from the list */
    static int getDestination(char * query, void * pntr);
    static int getAllDestinations_callback(void * pntr, int count, char ** data, char ** colName);
    static int getDestinationPOI_callback(void * pntr, int count, char ** data, char ** colName);


    /* Gather all the waiting times, at given position, from Database, and return a random wait time */
    static int getWaitTime(int dest, void * pntr);
    static int getWaitTime_callback(void*pntr, int count, char ** data, char ** colName);

    /* ******************************************************************* */


    // PUBLIC FUNCTION: CAN BE USED TO EXECUTE ANY QUERY
    // Callback function must be modified according to query
    static int execQuery(void* module, char * sql);
    static int queryCallback(void * unused, int count, char ** data, char ** colName);

    sqlWrapper();

    virtual ~sqlWrapper();
};

} /* namespace inet */

#endif /* INET_MOBILITY_SINGLE_SQLWRAPPER_H_ */
