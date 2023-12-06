import random
from num import A_2060
from num import A_40200
from num import A_50500
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

minadd=0.01 #定义最小增量
x_minadd=[]
y_sum=[]
while(minadd<1):
    #设置全局变量并初始化
    nu=20 #无人机数量
    nt=60 #任务量


    ni=[3]*nu #每个无人机最大可执行的任务,这里统一规定为3
    #nki=[([2]*nu) for i in range(K)] #对于每一个分组，每一个无人机最多可执行的任务，这里统一规定为2
    #K=3 #根据任务分成几组

    all_set=set([x for x in range(nt)]) #定义全集
    #K_old=[([0]*nt) for i in range(K)] #初始化原有多少已经中标



    A=[([0]*nt) for i in range(nu)]  #定义收益二维矩阵
    A=A_2060
    #A=[[3, 17, 1, 19, 18, 17, 13, 20, 3], [5, 8, 5, 3, 8, 14, 16, 1, 6], [17, 17, 10, 9, 2, 13, 0, 2, 20]]
    #A=[[11,18,11,18,33,4],[4,34	,33	,32	,26	,23],[3	,0	,27	,24	,14	,9],[25	,15	,25	,23	,7	,26],[30	,18	,34	,20	,17	,29],[5	,35	,34	,4	,17	,28]]
    #A=[[4,2,0],[1,3,1],[3,3,2]]
    #A=[[90, 80, 75, 70],[35, 85, 55, 65],[125, 95, 90, 95],[45, 110, 95, 115],[50, 100, 90, 100],]
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
        for j in range(nt):
            V[j]=A[i][j]-P[j] #计算每个商品的当前收益
        #print(V)
        V_order=sorted(V.items(),key=lambda x:x[1],reverse=True) 
        #print(V_order)
        re_J=set([])
        for j in range(nt):
            if ni[i]<=0:
                break
            if  V_order[j][1]>0:
                ni[i]-=1
                re_J.add(V_order[j][0])
        #print(re_J)
        #储存次优价格
        if V_order[j][1]>0:
            secondprice=V_order[j][1]
        else:
            secondprice=0
        #print(secondprice)
        #更新任务分配信息
        for j in re_J:
            J[i][j]=1
        #print(J[i])
        #更新价格
        for j in re_J:
            P_all[i][j]=P_all[i][j]+V[j]-secondprice+minadd
        #print(P_all[i])

        
        

    def BidingPhase(i): #定义投标阶段函数，参数i为第i个无人机投标
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
        re_J=set([])
        for j in range(nt):
            if re<=0:
                break
            if V_order[j][0] in leftset and V_order[j][1]>0:
                re-=1
                re_J.add(V_order[j][0])
        #print(re_J)
        #储存次优价格
        if V_order[j][1]>0:
            secondprice=V_order[j][1]
        else:
            secondprice=0
        #print(secondprice)
        #更新任务分配信息
        for j in re_J:
            J[i][j]=1
        #print(J[i])
        #更新价格
        if re_J==set():
            Pchange[i]=0
        else:
            for j in re_J:
                P_all[i][j]=round(P_all[i][j]+V[j]-secondprice+minadd,4)
            Pchange[i]=1
        #print(Pchange[i])
        #print(P_all[i])   
            
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

            
    n=0
    while(1):
        for i in range(nu):
            BidingPhase(i)
        #print(pri)
        pri=[([0]*nt) for i in range(nu)]#定义优先级，若投标值相等时，优先级为0则表示未中标，1表示中标,每一轮初始均为0
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
        # print(P)
        # print(J)
        if Pchange==[0]*nu:
            break

    #print("迭代次数%d"%n)
    sum=0
    for i in range(nu):
        ##print("无人机%d选择了目标"%i,end='')
        for j in range(nt):
            if J[i][j]==1:
                sum+=A[i][j]
                ##print("%d,"%j,end='')
        #print('')            
    #print("总收益值为%d"%sum)
    x_minadd.append(minadd)
    y_sum.append(sum)
    minadd+=0.01

plt.plot(x_minadd, y_sum, linewidth=1)
plt.show()


