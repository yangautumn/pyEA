## Gene.py
##
##

"""
1. What is the dimensionality for each gene type?

INPUT - [ m * n * k] - This is the case for a 2D gene (i.e., image)
        [ m * k ] - This is the case for a 1D gene (i.e., accelerometer)

2. Constraints on kernel_size, stripe or num_kernels when generating random Genes?

3. Can we sample on a Gaussion distribution to get the number of conv and pooling?
	Also number of fully connected?

"""


# Enumerate the different gene types
INPUT = "INPUT"
CONV1D = "CONV1D"
CONV2D = "CONV2D"
POOL1D = "POOL1D"
POOL2D = "POOL2D"
FULLY_CONNECTED = "FULLYCONNECTED"

import random
import numpy as np
from models.parts import *


MIN_CNN_WIDTH = 2
MAX_CNN_WIDTH = 75
MIN_CNN_KERNELS = 5
MAX_CNN_KERNELS = 30
MIN_CNN_STRIDE = 1
MAX_CNN_STRIDE = 5
MIN_POOL_SIZE = 2
MAX_POOL_SIZE = 5
MIN_POOL_STRIDE = 1
MAX_POOL_STRIDE = 5
MIN_FULL_CONNECTION = 5
MAX_FULL_CONNECTION = 200


class Gene:
	"""
	An abstract gene.
	"""

	def __init__(self):
		"""
		Create a new gene.  This shouldn't do anything for this abstract class
		"""


		# What type of gene is this?  Since this is abstract, it isn't anything
		self.type = None


 
	def canFollow(self, prevGene):
		"""
		Can this gene follow the previous gene?  I.e., are all constraints satisfied?
		"""

		pass


	#### Why was outputDimension hidden (two underlines makes it 'private' in Python)?  --Dana
	def outputDimension(self, prevGene):
		"""
		What is the dimensionality of the output of this gene?
		"""

		return None


	def mutate(self, prevGene, nextGene):
		"""
		Alter this gene, ensuring that the constraints from the previous and next gene are satisfied
		"""

		pass


	def generateLayer(self, name_suffix):
		"""
		Create the CNN part(s) (tuple of objects) used to construct this particular layer in the CNN
		"""

		pass


class InputGene(Gene):
	"""
	"""
	def __init__(self, input_shape):
		"""
		Placeholder gene for the input dimensionality of the problem set
		input_shape = (height, width, num_channels) (2D data)
						  (length, num_channels) (1D data)
		"""

		self.dimension = input_shape
		self.type = INPUT

	def canFollow(self, prevGene=None):
		"""
		This never follows a gene, it's the input
		"""

		return False

#		if prevGene is not None:
#			return False
#		else:
#			return True

	def outputDimension(self, prevGene=None):
		"""
		"""
		assert prevGene is None, "There shouldn't be prevGene for InputGene!"
		return self.dimension

	def mutate(self, prevGene, nextGene):
		"""
		"""
		assert prevGene is None, "The input should not have previous gene!"
		print "You are mutating an input, not allowed!"


