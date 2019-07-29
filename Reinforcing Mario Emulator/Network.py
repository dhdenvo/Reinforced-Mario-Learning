def sigmoid(x):
    return 2/(1+math.exp(-4.9*x))-1

class Network:
    def __init__(self, genome):
        self.neurons = []
    
        for i in range(0,Inputs):
            self.neurons.append(Neuron())
    
        for o in range(0,Outputs):
            self.neurons.append(Neuron())
    
        genome.genes = sorted(genomes.genes, key=lambda k: k.out)        
        #table.sort(genome.genes, def (a,b)
        #    return (a.out < b.out)
        #end)
        
        for i in range(0,len(genome.genes)):
            gene = genome.genes[i]
            if gene.enabled:
                if self.neurons[gene.out] == None:
                    self.neurons[gene.out] = Neuron()
                
                neuron = self.neurons[gene.out]
                neuron.incoming.append(gene)
                if self.neurons[gene.into] == None:
                    self.neurons[gene.into] = Neuron()
    
        #genome.network = network  
        
        
    def evaluateNetwork(self, inputs):
        inputs.append(1)
        if len(inputs) != Inputs:
            #console.writeline("Incorrect number of neural network inputs.")
            print("Incorrect number of neural network inputs.")
            return {}
    
        for i in range(0,Inputs):
            self.neurons[i].value = inputs[i]
    
        for neuron in self.neurons:
            sum = 0
            for j in range(0,len(neuron.incoming)):
                incoming = neuron.incoming[j]
                other = self.neurons[incoming.into]
                sum = sum + incoming.weight * other.value
    
            if len(neuron.incoming) > 0:
                neuron.value = sigmoid(sum)
    
        outputs = []
        for o in range(0,Outputs):
            button = ButtonNames[o]
            if self.neurons[MaxNodes+o].value > 0:
                outputs.append(True)
            else:
                outputs.append(False)
    
        return outputs