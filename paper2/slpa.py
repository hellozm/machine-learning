import numpy as np
import networkx as nx
from collections import defaultdict


def find_communities(G, T, r):
    """
    Speaker-Listener Label Propagation Algorithm (SLPA)
    see http://arxiv.org/abs/1109.5720
    """

    # Stage 1: Initialization
    memory = {i: {i: 1} for i in G.nodes()}

    # Stage 2: Evolution
    # 开始遍历T次所有节点
    for t in range(T):
        # 随机排列遍历顺序
        listenersOrder = list(G.nodes())
        np.random.shuffle(listenersOrder)
        # 开始遍历节点
        # print(listenersOrder)
        # print(memory)
        for listener in listenersOrder:
            # 每个节点的key就是与他相连的节点标签名
            speakers = G[listener].keys()  # listener的邻居节点
            # print(speakers)
            if len(speakers) == 0:
                continue
            # 存放每个邻居节点出现次数最多的标签
            labels = defaultdict(int)  # key不存在时，返回的是工厂函数的默认值，比如list对应[ ]，str对应的是空字符串，set对应set( )，int对应0
            # 遍历所有与其相关联的节点
            for j, speaker in enumerate(speakers):
                # Speaker Rule
                # print(speaker)
                total = float(sum(memory[speaker].values()))  # 计算speaker节点记忆标签总数
                # print(total)

                # 论文中应该是随机选取一个，因为标签出现次数越多，相应地被选中的概率也就越大
                # 查看speaker中memory中出现概率最大的标签并记录，存在加1，不存在赋值1，key是标签名，value是Listener与speaker之间的权
                labels[list(memory[speaker].keys())[
                    np.random.multinomial(1, [freq / total for freq in memory[speaker].values()]).argmax()]] += 1

            # Listener Rule
            # 查看labels中值最大的标签，让其成为当前listener的一个记录
            acceptedLabel = max(labels, key=labels.get)

            # Update listener memory
            if acceptedLabel in memory[listener]:
                memory[listener][acceptedLabel] += 1
            else:
                memory[listener][acceptedLabel] = 1

    # Stage 3:
    for node, mem in memory.items():
        flag = []
        for label, freq in mem.items():
            if freq / float(T + 1) < r:
                flag.append(label)
        for f in flag:
            del mem[f]
        # print(mem)
        # print('--------------')

    # Find nodes membership
    # 扫描memory中的记录标签，相同标签的节点加入同一个社区中
    communities = {}
    for node, mem in memory.items():
        for label in mem.keys():
            if label in communities:
                communities[label].add(node)
            else:
                communities[label] = set([node])

    # Remove nested communities
    nestedCommunities = set()
    keys = list(communities.keys())
    for i, label0 in enumerate(keys[:-1]):
        comm0 = communities[label0]
        for label1 in keys[i + 1:]:
            comm1 = communities[label1]
            if comm0.issubset(comm1):
                nestedCommunities.add(label0)
            elif comm0.issuperset(comm1):
                nestedCommunities.add(label1)

    for comm in nestedCommunities:
        del communities[comm]
    return communities


if __name__ == '__main__':
    G = nx.read_gml(r'dataset\football.gml', label='id')

    result = find_communities(G, 20, 0.45)
    print(result)
    count = []
    t = 0
    for k, v in result.items():
        count.append(len(result[k]))
        print(len(result[k]), end=' ')
        t += 1
    print()
    print(sum(count), t)
