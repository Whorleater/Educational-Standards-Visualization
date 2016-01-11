import pandas as pd
import json
from pprint import pprint 

hasChild = 'http://purl.org/gem/qualifiers/hasChild'
description = 'http://purl.org/dc/terms/description'
listID = 'http://purl.org/ASN/schema/core/listID'
statementNotation = 'http://purl.org/ASN/schema/core/statementNotation'
educationLevel = 'http://purl.org/dc/terms/educationLevel'
subject = 'http://purl.org/dc/terms/subject'

class standards:
    ID = ''
    children = []
    description = ''
    subject = ''
    educationLevel = []
    depth = -1
    def __init__(self, ID, description, children, subject, educationLevel, depth):
        self.ID = ID
        self.description = description
        self.children = children
        self.subject = subject
        self.educationLevel = educationLevel
        self.depth = depth
    

def printNode(data, node, level):
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
    currentNode = standards(currentNodeID, currentNodeDescription, children, subject, currentNodeEducation, level)
    #print the current node's description
    print("")
    print("{}ID: {}, Description: {}".format("    "*level, currentNode.ID, currentNode.description[:30]))
    #if the children exists, then loop through them and get their children
    if (children != None):
        for item in children:
            node = item["value"]
            level += 1
            printNode(data, node, level)
            

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
printNode(t1, t1root, 0)
#t1[t1root][hasChild][0]["value"]

