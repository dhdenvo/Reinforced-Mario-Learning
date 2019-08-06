import random
from Genome import Genome

class Species:
    def __init__(self):
        self.topFitness = 0
        self.staleness = 0
        self.genomes = []
        self.averageFitness = 0
    
    def calculateAverageFitness(self):
        total = 0
    
        for g in range(0,len(self.genomes)):
            genome = self.genomes[g]
            total = total + genome.globalRank
    
        self.averageFitness = total / len(self.genomes)   
        
    def breedChild(self):
        child = Genome()
        if random.random() < CrossoverChance:
            g1 = self.genomes[random.randint(1, len(self.genomes))]
            g2 = self.genomes[random.randint(1, len(self.genomes))]
            child = g1.crossover(g2)
        else:
            g = self.genomes[random.randint(1, len(self.genomes))]
            child = g.clone()
    
        child.mutate()
        return child  