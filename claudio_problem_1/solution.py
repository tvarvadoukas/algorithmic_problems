"""
General idea / Representation
-----------------------------
One has to find all the similar critics and then find an optimal assignment between them to
maximise the number of participants.

A brute force solution would give an exponential time. We can do better...

A natural representation is a graph where the vertices are the critics and an edge
between 2 critics means that they are similar and can participate in the same show.
  
After the construction of the graph, the problem is reduced to finding the maximum set of edges
without common vertices, which is the maximum matching problem: https://en.wikipedia.org/wiki/Matching_(graph_theory) 

The maximum matching problem has a simple (and multiple) solutions if the graph is bipartite. In
the following section I show why the graph is actually bipartite.

To find the actual matching I am using the Python `networkx` module, which uses
the Hopcroft-Karp algorithm under the hood, whose complexity is O(E sqrt(V)):
https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm


Proof: The graph is bipartite
-----------------------------
If we group all the critics by the number of preferences, then we can construct a dictionary
where the key is the number of preferences and the value is a list of critics' ids e.g.

{
  1: [1, 3]
  2: [2, 5, 6]
  3: []
  4: [4]
  ...
}

The maximum length is constrained by the problem's description and is the maximum number of 
novels, which is 20.

Key observation: if a critic belongs to bucket i (i number of preferences), he can only 
potentially match with the ones in the buckets (i-1) and (i+1)!

Reason: 
  - critics that belong to the same bucket CAN NOT be similar, since they would have either the 
    exactly same list of preferences, hence not similar, or would have at least 2 different preferences
    e.g. "1 3 4" vs. "1 3 5" ("4" and "5" produce 2 different preferences)
  - critics with more than 1 bucket difference [bucket i vs. (i +- c) for c >= 2] CAN NOT be 
    similar, since essentially they have at least 2 different preferences as well.
  - critics with 1 bucket difference CAN have a match, since from a given set of preferences in 
    order to obtain a similar one, we just need to append or remove one.


This observation leads us to an easy splitting rule between the vertices: EVENS and ODDS;
if a vertex belongs to bucket i and i is an even number, then it can have edges only with 
vertices that belong to (i-1) and (i+1) which are odd numbers. Hence, from EVENS we can only go to ODDS
and vice versa => bipartite graph!


Optimization: No need for all vs. all comparison for similarity
----------------------------------------------------------------
By using the data structure mentioned in the previous section (i.e. groupping critics by the
number of vertices) we can reduce the number of comparisons for similarity. For each bucket i
we only need to look for similarities in the bucket (i+1). In the worst-case of just having 2
buckets one after the other and each one having V/2 critics, the number of comparisons becomes 
V^2/4 vs. V^2. In many other cases this yields great reductions; e.g. a bucket with no neighbors
won't be taken into consideration at all etc.


Optimization: Checking if 2 critics are similar in O(1)
---------------------------------------------------------
This is a common operation so it'd be good if there was an optimization for speed and storage.

If we take the preferences of a speaker e.g. "1 3 4" and set the respective bits in a number,
it becomes "1101" (binary) = 13 (decimal). Imagine a similar speaker whose preferences are 
"1 4", that'd become "1001" (binary) = 9 (decimal). Two critics are similar when they differ
in exactly 1 bit, which is an O(1) operation using a few bitwise operations (see function 
`is_similar`).

Also in terms of storage, the preference of each speaker is reduced to an 32-bit integer, 
instead of a list of integers. The number of bits needed are equal to the maximum number of
novels, which in this problem is constrained to 20.
"""

import networkx as nx
from networkx.algorithms import bipartite

def is_similar(a, b):
    """Returns TRUE if 2 numbers differ in only 1 bit. """
    if a == b: return False
    c = a ^ b
    return (c == 1) or not (c & c-1)

def make_number(L):
    """Transform a list of preferences to an integer by setting the respective bits. """
    n = 0
    for l in L:
        n |= 1 << (l-1)
    return n

def create_bipartite_graph(n_critics, n_novels, preferences, length_to_critics):
    B = nx.Graph()
    for n in xrange(n_novels):
        try:
            for c1 in length_to_critics[n]:
                if (n-1 in length_to_critics) or (n+1 in length_to_critics):
                    B.add_nodes_from(length_to_critics[n], bipartite=n%2) 
                for c2 in length_to_critics[n+1]:
                    if is_similar(preferences[c1], preferences[c2]):
                        B.add_edge(c1, c2)
        except KeyError:
            continue
    return B

def display_maximum_matching(B):
    """Displays the maximum matching of a bipartite graph. """
    for k, v in bipartite.maximum_matching(B).iteritems():
        if k < v:
            print "%d %d" % (k+1, v+1)

if __name__ == "__main__":
    length_to_critics = {}
    preferences = []
    n_critics, n_novels = map(int, raw_input().split())
    for c in xrange(n_critics):
        p = map(int, raw_input().split())
        preferences.append(make_number(p))
        try:
            length_to_critics[len(p)].append(c)
        except KeyError:
            length_to_critics[len(p)] = [c]

    B = create_bipartite_graph(n_critics, n_novels, preferences, length_to_critics)
    display_maximum_matching(B)
