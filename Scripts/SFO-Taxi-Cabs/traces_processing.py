#!/usr/bin/env python2.7

import sys, os, math, sqlite3, os.path
from __main__ import *

''' Function to find minimum values present in the columns
     of "cartesian data" to normalize the data
    Returnable Value: Minimum values in cartesian coordinates & timestamp'''
def find_minimum(data):

    x_coord = []
    y_coord = []
    z_coord = []
    s_time = []

    for each in data:
        x_coord.append(each[0])
        y_coord.append(each[1])
        z_coord.append(each[2])
        s_time.append(each[3])

    return (min(x_coord), min(y_coord), min(z_coord), min(s_time))

''' Function to find the Points of Interests
    from the given data. Given data have the
    neighbors of each point and multiple
    close points indicated as potential POIs
    Returnable value: Identified POI's List'''
def reachable_points(neighborhood_data):
                                          # 'neighborhood_data' contains info of neighbors of each point
    temp_data = []                        # Stores the data in tuple form after conversion from strings
    temp_poi = []                         # Stores the POIs to be returned
    pois = []                             # Stores the extended list of POIs
    j = 0
    i = 1
    nextPointIsPOI = False

    # Convert data from strings to a meaningful form
    for each in neighborhood_data:
        temp_tup = tuple(each.strip().split())
        temp_data.append(temp_tup)

    # Find if the point is considered POI;
    # if yes, then add it to pois list
    for each in temp_data:
        length = len(each)
        if nextPointIsPOI == False:
            if (int(each[length-1].replace(")", "").replace(",", "")) == 1):
                nextPointIsPOI = True
            else:
                nextPointIsPOI = False
        else:
            pois.append(each)
            if (int(each[length-1].replace(")", "").replace(",", "")) == 1):
                nextPointIsPOI = True
            else:
                nextPointIsPOI = False

    x = float(pois[0][0].replace("(", "").replace(",", ""))
    y = float(pois[0][1].replace(",", ""))
    z = float(pois[0][2].replace(",", ""))
    t = float(pois[0][3].replace(")", "").replace(",", ""))
    temp_poi.append((x,y,z,t))

    while i < len(pois):
        j = 0
        count = 0
        x = float(pois[i][0].replace("(", "").replace(",", ""))
        y = float(pois[i][1].replace(",", ""))
        z = float(pois[i][2].replace(",", ""))
        t = float(pois[i][3].replace(")", "").replace(",", ""))

        if not ((x,y,z,t) in temp_poi):                                    # Check if POI is in list to be returned i.e. temp_poi
            while j < len(temp_poi):                                       # If not then check if it is in area of another POI
                dist = math.hypot(x-temp_poi[j][0], y-temp_poi[j][1])
                if dist < eps:                                             # If its in area of another POI then remove this point as POI
                    count += 1
                j = j + 1

        if count == 0:                                                     # If Desired poi is not inside another pois area;
            temp_poi.append((x,y,z,t))                                     # add it to the list
        i = i + 1
    return temp_poi


''' Function to find the index of min distance for vertices
    This function is used for Djikstra's algorithm
    Returnable Value: Index of POI with minimum distance from given POI'''
def minimum_Distance(dist_from_vertex, shortest_path_set, leng):
    min_dist = float('inf')
    for v in range(leng):
        if shortest_path_set[v] == False and dist_from_vertex[v][1] <= min_dist:
            min_dist, min_idx = dist_from_vertex[v][1], v
    return min_idx

''' Function which processes the timestamps & implements
    ASTIPI Algorithm to find the potential POIs from list
    Result: Identified POIs with waiting times & Output file with same data'''
