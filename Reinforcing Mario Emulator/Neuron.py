class Neuron:
    def __init__(self):
        self.incoming = []
        self.value = 0.0
        
    def equal(self, other):
        #equal = self.value == other.value
        equal = True
        if len(self.incoming) != len(other.incoming):
            return False
        for i, inc in enumerate(self.incoming):
            if inc != other.incoming[i]:
                return False
        return equal