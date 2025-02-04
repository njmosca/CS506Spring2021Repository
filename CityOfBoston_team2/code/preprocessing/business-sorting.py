"""
date updated: 04/07/2021
"""


import pandas as pd
import os
import ast

# paths to data, choices
data_path = '../../dataset_ignore/businesses_sanitized.csv'
output_path = '../../datasets_clean/businesses_sanitized.csv'

see_types = 0

# pulling data from excel file
if os.path.exists(data_path):
    print('acquiring data...')
    untyped = pd.read_csv(data_path,
                          usecols = ['name','zip','lat','lon','types'])  
    
    # types back to list
    untyped['types'] = untyped['types'].apply(ast.literal_eval)

# rejects if path has been changed
else:
    raise FileNotFoundError('invalid path to businesses.xlsx')

# looking at types
if see_types == 1:
    print('analyzing types...')
    
    # list of all types
    all_types = [item for sublist in untyped.types.tolist() for item in sublist]
    all_types = list(set(all_types))    
    
    print('the number of unique types is:', len(all_types))


# function to sort types
def sorter(types):
    '''
    takes: types, a list of strings
    returns: a string with category based on types
        (commercial, education, food access, healthcare, recreation, social)
    '''
    
    # keywords for each category (note commerical is all other)
    education = ['school', 'universit']
    food = ['restaurant', 'food', 'grocery', 'supermarket']
    health = ['clinic', 'hospi', 'doctor']
    recreation = ['park', 'gym', 'stadium', 'field']
    social = ['pubs', 'bars', 'club', 'dunkin','coffee','brew','caeffeine','wine','spirits']
    
    # note: order is very important
    categories = {'education': education,
                  'recreation': recreation,
                  'social': social,
                  'food': food,
                  'health': health,
                  }
    
    # what tags in what categories
    tags = []
    for item in types:
        for keywords in categories:
            if any(key in item for key in categories[keywords]):
                tags.append(keywords)
                break
    
    # from list of tags, decide dominant
    final = 'commercial'
    for option in categories:
        if option in tags:
            final = option
            break
    
    return final


# new df with categories
print('determining category...')
with_cat = untyped.copy(deep = True)
with_cat['category'] = untyped['types'].apply(sorter)

# outputting
print('outputting...')
with_cat = with_cat.drop(columns = ['types'])
with_cat.to_csv(output_path)
print('done.')
