def find_POIs(data_tup):

    global mintime                       # in seconds. Min Time, for a point to be considered as POI, if spent there
    global k                             # No of neighboring points to be checked for a point to be POI
    global eps                           # Considered radius of a Point of Interest
    global poi_all
    global data_all
    global pois_with_time

    edges = []

    # - Calculate the time difference between consecutive two points
    # - Used to find the POIs; time periods greater than minimum time indicates a POI
    i = 0
    while i < len(data_tup):
        temp_time = data_tup[i][3]
        x1 = data_tup[i][0]
        y1 = data_tup[i][1]
        while(i+1 < len(data_tup)):
            x2 = data_tup[i+1][0]
            y2 = data_tup[i+1][1]
            dist = math.hypot(x2-x1, y2-y1)
            if (dist < eps):         # for distance b/w 2 pts < eps meters, consider pts as same location
                data_tup[i] = data_tup[i] + (0,)
                i = i+1
            else:                    # else wise consider them seperate points
                data_tup[i] = data_tup[i] + (data_tup[i][3] - temp_time,)
                break
        if (i == len(data_tup)-1):
            data_tup[i] = data_tup[i] + (0,)
        i = i+1
    data = data_tup


    #                 ASTIPI ALGORITHM
    # Find the neighborhood of each point by iterating over its
    # next 'k' points. If next 'k' points are within its eps radius &
    # time difference b/w this and last point in eps radius is more than mintime,
    # then it is a POI

    neighborhood = []
    last_neighbor_index = 0
    neighbors = 0

    i = 0
    for i, each in enumerate(data):
        k_calculated = 0
        neighbors = 0
        x_cand = data[i][0]
        y_cand = data[i][1]
        z_cand = data[i][2]
        time_cand = data[i][3]
        neighbor_tup = (x_cand, y_cand, z_cand, time_cand)
        j = last_neighbor_index + 1
        if j == i:
            j = j + 1
        while j<len(data) and k_calculated < k:
            x = data[j][0]
            y = data[j][1]
            z = data[j][2]
            distance = math.hypot(x-x_cand, y-y_cand)
            if distance > int(eps):
                k_calculated = k_calculated + 1
            elif distance < int(eps):
                time = data[j][3]
                last_neighbor_index = j
                neighbors = neighbors + 1
                temp_tuple = (x,y,z,time)
                k_calculated = 0
                neighbor_tup = neighbor_tup + temp_tuple
            j = j + 1
        if neighbors > 0:
            time_diff = time - time_cand
        else:
            if last_neighbor_index <= i:
                last_neighbor_index = last_neighbor_index + 1
            if i+1 < len(data):
                time = data[i+1][3]
                time_diff = time - time_cand

        # Set the point as candidate POI by flagging it '1'
        if time_diff > mintime:
            neighbor_tup = neighbor_tup + (1,)
            neighborhood.append(str(neighbor_tup))
        # Just append the neighborhood of point (not a candidate POI)
        else:
            neighbor_tup = neighbor_tup + (0,)
            neighborhood.append(str(neighbor_tup))

    # Using the function find the Actual POIs from all candidates
    POIs = reachable_points(neighborhood)



    data_list = []
    poi_list = []
    edge = ()

    for each in data:
        x = each[0]
        y = each[1]
        z = each[2]
        time = each[3]
        t = (x,y,z,time)
        data_list.append(t)

    # A check to make sure that each line
    # contains single POI
    for each in POIs:
        poi_length = len(each)
        iterations = poi_length/4
        for i in range(0,iterations):
            x_poi = each[i*4 + 0]
            y_poi = each[i*4 + 1]
            z_poi = each[i*4 + 2]
            time_poi = each[i*4 + 3]
            poi_tup = (x_poi,y_poi,z_poi,time_poi)
            if poi_tup not in poi_list:
                poi_list.append(poi_tup)
                poi_all.append(poi_tup)

    # Append the times periods spent at each POI
    # at the end of that POI coordinates
    tp = ()
    i = 0
    j = 0
    start = False
    while i<len(poi_list):
        j = 0
        while j<len(data_list):
            d = math.hypot(poi_list[i][0]-data_list[j][0],poi_list[i][1]-data_list[j][1])
            if d <= eps:                                                # Get the first point inside POI radius
                t1 = data_list[j][3]                                    # Save the time stamp at this point
                start = True                                            # Iterate until the next point goes out of the POI
                j = j + 1                                               # Find the time difference between these two points
            else:
                t2 = data_list[j][3]
                if start == True:
                    t = t2-t1
                    tp = tp + (t,)                                      # Add this time period to the list of time periods
                    start = False                                       # spent at this POI
                j = j + 1
        if(len(tp) == 0):
            tp = tp + (0,)
        pois_with_time.append((poi_list[i][0],poi_list[i][1],poi_list[i][2]) + tp)     # Add the list of time period to the end of POI
        pois_with_time_all.append((poi_list[i][0],poi_list[i][1],poi_list[i][2]) + tp) # Add the list of time period to the end of POI
        tp = ()
        t1 = 0
        t2 = 0
        i = i + 1

    # Write all POIs to external file
    outfile = open ("pois.txt", 'a')
    for each in pois_with_time:
        i = 0
        while i < len(each):
            outfile.write(str(each[i])),
            outfile.write(' '),
            i = i + 1
        outfile.write('\n')
    outfile.close()

    print "*"*25

    print 'POIs Identified :: ', len(pois_with_time)


