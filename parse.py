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
    currentNodeDescription = str(data[node][description][0]["value"].encode('ascii','ignore'))
    #pprint(currentNodeDescription)
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

#dataLocation is a str to where the file is
#root is the root of the tree
#outputName is what the exit json file should be
def writeJsonFromList(dataLocation, root, outputName): 
    with open(dataLocation) as data_file:
        data = json.load(data_file)
    jsonData = {}
    sortedList = []
    printNode(sortedList, data, root, 0)
    
    dictionary = {}
    for item in sortedList:
        dictionary[item.uri] = item
        
    for childUri in dictionary[root].children: 
        child = dictionary[childUri]
        parent = writeRecursive(child, sortedList, dictionary)
        jsonData[childUri] = parent

    with open("revised-data/{}".format(outputName), "w") as f:
        f.write(json.dumps(jsonData, sort_keys=True, indent=4, separators=(',', ': ')))
                
             
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
t1root = "http://asn.jesandco.org/resources/S113BA1C"
writeJsonFromList("data/t1.json", t1root, "t1.json")

#t2.json
t2root = "http://asn.jesandco.org/resources/D100029D"
writeJsonFromList("data/t2.json", t2root, "t2.json")

#t3.json
t3root = "http://asn.jesandco.org/resources/D1000124"
writeJsonFromList("data/t3.json", t3root, "t3.json")

#t4.json
t4root = "http://asn.jesandco.org/resources/D1000379"
writeJsonFromList("data/t4.json", t4root, "t4.json")

#s1.json
s1root = "http://asn.jesandco.org/resources/D10003FB"
writeJsonFromList("data/s1.json", s1root, "s1.json")

#s2.json 
s2root = "http://asn.jesandco.org/resources/D10003FC"
writeJsonFromList("data/s2.json", s2root, "s2.json")