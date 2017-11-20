# MOEA for CNN architecture tuning

__We aim to automatically tune optical CNN architectures for different tasks using Multiobjective Evolutionary Algorithm. An optical CNN architecture should either have higher accuracy or have smaller number of parameters to save memory and computation.__

## Evolutionary Algorithms, EAs
Evolutionary Algorithms (EAs) are a non-deterministic algorithm to solve optimization problems for optimal solutions.

## Multiobjective Evolutionary Algorithms, MOEAs
If an optimization problem is designed to have multiple evaluation functions

There exists a lot of MOEAs, among which NSGAII and MOEA/D are two classic ones. NSGAII ranks the solutions based on their non-domination condition, dominated by less solutions, ranks topper. And then select top ranked solutions as the next generation to reproduce new solutions. However, MOEA/D decomposes the objectives to a lot of diversely distributed single objective sub-problems, so solutions are generated and compared on each sub-problem. In fact, each sub-problem is a weighted sum of all the objectives of the optimization problem. We, in this project, utilize NSGAII as NSGAII is easy to understand and implement, and is more general without problem-specific knowledge, while MOEA/D will need user's knowledge of the problems they are solving. MOEA/D is mainly designed for continuous optimization problems and the core-part of MODEA/D is the design of weights to define sub-problems. For example, the objectives/evaluation standards of convolutional neural network (CNN) aren't to the same scale, accuracy and number of parameters involved for example, which would need users' professional knowledge to design weights for different tasks/datasets.

## Convolutional Neural Network, CNN

Convolutional neural network (CNN) imitates the working mechanisms of animal brain, which consists of input layer, output layer, and hidden layer. The hidden layer is like a black box, which is usually composed by multiple convolutional layers, multiple pooling layers, and multiple fully connected layers. CNN is mainly used for classification. We can see CNN as a nonlinear fitting of data of the same kind or sampled on the same distribution. Our goal is feeding a CNN huge amount of labeled data to train network parameters. The resulting CNN is used to classify unlabeled data of the same kind. The better the resulting CNN fit the data, the more accurate the prediction would be, where overfitting is a special case to consider. It makes sense that we will need deeper and bigger network for more complicated dataset, which in turn results increasing classification accuracy and increasing number of network parameters.

With the increasing memory space and computing capability, and huge amount of data, we hope to obtain satisfying classification results in a limited budget.

## Corresponding Genotype Construction
CNN can be completely defined by a proper designed genotype, with each layer as a gene in the genotype. And a genotype is a solution of evolutionary algorithms. Gene types can either below:

- Input layer (One)
- Convolutional layers (Multiple)
- Pooling layer (Multiple)
- Fully connected layer (Multiple)
- Output layer (One)

__Constructing a genotype and checking its validity.__ Each layer of CNN has input, output, and meta-parameters. Use a N x N gray image as an example:

Network layer|Input size|Meta parameters|Output size
---|---|---|---
Input layer|(N, N)|None|(N, N)
Convolutional layer|(N1, N2, NK)|Kernel size: (K1, K2), Stride: (S1, S2),Number of kernels: NK_c|( (N1-K1)/S1+1, (N2-K2)/S2+1, NK_c )
Pooling layer|(N1, N2, NK)|Pool size: (P1, P2), Stride: (S1, S2)|( (N1-P1)/S1+1, (N2-P2)/S2+1, NK )
Fully connected layer|(N1, N2, NK)|Number of nodes: NF|NF
Output layer|NF|Number of classes: C|C

With a genotype, we can build the CNN. We can also calculate the number of parameters, which is the first objective; we train the network and evaluate its classification accuracy, which is the second objective. Definitely, users can define different evaluation standards as objectives.

A valid genotype should be subject to the following:

- A genotype starts with a input layer, which is determined only by input data.
- A genotype ends with a output layer, which is determined only by the number of classes.
- Meta-parameters of each gene/layer must be no bigger than related input of the layer, so that it has valid output.

Constraints on each kind of gene layer:

Gene layer| Forward gene constraint| Backward gene constraint
---|---|---
Input layer| None| Convolutional layer, pooling layer, fully connected layer, or output layer
Output layer|  Input layer, convolutional layer, pooling layer, or fully connected layer| None
Convolutional layer| Input layer, convolutional layer, or pooling layer| Convolutional layer, pooling layer, fully connected layer, or output layer
Pooling layer| Input layer, convolutional layer, or pooling layer| Convolutional layer, pooling layer, fully connected layer, or output layer
Fully connected layer| Input layer, convolutional layer, pooling layer, or fully connected layer| Fully connected layer or output layers


## Operators: crossover and computation