''' Function to identify the edges from Cartesian coordinates list.
    It iterates over points until a POI is found. Then it starts adding
    next points to the edge while iterating over them until a point
    is reached which is in the same POI or another POI.
    Output: Identified Edges list & output file with edges inside'''
def find_edges():

    global poi_all
    global data_all
    global edges

    ###########################################
    # For identification of edges (local usage)
    temp_poi = []
    temp_data = []

    for each in poi_all:
        tmp_poi = (each[0],each[1],each[2])
        temp_poi.append(tmp_poi)
    for each in data_all:
        tmp_data = (each[0],each[1],each[2])
        temp_data.append(tmp_data)
    ###########################################

    a = 0            # iterating counter for all points
    stop = False     # Stops the procedure of continuing an edge

    # Find the edges from each POI to other POIs
    # Edges are bidirectional

    while a < len(data_all):
        i = 0      # iterating counter for all POIs

        while i < len(poi_all) and a<len(data_all):
            if (math.hypot(data_all[a][0]-poi_all[i][0], data_all[a][1]-poi_all[i][1]) < eps):

                # Point is found which lies in a POI,
                # now edge will be started from here
                edge = poi_all[i]
                stop = strt = False
                distance = 0
                a += 1

                while (a<len(data_all)) and (math.hypot(data_all[a][0]-poi_all[i][0], data_all[a][1]-poi_all[i][1]) < eps):
                    if (data_all[a][0] == poi_all[i][0] and data_all[a][1] == poi_all[i][1] or strt):
                        strt = True
                        edge = edge +(data_all[a][0],data_all[a][1],data_all[a][2],data_all[a][3])
                    a += 1

                if(a>=len(data_all)):
                    break

                start_time = data_all[a][3]
                distance = distance + math.hypot(data_all[a][0]-data_all[a-1][0],data_all[a][1]-data_all[a-1][1])
                b = a + 1

                while b < len(data_all) and not stop:
                    j = 0

                    while j < len(poi_all) and not stop:
                        if math.hypot(data_all[b][0]-poi_all[j][0], data_all[b][1]-poi_all[j][1]) < eps and b<len(data_all):
                            # Edge has ended because a point is reached
                            # which is in same or another POI
                            travel_time = data_all[b][3] - start_time
                            while (b<len(data_all)) and (math.hypot(data_all[b][0]-poi_all[j][0], data_all[b][1]-poi_all[j][1]) < eps and not (data_all[a][0] == poi_all[i][0] and data_all[a][1] == poi_all[i][1])):
                                edge = edge + (data_all[b][0],data_all[b][1],data_all[b][2],data_all[b][3])
                                b += 1

                            if travel_time < 0:
                                travel_time *= -1
                            if distance < 0:
                                distance *= -1
                            elif distance == 0:
                                distance = math.hypot(poi_all[j][0]-poi_all[i][0],poi_all[j][1]-poi_all[i][1])

                            # At the end of edge, speed & length of edge is also added
                            edge = edge + poi_all[j] + (distance/travel_time, distance,)

                            # Direct jumps from one POI to another are not included as edges
                            # These occur when more than one GPS files are considered
                            if(len(edge) > 10):
                                edges.append(edge)
                            a = b - 2
                            stop = True

                        j += 1

                    if (b<len(data_all)):
                        edge = edge + (data_all[b][0],data_all[b][1],data_all[b][2],data_all[b][3])
                        distance = distance + math.hypot(data_all[b][0]-data_all[b-1][0],data_all[b][1]-data_all[b-1][1])
                    b += 1
            i += 1
        a += 1

    print 'No of Edges found :: ', len(edges)

    # Write all edges to an external file
    outfile = open ("edges.txt", 'w')
    for each in edges:
        i = 0
        while i < len(each):
            outfile.write(str(each[i])),
            outfile.write(' '),
            i = i + 1
        outfile.write('\n')
    outfile.close()

