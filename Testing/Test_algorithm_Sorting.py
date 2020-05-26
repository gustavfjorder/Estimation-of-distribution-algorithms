import sys
sys.path.append('C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP')
sys.path.append('C:/Users/gustavfjorder/OneDrive - QVARTZ/Documents/02_DTU/08 Estimation of distribution/EDAs_for_TSP/ProblemTypes')

import Sorting, TSP
from Algorithms import Perms_1x1EA, EHBSA, EHBSA_wt, MallowsModel, GeneralizedMallowsModel, UMDA

import visualization
import time
import numpy as np
import pandas as pd

# Start timer
# startTime = time.time()
problem_type = "Sorting"

Algorithms = {"Perms_1x1EA":Perms_1x1EA, "EHBSA":EHBSA, "EHBSA_wt":EHBSA_wt, "MallowsModel":MallowsModel, "GeneralizedMallowsModel":GeneralizedMallowsModel, "UMDA":UMDA}

# Algorithm_name = "Perms_1x1EA"
# Algorithm_name = "EHBSA"
# Algorithm_name = "EHBSA_wt"
# Algorithm_name = "MallowsModel"
# Algorithm_name = "GeneralizedMallowsModel"
# Algorithm_name = "UMDA"
# Algorithm = Algorithms[Algorithm_name]

maxTime = 10*60
tests = [5,10,15,20,25]
num_runs = 5

if len(sys.argv)>1:
    Algorithm_name = sys.argv[1]
    Algorithm = Algorithms[Algorithm_name]



result_fitness = {5:[],10:[],15:[],20:[],25:[]}
result_time = {5:[],10:[],15:[],20:[],25:[]}

for instance_size in tests:
    print("Test",instance_size)
    pop_size = 10*instance_size
    SortingInstance = Sorting.Sorting(instance_size)
    for test_num in range(1,num_runs+1):
        try:
            fitness_evals, time_used = Algorithm.Run("Sorting",SortingInstance, pop_size, maxTime = maxTime, NumberOfTemplateCuts=4, findIdentity = True)
            result_fitness[instance_size].append(fitness_evals)
            result_time[instance_size].append(time_used)
            print(fitness_evals)
        except RuntimeError:
            print("runtime error")
        except OverflowError:
            print("overflow error")
        except Exception as e:
            print("Other error",sys.exc_info()[0])
        

        SortingInstance.ResetFitnessCount()
df_fitness = pd.DataFrame(data=result_fitness)
df_time = pd.DataFrame(data=result_time)
df_fitness.to_excel(Algorithm_name+"_"+problem_type+"_"+time.strftime("%Y%m%d-%H%M%S")+"_fitness.xlsx")
df_time.to_excel(Algorithm_name+"_"+problem_type+"_"+time.strftime("%Y%m%d-%H%M%S")+"_time.xlsx")


df_individual.to_excel(problem_type+"/Popsize_"+str(pop_size_multiplier)+"N/"+Algorithm_name+"_"+problem_type+"_"+str(maxTime)+"s_"+str(pop_size_multiplier)+"N_"+time.strftime("%Y%m%d-%H%M%S")+"_individuals.xlsx")
df_fitness.to_excel(problem_type+"/Popsize_"+str(pop_size_multiplier)+"N/"+Algorithm_name+"_"+problem_type+"_"+str(maxTime)+"s_"+str(pop_size_multiplier)+"N_"+time.strftime("%Y%m%d-%H%M%S")+"_fitness.xlsx")




