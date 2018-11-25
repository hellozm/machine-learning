import random
import networkx as nx
import matplotlib.pyplot as plt


def read_graph_from_file(path):
    # read edge-list from file
    graph = nx.read_edgelist(path, data=(('weight', float), ))

    # initial graph node's attribute 'label' with its id
    for node, data in graph.nodes(data=True):
        data['label'] = node

    return graph


def generate_graph():
    G = nx.read_gml(r'dataset\dolphins.gml', label='id')
    for node, data in G.nodes(data=True):  # (node, {label: node})
        data['label'] = node  # 给node添加 label: node键值对
    return G


def lpa(graph):
    """
    label-propagation algorithm and use asynchronous updating for better results
    :param graph:
    :return:
    """
    def estimate_stop_cond():
        """
        算法终止条件：所有节点的标签与大部分邻居节点标签相同或者迭代次数超过指定值则停止
        :return:
        """
        for node in graph.nodes():
            count = {}
            for neighbor in graph.neighbors(node):
                neighbor_label = graph.node[neighbor]['label']
                count[neighbor_label] = count.setdefault(neighbor_label, 0) + 1  # 如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值

            # find out labels with maximum count
            count_items = count.items()
            count_items = sorted(count_items, key=lambda x: x[1], reverse=True)

            # if there is not only one label with maximum count then choose one randomly
            labels = [k for k, v in count_items if v == count_items[0][1]]

            if graph.node[node]['label'] not in labels:
                return False

        return True

    loop_count = 0

    while True:
        loop_count += 1
        print('loop', loop_count)

        for node in graph.nodes():
            count = {}
            for neighbor in graph.neighbors(node):
                neighbor_label = graph.node[neighbor]['label']
                count[neighbor_label] = count.setdefault(neighbor_label, 0) + 1

            # find out labels with maximum count
            count_items = count.items()
            count_items = sorted(count_items, key=lambda x: x[1], reverse=True)

            # if there is not only one label with maximum count then choose one randomly
            labels = [(k, v) for k, v in count_items if v == count_items[0][1]]
            # print(random.sample(labels, 1))
            label = random.sample(labels, 1)[0][0]  # 从labels中选择1个元素，并以列表形式返回

            graph.node[node]['label'] = label

        if estimate_stop_cond() is True or loop_count >= 10:
            print('complete')
            return


if __name__ == '__main__':
    # g = read_graph_from_file('karate')
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
    print(len(result.keys()))
    node_color = [float(g.node[v]['label']) for v in g]  # 将图中每个节点标签作为颜色编号
    print(node_color)
    nx.draw_networkx(g, node_color=node_color)
    plt.show()
