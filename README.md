# TRAILS - A Trace-Based Probabilistic Mobility Model

Modeling mobility is a key aspect when simulating different types of networks and a large number of various models has emerged in the last years. They are typically either trace-based, where GPS recordings are re-run in simulation, or synthetic models, which describe mobility with formal methods. Both concepts have advantages and disadvantages. For example, trace-based models are very in flexible in terms of simulation scenarios but have realistic behaviour, while synthetic models are very  flexible, but lack realism. To overcome these these issues, a mobility model by the name of TRAILS (TRAce-based ProbabILiStic Mobility Model) has been developed. This model spans the gap between both families and combines their advantages into a single model. This repository contains an implementation of this mobility model in OMNeT++, a C++ based discrete event simulator.

The immediately following section is the procedure for anyone who wishes to get TRAILS up and running after. 

TRAILS Setup Procedure
----------------------

TRAILS is uses the simulation environment of the OMNeT++ simulator and the scripts use Python and Bash. It is only meant for Linux or MacOS environments. The procedure for setting up and running TRAILS is given below.

- Open a console (terminal) 
- Install and setup OMNeT++ v5.2.1 or higher (use OMNeT++ installation Guide)
- Install `Python 2.7`
- Clone this repository: `git clone -b https://github.com/ComNets-Bremen/TRAILS`
- Change directory to `TRAILS`
- Download and untar the latest version of `OMNeT++ INET` from `https://inet.omnetpp.org/Download.html`
- Build INET: run `./build-INET.sh`
- Build mobility model testing environment (MobilityModelCheck): `./build-MobilityModelCheck.sh`
- Build TRAILS database and BonnMotion trace file from SFO Taxi Cab traces: run `cd ./Traces/SFO-Taxi-Cabs ; ./prepare-traces.sh ; cd ../../`
- Simulate mobility for 4 mobility models (Random Waypoint, SWIM, BonnMotion, TRAILS): run `./run-4-mobility-models.sh`
- Extract results from simulation output files in `MobilityModelCheck/results`



Creating TRAILS Database from SFO Taxi Cab Traces
-------------------------------------------------

Different TRAILS databased can be created with other parameters. Change the parameters given in the script `./prepare-traces.sh` in `./Traces/SFO-Taxi-Cabs` to suit requirements. 


Collecting and Creating Results from Simulation Output Files 
------------------------------------------------------------

There are a set of codes in the log files that gives details about the number of contacts made during a simulations. The following list gives these codes and their meanings.

|  Code    |             Description                |
|  ---     |                 ---                    |
| ANS      | accumulated neighbourhood size         | 
| TNRT     | total neighbourhood reporting times    |
| ACD      | accumulated contact durations          |
| TNC      | total number of contacts up to now     |

Statistics computed from these coded values are as follows.

- `Average Neighbourhood Size = ANS / TNRT`
- `Average Contact Duration = ACD / TNC`
- `Total Number of Contacts = TNC`

Always use the last values listed in the logs. To get the last values, run the following bash commands on a terminal.

``` 
grep "TNRT\|ANS\|TNC\|ACD" General-0-20180518-23:16:11-28993-log2.txt | tail
```

Replace the `General-0-20180518-23:16:11-28993-log2.txt` file with the log file in in your simulation folder.

A python script has been written to collect the above mentioned results (`results-collect.py`) and it is available at `Scripts/Results-Collect`.

Questions or Comments
---------------------

If you have any questions, comments or suggestions, please write to us using any of the e-mail adresses below.

  - Anna Förster (anna.foerster@comnets.uni-bremen.de)
  - Anas bin Muslim (anas1@uni-bremen.de)
  - Asanga Udugama (adu@comnets.uni-bremen.de)
  