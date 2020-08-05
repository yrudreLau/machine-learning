# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 23:30:45 2020

@author: 交通流小组
"""

import matplotlib.pyplot as plt
from pylab import *

DeciNode = dict(boxstyle = 'square, pad = 0.5', fc = '0.9')
LeafNode = dict(boxstyle = 'round4, pad = 0.5', fc = '0.9')
arrow_args = dict(arrowstyle = '<|-', connectionstyle="arc3", shrinkA=0,
                  shrinkB=16)
mpl.rcParams['font.sans-serif'] = ['SimHei']

def plotNode(Nodename, cenCoor, priorCoor, nodeType):  
    '''
    centerCoor: Node center coordinates
    priorPt: Starting point coordinates
    '''
    createFig.ax1.annotate(Nodename, xy = priorCoor, 
                            xycoords = 'axes fraction', xytext = cenCoor, 
                            textcoords = 'axes fraction', va = 'center', 
                            ha = 'center', bbox = nodeType, arrowprops = arrow_args)## plot charaters
    
def getLeafNum(Deci_Tree):
    '''
    Deci_Tree: dict, get by function DecisionTreeRecursive
    return number of leaf nodes
    '''
    
    ## initialization
    Leaf_Num = 0
    ## get the decision node
    RootNode = list(Deci_Tree.keys())[0] ## get root node
    BranchNodedict = Deci_Tree[RootNode] ## get the values of root node
    for key in BranchNodedict.keys():
        if type(BranchNodedict[key]).__name__ == 'dict': ## Determine whether the value is still a dictionary
            Leaf_Num += getLeafNum(BranchNodedict[key])
        else:
            Leaf_Num += 1
    
    return Leaf_Num

def getFloorNum(Deci_Tree):
    
    ## initialization
    maxFloor = 0    
#    currentFloor = 0
    RootNode = list(Deci_Tree.keys())[0] ## get root node
    BranchNodedict = Deci_Tree[RootNode] ## get the values of root node
    for key in BranchNodedict.keys():
        if type(BranchNodedict[key]).__name__ == 'dict': ## Determine whether the value is still a dictionary
            currentFloor = 1 + getFloorNum(BranchNodedict[key])
        else:
            currentFloor = 1
        if currentFloor > maxFloor:
            maxFloor = currentFloor
            
    return maxFloor



## define plot text function
def plotText(cenCoor, priorCoor, txtString):
    txtCoor_x = (priorCoor[0] + cenCoor[0]) / 2.0 # (priorCoor[0] - cenCoor[0]) / 2.0 + cenCoor[0] #
    txtCoor_y = (priorCoor[1] + cenCoor[1]) / 2.0 # (priorCoor[1] - cenCoor[1]) / 2.0 + cenCoor[1] #
    createFig.ax1.text(txtCoor_x, txtCoor_y, txtString)
    
def plotTree(Deci_Tree, priorCoor, nodeName):
    LeafNum = getLeafNum(Deci_Tree)
    Floor = getFloorNum(Deci_Tree)
    RootNode = list(Deci_Tree.keys())[0]
    cenCoor = (plotTree.xoff + (1.0 + float(LeafNum)) / 2.0 / plotTree.totalw,
              plotTree.yoff)
#    print(plotTree.yoff)
    plotText(cenCoor, priorCoor, nodeName)
    plotNode(RootNode, cenCoor, priorCoor, DeciNode)
    BranchNodeDict = Deci_Tree[RootNode]
    plotTree.yoff = plotTree.yoff - 1.0 / plotTree.totalh
#    print('1min = ',plotTree.yoff)
    for key in BranchNodeDict.keys():
        if type(BranchNodeDict[key]).__name__ == 'dict':
            plotTree(BranchNodeDict[key], cenCoor, str(key))
        else:
            plotTree.xoff = plotTree.xoff + 1.0 / plotTree.totalw
            plotNode(BranchNodeDict[key], (plotTree.xoff, plotTree.yoff), 
                     cenCoor, LeafNode)
            plotText((plotTree.xoff, plotTree.yoff), cenCoor, str(key))
    plotTree.yoff = plotTree.yoff + 1.0 / plotTree.totalh
#    print('2 min = ', plotTree.yoff)
    
def createFig(DecisionTree):
    fig = plt.figure(1, facecolor = 'white')
    fig.clf() ## clear figure plot area
    axprops = dict(xticks = [], yticks = [])
    createFig.ax1 = plt.subplot(111, frameon = False, **axprops)
    plotTree.totalw = float(getLeafNum(DecisionTree))
#    print('w=', plotTree.totalw)
    plotTree.totalh = float(getFloorNum(DecisionTree))
#    print('h=', plotTree.totalh)
    plotTree.xoff = -0.5 / plotTree.totalw
    plotTree.yoff = 1.0
    plotTree(DecisionTree, (0.5, 1.0), '')
#   plt.savefig('DecisionTree.jpg')
    plt.show()
