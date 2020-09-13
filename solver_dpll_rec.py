#!/usr/bin/env python
# coding: utf-8

# In[14]:


#importing libraries
import random
import sys
import math
import time

#global variables
n_var=0
n_clauses=0
heuristic = 'most_often'


#function to be used to display error
def display_error(s,i):
    if i==1:
        print('input error')
    elif i==2:
        print('command line arguments error')
    print(s)
    sys.exit()


#funtion to find all the unit length clauses in cnf formula
def find_unaries(cnf_formula):
    res = [c for c in cnf_formula if len(c) == 1]
    return res


#function to read the cnf formula from input file
def read_file(filename):
    cnf = []
    #n_var,n_clauses are declared as global , so that these global variables can be set here inside this function  
    global n_var, n_clauses      
    f = open(filename, "r")
    while True:
        line = f.readline()
        #skip lines if it starts with c.
        if not line.startswith('c'):
            break
    #if after comments, first line does not starts with p , then it is not in valid format.
    if not line.startswith('p cnf'):
        display_error('Expecting "p cnf" in the beginning of the input file',1)
    else:
        word = line.split()
        n_var = int(word[2])
        n_clauses = int(word[3])
    #if control reaches here, means input file is in valid format, hence read the clauses
    for line in f:
        clause = []
        for x in line[:-2].split():
            #if literal absolute value exceed the number of variables , then raise input error.
            if abs(int(x)) > n_var:
                display_error('Literal index larger than declared on the first line', 1);
            #literal is valid hence added to the clause
            elif x not in clause:
                clause.append(int(x))
        if(len(clause)==0):
            display_error('Empty clause not allowed in input formula',1) 
        #add clause to the cnf
        cnf.append(clause)
    return cnf
#end of read cnf.


#function to apply conditioning on cnf based on literal.
def bcp(cnf_formula, literal):
    cnf_modified = []
    for clause in cnf_formula:
        clause_tba =[]
        #clause contains -literal, then that literal needs to be removed from the clause
        if -literal in clause:
            clause_tba = [x for x in clause if x != -literal]
            if not clause_tba:
                return -1
            cnf_modified.append(clause_tba)
        #literal present in clause, then that clause will be true, hence no need to consider that anymore
        if literal in clause:
            continue
        else:
            #if literal and its negation both are not present in cnf, then clause should be remained in cnf.
            cnf_modified.append(clause)
    return cnf_modified


#unit resolution
def unit_resol(conditioned_cnf):
    var_assign=[]
    unaries = find_unaries(conditioned_cnf)
    #perform unit resolution till there are unit clauses present
    while len(unaries)>0:
        lit = unaries[0]
        conditioned_cnf = bcp(conditioned_cnf, lit[0])
        var_assign+= [lit[0]]
        if conditioned_cnf == -1:
            return -1,[]
        if len(conditioned_cnf)==0:
            return conditioned_cnf, var_assign
        unaries = find_unaries(conditioned_cnf)
    return conditioned_cnf, var_assign


#dpll flow using recursion
def dpll_rec(cnf, assignment):
    #apply unit resolution on the cnf with the unit clauses which are present in cnf initially.
    cnf, unit_assignment = unit_resol(cnf)
    #add these unit cluases to the assignment
    assignment = assignment + unit_assignment
    #cnf ={} , i.e. valid cnf and assignment will give a assignment for which cnf is true.
    if not cnf:
        return assignment
    
    #if and empty clause found in cnf , then unsatisfiable,
    #[this will be final , if no decision variable is present , else recusion will play it's role]
    if cnf == - 1:
        return []
    
    #if unit cluases exhaust and cnf size is >1
    #decide a variable based on the heuristic.
    decision_variable = heuristic(cnf)
    solution = dpll_rec(bcp(cnf, decision_variable), assignment + [decision_variable])
    if not solution:
        solution = dpll_rec(bcp(cnf, -decision_variable), assignment + [-decision_variable])

    return solution
#end of dpll_recursive


#heuristics for deciding the heuristics
def type_heur(heuristic):
    if heuristic == 'MO':
        return most_often
    if heuristic == 'SPC':
        return shortest_positive_clause
    if heuristic == 'JW':
        return jeroslow_wang
    else:
        display_error("HEURISTIC ERROR: Not valid heuristic. " + heuristic +
                 "\nValid heuristics are: \n" "MO , SPC , JW \n",1)
        

#count the appearances of literals in the clause
def get_counter(cnf):
    counter = {}
    for clause in cnf:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


#count the appearnces and provide the weight to the literal based on length of clause it appeared.
def get_weighted_counter(cnf, weight=2):
    counter = {}
    for clause in cnf:
        for literal in clause:
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return counter        
        
        

#selecting the liten which is most occurred        
def most_often(cnf):
    counter = get_counter(cnf)
    return max(counter, key=counter.get)


#selecting the smallest positive clause's firts literal as decision literal
def shortest_positive_clause(cnf):
    min_len = math.inf
    chosen_lit = 0
    for clause in cnf:
        negatives = sum(1 for literal in clause if literal < 0)
        if not negatives and len(clause) < min_len:
            chosen_lit = clause[0]
            min_len = len(clause)
    if not chosen_lit:
        return cnf[0][0]
    return chosen_lit


#jeroslow_wang heuristic
def jeroslow_wang(cnf):
    counter = get_weighted_counter(cnf)
    return max(counter, key=counter.get)


# Main
def main():
    global n_var
    global heuristic
    #noted the start time of the program 
    start_time = time.time()
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        display_error("Use: %s <cnf_file> [<branching_heuristic>]" % sys.argv[0],2)

    if len(sys.argv) == 3:
        heuristic = type_heur(sys.argv[2])
    else:
        heuristic = shortest_positive_clause
    cnf = read_file(sys.argv[1])
    
    #name of the output file
    output_file = 'Assignment.txt'
    
    #call to dpll
    sol = dpll_rec(cnf, [])
    
    #writing result to the screen and file.
    #writing the assignment to the output file only when cnf is satisfiable.
    #end time is stored.
    end_time = time.time()
    print('Execution Time : '+ str(end_time-start_time)), 
    fw = open(output_file, "w")
    if len(sol)>0:
        sol += [x for x in range(1, n_var + 1) if x not in sol and -x not in sol]
        sol.sort(key=abs)
        print('CNF is SATISFIABLE')
        print('Assignment to variables is ' + ' '.join([str(x) for x in sol]))
        print('End of Assignment')
        fw.write('CNF is SATISFIABLE\n')
        fw.write('Assignment to variables is \n' + ' '.join([str(x) for x in sol]))
        fw.write('\nEnd of Assignment')
    else:
        print('CNF is UNSATISFIABLE')
    fw.close()
#end of main.
        
        
#starting point
if __name__ == '__main__':
    main()


# In[ ]:




