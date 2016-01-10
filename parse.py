import pandas as pd

#t1-s1
df = pd.read_csv("data/t1-s1.csv")
uniqueSubjectNotations = pd.unique(df.subjectNotation.ravel())
uniqueSubjectNotations.sort()
print(uniqueSubjectNotations)
print(len(uniqueSubjectNotations))