# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 08:55:13 2019

@author: Shubham
"""

import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

file = 'data\world_bank_projects.json'
df = pd.read_json(file, 'r')

#to analyze all columns in the main dataframe
analyse_df = df.loc[:1]
trans_df = analyse_df.transpose()

project_num = defaultdict(int)
for country in df.countryname:
    project_num[country] += 1
    
pnum = pd.DataFrame.from_dict(project_num, orient='index', columns=['# Projects'])
sort_pnum = pnum.sort_values('# Projects', ascending=False)
                             
# Ten Countries with the top number of projects
top_10_projects = sort_pnum[:10]
sns.set()
ax = sns.barplot(data=top_10_projects, x=top_10_projects.index, y='# Projects')
plt.figure(1)
plt.xticks(rotation = 60)
plt.ylim(0,20)

plt.tight_layout()
plt.show()

print(type(df.mjtheme_namecode[0]))         # <class 'list'>
print(type(df.mjtheme_namecode[0][0]))      # <class 'dict'>

#Major project themes 
code_dict = {}
total_code_count = defaultdict(int)
name_dict = {}
total_name_count = defaultdict(int)

code_name_relation = {'1':'Economic management', '2':'Public sector governance','3':'Rule of law','4':'Financial and private sector development','5':'Trade and integration','6':'Social protection and risk management','7':'Social dev/gender/inclusion','8':'Human development','9':'Urban development','10':'Rural development','11':'Environment and natural resources management'}

for country1 in sort_pnum.index:
    country_df = df[df['countryname'] == country1]   #filtering data by country
    #codelist = []
    code_count = defaultdict(int)
    #namelist = []
    name_count = defaultdict(int)
    for list_themes in country_df['mjtheme_namecode']:    #iterating over the lists of dicts
        for dict_theme in list_themes:     #iterating over the dictionaries
            code = dict_theme['code']
            code_count[code] += 1
            name = dict_theme['name']
            #codelist.append(code)
            #namelist.append(name)
            if name == '':
                name = code_name_relation[code]         # code to fill missing project themes
            name_count[name] += 1
    
    code_dict[country1] = code_count         #assigning list of project codes to countries
    name_dict[country1] = name_count         #assigning list of project names to countries
    
for key in code_dict:
    for ccount in code_dict[key].keys():
        total_code_count[ccount] += code_dict[key][ccount]
        
for key in name_dict:
    for ncount in name_dict[key].keys():
        total_name_count[ncount] += name_dict[key][ncount]

labels = total_name_count.keys()
sizes = total_name_count.values()
explode = (0.1,0,0,0,0,.1,.1,0,0,0,0)

plt.figure(2)
plt.pie(sizes, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%')
plt.axis('equal')
plt.tight_layout()
plt.show()
"""
plt.figure(3)
total_df = pd.DataFrame()
for i, country in enumerate(top_10_projects.index):
    if total_df.empty:
        total_df = pd.DataFrame.from_dict(code_dict[country], orient='index')
        total_df['country%d' %i] = country
        #total_df.sort_index()
    else:
        top_df = pd.DataFrame.from_dict(code_dict[country],orient='index')
        top_df['country%d' %i] = country
        #top_df.sort_index()
        total_df.merge(top_df)
    
"""  


for key in code_name_relation.keys():
    print(total_code_count[key] == total_name_count[code_name_relation[key]])
