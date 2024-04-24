+++
categories = ['Statistical Analysis', 'Python']
date = '2022-05-23T19:30:32'
description = 'Comparing 5 years of methane emissions to determine if Climate Trace forecasts greater emissions than UN FAOSTAT.'
tags = ['data', 'university-of-malaysia', 'climate-change', 'emissions']
title = 'Rice Paddy Methane Emissions Estimation: Part 2'
featured_image = 'post-image.*'
author = "Justin Napolitano"
images = ['featured-rice-paddies.jpeg']
series = ['Rice Paddy Methane Emissions']
image = 'post-image.*'
+++

# Methane Emissions Estimation Data Part 2: A Comparison between FAOSTAT and University of Malaysia Estimates


This post documents the data exploration phase of a project that determines whether global methane emissions produced by rice paddies are undercounted. 

It is fairly code python and pandas heavy. 

The code and data exploration follows the summary below.  


## Hypothesis Testing the University of Malaysia Paper

## Claims

* That the distributions do not differ between 2020 and 2019
* That the means do no differ between 2020 and 2019

## What will be Tested.  

* Shapiro-Wilk Test
* Mann-Whitney U Test
* Kruskal Wallis
* Friedman



## Analysis


```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

```


```python
filepath = "/Users/jnapolitano/Projects/wattime-takehome/wattime-takehome/data/ch4_2015-2021.xlsx"

hypothesis_testing_df = pd.read_excel(filepath)
```

### Drop total row from the data


```python
hypothesis_testing_df = hypothesis_testing_df.loc[(hypothesis_testing_df['country_name'] != "Total")].copy() #copying to avoid modifying slices in memory.  Old df should also drop from memory in production environment.
```


```python
hypothesis_testing_df
```




<div style="overflow-x:auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>iso3_country</th>
      <th>country_name</th>
      <th>tCH4_2015</th>
      <th>tCH4_2016</th>
      <th>tCH4_2017</th>
      <th>tCH4_2018</th>
      <th>tCH4_2019</th>
      <th>tCH4_2020</th>
      <th>tCH4_2021</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>2.344420e+06</td>
      <td>2.278158e+06</td>
      <td>2.098958e+06</td>
      <td>2.141231e+06</td>
      <td>2.070985e+06</td>
      <td>2.106781e+06</td>
      <td>1.983974e+06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>3.410233e+05</td>
      <td>3.104189e+05</td>
      <td>3.725173e+05</td>
      <td>3.717030e+05</td>
      <td>3.294713e+05</td>
      <td>4.902874e+05</td>
      <td>4.544874e+05</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>6.133647e+06</td>
      <td>5.859531e+06</td>
      <td>6.355071e+06</td>
      <td>5.413962e+06</td>
      <td>5.603352e+06</td>
      <td>6.402353e+06</td>
      <td>6.068210e+06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>1.141464e+04</td>
      <td>1.334803e+04</td>
      <td>1.217299e+04</td>
      <td>1.405410e+04</td>
      <td>1.148324e+04</td>
      <td>1.305461e+04</td>
      <td>8.531579e+03</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>1.283649e+06</td>
      <td>1.023129e+06</td>
      <td>9.615327e+05</td>
      <td>1.176982e+06</td>
      <td>1.266668e+06</td>
      <td>1.188195e+06</td>
      <td>1.009936e+06</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>6.219887e+06</td>
      <td>5.309413e+06</td>
      <td>6.228451e+06</td>
      <td>6.589798e+06</td>
      <td>7.501556e+06</td>
      <td>7.599764e+06</td>
      <td>6.567960e+06</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>8.774407e+04</td>
      <td>9.180121e+04</td>
      <td>9.620217e+04</td>
      <td>8.875744e+04</td>
      <td>9.500199e+04</td>
      <td>9.600254e+04</td>
      <td>9.053525e+04</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>4.995968e+04</td>
      <td>4.937785e+04</td>
      <td>5.443679e+04</td>
      <td>4.469902e+04</td>
      <td>4.566914e+04</td>
      <td>5.101547e+04</td>
      <td>5.089759e+04</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>2.305465e+05</td>
      <td>2.284133e+05</td>
      <td>2.708935e+05</td>
      <td>1.548252e+05</td>
      <td>2.332056e+05</td>
      <td>2.835167e+05</td>
      <td>1.574007e+05</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>4.954698e+05</td>
      <td>5.731698e+05</td>
      <td>4.517045e+05</td>
      <td>5.592610e+05</td>
      <td>5.947277e+05</td>
      <td>6.412802e+05</td>
      <td>5.644891e+05</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>1.451878e+05</td>
      <td>1.274597e+05</td>
      <td>1.463222e+05</td>
      <td>1.293543e+05</td>
      <td>1.327782e+05</td>
      <td>1.165467e+05</td>
      <td>1.013006e+05</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>1.661169e+04</td>
      <td>1.696441e+04</td>
      <td>1.168063e+04</td>
      <td>1.009675e+04</td>
      <td>1.461058e+04</td>
      <td>2.136270e+04</td>
      <td>1.475014e+04</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>8.305626e+04</td>
      <td>1.011743e+05</td>
      <td>5.911841e+04</td>
      <td>9.018914e+04</td>
      <td>8.476088e+04</td>
      <td>9.248238e+04</td>
      <td>8.466966e+04</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1.132082e+06</td>
      <td>1.290806e+06</td>
      <td>1.205169e+06</td>
      <td>1.372447e+06</td>
      <td>1.256888e+06</td>
      <td>1.221904e+06</td>
      <td>1.289837e+06</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>1.057399e+05</td>
      <td>1.110049e+05</td>
      <td>1.111291e+05</td>
      <td>1.066525e+05</td>
      <td>1.056287e+05</td>
      <td>1.127141e+05</td>
      <td>1.069696e+05</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>1.007479e+05</td>
      <td>6.667161e+04</td>
      <td>8.081300e+04</td>
      <td>9.200752e+04</td>
      <td>1.164235e+05</td>
      <td>7.168401e+04</td>
      <td>4.811408e+04</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>4.852431e+05</td>
      <td>5.945922e+05</td>
      <td>5.372641e+05</td>
      <td>4.532297e+05</td>
      <td>6.528548e+05</td>
      <td>6.401201e+05</td>
      <td>4.849205e+05</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>3.432021e+05</td>
      <td>4.073554e+05</td>
      <td>3.836830e+05</td>
      <td>4.175210e+05</td>
      <td>3.584550e+05</td>
      <td>4.462836e+05</td>
      <td>4.383270e+05</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>1.143217e+05</td>
      <td>9.177653e+04</td>
      <td>1.085457e+05</td>
      <td>8.662578e+04</td>
      <td>9.655062e+04</td>
      <td>8.581038e+04</td>
      <td>7.735988e+04</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1.393798e+06</td>
      <td>1.780993e+06</td>
      <td>1.164699e+06</td>
      <td>9.166575e+05</td>
      <td>1.305046e+06</td>
      <td>1.520788e+06</td>
      <td>8.528673e+05</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>7.866956e+04</td>
      <td>8.089149e+04</td>
      <td>8.705634e+04</td>
      <td>8.138151e+04</td>
      <td>8.990870e+04</td>
      <td>8.333327e+04</td>
      <td>6.619861e+04</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>1.611324e+05</td>
      <td>1.618576e+05</td>
      <td>1.684799e+05</td>
      <td>1.657254e+05</td>
      <td>1.691351e+05</td>
      <td>1.941455e+05</td>
      <td>1.634842e+05</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1.346013e+06</td>
      <td>1.483777e+06</td>
      <td>1.406437e+06</td>
      <td>1.317455e+06</td>
      <td>1.269751e+06</td>
      <td>1.374450e+06</td>
      <td>1.502787e+06</td>
    </tr>
  </tbody>
