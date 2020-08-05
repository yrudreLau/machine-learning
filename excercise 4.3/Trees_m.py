# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 23:29:44 2020

@author: 交通流小组
"""

import numpy as np
import operator

def InformationEntropy(dataSet):
    Sample_Num = len(dataSet) ##count number of samples
    
    ## create a dict to record sample class and sample number of each class
    Sample_Class = {} 
    for datum in dataSet:
        Sample_Lablel = datum[-1]
        if Sample_Lablel not in Sample_Class.keys():
            Sample_Class[Sample_Lablel] = 1
        else:
            Sample_Class[Sample_Lablel] += 1
    
    ## calculate information entropy
    Ent_D = 0
    for key in Sample_Class:
        p_k = Sample_Class[key] / Sample_Num
        Ent_D -= p_k*np.log2(p_k)
        
    return Sample_Class, Ent_D

## split dataset by attribute return subset of input attribute value
def splitDataSet(dataSet, attri_index, attri_value):
    retDataSet = []
    featVec = []
    for featVec in dataSet:
        if featVec[attri_index] == attri_value:
#             print(featVec)
            reducedFeatVec = featVec[:attri_index]
#             print(reducedFeatVec)
            reducedFeatVec += featVec[attri_index + 1:]
#             print(b)
            retDataSet.append(reducedFeatVec)
    return retDataSet

## calculate optimal information Gain and choose optimal subset split mode
def optimal_attributeIndex(dataSet):
    ## get the attribute
    attribute_Num = len(dataSet[0]) - 1
    datasetInfEnt_D = InformationEntropy(dataSet)[-1]
    
    ## initialization
    optimal_InfGain_Da = 0
    optimal_attribute = -1
    
    ## calculate each attribute's information gain
    for i in range(attribute_Num):
        data_attribute = [data_attri[i] for data_attri in dataSet]
        data_values = set(data_attribute)
        attributeEntropy = 0
        for value in data_values:
            subDataSet = splitDataSet(dataSet, i, value)
            p_k = len(subDataSet) / float(len(dataSet))
            attributeEntropy += p_k * InformationEntropy(subDataSet)[-1]
        InfGain_Da = datasetInfEnt_D - attributeEntropy
#         print(InfGain_Da)
        if (InfGain_Da > optimal_InfGain_Da): ## choose optimal attribute
            optimal_InfGain_Da = InfGain_Da
            optimal_attribute = i
            
    return optimal_attribute

## return the major sample class by sorting
def majorSampleClass(ClassList):
    ClassCount = {}
    for datum in ClassList:
#         print(datum)
        if datum not in ClassCount.keys():
            ClassCount[datum] = 1
        else:
            ClassCount[datum] += 1
    sortedClassCount = sorted(ClassCount.items(), key = operator.itemgetter(1), reverse = True)
    
    return sortedClassCount[0][0]

## define decision tree recursive function
def DecisionTreeRecursive(dataSet, attributes):
    ClassList = [datum[-1] for datum in dataSet]
    if ClassList.count(ClassList[0]) == len(ClassList): ## if there is only one class, return, else return major class
        return ClassList[0]
    if len(dataSet[0]) == 1:
        return majorSampleClass(ClassList)
    optimal_attri = optimal_attributeIndex(dataSet) ## get index of optimal attribute 
    optimal_attriLabel = attributes[optimal_attri]
    Deci_Tree = {optimal_attriLabel:{}}
    del (attributes[optimal_attri]) ## delete attribute already chosen
    attributeValues = [datum[optimal_attri] for datum in dataSet]
    for value in attributeValues:
        subLabels = attributes[:]
        Deci_Tree[optimal_attriLabel][value] = DecisionTreeRecursive(
            splitDataSet(dataSet, optimal_attri, value), subLabels)
        
    return Deci_Tree
