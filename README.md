# Projects
# DPLL Sat Solver 	
Python Code file named "solver_dpll_rec.py" conatin the code to for solver to apply to the problems provided in cnf form.	
Instruction for the input file:
	1) This folder contain files with extention .cnf , use the name of the files in command line arguments to test the program for respective input file.	
	Instructions for running the python code file:
		1) To run the py code on terminal , just write the following command:
		python3 solver_dpll_rec.py [input_file] [heuristic : MO , SPC , JW]
		e.g.    python3 solver_dpll_rec.py aim-50-1_6-yes1-4.cnf SPC	
		where after program name, first argument is name of input file and next is the heuristic.
	
	Instructions for checking the output:	
		1) on console , you can check the result for the particular input.
		2) Assignment for the valid and satisfiable clauses can also be checked from "Assignment.txt".
Writeup is include in folder named : "SAT_Solver_DPLL_heuristics.pdf"





