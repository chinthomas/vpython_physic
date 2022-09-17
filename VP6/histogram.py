import sys
sys.path
sys.executable
sys.path.insert(0, "C:\\Users\\Chin\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages")
import numpy as np
import vpython as vp

class ghistogram:
    """ 
    def __init__(self, graph, bins, color=vp.color.red):\n\n

    def plot(self, data):\n
    
    it counts the number of occurrence of the values in data, averages the number of

    occurrence over times this method has been called and plots the latest results.
    """

    def __init__(self, graph, bins, color=vp.color.red):
        self.bins = bins
        self.slotnumber = len(bins)
        self.slotwidth = bins[1] - bins[0]
        self.n = 0
        self.slots = np.zeros(len(bins))
        self.bars = vp.gvbars(graph=graph, delta=self.slotwidth, color=color)



    def plot(self, data):
        currentslots = np.zeros(self.slotnumber)
        for value in data:
            
            currentslots[min(max(int((value - self.bins[0])/self.slotwidth), 0), self.slotnumber - 1)] += 1
        self.slots = (self.slots * self.n + currentslots)/(self.n + 1) 
        self.n += 1 
        if self.n == 1: 
            for (currentbin, barlength) in zip(self.bins, self.slots): 
                self.bars.plot( pos = (currentbin, barlength)) 
        else: 
            self.bars.data = list(zip(self.bins, self.slots)) 

if __name__ == '__main__': 
    """ You first import vpython and create a graph (here it is vdist). 
    
    Then you can create an ghistogram object (here it is observation), in which it must 
    
    specified in which graph it should display (graph = vdist), 
    
    the bins (here it is 1-1.5, 1.5-2, 2-2.5, 2.5-3), and the color of the histogram. 
    
    If you do not specify what color the histogram should be, it defaults to red. 
    
    Then in the method observation.plot, you give the data (can be list or array), 
    
    it then counts the number of occurrence of the values in data, 
    
    averages the number of occurrence over times this method has been called and plots the latest 
    
    results. If a value in data is smaller than the lower bound, it is counted as in the lowest bin, 
    
    similarly, if a value is larger than the upper bound, it is counted as in the highest bin. 
    
    For example, the 3 rows of data will yield the histogram in the figure. 
    """
    vdist = vp.graph(width = 450)   
    observation = ghistogram(graph = vdist, bins = np.arange(1, 3, 0.5)) 
    observation.plot(data=[1.2, 2.3, 4])
    observation.plot(data=[1, 1.7, 2.6]) 
    observation.plot (data=[-0.5, 2, 2.3])  