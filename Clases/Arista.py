class Arista(object):
    
    def __init__(self, u, v, attrs=None):
        self.u = u
        self.v = v
        self.id = (u.id, v.id)
        self.attrs = dict()

    def __eq__(self, other):
        
        return self.u == other.u and self.v == other.v

    def __repr__(self):
        
        return repr(self.id)

    def agregar_peso(self, peso):
        self.attrs['peso'] = peso

    def __iter__ (self):
        return Arista(self.u,self.v)