class Conv1DGene(Gene):
	"""
	"""
	def __init__(self, kernel_shape, stride, num_kernels, activation_function):
		"""
		kernel_shape - should be a 1-tuple, e.g, (20,)
		stride       - should be a 1-tuple, e.g, (2,)
		num_kernels  - should be an integer
		activation_function - a Tensorflow activation tensor (e.g., tf.sigmoid)
		"""

		self.kernel_shape = kernel_shape
		self.stride = stride
		self.num_kernels = num_kernels
		self.activation = activation_function

		self.type = CONV1D
		# dimension = (height, width, kernels)
		self.dimension = None

	def canFollow(self, prevGene):
		"""
		A Conv1Dgene can follow an 'InputGene' or an 'Pool1DGene'
		The constraints are kernel_size should not larger than prevGene.output_size
		"""
		if prevGene.type == INPUT or prevGene.type == POOL1D:
			## next step is to see if 
			prevLength, channels = prevGene.dimension

			return self.kernel_shape[0] <= prevLength
		else:
			return False

	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		assert prevGene.dimension.shape == 2, "prevGene output needs to be (length, channels) in shape!"

		prevLength, channels = prevGene.dimension
		myLength = (prevLength - self.kernel_size[0])/self.stride[0] + 1

		self.dimension = (myLength, self.num_kernels)
		return self.dimension


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_kernels should be mutated based on the constraints from prevGene and nextGene
		"""
		pass


class Conv2DGene(Gene):
	"""
	"""
	def __init__(self, kernel_shape, stride, num_kernels, activation_function):
		"""
		kernel_shape - should be a 2-tuple, e.g, (20,20)
		stride       - should be a 2-tuple, e.g, (2,2)
		num_kernels  - should be an integer
		activation_function - a Tensorflow activation tensor (e.g., tf.sigmoid)
		"""
		self.kernel_shape = kernel_shape
		self.stride = stride
		self.num_kernels = num_kernels
		self.activation = activation_function

		self.type = CONV2D
		self.dimension = None


	def canFollow(self, prevGene):
		"""
		A Conv2Dgene can follow an 'InputGene', 'Conv2DGene' or an 'Pool2DGene'
		The constraints are kernel_size should not larger than prevGene.output_size
		"""
		if prevGene.type == INPUT or prevGene.type == CONV2D or prevGene.type == POOL2D:
			## next step is to see if 
			height, width, channels = prevGene.dimension
			return self.kernel_shape[0] <= height and self.kernel_shape[1] <= width
		else:
			return False


	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		prevHeight, prevWidth, channels = prevGene.dimension
		myHeight = (prevHeight - self.kernel_size) / self.stride + 1
		myWidth = (prevWidth - self.kernel_size) / self.stride + 1

		self.dimension = (myHeight, myWidth, self.num_kernels)
		return self.dimension

	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_kernels should be mutated based on the constraints from prevGene and nextGene
		"""
		pass


class Pool1DGene(Gene):
	"""
	"""
	def __init__(self, pool_size, stride):
		"""
		pool_size    - should be a 1-tuple, e.g, (2,)
		stride       - should be a 1-tuple, e.g, (2,)
		"""

		self.pool_shape = pool_shape
		self.stride = stride

		self.type = POOL1D
		self.dimension = None

	def canFollow(self, prevGene):
		"""
		A Pool1DGene can only follow an 'Conv1DGene', or 'InputGene' (unusual, though, perhaps don't allow this?)
		"""

		prevLength, num_channels = prevGene.dimension

		if prevGene.type == CONV1D or prevGene.type == INPUT:
			return self.pool_shape[0] <= prevLength
		else:
			return False

	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		prevLength, num_kernels = prevGene.dimension
		myLength = (prevLength - self.pool_shape[0]) / self.stride[0] + 1

		self.dimension = (myLength, num_kernels)
		return self.dimension


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_kernels should be mutated based on the constraints from prevGene and nextGene		
		"""

		pass


class Pool2DGene(Gene):
	"""
	"""
	def __init__(self, pool_shape, stride):
		"""
		pool_size    - should be a 2-tuple, e.g, (2,2)
		stride       - should be a 2-tuple, e.g, (2,2)
		"""
		self.pool_shape = pool_shape
		self.stride = stride

		self.type = POOL2D
		self.dimension = None

	def canFollow(self, prevGene):
		"""
		A Pool2DGene can only follow an 'Conv2DGene' or 'InputGene'
		"""

		prevHeight, prevWidth, channels = prevGene.dimension

		if prevGene.type == CONV2D or prevGene.type == INPUT:
			return pool_shape[0] <= prevHeight or pool_shape[1] <= prevWidth
		else:
			return False

	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		prevHeight, prevWidth, channels = prevGene.dimension
		myHeight = (prevHeight - self.pool_shape[0]) / self.stride[0] + 1
		myWidth = (prevWidth - self.pool_shape[1]) / self.stride[1] + 1

		self.dimension = (myHeight, myWidth, channels)
		return self.dimension

	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_kernels should be mutated based on the constraints from prevGene and nextGene		
		"""
		pass


class FullyConnectedGene(Gene):
	"""
	"""
	def __init__(self, size, activation_function):
		"""
		size                - number of neurons (integer)
		activation_function - e.g., tf.sigmoid
		"""
		self.size = size
		self.activation = activation_function

		self.type = FULLY_CONNECTED
		self.dimension = size

	def canFollow(self, prevGene):
		"""
		A FullyConnectedGene can follow any of the other types of genes
		"""

		return True


	def outputDimension(self, prevGene):
		"""
		Calculate the output dimension based on the input dimension, kernel_size, and stride
		"""

		return self.dimension


	def mutate(self, prevGene, nextGene):
		"""
		kernel_size, stride and num_kernels should be mutated based on the constraints from prevGene and nextGene		
		"""
		pass