''' This Function
    1. Creates the database
    2. Implements Dijkstra's algorithm to find all possible paths
    3. Inserts POI and Edges information in database
    Output: Mobility Map Database'''
def database_functions():

    ########### DATABASE CREATION #########

    print "*"*25
    print "DB connected and opened"

    global conn
    global pois_with_time
    global dijkstras_switch

                                                                        # Table 'POIS' contains all the points of interests of the map
    conn.execute('''CREATE TABLE IF NOT EXISTS POIS
                 (ID INT             NOT NULL,
                  PX FLOAT            NOT NULL,
                  PY FLOAT            NOT NULL,
                  PZ FLOAT            NOT NULL,
                  PRIMARY KEY(ID));''')

    print 'POIS                 table    created'
                                                                        # Table 'POIS_WITH_TIME' contains the points of interests
                                                                        # along with the time periods that were spent in its vicinity
    conn.execute(''' CREATE TABLE IF NOT EXISTS POIS_WITH_TIME
                 (ID INT    PRIMARY KEY     NOT NULL,
                  POI_ID INT           NOT NULL,
                  TIME INT                     );''')

    print 'POIS_WITH_TIME       table    created'
                                                                        # Table 'EDGES_IDENTIFIER' contains the starting point and
                                                                        # ending points of each edge
    """conn.execute(''' CREATE TABLE IF NOT EXISTS EDGES_IDENTIFIER
                (START_POI_ID INT  NOT NULL,
                 END_POI_ID INT    NOT NULL);''')

    print 'EDGES_IDENTIFIER        table    created' """

                                                                        # Table 'EDGES' contains all the points of edges with the
                                                                        # starting point, ending point, speed & length of edge.
    conn.execute(''' CREATE TABLE IF NOT EXISTS EDGES
                (ID          INT     NOT NULL,
                START_POI_ID INT     NOT NULL,
                END_POI_ID   INT     NOT NULL,
                SPEED        INT               ,
                DISTANCE     INT             ,
                PX           FLOAT   NOT NULL,
                PY           FLOAT   NOT NULL,
                PZ           FLOAT   NOT NULL,
                PRIMARY KEY (ID));''')

    print 'EDGES                table    created'
                                                                        # Table 'DJIKSTRAS' gives the matrix values extracted from djikstras
                                                                        # algorithm. It also gives the information on 'via' points. for example
                                                                        # point B can be reached from point D 'via' A. So, along with the shortest
                                                                        # path this table also contains 'A' in it so the accurate route
                                                                        # can be accessible to each node.
    conn.execute(''' CREATE TABLE IF NOT EXISTS DJIKSTRAS
                (START_POI_ID INT,
                END_POI_ID INT,
                VIA_POI_ID INT,
                DISTANCE FLOAT);''')

    print 'DJIKSTRAs            table    created'

    # Inserting the values in the tables
    pois_for_db = []
    pois_table = []

    j = 1
    k = 1
    for each in pois_with_time:
        pois_table.append((j, each[0], each[1], each[2]))
        i = 3
        while i < len(each):
            db_entry = (k, j, each[i])
            pois_for_db.append(db_entry)
            i += 1
            k += 1
        j += 1

    ###########################################
    print 'INSERTING data in POIS Table'
    i = 0
    for each in pois_table:
        conn.execute("INSERT INTO POIS VALUES (?,?,?,?)", (each))
    conn.commit()
    ##########################################
    print 'INSERTING data in POIS_WITH_TIME Table'
    for each in pois_for_db:
        conn.execute("INSERT INTO POIS_WITH_TIME VALUES (?,?,?)", (each))
    conn.commit()
    ##########################################

    # Edges have time periods along with coordinates i.e. (x1,y1,z1,t1,x2,y2,z2,t2...);
    # removing these time periods i.e. (x1,y1,z1,x2,y2,z2...)

    edges_without_time = []
    for each in edges:
        i = 1
        e = (each[0],each[1],each[2])
        while i < len(each)/4:
            e = e + (each[4*i],) + (each[4*i+1],) +(each[4*i+2],)
            i += 1
        e = e + (math.ceil(each[len(each)-2]),) + (math.ceil(each[len(each)-1]),)  # Add the speed and distance at the end of the edge
        edges_without_time.append(e);

    # Making the edges in such way to be inserted in database
    # (ID, X1, Y1, Z1, X2, Y2, Z2, Speed, Distance, Px, Py, Pz)
    edges_for_db = []
    i = 0
    for each in edges_without_time:
        c = conn.execute("SELECT ID FROM POIS WHERE PX = ? AND PY = ? AND PZ = ?", (each[0], each[1], each[2]))
        for every in c:
            start_poi_id = every[0]
            break

        c = conn.execute("SELECT ID FROM POIS WHERE PX = ? AND PY = ? AND PZ = ?", (each[len(each)-5], each[len(each)-4], each[len(each)-3]))
        for every in c:
            end_poi_id = every[0]
            break

        j = 1
        while j < len(each)/3 - 1:
            i += 1
            edges_for_db.append((i,) + (start_poi_id, end_poi_id,) + (math.ceil(each[len(each)-2]),) + (math.ceil(each[len(each)-1]),) + (each[j*3],) + (each[j*3 + 1],) + (each[j*3 + 2],))
            j += 1

    # Edges are bidirectional so, reverse edge is also possible
    # Reversing the edges; so OMNeT doesnt have to do any work
    k = len(edges_without_time)
    while k > 0:
        k -= 1
        j = len(edges_without_time[k])/3 - 2
        while j > 0:
            i += 1
            ln = len(edges_without_time[k])

            c = conn.execute("SELECT ID FROM POIS WHERE PX = ? and PY = ? and PZ = ?", (edges_without_time[k][0], edges_without_time[k][1], edges_without_time[k][2]))
            for every in c:
                start_poi_id = every[0]
                break

            c = conn.execute("SELECT ID FROM POIS WHERE PX = ? and PY = ? and PZ = ?", (edges_without_time[k][ln-5], edges_without_time[k][ln-4], edges_without_time[k][ln-3]))
            for every in c:
                end_poi_id = every[0]
                break

            edges_for_db.append((i,) + (end_poi_id, start_poi_id,) + (math.ceil(edges_without_time[k][ln-2]),) + (math.ceil(edges_without_time[k][ln-1]),) + (edges_without_time[k][j*3 + 0],) + (edges_without_time[k][j*3 + 1],) + (edges_without_time[k][j*3 + 2],))
            j -= 1

    print 'INSERTING data in EDGES Table'
    for each in edges_for_db:
        each = list(each)
        each = tuple(each)
        conn.execute("INSERT INTO EDGES VALUES (?,?,?,?,?,?,?,?)",each)
    conn.commit()



