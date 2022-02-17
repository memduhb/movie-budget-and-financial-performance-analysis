import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
from sklearn.linear_model import LinearRegression

# ------PREPARATION OF DATA-------

# Reading the data
data = pd.read_csv('cost_revenue_dirty.csv')

# Getting rid of unwanted characters in the dataframe
chars_to_remove = ["$", ","]
columns_to_convert = ["USD_Production_Budget",
                      "USD_Worldwide_Gross",
                      "USD_Domestic_Gross"]

for col in columns_to_convert:
    for char in chars_to_remove:
        data[col] = data[col].astype(str).str.replace(char, "")
    data[col] = pd.to_numeric(data[col])

# Converting the Release_Date column to Pandas Datetime type
data.Release_Date = pd.to_datetime(data.Release_Date)

# Finding international releases
international_releases = data.loc[(data.USD_Domestic_Gross == 0) &
                                  (data.USD_Worldwide_Gross != 0)]

# Filtering unreleased films as of the date data was pulled
scrape_date = pd.Timestamp('2018-5-1')
unreleased_films = data.loc[(data.Release_Date > scrape_date)]
data_clean = data.drop(unreleased_films.index)  # Clean data = data_clean

# Creating a decade column where years are converted to their corresponding decades
data_clean['Decade'] = data_clean.Release_Date.dt.year - (data_clean.Release_Date.dt.year % 10)

# -----CHARTS for data_clean------

# Revenue vs Budget bubble chart for the data_clean
"""
plt.figure(figsize=(8, 4), dpi=200)

ax = sns.scatterplot(data=data_clean,
                     x='USD_Production_Budget',
                     y='USD_Worldwide_Gross',
                     hue='USD_Worldwide_Gross',
                     size='USD_Worldwide_Gross')

ax.set(ylim=(0, 3000000000),
       xlim=(0, 450000000),
       ylabel='Revenue in $ billions',
       xlabel='Budget in $100 millions')

plt.show()
"""

# Budget and Revenue vs Year bubble chart for the data_clean
"""
plt.figure(figsize=(8, 4), dpi=200)

with sns.axes_style('darkgrid'):
    ax = sns.scatterplot(data=data_clean,
                         x='Release_Date',
                         y='USD_Production_Budget',
                         hue='USD_Worldwide_Gross',
                         size='USD_Worldwide_Gross')

    ax.set(ylabel='Budget in $100 millions',
           xlabel='Year')

plt.show()
"""

# Separating the old and new films (1980 is taken as the border)
old_films = data_clean.loc[data_clean.Decade < 1980]
new_films = data_clean.loc[data_clean.Decade >= 1980]

# ----- NEW FILMS REVENUE vs BUDGET CHART (linear regression included) -----
"""
plt.figure(figsize=(8,4), dpi=200)


with sns.axes_style('darkgrid'):
    ax = sns.regplot(data=new_films,
                    x='USD_Production_Budget',
                    y='USD_Worldwide_Gross',
                    scatter_kws = {'alpha': 0.4},
                    line_kws = {'color': 'black'})
    ax.set(ylim=(0, 3000000000),
         xlim=(0, 450000000),
        ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions')

plt.show()
"""

# ----- OLD FILMS REVENUE vs BUDGET CHART (linear regression included) -----
"""
plt.figure(figsize=(8, 4), dpi=200)

with sns.axes_style('darkgrid'):
    ax = sns.regplot(data=old_films,
                     x='USD_Production_Budget',
                     y='USD_Worldwide_Gross',
                     scatter_kws={'alpha': 0.4},
                     line_kws={'color': 'black'})

    ax.set(xlim=(0, 45000000),
           ylabel='Revenue in $ billions',
           xlabel='Budget in $100 millions')

plt.show()
"""

# ---- RUNNING OUR OWN LINEAR REGRESSION FOR NEW FILMS -----
"""
regression = LinearRegression()
X = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])
regression.fit(X, y)

print(regression.score(X, y))# Our model explains about the percentage of the output of this value
# (~57% in this case)

print(regression.intercept_)
print(regression.coef_)
# intercept and coefficient values are used to estimate revenue for a given budget.
# Revenue = Intercept + coefficient * budget
"""