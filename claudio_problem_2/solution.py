"""
This is just asking for the MST of the graph.
"""
from networkx import nx

G = nx.Graph()
n_cities = int(raw_input())
n_routes = int(raw_input())
for _ in xrange(n_routes):
    source, dest, weight = raw_input().split()
    G.add_edge(int(source), int(dest), weight=float(weight))

T = nx.minimum_spanning_tree(G)
total_cost = 0
for e in sorted(T.edges(data=True), key=lambda k: k[2]["weight"]):
    print "%d %d %f" % (e[0], e[1], e[2]["weight"])
    total_cost += e[2]["weight"]
print total_cost
