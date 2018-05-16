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
 * The C++ implementation file for the database helper functions used by TRAILS Mobility Model
 * in OMNeT++.
 *
 * @author : Anas bin Muslim (anas1@uni-bremen.de)
 *
 */

#include "TRAILSMobility.h"
#include "inet/mobility/single/sqlWrapper.h"

namespace inet {

sqlite3* sqlWrapper::DB;

bool sqlWrapper::open = false;

int sqlWrapper::rc;
int sqlWrapper::timeFirstID = 0;
int sqlWrapper::timeLastID = 0;

char * sqlWrapper::zErrMsg;
std::string sqlWrapper::sql;

std::vector <int> sqlWrapper::IDs;
std::vector <float> sqlWrapper::times;

std::vector <int> sqlWrapper::targetPOIs;


sqlWrapper::sqlWrapper() {
    // TODO Auto-generated constructor stub

}

int sqlWrapper::openDB(){

    EV<<"ESTABILISHING CONNECTION TO DATABASE ... "<<std::endl;

    zErrMsg = 0;
    rc = sqlite3_open("map.db", &DB);

    if(rc){
        EV_FATAL<<"Cannot open database :: Error message :: "<<sqlite3_errmsg(DB)<<std::endl;
    }
    else{
        open = true;
        EV<<"CONNECTION ESTABILISHED !"<<std::endl;
    }

    return rc;
}

int sqlWrapper::getPOIID(char * sql, void * pntr){
    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;
    rc = sqlite3_exec(DB, sql, getPOIID_callback, (void*) pntr, &zErrMsg);
    return rc;
}

int sqlWrapper::getPOIID_callback(void * pntr, int count, char ** data, char ** colName){
    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;
    m->tempPOIID = atoi(data[0]);
    return 0;
}

int sqlWrapper::getEdge(void * pntr, int src, int dest, int idx){

    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;

    sql = "SELECT * FROM EDGES WHERE START_POI_ID = " + std::to_string(src)\
            + " and END_POI_ID = " + std::to_string(dest) + " and ID = " + std::to_string(idx);

    rc = sqlite3_exec(DB, sql.c_str(), getEdge_callback, (void*) pntr, &zErrMsg);

    return rc;
}

int sqlWrapper::getEdge_callback(void * unused, int count, char** data, char ** colName){

    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) unused;

    m->target.x = atoi(data[count-3]);
    m->target.y = atoi(data[count-2]);
    m->target.z = atoi(data[count-1]);

    // Get the movement speed too, if mobility model is instructed to
    if (m->speedFromMap == true){
        if(atoi(data[count-5]) <= 0 || atoi(data[count-5]) > 100)
            m->speedAtEdge = 1;
        else
            m->speedAtEdge = atoi(data[count-5]);
    }

    return 0;
}

int sqlWrapper::countPOIS(void * pntr){

    std::string stm = "SELECT COUNT(*) from POIS";
    rc = sqlite3_exec(DB, stm.c_str(), countPOIS_callback, (void*) pntr, &zErrMsg);

    return rc;
}

int sqlWrapper::countPOIS_callback(void * pntr, int count, char ** data, char ** colName){

    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;
    m->noOfPOIS = atoi(data[0]);

    return 0;
}

int sqlWrapper::getInitialPOI(char * sql, void * pntr){

    rc = sqlite3_exec(DB, sql, initialPOI_callback, (void*) pntr, &zErrMsg);

    return rc;
}

int sqlWrapper::initialPOI_callback(void * pntr, int count, char ** data, char ** colName){

    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;
    m->tempPOIID = atoi(data[0]);
    m->previousPOI.x = atoi(data[1]);
    m->previousPOI.y = atoi(data[2]);
    m->previousPOI.z = atoi(data[3]);

    return 0;
}

int sqlWrapper::getDestination(char * query, void * pntr){

    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;
    targetPOIs.clear();

    rc = sqlite3_exec(DB, query, getAllDestinations_callback, (void*) pntr, &zErrMsg);
    int random;
    if (targetPOIs.size() > 0){
        random = rand() % targetPOIs.size();
        m->tempPOIID = targetPOIs[random];

        sql = "SELECT PX, PY, PZ FROM POIS WHERE ID = " + std::to_string(targetPOIs[random]);
        rc = sqlite3_exec(DB, sql.c_str(), getDestinationPOI_callback, (void*) pntr, &zErrMsg);
    }
    else{
        m->tempPOIID = -1;
    }


    return rc;
}

