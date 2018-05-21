
#ifndef __MOBILITYMODELCHECK_WIRELESSINTERFACE_H_
#define __MOBILITYMODELCHECK_WIRELESSINTERFACE_H_

#include "inet/mobility/contract/IMobility.h"

#include <omnetpp.h>

using namespace omnetpp;
using namespace std;

int numContacts = 0;
double sumContactDurations = 0.0;
int sumNeighbourhoodSize = 0;
int totNeighbourhoodReportingTimes = 0;

class WirelessInterface : public cSimpleModule
{
  protected:
    virtual void initialize(int stage);
    virtual int numInitStages() const;
    virtual void handleMessage(cMessage *msg);

  private:
    typedef struct nodeinfo {
        string nodeName;
        inet::IMobility *nodeMobilityModule;
        bool contactStarted;
        double contactStartTime;
    } NodeInfo;

    int nodeIndex;
    double wirelessRange;
    string ownName;
    inet::IMobility *ownMobilityModule;
    list<NodeInfo*> allNodeInfoList;
    list<NodeInfo*> currentNeighbourNodeInfoList;
    list<NodeInfo*> newNeighbourNodeInfoList;
};

#endif
