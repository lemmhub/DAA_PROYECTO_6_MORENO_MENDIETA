import random
import numpy as np
import heapdict
import copy
import sys
from Clases.Arista import Arista


class Grafo(object):
   
    def __init__(self, id='grafo', dirigido=False):
        self.id =       id
        self.dirigido = dirigido
        self.V =        dict()
        self.E =        dict()
        self.attr =     dict()

    def copiar_grafo(self, id=f"copy", dirigido=False):
        
        other = Grafo(id, dirigido)
        other.V = copy.deepcopy(self.V)
        other.E = copy.deepcopy(self.E)
        other.attr = copy.deepcopy(self.attr)

        return other

    def costo(self):
      
        _costo = 0
        for edge in self.E.values():
            _costo += edge.attrs['peso']

        return _costo

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


    #Proyecto 3 generar pesos  
    def generar_pesos(self):
        for arista in self.E.values():
            arista.attrs['peso'] = random.randint(1, 50)


    def to_graphviz(self, filename):
       
        edge_connector = "--"
        graph_directive = "graph"
        if self.dirigido:
            edge_connector = "->"
            graph_directive = "digraph"

        with open(filename, 'w') as f:
            f.write(f"{graph_directive} {self.id} " + " {\n")
            for nodo in self.V:
                if "Dijkstra" in self.id:
                    f.write(f"\"{nodo} ({self.V[nodo].attrs['dist']})\";\n")
                else:
                    f.write(f"{nodo};\n")
            for arista in self.E.values():
                if "Dijkstra" in self.id:
                    peso = np.abs(self.V[arista.u.id].attrs['dist']
                                    - self.V[arista.v.id].attrs['dist'])
                    f.write(f"\"{arista.u} ({self.V[arista.u.id].attrs['dist']})\""
                            + f" {edge_connector} "
                            + f"\"{arista.v} ({self.V[arista.v.id].attrs['dist']})\""
                            + f";\n")
                else:
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

#proyecto 3
    def Dijkstra(self, s):
        tree = Grafo(id=f"{self.id}_Dijkstra")
        line = heapdict.heapdict()
        parents = dict()
        in_tree = set()


     
        line[s] = 0
        parents[s] = None
        for node in self.V:
            if node == s:
                continue
            line[node] = np.inf
            parents[node] = None

        while line:
            u, u_dist = line.popitem()
            if u_dist == np.inf:
                continue

            self.V[u].attrs['dist'] = u_dist
            tree.add_nodo(self.V[u])
            if parents[u] is not None:
                arista = Arista(self.V[parents[u]], self.V[u])
                tree.add_arista(arista)
            in_tree.add(u)

            # get neighbor nodes
            neigh = []
            for arista in self.E:
                if self.V[u].id in arista:
                    v = arista[0] if self.V[u].id == arista[1] else arista[1]
                    if v not in in_tree:
                        neigh.append(v)

            # actualizar distancias de ser necesario
            for v in neigh:
                arista = (u, v) if (u, v) in self.E else (v, u)
                if line[v] > u_dist + self.E[arista].attrs['peso']:
                    line[v] = u_dist + self.E[arista].attrs['peso']
                    parents[v] = u

        return tree

#Proyecto 4
    def KruskalD(self):
        #Minimal spanding Tree
        mst = Grafo(id=f"{self.id}_KruskalD_MST")

        # SE ENLISTAN LAS ARISTAS POR PESO
        edges_sorted = list(self.E.values())
        edges_sorted.sort(key = lambda edge: edge.attrs['peso'])

        # revisar los componentes conectados
        connected_comp = dict()
        for nodo in self.V:
            connected_comp[nodo] = nodo

       
        for edge in edges_sorted:
            u, v = edge.u, edge.v
            if connected_comp[u.id] != connected_comp[v.id]:
                # se agregan aristas al MST
                mst.add_nodo(u)
                mst.add_nodo(v)
                mst.add_arista(edge)

                for comp in connected_comp:
                    if connected_comp[comp] == connected_comp[v.id]:
                        other_comp = connected_comp[v.id]
                        connected_comp[comp] = connected_comp[u.id]

                        iterator = (key for key in connected_comp \
                                    if connected_comp[key] == other_comp)
                        for item in iterator:
                            connected_comp[item] = connected_comp[u.id]
        print("KRUSKAL END")
        return mst


    def KruskalI(self):
      
        mst = self.copiar_grafo(id=f"{self.id}_KruskalI_MST", dirigido=self.dirigido)

        edges_sorted = list(self.E.values())
        edges_sorted.sort(key = lambda edge: edge.attrs['peso'], reverse=True)

        for edge in edges_sorted:
            u, v = edge.u.id, edge.v.id
            key, value = (u, v), edge
            del(mst.E[(u, v)])
            if len(mst.BFS(edge.u).V) != len(mst.V):
                mst.E[(u, v)] = edge
        
        print("KRUSKAL I END")
        return mst


    def Prim(self):
        mst = Grafo(id=f"{self.id}_Prim")
        line = heapdict.heapdict()
        parents = dict()
        in_tree = set()

        s = random.choice(list(self.V.values()))

        #Asignar valores infinitos a los nodos y buscar nodo padre
        line[s.id] = 0
        parents[s.id] = None
        for node in self.V:
            if node == s.id:
                continue
            line[node] = np.inf
            parents[node] = None

        while line:
            u, u_dist = line.popitem()
            if u_dist == np.inf:
                continue

            self.V[u].attrs['dist'] = u_dist
            mst.add_nodo(self.V[u])
            if parents[u] is not None:
                arista = Arista(self.V[parents[u]], self.V[u])
                if (u, parents[u]) in self.E:
                    weight = self.E[(u, parents[u])].attrs['peso']
                else:
                    weight = self.E[(parents[u], u)].attrs['peso']
                arista.attrs['peso'] = weight
                mst.add_arista(arista)
            in_tree.add(u)

            # Buscar los nodos vecinos
            neigh = []
            for arista in self.E:
                if self.V[u].id in arista:
                    v = arista[0] if self.V[u].id == arista[1] else arista[1]
                    if v not in in_tree:
                        neigh.append(v)

            # actualizar pesos
            for v in neigh:
                arista = (u, v) if (u, v) in self.E else (v, u)
                if line[v] > self.E[arista].attrs['peso']:
                    line[v] = self.E[arista].attrs['peso']
                    parents[v] = u
        print("PRIM END")
        return mst