## The following script is used to evaluate, using a function of input arguments the start and end station, what the route
## of minimum stops is. In addition it involves a simple "Did you mean" capability in order to add redundancy in user input
## Created by Michalis Hadjiandreou on 7th Dec 2020


#### Hard-coded routes of the 5 tube lines
Victoria = [ "Highbury Islington", "Kings Cross", "Euston", "Warren Street", "Oxford Circus", "Green Park" ] 
Piccadilly = [ "Kings Cross", "Russell Square", "Holborn", "Covent Garden", "Leicester Square", "Piccadilly Circus", "Green Park" ] 
CrossRail = [ "Liverpool Street", "Farringdon", "Tottenham Court Road", "Bond Street" ] 
Jubilee = [ "Baker Street", "Bond Street", "Green Park" ] 
Circle = [ "Euston", "Kings Cross", "Farringdon", "Barbican" ]

#### The function below counts the matching characters within a pair of strings
def countPairs(string1, length1, string2, length2) :  
    occ1 = [0] * 26  
    occ2 = [0] * 26  
    counter=0
  
    #capture the characters of string 1
    for i in range(length1) :  
        occ1[ord(string1[i]) - ord('a')] += 1;  
  
    #capture the characters of string 2
    for i in range(length2) :
        occ2[ord(string2[i]) - ord('a')] += 1;  
  
    # quantify the matching pairs
    for i in range(26) : 
        counter += min(occ1[i], occ2[i]);  
    
    return counter;

## The following function suggests alternatives in a quantitative manner (%match of strings)
def suggestalternatives(string,data):
    #remove the spaces for standardization
    string=string.replace(" ","")
    string=string.lower()
    #initialise the final result array
    final_quant=[]
    
    # iterate through our hard-coded routes to test similarity
    for candidate in data:
        # remove space as above
        candidate=candidate.replace(" ","")
        # convert to lower case for standardisation
        candidate=candidate.lower()
        
        # needed to be fed on the countPairs algorithm
        lenCandidate=len(candidate)
        lenString=len(string)
        
        ## return the number of matching characters as a percentage of the the maximum of either string's character length
        final_quant.append(countPairs(string,lenString,candidate,lenCandidate)/max(lenString,lenCandidate)*100)
        
        # returns a list with percentages according to the matching characters of the two stringss
    return final_quant

# concacate the strings to have a uniform collection
total=Victoria+Piccadilly+CrossRail+Jubilee+Circle


## Driver code
#START STATION INPUT
print('Please input the starting station:')
start_st=input()
while start_st not in total:
    final_quant=suggestalternatives(start_st,total)    
    print("Did you mean [Y/N]: ")
    print(total[final_quant.index(max(final_quant))])
    ans=input().lower()
    if 'y' in ans:
        start_st=total[final_quant.index(max(final_quant))]
        break
    else:
        print('Please re-input the starting station:')
        start_st=input()
        

# DESTINATION STATION INPUT
print('Please input the final station:')
end_st=input()
while end_st not in total:
    final_quant=suggestalternatives(end_st,total)    
    print("Did you mean [Y/N]: ")
    print(total[final_quant.index(max(final_quant))])
    ans=input().lower()
    if 'y' in ans:
        end_st=total[final_quant.index(max(final_quant))]
        break
    else:
        print('Please re-input the final station:')
        end_st=input()
    

print('Evaluating your journey from ',start_st,'to ',end_st)
print('=====================================================')

############################ CORE CODE ======================================

# Create the graph of stations (as shown in the report)
graph = {'A': ['O','P','I','H'],
         'B': ['G','K'],
         'C': ['N','D','M'],
         'D': ['H','C'],
         'E': ['H','I'],
         'F': ['I','Q'],
         'G': ['B','J'],
         'H':['A','L','E','D'],
         'I':['A','F','E'],
         'J':['P','G'],
         'K':['B','M'],
         'L':['H'],
         'M':['K','Q','C'],
         'N':['C'],
         'O':['A'],
         'P':['A','J'],
         'Q':['F','M']}

# Map the stations to the nodes (see report)
stations_dict2={
    'Kings Cross': 'A',
    'Leicester Square':'B',
    'Bond Street':'C',
    'Tottenham Court Road':'D',
    'Barbican':'E',
    'Warren Street': 'F',
    'Covent Garden': 'G',
    'Farringdon': 'H',
    'Euston': 'I',
    'Holborn':'J',
    'Piccadilly Circus':'K',
    'Liverpool Street':'L',
    'Green Park':'M',
    'Baker Street':'N',
    'Highbury Islington':'O',
    'Russell Square':'P',
    'Oxford Circus':'Q',
    }


## BFS
def BFS(graph, start, destination):
    visited = []
    queue = [[start]]

    # check if the start and final stations are the same
    if start == destination:
        print('Your start and final station are the same')
        return 
 
    
    # BFS implementation
    while queue:
        # dequeue and assign on path list (which is used to track the path)
        path = queue.pop(0)
        # we select the next node as governed by the BFS rules
        node_inv = path[-1]
        
        # proceed only if we haven't revisited that node
        if node_inv not in visited:
            # extract its neighbours from the dictionary above
            neighbours_connected = graph[node_inv]
            
            # for each neighbour construct a new path and update our queue
            for neighbour in neighbours_connected:
                upd_path = list(path)
                upd_path.append(neighbour)
                queue.append(upd_path)
                
                ## TERMINATING CONDITION: if the neighbour node is our goal then it is guaranteed we reached the shortest path to our goal
                if neighbour == destination:
                    print('The shortest route from ',stations_dict[start],' to ', stations_dict[destination], 
                          ' with a total of ', len(upd_path), '(inclusive start and end stations) is: ')
                    print('==================================================== ***** ====================================================')
                    [print(stations_dict[x]) for x in upd_path]
                    
                    return upd_path
 
            # update our explored list since our visit has ended
            visited.append(node_inv)
 
    # If link doesnt exist between the two nodes
    print("Current network does not provide link between the two stations.")            
    return 


## ENTRY POINT BFS
# Extract the starting and destination node letters
start_node=stations_dict2[start_st]
end_node=stations_dict2[end_st]

# flip the dictionary for ease of extracting the final result after BFS
stations_dict = {v: k for k, v in stations_dict2.items()}

# Call BFS
BFS(graph,start_node,end_node)  































