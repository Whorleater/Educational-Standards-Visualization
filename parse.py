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
    currentNode = standards(currentNodeID, currentNodeDescription, children, currentNodeSubject, currentNodeEducation, node)
    l.append(currentNode)
    #print("{}ID: {}, Description: {}".format("    "*level, currentNode.ID, currentNode.description[:30]))
    #if the children exists, then loop through them and get their children
    if (children != None):
        for item in children:
            node = item["value"]
            level += 1
            currentNode.hasChildren = True
            printNode(l, data, node, level)

def writeJson(data, sortedList):
    for item in sortedList:
        if (len(item.ID) == 2):
            jsonObject = data[item.uri]
            jsonObject[hasChild] = []
            #pprint(json.dumps(jsonObject))
            for child in item.children:
                writeRecursive(data, sortedList, child, jsonObject[hasChild])
            
    pprint(json.dumps(jsonObject))
    
def writeRecursive(data, sortedList, item, childArray):
    jsonObject = data[item["value"]]
    jsonObject[hasChild] = []
    children = data[item["value"]].get(hasChild)
    if (children != None):
        for child in children:
            writeRecursive(data, sortedList, item, jsonObject[hasChild])
    childArray.append(json.dumps(jsonObject))
    
#t1-s1
t1s1 = pd.read_csv("data/t1-s1.csv")
uniqueSubjectNotations = pd.unique(t1s1.subjectNotation.ravel())
uniqueSubjectNotations.sort()
#print(uniqueSubjectNotations)
#print(len(uniqueSubjectNotations))

#t1.json
with open("data/t1.json") as t1_file:
    t1 = json.load(t1_file)
    
#pprint(t1["http://asn.jesandco.org/resources/D10003B9"]['http://purl.org/gem/qualifiers/hasChild'][0]["value"])
#print("\n\n")
#pprint(t1[t1["http://asn.jesandco.org/resources/D10003B9"]['http://purl.org/gem/qualifiers/hasChild'][0]["value"]]) 

t1root = "http://asn.jesandco.org/resources/D10003B9"

l = []
printNode(l, t1, t1root, 0)

# for item in l:
#     print("{} {}".format(item.ID, item.children))

writeJson(t1, l)

#t1[t1root][hasChild][0]["value"]

