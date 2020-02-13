import numpy as np
import pandas as pd
from collections import defaultdict

# makes a list of values for same keys in diff dictionaries
def combine_dict(list_of_dictionaries):
    dic = defaultdict(lambda: list())
    for d in list_of_dictionaries:  
        for item in d.items():
            dic[item[0]].append(item[1])
    return dic

# Scale Data features on range or SD
def scale(df,col,on_range = True):
    if on_range: # Scaling based on Range
        df[col] -= df[col].min()
        df[col] /= df[col].max()
    else: # Scaling based on SD
        sd = df[col].std()
        df[col] -= df[col].mean()
        df[col] /= sd
    return

Stud_Data = pd.read_excel('./Course_Advisory_Data.xlsx')

# Extract Col, Semester, RollNo of Students
columns = Stud_Data.columns.to_list()
semesters = list(Stud_Data.Semester.unique())
roll_nos = list(Stud_Data['Sr. No'].unique())

# Dictionary for Course Code and Course Title and Credit Hours
course_guide = combine_dict([dict(zip(Stud_Data['Course Code'], Stud_Data['Course Title'])),dict(zip(Stud_Data['Course Code'], Stud_Data['Credit Hours']))])
# Dictionary for Grade and Grade Point
grade_dictionary = dict(zip(Stud_Data['Grade'], Stud_Data['Grade Point']))

# Set Index To Student's Roll No's
Stud_Data.set_index('Sr. No',inplace= True)
# Drop 'Course Title','Grade','Credit Hours' as not used in KNN
Stud_Data = Stud_Data.drop(labels = ['Course Title','Grade','Credit Hours'],axis = 1)

# Scale Numerical Cols on Range
# scale(data, 'CGPA')
# scale(data, 'SGPA')
# scale(data, 'Grade Point')

# Redifine Data Structure
modified_data = pd.DataFrame(columns=['Roll_No'],data=roll_nos)
modified_data.set_index(['Roll_No'],inplace=True)

for c in ['Course','Grade_Point','Semester','Warning','SGPA','CGPA']:
    modified_data[c] = np.empty((len(roll_nos), 0)).tolist()

roll_nos.sort()
for roll in roll_nos:
    for semester in semesters:
        try:
            # Convert Each Group To a Separate DataFrame
            df = pd.DataFrame(Stud_Data.loc[roll])
            df = df.groupby(['Semester']).get_group(semester)

            # Transfer Data to a new Dataframe
            modified_data.ix[roll].Semester.append([semester])
            modified_data.ix[roll].Course.append(list(df['Course Code'].to_list()))
            modified_data.ix[roll].Grade_Point.append(list(df['Grade Point'].to_list()))
            modified_data.ix[roll].Warning.append(list([df['Warning'].to_list()[0]]))
            modified_data.ix[roll].SGPA.append(list([df['SGPA'].to_list()[0]]))
            modified_data.ix[roll].CGPA.append(list([df['CGPA'].to_list()[0]]))
        except KeyError:
            pass

# Write Data to an excel file
modified_data.to_pickle('New_Data1.sav')

# data = pd.read_pickle('./New_Data_pickle.xlsx')
