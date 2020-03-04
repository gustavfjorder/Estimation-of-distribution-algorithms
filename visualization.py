import matplotlib.pyplot as plt
import TSP

def visualize(TSPInstance, solution, solutionLength):

    fig = plt.plot()
    x = [TSPInstance.nodesDict[city][0] for city in solution]
    y = [TSPInstance.nodesDict[city][1] for city in solution]

    plt.plot(x,y,'k.')

    # connect points
    def connectpoints(x,y,p1,p2):
        x1, x2 = x[p1], x[p2]
        y1, y2 = y[p1], y[p2]
        plt.plot([x1,x2],[y1,y2],'k-')


    for cityIndex in range(len(solution)-1):
        connectpoints(x,y,cityIndex,cityIndex+1)
    connectpoints(x,y,TSPInstance.dim-1,0)

    plt.title("Solution of length "+str(solutionLength))
    plt.show()