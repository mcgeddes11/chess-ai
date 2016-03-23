# -*- coding: utf-8 -*-
"""
Created on Sat Oct 03 15:03:27 2015

@author: jcocks
"""

import numpy

def nonlin(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)
	return 1/(1+numpy.exp(-x))
 
    
X = numpy.array([[0,0,1],
            [0,1,1],
            [1,0,1],
            [1,1,1]])
                
y = numpy.array([[0],
			[1],
			[1],
			[0]])

numpy.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = 2*numpy.random.random((3,4)) - 1
syn1 = 2*numpy.random.random((4,1)) - 1

for j in xrange(60000):

	# Feed forward through layers 0, 1, and 2
    l0 = X
    l1 = nonlin(numpy.dot(l0,syn0))
    l2 = nonlin(numpy.dot(l1,syn1))

    # how much did we miss the target value?
    l2_error = y - l2

    if (j% 10000) == 0:
        print "Error:" + str(numpy.mean(numpy.abs(l2_error)))

    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error*nonlin(l2,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = l2_delta.dot(syn1.T)

    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1,deriv=True)

    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)



#
#
# from pybrain.tools.shortcuts import buildNetwork
# from pybrain.supervised.trainers import BackpropTrainer
# from pybrain.datasets import SupervisedDataSet
# from pybrain.structure import TanhLayer
#
# # Test neural network on small input
# net = buildNetwork(1, 2, 1, bias=True, hiddenclass=TanhLayer)
# ds = SupervisedDataSet(numpy.shape(X)[1], 1)
# for ix, yVal in enumerate(y):
#     ds.addSample(tuple(X[ix]),tuple(y[ix]))
#
# trainer = BackpropTrainer(net, ds)
# trainer.trainUntilConvergence()