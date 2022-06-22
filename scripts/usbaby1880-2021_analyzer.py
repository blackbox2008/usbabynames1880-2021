# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:30:27 2022

@author: Massoud Sharifi
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 08:25:46 2022

@author: Massoud Sharifi
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

total_births = names.pivot_table('births', index='year',
                                 columns='sex', aggfunc=sum)
total_births.plot(title='Total births by sex and year')

#add a column proportion with the fraction of babies given each name in each sex relative to
# the total number of births per year.

def add_proportion(df):
    df['proportion'] = df.births / df.births.sum()
    return df

names = names.groupby(['year', 'sex']).apply(add_proportion)

# a subset of top 1000 names is extracted from data for each year/sex combination
def extract_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]

grouped_names = names.groupby(['year', 'sex'])
top1000 = grouped_names.apply(extract_top1000)
# Drop the group index, not needed
top1000.reset_index(inplace=True, drop=True)
# Split top1000 names to males aand females
males = top1000[top1000['sex'] == 'M']
females = top1000[top1000['sex'] == 'F']

# Total births pivot table by year and name
total_births_by_name_per_year = top1000.pivot_table('births', index='year', columns = 'name', aggfunc=sum)

total_births_subset = total_births_by_name_per_year[['Jack', 'Oliver', 'Elizabeth', 'Monica']]

total_births_subset.plot(subplots=True, figsize=(15, 10), grid=False,
            title="Number of births per year")
prop_table = top1000.pivot_table('proportion', index=['year'], columns=['sex'], aggfunc=sum)
prop_table.plot(title='Sum of Top 1000 proportion by year and sex',
                yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2030, 10), figsize=(20,10))


#Taking the cumulative sum, cumsum, of propoprtion and then calling the method
#returns the position in the cumulative sum at searchsorted which would 
# need to be inserted to keep it in sorted order: 0.5
df_female_names2021 = females[females.year == 2021]
proportion_cumsum_2021 = df_female_names2021.sort_values(by='proportion', ascending=False).proportion.cumsum()
proportion_cumsum_2021.values.searchsorted(0.5) + 1 #adding one to make up for index 0

df_female_names1921 = females[females.year == 1921]
proportion_cumsum_1921 = df_female_names1921.sort_values(by='proportion', ascending=False).proportion.cumsum()
proportion_cumsum_1921.values.searchsorted(0.5) + 1


def cumsum_calc(group, q=0.5):
    prop_cumsum = group.sort_values(by='proportion', ascending=False).proportion.cumsum()
    return prop_cumsum.searchsorted(q)

proportion_cumsum_per_year_and_sex = grouped_names.apply(cumsum_calc)

# Two time series, one for each sex,indexed by year.
diversity = proportion_cumsum_per_year_and_sex.unstack('sex')

diversity.plot(title="Number of popular names in top half")

# First Letter changing through time
first_letters = names.name.map(lambda x: x[0])
first_letters.name = 'first letter'
first_letter_pivot_table = names.pivot_table('births', index=first_letters, columns=['sex', 'year'], aggfunc=sum)
first_letter_subtable = first_letter_pivot_table.reindex(columns=[1921, 1971, 2021], level='year')
letter_proportion = first_letter_subtable / first_letter_subtable.sum()
fig, axes = plt.subplots(2, 1, figsize=(15, 12))
letter_proportion['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_proportion['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',
legend=False)

letter_proportion2 = first_letter_pivot_table / first_letter_pivot_table.sum() #in whole data
fig, axes = plt.subplots(2, 1, figsize=(15, 12))
density_ts_male = letter_proportion2.loc[['A', 'D', 'W'], 'M'].T #transposing to make each column a time series
density_ts_female = letter_proportion2.loc[['A', 'E', 'M'], 'F'].T
density_ts_male.plot(ax=axes[0], title='Male')
density_ts_female.plot(ax=axes[1], title='Female',
legend=True)