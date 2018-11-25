import random
import networkx as nx
import matplotlib.pyplot as plt
from LFR import generate_lfr_graph


def generate_graph():
    G = generate_lfr_graph()  # 节点编号从0开始
    for node, data in G.nodes(data=True):  # (node, {label: node})
        data['label'] = node  # 给node添加 label: node键值对
    return G


def lpa(graph):

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
        last_label = [graph.node[i]['label'] for i in graph]

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
    print(len(result.keys()))
    for k, v in result.items():
        result[k] = [n+1 for n in v]
    # print(result)
