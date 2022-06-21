# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 08:25:46 2022

@author: Massoud Sharifi
"""
import pandas as pd

years = range(1880, 2022)
file_pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = r'C:\Users\Massoud\Documents\GitHub\usbabynames1880-2021\datasets\names\yob%d.txt' % year
    df = pd.read_csv(path, names=columns)
    df['year'] = year
    file_pieces.append(df)
# Concatenate everything into a single DataFrame
names = pd.concat(file_pieces, ignore_index=True)
# Write the concatenated DataFrame to a new text file
names.to_csv(r'C:\Users\Massoud\Documents\GitHub\usbabynames1880-2021\datasets\names\yob1880-2021.txt', 
             sep = ',', index=False, header=False)