</table>
</div>



### Test for Normality: Shapiro-Wilk

#### 2019


```python
## Selecting Malaysia 2019 Data 
data_2019 = hypothesis_testing_df['tCH4_2019']
data_2019
```




    0     2.070985e+06
    1     3.294713e+05
    2     5.603352e+06
    3     1.148324e+04
    4     1.266668e+06
    5     7.501556e+06
    6     9.500199e+04
    7     4.566914e+04
    8     2.332056e+05
    9     5.947277e+05
    10    1.327782e+05
    11    1.461058e+04
    12    8.476088e+04
    13    1.256888e+06
    14    1.056287e+05
    15    1.164235e+05
    16    6.528548e+05
    17    3.584550e+05
    18    9.655062e+04
    19    1.305046e+06
    20    8.990870e+04
    21    1.691351e+05
    22    1.269751e+06
    Name: tCH4_2019, dtype: float64




```python
results = stats.shapiro(data_2019)
print('stat=%.3f, p=%.3f' % (results.statistic, results.pvalue))
if results.pvalue > 0.05:
	print('Probably Gaussian')
else:
	print('Probably not Gaussian')
```

    stat=0.567, p=0.000
    Probably not Gaussian


##### Results

The distribution is not gausian so a non-paremtric test must be completed.  It is not necessary to perform this test on the 2020 data, but I will do so anyways for practice.

#### 2020


```python
## Selecting the Malaysia Data 2020
data_2020 = hypothesis_testing_df['tCH4_2020']
```


```python
results = stats.shapiro(data_2020)
print('stat=%.3f, p=%.3f' % (results.statistic, results.pvalue))
if results.pvalue > 0.05:
	print('Probably Gaussian')
else:
	print('Probably not Gaussian')
```

    stat=0.565, p=0.000
    Probably not Gaussian


##### Results

The 2020 data is not gausian which verifies that we will need to perform a non parmetric test

### Independence of Samples.  
We have to assume that the samples are independent of each other as we know they are dependent on hecatares.  
Though the correlations are rather high this is due to the smiliarity of hectares per year.  Thus the amount of ch4 is similiar


### Distribution Similiarity

#### Mann-Whitney U Test


```python
# Example of the Mann-Whitney U Test

stat, p = stats.mannwhitneyu(data_2019, data_2020)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')
```

    stat=266.000, p=0.982
    Probably the same distribution


### Kruskal Wallis test


```python

stat, p = stats.kruskal(data_2019, data_2020)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')
```

    stat=0.001, p=0.974
    Probably the same distribution


### Friedman Test

Just for the sake of it I will compare data across all distributions


```python
# Example of the Friedman Test
#data_2014 = hypothesis_testing_df['tCH4_2014']
data_2015 = hypothesis_testing_df['tCH4_2015']
data_2016 = hypothesis_testing_df['tCH4_2016']
data_2017 = hypothesis_testing_df['tCH4_2017']
data_2018 = hypothesis_testing_df['tCH4_2018']

stat, p = stats.friedmanchisquare(data_2015, data_2016, data_2017, data_2018, data_2019, data_2020)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')
```

    stat=11.472, p=0.043
    Probably different distributions


#### Results.  

Some distributions differ from one another.  Which those are have yet to be discovered.  For the sake of this analysis I will not attempt to identify them.  

The statment that the distributions of the 2019 and 2020 data do not differ cannot differ.  That said we also cannot claim that the means are statistically equivalent as the data is not parametric.  


