import networkx as nx
import numpy as np
from collections import defaultdict
from imp_slpa import find_communities


def Qov(result):
    G = nx.read_gml(r'dataset\football.gml', label='id')
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
    result = {0: [1, 25, 33, 37, 45, 89, 103, 105, 109], 1: [19, 29, 30, 35, 55, 79, 80, 82, 94, 101], 2: [2, 6, 13, 15, 32, 39, 47, 60, 64, 100, 106], 3: [3, 5, 10, 40, 52, 72, 74, 81, 84, 98, 102, 107], 4: [44, 48, 57, 66, 75, 86, 91, 92, 112], 5: [58, 59, 63, 97], 6: [12, 14, 18, 26, 31, 34, 36, 38, 42, 43, 54, 61, 71, 85, 99], 7: [0, 4, 9, 16, 23, 41, 93, 104], 8: [7, 8, 21, 22, 51, 68, 77, 78, 108, 111], 9: [17, 20, 27, 56, 62, 65, 70, 76, 87, 95, 96, 113], 10: [11, 24, 28, 50, 69, 90], 11: [46, 49, 53, 67, 73, 83, 88, 110, 114]}
    result = {0: {0, 4, 104, 9, 41, 16, 23, 93}, 1: {89, 1, 33, 37, 103, 105, 45, 109, 25}, 2: {32, 64, 2, 100, 6, 39, 106, 13, 15, 47, 60}, 3: {97, 98, 3, 5, 102, 40, 72, 10, 11, 74, 107, 81, 52, 84, 24}, 7: {68, 7, 8, 108, 77, 78, 111, 50, 51, 21, 22}, 61: {34, 99, 36, 38, 71, 43, 12, 14, 18, 85, 54, 26, 61, 31}, 76: {96, 65, 70, 59, 76, 17, 113, 20, 95, 87, 56, 58, 27, 62, 63}, 30: {35, 101, 42, 79, 80, 82, 19, 55, 94, 29, 30}, 78: {24, 90, 28, 69}, 91: {66, 75, 44, 48, 112, 86, 57, 91, 92}, 88: {67, 69, 73, 46, 110, 49, 114, 83, 53, 88, 58}}

    Qov(result)
    """
    r = []
    for i in range(10):
        r.append(Qov(find_communities(G, 100, 0.33)))
    print(np.mean(r))
    """

