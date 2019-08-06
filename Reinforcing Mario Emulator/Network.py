from NeuralConstants import *
from Neuron import Neuron
import math

def sigmoid(x):
    return 2/(1+math.exp(-4.9*x))-1

class Network:
    def __init__(self, genome):
        self.neurons = [None for neur in range(MaxNodes + Outputs + 1)]
    
        for i in range(0,Inputs):
            self.neurons[i] = Neuron()
    
        for o in range(0,Outputs):
            self.neurons[MaxNodes + o] = Neuron()
    
        genome.genes = sorted(genome.genes, key=lambda k: k.out)        
        #table.sort(genome.genes, def (a,b)
        #    return (a.out < b.out)
        #end)
                 
        for i in range(0,len(genome.genes)):
            gene = genome.genes[i]
            if gene.enabled:
                #print(self.neurons[gene.out])
                try:
                    if self.neurons[gene.out] == None:
                        self.neurons[gene.out] = Neuron()
                except IndexError:
                    self.neurons[gene.out] = Neuron()               
                
                neuron = self.neurons[gene.out]
                neuron.incoming.append(gene)
                try:
                    if self.neurons[gene.into] == None:
                        self.neurons[gene.into] = Neuron()
                except IndexError:
                    pass
    
        #genome.network = network  
        
        
    def evaluateNetwork(self, inputs):
        #inputs.append(1)
        inputs[0] = 0
        #print(len(inputs))
        #print(inputs)
        if len(inputs) != Inputs:
            print("Incorrect number of neural network inputs.")
            return {}
    
        for i in range(0,Inputs):
            self.neurons[i].value = inputs[i]
            
        for neuron in self.neurons:
            sum = 0
            #if not neuron.equal(Neuron()):
            #    print("HELLOOOO")
            #    print(neuron.incoming)
            #    print(neuron.value)
            if neuron != None:
                for incoming in neuron.incoming:
                    other = self.neurons[incoming.into]
                    sum = sum + incoming.weight * other.value
        
                if len(neuron.incoming) > 0:
                    neuron.value = sigmoid(sum)
                
        outputs = {}
        for o in range(0,Outputs):
            button = ButtonNames[o]
            #if self.neurons[MaxNodes+o].value > 0:
            if self.neurons[MaxNodes + o].value > 0:
                outputs[button] = True
            else:
                outputs[button] = False
    
        return outputs