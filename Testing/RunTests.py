from multiprocessing import Process
from Test_algorithm import RunTest



if __name__ == '__main__':
    proc = []
    num_runs = 5
    maxTime = 5*60
    for pop_size_multiplier in ["sqrt",1,10]:
        for problemType in ["TSP","Sorting"]:
            for algorithmName in ["Perms_1x1EA", "EHBSA", "EHBSA_wt", "MallowsModel", "GeneralizedMallowsModel", "UMDA"]:

                p = Process(target=RunTest, args = (problemType, algorithmName, pop_size_multiplier, num_runs, maxTime, ))
                p.start()
                proc.append(p)
    
    for p in proc:
        p.join()


