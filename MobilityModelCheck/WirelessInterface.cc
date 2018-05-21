
#include "WirelessInterface.h"

Define_Module(WirelessInterface);

void WirelessInterface::initialize(int stage)
{
    if (stage == 0) {

        nodeIndex = par("nodeIndex");
        wirelessRange = par("wirelessRange");

        ownName = getParentModule()->getFullName();
        for (cModule::SubmoduleIterator it(getParentModule()); !it.end(); ++it) {
            ownMobilityModule = dynamic_cast<inet::IMobility*>(*it);
            if (ownMobilityModule != NULL) {
                break;
            }
        }

        if (nodeIndex == 1) {
            numContacts = 0;
            sumContactDurations = 0.0;
            sumNeighbourhoodSize = 0;
            totNeighbourhoodReportingTimes = 0;
        }

    } else if (stage == 1) {

        for (int id = 0; id <= getSimulation()->getLastComponentId(); id++) {
            cModule *unknownModule = getSimulation()->getModule(id);
            if (unknownModule == NULL) {
                continue;
            }
            inet::IMobility *mobilityModule = dynamic_cast<inet::IMobility*>(unknownModule);
            if (mobilityModule == NULL) {
                continue;
            }

            if (strstr(unknownModule->getParentModule()->getFullName(), ownName.c_str()) != NULL) {
                continue;
            }

            NodeInfo *nodeInfo = new NodeInfo();
            nodeInfo->nodeMobilityModule = mobilityModule;
            nodeInfo->nodeName = unknownModule->getParentModule()->getFullName();
            nodeInfo->contactStartTime = 0.0;
            nodeInfo->contactStarted = true;
            allNodeInfoList.push_back(nodeInfo);

        }

        cMessage *checkNeighboursEvent = new cMessage("Check Neighbours Event");
        scheduleAt(simTime() + 1.0, checkNeighboursEvent);
    }

}

int WirelessInterface::numInitStages() const
{
    return 2;
}

void WirelessInterface::handleMessage(cMessage *msg)
{
    if (msg->isSelfMessage()) {

        // init the new list
        while (newNeighbourNodeInfoList.size() > 0) {
            list<NodeInfo*>::iterator iteratorNeighbourNodeInfo = newNeighbourNodeInfoList.begin();
            NodeInfo *nodeInfo = *iteratorNeighbourNodeInfo;
            newNeighbourNodeInfoList.remove(nodeInfo);
        }

        // get current position of self
        inet::Coord ownCoord = ownMobilityModule->getCurrentPosition();

        // make the new neighbour list
        list<NodeInfo*>::iterator iteratorNeighbourNodeInfo = allNodeInfoList.begin();
        while (iteratorNeighbourNodeInfo != allNodeInfoList.end()) {
            NodeInfo *nodeInfo = *iteratorNeighbourNodeInfo;
            inet::Coord neighCoord = nodeInfo->nodeMobilityModule->getCurrentPosition();

            double l = ((neighCoord.x - ownCoord.x) * (neighCoord.x - ownCoord.x))
                + ((neighCoord.y - ownCoord.y) * (neighCoord.y - ownCoord.y));
            double r = wirelessRange * wirelessRange;
            if (l <= r) {
                newNeighbourNodeInfoList.push_back(nodeInfo);
            }
            iteratorNeighbourNodeInfo++;
        }
	if (newNeighbourNodeInfoList.size() > 0) {
	    sumNeighbourhoodSize += newNeighbourNodeInfoList.size();
            totNeighbourhoodReportingTimes++;
            // ANS = accumulated neighbourhood size
            // TNRT = total neighbourhood reporting times
            EV_INFO << " " << simTime() << " " << ownName << " ANS " << sumNeighbourhoodSize << " TNRT " << totNeighbourhoodReportingTimes << "\n";
        }


        // check and update left neighbours
        list<NodeInfo*>::iterator iteratorOldNeighbourNodeInfo = currentNeighbourNodeInfoList.begin();
        while (iteratorOldNeighbourNodeInfo != currentNeighbourNodeInfoList.end()) {
            NodeInfo *oldNodeInfo = *iteratorOldNeighbourNodeInfo;

            bool found = false;
            list<NodeInfo*>::iterator iteratorNewNeighbourNodeInfo = newNeighbourNodeInfoList.begin();
            while (iteratorNewNeighbourNodeInfo != newNeighbourNodeInfoList.end()) {
                NodeInfo *newNodeInfo = *iteratorNewNeighbourNodeInfo;

                if (strstr(oldNodeInfo->nodeName.c_str(), newNodeInfo->nodeName.c_str()) != NULL) {
                    found = true;
                    break;
                }
                iteratorNewNeighbourNodeInfo++;
            }

            if (!found) {
                double contactDuration = simTime().dbl() - oldNodeInfo->contactStartTime;
                EV_DEBUG << " " << ownName << " says: Contact with " << oldNodeInfo->nodeName << " ended at " << simTime().dbl() << " seconds - Contact duration was " << contactDuration << " seconds \n";
                oldNodeInfo->contactStarted = false;
                oldNodeInfo->contactStartTime = 0.0;
                currentNeighbourNodeInfoList.remove(oldNodeInfo);

                if (contactDuration > 0.0) {
                    sumContactDurations += contactDuration;
                    numContacts++;
                    // ACD = accumilated contact durations
                    // TNC = total number of contacts upto now
                    EV_INFO << " " << simTime() << " " << ownName << " ACD " << sumContactDurations << " TNC " << numContacts << "\n";
                }
            }

            if (!found) {
                iteratorOldNeighbourNodeInfo = currentNeighbourNodeInfoList.begin();
            } else {
                iteratorOldNeighbourNodeInfo++;
            }
        }

        // check and update new neighbours
        list<NodeInfo*>::iterator iteratorNewNeighbourNodeInfo = newNeighbourNodeInfoList.begin();
        while (iteratorNewNeighbourNodeInfo != newNeighbourNodeInfoList.end()) {
            NodeInfo *newNodeInfo = *iteratorNewNeighbourNodeInfo;

            bool found = false;
            list<NodeInfo*>::iterator iteratorOldNeighbourNodeInfo = currentNeighbourNodeInfoList.begin();
            while (iteratorOldNeighbourNodeInfo != currentNeighbourNodeInfoList.end()) {
                NodeInfo *oldNodeInfo = *iteratorOldNeighbourNodeInfo;

                if (strstr(newNodeInfo->nodeName.c_str(), oldNodeInfo->nodeName.c_str()) != NULL) {
                    found = true;
                    break;
                }
                iteratorOldNeighbourNodeInfo++;
            }

            if (!found) {
                EV_DEBUG << ownName << " says: Contact with " << newNodeInfo->nodeName << " started at " << simTime().dbl() << " seconds \n";
                newNodeInfo->contactStarted = true;
                newNodeInfo->contactStartTime = simTime().dbl();
                currentNeighbourNodeInfoList.push_back(newNodeInfo);
            }
            iteratorNewNeighbourNodeInfo++;
        }

        scheduleAt(simTime() + 1.0, msg);
    }
}
