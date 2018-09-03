from random import randint
import numpy as np
from copy import copy,deepcopy


class Skyscraper:

    def __init__(self,N=4,see_list = [],const_list=[]):
        pass
        self.N = N
        #self.state =  np.array([N*[i+1] for i in range(N)])

        self.state = np.array([[0 for _ in range(self.N)] for i in range(self.N)])

        #The way I'm gonna organize this is as a list of lists, where it goes
        #left, right, top, down
        self.see_list = np.array(see_list)

        self.const_list = const_list
        for const in self.const_list:
            ind = const[0]
            val = const[1]
            self.state[ind[0],ind[1]] = val


        self.const_list_indices = [x[0] for x in self.const_list]
        #print(self.const_list)
        #print(self.const_list_indices)

        self.max_FF = 16*(self.N-1) + 8*(self.N)



    def printState(self):
        board = '\n\n'

        #board = board + '  ' + ' '.join([str(x) for x in self.see_list[2]]) + '\n'

        #board = board + '  ' + '__'*(self.N-1) + '_' + ' ' + '\n'

        board = board + '  ' +  '\033[4m' + ' '.join([str(x) for x in self.see_list[2]]) +  '\033[0m' + '\n'

        """for i in range(self.N):

            board = board + str(self.see_list[0][i]) + '|'

            board = board + ' '.join([str(x) for x in self.state[i,:]])

            board = board + '|' + str(self.see_list[1][i])

            board = board + '\n'"""

        for i in range(self.N-1):

            board = board + str(self.see_list[0][i]) + '|'

            board = board + ' '.join([str(x) for x in self.state[i,:]])

            board = board + '|' + str(self.see_list[1][i])

            board = board + '\n'

        board = board + str(self.see_list[0][self.N-1]) + '|'

        board = board + '\033[4m' + ' '.join([str(x) for x in self.state[self.N-1,:]]) + '\033[0m'

        board = board + '|' + str(self.see_list[1][self.N-1])

        board = board + '\n'

        #board = board + '  ' + '‾‾'*(self.N-1) + '‾' + ' ' + '\n'
        board = board + '  ' + ' '.join([str(x) for x in self.see_list[3]]) + '\n'

        print(board)

    def countSeen(self,sel,row_num):
        #will return a tuple of what you see from the left and right if you pass it 'row',
        #up and down if you pass it 'col'

        if sel=='row':
            row = self.state[row_num]
        if sel=='col':
            row = self.state[:,row_num]

        #print(row)
        max_left = max_right = -10000
        seen_left = seen_right = 0

        for i in range(self.N):
            if row[i]>max_left:
                max_left = row[i]
                seen_left += 1
                if row[i]==self.N:
                    break

        #and for from the other direction:
        row = np.flip(row,axis=0)
        #print(row)
        for i in range(self.N):
            if row[i]>max_right:
                max_right = row[i]
                seen_right += 1
                if row[i]==self.N:
                    break

        #print([seen_left,seen_right])
        return([seen_left,seen_right])



    def countOccurrenceErrors(self):

        base_occur = [-1]*self.N

        error_sum = 0

        for i in range(self.N):

            occur_row = copy(base_occur)
            occur_col = copy(base_occur)

            for j in range(self.N):

                occur_row[self.state[i,j]-1] += 1
                occur_col[self.state[j,i]-1] += 1


            #print('there are {} errors in row {}'.format(sum(np.absolute(occur_row)), i))
            #print('there are {} errors in col {}'.format(sum(np.absolute(occur_col)), i))
            error_sum += sum(np.absolute(occur_row)) + sum(np.absolute(occur_col))

        return(error_sum)

    def fitnessFunction(self):

        occur_errors = self.countOccurrenceErrors()

        seen_errors = 0

        for i in range(self.N):
            row_seen = self.countSeen('row',i)
            col_seen = self.countSeen('col',i)

            row_seen_error = sum(np.absolute(row_seen - self.see_list[[0,1],i]))
            col_seen_error = sum(np.absolute(col_seen - self.see_list[[2,3],i]))

            #print('row_seen_error',row_seen_error)
            #print('col_seen_error',col_seen_error)
            seen_errors += row_seen_error + col_seen_error

        return(occur_errors + seen_errors)

    def solFound(self):
        if self.fitnessFunction()<1:
            return(True)
        else:
            return(False)

    def isSameState(self,other):
        return((self.state==other.state).all())

    def mutate(self):
        row = randint(0,self.N-1)
        col = randint(0,self.N-1)
        if [row,col] not in self.const_list_indices:
            self.state[row,col] = randint(1,self.N)


    def mate(self,other):

        new_1 = deepcopy(self)
        new_2 = deepcopy(other)

        r1 = randint(0,self.N-1)
        r2 = randint(r1+1,self.N)

        c1 = randint(0,self.N-1)
        c2 = randint(c1+1,self.N)

        temp_slice = copy(new_1.state[r1:r2,c1:c2])
        new_1.state[r1:r2,c1:c2] = copy(new_2.state[r1:r2,c1:c2])
        new_2.state[r1:r2,c1:c2] = temp_slice

        return((new_1,new_2))













#