####################################################
#           DJIKSTRA'S ALGORITHM
# Create the djikstras matrix
# From one POI:
#     -take all edges
#     -see to which POIs the edges goes to
#     -take the edges from those POIs and iterate
###################################################

################ Djikstra's Algorithm #############

    if dijkstras_switch == 'on':
        pois_djk = []
        edges_id_djk = []                # Copying edges to make a list like [(P1 P2 dist),(P1 P2 dist)...]
        for each in edges_for_db:
            djk_temp = (each[1],each[2],each[len(each)-4])
            if djk_temp not in edges_id_djk:
                edges_id_djk.append(djk_temp)

        # Copying POIs for Djikstra algorithm
        for each in pois_table:
            djk_temp = (each[0])
            if djk_temp not in pois_djk:
                pois_djk.append(djk_temp)

        V = len(pois_djk)                # Number of vertices in graph

# A list representing the graph with infinite values as zero
# Creaing a distance matrix to store distance from POI to POI
# where direct edges exist
        dist_matrix = []                # Stores the Distance Matrix (List of Lists)
        i = 0
        while i < V:
            j = 0
            dist = [()] * V
            while j < V:
                count = 0
                if pois_djk[j] == pois_djk[i]:                # Distance from node to itself is 0 in djikstras
                    dist[j] = dist[j] + (pois_djk[j],0,)
                else:                                         # Distance from node to other is retrieved from Edges table if edge b/w these points exist
                    conn_dist = conn.execute("SELECT DISTINCT DISTANCE FROM EDGES WHERE START_POI_ID = ? and END_POI_ID = ?", (pois_djk[i], pois_djk[j]))
                    dist_lst = []
                    for each in conn_dist:
                        count += 1
                        dist_lst.append(int(each[0]))

                    if len(dist_lst) > 0:                                    # If edge exist then update the djikstras matrix
                        dist[j] = dist[j] + (pois_djk[j], min(dist_lst),)
                    else:                                                    # If edge does not exist then assign it the values zero and it will be updated later
                        dist[j] = dist[j] + (pois_djk[j], 0,)
                j += 1
            dist_matrix.append(dist)                                         # Add a row for each node to every other node in the djikstras matrix
            i += 1

    # Completes the distance matrix by running djikstra's algorithm on it
    # Find all the possbile edges and fill in the matrix where the values are zero
        djikstra = []
        from_vertex = 1
        while from_vertex <= V:                                         # Loop to find shortest path for each vertex
            dist_from_vertex = []
            for i in range(V):
                dist_from_vertex.append((0,float('inf')))               # Contains the shortest path from from_vertex to all other vertices
            shortest_path_set = [False for _ in range(V)]               # Contains the boolean to check if shortest path from from_vertex to this vertex is set or not

            dist_from_vertex[from_vertex-1] = (from_vertex, 0)          # Distance to itself is zero

            for count in range(V):
                idx = minimum_Distance(dist_from_vertex, shortest_path_set, V)
                shortest_path_set[idx] = True

            # If the direct distance to end POI is larger than the distance to newly added POI
            # and then to end POI AND If the the sum of this distance is less than infinity then
            # add the newly added POI and VIA POI and create an edge from Source to Destination

                for r in range(V):
                    if (not(shortest_path_set[r]) and dist_matrix[idx][r][1]>0 and dist_from_vertex[idx][1]!=float('inf') and dist_from_vertex[idx][1]+dist_matrix[idx][r][1] < dist_from_vertex[r][1]):
                        dist_from_vertex[r] = (pois_djk[idx],dist_from_vertex[idx][1]+dist_matrix[idx][r][1])

            djikstra.append(dist_from_vertex)
            from_vertex += 1

        # Add the Edges created by Djikstra's algorithm to the 'DJIKSTRAS' table
        print 'INSERTING data in DJIKSTRAS Table'
        i = 0
        while i < len(pois_djk):
            j = 0
            while j < len(pois_djk):
                conn.execute("INSERT INTO DJIKSTRAS VALUES (?,?,?,?)",(pois_djk[i], pois_djk[j], djikstra[i][j][0],djikstra[i][j][1]))
                j += 1
            i += 1
        conn.commit()

        print "*"*25

        print 'Making edges from Djikstras matrix, for database'

        i = 0
        prev = []
        ln_p = len(pois_djk)                                                # Construct the edge from each (POI) to every (POI)
                                                                            # by running sql commands on djikstra's table

        while i < len(pois_djk):                                            # Assemble the complete edges including the mid points
            j = 0                                                           # Previously edges consisted of Source, Destination and VIA POIs
            print i, 'of', ln_p, ':: finding edge from POI ID ', pois_djk[i], 'to POI IDs :: ',
            while j < len(pois_djk):
                print pois_djk[j],

                # If the edge from source to destination exists in EDGES_IDENTIFIER
                # then there is no need to make an edge from Djikstras
                # If it doesn't exists then go further and make it

                conn_dist = conn.execute("SELECT DISTINCT * FROM EDGES WHERE START_POI_ID = ? and END_POI_ID = ?", (pois_djk[i], pois_djk[j]))
                result = conn_dist.fetchone()

                if result == None:                                           # Edge does not exist so make it
                    conn_dist = conn.execute("SELECT MAX(ID) FROM EDGES")    # Max(ID) is needed so the new edge can be added with the max(ID) + 1

                    for each in conn_dist:
                        maxID = each[0]

                    lst = []                                                # Get all the VIA POIs from Source to Destination
                    lst.append((pois_djk[j],0))                             # Start from the Source POI to Destination POI and save the VIA POIs
                    conn_dist = conn.execute("SELECT DISTINCT VIA_POI_ID, DISTANCE FROM DJIKSTRAS WHERE START_POI_ID = ? and END_POI_ID = ?", (pois_djk[i], pois_djk[j]))

                    for a in conn_dist:
                        lst.append(a)

                        if lst[len(lst)-1][len(lst[len(lst)-1])-1] == float('inf'):
                            break
                        else:
                            while a != (pois_djk[i], 0):
                                conn_dist = conn.execute("SELECT DISTINCT VIA_POI_ID, DISTANCE FROM DJIKSTRAS WHERE START_POI_ID = ? and END_POI_ID = ?",(pois_djk[i], a[0]))
                                for a in conn_dist:
                                    lst.append(a)


                    # We have all the VIA POIs, now gather the midpoints (non POIs)
                    # and save them in the final path, which will then be added to Database table

                    idx = len(lst)-2
                    path = []

                    while idx > 0:
                        temp = (lst[idx], lst[idx-1])

                        conn_qry = conn.execute("SELECT DISTINCT * FROM EDGES WHERE START_POI_ID = ? and END_POI_ID = ?", (lst[idx][0], lst[idx-1][0],))

                        for each in conn_qry:
                            ln = len(each)
                            maxID += 1
                            path.append((maxID, pois_djk[i], pois_djk[j], each[ln-5], each[ln-4], each[ln-3], each[ln-2], each[ln-1]))
                        idx -= 1


                    for each in path:            # Djikstras path is finalized, Adding it to Edges table in Database
                        each = list(each)
                        each = tuple(each)
                        conn.execute("INSERT INTO EDGES VALUES (?,?,?,?,?,?,?,?)",each)

                j += 1
            print
            i += 1
        conn.commit()



