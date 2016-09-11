#!/usr/bin/python
# Basic Vivaldi implementation

import random
from numpy import array, median
from numpy.linalg import norm
from Graph import Graph

class Vivaldi():
    def __init__(self, graph, configuration):
        self.graph = graph
        self.configuration = configuration
        
        self.N = configuration.getNumNodes()
        self.d = configuration.getNumDimension()
        self.cc = configuration.getCc()
        self.ce = configuration.getCe()
        self.numNeighbors = configuration.getNumNeighbors()
        self.initialization()
        
    def initialization(self):
        ### Initial coordinates
        self.coordinates = {node: array([0]*self.d, dtype=float) for node in range(self.N)}
        
        ### Initial error estimates
        ## Errors are stored in a list: {error_node1, ..., error_noden}
        self.error = {node: 1. for node in range(self.N)}
        
        ### Displacement
        ## Displacements are stored in a list: [median_displacement_iteration1, ...,median_displacement_iterationn]
        self.convergence = []
        self.displacement = []
        
        return 1
        
    # Core of the Vivaldi algorithm
    def run(self):
        # For each iteration
        for it in range(self.configuration.getNumIterations()):
            moves = []
            
            # For each node pick up K random neighbors
            for i in range(self.N):
                node = self.getPosition(i)
                
                node_neighbors = self.graph.getAdjacent(i)
                number_of_neighbors_for_node = len(node_neighbors)
                
                ## Pick up random neighbors
                # Handles a too small number of neighbors
                if number_of_neighbors_for_node <= self.numNeighbors:
                    random_neighbors = [neighbor for neighbor in node_neighbors]
                    
                else:
                    random_neighbors = random.sample(self.graph.getAdjacent(i), self.configuration.getNumNeighbors())

                # Keep in memory coordinates of node before motion
                initial_position = array(node, copy=True)
                
                ## Vivaldi process
                for j,rtt in random_neighbors:
                        neighbor = self.getPosition(j)

                        # Check how much the node has to "move" in terms of RTT towards/away from his neighbors
                        distance = norm(node - neighbor)
                        error = rtt - distance
                        delta = self._computeAdaptiveTimestep(i, j, rtt, distance)

                        # Compute the new coordinates
                        direction = self._getDirection(node, neighbor, distance)
                        node += delta * error * direction

                        ## Compute the displacement of node during current iteration
                        moves.append(norm(node - initial_position))

                ## Compute the global error in each iteration
                global_error = 0
                for i in range(self.N):
                        for j,rtt in self.graph.getAdjacent(i):
                                global_error += (rtt - norm(self.getPosition(i) - self.getPosition(j)))**2

                self.convergence.append(global_error)
                self.displacement.append(median(moves))

        return 1
    
    # Get the predicted RTT graph following Vivaldi.
    def getRTTGraph(self):
        # Handles update of coordinates
        self.run()

        ## Predicted RTT graph is built according to the same model as the measured rtt graph
        predicted_graph = Graph(self.N)
        
        for i in range(self.N):
                for j in range(self.N):
                        if i != j:
                                predicted_graph.addVertex(i, j, norm(self.getPosition(i) - self.getPosition(j)))
        return predicted_graph
        
    # Get the position of a node
    def getPosition(self, node):
        return self.coordinates[node]
    
    # Get the displacement of the Vivaldi algorithm
    def getDisplacement(self):
        return self.displacement

    # Get the convergence of the Vivaldi algorithm
    def getConvergence(self):
        return self.convergence
    
    # Relative error of the predicted graph wrt real RTT graph
    def getRelativeError(self, predicted_graph):
        error_values = []
        for i in range(self.N):
            link_errors = []
            for j,rtt in self.graph.getAdjacent(i):
                link_errors.append(abs(rtt - predicted_graph.getRTT(i,j)) / rtt)
                
        # Error of a node: the median of the link errors for links involving that node
        error_values.append(median(link_errors))
        return error_values
        
    # Basic CDF computation
    def computeCDF(self, input_):
        x = sorted(input_)
        y = map(lambda x: x / float((len(input_) + 1)), range(len(input_)))
        return x,y


    # Compute the adaptive
    def _computeAdaptiveTimestep(self, node, neighbor, rtt, distance):
        relative_error = abs(rtt - distance) / rtt
        
        # Compute the weight
        weight = self.error[node] / (self.error[node] + self.error[neighbor])
        
        # Update the error estimate
        self.error[node] = relative_error * self.ce * weight + self.error[node] * (1 - self.ce * weight)
        
        # Compute the adaptative timestep
        return self.cc * weight


    # Get the direction of the force
    def _getDirection(self, node, neighbor, distance):
            # If the two nodes have the same coordinates choose a random direction
            if distance == 0:
                    direction = array([random.random() for x in range(self.d)])
                    return direction / norm(direction)
            else:
                    return (node - neighbor) / distance