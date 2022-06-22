# USbabynames1880-2021
The United States Social Security Administration (SSA) has made available data on
the frequency of baby names from 1880 through the present (2021).
What to anlyze?
There are many things you might want to do with the dataset:
• Visualize the proportion of babies given a particular name over time
• Determine the relative rank of a name
• Determine the most popular names in each year or the names whose popularity
  has advanced or declined the most
• Track the changing trends in letters of the names(Initial, Central, Final letters)
  (First letter changing trends are analyzed in this project)


**How the analysis is fulfilled?
Steps required to load, wrangle and transform data for analysis are as follows:
1- load babayname files into Pandas data frame
the US Social Security Administration makes available data files,
one per year, containing the total number of births for each sex/name combination.
The raw archive of these files can be obtained from http://www.ssa.gov/oact/baby
names/limits.html.
for each year from 1880 to 2021, there exists a text file named yob####.txt where #### is the 
four-digit year (1880-2021). The text file is simliar to CSV files in format (field separated by commas)
you can open the file in a text editor on Windows or Linux to the contents. For example a sample of file yob2021 is as follows:

Olivia,F,17728
Emma,F,15433
Charlotte,F,13285
Amelia,F,12952
Ava,F,12759
Sophia,F,12496
Isabella,F,11201
Mia,F,11096
Evelyn,F,9434

A script named "dataloadscript.py" in the scripts folder exists that you can run to create a 
dataframe (names) by loading  the files saved at
 "C:\Users\Massoud\Documents\GitHub\usbabynames1880-2021\datasets\names\"
 you can save the files on different folders on your computer and change the related path in the python code.
 - Then, we write the concatenated DataFrame to a new text file (yob1880-2021.txt) so that we can load it to another DataFrame
 in the next script.

 2- Aggragating the data
 - run script "aggregatescript.py
For some privacy and legal reasons, The DataFrame only contains names with at least five occurrences in each year, so for simplicity’s
sake we can use the sum of the births column by sex as the total number of births in that year.

-------------------------
 *** Note that it is possible to integrate all scripts into a single script to have a One-button script.
 I've also written this script for you "usbaby1880-2021_analyzer.py" which is the integration of two scripts:
 "dataloadscript.py" and "aggregatescript.py"
 ------------------------

we start aggregating the data at the year and sex level using groupby or pivot_table:

>>>total_births = names.pivot_table('births', index='year',
.....: columns='sex', aggfunc=sum)
Then plot the total_births:
total_births.plot(title='Total births by sex and year')

- add a column proportion with the fraction of babies given each name in each sex relative to
  the total number of births per year.
  
>>>def add_proportion(df):
...df['proportion'] = df.births / df.births.sum()
...return df

names = names.groupby(['year', 'sex']).apply(add_proportion)

              name sex  births  year  proportion
0             Anna   F    2604  1880    0.031026
1             Emma   F    2003  1880    0.023865
2        Elizabeth   F    1939  1880    0.023103
3           Minnie   F    1746  1880    0.020803
4         Margaret   F    1578  1880    0.018802
           ...  ..     ...   ...         ...
2052775     Zyeire   M       5  2021    0.000003
2052776       Zyel   M       5  2021    0.000003
2052777      Zyian   M       5  2021    0.000003
2052778      Zylar   M       5  2021    0.000003
2052779        Zyn   M       5  2021    0.000003

[2052780 rows x 5 columns]

proportion is a number between 0 and 1. For example, in row 0, the proportion 0.03 means that 3 out of 100 names 
in year 1880 was "Anna" or in the last row, the proportion 0.000003 means that 3 out of 1,000,000 names in the year 2021 was "Zyn".

---------------------
Next, to facilitate further analysis, a subset of top 1000 names is extracted from data for each year/sex combination.
A function named "extract_top1000(group)" is defined and applied to the data grouped by year/sex.
-----------------------
From now on we use this TOP 1000 dataset to explore and analyze data.

** Analyzing naming trends **
now we can do some analysis on naming trends.
First, we can simply split the names to males and females:
>>> males = top1000[top1000['sex'] == 'M']
>>> females = top1000[top1000['sex'] == 'F']

# we can also build a pivot table that calculates the total births per name in each year
total_births_by_name_per_year = top1000.pivot_table('births', index='year', columns = 'name', aggfunc=sum)
 
>>> total_births_by_name_per_year.info()
<class 'pandas.core.frame.DataFrame'>
Int64Index: 142 entries, 1880 to 2021
Columns: 7276 entries, Aaden to Zyon
dtypes: float64(7276)
memory usage: 7.9 MB
 
Then, we can choose a desired subset of names and plot the related trends.
You can modify the the list of names to see the different results.

>>> total_births_subset = total_births_by_name_per_year[['Jack', 'Oliver', 'Elizabeth', 'Monica']]
>>> total_births_subset.plot(subplots=True, figsize=(15, 10), grid=False,
            title="Number of births per year")
			
By looking at the trends we can see some names have been in favor in some periods and out of favor in other periods.
but other factors such as name diversity cause decrease in choosing some names by parents.

