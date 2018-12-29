import networkx as nx
import numpy as np
from collections import defaultdict


def Qov(result):
    G = nx.read_gml('dataset\karate.gml', label='id')
    print(G.nodes)
    B = nx.modularity_matrix(G)  # G的模块度矩阵,nx的官方文档写错了
    node_cummunity = {}  # 每个节点所在社区键值对
    for key, values in result.items():
        for node in values:
            if node in node_cummunity.keys():
                node_cummunity[node].append(key)
            else:
                node_cummunity[node] = [key]
    print(node_cummunity)

    number_of_communities = defaultdict(int)  # 节点所属社团数
    for community, nodes in result.items():
        for node in nodes:
            number_of_communities[node] += 1
    print(number_of_communities)

    # 判断节点是否属于同一社团
    for i in range(len(G.nodes)):
        for j in range(len(G.nodes)):
            if node_cummunity[i+1] != node_cummunity[j+1]:
                B[i, j] = 0

    # 节点所属社团数
    for i in range(len(G.nodes)):
        for j in range(len(G.nodes)):
            B[i, j] *= 1 / (number_of_communities[i + 1] * number_of_communities[j + 1])

    print(len(G.edges()))
    print(np.sum(B) / (2*len(G.edges())))
    return np.sum(B) / (2*len(G.edges()))


if __name__ == '__main__':
    G = nx.read_gml(r'dataset\karate.gml', label='id')
    result = {1: [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 17, 18, 20, 22],
              34: [9, 10, 15, 16, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]}

    Qov(result)
    """
    r = []
    for i in range(100):
        r.append(Qov(find_communities(G, 100, 0.33)))
    print(np.mean(r))
    """

