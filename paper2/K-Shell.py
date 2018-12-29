import networkx as nx


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


def fusion(kshell, iterations):
    kshell_iterations = {}
    # 加kshell值
    for ks, nodes in kshell.items():
        for node in nodes:
            kshell_iterations[node] = ks
    print(kshell_iterations)
    # 加迭代次数
    for iter, nodes in iterations.items():
        for node in nodes:
            kshell_iterations[node] += iter
    nodesss = [n for n in kshell_iterations.keys()]
    print(nodesss)
    print("ksehll值融合迭代层数：")
    print(kshell_iterations)

    # 加节点度值
    G = nx.read_gml(r'dataset\football.gml', label='id')
    node_degree = G.degree()
    for node, degree in node_degree():
        kshell_iterations[node] += degree
    print("ksehll值融合迭代层数和度值为：")
    print(kshell_iterations)
    return kshell_iterations


def interface():
    G = nx.read_gml(r'dataset\football.gml', label='id')
    kshell, iterations = k_shell(G)
    kshell_iterations = fusion(kshell, iterations)
    nodes = [n for n in kshell_iterations.keys()]
    print(nodes)


if __name__ == '__main__':
    interface()