import random
import matplotlib.pyplot as plt
import networkx as nx
import copy
from copy import deepcopy
import time
from graph import arcs_5
from num import A_2060
from num import A_40200
from num import A_50500


#设置全局变量并初始化

nu=50 #无人机数量
nt=500#任务量
nf=5 #联邦数量
minadd=1 #定义最小增量
ns=20 #根据任务分成几组
ni=[10]*nu #每个无人机最大可执行的任务,这里统一规定为3
nki=[([1]*ns) for i in range(nu)] #对于每一个分组，每一个无人机最多可执行的任务，这里统一规定为1
#print(nki)
K_dic={} #分组对应字典
avek=int(nt/ns) #每个分组有多少个成员
for i in range(nt):#建立任务和任务分组关系的字典
    K_dic[i]=int(i/avek)
#K_old=[([0]*nt) for i in range(ns)] #初始化原有多少已经中标
all_set=set([x for x in range(nt)]) #定义全集
Kall_set=[] #定义分组的全集
for i in range(ns):
    Kall_set.append(set([x for x in range(i*avek,(i+1)*avek)]))

F_dic={} 
avef=int(nu/nf) #每个联邦有多少个成员
for i in range(nu):#建立无人机和联邦号的对应字典
    F_dic[i]=int(i/avef)

A=[([0]*nt) for i in range(nu)]  #定义收益二维矩阵
A=A_50500
arcs_f=arcs_5
# arcs_f=[([0]*nf) for i in range(nf)]
# #cnt=0
# for i in range(nf):
#     for j in range(nf):
#         if i<j:
#             arcs_f[j][i]=arcs_f[i][j]=random.randint(0,1)
G=nx.Graph()  # 新建一个无向图
nodes=[]
edges=[]
for i in range(nf):
    G.add_node(i)
for i in range(nf):
    for j in range(nf):
        if arcs_f[i][j]==1:
            G.add_edge(i,j)
netdiameter_f=nx.diameter(G)
# nx.draw(G,with_labels=True)
# plt.show()

P_f=[[0]*nt for i in range(nf)] #初始化价格向量P
#print(P)
P_all=[([0]*nt) for i in range(nu)] #定义P_all为每次投标时各无人机的出价，初始化为0
J=[([0]*nt) for i in range(nu)] #用于记录上一次每个无人机投标集合，0表示未投标，1表示投标
Pchange=[1]*nu #记录价格是否修改过，0表示此轮未修改，1表示此轮修改过
B_f=[[-1]*nt for i in range(nf)]



# 程序主函数
def BidingFirst_f(i):
    f_order=F_dic[i]
    V={}
    nil=ni[i]
    nkicopy=deepcopy(nki)
    for j in range(nt):
        V[j]=A[i][j]-P_f[f_order][j] #计算每个商品的当前收益
    #print(V)
    V_order=sorted(V.items(),key=lambda x:x[1],reverse=True) 
    #print(V_order)
    re_K=[set() for i in range(ns)] #用于记录每个分组想投标的集合
    #print(re_K)
    k_secondprice=[0]*ns #用于记录每个分组的次优价格
    k_flag=[0]*ns #用于辅助记录次优价格，1表示已经存过
    
    for j in range(nt):
        k_ord=K_dic[V_order[j][0]] #根据物品j查的其所在分组的下标
        if k_flag==[1]*ns: #当所有分组次优价格都记录后退出循环
            break
        if  V_order[j][1]>0 and nkicopy[i][k_ord]>0: #如果价值大于0且没到分组限制上限
            #ni[i]-=1
            nkicopy[i][k_ord]-=1
            #re_J.add(V_order[j][0])
            re_K[k_ord].add(V_order[j][0])
        else:
            if V_order[j][1]>0 and k_flag[k_ord]==0:
                k_secondprice[k_ord]=V_order[j][1]
                k_flag[k_ord]=1
            elif V_order[j][1]<=0 and k_flag[k_ord]==0:
                k_secondprice[k_ord]=0
                k_flag[k_ord]=1
    # print(nki[i])
    # print(k_flag)
    #print(k_secondprice)  
    # print(re_K)
    #print(re_J)
    kchose_set=set() #用于记录投标全集
    for k in range(ns):
        kchose_set=kchose_set|re_K[k]
    C={}
    cnt=0
    for j in kchose_set:
        C[j]=V[j]
        cnt+=1
    C_order=sorted(C.items(),key=lambda x:x[1],reverse=True) 
    #print(C_order)
    #print(cnt)
    #print(kchose_set)

    re_J=set([])
    for j in range(cnt):
        if nil<=0: #若超过载核限制则退出
            break
        nil-=1
        re_J.add(C_order[j][0])
        #print(j,nil)
    #print(re_J)
    #储存载核的次优价格
    if ni[i]>=cnt: 
        secondprice=0
    else:
        secondprice=C_order[j][1]
    # for k in range(ns):
    #     print(Kall_set[k]-re_K[k])
    #print(secondprice)
    #更新任务分配信息
    for j in re_J:
        J[i][j]=1
    #print(J[i])
    #更新价格
    for j in re_J:
        k_ord=K_dic[j]
        maxsecondprice=max(secondprice,k_secondprice[k_ord])
        P_all[i][j]=round(P_all[i][j]+V[j]-maxsecondprice+minadd,4)
    #print(P_all[i])

    
    

