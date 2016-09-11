#!/usr/bin/python
###
# Basic configuration for running Vivaldi.
# n: number of nodes
# K: number of neighbors
# num_iterations: number of iterations for adjusting the coordinates
# d: number of dimensions (network coordinates)
#
# The following parameters can be used to weight the movement and the error estimation.
# However, this depends also on your implementation.
# If you do not use them, remove them.
#
# cc: scale factor of the movement
# ce: precision weight in error estimation
# 
###
class Configuration():
	def __init__(self, n, K, num_iterations, d=3, cc=0.1, ce=0.25):
		self.num_nodes = n
		self.num_neighbors = K
		self.num_iterations = num_iterations
		self.num_dimension = d
		self.cc = cc
		self.ce = ce
		
	# Getter methods
	def getNumIterations(self):
		return self.num_iterations
		
	def getNumNodes(self):
		return self.num_nodes
		
	def getNumNeighbors(self):
		return self.num_neighbors
	
	def getNumDimension(self):
		return self.num_dimension
	
	def getCc(self):
		return self.cc
	
	def getCe(self):
		return self.ce
	
