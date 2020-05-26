
class TSP:
    def __init__(self):
        pass

    def loadProblem(self,path):
        """Loads TSP problem instance. Must follow TSPlib format
        
        Arguments:
            path {String} -- path to TSP instance
        """
        # Open and read file
        f = open(path, 'r')
        x = f.readlines()
        f.close()

        # Fill fields

        self.name = x[0].replace(":","").split()[1]
        self.type = x[1].replace(":","").split()[1]
        self.comment = " ".join(x[2].replace(":","").split()[1:])
        self.dim = int(x[3].replace(":","").split()[1])
        self.edge_weight_type = x[4].replace(":","").split()[1]

        self.fitness_evaluations = 0

        # Create list of nodes
        # Each node is represented by a list of the format [CityIndex, x-coordinate, y-coordinate]
        self.nodesList = [list(map(float,node.split())) for node in x[6:self.dim+6]]
        # Subtracting one to change from 1-indexed to 0-indexed
        for node in self.nodesList:
            node[0] = int(node[0]-1)

        # Create dict of nodes
        # Key is city index and value is tuple (x-coordinate, y-coordinate)
        self.nodesDict = {}
        for node in self.nodesList:
            self.nodesDict[node[0]] = node[1],node[2]

        return self
    def calculateDist(self,location1,location2):
        """Calculates Euclidean distance between two cities
        
        Arguments:
            location1 {int} -- Index of start city
            location2 {int} -- Index of end city
        
        Returns:
            distance [float] -- Euclidean distance between the two cities
        """
        # Get positions of the two cities
        pos1, pos2 = self.nodesDict[location1], self.nodesDict[location2]

        # Calculate the difference in x and y dimensions
        x_dist, y_dist = abs(pos1[0]-pos2[0]), abs(pos1[1]-pos2[1])

        # Calculate distance between the two points
        distance = (x_dist**2 + y_dist**2)**0.5

        return distance
    
    def ResetFitnessCount(self):
        self.fitness_evaluations = 0
        
    def Fitness(self, DistanceMeasure, solution):
        """Calculates fitness of a given tour/solution
        
        Arguments:
            solution {List} -- Order of cities to visit. Must contain integers from 0 to 51 for a problem of size 52
        
        Returns:
            Fitness [float] -- Negative length of tour/solution using Euclidean distance
        """
        self.fitness_evaluations += 1
        if DistanceMeasure != None:
            print("We should not have a distance measure in this fitness function")
            raise Error

        # Check that the tour is legal
        if len(solution) != self.dim or not all([x in solution for x in range(self.dim)]):
            print(solution)
            raise Error
        
        
        
        tourLength = 0

        # Distance between each pair from (0,1) to (dim-2,dim-1)
        for cityIndex in range(self.dim-1):
            tourLength += self.calculateDist(solution[cityIndex],solution[cityIndex+1])

        # Distance from dim-1 to 0
        tourLength += self.calculateDist(solution[self.dim-1],solution[0])

        tourLength = round(tourLength,2)
        return -tourLength


