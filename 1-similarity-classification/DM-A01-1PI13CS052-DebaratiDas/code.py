# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 09:29:07 2016

@author: Debarati Das 
"""
#import os
import random
import csv
import operator
import math
import pandas as pd
import sys

# functions to create the matrix of distances from each element in the training set to other 

def func_find_min(distMatrix,fresult, trainingSet):
    ctr=0
    min_t = (-1, 99999999999, -1)
    max_t = (-1, -1, -1)
    for i in distMatrix:
        for newlist in i:
            if newlist[1] > max_t[1]: max_t = (newlist[0], newlist[1], ctr)
            if newlist[1] < min_t[1]: min_t = (newlist[0], newlist[1], ctr)

        # print >>fresult, "For Element number in train dataset : "+str(ctr+1)
        # print >>fresult, "Species of minimum distance element : "+str(newlist[1][0][4])
        # print >>fresult, "Minimum distance element and distance : "+str(newlist[1])
        # print >>fresult,"Species of Maximum distance element: "+str(newlist[len(newlist)-1][0][4])
        # print >>fresult, "Maximum distance element and distance: "+str(newlist[len(newlist)-1])
        #
        # print >>fresult,'\n'

        ctr+=1
    print >>fresult, "Minimum:", str(min_t[1]), trainingSet[min_t[2]][0], "(", trainingSet[min_t[2]][-1], ")", min_t[0][0], "(", min_t[0][-1], ")"
    print >>fresult, "Maximum:",  str(max_t[1]), trainingSet[max_t[2]][0], "(", trainingSet[max_t[2]][-1], ")", max_t[0][0], "(", max_t[0][-1], ")"

def calculateDistanceMatrixEuclid(trainingSet):
    #first create  a list of lists
    k=len(trainingSet) #what is the number of training data
    #print 'debug : Length of training set \n'    
    #print k 
    d = [[] for x in xrange(k)] # this is the list of lists
    length=len(trainingSet[0]) # we need this in distance calculation
    for y in range(k): # for each element, now create the list of distances
        testInstance= trainingSet[y]
        for x in range(len(trainingSet)):
            if y == x: continue
            dist=euclideanDistance(testInstance, trainingSet[x], length)
            d[y].append((trainingSet[x], dist))
    return d

def calculateDistanceMatrixManhattan(trainingSet):
    #first create  a list of lists
    k=len(trainingSet) #what is the number of training data 
    d = [[] for x in xrange(k)] # this is the list of lists
    length=len(trainingSet[0]) # we need this in distance calculation
    for y in range(k): # for each element, now create the list of distances
        testInstance= trainingSet[y]        
        for x in range(len(trainingSet)):
            if y == x: continue
            dist=manhattanDistance(testInstance, trainingSet[x], length)
            d[y].append((trainingSet[x], dist))
    return d

def calculateDistanceMatrixSupremum(trainingSet):
    #first create  a list of lists
    k=len(trainingSet) #what is the number of training data 
    d = [[] for x in xrange(k)] # this is the list of lists
    #length=len(trainingSet[0]) # we need this in distance calculation
    for y in range(k): # for each element, now create the list of distances
        testInstance= trainingSet[y]        
        for x in range(len(trainingSet)):
            if y == x: continue
            dist=supremumDistance(testInstance, trainingSet[x])
            d[y].append((trainingSet[x], dist))
    return d


def getResponseFrom(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def deriveAccuracy(testSet, predictions):

	correct = 0
	for x in range(len(testSet)):	 
		if testSet[x][-1] == predictions[x]:
			correct += 1

	return (correct/float(len(testSet))) * 100.0


def euclideanDistance(instance1, instance2, length):
	distance = 0
     #length is the number of dimension and last dimension is class ( not required for distance)
	for x in range(1, length-1):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def manhattanDistance(instance1, instance2, length):
    distance = 0
    #length is the number of dimension and last dimension is class ( not required for distance)
    for x in range(1, length-1):
         distance += abs(instance1[x] - instance2[x])
    return distance

def supremumDistance(x,y):    
    return max(abs(a-b) for a,b in zip(x,y)[1:5])
 


def getNeighborsEuclid(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getNeighborsManhattan(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = manhattanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getNeighborsSupremum(trainingSet, testInstance, k):
	distances = []
	for x in range(len(trainingSet)):
		dist = supremumDistance(testInstance, trainingSet[x])
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors


def loadDataset(filename, data=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        # next(lines)  #as there is no header
        dataset = list(lines)[1:]
        for x in range(len(dataset)):
            dataset[x][0] = int(dataset[x][0])
            for y in range(1, 5):
                dataset[x][y] = float(dataset[x][y])
            data.append(dataset[x])
        print 'loaded data: ' + repr(len(data))
         

####################################################################
# Assignment 
###############################################################

def assignment():    
    trainingSet=[] 
    testSet=[]
    predictions=[]
    trainList=[]
    testList=[]
    
#    testk=75  #use default values 
#    traink=75
   

    ######################################################################################
    #Step 1  
    #######################################################################################
   
    
    fresult=open('./DebaratiResult.txt', 'wt')
    
    
    print >>fresult,'Data Mining assignment# 1  By Debarati Das  USN : XXXXX'
    print "Test results are stored in the file resultfile.txt \n"
    
    print >>fresult,'\n' 
    print >>fresult,'====================================================='
    print >>fresult,'Results of Data Mining assignment# 1 Step#1'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
    
    testk = 10
    traink=150-testk
    print >> fresult,"You have entered TestSet count= %d \n" %(testk)
    print >> fresult,"Since it is 150 element dataset, Traincount= 150-Testcount= %d \n" %(traink)
    
   
    # open the three files from the current directory
    random.seed(31)
    trainingSet=[]
    testSet=[]
    print >>fresult, "Loading training data... \n"
    loadDataset('iris.csv',trainingSet)
    testSet = random.sample(trainingSet, 10)
    trainingSet = list(filter(lambda x: x not in testSet, trainingSet))
    print >>fresult, "Loading test data... \n"
    print >>fresult, "Test ids are", list(map(lambda x: x[0], testSet))
    ######################################################################################
    #Step 2  
    #######################################################################################
    
    print >>fresult,'\n'    
    print >>fresult,'====================================================='
    print >>fresult,'Results of Data Mining assignment#1 Step#2 (descriptive statistics)'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
    DF = pd.read_csv("iris.csv", na_values=[" "]) #you need not replace na 
    
    #print DF descriptive statistics for full dataset

    print >>fresult,'====================================================='
    print >>fresult,'(step 2 : Part 1) Descriptive statistics of full datatset'
    print >>fresult,'====================================================='
    
    print  >>fresult, DF.describe(percentiles=None)
    
    print >>fresult,'\n' 
    print >>fresult,'====================================================='
    print >>fresult,'(step 2 : Part 1) Descriptive statistics of full datatset grouped by species'
    print >>fresult,'====================================================='
    print >>fresult, DF.groupby('Species').describe(percentiles=None)
    print >>fresult,'\n' 
    print >>fresult,'====================================================='
    print >>fresult,'Results of Data Mining assignment# 1 Step#2 Part #2 (distance computation)'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
  
    #First we load the train and test dataset into separate lists  
    #we reset the training and test dataset


    print >>fresult,'====================================================='
    print >>fresult,'(step 2 : Part 2) Calculate different types of distance between any two points and find the minimum and maximum of those'
    print >>fresult,'====================================================='
    print >>fresult,'\n'     
    # all we have to do is : for each member of the training set, define it as testSetSingle while the rest 149 can be training set
    #calculate three kinds of distances in a for loop for each one with the other 149  
    # do euclideanDistance(instance1, instance2, length) etc.  
    k=len(trainingSet) #what is the number of training data 
    distMatrix = [[] for x in xrange(k)] # this is the list of lists
    print >>fresult,'====================================================='
    print >> fresult, "Distance matrix for Each Element of training set from each including itself ... \n"
    print >>fresult,'====================================================='
    print >> fresult, "nxn distance matrix using Euclidean distance..............\n"
    print >>fresult,'====================================================='
    distMatrix=calculateDistanceMatrixEuclid(trainingSet)
    
#    for elem in distMatrix:
#        print >>fresult,elem
    
    #print "TESTING NEW FUNC LOL"
    print >>fresult, '\n'
    print >>fresult,'====================================================='    
    print >> fresult, "For each element(in train dataset) minimum and maximum distance(Euclidean) element & distance..............\n"
    print >>fresult,'====================================================='

    func_find_min(distMatrix,fresult, trainingSet)
    
    print >>fresult,'====================================================='
    print >> fresult, "nxn distance matrix using Manhattan distance..............\n"
    print >>fresult,'====================================================='
    distMatrix= calculateDistanceMatrixManhattan(trainingSet)
#    for elem in distMatrix:
#        print >>fresult,elem
    print >>fresult, '\n'    
    print >>fresult,'====================================================='    
    print >> fresult, "For each element (in train dataset) minimum and maximum distance(Manhattan) element & distance..............\n"
    print >>fresult,'====================================================='
    func_find_min(distMatrix,fresult, trainingSet)
    
    print >>fresult,'====================================================='    
    print >> fresult, "nxn distance matrix using Supremum distance..............\n"
    print >>fresult,'====================================================='
    distMatrix= calculateDistanceMatrixSupremum(trainingSet)
#    for elem in distMatrix:
#        print >>fresult,elem
    print >>fresult, '\n'
    print >>fresult,'====================================================='    
    print >> fresult, "For each element(in train dataset) minimum and maximum distance(Supremum) element & distance..............\n"
    print >>fresult,'====================================================='
    
    func_find_min(distMatrix,fresult, trainingSet)

###########################################################################################################
#                     Step 3 
#########################################################################################################     

    print >>fresult,'====================================================='
    print >>fresult,'Assignment 1 : step 3 !!'
    print >>fresult,'====================================================='
    print >>fresult,'\n' 
    
    for k in range(1,6):	# thisis effectively k =1 to 5 	
		# generate predictions
		print >>fresult,'Classification using k nearest neighbour with k='+ str(k)
		print >>fresult,'=====================================================' 
		print >>fresult,'Classification using Euclidean distance !!'
		print >>fresult,'====================================================='
	 
		predictions=[]
		
		for x in range(len(testSet)):
			neighbors = getNeighborsEuclid(trainingSet, testSet[x], k)
			print >>fresult,"===========neighbours of ===========\n"
			print >> fresult,testSet[x]
			print >>fresult,"neighbors are :"
			print >>fresult,list(map(lambda x: x[-1], neighbors))
			result = getResponseFrom(neighbors)
			predictions.append(result)
			print >> fresult,'> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])
		accuracy = deriveAccuracy(testSet, predictions)
		print>> fresult,'Accuracy: ' + repr(accuracy) + '%'

		print >>fresult,'\n'
		print >>fresult,'====================================================='
		print >>fresult,'Classification using Manhattan distance !!'
		print >>fresult,'====================================================='


		predictions=[]

		for x in range(len(testSet)):
			neighbors = getNeighborsManhattan(trainingSet, testSet[x], k)
			print >>fresult,"===========neighbours of==========="
			print >> fresult,testSet[x]
			print >>fresult,"neighbors are :"
			print >>fresult,list(map(lambda x: x[-1], neighbors))
			result = getResponseFrom(neighbors)
			predictions.append(result)
			print >> fresult,'> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])
		accuracy = deriveAccuracy(testSet, predictions)
		print >> fresult,'Accuracy: ' + repr(accuracy) + '%'


		print >>fresult,'====================================================='
		print >>fresult,'Classification using Supremum distance !!'
		print >>fresult,'====================================================='

		predictions=[]

		for x in range(len(testSet)):
			neighbors = getNeighborsSupremum(trainingSet, testSet[x], k)
			print >>fresult,"===========neighbours of==========="
			print >> fresult,testSet[x]
			print >>fresult,"neighbors are :"
			print >>fresult,list(map(lambda x: x[-1], neighbors))
			result = getResponseFrom(neighbors)
			predictions.append(result)
			print >> fresult,'> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1])
		accuracy = deriveAccuracy(testSet, predictions)
		print >> fresult,'Accuracy: ' + repr(accuracy) + '%'

    
    #############################################################################################
    #close the result file 
    print >>fresult,'====================================================='
    print  >> fresult, "...Assignment 1 done...Check resultfile.txt for results ...\n"
    print >>fresult,'====================================================='
    fresult.close()
    print "...Assignment 1 done...Check resultfile.txt for results ...\n"

######################################################################

def main():

    assignment()
    
if __name__ == "__main__":
  main()

######################################################################## 
  
