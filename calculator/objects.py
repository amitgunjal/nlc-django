class Operand:
    def __init__(self, v, n, d):
        self.value = v
        self.numerators = n
        self.denominators = d
    def __repr__(self):
        return '<Operand: {0}>'.format(self.value)