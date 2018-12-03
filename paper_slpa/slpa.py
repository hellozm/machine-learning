import numpy as np
import networkx as nx
from collections import defaultdict


def find_communities(G, T):
    """
    Speaker-Listener Label Propagation Algorithm (SLPA)
    see http://arxiv.org/abs/1109.5720
    """

    # Stage 1: Initialization
    memory = {i: {i: 1} for i in G.nodes()}
    node_importance = {12: 3, 10: 5, 13: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5, 21: 5, 22: 5, 23: 5, 27: 5, 5: 7, 6: 8, 7: 8, 11: 7, 20: 7, 25: 7, 26: 7, 29: 7, 30: 8, 24: 10, 28: 9, 32: 11, 8: 9, 31: 9, 33: 17, 34: 22, 2: 15, 4: 12, 9: 11, 14: 11, 1: 23, 3: 17}

    # Stage 2: Evolution
    # 开始遍历T次所有节点
    for t in range(T):
        # 按节点重要性降序排列
        order = sorted(node_importance.items(), key=lambda x: x[1], reverse=True)
        listenersOrder = [n[0] for n in order]
        print(listenersOrder)

        # 开始遍历节点
        for listener in listenersOrder:
            # 每个节点的key就是与他相连的节点标签名
            speakers = G[listener].keys()  # listener的邻居节点
            print(speakers)
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
                print(labels)

            # Listener Rule
            # 查看labels中值最大的标签，让其成为当前listener的一个记录；若有多个，则选择标签影响力最大的一个
            candidateLabel= sorted(labels.items(), key=lambda x: x[1], reverse=True)
            freq_max_labels = [(k, v) for k, v in candidateLabel if v == candidateLabel[0][1]]
            print('候选标签：')
            print(freq_max_labels)
            for candidate in freq_max_labels:
                node_importance[candidate[0]]
            acceptedLabel = max(freq_max_labels, key=lambda x: node_importance[x[0]])[0]
            print(acceptedLabel)

            # Update listener memory
            if acceptedLabel in memory[listener]:
                memory[listener][acceptedLabel] += 1
            else:
                memory[listener][acceptedLabel] = 1

    # Stage 3:
    for node, mem in memory.items():
        # print(node, mem)
        maximum = 0
        flag = ''
        for label, fre in mem.items():
            if fre > maximum:
                maximum = fre
                flag = label
        memory[node] = flag

    # Find nodes membership
    # 扫描memory中的记录标签，相同标签的节点加入同一个社区中
    return memory


if __name__ == '__main__':

    data = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13), (1, 14), (1, 18), (1, 20), (1, 22), (1, 32),(2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31), (3, 4), (3, 8), (3, 9), (3,10), (3, 14), (3, 28), (3, 29), (3, 33), (4, 8), (4, 13), (4, 14), (5, 7), (5, 11), (6, 7), (6, 11), (6, 17), (7, 17), (9, 31), (9, 33), (9, 34), (10, 34), (14, 34), (15, 33), (15, 34), (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34), (24, 26), (24, 28), (24, 30), (24, 33), (24, 34), (25, 26), (25, 28), (25, 32), (26, 32), (27, 30), (27, 34), (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 33), (31, 34), (32, 33), (32, 34), (33, 34)]
    G = nx.Graph()
    G.add_edges_from(data)
    result = find_communities(G, 50)
    community = {}
    for k, v in result.items():
        community.setdefault(v, [])
        community[v].append(k)
    print(community)
    for value in community.values():
        print(sorted(value))
