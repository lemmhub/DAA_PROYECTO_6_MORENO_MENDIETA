class Arista(object):
    
    def __init__(self, u, v, attrs=None):
        self.u = u
        self.v = v
        self.id = (u.id, v.id)
        self.attrs = attrs

   