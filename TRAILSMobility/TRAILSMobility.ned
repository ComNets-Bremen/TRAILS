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

//
// The NED file of the TRAILS Mobility Model for the INET Framework
// in OMNeT++.
//
// author : Anas bin Muslim (anas1@uni-bremen.de)
//
// Change History:
// Asanga Udugama (adu@comnets.uni-bremen.de)
// - name change
//

package inet.mobility.single;
import inet.mobility.base.MovingMobilityBase;

simple TRAILSMobility extends MovingMobilityBase{
    parameters:
        
        bool initFromDisplayString = default(true);
        bool speedFromMap = default(true);
        
        int usedRNG = default(0);
        
        double speed @unit(mps) = default(20mps);
        volatile double waitTime @unit(s) = default(uniform(0s,10s));
        
        @class (TRAILSMobility);
}
        