def BidingPhase_f(i): #定义投标阶段函数，参数i为第i个无人机投标
    f_order=F_dic[i]
    re_Knum=[0]*ns #每一组当前含最高价格的投标数
    re=0 #需要重新投标数
    J_old=set()
    #print(J[i])
    for j in range(nt): #将列表转化为集合
        if J[i][j]==1:
            J_old.add(j)
    #print(J_old)
    for j in J_old.copy():
        #非当前最高价需要重新投标或者存在同时最高价，低优先级无人机需要重新投标
        if P_all[i][j]<P_f[f_order][j] or P_all[i][j]==P_f[f_order][j] and B_f[f_order][j]!=i :
            J_old.remove(j)
            J[i][j]=0 #重新投标清除标记
            re+=1
        #记录各分组当前中标数量
        elif P_all[i][j]>P_f[f_order][j] or P_all[i][j]==P_f[f_order][j] and B_f[f_order][j]==i :
            k_ord=K_dic[j]
            re_Knum[k_ord]+=1
    #print(re_Knum)
    #print(J_old)
    new_Knum={} #每个分组需要补充的数量，使用字典表示
    secondnum=0 #记录有多少个组需要重新补充任务
    for k in range(ns):
        if nki[i][k]-re_Knum[k]!=0:
            new_Knum[k]=nki[i][k]-re_Knum[k]
            secondnum+=1
    #print(new_Knum)
    #print(secondnum)
    V={}
    #print(re)
    #print(J_old)
    #print(A[i])
    for j in range(nt):
        V[j]=round(A[i][j]-P_f[f_order][j],4) #计算每个商品的当前收益,小数点保留四位
    #print(V)
    V_order=sorted(V.items(),key=lambda x:x[1],reverse=True) 
    #print(V_order)
    leftset=all_set-J_old #再余下的集合中将投标补至ni
    #print(leftset)
    

    re_K=[set() for i in range(ns)] #用于记录每个分组想投标的集合
    #print(re_K)
    k_secondprice=[0]*ns #用于记录每个分组的次优价格
    k_flag=[0]*ns #用于辅助记录次优价格，1表示已经存过
    flagnum=0
    for j in range(nt):
        k_ord=K_dic[V_order[j][0]] #根据物品j查的其所在分组的下标
        if new_Knum=={}:
            break
        jud = all(x == 0 for x in new_Knum.values())
        if jud and flagnum==secondnum: #
            break
        if V_order[j][0] in leftset and k_ord in new_Knum.keys():
            if  V_order[j][1]>0 and new_Knum[k_ord]>0: #如果价值大于0且没到分组限制上限
                new_Knum[k_ord]-=1
                re_K[k_ord].add(V_order[j][0])
            else:
                if V_order[j][1]>0 and k_flag[k_ord]==0:
                    k_secondprice[k_ord]=V_order[j][1]
                    k_flag[k_ord]=1
                    flagnum+=1
                elif V_order[j][1]<=0 and k_flag[k_ord]==0:
                    k_secondprice[k_ord]=0
                    k_flag[k_ord]=1
                    flagnum+=1
    #print(re_K)
    #print(k_secondprice)
    # print()  

    kchose_set=set() #用于记录投标全集
    for k in range(ns):
        kchose_set=kchose_set|re_K[k]
    C={}
    cnt=0
    for j in kchose_set:
        C[j]=V[j]
        cnt+=1
    C_order=sorted(C.items(),key=lambda x:x[1],reverse=True) 
    #print(C_order)
    #print(cnt)
    #print(kchose_set)

    re_J=set([])
    for j in range(cnt):
        if re<=0: #若超过载核限制则退出
            break
        re-=1
        re_J.add(C_order[j][0])
    #print(re_J)
    #储存载核的次优价格
    if ni[i]>=cnt: 
        secondprice=0
    else:
        secondprice=C_order[j][1]
    # for k in range(ns):
    #     print(Kall_set[k]-re_K[k])
    #print(secondprice)
    #print()
    #更新任务分配信息
    for j in re_J:
        J[i][j]=1
    #print(J[i])
    #更新价格
    if re_J==set():
        Pchange[i]=0
    else:
        for j in re_J:
            k_ord=K_dic[j]
            maxsecondprice=max(secondprice,k_secondprice[k_ord])
            P_all[i][j]=round(P_all[i][j]+V[j]-maxsecondprice+minadd,4)
        Pchange[i]=1
    
    #print(P_all[i])

