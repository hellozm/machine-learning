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


def fusion(kshell, iterations):
    """
    node_kshell = {}
    node_iterations = {}
    for ks, nodes in kshell.items():
        for node in nodes:
            node_kshell[node] = ks
    for iter, nodes in iterations.items():
        for node in nodes:
            node_iterations[node] = iter
    print(node_kshell)
    print(node_iterations)
    """
    kshell_iterations = {}
    for ks, nodes in kshell.items():
        for node in nodes:
            kshell_iterations[node] = ks
    for iter, nodes in iterations.items():
        for node in nodes:
            kshell_iterations[node] += iter
    print("ksehll值融合迭代层数为：")
    print(kshell_iterations)
    return kshell_iterations


# 节点度值归一化
def normalization_degree(G):
    normal_degree = {}
    max_degree_node, max_degree = max(nx.degree(G), key=lambda x: x[1])  # 求最大度值以及对应的节点
    for node, degree in dict(nx.degree(G)).items():
        normal_degree[node] = degree/max_degree
    print("归一化度值为：")
    print(normal_degree)
    return normal_degree


# 求节点以及邻居节点综合影响力（融合kshell、迭代层数和归一化度值）
def extend_ks(ks):
    G = nx.read_gml(r'dataset\football.gml', label='id')
    normal_degree = normalization_degree(G)

    node_own_eks = {}
    for node, value in normal_degree.items():
        node_own_eks[node] = value + ks[node]
    print(node_own_eks)
    # print(list(nx.neighbors(G, 10)))  # 检验结果

    eks = {}
    for node, value in normal_degree.items():
        eks[node] = value + ks[node]
    # 求节点以及邻居节点影响力之和
    for node in nx.nodes(G):
        for neighbor in nx.neighbors(G, node):
            eks[node] += node_own_eks[neighbor]
    desc_eks = sorted(eks.items(), key=lambda x: x[1], reverse=False)  # 按节点重要性升序排序
    print("最终结果：")
    print(desc_eks)
    return desc_eks


def interface():
    G = nx.read_gml(r'dataset\football.gml', label='id')
    # print(len(nx.nodes(G)))
    print(nx.degree(G))
    kshell, iterations = k_shell(G)
    print("kshell值为：")
    print(kshell)  # 图G的k-shell值
    print("迭代层数为：")
    print(iterations)  # 图G的迭代层数
    kshell_iterations = fusion(kshell, iterations)
    desc_eks = extend_ks(kshell_iterations)

    # 字典形式的结果
    desc_eks_node = [node[0] for node in desc_eks]
    desc_eks_value = [value[1] for value in desc_eks]
    dict_desc_eks = {i: j for i, j in zip(desc_eks_node, desc_eks_value)}
    print(dict_desc_eks)

    node = [n[0] for n in desc_eks]
    print(node)
    return dict_desc_eks, node


if __name__ == '__main__':
    interface()