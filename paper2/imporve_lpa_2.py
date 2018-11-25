import random
import networkx as nx
import matplotlib.pyplot as plt
from kshell import interface


def generate_graph():
    """
    generate graph
    initial graph node's attribute 'label' with its id
    :return: G
    """
    G = nx.read_gml(r'dataset\football.gml', label='id')  # 节点编号从0开始
    for node, data in G.nodes(data=True):  # (node, {label: node})
        data['label'] = node  # 给node添加 label: node键值对
    return G


def lpa(graph):
    """
    label-propagation algorithm and use asynchronous updating for better results
    :param graph:
    :return:
    """
    node_influence, _ = interface()

    def estimate_stop_cond():
        """
        算法终止条件：所有节点的标签不再变化
        :return:
        """
        now_label = [graph.node[j]['label'] for j in graph]
        if now_label == last_label:
            return True
        else:
            return False

    loop_count = 0

    while True:
        loop_count += 1
        print('loop', loop_count)
        _, nodes = interface()
        last_label = [graph.node[i]['label'] for i in graph]
        for node in nodes:
            count = {}
            for neighbor in graph.neighbors(node):
                neighbor_label = graph.node[neighbor]['label']
                count[neighbor] = neighbor_label
            # 计算邻居节点相同标签影响力之和
            neighbor_label_node = {}  # 邻居节点的{标签：[节点]}
            for neighbor_node, neighbor_label in count.items():
                if neighbor_label in neighbor_label_node.keys():
                    neighbor_label_node[neighbor_label].append(neighbor_node)
                else:
                    neighbor_label_node.setdefault(neighbor_label, [])
                    neighbor_label_node[neighbor_label].append(neighbor_node)

            label_influence = {}  # {标签：相同标签影响力之和}
            for label, nodes in neighbor_label_node.items():
                label_influence[label] = 0
                for n in nodes:
                    label_influence[label] += node_influence[n]
            max_label = max(label_influence.items(), key=lambda x: x[1])[0]
            graph.node[node]['label'] = max_label
            print(neighbor_label_node)
            print(label_influence)
            print(max_label)
            print('---------')

        if estimate_stop_cond() is True:
            print('complete')
            return


if __name__ == '__main__':
    g = generate_graph()
    lpa(g)

    result = {}
    for node in g:
        if g.node[node]['label'] in result.keys():
            result[g.node[node]['label']].append(node)
        else:
            result.setdefault(g.node[node]['label'], [])
            result[g.node[node]['label']].append(node)
    print(result)
    """
    # 结果中节点序号加1
    for a, b in result.items():
        result[a] = [c+1 for c in b]
    print(result)
    """
    print(len(result.keys()))

    node_list = [0 for i in range(len(g.nodes()))]
    print(len(node_list))
    for i, j in result.items():
        for k in j:
            node_list[k] = i
    print(node_list)

    node_color = [float(g.node[v]['label']) for v in g]  # 将图中每个节点标签作为颜色编号
    nx.draw_networkx(g, node_color=node_color)
    plt.show()
