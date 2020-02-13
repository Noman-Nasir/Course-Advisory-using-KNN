# DM-Assignment-1

Data Structure of Course_Advisiory.xlsx was changed such that each row contains the data of a single student.

General idea for applying KNN is to apply weight to [subjects similarity * Respective Grade],[SGPA],[CGPA],[Warning]

Proposed weights :
        
        [subjects similarity * Respective Grade] => 0.7
        [SGPA]                                   => 0.1
        [CGPA]                                   => 0.1
        [Warning]                                => 0.1
        
Find Score against Each student for each semester and keep the best score against each student 
along with the semester no. for that score.
Select k students with top scores and Find the subjects they took in next semester. 
Cross Examine each subject with their credit hours and recommend courses with Cr.hrs <= 19.


# Another Approach

Take each semester as x and the next semester as y


Taken Courses(X1)	      Courses Taken in a semester DIP, CNET, Automata 	
Grades(X2)	            Grades in That Semester   A, B, C	
CGPA(X3)                CGPA till that semester         2.5	 
SGPA(X4)                SGPA in a semester         3.5	   
Warning(X5)             Warning Count in a semester     1	     
Recommended Courses(Y)  Courses Taken in  next semester  DM, Num. Meth, SE


Match with best x with given weights to find suitable y
