import networkx as nx
from collections import defaultdict


result = {1: [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 17, 18, 20, 22],
          34: [9, 10, 15, 16, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]}

G = nx.read_gml('../dataset/karate.gml', label='id')
B = nx.modularity_matrix(G)
print(B[0, 0])
print((nx.degree(G, 1)**2)/(2*len(G.edges)))

number_of_communities = defaultdict(int)  # 节点所属社团数
for community, nodes in result.items():
    for node in nodes:
        number_of_communities[node] += 1
print(number_of_communities)

Q = []
for community in result.values():
    for i in range(len(community)):
        for j in range(len(community)):
            modularity = B[community[i]-1, community[j]-1] * \
                             (1/(number_of_communities[community[i]]*number_of_communities[community[j]]))
            Q.append(modularity)
print(len(Q))
print(sum(Q)/(2*len(G.edges)))

