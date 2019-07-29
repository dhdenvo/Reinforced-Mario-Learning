class Species:
    def __init__(self):
        self.topFitness = 0
        self.staleness = 0
        self.genomes = []
        self.averageFitness = 0

    def clone(self):
        gene_two = Gene()
        gene_two.into = self.into
        gene_two.out = self.out
        gene_two.weight = self.weight
        gene_two.enabled = self.enabled
        gene_two.innovation = self.innovation
    
        return gene_two
    
    def calculateAverageFitness(self):
        total = 0
    
        for g in range(0,len(self.genomes)):
            genome = self.genomes[g]
            total = total + genome.globalRank
    
        self.averageFitness = total / len(self.genomes)   
        
    def breedChild(self):
        child = {}
        if random.random() < CrossoverChance:
            g1 = self.genomes[random.randint(1, len(self.genomes))]
            g2 = self.genomes[random.randint(1, len(self.genomes))]
            child = crossover(g1, g2)
        else:
            g = self.genomes[random.randint(1, len(self.genomes))]
            child = g.clone()
    
        mutate(child)
        return child  