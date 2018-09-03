from __future__ import print_function
from Skyscraper import Skyscraper
import sys
from ortools.constraint_solver import pywrapcp
import numpy as np
from time import time

med_88_SS = [[2,3,2,4,4,2,3,1],[1,3,5,3,2,3,2,4],[2,3,2,2,4,6,3,1],[1,2,3,4,3,2,2,4]]
med_88_constlist = [([0,1],1),([1,3],1),([2,1],3),([3,2],3),([4,2],6),([4,3],3),([4,5],5),([5,0],4),([5,4],6),([6,1],2),([6,4],1),([7,4],5)]

hard_88_ss = [[3,2,0,0,0,0,4,0],[3,0,2,4,4,2,0,0],[0,3,0,4,5,4,0,0],[0,3,4,0,2,1,4,2]]
hard_88_constlist = [([1,1],2),([2,1],5),([2,3],3),([4,3],4),([3,7],2),([5,5],1),([6,1],3),([6,7],1),([7,4],3)]

ss_99 = [[1,4,5,2,3,2,3,2,4],[2,2,2,3,4,3,1,3,5],[1,4,3,3,4,3,3,2,2],[4,2,3,2,1,3,2,3,3]]
ss_99_constlist = [([0,3],6),([0,7],2),([1,0],3),([1,8],6),([2,0],5),([2,3],7),
([2,6],2),([3,1],1),([3,5],2),([3,6],8),([4,6],7),([4,7],5),
([5,1],4),([5,3],1),([5,7],7),([5,8],3),([6,1],3),([6,3],5),
([6,4],1),([7,5],3),([7,7],8),([8,5],7)]

see_list = ss_99
const_list = ss_99_constlist
#see_list=[[4,2,2,1],[1,2,2,4],[4,2,2,1],[1,2,2,4]]
#left (t to b), right (t to b), top (l to r), down (l to r)
#s = Skyscraper(4,see_list=[[2,1,3,4],[2,1,3,4],[2,1,3,4],[2,1,3,4]])
size = len(see_list[0])
s = Skyscraper(size,see_list=see_list)
s.printState()


# Creates the solver.
solver = pywrapcp.Solver("simple_example")

#Create the variables we'll solve for
ss_vars = np.array([[solver.IntVar(1, size, "a_{}{}".format(i,j)) for j in range(size)] for i in range(size)])

#CONSTRAINTS

# All rows and columns must be different.
for i in range(len(ss_vars)):
    solver.Add(solver.AllDifferent(ss_vars[i,:].tolist()))
    solver.Add(solver.AllDifferent(ss_vars[:,i].tolist()))

#Make the 'buildings seen' correct.
#I'm going to do it in pairs, because the way it is, I have to reverse stuff.
#'sidepair 0' are going to be the left and right sides, where the var list will have to be switched for the right.
#similarly, sidepair 1 is for the top and bottom.
for entry in range(size):
    #left and right
    sidepair = 0
    left_top = 2*sidepair
    right_bot = 2*sidepair + 1
    #print('adding constraint for left/right sidepair {}, entry {}: {} and {}'.format(sidepair,entry,see_list[left_top][entry],see_list[right_bot][entry]))
    if see_list[left_top][entry]!=0:
        solver.Add((1 + solver.Sum([solver.Min(solver.Max(ss_vars[entry,:j+1].tolist()) - solver.Max(ss_vars[entry,:j].tolist()),1) for j in range(1,size)])) == see_list[left_top][entry])
    if see_list[right_bot][entry]!=0:
        solver.Add((1 + solver.Sum([solver.Min(solver.Max(ss_vars[entry,-(j+1):].tolist()) - solver.Max(ss_vars[entry,-j:].tolist()),1) for j in range(1,size)])) == see_list[right_bot][entry])
    #top and bottom
    sidepair = 1
    left_top = 2*sidepair
    right_bot = 2*sidepair + 1
    #print('adding constraint for left/right sidepair {}, entry {}: {} and {}'.format(sidepair,entry,see_list[left_top][entry],see_list[right_bot][entry]))
    if see_list[left_top][entry]!=0:
        solver.Add((1 + solver.Sum([solver.Min(solver.Max(ss_vars[:j+1,entry].tolist()) - solver.Max(ss_vars[:j,entry].tolist()),1) for j in range(1,size)])) == see_list[left_top][entry])
    if see_list[right_bot][entry]!=0:
        solver.Add((1 + solver.Sum([solver.Min(solver.Max(ss_vars[-(j+1):,entry].tolist()) - solver.Max(ss_vars[-j:,entry].tolist()),1) for j in range(1,size)])) == see_list[right_bot][entry])

#Add constraints for given constants, if there are any
for const in const_list:
    ind = const[0]
    val = const[1]
    solver.Add(ss_vars[ind[0],ind[1]] == val)


#Soluion collector
collector = solver.AllSolutionCollector()
collector.Add(ss_vars.flatten().tolist())

#The "decision builder". I just used the one from:
#https://developers.google.com/optimization/cp/cp_tasks
db = solver.Phase(ss_vars.flatten().tolist(), solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

#Solve it!
time_limit_s = 1
solver.TimeLimit(1000*time_limit_s)
print('\n\nstarting solver with {}s time limit!'.format(time_limit_s))
start_time = time()
solver.Solve(db, [collector])
print('\ndone after {:.2f}s'.format(time()-start_time))

#print solutions
print('\nthis many solutions found:',collector.SolutionCount())
for sol_num in range(collector.SolutionCount()):
    sol = np.array([[collector.Value(sol_num,ss_vars[i,j]) for j in range(size)] for i in range(size)])
    print('\nsolution #{}:\n'.format(sol_num))
    print(sol)




#
