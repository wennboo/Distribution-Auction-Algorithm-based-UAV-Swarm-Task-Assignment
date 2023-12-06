import networkx as nx
import matplotlib.pyplot as plt
import random


nodes = [1, 2, 3, 4]
edge_list = [(1, 2), (2, 3), (2, 4), (3, 4)]

pos = {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0)}
# for e in edge_list:  # 添加边， 参数name为边权值
#     g.add_edge(e[0], e[1], name=e[2])
def test():
    fig = plt.figure()  # 生成画布
    plt.ion()  # 打开交互模式
    cnt=0
    while(cnt<=10):
        fig.clf()
        ax = fig.add_subplot(111)
        ax.set(xlim=[-10, 10], ylim=[-10, 10], title='An Example Axes',ylabel='Y-Axis', xlabel='X-Axis')
        plt.show()
        g = nx.Graph()  # 新建一个无向图
        g.add_nodes_from(nodes)
        g.add_edges_from(edge_list)
        l=len(nodes)
        for i in range(1,l+1):
            t=(pos[i][0]+random.randint(-1,1),pos[i][1]+random.randint(-1,1))
            pos[i]=t
        nx.draw(g,pos,ax,with_labels=True)
        plt.pause(1)
        cnt+=1
    # 关闭交互模式
    plt.ioff()
    plt.show()

test()


