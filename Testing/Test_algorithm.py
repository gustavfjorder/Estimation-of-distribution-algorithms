import sys
sys.path.append('C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP')
sys.path.append('C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP/ProblemTypes')
import math
from ProblemTypes.TSP import *
from Algorithms import Perms_1x1EA, EHBSA, EHBSA_wt, MallowsModel, GeneralizedMallowsModel, UMDA
import Sorting
import time
import numpy as np
import pandas as pd


TSPInstance = TSP()
Algorithms = {"Perms_1x1EA":Perms_1x1EA, "EHBSA":EHBSA, "EHBSA_wt":EHBSA_wt, "MallowsModel":MallowsModel, "GeneralizedMallowsModel":GeneralizedMallowsModel, "UMDA":UMDA}



path_to_tests = "C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP/TSP_instances/"
tests_TSP = ["ulysses22.txt", "att48.txt", "berlin52.txt", "st70.txt", "bier127.txt"]
tests_TSP = ["bier127.txt"]
tests_Sorting = [5,10,15,20,25]
# tests_Sorting = [30]

def RunTest(problem_type, Algorithm_name, pop_size_multiplier = 10, num_runs = 5, maxTime = 3*60):
    Algorithm = Algorithms[Algorithm_name]

    if problem_type == "TSP":
        tests = tests_TSP
        findIdentity = False
        res_fitness = {}
        res_individual = {}
        for instance in tests:
            res_individual[instance] = [None]*num_runs
            res_fitness[instance] = [None]*num_runs


    elif problem_type == "Sorting":
        tests = tests_Sorting
        findIdentity = True
        res_fitness_evals = {}
        res_time = {}

        for instance in tests:
            res_fitness_evals[instance] = [None]*num_runs
            res_time[instance] = [None]*num_runs
        
    else:
        raise ValueError("Must be ")


    for instance in tests:
        if problem_type == "TSP":
            ProblemInstance = TSPInstance.loadProblem(path_to_tests+instance)
        elif problem_type == "Sorting":
            ProblemInstance = Sorting.Sorting(instance)

        if pop_size_multiplier == "sqrt":
            pop_size = math.ceil(math.sqrt(ProblemInstance.dim))
        else:
            pop_size = pop_size_multiplier * ProblemInstance.dim

        print("Test",problem_type, Algorithm_name, instance)

        for test_num in range(num_runs):
            try:
                (val1, val2) = Algorithm.Run(problem_type,ProblemInstance, pop_size, maxTime = maxTime, NumberOfTemplateCuts=4, findIdentity = findIdentity)

                if problem_type == "TSP":
                    val2 = -val2
                    res_individual[instance][test_num] = val1
                    res_fitness[instance][test_num] = val2
                elif problem_type == "Sorting":
                    res_fitness_evals[instance][test_num] = val1
                    res_time[instance][test_num] = val2

                # print(val1,val2)
            except RuntimeError:
                print("runtime error",problem_type, Algorithm_name)
            except OverflowError as e:
                print("overflow error",problem_type, Algorithm_name,str(e))
            except Exception as e:
                print("Other error",sys.exc_info()[0],problem_type, Algorithm_name)

            ProblemInstance.ResetFitnessCount()

    path = "C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP/Testing/"

    path += problem_type
    path += "/Popsize_" + str(pop_size_multiplier)+"N/"
    path += Algorithm_name+"_"
    path += problem_type+"_"
    path += str(maxTime)+"s_"
    path += str(pop_size_multiplier)+"N_"
    path += time.strftime("%Y%m%d-%H%M%S")


    if problem_type == "TSP":
        df_res_fitness = pd.DataFrame(data=res_fitness)
        df_res_individual = pd.DataFrame(data=res_individual)
        
        df_res_fitness.to_excel(path+"_fitness.xlsx")
        df_res_individual.to_excel(path+"_individual.xlsx")
        print("Exported to Excel")
        
    elif problem_type == "Sorting":
        df_res_fitness_evals = pd.DataFrame(data=res_fitness_evals)
        df_res_time = pd.DataFrame(data=res_time)

        df_res_fitness_evals.to_excel(path+"_fitnessEvaluations.xlsx")
        df_res_time.to_excel(path+"_timeUsed.xlsx")
        print("Exported to Excel")

    print("Finished",problem_type, Algorithm_name)

RunTest("TSP", "GeneralizedMallowsModel", pop_size_multiplier = 1, num_runs = 5, maxTime = 30)