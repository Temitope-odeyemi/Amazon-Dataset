#!/usr/bin/env python
# coding: utf-8

# In[192]:


import pandas as pd
import numpy as np


# In[193]:


df = pd.read_csv('Amazon_dataset.csv')


# In[194]:


df.head(3)


# In[195]:


df.shape


# In[196]:


df.columns


# In[197]:


df.info()


# #### Dropping columns that are  not needed

# In[198]:


df.drop(columns=['link', 'complete_link', 'ISBN_13'], axis=1, inplace =True)


# #### Checking for duplicates

# In[199]:


df[df.duplicated()] #checking for duplicates


# Since there are no duplicates, we can move on

# #### Checking for null values

# In[200]:


df.isnull().sum()


# #### Filling nan cells

# In[201]:


# Filling the empty cells in the author column 
df['author'].fillna('Not Provided', inplace=True)
df['publisher'].fillna('Not Provided', inplace=True)
df['language'].fillna('Not_Stated', inplace=True)


# In[202]:


df['price'].fillna('0', inplace=True)
df['dimensions'].fillna('0', inplace=True)
df['avg_reviews'].fillna('0', inplace=True)
df['n_reviews'].fillna('0', inplace=True)
df['star5'].fillna('0', inplace=True)
df['star4'].fillna('0', inplace=True)
df['star3'].fillna('0', inplace=True)
df['star2'].fillna('0', inplace=True)
df['star1'].fillna('0', inplace=True)
df['price (including used books)'].fillna('0', inplace=True)
df['pages'].fillna('0', inplace=True)
df['weight'].fillna('0', inplace=True)


# In[203]:


df['weight'].unique()


# #### Cleaning Weight column

# In[204]:


def weight_converter(item):
    if item.split()[-1] == "pounds":
        return float(item.split()[0]) * 0.45359237
    elif item.split()[-1] == "ounces":
        return float(item.split()[0]) * 0.02834952


# In[205]:


df['weight'] = df['weight'].apply(weight_converter)


# #### Cleaning Star1, Star2, Star3, Star4, Star5 Columns

# In[206]:


def remove_percent(x):
    x = x.replace('%', '')
    return x


# In[207]:


df['star1'] = df['star1'].apply(remove_percent)
df['star2'] = df['star2'].apply(remove_percent)
df['star3'] = df['star3'].apply(remove_percent)
df['star4'] = df['star4'].apply(remove_percent)
df['star5'] = df['star5'].apply(remove_percent)


# #### Cleaning Author Column

# In[208]:


def clean_author(x):
    if x == x:
        return x.lstrip('[ ').rstrip(']').replace(',  and ,', ' and')
    else:
        return x


# In[209]:


df['author'] = df['author'].apply(clean_author)


# #### Cleaning Language Column

# In[210]:


df['language'].unique()


# In[211]:


def clean_language(row):
    lang = row.language
    if lang == 'Unqualified, Japanese (Dolby Digital 2.0 Mono), English (Dolby Digital 5.1), English (Dolby Digital 2.0 Mono)' :
        row.language = 'English, Japanese'
    elif lang == 'English (Dolby Digital 2.0 Mono)' :
        row.language = 'English'
    elif lang == 'English (DTS-HD Master Audio 5.1), French (DTS-HD 2.0)' :
        row.language = 'English, French'
    return row


# In[212]:


df = df.apply(clean_language, axis=1)


# In[213]:


contains_english = df.language.str.contains('English')
contains_spanish = df.language.str.contains('Spanish')
contains_japanese = df.language.str.contains('Japanese')
contains_french = df.language.str.contains('French')
contains_Not_Stated = df.language.str.contains('Not_Stated')


# In[214]:


not_language_info = ~(contains_english | contains_spanish | contains_japanese | contains_french | contains_Not_Stated )


# In[215]:


df.loc[not_language_info, ['language']] = np.nan


# In[216]:


df['language'].unique()


# #### Cleaning Dimension Column

# In[217]:


def dimension_conv(item):
    if item.split()[:-1].__len__() == 5:
        x = float(item.split()[:-1][0]) * 2.54 #cm
        y = float(item.split()[:-1][2]) * 2.54  #cm

        z = float(item.split()[:-1][4]) * 2.54  #cm
        return round(x*y*z, 1)
    else:
        return None


# In[218]:


df['dimensions'] = df['dimensions'].apply(dimension_conv)


# #### Change data type

# In[219]:


df['star1'] = df['star1'].astype("int")
df['star2'] = df['star2'].astype("int")
df['star3'] = df['star3'].astype("int")
df['star4'] = df['star4'].astype("int")
df['star5'] = df['star5'].astype("int")


# #### Descibe dataset

# In[220]:


df.describe()


# #### Save cleaned file

# In[221]:


df.to_csv("Amazon_data_science_books_cleaned_file.csv", index=False)

