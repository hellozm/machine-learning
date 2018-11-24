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
    """
    generate graph
    initial graph node's attribute 'label' with its id
    :return: G
    """
    """
    data = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 18),
            (1, 20), (1, 22), (1, 32), (2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31), (3, 4),
            (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29), (3, 33), (4, 8), (4, 13), (4, 14), (5, 7), (5, 11),
            (6, 7), (6, 11), (6, 17), (7, 17), (9, 31), (9, 33), (9, 34), (10, 34), (14, 34), (15, 33), (15, 34),
            (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34), (24, 26),
            (24, 28), (24, 30), (24, 33), (24, 34), (25, 26), (25, 28), (25, 32), (26, 32), (27, 30), (27, 34),
            (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 33), (31, 34), (32, 33), (32, 34), (33, 34)]
    G = nx.Graph()
    G.add_edges_from(data)
    """
    G = nx.read_gml(r'dataset\karate.gml', label='id')
    for node, data in G.nodes(data=True):  # (node, {label: node})
        data['label'] = node  # 给node添加 label: node键值对
    return G


def lpa(graph):
    """
    label-propagation algorithm and use asynchronous updating for better results
    :param graph:
    :return:
    """
    node_influence = {1: 84.00000000000001, 34: 79.82352941176471, 3: 64.47058823529413, 33: 61.29411764705882, 2: 55.58823529411765, 4: 43.05882352941176, 14: 40.705882352941174, 9: 38.764705882352935, 32: 37.529411764705884, 8: 33.647058823529406, 24: 30.647058823529413, 31: 29.764705882352942, 28: 28.294117647058822, 20: 24.647058823529413, 30: 24.352941176470587, 6: 23.705882352941174, 7: 23.705882352941174, 29: 23.11764705882353, 5: 20.52941176470588, 11: 20.52941176470588, 26: 19.0, 25: 18.941176470588236, 18: 17.588235294117645, 22: 17.588235294117645, 13: 17.41176470588235, 10: 16.705882352941174, 15: 14.823529411764707, 16: 14.823529411764707, 19: 14.823529411764707, 21: 14.823529411764707, 23: 14.823529411764707, 27: 13.352941176470589, 17: 11.588235294117649, 12: 10.0}
    # node_influence = {45: 128.33333333333334, 14: 122.75, 37: 115.66666666666667, 33: 107.75, 29: 103.5, 51: 103.25000000000001, 18: 97.41666666666667, 21: 91.33333333333333, 50: 88.91666666666667, 24: 88.16666666666667, 20: 87.41666666666666, 40: 77.83333333333333, 16: 76.25, 43: 76.08333333333334, 38: 76.08333333333333, 57: 73.83333333333331, 15: 73.33333333333334, 13: 71.83333333333334, 17: 68.75, 54: 64.33333333333334, 9: 63.25, 1: 62.41666666666667, 6: 59.0, 8: 58.166666666666664, 36: 56.41666666666666, 0: 56.166666666666664, 41: 53.666666666666664, 34: 50.666666666666664, 47: 49.5, 52: 49.416666666666664, 42: 49.25000000000001, 59: 45.25, 10: 45.0, 28: 44.25, 7: 39.833333333333336, 23: 38.583333333333336, 30: 38.583333333333336, 5: 36.5, 27: 35.75, 44: 34.5, 19: 33.41666666666667, 3: 28.166666666666668, 2: 25.833333333333332, 55: 25.583333333333336, 32: 24.583333333333332, 61: 23.666666666666668, 25: 22.666666666666668, 26: 21.583333333333336, 39: 19.5, 53: 18.0, 56: 17.0, 46: 16.916666666666668, 4: 15.916666666666668, 11: 15.916666666666668, 35: 15.833333333333334, 12: 13.916666666666668, 49: 12.75, 48: 11.833333333333334, 58: 11.75, 22: 10.833333333333334, 31: 10.833333333333334, 60: 5.333333333333334}

    def estimate_stop_cond():
        """
        算法终止条件：所有节点的标签与大部分邻居节点标签相同或者迭代次数超过指定值则停止
        :return:
        """
        for node in graph.nodes():
            count = {}
            for neighbor in graph.neighbors(node):
                neighbor_label = graph.node[neighbor]['label']
                count[neighbor_label] = count.setdefault(neighbor_label, 0) + 1  # 如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值0

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
        nodes = [1, 34, 3, 33, 2, 4, 14, 9, 32, 8, 24, 31, 28, 20, 30, 6, 7, 29, 5, 11, 26, 25, 18, 22, 13, 10, 15, 16, 19, 21, 23, 27, 17, 12]
        # nodes = [45, 14, 37, 33, 29, 51, 18, 21, 50, 24, 20, 40, 16, 43, 38, 57, 15, 13, 17, 54, 9, 1, 6, 8, 36, 0, 41, 34, 47, 52, 42, 59, 10, 28, 7, 23, 30, 5, 27, 44, 19, 3, 2, 55, 32, 61, 25, 26, 39, 53, 56, 46, 4, 11, 35, 12, 49, 48, 58, 22, 31, 60]

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
            #print(neighbor_label_node)
            #print(label_influence)
            print(max_label)
            #print('---------')
            """
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
            """

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

    node_color = [float(g.node[v]['label']) for v in g]  # 将图中每个节点标签作为颜色编号
    print(node_color)
    nx.draw_networkx(g, node_color=node_color)
    plt.show()
