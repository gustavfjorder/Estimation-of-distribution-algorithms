import math
import sys
sys.path.append('C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP')
sys.path.append('C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP/ProblemTypes')
from ProblemTypes.TSP import *
TSP
import Sorting
# from TSP import TSP
from Algorithms import Perms_1x1EA, EHBSA, EHBSA_wt, MallowsModel, GeneralizedMallowsModel, UMDA

import visualization
import time
import numpy as np
import pandas as pd
from DistanceMeasures import HammingDistance, SwapDistance, CayleyDistance, NumberOfSortedBlocks, NegativeLengthOfLongestAscendingSubsequence

# Start timer
# startTime = time.time()
TSPInstance = TSP()
Algorithms = {"Perms_1x1EA":Perms_1x1EA, "EHBSA":EHBSA, "EHBSA_wt":EHBSA_wt, "MallowsModel":MallowsModel, "GeneralizedMallowsModel":GeneralizedMallowsModel, "UMDA":UMDA}
distances = {"Hamming":HammingDistance, "Kendall":SwapDistance, "Cayley":CayleyDistance, "RUN":NumberOfSortedBlocks, "LAS":NegativeLengthOfLongestAscendingSubsequence}


path_to_tests = "C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP/TSP_instances/"
tests_TSP = ["ulysses22.txt", "att48.txt", "berlin52.txt", "st70.txt", "bier127.txt"]

def RunTest(problem_type, Algorithm_name , num_runs = 2, maxTime = 60):
    
    Algorithm = Algorithms[Algorithm_name]
    findIdentity = True
    res_fitness_evals = {}
    res_time = {}
    prob_size = 10

    distance_names = ["Hamming", "Kendall", "Cayley", "RUN", "LAS"]
    # distance_names = ["Cayley", "RUN", "LAS"]


    for dist_name in distance_names:
        res_fitness_evals[dist_name] = [None]*num_runs
        res_time[dist_name] = [None]*num_runs
        

    
    for dist_name in distance_names:
        DistanceMeasure = distances[dist_name]

        ProblemInstance = Sorting.Sorting(prob_size)

        if Algorithm_name == "EHBSA_wt" or Algorithm_name == "UMDA":
            pop_size = math.ceil(math.sqrt(ProblemInstance.dim))
        elif Algorithm_name == "GeneralizedMallowsModel":
            pop_size = 10 * ProblemInstance.dim

        # print("Test",problem_type, Algorithm_name, instance)

        for test_num in range(num_runs):
            print(dist_name,"test",test_num)

            try:
                (val1, val2) = Algorithm.Run(problem_type,ProblemInstance, pop_size, maxTime = maxTime, NumberOfTemplateCuts=4, findIdentity = findIdentity, DistanceMeasure = DistanceMeasure)
                
                res_fitness_evals[dist_name][test_num] = val1
                res_time[dist_name][test_num] = val2

                # print(val1,val2)
            except RuntimeError:
                print("runtime error",problem_type, Algorithm_name)
            except OverflowError as e:
                print("overflow error",problem_type, Algorithm_name,str(e))
            except Exception as e:
                print("Other error",sys.exc_info()[0],problem_type, Algorithm_name,str(e))

            ProblemInstance.ResetFitnessCount()

    path = "C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP/Testing/"
    path += "DMs/"
    path += Algorithm_name+"_"
    path += str(maxTime)+"s_"
    path += time.strftime("%Y%m%d-%H%M%S")


        
    df_res_fitness_evals = pd.DataFrame(data=res_fitness_evals)
    df_res_time = pd.DataFrame(data=res_time)

    df_res_fitness_evals.to_excel(path+"_fitnessEvaluations.xlsx")
    df_res_time.to_excel(path+"_timeUsed.xlsx")
    print("Exported to Excel")

    print("Finished",Algorithm_name,problem_type, Algorithm_name)

# RunTest("Sorting", "GeneralizedMallowsModel", num_runs = 2, maxTime = 30)