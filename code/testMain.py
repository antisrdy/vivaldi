#!/usr/bin/python

from Graph import Graph
from Configuration import Configuration
from Vivaldi import Vivaldi

import sys
import numpy as np
import pylab as py

def buildgraph(rows):
    g = Graph(len(rows))
    for node in range(len(rows)):
        arr = rows[node].strip().split(" ")
        rtts = [float(x) for x in arr if len(x) > 0]
        for neighbor in range(len(rtts)):
            g.addVertex(node,neighbor,rtts[neighbor])
    return g

	
if __name__== "__main__":
	if len(sys.argv) != 2:
		print ("Usage: %s <rtt_file>")%sys.argv[0]
		sys.exit(0)
	
	rttfile = sys.argv[1]
	infile = open(rttfile, 'r')
	rows = infile.readlines()
	num_nodes = len(rows)
	infile.close()
	
	## Input parameters
	num_neighbors = input("Neighbors picked up for each node: ")
	num_iterations = input("Number of iterations: ")

	# Build a configuration and load the matrix into the graph
	c = Configuration(num_nodes, num_neighbors, num_iterations)
	init_graph = buildgraph(rows)

	print("    ****************************************\n    * Running Vivaldi on a %d size matrix *\n    ****************************************")% num_nodes
	print("\n    Configuration")
	print("          Num dimensions = {}".format(c.getNumDimension()))
	print("          Num neighbors = {}".format(int(num_neighbors)))
	print("          Num iterations = {}".format(int(num_iterations)))

	## Create instance of Vivaldi
	v = Vivaldi(init_graph, c)

	## Retrieve relative error and update displacement
	predicted = v.getRTTGraph()
	rerr = v.getRelativeError(predicted)

	## CDF of relative prediction error
	x,y = v.computeCDF(rerr)

	## Statistics on relative prediction error
	print("\n    Relative Error statistics:")
	print("          Mean:", np.mean(x))
	print("          Variance:", np.var(x))
	print("          Min:", min(x))
	print("          Max:", max(x))
	print("          Median:", np.median(x))
	print("          90-th percentile:", np.percentile(x, 90))
	print("          99-th percentile:", np.percentile(x, 99))

	## Plot of the CDF
	py.subplot(1,3,1)
	py.plot(x,y)
	py.title('CDF of the relative prediction error')
	py.xlabel('Relative prediction error')
	py.ylabel('CDF')

	## Retrieve median error
	convergence = v.getConvergence()

	## Statistics on the median error
	print("\n    Median error statistics:")
	print("          Mean:", np.mean(convergence))
	print("          Variance:", np.var(convergence))
	print("          Min:", min(convergence))
	print("          Max:", max(convergence))
	print("          Median:", np.median(convergence))
	print("          90-th percentile:", np.percentile(convergence, 90))
	print("          99-th percentile:", np.percentile(convergence, 99))

	## Plot of the median error
	py.subplot(1,3,2)
	py.plot(range(num_iterations), convergence)
	py.title('Convergence in terms of median error')
	py.xlabel('Number of iterations')
	py.ylabel('Median error (ms)')

	## Retrieve the displacement
	displacement = v.getDisplacement();

	## Statistics on the displacement
	print("\n    Displacement statistics:")
	print("          Mean:", np.mean(displacement))
	print("          Variance:", np.var(displacement))
	print("          Min:", min(displacement))
	print("          Max:", max(displacement))
	print("          Median:", np.median(displacement))
	print("          90-th percentile:", np.percentile(displacement, 90))
	print("          99-th percentile:", np.percentile(displacement, 99))

	## Plot of the displacement
	py.subplot(1,3,3)
	py.plot(range(num_iterations), displacement)
	py.title('Convergence in terms of displacement')
	py.xlabel('Number of iterations')
	py.ylabel('Displacement')

	py.show()