To analyze the diversity of names from 1880 to 2021 we can extract unique names from the whole names data to get a hint and also 
plot the proportion trends of names per year and sex.
It's also possible to calculate cumulative sum of a percentage from top1000 and observe the number of distinct names constructing this percentage.
These analyses are shown below:

>>> unames = names.groupby(['year']).names['name'].unique()
>>> len(unames[1880])
Out[]: 1889
>>>len(unames[1960])
Out[]: 10751
>>>len(unames[2021])
Out[]: 28801

Proportion of births per year and sex is plotted to see the trends in name diversification.
prop_table = top1000.pivot_table('proportion', index=['year'], columns=['sex'], aggfunc=sum)
prop_table.plot(title='Sum of Top 1000 proportion by year and sex',
                yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2030, 10), figsize=(20,10))
				
By looking at the decreasing trends for both females and males, we can deduce that diversity of names 
has increased from past to present.

Now let’s consider just the female names from 1921 and 2021:
>>> df_female_names2021 = females[females.year == 1921]
>>>>df_female_names1921 = females[females.year == 2021]
>>> proportion_cumsum_1921 = df_female_names1921.sort_values(by='proportion', ascending=False).proportion.cumsum()
>>> proportion_cumsum_1921.values.searchsorted(0.5) + 1 #adding one to make up for index 0
Out[]: 50
>>> proportion_cumsum_2021 = df_female_names2021.sort_values(by='proportion', ascending=False).proportion.cumsum()
>>> proportion_cumsum_2021.values.searchsorted(0.5) + 1 #adding one to make up for index 0
Out[]: 276

#Taking the cumulative sum, cumsum, of propoprtion and then calling the method
#returns the position (50 for 1921, and 276 for 2021 above) in the cumulative sum at searchsorted which would 
# need to be inserted to keep it in sorted order.

Now we can extend this idea to calculate the cumulative sum for all the years and sexes from 1880 to 2021.
To fulfil this task, we write a function (cumsum_clac): 
def cumsum_calc(group, q=0.5):
    prop_cumsum = group.sort_values(by='proportion', ascending=False).proportion.cumsum()
    return prop_cumsum.searchsorted(q)

Apply this function to the top1000 grouped previously by year/sex combination (grouped_names DataFrame)

>>> proportion_cumsum_per_year_and_sex = grouped_names.apply(cumsum_calc)
# diversiy has two time series, one for each sex,indexed by year.
>>> diversity = proportion_cumsum_per_year_and_sex.unstack('sex')
>>> diversity.plot(title="Number of popular names in top half")
The plot shows increasing diversity for both men and women through time. the slope 
is steeper for females, especially from 1992 to 2010 (18 years): popular names for girls in top 50 percent has soared more than double.
>>> diversity.loc[1992:2010]
Out[224]: 
sex     F    M
year          
1992  101   50
1993  106   53
1994  111   56
1995  114   59
1996  121   63
1997  128   66
1998  137   69
1999  145   72
2000  154   76
2001  164   80
2002  169   82
2003  178   86
2004  190   91
2005  198   95
2006  209   98
2007  222  102
2008  233  108

 ** Track the changing trends in the first letters of the names
 
>>>first_letters = names.name.map(lambda x: x[0])
>>>first_letters.name = 'first letter'

Initially, all of the births in the full dataset are aggregated by year, sex, and first letter:
>>>first_letter_pivot_table = names.pivot_table('births', index=first_letters, columns=['sex', 'year'], aggfunc=sum)
we choose a sample of 3 years from the start, middle and end of the time interval (1921, 1971, 2021).

>>>first_letter_subtable = first_letter_pivot_table.reindex(columns=[1921, 1971, 2021], level='year')
>>>letter_proportion = first_letter_subtable / first_letter_subtable.sum()
Then plot the bar chart to see the first letter changing trends for all letters of the English alphabet (a-z)
for the 3 years mentiond.

>>>fig, axes = plt.subplots(2, 1, figsize=(15, 12))
>>>letter_proportion['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
>>>letter_proportion['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',
legend=False)

Next, we calculate the first letter proportion for the full dataset
and this time plot, for instance, changing trends of 3 letters in the whole time interval (1880-2021)
As we see from the plots, the letter "W" for males and "M" for females has significantly dropped in use.
Letter "D" has a rising-falling pattern form males and the letter "E" falling-rising for females.
and the letter "A" has a steady-falling-rising pattern for both males and females and started falling from around 2016

>>>letter_proportion2 = first_letter_pivot_table / first_letter_pivot_table.sum() #in whole data
>>>fig, axes = plt.subplots(2, 1, figsize=(15, 12))
>>>density_ts_male = letter_proportion2.loc[['A', 'D', 'W'], 'M'].T #transposing to make each column a time series
>>>density_ts_female = letter_proportion2.loc[['A', 'E', 'M'], 'F'].T
>>>density_ts_male.plot(ax=axes[0], title='Male')
>>>density_ts_female.plot(ax=axes[1], title='Female',
legend=True)
(To be continued)