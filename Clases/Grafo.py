import sys
from Clases.Arista import Arista


class Grafo(object):
   
    def __init__(self, id='grafo', dirigido=False):
        self.id =       id
        self.dirigido = dirigido
        self.V =        dict()
        self.E =        dict()
        self.attr =     dict()

    def __repr__(self):
      
        return str("id: " + str(self.id) + '\n'
                   + 'nodos: ' + str(self.V.values()) + '\n'
                   + 'aristas: ' + str(self.E.values()))

    def add_nodo(self, nodo):
       
        self.V[nodo.id] = nodo

    def add_arista(self, arista):
       
        if self.get_arista(arista.id):
            return False

        self.E[arista.id] = arista
        return True

    def get_arista(self, arista_id):
       
        if self.dirigido:
            return arista_id in self.E
        else:
            u, v = arista_id
            return (u, v) in self.E or (v, u) in self.E

    def to_graphviz(self, filename):
       
        edge_connector = "--"
        graph_directive = "graph"
        if self.dirigido:
            edge_connector = "->"
            graph_directive = "digraph"

        with open(filename, 'w') as f:
            f.write(f"{graph_directive} {self.id} " + " {\n")
            for nodo in self.V:
                f.write(f"{nodo};\n")
            for arista in self.E.values():
                f.write(f"{arista.u} {edge_connector} {arista.v};\n")
            f.write("}")

#PROYECTO 2
    def BFS(self, s):
            if not s.id in self.V:
                print("Error, nodo no encontrado", file=sys.stderr)
                exit(-1)

            bfs = Grafo(id=f"BFS_{self.id}", dirigido=self.dirigido)
            discovered = set()
            bfs.add_nodo(s)
            L0 = [s]
            discovered = set()
            added = [s.id]

            while True:
                L1 = []
                for node in L0:
                    aristas = [ids_arista for ids_arista in self.E
                                if node.id in ids_arista]

                    for arista in aristas:
                        v = arista[1] if node.id == arista[0] else arista[0]

                        if v in discovered:
                            continue

                        bfs.add_nodo(self.V[v])
                        bfs.add_arista(self.E[arista])
                        discovered.add(v)
                        L1.append(self.V[v])

                L0 = L1
                if not L0:
                    break

            return bfs

    def DFS_R(self, u):
        
        dfs = Grafo(id=f"DFS_R_{self.id}", dirigido=self.dirigido)
        discovered = set()
        self.DFS_rec(u, dfs, discovered)

        return dfs

    def DFS_rec(self, u, dfs, discovered):
        
        dfs.add_nodo(u)
        discovered.add(u.id)
        aristas = (arista for arista in self.E if u.id in arista)

        for arista in aristas:
            v = arista[1]
            if not self.dirigido:
                v = arista[0] if u.id == arista[1] else arista[1]
            if v in discovered:
                continue
            dfs.add_arista(self.E[arista])
            self.DFS_rec(self.V[v], dfs, discovered)

    def DFS_I(self, s):
        dfs = Grafo(id=f"DFS_I_{self.id}", dirigido=self.dirigido)
        discovered = {s.id}
        dfs.add_nodo(s)
        u = s.id
        frontera = []
        while True:
            aristas = (arista for arista in self.E if u in arista)
            for arista in aristas:
                v = arista[1] if u == arista[0] else arista[0]
                if v not in discovered:
                    frontera.append((u, v))

            # si se encuentra vacía romper el while
            if not frontera:
                break

            parent, child = frontera.pop()
            
            if child not in discovered:
                dfs.add_nodo(self.V[child])
                arista = Arista(self.V[parent], self.V[child])
                dfs.add_arista(arista)
                discovered.add(child)

            u = child

        return dfs