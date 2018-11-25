import numpy as np
from sklearn import metrics


# football实验结果
A = np.array(
    [78, 1, 15, 74, 78, 74, 15, 78, 78, 78, 74, 78, 31, 15, 31, 15, 78, 87, 31, 82, 87, 78, 78, 78, 78, 1, 31, 87, 78,
     82, 82, 31, 15, 1, 31, 82, 31, 1, 31, 15, 74, 78, 31, 31, 53, 1, 88, 15, 53, 88, 78, 78, 74, 88, 31, 82, 87, 53,
     88, 87, 15, 31, 87, 87, 15, 87, 53, 88, 78, 78, 87, 31, 74, 88, 74, 53, 87, 78, 78, 82, 82, 74, 82, 88, 74, 31, 53,
     87, 88, 1, 78, 53, 53, 78, 82, 87, 87, 74, 74, 31, 15, 82, 74, 1, 78, 1, 15, 74, 78, 1, 88, 78, 53, 87, 88])

node_dict = {}
with open(r'standard_result_devide\football标准结果.txt') as f:
    t = 0
    for line in f:
        node_dict[t] = [int(n) for n in line.strip().split(',')]
        t += 1

print(node_dict)
node_list = [0 for i in range(115)]
for i, j in node_dict.items():
    for k in j:
        node_list[k] = i
print(node_list)

# football标准划分结果
B = np.array(node_list)
print(metrics.normalized_mutual_info_score(A, B))