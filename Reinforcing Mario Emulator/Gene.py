class Gene:
    def __init__(self):
        self.into = 0
        self.out = 0
        self.weight = 0.0
        self.enabled = True
        self.innovation = 0  
        
    def clone(self):
        gene_two = Gene()
        gene_two.into = self.into
        gene_two.out = self.out
        gene_two.weight = self.weight
        gene_two.enabled = self.enabled
        gene_two.innovation = self.innovation
    
        return gene_two