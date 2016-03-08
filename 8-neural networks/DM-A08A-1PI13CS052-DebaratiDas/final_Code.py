import numpy as np
import math

def tanh_function(x):
    return math.tanh(x)

class NeuralNetwork:

	def __init__(self, layers):
		self.activation = tanh_function # range of weight values (-1,1)
		
		np.random.seed(2) #predictable 
		#3X2 matrix of weights from input to hidden layer
		self.w1 = 2*np.random.random((layers[1], layers[0])) -1 
		#2X2 matrix of weights from input to hidden layer
		self.w2 = 2*np.random.random( (layers[2], layers[1])) - 1
		#bias for hidden layer units
		self.b1 = 2*np.random.random((1,2)) -1 
		#bias for output layer units
		self.b2 = 2*np.random.random((1,2)) -1 
	
		print("...INITIALY, MODEL'S Learnable parameters... :")
		print("Weights and Bases: ")
		self.display()
		
	def display(self):
		self.display_params(self.w1,self.b1,[4,5],[1,2,3])
		self.display_params(self.w2,self.b2,[6,7],[4,5])
	
	def display_params(self,weight,bias,to_node,from_node):
		for i in range(len(to_node)):
			print("For Neuron ",to_node[i])
			print("Contributing neurons are :")
			for j in range(len(from_node)):
				print("\tNeuron"+str(from_node[j])+"\t"+"{0:.2f}".format(weight[i][j]))
			print("\tBias at this node is : \t"+"{0:.2f}".format(bias[0][i]))
			print("____________________________________________________________________")
		print()

	def train(self, X, y, learning_rate=0.2,epochs=1000):
         
		print("Number of iterations = ",epochs)
		
		for k in range(epochs):
			# ------ Forward Propagation ---------- #
			#LAYER 2
			a=[] #output from the hidden layer
			ij1 = []
			for l in range(2):
					dot_value = np.dot(X,self.w1[l]) # Iij=sigma(w(ij)*X)
					dot_value += self.b1[0][l] # z= Iij+bias
					ij1.append(dot_value) # this list will contain all z's before the activation function applied
					activation = self.activation(dot_value) # after activation is applied 
					a.append(activation) # this list contains all values after activation or outputs (Oij)
			
			#LAYER2
			b=[] #final output layer
			ij2 = []
			for l in range(2):
					dot_value = np.dot(a,self.w2[l]) # Iij=sigma(w(ij)*X)
					dot_value += self.b2[0][l] # z= Iij+bias
					ij2.append(dot_value)
					activation = self.activation(dot_value)
					b.append(activation)# this list contains all values after activation or outputs (Oij)

			#------Back propagate error ---------#
			# At output layer
			b = np.array(b)
			m1 = y- b # target output- predicted output
			m2 = [4*math.e**(2*x)/(math.e**(2*x)+1)**2 for x in ij2] # optimises the cost function
			m3 = np.multiply(m1,m2) #error at output unit
			
			# At hidden layer
			a = np.array(a)
			n1 = 1-a
			transposed = self.w2.T
			err =[]
			for i in range(2):
				err.append(np.dot(transposed[i],m3))
			err = np.array(err)
			n2 = [4*math.e**(2*x)/(math.e**(2*x)+1)**2 for x in ij1]
			n3 = np.multiply(n2,err) #Oj*(1-Oj)*sigma
			
			self.b1 += learning_rate*n3 #update biases for the intermediate layer
			self.b2 += learning_rate*m3 #update biases for the output layer
			
			#------Update errors and Biases  ---------#
			for i in range(2):
				j = n3[i]*X
				self.w1[i] = self.w1[i] + learning_rate*j #update weights to the hidden layer
				
			for i in range(2):
				j = a*m3[i]
				self.w2[i] = self.w2[i] + learning_rate*j #update weights to the output layer	
				
		print("...Finally, MODEL'S Learnable parameters... :")
		print("Weights and Bases: ")
		self.display()
		print("FINAL OUTPUTS:\n")
		self.output(a,[4,5])
		self.output(b,[6,7])
		
	def output(self,arr,fro):
		for i in range(len(fro)):
			print("Node "+str(fro[i])+"\t"+"{0:.3f}".format(arr[i]))
		print()
		
		
		
if __name__ == '__main__':

	Nobj = NeuralNetwork([3,2,2])
	X = np.array([1,0.25,-0.5])
	y = np.array([1,-1])	
	Nobj.train(X, y)
	print("____________________________________________________________________")