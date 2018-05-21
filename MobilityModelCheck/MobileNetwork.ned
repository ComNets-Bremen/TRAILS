
network MobileNetwork
{
   parameters:
        int numNodes = default(20);

    submodules:

        // nodes of the network
        node[numNodes]: MobileNode {
            nodeID = index;
        }
}
