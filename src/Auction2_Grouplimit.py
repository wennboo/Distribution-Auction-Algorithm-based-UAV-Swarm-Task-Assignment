import random
import copy
from copy import deepcopy
import time
from num import A_2060
from num import A_40200
from num import A_50500


#设置全局变量并初始化
nu=20 #无人机数量
nt=60#任务量
minadd=1 #定义最小增量
ns=4 #根据任务分成几组
ni=[3]*nu #每个无人机最大可执行的任务,这里统一规定为3
nki=[([1]*ns) for i in range(nu)] #对于每一个分组，每一个无人机最多可执行的任务，这里统一规定为1
#print(nki)
K_dic={}
ave=int(nt/ns) #每个分组有多少个成员
for i in range(nt):#建立任务和任务分组关系的字典
    K_dic[i]=int(i/ave)
#K_old=[([0]*nt) for i in range(ns)] #初始化原有多少已经中标
all_set=set([x for x in range(nt)]) #定义全集
Kall_set=[] #定义分组的全集
for i in range(ns):
    Kall_set.append(set([x for x in range(i*ave,(i+1)*ave)]))

A=[([0]*nt) for i in range(nu)]  #定义收益二维矩阵
A=A_2060
#A=[[3, 17, 1, 19, 18, 17, 13, 20, 3], [5, 8, 5, 3, 8, 14, 16, 1, 6], [17, 17, 10, 9, 2, 13, 0, 2, 20]]
# A=[[11,18,11,18,33,4],[4,34	,33	,32	,26	,23],[3	,0	,27	,24	,14	,9],[25	,15	,25	,23	,7	,26],[30	,18	,34	,20	,17	,29],[5	,35	,34	,4	,17	,28]]
#A=[[4,2,0],[1,3,1],[3,3,2]]

# for i in range(nu):
#     for j in range(nt):
#         A[i][j]=random.randint(0,20) #生成0-20内的随机数作为收益
# print(A)
#print(A[0])
P=[0]*nt #初始化价格向量P
#print(P)
P_all=[([0]*nt) for i in range(nu)] #定义P_all为每次投标时各无人机的出价，初始化为0
J=[([0]*nt) for i in range(nu)] #用于记录上一次每个无人机投标集合，0表示未投标，1表示投标
Pchange=[1]*nu #记录价格是否修改过，0表示此轮未修改，1表示此轮修改过

# L=[1,2,3]
# S=set(L)
# S1=S.copy()
# for s in S.copy():
#     if s==1:
#         S.remove(s)
# print(S)
# print(S1)



# 程序主函数
def BidingFirst(i):
    V={}
    nil=ni[i]
    nkicopy=deepcopy(nki)
    for j in range(nt):
        V[j]=A[i][j]-P[j] #计算每个商品的当前收益
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

    
    

def BidingPhase(i): #定义投标阶段函数，参数i为第i个无人机投标
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
        if P_all[i][j]<P[j] or P_all[i][j]==P[j] and pri[i][j]==0 :
            J_old.remove(j)
            J[i][j]=0 #重新投标清除标记
            re+=1
        #记录各分组当前中标数量
        elif P_all[i][j]>P[j] or P_all[i][j]==P[j] and pri[i][j]==1 :
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
        V[j]=round(A[i][j]-P[j],4) #计算每个商品的当前收益,小数点保留四位
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
    BidingFirst(i)
pri=[([0]*nt) for i in range(nu)]#定义优先级，若投标值相等时，优先级为0则表示未中标，1表示中标,每一轮初始均为0
for j in range(nt): #第一轮价格一致阶段
    l=-1
    m=-1
    for i in range(nu):#在此方法中序号越高的无人机优先级越高
        if P_all[i][j]==0 and P[j]==0:
                continue
        elif P_all[i][j]>=P[j] :
            P[j]=P_all[i][j]
            l=i
            m=j
    if l!=-1 and m!=-1:
        pri[l][m]=1
# print(0)
# print(P_all)
# print(P)
# print(J)

# BidingPhase(0)
# BidingPhase(1)
# BidingPhase(2)                    
n=0
while(1):
    for i in range(nu):
        BidingPhase(i)
    #print(pri)
    pri=[([0]*nt) for i in range(nu)]#定义优先级，若投标值相等时，优先级为0则表示未中标，1表示中标,每一轮初始均为0
    # maxpos=[-1]*nt #用于记录当前最大价格的下标
    # #print(maxpos)
    # for u in range(nu):
    #     for j in range(nt):
    #         if P_all[u][j]==0 and P[j]==0: #都没有投标
    #             continue
    #         elif P_all[u][j]>P[j]:
    #             P[j]=P_all[u][j]
    #             maxpos[j]=u
    #         elif P_all[u][j]==P[j] and u>maxpos[j]:#如果优先级更高，那么更新最大下标集
    #             maxpos[j]=u
    # for j in range(nt):
    #     if maxpos[j]==-1:
    #         continue
    #     else:
    #         pri[maxpos[j]][j]=1
    for j in range(nt):
        l=-1
        m=-1
        for i in range(nu):
            if P_all[i][j]==0 and P[j]==0:
                continue
            elif P_all[i][j]>=P[j] :
                P[j]=P_all[i][j]
                l=i
                m=j
        if l!=-1 and m!=-1:
            pri[l][m]=1
    n+=1
    # print(n)
    # print(P_all)
    #print(P)
    # print(J)
    if Pchange==[0]*nu:
        break

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