int sqlWrapper::getAllDestinations_callback(void * pntr, int count, char ** data, char ** colName){

    for (int i=0;i<count;i++){
        targetPOIs.push_back(atoi(data[i]));
    }

    return 0;
}

int sqlWrapper::getDestinationPOI_callback(void * pntr, int count, char ** data, char ** colName){
    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;

    m->finalPOI.x = atoi(data[0]);
    m->finalPOI.y = atoi(data[1]);
    m->finalPOI.z = atoi(data[2]);

    return 0;
}


int sqlWrapper::getFirstLastID(void * pntr, int src, int dest){
    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;

    std::vector <int> startToEnd;
    std::vector < std::vector <int> > edgesID;
    IDs.clear();

    sql = "SELECT ID FROM EDGES WHERE START_POI_ID = " + std::to_string(src) + " and END_POI_ID = " + std::to_string(dest);
    rc = sqlite3_exec(DB, sql.c_str(), getEdgeID_callback, (void*) pntr, &zErrMsg);

    // No edges found from source to destination
    if(IDs.size()<=0){
        m->lastID = m->firstID = 0;
        return rc;
    }

    // Edges found
    else{
        // For more than one edges; node must distinguish starting and ending IDs of each edge
        if (IDs.size() == (IDs[IDs.size()-1] - IDs[0] + 1)){
            m->firstID = IDs[0];
            m->lastID = IDs[IDs.size()-1];
        }
        else{
            if(IDs.size()>=0){
                m->firstID = 0;
                m->lastID = 0;
                startToEnd.push_back(IDs[0]);

                for (int i=0;i<IDs.size()-1;i++){
                    if(IDs[i+1]-IDs[i] == 1){
                        if(i+1 == int(IDs.size()-1)){
                            startToEnd.push_back(IDs[i+1]);
                            edgesID.push_back(startToEnd);
                        }
                    }
                    else if (IDs[i+1]-IDs[i] > 1){
                        startToEnd.push_back(IDs[i]);
                        edgesID.push_back(startToEnd);
                        startToEnd.clear();
                        startToEnd.push_back(IDs[i+1]);
                        if(i+1 == int(IDs.size()-1)){
                            startToEnd.push_back(IDs[i+1]);
                            edgesID.push_back(startToEnd);
                        }
                    }
                }

                int rndm = rand()%edgesID.size(); //intuniform(0,edgesID.size()-1);

                // Edge is chosen; Passing starting and ending ID of edge to node
                m->firstID = edgesID[rndm][0];
                m->lastID = edgesID[rndm][1];
            }
        }
    }

    return rc;
}

int sqlWrapper::getEdgeID_callback(void * unused, int count, char ** data, char ** colName){
    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) unused;

    for (int i=0;i<count;i++){
        IDs.push_back(atoi(data[i]));
    }

    return 0;
}

int sqlWrapper::getWaitTime(int dest, void * pntr){
    int count = 0;
    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) pntr;
    times.clear();

    sql = "SELECT TIME from POIS_WITH_TIME WHERE POI_ID = " + std::to_string(dest);

    rc = sqlite3_exec(DB, sql.c_str(), getWaitTime_callback, (void*) pntr, &zErrMsg);

    if(times.size()>=1){
        do{
            int rnd = rand()%times.size(); //intuniform(1,wait.size())-1;
            m->waitT = times[rnd];
            count++;
        }while (m->waitT <= 0 && count < 9);
    }
    else{
        m->waitT = 0;
    }
    return rc;
}

int sqlWrapper::getWaitTime_callback(void * pntr, int count, char ** data, char ** colName){
    times.push_back(atoi(data[0]));
    return 0;
}


int sqlWrapper::execQuery(void* module, char * sql){
    rc = sqlite3_exec(DB, sql, queryCallback, (void*) module, &zErrMsg);
    return rc;
}

int sqlWrapper::queryCallback(void * unused, int count, char ** data, char ** colName){
    TraceBasedProbabilisticMobility * m = (TraceBasedProbabilisticMobility *) unused;
    // Do something; Save something in m->whatever
    return 0;
}


sqlWrapper::~sqlWrapper() {
    // TODO Auto-generated destructor stub
    sqlite3_close(DB);
}

} /* namespace inet */