start=time.time()

for i in range(nu): #第一轮价格初始化
    BidingFirst_f(i)

for j in range(nt): #第一轮联邦内价格一致阶段
    for f in range(nf): #每一个联邦进行价格一致
        for i in range(f*avef,(f+1)*avef):
            if P_all[i][j]==0 and P_f[f][j]==0:
                    continue
            elif P_all[i][j]>P_f[f][j]:
                P_f[f][j]=P_all[i][j]
                B_f[f][j]=i
            elif P_all[i][j]==P_f[f][j] and i>B_f[f][j]:
                B_f[f][j]=i


n=0
lcr=0 #least communication rounds停止需要的最少轮次
while(1):
    for f in range(nf):
        for fb in range(nf):
            if arcs_f[f][fb]==1:
                for j in range(nt):
                    if P_f[fb][j]>P_f[f][j]:
                        P_f[f][j]=P_f[fb][j]
                        B_f[f][j]=B_f[fb][j]
                    if P_f[fb][j]==P_f[f][j] and B_f[fb][j]>B_f[f][j]:
                        B_f[f][j]=B_f[fb][j]

    #每一轮竞标之前，代理通讯阶段
    for i in range(nu):
        BidingPhase_f(i)
    #print(pri)
    for j in range(nt): #第一轮联邦内价格一致阶段
        for f in range(nf): #每一个联邦进行价格一致
            for i in range(f*avef,(f+1)*avef):
                if P_all[i][j]==0 and P_f[f][j]==0:
                        continue
                elif P_all[i][j]>P_f[f][j]:
                    P_f[f][j]=P_all[i][j]
                    B_f[f][j]=i
                elif P_all[i][j]==P_f[f][j] and i>B_f[f][j]:
                    B_f[f][j]=i
    n+=1
    # print(n)
    # print(P_all)
    #print(P)
    # print(J)
    if Pchange==[0]*nu:
        lcr+=1
        if lcr==netdiameter_f:
            break
    else:
        lcr=0

end=time.time()

print("迭代次数%d"%n)
sum=0
for i in range(nu):
    print("无人机%d选择了目标"%i,end='')
    for j in range(nt):
        if J[i][j]==1:
            sum+=A[i][j]
            print("%d(%d),"%(j,K_dic[j]),end='')
    print('')            
print("总收益值为%d"%sum)
print(end-start)
