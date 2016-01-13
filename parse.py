import pandas as pd
import json
from pprint import pprint 

hasChild = 'http://purl.org/gem/qualifiers/hasChild'
description = 'http://purl.org/dc/terms/description'
listID = 'http://purl.org/ASN/schema/core/listID'
statementNotation = 'http://purl.org/ASN/schema/core/statementNotation'
educationLevel = 'http://purl.org/dc/terms/educationLevel'
subject = 'http://purl.org/dc/terms/subject'

#make a standard 
class standards:
    ID = ''
    children = []
    description = ''
    subject = ''
    educationLevel = []
    uri = ''
    hasChildren = False
    def __init__(self, ID, description, children, subject, educationLevel, uri):
        self.ID = ID
        self.description = description
        self.children = children
        self.subject = subject
        self.educationLevel = educationLevel
        self.uri = uri


def printNode(l, data, node, level):
    currentNodeDescription = str(data[node][description][0]["value"])

    if (data[node].get(listID)):
        currentNodeID = data[node][listID][0]["value"]
    elif (data[node].get(statementNotation)): 
        currentNodeID = data[node][statementNotation][0]["value"]
    else:
        currentNodeID = ''

    #get the current node's children if they exist, returns None if they don't
    children = data[node].get(hasChild)

    #get the subject and education level
    currentNodeSubject = data[node][subject][0]["value"]
    currentNodeEducation = data[node][educationLevel]
    #create the node object
    currentNode = standards(currentNodeID, currentNodeDescription, [], currentNodeSubject, currentNodeEducation, node)
    l.append(currentNode)
    #print("{}ID: {}, Description: {}".format("    "*level, currentNode.ID, currentNode.description[:30]))
    #if the children exists, then loop through them and get their children
    if (children != None):
        currentNode.hasChildren = True
        for item in children:
            node = item["value"]
            currentNode.children.append(node)
            level += 1
            printNode(l, data, node, level)

# def writeJson(data, sortedList, dictionary):
#     #copy the data
#     dataCopy = data
#
#     #for each first level, start the recursion
#     for item in sortedList:
#         if (len(item.ID) == 2):
#             #empty out the child array in the copy
#             dataCopy[item.uri][hasChild] = []
#             #for each child in the first level
#             for child in item.children:
#                 writeRecursive(dataCopy, sortedList, dictionary, child, dataCopy[item.uri][hasChild])
#
#     #prune all the ones that don't have children
#     for key in dataCopy.keys():
#         if ((dictionary[key].hasChildren) == False):
#             dataCopy.pop(key, None)
#     pprint(json.dumps(dataCopy))
#
# def writeRecursive(dataCopy, sortedList, dictionary, uri, childArray):
#     #see if the next layer has children, if it does, recursive another level, if it doesn't, just append to the child array
#
#     if(dictionary[uri].hasChildren):
#         for child in dictionary[uri].children:
#                 writeRecursive(dataCopy, sortedList, dictionary, child, dataCopy[uri][hasChild])
#
#     childArray.append(dataCopy[uri])
#
    
def writeJsonFromList(data, root): 
    jsonData = {}
    sortedList = []
    printNode(sortedList, data, root, 0)
    dictionary = {}
    for item in sortedList:
        dictionary[item.uri] = item
        
    for item in sortedList: 
        if (len(item.ID) == 2):
            parent = writeRecursive(item, sortedList, dictionary)
            jsonData[item.uri] = parent
    f = open("t1-revised.json", "w")
    f.write(json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': ')))
    f.close()
                
             
def writeRecursive(item, sortedList, dictionary):
    itemDictionary = {}
    itemDictionary["ID"] = item.ID
    itemDictionary["description"] = item.description
    itemDictionary["subject"] = item.subject
    itemDictionary["educationLevel"] = item.educationLevel
    itemDictionary["uri"] = item.uri
    itemDictionary["children"] = []
    for child in item.children:
        itemDictionary["children"].append(writeRecursive(dictionary[child], sortedList, dictionary))
        
    return itemDictionary
#t1-s1
t1s1 = pd.read_csv("data/t1-s1.csv")
uniqueSubjectNotations = pd.unique(t1s1.subjectNotation.ravel())
uniqueSubjectNotations.sort()
#print(uniqueSubjectNotations)
#print(len(uniqueSubjectNotations))

#t1.json
with open("data/t1.json") as t1_file:
    t1 = json.load(t1_file)
t1root = "http://asn.jesandco.org/resources/D10003B9"


writeJsonFromList(t1, t1root)

