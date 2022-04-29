import sys
import random

from Clases.Grafo import Grafo
from Clases.Arista import Arista
from Clases.Nodo import Nodo

def grafoMalla(m, n, dirigido=False):
    
    if m < 2 or n < 2:
        print("m y n, deben ser mayores a 1", file=sys.stderr)
        exit(-1)

    total_nodes = m*n
    last_col = m - 1
    last_row = n - 1
    grafito= Grafo(id=f"grafoMalla_{m}_{n}", dirigido=dirigido)
    nodos = grafito.V

    for id in range(total_nodes):
        grafito.add_nodo(Nodo(id))

   
    grafito.add_arista(Arista(nodos[0], nodos[1]))
    grafito.add_arista(Arista(nodos[0], nodos[m]))
    for node in range(1, m - 1):
        grafito.add_arista(Arista(nodos[node], nodos[node - 1]))
        grafito.add_arista(Arista(nodos[node], nodos[node + 1]))
        grafito.add_arista(Arista(nodos[node], nodos[node + m]))
    grafito.add_arista(Arista(nodos[m-1], nodos[m-2]))
    grafito.add_arista(Arista(nodos[m-1], nodos[m - 1 + m]))

    for node in range(m, total_nodes - m):
        col = node % m
        grafito.add_arista(Arista(nodos[node], nodos[node - m]))
        grafito.add_arista(Arista(nodos[node], nodos[node + m]))
        if col == 0:
            grafito.add_arista(Arista(nodos[node], nodos[node + 1]))
        elif col == last_col:
            grafito.add_arista(Arista(nodos[node], nodos[node - 1]))
        else:
            grafito.add_arista(Arista(nodos[node], nodos[node + 1]))
            grafito.add_arista(Arista(nodos[node], nodos[node - 1]))

    col_0 = total_nodes - m
    col_1 = col_0 + 1
    last_node = total_nodes - 1
    grafito.add_arista(Arista(nodos[col_0], nodos[col_1]))
    grafito.add_arista(Arista(nodos[col_0], nodos[col_0 - m]))
    for node in range(col_1, last_node):
        grafito.add_arista(Arista(nodos[node], nodos[node - 1]))
        grafito.add_arista(Arista(nodos[node], nodos[node + 1]))
        grafito.add_arista(Arista(nodos[node], nodos[node - m]))
    grafito.add_arista(Arista(nodos[last_node], nodos[last_node - m]))
    grafito.add_arista(Arista(nodos[last_node], nodos[last_node - 1]))

    return grafito

def grafoErdosRenyi(n, m, dirigido=False, auto=False):
   
    if m < n-1 or n < 1:
        print("n debe ser mayor 0 y m mayor o igual a n - 1", file=sys.stderr)
        exit(-1)

    grafito= Grafo(id=f"grafoErdos_Renyi_{n}_{m}")
    nodos = grafito.V

    for nodo in range(n):
        grafito.add_nodo(Nodo(nodo))

    rand_node = random.randrange
    for arista in range(m):
        while True:
            u = rand_node(n)
            v = rand_node(n)
            if u == v and not auto:
                continue
            if grafito.add_arista(Arista(nodos[u], nodos[v])):
                break

    return grafito

def grafoGilbert(n, p, dirigido=False, auto=False):
    if p > 1 or p < 0 or n < 1:
        print(" 0 <= p <= 1 y n > 0", file=sys.stderr)
        exit(-1)

    grafito= Grafo(id=f"grafoGilbert_{n}_{int(p * 100)}", dirigido=dirigido)
    nodos = grafito.V

    for nodo in range(n):
        grafito.add_nodo(Nodo(nodo))
    if auto:
        pairs = ((u, v) for u in nodos.keys() for v in nodos.keys())
    else:
        pairs = ((u, v) for u in nodos.keys() for v in nodos.keys() if u != v)

    for u, v in pairs:
        add_prob = random.random()
        if add_prob <= p:
            grafito.add_arista(Arista(nodos[u], nodos[v]))

    return grafito

def grafoGeografico(n, r, dirigido=False, auto=False):
    if r > 1 or r < 0 or n < 1:
        print("Error: 0 <= r <= 1 y n > 0", file=sys.stderr)
        exit(-1)

    coords = dict()
    grafito= Grafo(id=f"grafoGeografico_{n}_{int(r * 100)}", dirigido=dirigido)
    nodos = grafito.V

    for nodo in range(n):
        grafito.add_nodo(Nodo(nodo))
        x = round(random.random(), 3)
        y = round(random.random(), 3)
        coords[nodo] = (x, y)

    r **= 2
    for u in nodos:
        vs = (v for v in nodos if u != v)
        if auto:
            grafito.add_arista(Arista(nodos[u], nodos[u]))
        for v in vs:
            dist = (coords[u][0] - coords[v][0]) ** 2 \
                    + (coords[u][1] - coords[v][1]) ** 2
            if dist <= r:
                grafito.add_arista(Arista(nodos[u], nodos[v]))
    return grafito

def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
    if n < 1 or d < 2:
        print("Error: n > 0 y d > 1", file=sys.stderr)
        exit(-1)

    grafito= Grafo(id=f"grafoBarabasi_{n}_{d}", dirigido=dirigido)
    nodos = grafito.V
    nodos_deg = dict()

    for nodo in range(n):
        grafito.add_nodo(Nodo(nodo))
        nodos_deg[nodo] = 0

    for nodo in nodos:
        for v in nodos:
            if nodos_deg[nodo] == d:
                break
            if nodos_deg[v] == d:
                continue
            p = random.random()
            equal_nodes = v == nodo
            if equal_nodes and not auto:
                continue

            if p <= 1 - nodos_deg[v] / d \
               and grafito.add_arista(Arista(nodos[nodo], nodos[v])):
                nodos_deg[nodo] += 1
                if not equal_nodes:
                        nodos_deg[v] += 1

    return grafito

def grafoDorogovtsevMendes(n, dirigido=False):
    if n < 3:
        print("Error: n >= 3", file=sys.stderr)
        exit(-1)

    grafito= Grafo(id=f"grafoDorogovtsev_{n}", dirigido=dirigido)
    nodos = grafito.V
    aristas = grafito.E

    for nodo in range(3):
        grafito.add_nodo(Nodo(nodo))
    pairs = ((u, v) for u in nodos for v in nodos if u != v)
    for u, v in pairs:
        grafito.add_arista(Arista(nodos[u], nodos[v]))

    for nodo in range(3, n):
        grafito.add_nodo(Nodo(nodo))
        u, v = random.choice(list(aristas.keys()))
        grafito.add_arista(Arista(nodos[nodo], nodos[u]))
        grafito.add_arista(Arista(nodos[nodo], nodos[v]))

    return grafito