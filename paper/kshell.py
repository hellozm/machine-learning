import networkx as nx


def k_shell(G):
    """
    计算k-sell值
    :param G: 图
    :return: 键值对
    """
    k = 1
    result = {}
    while nx.nodes(G):
        result.setdefault(k, [])
        for n in range(len(nx.nodes(G))):
            min_degree_node, _ = min(nx.degree(G), key=lambda x: x[1])  # 求出度最小的节点
            if nx.degree(G, min_degree_node) <= k:
                result[k].append(min_degree_node)
                G.remove_node(min_degree_node)
        k += 1
    return result


if __name__ == '__main__':
    G = nx.read_gml(r'dataset\karate.gml', label='id')
    print(nx.degree(G))
    print(k_shell(G))
