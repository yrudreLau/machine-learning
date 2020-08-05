# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 23:06:47 2020

@author: 交通流小组
"""

import Trees_m
import Tree_mplotter
import numpy as np
import pandas as pd



#% matplotlib inline

data = pd.read_csv('watermelon3_0.csv')

D = np.array(data)

X = D[:, :-3]
y = D[:, -1].reshape([17,1])

dataSet = np.hstack((X, y)).tolist()



attributes = data.columns[:-3].tolist()
DecisionTree = Trees_m.DecisionTreeRecursive(dataSet, attributes)

## set the shape and style of decision nodes, leaf nodes and arrows



    
Tree_mplotter.createFig(DecisionTree)