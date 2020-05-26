from multiprocessing import Process
from Test_Distance_Measures import RunTest


# RunTest("Sorting", "GeneralizedMallowsModel", num_runs = 2, maxTime = 30)
if __name__ == '__main__':
    proc = []
    for algorithmName in ["EHBSA_wt", "GeneralizedMallowsModel", "UMDA"]:
        p = Process(target=RunTest, args = ("Sorting", algorithmName, 3, 120, ))
        p.start()
        proc.append(p)
    
    for p in proc:
        p.join()


