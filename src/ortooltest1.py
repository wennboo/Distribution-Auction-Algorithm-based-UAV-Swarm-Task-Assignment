from ortools.linear_solver import pywraplp
import random
from num import A_2060
from num import A_40200
from num import A_50500
import matplotlib.pyplot as plt

x_n=[]
y_sum=[]
def main(n):
    # Data
    # costs = [
    #     [90, 80, 75, 70],
    #     [35, 85, 55, 65],
    #     [125, 95, 90, 95],
    #     [45, 110, 95, 115],
    #     [50, 100, 90, 100],
    # ]
    A=[([0]*n) for i in range(n)]  #定义收益二维矩阵
    for i in range(n):
        for j in range(n):
            A[i][j]=random.randint(0,20) #生成0-20内的随机数作为收益
    costs=A
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        return

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if worker i is assigned to task j.
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0, 1, '')
    
    # Constraints
    # Each worker is assigned to at most 1 task.
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)

    # Objective
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Maximize(solver.Sum(objective_terms))

    # Solve
    status = solver.Solve()

    # # Print solution.
    # if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    #     print(f'Total cost = {solver.Objective().Value()}\n')
    #     for i in range(num_workers):
    #         for j in range(num_tasks):
    #             # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
    #             if x[i, j].solution_value() > 0.5:
    #                 print(f'Worker {i} assigned to task {j}.' +
    #                       f' Cost: {costs[i][j]}')
    # else:
    #     print('No solution found.')
    x_n.append(n)
    y_sum.append(solver.Objective().Value())
n=10
while(n<=100):
    main(n)
    n+=10
plt.plot(x_n,y_sum, linewidth=1,c='red')
plt.show()