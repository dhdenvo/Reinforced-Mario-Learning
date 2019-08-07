from NeuralConstants import *
from Neuron import Neuron
import math

def sigmoid(x):
    return 2/(1+math.exp(-4.9*x))-1

class Network:
    def __init__(self, genome):
        self.neurons = {}
    
        for i in range(1,Inputs + 1):
            self.neurons[i] = Neuron()
    
        for o in range(1,Outputs + 1):
            self.neurons[MaxNodes + o] = Neuron()
    
        genome.genes = sorted(genome.genes, key=lambda k: k.out)        
        #table.sort(genome.genes, def (a,b)
        #    return (a.out < b.out)
        #end)
                 
        for i in range(1,len(genome.genes) + 1):
            gene = genome.genes[i - 1]
            if gene.enabled:
                #print(self.neurons[gene.out])
                #if self.neurons.get(gene.out, None) == None:
                #    self.neurons[gene.out] = Neuron()       
                self.neurons.setdefault(gene.out, Neuron())
                
                neuron = self.neurons[gene.out]
                neuron.incoming.append(gene)
                #if self.neurons.get(gene.into, None) == None:
                #    self.neurons[gene.into] = Neuron()
                self.neurons.setdefault(gene.into, Neuron())
            
    
        #genome.network = network  
        
        
    def evaluateNetwork(self, inputs):
        q = list(inputs.keys())[-1]
        z = len(inputs)        
        inputs[list(inputs.keys())[-1] + 1] = 1
        x = list(inputs.keys())[-1]
        y = len(inputs)
                
        '''for x in range(0, BoxRadius*2+1):
            for y in range(0, BoxRadius*2+1):
                print(inputs[(x + 1) * (y + 1)], end="")
            print("")
        print("")'''
        
        if len(inputs) != Inputs:
            print("Incorrect number of neural network inputs.")
            return {}
    
        for i in range(1,Inputs + 1):
            self.neurons[i].value = inputs[i]
            
        for neuron in self.neurons.values():
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
        for o in range(1,Outputs + 1):
            button = ButtonNames[o - 1]
            #if self.neurons[MaxNodes+o].value > 0:
            if self.neurons[MaxNodes + o].value > 0:
                outputs[button] = True
            else:
                outputs[button] = False
    
        return outputs