import numpy as np
import networkx as nx
from collections import defaultdict
import random


def find_communities(G, T, r):
    """
    Speaker-Listener Label Propagation Algorithm (SLPA)
    see http://arxiv.org/abs/1109.5720
    """
    # Stage 1: Initialization
    memory = {i: {i: 1} for i in G.nodes()}
    node_importance = {67: 322.1666666666667, 7: 318.0, 2: 309.1666666666667, 73: 304.3333333333333, 46: 304.25, 53: 304.0833333333333, 88: 304.0, 15: 298.0, 83: 296.25, 111: 294.0, 49: 293.25, 77: 293.0, 74: 292.0, 22: 291.99999999999994, 40: 291.83333333333326, 110: 291.1666666666667, 6: 290.9166666666667, 3: 290.74999999999994, 68: 289.0, 104: 288.91666666666663, 21: 288.0, 114: 287.33333333333337, 81: 286.99999999999994, 72: 286.8333333333333, 47: 286.25, 8: 285.8333333333333, 84: 285.8333333333333, 32: 285.1666666666667, 51: 284.6666666666667, 5: 283.33333333333326, 100: 283.0833333333333, 13: 279.0833333333333, 78: 278.66666666666663, 0: 276.75, 39: 275.0833333333333, 9: 274.9166666666667, 64: 274.0, 82: 270.9166666666667, 23: 269.83333333333337, 60: 268.8333333333333, 108: 267.0833333333333, 1: 266.6666666666667, 98: 266.5, 106: 266.1666666666667, 102: 264.75, 16: 264.08333333333337, 25: 260.83333333333337, 89: 260.83333333333337, 4: 259.83333333333337, 10: 259.8333333333333, 107: 255.91666666666663, 52: 255.08333333333331, 41: 253.16666666666669, 55: 250.83333333333334, 45: 249.83333333333331, 109: 246.66666666666663, 79: 244.83333333333334, 37: 241.5, 30: 240.66666666666666, 80: 239.58333333333334, 31: 238.58333333333334, 33: 237.0, 103: 236.83333333333331, 93: 235.08333333333331, 35: 233.91666666666666, 105: 231.91666666666663, 29: 230.5, 38: 230.25, 19: 229.5, 61: 227.66666666666666, 69: 227.33333333333334, 94: 225.91666666666666, 101: 222.91666666666663, 71: 222.74999999999997, 34: 221.16666666666669, 99: 219.58333333333331, 14: 218.58333333333334, 54: 217.75, 18: 211.08333333333337, 62: 209.75, 11: 209.33333333333331, 24: 208.41666666666666, 43: 204.99999999999997, 70: 204.66666666666669, 87: 202.66666666666669, 48: 200.83333333333331, 50: 200.49999999999997, 17: 199.58333333333337, 12: 198.41666666666663, 90: 197.66666666666669, 27: 197.58333333333334, 26: 197.41666666666666, 20: 194.50000000000003, 85: 193.75000000000003, 65: 193.66666666666669, 92: 192.83333333333334, 44: 189.75, 91: 187.75000000000003, 95: 186.83333333333334, 28: 186.41666666666666, 58: 185.25, 56: 182.75000000000003, 76: 182.33333333333337, 86: 181.66666666666663, 113: 173.41666666666669, 96: 171.75, 66: 168.5, 75: 160.75000000000003, 57: 153.5, 112: 151.25, 36: 141.58333333333334, 63: 139.00000000000003, 97: 129.41666666666669, 42: 124.66666666666667, 59: 118.16666666666667}

    # Stage 2: Evolution
    # 开始遍历T次所有节点
    order = [59, 42, 97, 63, 36, 112, 57, 75, 66, 96, 113, 86, 76, 56, 58, 28, 95, 91, 44, 92, 65, 85, 20, 26, 27, 90, 12, 17, 50, 48, 87, 70, 43, 24, 11, 62, 18, 54, 14, 99, 34, 71, 101, 94, 69, 61, 19, 38, 29, 105, 35, 93, 103, 33, 31, 80, 30, 37, 79, 109, 45, 55, 41, 52, 107, 10, 4, 25, 89, 16, 102, 106, 98, 1, 108, 60, 23, 82, 64, 9, 39, 0, 78, 13, 100, 5, 51, 32, 8, 84, 47, 72, 81, 114, 21, 104, 68, 3, 6, 110, 40, 22, 74, 77, 49, 111, 83, 15, 88, 53, 46, 73, 2, 7, 67]

    for t in range(T):
        # 按节点重要性降序排列
        listenersOrder = order
        # print(listenersOrder)

        # 开始遍历节点
        for listener in listenersOrder:
            # 每个节点的key就是与他相连的节点标签名
            # print(listener)
            speakers = G[listener].keys()  # listener的邻居节点
            # print(speakers)
            if len(speakers) == 0:
                continue
            # 存放每个邻居节点出现次数最多的标签
            labels = defaultdict(int)  # key不存在时，返回的是工厂函数的默认值，比如list对应[ ]，str对应的是空字符串，set对应set( )，int对应0
            # 遍历所有与其相关联的节点
            for j, speaker in enumerate(speakers):
                # Speaker Rule
                total = float(sum(memory[speaker].values()))  # 计算speaker节点记忆标签总数

                # 论文中应该是随机选取一个，因为标签出现次数越多，相应地被选中的概率也就越大
                # 查看speaker中memory中出现概率最大的标签并记录，存在加1，不存在赋值1，key是标签名，value是Listener与speaker之间的权
                labels[list(memory[speaker].keys())[
                    np.random.multinomial(1, [freq / total for freq in memory[speaker].values()]).argmax()]] += 1
                # print(labels)

            # Listener Rule
            # 查看labels中值最大的标签，让其成为当前listener的一个记录；若有多个，则选择标签影响力最大的一个
            candidateLabel = sorted(labels.items(), key=lambda x: x[1], reverse=True)
            freq_max_labels = [(k, v) for k, v in candidateLabel if v == candidateLabel[0][1]]
            # print('候选标签：')
            # print(freq_max_labels)
            for candidate in freq_max_labels:
                node_importance[candidate[0]]
            acceptedLabel = max(freq_max_labels, key=lambda x: node_importance[x[0]])[0]
            # print(acceptedLabel)

            # Update listener memory
            if acceptedLabel in memory[listener]:
                memory[listener][acceptedLabel] += 1
            else:
                memory[listener][acceptedLabel] = 1

    # Stage 3:
    node_label = {}
    for node, mem in memory.items():
        print(node, mem)
        max_count = max(mem.items(), key=lambda x: x[1])[1]
        max_label_list = [label for label, count in mem.items() if count == max_count]
        node_label[node] = random.choice(max_label_list)
    return node_label


if __name__ == '__main__':
    G = nx.read_gml(r'dataset\football.gml', label='id')
    result = find_communities(G, 10, 0.4)
    print(result)
    community = {}
    for k, v in result.items():
        if v in community.keys():
            community[v].append(k)
        else:
            community.setdefault(v, [k])
    print(community)
    print(len(community.keys()))
    for k,  v in community.items():
        print(len(community[k]), end=' ')
