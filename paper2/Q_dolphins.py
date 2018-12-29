import networkx as nx
import numpy as np
from collections import defaultdict
from imp_slpa import find_communities


def Qov(result):
    G = nx.read_gml(r'dataset\dolphins.gml', label='id')
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
            if node_cummunity[i] != node_cummunity[j]:
                B[i, j] = 0

    # 节点所属社团数
    for i in range(len(G.nodes)):
        for j in range(len(G.nodes)):
            B[i, j] *= 1 / (number_of_communities[i] * number_of_communities[j])

    print(len(G.edges()))
    print(np.sum(B) / (2*len(G.edges())))
    return np.sum(B) / (len(G.edges()))


if __name__ == '__main__':
    G = nx.read_gml(r'dataset\football.gml', label='id')
    result = {0: [0, 2, 3, 4, 8, 10, 11, 12, 14, 15, 16, 18, 20, 21, 23, 24, 28, 29, 30, 33, 34, 35, 36, 37, 38, 40, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 55, 58, 59, 61],
              1: [1, 5, 6, 7, 9, 13, 17, 19, 22, 25, 26, 27, 31, 32, 39, 41, 48, 54, 56, 57, 60]}
    Qov(result)
    """
    r = []
    for i in range(10):
        r.append(Qov(find_communities(G, 100, 0.33)))
    print(np.mean(r))
    """

