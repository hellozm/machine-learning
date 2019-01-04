import networkx as nx


G = nx.read_gml(r'./polbooks.gml', label='id')
print(G.edges)
with open('polbooks.txt', 'a') as f:
    for edge in G.edges:
        start, end = edge
        content = str(start) + '\t' + str(end)
        f.write(content+'\n')