
import inet.mobility.contract.IMobility;

module MobileNode
{
    parameters:
        @networkNode();

        // unique node identifier
        int nodeID;
		
        // mobility model used
        string mobilityType = default("StationaryMobility");
		
        // icon
        @display("i=device/palm2;bgb=250,340");

    submodules:

         // wifi adhoc interface
        wirelessIfc: WirelessInterface {
            nodeIndex = nodeID;
        }

        // mobility
        mobility: <mobilityType> like IMobility;
}
