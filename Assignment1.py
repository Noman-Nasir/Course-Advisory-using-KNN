import numpy as np
import pandas as pd
from collections import defaultdict

class KNN:
	def __init__(self, k=1):
		self.K = k

	def train(self, x, y):
		self.X = x
		self.Y = y

	def predict(self, x_pred):

		scores = []
		for x in self.X:
			# ['Taken_Courses', 'Grades', 'CGPA', 'SGPA', 'Warning', 'Recommended']
			if len(set(x[0])&set(x_pred[0])) != 0:
				score = 0
				uncommon = len(set(x[0])) + len(set(x_pred[0])) - len(set(x[0])&set(x_pred[0]))*2
				common = list(set(x[0])&set(x_pred[0]))
				
				for c in common:
					id1 = x_pred[0].index(c)
					id2 = x[0].index(c)
					score += (x_pred[1][id1] - x[1][id2])**2
				score **=0.5
				score += ((x_pred[2][0] - x[2][0])**2)
				score += ((x_pred[3][0] - x[3][0])**2)
				score += ((x_pred[4][0] - x[4][0])**2)
				score += uncommon
				scores.append(score)
			else:
				scores.append(999)
			
		scores = np.array(scores)	
		min_vals = np.argpartition(scores,self.K)[:self.K]
		l = [j for sub in list(self.Y[:, 0][min_vals]) for j in sub]
		d = dict((x, l.count(x)) for x in set(l))
		d = {k: v for k, v in sorted(d.items(),reverse= True, key=lambda item: item[1])}
		return d
	def evaluate(self):
		pass

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


def adviseMe(classifier, semesterData, course_guide):
    courses = classifier.predict(semesterData)
    creditLimit = 19
    if semesterData[4][0] != 0: # Check Warning Count
        creditLimit = 15
    assignedLimit = 0
    coursesList = list(courses.keys())
    suggestedCourses = []
    otherSuggestions = []
    for c in coursesList:
        if assignedLimit + course_guide.get(c) <= creditLimit:
            suggestedCourses.append(c)
            assignedLimit += course_guide.get(c)
        elif assignedLimit >= creditLimit:
            otherSuggestions.append(c)
    return suggestedCourses,assignedLimit,otherSuggestions


if __name__ == "__main__":

    Stud_Data = pd.read_excel('./Course_Advisory_Data.xlsx')
    Stud_Data.dropna(inplace= True)
    # Extract Col, Semester, RollNo of Students

    # Dictionary for Course Code and Course Title and Credit Hours
    course_guide = dict(zip(Stud_Data['Course Title'], Stud_Data['Credit Hours']))
    # Dictionary for Grade and Grade Point
    grade_dictionary = dict(zip(Stud_Data['Grade Point'], Stud_Data['Grade']))


    # Set Index To Student's Roll No's
    Stud_Data.set_index('Sr. No',inplace= True)

    delete_courses = ['Advanced Research Methods','Research in Marketing','MS Thesis - I',
            'MS Thesis - II','PhD Thesis - I','PhD Thesis - II','PhD Thesis - III',
            'PhD Thesis - IV','Applied Programming','Research Methodology']

    delete_semesters =   [20111,20121,20123,20131]


    for line in delete_courses:
        indexNames = Stud_Data[ Stud_Data['Course Title'] == line ].index
        Stud_Data.drop(indexNames,inplace=True)
    for ds in delete_semesters:
        indexNames = Stud_Data[ Stud_Data['Semester'] == ds ].index
        Stud_Data.drop(indexNames,inplace=True)
    grades = [ 'I', 'W', 'FA', 'L1', 'LL', 'L2', 'F/R', 'CN']
    assignedVal = -1
    for g in grades:
        Stud_Data.loc[Stud_Data['Grade'] == g, 'Grade Point'] = assignedVal
        assignedVal -= 1

    columns = Stud_Data.columns.to_list()
    semesters = list(Stud_Data.Semester.unique())
    roll_nos = list(Stud_Data.index.unique())





    # Scale Numerical Cols on Range
    # scale(data, 'CGPA')
    # scale(data, 'SGPA')
    # scale(data, 'Grade Point')

    semesters = ['Fall 2016','Spring 2017','Summer 2017',
    'Fall 2017','Spring 2018','Summer 2018','Fall 2018',
    'Spring 2019','Summer 2019','Fall 2019']

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
                modified_data.loc[roll].Semester.append([semester])
                modified_data.loc[roll].Course.append(list(df['Course Title'].to_list()))
                modified_data.loc[roll].Grade_Point.append(list(df['Grade Point'].to_list()))
                modified_data.loc[roll].Warning.append(list([df['Warning'].to_list()[0]]))
                modified_data.loc[roll].SGPA.append(list([df['SGPA'].to_list()[0]]))
                modified_data.loc[roll].CGPA.append(list([df['CGPA'].to_list()[0]]))
            except KeyError:
                pass

    # Write Data to an excel Stud_Datae
    modified_data.to_pickle('intermediateData.sav')

    data = pd.read_pickle('intermediateData.sav')
    cols = data.columns.to_list()
    students = data.index.to_list()

    xyData = pd.DataFrame(columns=['Taken_Courses','Grades','CGPA','SGPA','Warning','Recommended'])

    for student in students:
        student_data = data.loc[student]
        for i in range(len(data.loc[student].Semester)-1):
            # print(student_data['Course Title'])
            xyData = xyData.append({'Taken_Courses':student_data['Course'][i],
            'Grades':student_data.Grade_Point[i],
            'CGPA': student_data.CGPA[i],
            'SGPA':student_data.SGPA[i],
            'Warning':student_data.Warning[i],
            'Recommended':student_data['Course'][i+1]} ,
            ignore_index=True)
            if len(student_data['Course'][i]) != len(student_data.Grade_Point[i]):
                print(len(student_data['Course'][i]),len(student_data.Grade_Point[i]))

    xyData.to_pickle('xydata.xlsx')




    ratio = 0.8
    size = int(len(xyData) * ratio)
    x_train = xyData.values[:size,:5]
    y_train = xyData.values[:size,5:]

    # print(x_train.shape,y_train.shape)

    x_test = xyData.values[size:,:5]
    y_test = xyData.values[size:,5:]

    # print(x_test.shape,y_test.shape)


    k = 7
    r = 1000
    classifier = KNN(k)
    classifier.train(x_train,y_train)

    cour, lim, other = adviseMe(classifier,x_test[r], course_guide)

    for idx,y in enumerate(x_test[r][0]):
        print(y,grade_dictionary.get(x_test[r][1][idx]))

    print('\nWarning Count : ',x_test[r][4][0])
    print('\n\n')

    print(*cour, '\nCredit Hours : '+str(lim), sep= '\n')

    print('\n\n\n*********Other Possible Suggestions****************\n' ,*other, sep= '\n')
