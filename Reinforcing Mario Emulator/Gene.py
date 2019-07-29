class Gene:
    def __init__(self):
        self.into = 0
        self.out = 0
        self.weight = 0.0
        self.enabled = True
        self.innovation = 0  
        
    def copyGene(self):
        gene_two = Gene()
        gene_two.into = gene.into
        gene_two.out = gene.out
        gene_two.weight = gene.weight
        gene_two.enabled = gene.enabled
        gene_two.innovation = gene.innovation
    
        return gene2