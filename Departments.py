# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 09:58:20 2020

@author: Sibghat
"""
import numpy as np
import pandas as pd
from collections import defaultdict
def EE_roll_nos(Stud_Data):
    EE_Crs=['Engineering Workshop','Engineering Drawing','Engineering Workshop',
            'Electrical Network Analysis','Signals and Systems','Electro Mechanical Systems',
            'Multivariable Calculus','µP Interfacing and Programming','Electromagnetic Theory',
            'Feedback Control Systems','Engineering Economics','Applied Calculus',
            'Physics for Engineers','Linear Circuit Analysis','Electronic Devices and Circuits',
            'Probability and Random']
    EE_Depart=pd.DataFrame(columns = Stud_Data.columns.to_list())
    for crs in EE_Crs:
        EE_Depart=EE_Depart.append(Stud_Data[Stud_Data['Course Title'] == crs],ignore_index=True)
    roll_nos = list(EE_Depart['Sr. No'].unique())
    return roll_nos
def Business_roll_nos(Stud_Data):
    Business_Crs=['IT in Business','Fundamentals of Accounting','Business Math - I',
                  'Business Math - II','Financial Accounting','Business Statistics',
                  'Management Accounting','Statistical Inference','Statistical Inference',
                  'Business Communication - I','Organizational Behavior','Business Finance',
                  'Consumer Behavior','Micro Economics','Financial Management',
                  'Operations Management','Human Resource Management','Macro Economics',
                  'Management Info. Systems','Business Law','Methods in Business Research',
                  'Financial Institutions and Markets','Business Communication - II',
                  'Strategic Management','Business Ethics']
    Business_Depart=pd.DataFrame(columns = Stud_Data.columns.to_list())
    for crs in Business_Crs:
        Business_Depart=Business_Depart.append(Stud_Data[Stud_Data['Course Title'] == crs],ignore_index=True)
    roll_nos = list(Business_Depart['Sr. No'].unique())
    return roll_nos
def CS_roll_nos(Stud_Data):
    CS_Crs=['Applied Physics','Basic Electronics','Calculus - I','Calculus - II',
            'Data Structures','Discrete Structures','Comp. Organization and Assembly Lang.',
            'Database Systems','Operating Systems','Design and Analysis of Algorithms',
            'Theory of Automata','Computer Networks','Object Oriented Analysis and Design',
            'Probability and Statistics','Software Engineering','Artificial Intelligence',
            'Human Computer Interaction','Computer Architecture','Professional Issues in IT']
    CS_Depart=pd.DataFrame(columns = Stud_Data.columns.to_list())
    for crs in CS_Crs:
        CS_Depart=CS_Depart.append(Stud_Data[Stud_Data['Course Title'] == crs],ignore_index=True)
    roll_nos = list(CS_Depart['Sr. No'].unique())
    return roll_nos
Stud_Data = pd.read_excel('./Course_Advisory_Data.xlsx')
rn= EE_roll_nos(Stud_Data)