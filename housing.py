
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[5]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 

# In[6]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[13]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
     '''
    
    df = pd.read_table('university_towns.txt', header=None)
    df = pd.DataFrame(df)
    collegetown=[]
    df['State']=np.nan
    for line in df[0]:
        if line[-6:] == '[edit]':
            state = line[:-6]
        else:
            city = line
            collegetown.append([state, city])
         
        df = pd.DataFrame(collegetown,columns = ['State','RegionName'])
        df['RegionName'] = df['RegionName'].str.replace(r'\s\(.*', '')
        df.columns = ["State", "RegionName"]
    
    return df

get_list_of_university_towns()


# In[14]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows=220, header=None)
    gdp = gdp.iloc[:, [4, 6]]
    gdp.columns = ['Quarterly', 'GDP in billions of chained 2009 dollars']
    q = []
    for i in range(len(gdp)-2):
        if (gdp.iloc[i][1] > gdp.iloc[i+1][1]) & (gdp.iloc[i+1][1] > gdp.iloc[i+2][1]):
            q.append(gdp.iloc[i+1][0])
            
    return q[0]

get_recession_start()


# In[15]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    gdp = pd.read_excel('gdplev.xls', skiprows=254, header=None)
    gdp = gdp.iloc[:, [4, 6]]
    gdp.columns = ['Quarterly', 'GDP in billions of chained 2009 dollars']
    q_end = []
    for i in range(len(gdp)-2):
        if (gdp.iloc[i+2][1] > gdp.iloc[i+1][1])  & (gdp.iloc[i+1][1] > gdp.iloc[i][1]):
            q_end.append(gdp.iloc[i+2][0])
    
       
    return q_end[0]

get_recession_end()


# In[16]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows=220, header=None)
    gdp = gdp.iloc[:, [4, 6]]
    gdp.columns = ['Quarterly', 'GDP in billions of chained 2009 dollars']
    gdp = gdp.set_index('Quarterly')
    start = get_recession_start()
    end = get_recession_end()
    
    btm = gdp.loc[start:end, :].idxmin().values[0]
    
    return btm

get_recession_bottom()


# In[17]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    housing['State'] = housing['State'].map(states)
    housing= housing.set_index(['State','RegionName'])
    housing= housing.loc[:, '2000-01':]
        
    def quarters(col):
        if col.endswith(("01", "02", "03")):
            s = col[:4] + "q1"
        elif col.endswith(("04", "05", "06")):
            s = col[:4] + "q2"
        elif col.endswith(("07", "08", "09")):
            s = col[:4] + "q3"
        else:
            s = col[:4] + "q4"
        return s  

    housing = housing.groupby(quarters, axis = 1).mean()
    housing = housing.sort_index()

        
    return housing


convert_housing_data_to_quarters()


# In[18]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    '''
    
    housing = convert_housing_data_to_quarters()
    start = get_recession_start()
    end = get_recession_end()
    btm = get_recession_bottom()
    before = '2008q2'
    
    
    housing = housing[[before, end]]
    
    housing['Ratio'] = housing[before]/ housing[end]
    
    housing = housing.reset_index().dropna()
    
    university_town = get_list_of_university_towns()

#     for i in housing['RegionName']:
#         for j in ut:
#             if i in j:
#                 ut.append(i)
#             else:
#                 not_university_town.append(i)
                
    
    
    
    ut = pd.merge(housing, university_town, how='inner', left_on=['State', 'RegionName'], right_on = ['State', 'RegionName'])
    
    nut = housing[~housing.index.isin(ut.index)]

    #Run T Test
    
    ttest = ttest_ind(ut['Ratio'], nut['Ratio'])
    
    Reject_H0 = None
    Better = None

    
    if ttest[1] < 0.01:
        Reject_H0 = True
    else:
        Reject_H0 = False
        
    if ttest[0] < 0:
        Better = 'university town'
    else:
        Better = 'non-university town'

    
    
    return (Reject_H0, ttest[1], Better)

run_ttest()


# In[ ]:




