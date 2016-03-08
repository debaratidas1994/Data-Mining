


## ----------------------- Part 1 ---------------------------- ##
import numpy as np
from numpy import array

# X = (hours sleeping, hours studying), y = Score on test
X = np.array(([1,0.25,-0.5]), dtype=float)
y = np.array(([1.0], [-1.0]), dtype=float)

# Normalize
X = X/np.amax(X, axis=0)
y = y/np.amax(y,axis=0) #Max test score is 100

## ----------------------- Part 2 ---------------------------- ##

class Neural_Network(object):
    def __init__(self):        
        #Define Hyperparameters
        self.inputLayerSize = 3
        self.outputLayerSize = 2
        self.hiddenLayerSize = 2
        
        #Weights (parameters)
        self.W1=np.random.uniform(low=-1.0,high=1.0,size=(self.inputLayerSize, self.hiddenLayerSize))
        print(" W1 initialised")
        print self.W1
        self.W2=np.random.uniform(low=-1.0,high=1.0,size=(self.hiddenLayerSize, self.outputLayerSize))
        print(" W2 initialised")
        print self.W2
        print(" biases initialised ")

        self.b4=np.random.uniform(low=-1.0,high=1.0)
        self.b5=np.random.uniform(low=-1.0,high=1.0)
        self.biaslayer2=array([self.b4,self.b5])

        print("Bias for Layer 2 : ",self.biaslayer2)
        

        self.b6=np.random.uniform(low=-1.0,high=1.0)
        self.b7=np.random.uniform(low=-1.0,high=1.0)
        self.biaslayer3=array([self.b6,self.b7])
        
        print("Bias for Layer 3 : ",self.biaslayer3)
        #self.W1 = np.random.randn(self.inputLayerSize, self.hiddenLayerSize)
        #self.W2 = np.random.randn(self.hiddenLayerSize, self.outputLayerSize)
        
    def forward(self, X):
        #Propagate inputs though network
        print("forward propagating !")
        #ij matrix hidden
        self.ij1=np.dot(X, self.W1)
        self.z2 = self.ij1+ self.biaslayer2
        self.a2 = self.sigmoid(self.z2)
        #ij matrix output
        self.ij2=np.dot(self.a2, self.W2)
        self.z3 = nself.ij2 + self.biaslayer3
        yHat = self.sigmoid(self.z3)  # output 
        print yHat
        return yHat
        
    def sigmoid(self, z):
        #Apply sigmoid activation function to scalar, vector, or matrix
        return 1/(1+np.exp(-z))
    '''
    def tanh(self,z):
        return (( np.exp(z) - np.exp(-z)/( np.exp(z) + np.exp(-z))

    def tanhPrime(self,z):
        #Gradient of sigmoid
        out2 = np.tanh([z], out1)
        return 1-(out2*out2)
    '''
    def sigmoidPrime(self,z):
        #Gradient of sigmoid
        return np.exp(-z)/((1+np.exp(-z))**2)
    
    def costFunction(self, X, y):
        #Compute cost for given X,y, use weights already stored in class.
        #J=sigma(1/2(y=y^)^2)
        self.yHat = self.forward(X)
        J = 0.5*sum((y-self.yHat)**2)
        return J
        
    def costFunctionPrime(self, X, y):
        #Compute derivative with respect to W and W2 for a given X and y:
        '''
        self.yHat = self.forward(X)
        
        delta3 = np.multiply(-(y-self.yHat), self.sigmoidPrime(self.z3))
        print "testing"
        print self.a2.T
        print delta3
        dJdW2 = np.dot(self.a2.T, delta3)
        print dJdW2
        
        delta2 = np.dot(delta3, self.W2.T)*self.sigmoidPrime(self.z2)
        print "testing"
        print X.T
        print delta2
        dJdW1 = np.dot(X.T, delta2)
        print dJdW1  
        return dJdW1, dJdW2
        '''

Nobj=Neural_Network()
cost1=Nobj.costFunction(X,y)
dJdW1,dJdW2=Nobj.costFunctionPrime(X,y)
print("dJdW1 ",dJdW1)
print("dJdW2 ",dJdW2)
scalar=3
print("adding scalar to derivative :")
Nobj.W1=Nobj.W1+scalar*dJdW1
Nobj.W2=Nobj.W2+scalar*dJdW2
cost2=Nobj.costFunction(X,y)
print ("cost 1 : ",cost1)
print ("cost 2 : ",cost2)
if(cost1>cost2):
    print "cost has decreased,downhill"
else:
    print "cost has increased, uphill"
Nobj.W1=Nobj.W1-scalar*dJdW1
Nobj.W2=Nobj.W2-scalar*dJdW2
cost2=Nobj.costFunction(X,y)
print ("cost 1 : ",cost1)
print ("cost 2 : ",cost2)
if(cost1>cost2):
    print "cost has decreased,downhill"
else:
    print "cost has increased,uphill"
#yHat=Nobj.forward(X)
