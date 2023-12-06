import random
import matplotlib.pyplot as plt
import networkx as nx


nu=5
arcs=[([0]*nu) for i in range(nu)]
#cnt=0
for i in range(nu):
    for j in range(nu):
        if i<j:
            arcs[j][i]=arcs[i][j]=random.randint(0,1)
            # if arcs[j][i]==1:
            #     cnt+=1
#print(cnt)
for i in range(nu):
    print(arcs[i])
print(arcs)

G=nx.Graph()  # 新建一个无向图
nodes=[]
edges=[]
for i in range(nu):
    G.add_node(i)
for i in range(nu):
    for j in range(nu):
        if arcs[i][j]==1:
            G.add_edge(i,j)
print(nx.diameter(G))
nx.draw(G,with_labels=True)
plt.show()
