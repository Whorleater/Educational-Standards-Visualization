import pandas as pd
import json
from pprint import pprint 

hasChild = 'http://purl.org/gem/qualifiers/hasChild'
description = 'http://purl.org/dc/terms/description'

def printNode(data, node, level):
    #print the current node's description
    print("")
    print("{}{}".format("    "*level, data[node][description][0]["value"]))
    #get the current node's children if they exist, returns None if they don't
    children = data[node].get(hasChild)
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