# MAIN STARTS HERE
# User defined variables
def main():
    global mintime
    global k
    global eps
    global conn
    global poi_all
    global data_all
    global pois_with_time
    global pois_with_time_all
    global edges
    global dijkstras_switch

    traces_directory = sys.argv[2]
    mintime = int(sys.argv[3])  #600                    # in seconds. Min Time, for a point to be considered as POI, if spent there
    k = int(sys.argv[4])        #75                     # No of neighboring points to be checked for a point to be POI
    eps = int(sys.argv[5])      #500                    # Considered radius of a POI
    dijkstras_switch = sys.argv[6]

    poi_all = []
    data_all = []
    pois_with_time = []
    pois_with_time_all = []
    edges = []
    pois_djk = []
    local_minima_list = []

    print "Minimum time period                    : ", mintime, "s"
    print "No of neighbor points to be considered : ", k
    print "Eps Radius of POI                      : ", eps, "m"

    # - Removing Old database if present
    # - Reading contents of directory
    # - Creating and connecting to Database

    if not os.path.exists(traces_directory):
        print "Given directory does not exists"
        quit()

    trace_files = os.listdir(traces_directory)

    if len(trace_files) == 0:
        print "No trace files are present in mentioned directory"
        quit()

    if os.path.isfile("map.db"):
                os.remove("map.db")

    #cwd = os.getcwd()
    lst = os.listdir(traces_directory)
    lst.sort()

    conn = sqlite3.connect("map.db");

    # - Open the text files to write cartesian coordinates and POIs to
    open('pois.txt','w').close()

    count = 1

    '''###
    # Code commented like this is used to write normalized
    # coordinates, to external files with extended trace names

    i = 0
    name = []
    ###'''

    #data_all = []
    #min_list_all = []


    # - Open all the trace files and read the data
    # - Convert to cartesian coordinates and find the minimum values
    #   each of x,y and z coordinate
    # - Append this data to list for further processing

    for cartesian_trace in lst:
        if '-cartesian' in cartesian_trace:
            print count, 'of', len(lst), " :: Reading Cartesian Trace :: ", cartesian_trace

            '''####
            name.append(cartesian_trace.replace("-cartesian.txt","") + "-normalized.txt")
            ####'''

            cartesian_trace_data = []

            with open(traces_directory + "/" + cartesian_trace) as filedata:
                content = filedata.readlines()
            filedata.close()

            for each in content:
                temp = tuple(each.strip().split())                      # Stores the data in tuple form
                cartesian_trace_data.append( (float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3])) )

            local_minimas = find_minimum(cartesian_trace_data)
            local_minima_list.append(local_minimas)

            temp_cartesian_trace_list = []
            for each in cartesian_trace_data:
                temp_cartesian_trace_list.append( (each[0], each[1], each[2], each[3]-local_minimas[3]) )

            data_all.append(temp_cartesian_trace_list)
            count = count + 1

        # Find global minimum values for cartesian coordiantes to normalize
    global_minima = map(min, zip(*local_minima_list))

    print global_minima

    # - Normalize the data with minimum values of x, y, z coordinates and time
    # - Needed because the minimum values on simulation canvass starts from 0,0,0 and simulation time from 0
    temp_cartesian_trace_list2 = []
    for each in data_all:
        temp_cartesian_trace_list = []
        for every in each:
            temp_cartesian_trace_list.append((every[0]-global_minima[0], every[1]-global_minima[1], every[2]-global_minima[2], every[3]))
        temp_cartesian_trace_list.sort(key=lambda tup: tup[3])

        '''###
        outfile = open(name[i], "w+")
        for each in temp_cartesian_trace_list:
            outfile.write(str(each[0]))
            outfile.write(" ")
            outfile.write(str(each[1]))
            outfile.write(" ")
            outfile.write(str(each[2]))
            outfile.write(" ")
            outfile.write(str(each[3]))
            outfile.write("\n")
        outfile.close()
        i = i + 1
        ###'''

        temp_cartesian_trace_list2.append(temp_cartesian_trace_list)

    data_all = []
    for each in temp_cartesian_trace_list2:
        for every in each:
            data_all.append(every)

    # - Identify the POIs from data list
    find_POIs(data_all)

    # - Identify and search for the edges which can be directly
    #   deduced from data list

    dijkstras_switch = dijkstras_switch.replace('dijkstras=', '')
    find_edges()

    # - Create database, add all the mobility map information in database
    # - Using Djikstra's algorithm, create missing edges on the map and save
    database_functions()

    conn.close()


if __name__ == "__main__":
    main()



