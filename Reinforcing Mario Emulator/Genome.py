import random

def sigmoid(x):
    return 2/(1+math.exp(-4.9*x))-1

class Genome:
    def __init__(self, pool):
        self.genes = []
        self.pool = pool
        self.fitness = 0
        self.adjustedFitness = 0
        self.network = {}
        self.maxneuron = 0
        self.globalRank = 0
        self.mutationRates = {}
        self.mutationRates["connections"] = MutateConnectionsChance
        self.mutationRates["link"] = LinkMutationChance
        self.mutationRates["bias"] = BiasMutationChance
        self.mutationRates["node"] = NodeMutationChance
        self.mutationRates["enable"] = EnableMutationChance
        self.mutationRates["disable"] = DisableMutationChance
        self.mutationRates["step"] = StepSize
        
    def clone(self):
        genome_two = Genome()

        genome_two.genes = self.genes[:]
        genome_two.maxneuron = self.maxneuron
        genome_two.mutationRates["connections"] = self.mutationRates["connections"]
        genome_two.mutationRates["link"] = self.mutationRates["link"]
        genome_two.mutationRates["bias"] = self.mutationRates["bias"]
        genome_two.mutationRates["node"] = self.mutationRates["node"]
        genome_two.mutationRates["enable"] = self.mutationRates["enable"]
        genome_two.mutationRates["disable"] = self.mutationRates["disable"]
    
        return genome_two
    
    
    def nodeMutate(self):
        if len(self.genes) == 0:
            return
    
        self.maxneuron = self.maxneuron + 1
    
        gene = self.genes[random.randint(1,len(self.genes))]
        if not gene.enabled:
            return
        
        gene.enabled = False
    
        gene_one = gene.clone()
        gene_one.out = self.maxneuron
        gene_one.weight = 1.0
        ########################################################NEW INNOVATION
        gene_one.innovation = self.pool.new_innovation()
        gene_one.enabled = True
        table.insert(self.genes, gene_one)
    
        gene_two = gene.clone()
        gene_two.into = self.maxneuron
        gene_two.innovation = self.pool.new_innovation()
        gene_two.enabled = True
        table.insert(self.genes, gene_two)
     
    
    def enableDisableMutate(enable):
        candidates = []
        for gene in self.genes:
            if gene.enabled != enable:
                candidates.append(gene)
    
        if len(candidates) == 0:
            return
    
        gene = candidates[random.randint(1,len(candidates))]
        gene.enabled = not gene.enabled 
    
    def mutate(self):
        for mutation,rate in self.mutationRates.items():
            if random.randint(1,2) == 1:
                genome.mutationRates[mutation] = 0.95 * rate
            else:
                genome.mutationRates[mutation] = 1.05263 * rate
    
        if random.random() < genome.mutationRates["connections"]:
            self.point_mutate()

        p = self.mutationRates["link"]
        while p > 0:
            if random.random() < p:
                self.linkMutate(False)
            p = p - 1
    
        p = self.mutationRates["bias"]
        while p > 0:
            if random.random() < p:
                self.linkMutate(True)
            p = p - 1
    
        p = self.mutationRates["node"]
        while p > 0:
            if random.random() < p:
                self.nodeMutate()
            p = p - 1
    
        p = self.mutationRates["enable"]
        while p > 0:
            if random.random() < p:
                self.enableDisableMutate(True)
            p = p - 1
    
        p = self.mutationRates["disable"]
        while p > 0:
            if random.random() < p:
                self.enableDisableMutate(False)
            p = p - 1
            
    
    def basicGenome(self, pool):
        #I think this line is useless
        self.__init__(pool)
        innovation = 1
    
        self.maxneuron = Inputs
        self.mutate()
        
    def crossover(self, other):
        # Make sure self is the higher fitness genome
        if other.fitness > self.fitness:
            tempg = self
            self = other
            other = tempg
    
        child = Genome()
    
        innovations2 = {}
        for i in range(0,len(other.genes)):
            gene = other.genes[i]
            innovations2[gene.innovation] = gene
    
        for i in range(0,len(self.genes)):
            gene1 = self.genes[i]
            gene2 = innovations2[gene1.innovation]
            if gene2 != None and math.random(2) == 1 and gene2.enabled:
                table.insert(child.genes, gene2.clone())
            else:
                table.insert(child.genes, gene1.clone())
    
        child.maxneuron = max(self.maxneuron, other.maxneuron)
    
        for mutation,rate in self.mutationRates.items():
            child.mutationRates[mutation] = rate
    
        return child

    def contains_link(self, link):
        for i in range(0,len(self.genes)):
            gene = self.genes[i]
            if gene.into == link.into and gene.out == link.out:
                return True
        return False    
    
    def point_mutate(self):
        step = self.mutationRates["step"]
    
        for i in range(0,len(self.genes)):
            gene = self.genes[i]
            rand = random.random()            
            if rand < PerturbChance:
                gene.weight = gene.weight + rand * step * 2 - step
            else:
                gene.weight = rand * 4 - 2  
                
    def randomNeuron(self, nonInput):
        genes = self.genes
        neurons = []
        if not nonInput:
            for i in range(0,Inputs):
                neurons.append(True)
        #Might not be required
        else:
            for i in range(0,Inputs):
                neurons.append(False)            

        for o in range(0, Outputs):
            neurons.append(True)

        for i in range(0,len(genes)):
            if (not nonInput) or genes[i].into > Inputs:
                neurons[genes[i].into] = True
            if (not nonInput) or genes[i].out > Inputs:
                neurons[genes[i].out] = True

        count = 0
        for neuron in neurons:
            if neuron:
                count = count + 1

        n = random.randint(1, count)

        for k,v in enumerate(neurons):
            n = n-1
            if n == 0:
                return k

        return 0    
    
    def linkMutate(self, forceBias):
        neuron1 = self.randomNeuron(False)
        neuron2 = self.randomNeuron(True)
    
        newLink = Gene()
        if neuron1 <= Inputs and neuron2 <= Inputs:
            #Both input nodes
            return
        
        if neuron2 <= Inputs:
            # Swap output and input
            temp = neuron1
            neuron1 = neuron2
            neuron2 = temp
        
    
        newLink.into = neuron1
        newLink.out = neuron2
        if forceBias:
            newLink.into = Inputs
        
        if self.contains_link(newLink):
            return
        
        newLink.innovation = self.pool.new_innovation()
        newLink.weight = random.random()*4-2
    
        self.genes.append(newLink)
        
    def disjoint(self, other):
        i1 = {}
        for i in range(0,len(self.genes)):
            gene = self.genes[i]
            i1[gene.innovation] = True
    
        i2 = {}
        for i in range(0,len(other.genes)):
            gene = other.genes[i]
            i2[gene.innovation] = True
    
        disjointGenes = 0
        for i in range(0,len(self.genes)):
            gene = self.genes[i]
            if not i2[gene.innovation]:
                disjointGenes = disjointGenes+1
    
        for i in range(0,len(other.genes)):
            gene = other.genes[i]
            if not i1[gene.innovation]:
                disjointGenes = disjointGenes+1
    
        n = math.max(len(self.genes), len(other.genes))
    
        return disjointGenes / n     
        
        
    def weights(self, other):
        i_two = {}
        for i in range(0,len(other.genes)):
            gene = other.genes[i]
            i_two[gene.innovation] = gene
    
        sum = 0
        coincident = 0
        for i in range(0,len(self.genes)):
            gene = self.genes[i]
            if i_two.get(gene.innovation, None) != None:
                gene_two = i_two[gene.innovation]
                sum = sum + math.abs(gene.weight - gene_two.weight)
                coincident = coincident + 1
    
        return sum / coincident        
        
        
    def sameSpecies(self, other):
        dd = DeltaDisjoint * self.disjoint(other)
        dw = DeltaWeights * self.weights(other) 
        return dd + dw < DeltaThreshold
    
    '''def displayGenome(genome):
        local network = genome.network
        local cells = {}
        local i = 1
        local cell = {}
        for dy=-BoxRadius,BoxRadius do
            for dx=-BoxRadius,BoxRadius do
                cell = {}
                cell.x = 50+5*dx
                cell.y = 70+5*dy
                cell.value = network.neurons[i].value
                cells[i] = cell
                i = i + 1
            end
        end
        local biasCell = {}
        biasCell.x = 80
        biasCell.y = 110
        biasCell.value = network.neurons[Inputs].value
        cells[Inputs] = biasCell
    
        for o = 1,Outputs do
            cell = {}
            cell.x = 220
            cell.y = 30 + 8 * o
            cell.value = network.neurons[MaxNodes + o].value
            cells[MaxNodes+o] = cell
            local color
            if cell.value > 0 then
                color = 0xFF0000FF
            else
                color = 0xFF000000
            end
            gui.drawText(223, 24+8*o, ButtonNames[o], color, 9)
        end
    
        for n,neuron in pairs(network.neurons) do
            cell = {}
            if n > Inputs and n <= MaxNodes then
                cell.x = 140
                cell.y = 40
                cell.value = neuron.value
                cells[n] = cell
            end
        end
    
        for n=1,4 do
            for _,gene in pairs(genome.genes) do
                if gene.enabled then
                    local c1 = cells[gene.into]
                    local c2 = cells[gene.out]
                    if gene.into > Inputs and gene.into <= MaxNodes then
                        c1.x = 0.75*c1.x + 0.25*c2.x
                        if c1.x >= c2.x then
                            c1.x = c1.x - 40
                        end
                        if c1.x < 90 then
                            c1.x = 90
                        end
    
                        if c1.x > 220 then
                            c1.x = 220
                        end
                        c1.y = 0.75*c1.y + 0.25*c2.y
    
                    end
                    if gene.out > Inputs and gene.out <= MaxNodes then
                        c2.x = 0.25*c1.x + 0.75*c2.x
                        if c1.x >= c2.x then
                            c2.x = c2.x + 40
                        end
                        if c2.x < 90 then
                            c2.x = 90
                        end
                        if c2.x > 220 then
                            c2.x = 220
                        end
                        c2.y = 0.25*c1.y + 0.75*c2.y
                    end
                end
            end
        end
    
        gui.drawBox(50-BoxRadius*5-3,70-BoxRadius*5-3,50+BoxRadius*5+2,70+BoxRadius*5+2,0xFF000000, 0x80808080)
        for n,cell in pairs(cells) do
            if n > Inputs or cell.value ~= 0 then
                local color = math.floor((cell.value+1)/2*256)
                if color > 255 then color = 255 end
                if color < 0 then color = 0 end
                local opacity = 0xFF000000
                if cell.value == 0 then
                    opacity = 0x50000000
                end
                color = opacity + color*0x10000 + color*0x100 + color
                gui.drawBox(cell.x-2,cell.y-2,cell.x+2,cell.y+2,opacity,color)
            end
        end
        for _,gene in pairs(genome.genes) do
            if gene.enabled then
                local c1 = cells[gene.into]
                local c2 = cells[gene.out]
                local opacity = 0xA0000000
                if c1.value == 0 then
                    opacity = 0x20000000
                end
    
                local color = 0x80-math.floor(math.abs(sigmoid(gene.weight))*0x80)
                if gene.weight > 0 then 
                    color = opacity + 0x8000 + 0x10000*color
                else
                    color = opacity + 0x800000 + 0x100*color
                end
                gui.drawLine(c1.x+1, c1.y, c2.x-3, c2.y, color)
            end
        end
    
        gui.drawBox(49,71,51,78,0x00000000,0x80FF0000)
    
        #if forms.ischecked(showMutationRates) then
        #	local pos = 100
        #	for mutation,rate in pairs(genome.mutationRates) do
        #		gui.drawText(100, pos, mutation .. ": " .. rate, 0xFF000000, 10)
        #		pos = pos + 8
        #	end
        #end
    end '''    