"""
# Helper function
# randomly generate a ConvGene based on the lastGene's output dimension
"""
def generateConvGene(ConvGene, lastGene):
	## specify the min and max for each random functions
	max_size = min(MAX_CNN_WIDTH, lastGene.dimension[0])
	kernel_size = np.random.randint(MIN_CNN_WIDTH, max_size+1)
	conv_stride = np.random.randint(MIN_CNN_STRIDE, MAX_CNN_STRIDE+1)
	num_kernels = np.random.randint(MIN_CNN_KERNELS, MAX_CNN_KERNELS+1)

	# activation_function ???
	return ConvGene(kernel_size, conv_stride, num_kernels, activation_function=None)

"""
# Helper function
# randomly generate a PoolGene based on the lastGene's output dimension
"""
def generatePoolGene(PoolGene, lastGene):
	## specify the min and max for each random functions
	max_size = min(MAX_POOL_SIZE, lastGene.dimension[0])
	pool_size = np.random.randint(MIN_POOL_SIZE, max_size+1)
	pool_stride = np.random.randint(MIN_POOL_STRIDE, MAX_POOL_STRIDE+1)

	# activation_function ???
	return PoolGene(pool_size, pool_stride, lastGene.num_kernels, activation_function=None)

"""
# Helper function
# randomly generate a FullyConnectedGene based on the lastGene's output dimension
"""
def generateFullConnectedGene(FullyConnectedGene, lastGene):
	## specify the min and max for each random functions
	size = np.random.randint(MIN_FULL_CONNECTION, MAX_FULL_CONNECTION+1)

	# activation_function ???
	return FullyConnectedGene(size, activation_function=None)

"""
Create a list of genes that describes a random, valid CNN
"""
def generateGenotypeProb(input_size, output_size, ConvProb, PoolProb=1.0, FullConnectProb = 0.5):

	# Is this a 1D or 2D input shape?
	if input_size.shape == 2:
		is2D = False
	else:
		is2D = True

	# Pick out the appropriate Gene types
	if is2D:
		ConvGene = Conv2DGene
		PoolGene = Pool2DGene
	else:
		ConvGene = Conv1DGene
		PoolGene = Pool1DGene

	lastGene = InputGene(input_size)
	genotype = [lastGene]
	print(lastGene.dimension)

	#### NOTE: May need to have two generateConvGene and generatePoolGene, for each possible shape (1D and 2D)

	# Add convolution layers (and possibly pooling layers) until a random check fails
	while random.random() < ConvProb:
		if MIN_CNN_WIDTH > lastGene.dimension[0]:
			break

		# Add the Convolution layer, with random arguments...
		tmpGene = generateConvGene(ConvGene, lastGene)
		print('kernel_size: {}, conv_stride: {}, num_kernels: {}'.format(tmpGene.kernel_shape, tmpGene.stride, tmpGene.num_kernels))
		if tmpGene.canFollow(lastGene):
			lastGene = tmpGene
			genotype.append(lastGene)
			print(lastGene.dimension)
			print("ConvGene added!")
		else:
			print("ConvGene can not follow lastGene!")
			print('Failed to create a Genotype!')
			print('=======================')
			return

		# Should a pooling layer be added?
		if random.random() < PoolProb:
			if MIN_POOL_SIZE > lastGene.dimension[0]:
				break
			tmpGene = generatePoolGene(PoolGene, lastGene)
			print('kernel_size: {}, pool_stride: {}, num_kernels: {}'.format(tmpGene.pool_shape, tmpGene.stride, tmpGene.num_kernels))
			if tmpGene.canFollow(lastGene):
				lastGene = tmpGene
				genotype.append(lastGene)
				print(lastGene.dimension)
				print("PoolGene added!")
			else:
				print("PoolGene can not follow lastGene!")
				print('Failed to create a Genotype!')
				print('=======================')
				return

	# Added all the Convolution layers, now add FC layers
	while random.random() < FullConnectProb:
		# Add a fully connected layer
		tmpGene = generateFullConnectedGene(FullyConnectedGene, lastGene)
		if tmpGene.canFollow(lastGene):
			lastGene = tmpGene
			genotype.append(lastGene)
			print(lastGene.dimension)
			print("FullyConnectedGene added!")
		else:
			print("FullyConnectedGene can not follow lastGene!")
			print('Failed to create a Genotype!')
			print('=======================')
			return

	print('Successfuly Created a Genotype!')
	print('=======================')

	return genotype