nu=20
avef=4
nt=60
nf=5
for j in range(nt): #第一轮价格一致阶段
    for f in range(nf): #每一个联邦进行价格一致
        print()
        for i in range(f*avef,(f+1)*avef):
            print(i,end='')