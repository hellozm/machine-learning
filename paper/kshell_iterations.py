import networkx as nx


"""
def k_shell(G):
    k = 1
    result = {}
    while nx.nodes(G):
        result.setdefault(k, [])
        min_degree_node, _ = min(nx.degree(G), key=lambda x: x[1])  # 求出度最小的节点
        if nx.degree(G, min_degree_node) <= k:
            result[k].append(min_degree_node)
            G.remove_node(min_degree_node)
            continue
        else:
            k += 1
    return result
"""


def k_shell(G):
    """
    求融合迭代层数以及k-shell值
    :param G:
    :return:kshell, iterations
    """
    k = 1
    t = 1
    iterations = {}
    kshell = {}
    while nx.nodes(G):
        kshell.setdefault(k, [])
        iterations.setdefault(t, [])
        same_shell_nodes = [node_degree[0] for node_degree in nx.degree(G) if node_degree[1] <= k]
        # print(same_shell_nodes)  # 注释去掉通过观察输出层数可知迭代次数
        if same_shell_nodes:
            G.remove_nodes_from(same_shell_nodes)
            kshell[k].extend(same_shell_nodes)
            iterations[t].extend(same_shell_nodes)
            t += 1
            continue
        else:
            k += 1
            t = 1
    return kshell, iterations


if __name__ == '__main__':
    G = nx.read_gml(r'dataset\karate.gml', label='id')
    # print(len(nx.nodes(G)))
    # print(nx.degree(G))
    kshell, iterations = k_shell(G)
    print(kshell)  # 图G的k-shell值
    print(iterations)  # 图G的迭代层数
