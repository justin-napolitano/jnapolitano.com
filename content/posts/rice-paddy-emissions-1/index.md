+++
categories = ['Statistical Analysis', 'Python']
date = '2022-05-21T08:30:32'
description = 'Fact checking reported methane emissions proposed by the UN and Climate TRACE'
tags = ['data', 'university-of-malaysia', 'climate-change', 'emissions']
title = 'Rice Paddy Methane Emissions Estimation: Part 1'
featured_image = 'post-image.*'
author = "Justin Napolitano"
images = ['featured-rice-paddies.jpeg']
series = ['Rice Paddy Methane Emissions']
image = 'featured.*'
+++

# Methane Emissions Estimation Data Part 1: A Comparison between FAOSTAT and University of Malaysia Estimates


This post documents the data exploration phase of a project that determines whether global methane emissions produced by rice paddies are undercounted. 

It is fairly code python and pandas heavy. 

The code and data exploration follows the summary below.  

## Inspiration for this work

The University of Malaysia in partnership with Climate TRACE release a paper stating that the UN undercounts rice paddy methane emissions by about 16%.  Upon review of their claims, I decided to test the data myself across a 5 year distribution to verify that the claims hold up across multiple distributions.  

### University of Malaysia Methodological Deficiencies
* Comparing a 2019 distribution FAOSTAT to a 2020 distribution.
* Rounding to 4 signficant figures.
* Testing only one year of emissions data.
* Did not publish data to hypothesis testing to determine if emission distributions significantly vary annually and between states.
* Relying only on satellite data may undercount hectares in cultivation at higher altitudes.  

### FaoStat Methodological Deficiencies
* Relies upon official government statistics which can be manipulated at any point along the bureaucratic paper chain.
* There is an incentive for certain nations to reduce their counts in order to receive international aid and to meet emissions standards.  

### University of Malaysia acknowledging deficiencies (like all good papers should)

"The difference between harvested rice cultivation area from statistical data and remote-sensing estimates can be due to two factors: (i) MODIS data which have moderate spatial resolution lead to mixed pixels, where rice fields and non-rice fields are combined. This can overestimate area, especially in lowland regions and have a low ability to detect small rice field patches in upland regions (Frolking et al 1999, Seto et al 2000); and (ii) political and policy factors (Yan et al., 2019) such as determination of the amount of subsidies for fertilizers and evaluation of achievement of government programs in the agricultural sector. Other factors that contribute to discrepancy in CH4 emission are from different emission and scale factors that are related to water regime and organic amendment. These values give high uncertainty since the availability of these data are limited and quite variable."

## My Initial Impressions and findings

### Initial 

The percent difference and the tonnage difference do not support each other.  I need to recalculate the totals section to ensure that we are doing things correctly.  

I need to confirm the values, but I'm initially impressed by the fact that the FAOSTAT data reports higher values than the Malaysia data on average.  According to the included paper this should not be the case.  

### Verified

I calculated differences totals and means per DataFrame to ensure accuracy prior to the join.  I also dropped pre-calcuated values when joining to ensure that the aggregation algorithms to not modify the results. 

The data is now consistent and supports the findings of the University of Malaysia Paper.  With that said it is important to note that the differences recorded are far smaller than suggested.  

## Import Dependencies


```python
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import contextily as cx
from shapely.geometry import Point, LineString, Polygon
import numpy as np
from scipy.spatial import cKDTree
from geopy.distance import distance
import scipy.stats as stats

```

### Dependencies 

* Geopandas
* pandas
* openpyxl
* Shapely 
* geopy Distance
* numpy

## Exploration Plan

### Data Imports

* /Users/jnapolitano/Projects/wattime-takehome/data/ch4_2015-2021.xlsx
* /Users/jnapolitano/Projects/wattime-takehome/data/emissions_csv_fao_emiss_csv_ch4_fao_2015_2019_tonnes.xlsx

### Import Data Frames
Since jupyter caches the data to the notebook json I can import the dataframes that I will be using together.

If I were to build automated scripts to perform the analysis I would only load the data necessary to perform a process. 

### Experiment with Plots for each Set
I don't know exactly which plots I want to include in the final report. 

I 'll plot a few for each data set 

### Calculate differences between the datasets
* create a differences data frame
* write to file for use
* plot



## University of Malaysia Emission Estimates


```python
filepath = "/Users/jnapolitano/Projects/wattime-takehome/wattime-takehome/data/ch4_2015-2021.xlsx"

malaysia_emissions_df = pd.read_excel(filepath)
```

### Print Df Head


```python
malaysia_emissions_df
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
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>Total</td>
      <td>2.270357e+07</td>
      <td>2.205208e+07</td>
      <td>2.237234e+07</td>
      <td>2.179462e+07</td>
      <td>2.340491e+07</td>
      <td>2.485387e+07</td>
      <td>2.218801e+07</td>
    </tr>
  </tbody>
</table>
</div>



### Calculate Co2 Equivalency


```python
malaysia_emissions_df['tCO2_2015'] = (malaysia_emissions_df['tCH4_2015'] * 25)
malaysia_emissions_df['tCO2_2016'] = (malaysia_emissions_df['tCH4_2016'] * 25)
malaysia_emissions_df['tCO2_2017'] = (malaysia_emissions_df['tCH4_2017'] * 25)
malaysia_emissions_df['tCO2_2018'] = (malaysia_emissions_df['tCH4_2018'] * 25)
malaysia_emissions_df['tCO2_2019'] = (malaysia_emissions_df['tCH4_2019'] * 25)
```

### Calculate Means 


```python
malaysia_emissions_df.loc['mean'] = malaysia_emissions_df.loc[(malaysia_emissions_df['country_name'] != "Total")].select_dtypes(np.number).mean()
malaysia_emissions_df.at['mean','country_name'] = 'mean'
malaysia_emissions_df
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
      <th>tCO2_2015</th>
      <th>tCO2_2016</th>
      <th>tCO2_2017</th>
      <th>tCO2_2018</th>
      <th>tCO2_2019</th>
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
      <td>5.861049e+07</td>
      <td>5.695395e+07</td>
      <td>5.247394e+07</td>
      <td>5.353076e+07</td>
      <td>5.177463e+07</td>
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
      <td>8.525583e+06</td>
      <td>7.760473e+06</td>
      <td>9.312934e+06</td>
      <td>9.292575e+06</td>
      <td>8.236783e+06</td>
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
      <td>1.533412e+08</td>
      <td>1.464883e+08</td>
      <td>1.588768e+08</td>
      <td>1.353491e+08</td>
      <td>1.400838e+08</td>
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
      <td>2.853661e+05</td>
      <td>3.337007e+05</td>
      <td>3.043248e+05</td>
      <td>3.513524e+05</td>
      <td>2.870810e+05</td>
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
      <td>3.209122e+07</td>
      <td>2.557824e+07</td>
      <td>2.403832e+07</td>
      <td>2.942454e+07</td>
      <td>3.166670e+07</td>
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
      <td>1.554972e+08</td>
      <td>1.327353e+08</td>
      <td>1.557113e+08</td>
      <td>1.647450e+08</td>
      <td>1.875389e+08</td>
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
      <td>2.193602e+06</td>
      <td>2.295030e+06</td>
      <td>2.405054e+06</td>
      <td>2.218936e+06</td>
      <td>2.375050e+06</td>
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
      <td>1.248992e+06</td>
      <td>1.234446e+06</td>
      <td>1.360920e+06</td>
      <td>1.117475e+06</td>
      <td>1.141729e+06</td>
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
      <td>5.763662e+06</td>
      <td>5.710333e+06</td>
      <td>6.772337e+06</td>
      <td>3.870631e+06</td>
      <td>5.830141e+06</td>
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
      <td>1.238675e+07</td>
      <td>1.432925e+07</td>
      <td>1.129261e+07</td>
      <td>1.398153e+07</td>
      <td>1.486819e+07</td>
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
      <td>3.629695e+06</td>
      <td>3.186493e+06</td>
      <td>3.658056e+06</td>
      <td>3.233858e+06</td>
      <td>3.319455e+06</td>
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
      <td>4.152924e+05</td>
      <td>4.241102e+05</td>
      <td>2.920158e+05</td>
      <td>2.524186e+05</td>
      <td>3.652645e+05</td>
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
      <td>2.076407e+06</td>
      <td>2.529358e+06</td>
      <td>1.477960e+06</td>
      <td>2.254728e+06</td>
      <td>2.119022e+06</td>
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
      <td>2.830206e+07</td>
      <td>3.227014e+07</td>
      <td>3.012923e+07</td>
      <td>3.431117e+07</td>
      <td>3.142221e+07</td>
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
      <td>2.643498e+06</td>
      <td>2.775123e+06</td>
      <td>2.778227e+06</td>
      <td>2.666313e+06</td>
      <td>2.640717e+06</td>
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
      <td>2.518697e+06</td>
      <td>1.666790e+06</td>
      <td>2.020325e+06</td>
      <td>2.300188e+06</td>
      <td>2.910588e+06</td>
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
      <td>1.213108e+07</td>
      <td>1.486480e+07</td>
      <td>1.343160e+07</td>
      <td>1.133074e+07</td>
      <td>1.632137e+07</td>
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
      <td>8.580052e+06</td>
      <td>1.018389e+07</td>
      <td>9.592074e+06</td>
      <td>1.043803e+07</td>
      <td>8.961374e+06</td>
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
      <td>2.858041e+06</td>
      <td>2.294413e+06</td>
      <td>2.713641e+06</td>
      <td>2.165645e+06</td>
      <td>2.413765e+06</td>
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
      <td>3.484495e+07</td>
      <td>4.452483e+07</td>
      <td>2.911748e+07</td>
      <td>2.291644e+07</td>
      <td>3.262615e+07</td>
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
      <td>1.966739e+06</td>
      <td>2.022287e+06</td>
      <td>2.176408e+06</td>
      <td>2.034538e+06</td>
      <td>2.247717e+06</td>
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
      <td>4.028310e+06</td>
      <td>4.046440e+06</td>
      <td>4.211999e+06</td>
      <td>4.143136e+06</td>
      <td>4.228377e+06</td>
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
      <td>3.365033e+07</td>
      <td>3.709441e+07</td>
      <td>3.516092e+07</td>
      <td>3.293637e+07</td>
      <td>3.174377e+07</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>Total</td>
      <td>2.270357e+07</td>
      <td>2.205208e+07</td>
      <td>2.237234e+07</td>
      <td>2.179462e+07</td>
      <td>2.340491e+07</td>
      <td>2.485387e+07</td>
      <td>2.218801e+07</td>
      <td>5.675891e+08</td>
      <td>5.513021e+08</td>
      <td>5.593084e+08</td>
      <td>5.448654e+08</td>
      <td>5.851228e+08</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>NaN</td>
      <td>mean</td>
      <td>9.871116e+05</td>
      <td>9.587863e+05</td>
      <td>9.727103e+05</td>
      <td>9.475920e+05</td>
      <td>1.017605e+06</td>
      <td>1.080603e+06</td>
      <td>9.646959e+05</td>
      <td>2.467779e+07</td>
      <td>2.396966e+07</td>
      <td>2.431776e+07</td>
      <td>2.368980e+07</td>
      <td>2.544012e+07</td>
    </tr>
  </tbody>
</table>
</div>



### Calculate Means and Totals Across Rows


```python
mean_series = malaysia_emissions_df[['tCH4_2015','tCH4_2016','tCH4_2017','tCH4_2018','tCH4_2019']].select_dtypes(np.number).mean(axis=1)
total_series = malaysia_emissions_df[['tCH4_2015','tCH4_2016','tCH4_2017','tCH4_2018','tCH4_2019']].select_dtypes(np.number).sum(axis=1)
malaysia_emissions_df["Mean_CH4"] = mean_series
malaysia_emissions_df['Total_CH4'] = total_series 
```


```python
## the select np.number is uncecessary, but i'm including anyways as it doesnt really hurt but for a small calculation penalty
mean_series = malaysia_emissions_df[['tCO2_2015','tCO2_2016','tCO2_2017','tCO2_2018','tCO2_2019']].select_dtypes(np.number).mean(axis=1)
total_series = malaysia_emissions_df[['tCO2_2015','tCO2_2016','tCO2_2017','tCO2_2018','tCO2_2019']].select_dtypes(np.number).sum(axis=1)
malaysia_emissions_df["Mean_CO2"] = mean_series
malaysia_emissions_df['Total_CO2'] = total_series 
```


```python
malaysia_emissions_df.reset_index(inplace=True, drop = True)
```


```python
malaysia_emissions_df
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
      <th>tCO2_2015</th>
      <th>tCO2_2016</th>
      <th>tCO2_2017</th>
      <th>tCO2_2018</th>
      <th>tCO2_2019</th>
      <th>Mean_CH4</th>
      <th>Total_CH4</th>
      <th>Mean_CO2</th>
      <th>Total_CO2</th>
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
      <td>5.861049e+07</td>
      <td>5.695395e+07</td>
      <td>5.247394e+07</td>
      <td>5.353076e+07</td>
      <td>5.177463e+07</td>
      <td>2.186750e+06</td>
      <td>1.093375e+07</td>
      <td>5.466875e+07</td>
      <td>2.733438e+08</td>
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
      <td>8.525583e+06</td>
      <td>7.760473e+06</td>
      <td>9.312934e+06</td>
      <td>9.292575e+06</td>
      <td>8.236783e+06</td>
      <td>3.450268e+05</td>
      <td>1.725134e+06</td>
      <td>8.625670e+06</td>
      <td>4.312835e+07</td>
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
      <td>1.533412e+08</td>
      <td>1.464883e+08</td>
      <td>1.588768e+08</td>
      <td>1.353491e+08</td>
      <td>1.400838e+08</td>
      <td>5.873113e+06</td>
      <td>2.936556e+07</td>
      <td>1.468278e+08</td>
      <td>7.341391e+08</td>
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
      <td>2.853661e+05</td>
      <td>3.337007e+05</td>
      <td>3.043248e+05</td>
      <td>3.513524e+05</td>
      <td>2.870810e+05</td>
      <td>1.249460e+04</td>
      <td>6.247300e+04</td>
      <td>3.123650e+05</td>
      <td>1.561825e+06</td>
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
      <td>3.209122e+07</td>
      <td>2.557824e+07</td>
      <td>2.403832e+07</td>
      <td>2.942454e+07</td>
      <td>3.166670e+07</td>
      <td>1.142392e+06</td>
      <td>5.711960e+06</td>
      <td>2.855980e+07</td>
      <td>1.427990e+08</td>
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
      <td>1.554972e+08</td>
      <td>1.327353e+08</td>
      <td>1.557113e+08</td>
      <td>1.647450e+08</td>
      <td>1.875389e+08</td>
      <td>6.369821e+06</td>
      <td>3.184910e+07</td>
      <td>1.592455e+08</td>
      <td>7.962276e+08</td>
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
      <td>2.193602e+06</td>
      <td>2.295030e+06</td>
      <td>2.405054e+06</td>
      <td>2.218936e+06</td>
      <td>2.375050e+06</td>
      <td>9.190138e+04</td>
      <td>4.595069e+05</td>
      <td>2.297534e+06</td>
      <td>1.148767e+07</td>
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
      <td>1.248992e+06</td>
      <td>1.234446e+06</td>
      <td>1.360920e+06</td>
      <td>1.117475e+06</td>
      <td>1.141729e+06</td>
      <td>4.882850e+04</td>
      <td>2.441425e+05</td>
      <td>1.220712e+06</td>
      <td>6.103562e+06</td>
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
      <td>5.763662e+06</td>
      <td>5.710333e+06</td>
      <td>6.772337e+06</td>
      <td>3.870631e+06</td>
      <td>5.830141e+06</td>
      <td>2.235768e+05</td>
      <td>1.117884e+06</td>
      <td>5.589421e+06</td>
      <td>2.794710e+07</td>
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
      <td>1.238675e+07</td>
      <td>1.432925e+07</td>
      <td>1.129261e+07</td>
      <td>1.398153e+07</td>
      <td>1.486819e+07</td>
      <td>5.348666e+05</td>
      <td>2.674333e+06</td>
      <td>1.337166e+07</td>
      <td>6.685832e+07</td>
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
      <td>3.629695e+06</td>
      <td>3.186493e+06</td>
      <td>3.658056e+06</td>
      <td>3.233858e+06</td>
      <td>3.319455e+06</td>
      <td>1.362205e+05</td>
      <td>6.811023e+05</td>
      <td>3.405512e+06</td>
      <td>1.702756e+07</td>
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
      <td>4.152924e+05</td>
      <td>4.241102e+05</td>
      <td>2.920158e+05</td>
      <td>2.524186e+05</td>
      <td>3.652645e+05</td>
      <td>1.399281e+04</td>
      <td>6.996406e+04</td>
      <td>3.498203e+05</td>
      <td>1.749102e+06</td>
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
      <td>2.076407e+06</td>
      <td>2.529358e+06</td>
      <td>1.477960e+06</td>
      <td>2.254728e+06</td>
      <td>2.119022e+06</td>
      <td>8.365981e+04</td>
      <td>4.182990e+05</td>
      <td>2.091495e+06</td>
      <td>1.045748e+07</td>
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
      <td>2.830206e+07</td>
      <td>3.227014e+07</td>
      <td>3.012923e+07</td>
      <td>3.431117e+07</td>
      <td>3.142221e+07</td>
      <td>1.251478e+06</td>
      <td>6.257392e+06</td>
      <td>3.128696e+07</td>
      <td>1.564348e+08</td>
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
      <td>2.643498e+06</td>
      <td>2.775123e+06</td>
      <td>2.778227e+06</td>
      <td>2.666313e+06</td>
      <td>2.640717e+06</td>
      <td>1.080310e+05</td>
      <td>5.401551e+05</td>
      <td>2.700775e+06</td>
      <td>1.350388e+07</td>
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
      <td>2.518697e+06</td>
      <td>1.666790e+06</td>
      <td>2.020325e+06</td>
      <td>2.300188e+06</td>
      <td>2.910588e+06</td>
      <td>9.133271e+04</td>
      <td>4.566635e+05</td>
      <td>2.283318e+06</td>
      <td>1.141659e+07</td>
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
      <td>1.213108e+07</td>
      <td>1.486480e+07</td>
      <td>1.343160e+07</td>
      <td>1.133074e+07</td>
      <td>1.632137e+07</td>
      <td>5.446368e+05</td>
      <td>2.723184e+06</td>
      <td>1.361592e+07</td>
      <td>6.807960e+07</td>
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
      <td>8.580052e+06</td>
      <td>1.018389e+07</td>
      <td>9.592074e+06</td>
      <td>1.043803e+07</td>
      <td>8.961374e+06</td>
      <td>3.820433e+05</td>
      <td>1.910216e+06</td>
      <td>9.551082e+06</td>
      <td>4.775541e+07</td>
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
      <td>2.858041e+06</td>
      <td>2.294413e+06</td>
      <td>2.713641e+06</td>
      <td>2.165645e+06</td>
      <td>2.413765e+06</td>
      <td>9.956405e+04</td>
      <td>4.978202e+05</td>
      <td>2.489101e+06</td>
      <td>1.244551e+07</td>
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
      <td>3.484495e+07</td>
      <td>4.452483e+07</td>
      <td>2.911748e+07</td>
      <td>2.291644e+07</td>
      <td>3.262615e+07</td>
      <td>1.312239e+06</td>
      <td>6.561194e+06</td>
      <td>3.280597e+07</td>
      <td>1.640298e+08</td>
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
      <td>1.966739e+06</td>
      <td>2.022287e+06</td>
      <td>2.176408e+06</td>
      <td>2.034538e+06</td>
      <td>2.247717e+06</td>
      <td>8.358152e+04</td>
      <td>4.179076e+05</td>
      <td>2.089538e+06</td>
      <td>1.044769e+07</td>
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
      <td>4.028310e+06</td>
      <td>4.046440e+06</td>
      <td>4.211999e+06</td>
      <td>4.143136e+06</td>
      <td>4.228377e+06</td>
      <td>1.652661e+05</td>
      <td>8.263305e+05</td>
      <td>4.131652e+06</td>
      <td>2.065826e+07</td>
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
      <td>3.365033e+07</td>
      <td>3.709441e+07</td>
      <td>3.516092e+07</td>
      <td>3.293637e+07</td>
      <td>3.174377e+07</td>
      <td>1.364686e+06</td>
      <td>6.823432e+06</td>
      <td>3.411716e+07</td>
      <td>1.705858e+08</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>Total</td>
      <td>2.270357e+07</td>
      <td>2.205208e+07</td>
      <td>2.237234e+07</td>
      <td>2.179462e+07</td>
      <td>2.340491e+07</td>
      <td>2.485387e+07</td>
      <td>2.218801e+07</td>
      <td>5.675891e+08</td>
      <td>5.513021e+08</td>
      <td>5.593084e+08</td>
      <td>5.448654e+08</td>
      <td>5.851228e+08</td>
      <td>2.246550e+07</td>
      <td>1.123275e+08</td>
      <td>5.616376e+08</td>
      <td>2.808188e+09</td>
    </tr>
    <tr>
      <th>24</th>
      <td>NaN</td>
      <td>mean</td>
      <td>9.871116e+05</td>
      <td>9.587863e+05</td>
      <td>9.727103e+05</td>
      <td>9.475920e+05</td>
      <td>1.017605e+06</td>
      <td>1.080603e+06</td>
      <td>9.646959e+05</td>
      <td>2.467779e+07</td>
      <td>2.396966e+07</td>
      <td>2.431776e+07</td>
      <td>2.368980e+07</td>
      <td>2.544012e+07</td>
      <td>9.767610e+05</td>
      <td>4.883805e+06</td>
      <td>2.441902e+07</td>
      <td>1.220951e+08</td>
    </tr>
  </tbody>
</table>
</div>



### Write Data to File


```python
outfile = "/Users/jnapolitano/Projects/wattime-takehome/wattime-takehome/data/TRACE_DATA.csv"

malaysia_emissions_df.to_csv(outfile)
```

## University of Malaysia Plots

### University of Malaysia Bar Plot


```python
malaysia_emissions_df.plot(kind = "barh", x = 'country_name', xlabel = "Country Name", ylabel = "CH4 Tonnes", figsize = (10,5))
```




    <AxesSubplot:ylabel='Country Name'>




    
![png](data_exploration_files/data_exploration_28_1.png)
    


### University of Malaysia Density Plot


```python
malaysia_emissions_df.plot(rot = 0, kind = "density", figsize = (15,5)) 
```




    <AxesSubplot:ylabel='Density'>




    
![png](data_exploration_files/data_exploration_30_1.png)
    


I did not exclude totals or mean from the dataframe, but as we can see the second hump in the density graph shows the distribution of totals annualy.  Interestingly the 2020 data is shifted further to the right than other years.  This actually questions the validity of the study promoted by the University of malaysia

## FAOSTAT Data 


```python
filepath = "/Users/jnapolitano/Projects/wattime-takehome/wattime-takehome/data/emissions_csv_fao_emiss_csv_ch4_fao_2015_2019_tonnes.xlsx"

faostat_emissions_df = pd.read_excel(filepath)
```

### Print FAOSTAT Data


```python
## I didn't write the index to the csv file in the previous step.  IF time permits go back and fix this error
faostat_emissions_df

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
      <th>code</th>
      <th>country</th>
      <th>country_fao</th>
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>2020</th>
      <th>2021</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1093480.4</td>
      <td>1154531.0</td>
      <td>1144591.0</td>
      <td>1144745.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>126278.2</td>
      <td>130322.9</td>
      <td>121615.2</td>
      <td>111084.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>China, mainland</td>
      <td>5406593.9</td>
      <td>5399920.0</td>
      <td>5400129.0</td>
      <td>5302173.1</td>
      <td>5214454.7</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>55073.1</td>
      <td>54232.4</td>
      <td>52925.0</td>
      <td>52098.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2387656.4</td>
      <td>2425290.6</td>
      <td>2405613.8</td>
      <td>2257604.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4559136.4</td>
      <td>4620790.8</td>
      <td>4661154.9</td>
      <td>4621416.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>131008.5</td>
      <td>87233.6</td>
      <td>93936.6</td>
      <td>96103.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>118003.0</td>
      <td>118003.0</td>
      <td>109463.8</td>
      <td>110895.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>326403.0</td>
      <td>323700.3</td>
      <td>322245.0</td>
      <td>320581.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>459003.1</td>
      <td>473745.3</td>
      <td>479362.7</td>
      <td>468378.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>Republic of Korea</td>
      <td>167862.2</td>
      <td>163534.1</td>
      <td>158489.7</td>
      <td>154911.3</td>
      <td>153260.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>Lao People's Democratic Republic</td>
      <td>94826.8</td>
      <td>95630.0</td>
      <td>93940.7</td>
      <td>83333.6</td>
      <td>77005.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>121756.3</td>
      <td>84456.3</td>
      <td>111049.0</td>
      <td>102156.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1052287.7</td>
      <td>1087029.5</td>
      <td>1118850.0</td>
      <td>1083100.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>123232.8</td>
      <td>122656.3</td>
      <td>125238.5</td>
      <td>122453.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>142723.7</td>
      <td>162574.6</td>
      <td>153890.8</td>
      <td>156215.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>381361.8</td>
      <td>406083.3</td>
      <td>393404.2</td>
      <td>424755.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>Philippines</td>
      <td>1557810.6</td>
      <td>1524292.5</td>
      <td>1609862.5</td>
      <td>1606047.8</td>
      <td>1556225.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>Democratic People's Republic of Korea</td>
      <td>82823.3</td>
      <td>83442.3</td>
      <td>84596.2</td>
      <td>83943.3</td>
      <td>82937.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1703327.7</td>
      <td>1714465.6</td>
      <td>1702989.1</td>
      <td>1553835.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>China, Taiwan Province of</td>
      <td>45838.7</td>
      <td>49838.3</td>
      <td>49991.2</td>
      <td>49414.1</td>
      <td>49152.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>United States of America</td>
      <td>364728.0</td>
      <td>438662.0</td>
      <td>336255.5</td>
      <td>412177.5</td>
      <td>350136.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1365173.8</td>
      <td>1360551.6</td>
      <td>1336231.2</td>
      <td>1318431.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Total</td>
      <td>23829994.0</td>
      <td>23917225.1</td>
      <td>24075931.9</td>
      <td>24042561.5</td>
      <td>23446028.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



### Change code to iso3_country


```python

faostat_emissions_df.rename(columns={"code": "iso3_country"}, inplace =True)
faostat_emissions_df.rename(columns={"country": "country_name"}, inplace =True)
# The column title is not a string.  It is understood as an int or a datetime.  
#faostat_emissions_df['2015']
faostat_emissions_df
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
      <th>country_fao</th>
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>2020</th>
      <th>2021</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1093480.4</td>
      <td>1154531.0</td>
      <td>1144591.0</td>
      <td>1144745.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>126278.2</td>
      <td>130322.9</td>
      <td>121615.2</td>
      <td>111084.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>China, mainland</td>
      <td>5406593.9</td>
      <td>5399920.0</td>
      <td>5400129.0</td>
      <td>5302173.1</td>
      <td>5214454.7</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>55073.1</td>
      <td>54232.4</td>
      <td>52925.0</td>
      <td>52098.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2387656.4</td>
      <td>2425290.6</td>
      <td>2405613.8</td>
      <td>2257604.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4559136.4</td>
      <td>4620790.8</td>
      <td>4661154.9</td>
      <td>4621416.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>131008.5</td>
      <td>87233.6</td>
      <td>93936.6</td>
      <td>96103.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>118003.0</td>
      <td>118003.0</td>
      <td>109463.8</td>
      <td>110895.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>326403.0</td>
      <td>323700.3</td>
      <td>322245.0</td>
      <td>320581.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>459003.1</td>
      <td>473745.3</td>
      <td>479362.7</td>
      <td>468378.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>Republic of Korea</td>
      <td>167862.2</td>
      <td>163534.1</td>
      <td>158489.7</td>
      <td>154911.3</td>
      <td>153260.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>Lao People's Democratic Republic</td>
      <td>94826.8</td>
      <td>95630.0</td>
      <td>93940.7</td>
      <td>83333.6</td>
      <td>77005.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>121756.3</td>
      <td>84456.3</td>
      <td>111049.0</td>
      <td>102156.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1052287.7</td>
      <td>1087029.5</td>
      <td>1118850.0</td>
      <td>1083100.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>123232.8</td>
      <td>122656.3</td>
      <td>125238.5</td>
      <td>122453.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>142723.7</td>
      <td>162574.6</td>
      <td>153890.8</td>
      <td>156215.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>381361.8</td>
      <td>406083.3</td>
      <td>393404.2</td>
      <td>424755.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>Philippines</td>
      <td>1557810.6</td>
      <td>1524292.5</td>
      <td>1609862.5</td>
      <td>1606047.8</td>
      <td>1556225.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>Democratic People's Republic of Korea</td>
      <td>82823.3</td>
      <td>83442.3</td>
      <td>84596.2</td>
      <td>83943.3</td>
      <td>82937.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1703327.7</td>
      <td>1714465.6</td>
      <td>1702989.1</td>
      <td>1553835.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>China, Taiwan Province of</td>
      <td>45838.7</td>
      <td>49838.3</td>
      <td>49991.2</td>
      <td>49414.1</td>
      <td>49152.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>United States of America</td>
      <td>364728.0</td>
      <td>438662.0</td>
      <td>336255.5</td>
      <td>412177.5</td>
      <td>350136.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1365173.8</td>
      <td>1360551.6</td>
      <td>1336231.2</td>
      <td>1318431.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Total</td>
      <td>23829994.0</td>
      <td>23917225.1</td>
      <td>24075931.9</td>
      <td>24042561.5</td>
      <td>23446028.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



### Set country_name total to total


```python
faostat_emissions_df.at[23,'country_name'] = 'Total'
```

### Drop Fao Country Code


```python
faostat_emissions_df.drop(labels = ['country_fao'], axis=1, inplace=True)
faostat_emissions_df
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
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>2020</th>
      <th>2021</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1093480.4</td>
      <td>1154531.0</td>
      <td>1144591.0</td>
      <td>1144745.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>126278.2</td>
      <td>130322.9</td>
      <td>121615.2</td>
      <td>111084.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5399920.0</td>
      <td>5400129.0</td>
      <td>5302173.1</td>
      <td>5214454.7</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>55073.1</td>
      <td>54232.4</td>
      <td>52925.0</td>
      <td>52098.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2387656.4</td>
      <td>2425290.6</td>
      <td>2405613.8</td>
      <td>2257604.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4559136.4</td>
      <td>4620790.8</td>
      <td>4661154.9</td>
      <td>4621416.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>131008.5</td>
      <td>87233.6</td>
      <td>93936.6</td>
      <td>96103.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>118003.0</td>
      <td>118003.0</td>
      <td>109463.8</td>
      <td>110895.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>326403.0</td>
      <td>323700.3</td>
      <td>322245.0</td>
      <td>320581.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>459003.1</td>
      <td>473745.3</td>
      <td>479362.7</td>
      <td>468378.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>163534.1</td>
      <td>158489.7</td>
      <td>154911.3</td>
      <td>153260.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>95630.0</td>
      <td>93940.7</td>
      <td>83333.6</td>
      <td>77005.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>121756.3</td>
      <td>84456.3</td>
      <td>111049.0</td>
      <td>102156.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1052287.7</td>
      <td>1087029.5</td>
      <td>1118850.0</td>
      <td>1083100.3</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>123232.8</td>
      <td>122656.3</td>
      <td>125238.5</td>
      <td>122453.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>142723.7</td>
      <td>162574.6</td>
      <td>153890.8</td>
      <td>156215.4</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>381361.8</td>
      <td>406083.3</td>
      <td>393404.2</td>
      <td>424755.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1524292.5</td>
      <td>1609862.5</td>
      <td>1606047.8</td>
      <td>1556225.8</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>83442.3</td>
      <td>84596.2</td>
      <td>83943.3</td>
      <td>82937.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1703327.7</td>
      <td>1714465.6</td>
      <td>1702989.1</td>
      <td>1553835.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>49838.3</td>
      <td>49991.2</td>
      <td>49414.1</td>
      <td>49152.0</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>438662.0</td>
      <td>336255.5</td>
      <td>412177.5</td>
      <td>350136.5</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1365173.8</td>
      <td>1360551.6</td>
      <td>1336231.2</td>
      <td>1318431.1</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>Total</td>
      <td>23829994.0</td>
      <td>23917225.1</td>
      <td>24075931.9</td>
      <td>24042561.5</td>
      <td>23446028.9</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



### Calculate Co2 Equivalency


```python
faostat_emissions_df['tCO2_2015'] = faostat_emissions_df[2015] * 25
faostat_emissions_df['tCO2_2016'] = faostat_emissions_df[2016] * 25
faostat_emissions_df['tCO2_2017'] = faostat_emissions_df[2017] * 25
faostat_emissions_df['tCO2_2018'] = faostat_emissions_df[2018] * 25
faostat_emissions_df['tCO2_2019'] = faostat_emissions_df[2019] * 25
```

### Calculate Means


```python
faostat_emissions_df.loc['mean'] = faostat_emissions_df.loc[(faostat_emissions_df['country_name'] != "Total")].select_dtypes(np.number).mean()
faostat_emissions_df.at['mean','country_name'] = 'mean'
faostat_emissions_df.reset_index(inplace=True, drop=True)
#faostat_emissions_df.at['mean','country_fao'] = 'mean'

```

### Calculate Means and Totals Across Rows


```python
mean_series = faostat_emissions_df[[2015,2016,2017,2018,2019]].select_dtypes(np.number).mean(axis=1)
total_series = faostat_emissions_df[[2015,2016,2017,2018,2019]].select_dtypes(np.number).sum(axis=1)
faostat_emissions_df["Mean_CH4"] = mean_series
faostat_emissions_df['Total_CH4'] = total_series 
```


```python
## the select np.number is uncecessary, but i'm including anyways as it doesnt really hurt but for a small calculation penalty
mean_series = faostat_emissions_df[['tCO2_2015','tCO2_2016','tCO2_2017','tCO2_2018','tCO2_2019']].select_dtypes(np.number).mean(axis=1)
total_series = faostat_emissions_df[['tCO2_2015','tCO2_2016','tCO2_2017','tCO2_2018','tCO2_2019']].select_dtypes(np.number).sum(axis=1)
faostat_emissions_df["Mean_CO2"] = mean_series
faostat_emissions_df['Total_CO2'] = total_series 
```


```python
faostat_emissions_df.reset_index(inplace=True, drop=True)
```


```python
faostat_emissions_df
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
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>2020</th>
      <th>2021</th>
      <th>tCO2_2015</th>
      <th>tCO2_2016</th>
      <th>tCO2_2017</th>
      <th>tCO2_2018</th>
      <th>tCO2_2019</th>
      <th>Mean_CH4</th>
      <th>Total_CH4</th>
      <th>Mean_CO2</th>
      <th>Total_CO2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1.093480e+06</td>
      <td>1.154531e+06</td>
      <td>1.144591e+06</td>
      <td>1.144745e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>28282335.0</td>
      <td>2.733701e+07</td>
      <td>2.886328e+07</td>
      <td>2.861478e+07</td>
      <td>2.861863e+07</td>
      <td>1.133728e+06</td>
      <td>5.668641e+06</td>
      <td>2.834321e+07</td>
      <td>1.417160e+08</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>1.262782e+05</td>
      <td>1.303229e+05</td>
      <td>1.216152e+05</td>
      <td>1.110848e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3472757.5</td>
      <td>3.156955e+06</td>
      <td>3.258072e+06</td>
      <td>3.040380e+06</td>
      <td>2.777120e+06</td>
      <td>1.256423e+05</td>
      <td>6.282114e+05</td>
      <td>3.141057e+06</td>
      <td>1.570528e+07</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5.399920e+06</td>
      <td>5.400129e+06</td>
      <td>5.302173e+06</td>
      <td>5.214455e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>135164847.5</td>
      <td>1.349980e+08</td>
      <td>1.350032e+08</td>
      <td>1.325543e+08</td>
      <td>1.303614e+08</td>
      <td>5.344654e+06</td>
      <td>2.672327e+07</td>
      <td>1.336164e+08</td>
      <td>6.680818e+08</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>5.507310e+04</td>
      <td>5.423240e+04</td>
      <td>5.292500e+04</td>
      <td>5.209850e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1377055.0</td>
      <td>1.376828e+06</td>
      <td>1.355810e+06</td>
      <td>1.323125e+06</td>
      <td>1.302462e+06</td>
      <td>5.388224e+04</td>
      <td>2.694112e+05</td>
      <td>1.347056e+06</td>
      <td>6.735280e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2.387656e+06</td>
      <td>2.425291e+06</td>
      <td>2.405614e+06</td>
      <td>2.257604e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>60198837.5</td>
      <td>5.969141e+07</td>
      <td>6.063226e+07</td>
      <td>6.014035e+07</td>
      <td>5.644011e+07</td>
      <td>2.376824e+06</td>
      <td>1.188412e+07</td>
      <td>5.942059e+07</td>
      <td>2.971030e+08</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4.559136e+06</td>
      <td>4.620791e+06</td>
      <td>4.661155e+06</td>
      <td>4.621417e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>114506210.0</td>
      <td>1.139784e+08</td>
      <td>1.155198e+08</td>
      <td>1.165289e+08</td>
      <td>1.155354e+08</td>
      <td>4.608549e+06</td>
      <td>2.304275e+07</td>
      <td>1.152137e+08</td>
      <td>5.760687e+08</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>1.310085e+05</td>
      <td>8.723360e+04</td>
      <td>9.393660e+04</td>
      <td>9.610340e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2912167.5</td>
      <td>3.275212e+06</td>
      <td>2.180840e+06</td>
      <td>2.348415e+06</td>
      <td>2.402585e+06</td>
      <td>1.049538e+05</td>
      <td>5.247688e+05</td>
      <td>2.623844e+06</td>
      <td>1.311922e+07</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>1.180030e+05</td>
      <td>1.180030e+05</td>
      <td>1.094638e+05</td>
      <td>1.108951e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2864370.0</td>
      <td>2.950075e+06</td>
      <td>2.950075e+06</td>
      <td>2.736595e+06</td>
      <td>2.772378e+06</td>
      <td>1.141879e+05</td>
      <td>5.709397e+05</td>
      <td>2.854698e+06</td>
      <td>1.427349e+07</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>3.264030e+05</td>
      <td>3.237003e+05</td>
      <td>3.222450e+05</td>
      <td>3.205818e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>8258827.5</td>
      <td>8.160075e+06</td>
      <td>8.092508e+06</td>
      <td>8.056125e+06</td>
      <td>8.014545e+06</td>
      <td>3.246566e+05</td>
      <td>1.623283e+06</td>
      <td>8.116416e+06</td>
      <td>4.058208e+07</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>4.590031e+05</td>
      <td>4.737453e+05</td>
      <td>4.793627e+05</td>
      <td>4.683789e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>10920650.0</td>
      <td>1.147508e+07</td>
      <td>1.184363e+07</td>
      <td>1.198407e+07</td>
      <td>1.170947e+07</td>
      <td>4.634632e+05</td>
      <td>2.317316e+06</td>
      <td>1.158658e+07</td>
      <td>5.793290e+07</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>1.635341e+05</td>
      <td>1.584897e+05</td>
      <td>1.549113e+05</td>
      <td>1.532609e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>4196555.0</td>
      <td>4.088352e+06</td>
      <td>3.962243e+06</td>
      <td>3.872783e+06</td>
      <td>3.831522e+06</td>
      <td>1.596116e+05</td>
      <td>7.980582e+05</td>
      <td>3.990291e+06</td>
      <td>1.995146e+07</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>9.563000e+04</td>
      <td>9.394070e+04</td>
      <td>8.333360e+04</td>
      <td>7.700550e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2370670.0</td>
      <td>2.390750e+06</td>
      <td>2.348518e+06</td>
      <td>2.083340e+06</td>
      <td>1.925138e+06</td>
      <td>8.894732e+04</td>
      <td>4.447366e+05</td>
      <td>2.223683e+06</td>
      <td>1.111842e+07</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>1.217563e+05</td>
      <td>8.445630e+04</td>
      <td>1.110490e+05</td>
      <td>1.021563e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3316000.0</td>
      <td>3.043908e+06</td>
      <td>2.111408e+06</td>
      <td>2.776225e+06</td>
      <td>2.553908e+06</td>
      <td>1.104116e+05</td>
      <td>5.520579e+05</td>
      <td>2.760290e+06</td>
      <td>1.380145e+07</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1.052288e+06</td>
      <td>1.087030e+06</td>
      <td>1.118850e+06</td>
      <td>1.083100e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>26485240.0</td>
      <td>2.630719e+07</td>
      <td>2.717574e+07</td>
      <td>2.797125e+07</td>
      <td>2.707751e+07</td>
      <td>1.080135e+06</td>
      <td>5.400677e+06</td>
      <td>2.700339e+07</td>
      <td>1.350169e+08</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>1.232328e+05</td>
      <td>1.226563e+05</td>
      <td>1.252385e+05</td>
      <td>1.224538e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3048565.0</td>
      <td>3.080820e+06</td>
      <td>3.066408e+06</td>
      <td>3.130962e+06</td>
      <td>3.061345e+06</td>
      <td>1.231048e+05</td>
      <td>6.155240e+05</td>
      <td>3.077620e+06</td>
      <td>1.538810e+07</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>1.427237e+05</td>
      <td>1.625746e+05</td>
      <td>1.538908e+05</td>
      <td>1.562154e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3731555.0</td>
      <td>3.568093e+06</td>
      <td>4.064365e+06</td>
      <td>3.847270e+06</td>
      <td>3.905385e+06</td>
      <td>1.529333e+05</td>
      <td>7.646667e+05</td>
      <td>3.823334e+06</td>
      <td>1.911667e+07</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>3.813618e+05</td>
      <td>4.060833e+05</td>
      <td>3.934042e+05</td>
      <td>4.247551e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>9588232.5</td>
      <td>9.534045e+06</td>
      <td>1.015208e+07</td>
      <td>9.835105e+06</td>
      <td>1.061888e+07</td>
      <td>3.978267e+05</td>
      <td>1.989134e+06</td>
      <td>9.945668e+06</td>
      <td>4.972834e+07</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1.524292e+06</td>
      <td>1.609862e+06</td>
      <td>1.606048e+06</td>
      <td>1.556226e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>38945265.0</td>
      <td>3.810731e+07</td>
      <td>4.024656e+07</td>
      <td>4.015120e+07</td>
      <td>3.890564e+07</td>
      <td>1.570848e+06</td>
      <td>7.854239e+06</td>
      <td>3.927120e+07</td>
      <td>1.963560e+08</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>8.344230e+04</td>
      <td>8.459620e+04</td>
      <td>8.394330e+04</td>
      <td>8.293700e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2070582.5</td>
      <td>2.086058e+06</td>
      <td>2.114905e+06</td>
      <td>2.098582e+06</td>
      <td>2.073425e+06</td>
      <td>8.354842e+04</td>
      <td>4.177421e+05</td>
      <td>2.088710e+06</td>
      <td>1.044355e+07</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1.703328e+06</td>
      <td>1.714466e+06</td>
      <td>1.702989e+06</td>
      <td>1.553836e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>38856350.0</td>
      <td>4.258319e+07</td>
      <td>4.286164e+07</td>
      <td>4.257473e+07</td>
      <td>3.884589e+07</td>
      <td>1.645774e+06</td>
      <td>8.228872e+06</td>
      <td>4.114436e+07</td>
      <td>2.057218e+08</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>4.983830e+04</td>
      <td>4.999120e+04</td>
      <td>4.941410e+04</td>
      <td>4.915200e+04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1145967.5</td>
      <td>1.245958e+06</td>
      <td>1.249780e+06</td>
      <td>1.235352e+06</td>
      <td>1.228800e+06</td>
      <td>4.884686e+04</td>
      <td>2.442343e+05</td>
      <td>1.221172e+06</td>
      <td>6.105858e+06</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>4.386620e+05</td>
      <td>3.362555e+05</td>
      <td>4.121775e+05</td>
      <td>3.501365e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>9118200.0</td>
      <td>1.096655e+07</td>
      <td>8.406388e+06</td>
      <td>1.030444e+07</td>
      <td>8.753412e+06</td>
      <td>3.803919e+05</td>
      <td>1.901960e+06</td>
      <td>9.509798e+06</td>
      <td>4.754899e+07</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1.365174e+06</td>
      <td>1.360552e+06</td>
      <td>1.336231e+06</td>
      <td>1.318431e+06</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>34543610.0</td>
      <td>3.412934e+07</td>
      <td>3.401379e+07</td>
      <td>3.340578e+07</td>
      <td>3.296078e+07</td>
      <td>1.352426e+06</td>
      <td>6.762132e+06</td>
      <td>3.381066e+07</td>
      <td>1.690533e+08</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>Total</td>
      <td>23829994.0</td>
      <td>2.391723e+07</td>
      <td>2.407593e+07</td>
      <td>2.404256e+07</td>
      <td>2.344603e+07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>595749850.0</td>
      <td>5.979306e+08</td>
      <td>6.018983e+08</td>
      <td>6.010640e+08</td>
      <td>5.861507e+08</td>
      <td>2.386235e+07</td>
      <td>1.193117e+08</td>
      <td>5.965587e+08</td>
      <td>2.982794e+09</td>
    </tr>
    <tr>
      <th>24</th>
      <td>NaN</td>
      <td>mean</td>
      <td>948478.0</td>
      <td>9.522272e+05</td>
      <td>9.590840e+05</td>
      <td>9.575896e+05</td>
      <td>9.316100e+05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>23711950.0</td>
      <td>2.380568e+07</td>
      <td>2.397710e+07</td>
      <td>2.393974e+07</td>
      <td>2.329025e+07</td>
      <td>9.497978e+05</td>
      <td>4.748989e+06</td>
      <td>2.374494e+07</td>
      <td>1.187247e+08</td>
    </tr>
  </tbody>
</table>
</div>



### FAOSTAT Data to File


```python
outfile = "/Users/jnapolitano/Projects/wattime-takehome/wattime-takehome/data/FAOSTAT_DATA.csv"

faostat_emissions_df.to_csv(outfile)
```

## FaoSTAT PLOTS

### FAOSTAT Hectare Estimates Bar Plot


```python
faostat_emissions_df.plot(kind = "barh", x = 'country_name', y = [2015, 2016, 2017, 2018, 2019], xlabel = "Country Name", ylabel = "Tonnes CH4", figsize = (10,5))
```




    <AxesSubplot:ylabel='Country Name'>




    
![png](data_exploration_files/data_exploration_55_1.png)
    


### FAOSTAT Density Plot


```python
faostat_emissions_df.plot(rot = 90, kind = "density",y = [2015, 2016, 2017, 2018, 2019], figsize = (15,5)) 
```




    <AxesSubplot:ylabel='Density'>




    
![png](data_exploration_files/data_exploration_57_1.png)
    


The density plot is fairly consistent.  There is nearly no variation between nations and in total.  The 2020 data may show otherwise as the Malaysian data shows.  

## Join Df's by ISO3 Country

### Drop totals and means from the original df.

Because I am joining on iso3 country country code if the totals and means are located at different indexes we may experience merge and calculation errors


```python
faostat_emissions_df = faostat_emissions_df[(faostat_emissions_df["country_name"] != "Total") & (faostat_emissions_df['country_name'] != 'mean')].copy()
```


```python
malaysia_emissions_df = malaysia_emissions_df[(malaysia_emissions_df["country_name"] != "Total") & (malaysia_emissions_df['country_name'] != 'mean')].copy()
```


```python
faostat_emissions_df
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
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>2020</th>
      <th>2021</th>
      <th>tCO2_2015</th>
      <th>tCO2_2016</th>
      <th>tCO2_2017</th>
      <th>tCO2_2018</th>
      <th>tCO2_2019</th>
      <th>Mean_CH4</th>
      <th>Total_CH4</th>
      <th>Mean_CO2</th>
      <th>Total_CO2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1093480.4</td>
      <td>1154531.0</td>
      <td>1144591.0</td>
      <td>1144745.4</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>28282335.0</td>
      <td>27337010.0</td>
      <td>28863275.0</td>
      <td>28614775.0</td>
      <td>28618635.0</td>
      <td>1133728.24</td>
      <td>5668641.2</td>
      <td>28343206.0</td>
      <td>141716030.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>126278.2</td>
      <td>130322.9</td>
      <td>121615.2</td>
      <td>111084.8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3472757.5</td>
      <td>3156955.0</td>
      <td>3258072.5</td>
      <td>3040380.0</td>
      <td>2777120.0</td>
      <td>125642.28</td>
      <td>628211.4</td>
      <td>3141057.0</td>
      <td>15705285.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5399920.0</td>
      <td>5400129.0</td>
      <td>5302173.1</td>
      <td>5214454.7</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>135164847.5</td>
      <td>134998000.0</td>
      <td>135003225.0</td>
      <td>132554327.5</td>
      <td>130361367.5</td>
      <td>5344654.14</td>
      <td>26723270.7</td>
      <td>133616353.5</td>
      <td>668081767.5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>55073.1</td>
      <td>54232.4</td>
      <td>52925.0</td>
      <td>52098.5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1377055.0</td>
      <td>1376827.5</td>
      <td>1355810.0</td>
      <td>1323125.0</td>
      <td>1302462.5</td>
      <td>53882.24</td>
      <td>269411.2</td>
      <td>1347056.0</td>
      <td>6735280.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2387656.4</td>
      <td>2425290.6</td>
      <td>2405613.8</td>
      <td>2257604.3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>60198837.5</td>
      <td>59691410.0</td>
      <td>60632265.0</td>
      <td>60140345.0</td>
      <td>56440107.5</td>
      <td>2376823.72</td>
      <td>11884118.6</td>
      <td>59420593.0</td>
      <td>297102965.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4559136.4</td>
      <td>4620790.8</td>
      <td>4661154.9</td>
      <td>4621416.8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>114506210.0</td>
      <td>113978410.0</td>
      <td>115519770.0</td>
      <td>116528872.5</td>
      <td>115535420.0</td>
      <td>4608549.46</td>
      <td>23042747.3</td>
      <td>115213736.5</td>
      <td>576068682.5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>131008.5</td>
      <td>87233.6</td>
      <td>93936.6</td>
      <td>96103.4</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2912167.5</td>
      <td>3275212.5</td>
      <td>2180840.0</td>
      <td>2348415.0</td>
      <td>2402585.0</td>
      <td>104953.76</td>
      <td>524768.8</td>
      <td>2623844.0</td>
      <td>13119220.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>118003.0</td>
      <td>118003.0</td>
      <td>109463.8</td>
      <td>110895.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2864370.0</td>
      <td>2950075.0</td>
      <td>2950075.0</td>
      <td>2736595.0</td>
      <td>2772377.5</td>
      <td>114187.94</td>
      <td>570939.7</td>
      <td>2854698.5</td>
      <td>14273492.5</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>326403.0</td>
      <td>323700.3</td>
      <td>322245.0</td>
      <td>320581.8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>8258827.5</td>
      <td>8160075.0</td>
      <td>8092507.5</td>
      <td>8056125.0</td>
      <td>8014545.0</td>
      <td>324656.64</td>
      <td>1623283.2</td>
      <td>8116416.0</td>
      <td>40582080.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>459003.1</td>
      <td>473745.3</td>
      <td>479362.7</td>
      <td>468378.9</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>10920650.0</td>
      <td>11475077.5</td>
      <td>11843632.5</td>
      <td>11984067.5</td>
      <td>11709472.5</td>
      <td>463463.20</td>
      <td>2317316.0</td>
      <td>11586580.0</td>
      <td>57932900.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>163534.1</td>
      <td>158489.7</td>
      <td>154911.3</td>
      <td>153260.9</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>4196555.0</td>
      <td>4088352.5</td>
      <td>3962242.5</td>
      <td>3872782.5</td>
      <td>3831522.5</td>
      <td>159611.64</td>
      <td>798058.2</td>
      <td>3990291.0</td>
      <td>19951455.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>95630.0</td>
      <td>93940.7</td>
      <td>83333.6</td>
      <td>77005.5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2370670.0</td>
      <td>2390750.0</td>
      <td>2348517.5</td>
      <td>2083340.0</td>
      <td>1925137.5</td>
      <td>88947.32</td>
      <td>444736.6</td>
      <td>2223683.0</td>
      <td>11118415.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>121756.3</td>
      <td>84456.3</td>
      <td>111049.0</td>
      <td>102156.3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3316000.0</td>
      <td>3043907.5</td>
      <td>2111407.5</td>
      <td>2776225.0</td>
      <td>2553907.5</td>
      <td>110411.58</td>
      <td>552057.9</td>
      <td>2760289.5</td>
      <td>13801447.5</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1052287.7</td>
      <td>1087029.5</td>
      <td>1118850.0</td>
      <td>1083100.3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>26485240.0</td>
      <td>26307192.5</td>
      <td>27175737.5</td>
      <td>27971250.0</td>
      <td>27077507.5</td>
      <td>1080135.42</td>
      <td>5400677.1</td>
      <td>27003385.5</td>
      <td>135016927.5</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>123232.8</td>
      <td>122656.3</td>
      <td>125238.5</td>
      <td>122453.8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3048565.0</td>
      <td>3080820.0</td>
      <td>3066407.5</td>
      <td>3130962.5</td>
      <td>3061345.0</td>
      <td>123104.80</td>
      <td>615524.0</td>
      <td>3077620.0</td>
      <td>15388100.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>142723.7</td>
      <td>162574.6</td>
      <td>153890.8</td>
      <td>156215.4</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3731555.0</td>
      <td>3568092.5</td>
      <td>4064365.0</td>
      <td>3847270.0</td>
      <td>3905385.0</td>
      <td>152933.34</td>
      <td>764666.7</td>
      <td>3823333.5</td>
      <td>19116667.5</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>381361.8</td>
      <td>406083.3</td>
      <td>393404.2</td>
      <td>424755.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>9588232.5</td>
      <td>9534045.0</td>
      <td>10152082.5</td>
      <td>9835105.0</td>
      <td>10618877.5</td>
      <td>397826.74</td>
      <td>1989133.7</td>
      <td>9945668.5</td>
      <td>49728342.5</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1524292.5</td>
      <td>1609862.5</td>
      <td>1606047.8</td>
      <td>1556225.8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>38945265.0</td>
      <td>38107312.5</td>
      <td>40246562.5</td>
      <td>40151195.0</td>
      <td>38905645.0</td>
      <td>1570847.84</td>
      <td>7854239.2</td>
      <td>39271196.0</td>
      <td>196355980.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>83442.3</td>
      <td>84596.2</td>
      <td>83943.3</td>
      <td>82937.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2070582.5</td>
      <td>2086057.5</td>
      <td>2114905.0</td>
      <td>2098582.5</td>
      <td>2073425.0</td>
      <td>83548.42</td>
      <td>417742.1</td>
      <td>2088710.5</td>
      <td>10443552.5</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1703327.7</td>
      <td>1714465.6</td>
      <td>1702989.1</td>
      <td>1553835.5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>38856350.0</td>
      <td>42583192.5</td>
      <td>42861640.0</td>
      <td>42574727.5</td>
      <td>38845887.5</td>
      <td>1645774.38</td>
      <td>8228871.9</td>
      <td>41144359.5</td>
      <td>205721797.5</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>49838.3</td>
      <td>49991.2</td>
      <td>49414.1</td>
      <td>49152.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1145967.5</td>
      <td>1245957.5</td>
      <td>1249780.0</td>
      <td>1235352.5</td>
      <td>1228800.0</td>
      <td>48846.86</td>
      <td>244234.3</td>
      <td>1221171.5</td>
      <td>6105857.5</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>438662.0</td>
      <td>336255.5</td>
      <td>412177.5</td>
      <td>350136.5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>9118200.0</td>
      <td>10966550.0</td>
      <td>8406387.5</td>
      <td>10304437.5</td>
      <td>8753412.5</td>
      <td>380391.90</td>
      <td>1901959.5</td>
      <td>9509797.5</td>
      <td>47548987.5</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1365173.8</td>
      <td>1360551.6</td>
      <td>1336231.2</td>
      <td>1318431.1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>34543610.0</td>
      <td>34129345.0</td>
      <td>34013790.0</td>
      <td>33405780.0</td>
      <td>32960777.5</td>
      <td>1352426.42</td>
      <td>6762132.1</td>
      <td>33810660.5</td>
      <td>169053302.5</td>
    </tr>
  </tbody>
</table>
</div>




```python
malaysia_emissions_df
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
      <th>tCO2_2015</th>
      <th>tCO2_2016</th>
      <th>tCO2_2017</th>
      <th>tCO2_2018</th>
      <th>tCO2_2019</th>
      <th>Mean_CH4</th>
      <th>Total_CH4</th>
      <th>Mean_CO2</th>
      <th>Total_CO2</th>
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
      <td>5.861049e+07</td>
      <td>5.695395e+07</td>
      <td>5.247394e+07</td>
      <td>5.353076e+07</td>
      <td>5.177463e+07</td>
      <td>2.186750e+06</td>
      <td>1.093375e+07</td>
      <td>5.466875e+07</td>
      <td>2.733438e+08</td>
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
      <td>8.525583e+06</td>
      <td>7.760473e+06</td>
      <td>9.312934e+06</td>
      <td>9.292575e+06</td>
      <td>8.236783e+06</td>
      <td>3.450268e+05</td>
      <td>1.725134e+06</td>
      <td>8.625670e+06</td>
      <td>4.312835e+07</td>
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
      <td>1.533412e+08</td>
      <td>1.464883e+08</td>
      <td>1.588768e+08</td>
      <td>1.353491e+08</td>
      <td>1.400838e+08</td>
      <td>5.873113e+06</td>
      <td>2.936556e+07</td>
      <td>1.468278e+08</td>
      <td>7.341391e+08</td>
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
      <td>2.853661e+05</td>
      <td>3.337007e+05</td>
      <td>3.043248e+05</td>
      <td>3.513524e+05</td>
      <td>2.870810e+05</td>
      <td>1.249460e+04</td>
      <td>6.247300e+04</td>
      <td>3.123650e+05</td>
      <td>1.561825e+06</td>
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
      <td>3.209122e+07</td>
      <td>2.557824e+07</td>
      <td>2.403832e+07</td>
      <td>2.942454e+07</td>
      <td>3.166670e+07</td>
      <td>1.142392e+06</td>
      <td>5.711960e+06</td>
      <td>2.855980e+07</td>
      <td>1.427990e+08</td>
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
      <td>1.554972e+08</td>
      <td>1.327353e+08</td>
      <td>1.557113e+08</td>
      <td>1.647450e+08</td>
      <td>1.875389e+08</td>
      <td>6.369821e+06</td>
      <td>3.184910e+07</td>
      <td>1.592455e+08</td>
      <td>7.962276e+08</td>
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
      <td>2.193602e+06</td>
      <td>2.295030e+06</td>
      <td>2.405054e+06</td>
      <td>2.218936e+06</td>
      <td>2.375050e+06</td>
      <td>9.190138e+04</td>
      <td>4.595069e+05</td>
      <td>2.297534e+06</td>
      <td>1.148767e+07</td>
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
      <td>1.248992e+06</td>
      <td>1.234446e+06</td>
      <td>1.360920e+06</td>
      <td>1.117475e+06</td>
      <td>1.141729e+06</td>
      <td>4.882850e+04</td>
      <td>2.441425e+05</td>
      <td>1.220712e+06</td>
      <td>6.103562e+06</td>
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
      <td>5.763662e+06</td>
      <td>5.710333e+06</td>
      <td>6.772337e+06</td>
      <td>3.870631e+06</td>
      <td>5.830141e+06</td>
      <td>2.235768e+05</td>
      <td>1.117884e+06</td>
      <td>5.589421e+06</td>
      <td>2.794710e+07</td>
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
      <td>1.238675e+07</td>
      <td>1.432925e+07</td>
      <td>1.129261e+07</td>
      <td>1.398153e+07</td>
      <td>1.486819e+07</td>
      <td>5.348666e+05</td>
      <td>2.674333e+06</td>
      <td>1.337166e+07</td>
      <td>6.685832e+07</td>
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
      <td>3.629695e+06</td>
      <td>3.186493e+06</td>
      <td>3.658056e+06</td>
      <td>3.233858e+06</td>
      <td>3.319455e+06</td>
      <td>1.362205e+05</td>
      <td>6.811023e+05</td>
      <td>3.405512e+06</td>
      <td>1.702756e+07</td>
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
      <td>4.152924e+05</td>
      <td>4.241102e+05</td>
      <td>2.920158e+05</td>
      <td>2.524186e+05</td>
      <td>3.652645e+05</td>
      <td>1.399281e+04</td>
      <td>6.996406e+04</td>
      <td>3.498203e+05</td>
      <td>1.749102e+06</td>
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
      <td>2.076407e+06</td>
      <td>2.529358e+06</td>
      <td>1.477960e+06</td>
      <td>2.254728e+06</td>
      <td>2.119022e+06</td>
      <td>8.365981e+04</td>
      <td>4.182990e+05</td>
      <td>2.091495e+06</td>
      <td>1.045748e+07</td>
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
      <td>2.830206e+07</td>
      <td>3.227014e+07</td>
      <td>3.012923e+07</td>
      <td>3.431117e+07</td>
      <td>3.142221e+07</td>
      <td>1.251478e+06</td>
      <td>6.257392e+06</td>
      <td>3.128696e+07</td>
      <td>1.564348e+08</td>
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
      <td>2.643498e+06</td>
      <td>2.775123e+06</td>
      <td>2.778227e+06</td>
      <td>2.666313e+06</td>
      <td>2.640717e+06</td>
      <td>1.080310e+05</td>
      <td>5.401551e+05</td>
      <td>2.700775e+06</td>
      <td>1.350388e+07</td>
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
      <td>2.518697e+06</td>
      <td>1.666790e+06</td>
      <td>2.020325e+06</td>
      <td>2.300188e+06</td>
      <td>2.910588e+06</td>
      <td>9.133271e+04</td>
      <td>4.566635e+05</td>
      <td>2.283318e+06</td>
      <td>1.141659e+07</td>
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
      <td>1.213108e+07</td>
      <td>1.486480e+07</td>
      <td>1.343160e+07</td>
      <td>1.133074e+07</td>
      <td>1.632137e+07</td>
      <td>5.446368e+05</td>
      <td>2.723184e+06</td>
      <td>1.361592e+07</td>
      <td>6.807960e+07</td>
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
      <td>8.580052e+06</td>
      <td>1.018389e+07</td>
      <td>9.592074e+06</td>
      <td>1.043803e+07</td>
      <td>8.961374e+06</td>
      <td>3.820433e+05</td>
      <td>1.910216e+06</td>
      <td>9.551082e+06</td>
      <td>4.775541e+07</td>
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
      <td>2.858041e+06</td>
      <td>2.294413e+06</td>
      <td>2.713641e+06</td>
      <td>2.165645e+06</td>
      <td>2.413765e+06</td>
      <td>9.956405e+04</td>
      <td>4.978202e+05</td>
      <td>2.489101e+06</td>
      <td>1.244551e+07</td>
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
      <td>3.484495e+07</td>
      <td>4.452483e+07</td>
      <td>2.911748e+07</td>
      <td>2.291644e+07</td>
      <td>3.262615e+07</td>
      <td>1.312239e+06</td>
      <td>6.561194e+06</td>
      <td>3.280597e+07</td>
      <td>1.640298e+08</td>
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
      <td>1.966739e+06</td>
      <td>2.022287e+06</td>
      <td>2.176408e+06</td>
      <td>2.034538e+06</td>
      <td>2.247717e+06</td>
      <td>8.358152e+04</td>
      <td>4.179076e+05</td>
      <td>2.089538e+06</td>
      <td>1.044769e+07</td>
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
      <td>4.028310e+06</td>
      <td>4.046440e+06</td>
      <td>4.211999e+06</td>
      <td>4.143136e+06</td>
      <td>4.228377e+06</td>
      <td>1.652661e+05</td>
      <td>8.263305e+05</td>
      <td>4.131652e+06</td>
      <td>2.065826e+07</td>
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
      <td>3.365033e+07</td>
      <td>3.709441e+07</td>
      <td>3.516092e+07</td>
      <td>3.293637e+07</td>
      <td>3.174377e+07</td>
      <td>1.364686e+06</td>
      <td>6.823432e+06</td>
      <td>3.411716e+07</td>
      <td>1.705858e+08</td>
    </tr>
  </tbody>
</table>
</div>




```python
merged_df = faostat_emissions_df.merge(malaysia_emissions_df,suffixes=('_FAOSTAT', '_TRACE'), on='iso3_country', how='left', sort=False)
```

### Dropping 2020 and 2021 from the data sets

I will only compare data compiled from the same year. 


```python
merged_df.drop([2020, 2021, "tCH4_2020","tCH4_2021"], axis = 1, inplace = True)
```


```python
merged_df
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
      <th>country_name_FAOSTAT</th>
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>tCO2_2015_FAOSTAT</th>
      <th>tCO2_2016_FAOSTAT</th>
      <th>tCO2_2017_FAOSTAT</th>
      <th>...</th>
      <th>tCH4_2019</th>
      <th>tCO2_2015_TRACE</th>
      <th>tCO2_2016_TRACE</th>
      <th>tCO2_2017_TRACE</th>
      <th>tCO2_2018_TRACE</th>
      <th>tCO2_2019_TRACE</th>
      <th>Mean_CH4_TRACE</th>
      <th>Total_CH4_TRACE</th>
      <th>Mean_CO2_TRACE</th>
      <th>Total_CO2_TRACE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1093480.4</td>
      <td>1154531.0</td>
      <td>1144591.0</td>
      <td>1144745.4</td>
      <td>28282335.0</td>
      <td>27337010.0</td>
      <td>28863275.0</td>
      <td>...</td>
      <td>2.070985e+06</td>
      <td>5.861049e+07</td>
      <td>5.695395e+07</td>
      <td>5.247394e+07</td>
      <td>5.353076e+07</td>
      <td>5.177463e+07</td>
      <td>2.186750e+06</td>
      <td>1.093375e+07</td>
      <td>5.466875e+07</td>
      <td>2.733438e+08</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>126278.2</td>
      <td>130322.9</td>
      <td>121615.2</td>
      <td>111084.8</td>
      <td>3472757.5</td>
      <td>3156955.0</td>
      <td>3258072.5</td>
      <td>...</td>
      <td>3.294713e+05</td>
      <td>8.525583e+06</td>
      <td>7.760473e+06</td>
      <td>9.312934e+06</td>
      <td>9.292575e+06</td>
      <td>8.236783e+06</td>
      <td>3.450268e+05</td>
      <td>1.725134e+06</td>
      <td>8.625670e+06</td>
      <td>4.312835e+07</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5399920.0</td>
      <td>5400129.0</td>
      <td>5302173.1</td>
      <td>5214454.7</td>
      <td>135164847.5</td>
      <td>134998000.0</td>
      <td>135003225.0</td>
      <td>...</td>
      <td>5.603352e+06</td>
      <td>1.533412e+08</td>
      <td>1.464883e+08</td>
      <td>1.588768e+08</td>
      <td>1.353491e+08</td>
      <td>1.400838e+08</td>
      <td>5.873113e+06</td>
      <td>2.936556e+07</td>
      <td>1.468278e+08</td>
      <td>7.341391e+08</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>55073.1</td>
      <td>54232.4</td>
      <td>52925.0</td>
      <td>52098.5</td>
      <td>1377055.0</td>
      <td>1376827.5</td>
      <td>1355810.0</td>
      <td>...</td>
      <td>1.148324e+04</td>
      <td>2.853661e+05</td>
      <td>3.337007e+05</td>
      <td>3.043248e+05</td>
      <td>3.513524e+05</td>
      <td>2.870810e+05</td>
      <td>1.249460e+04</td>
      <td>6.247300e+04</td>
      <td>3.123650e+05</td>
      <td>1.561825e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2387656.4</td>
      <td>2425290.6</td>
      <td>2405613.8</td>
      <td>2257604.3</td>
      <td>60198837.5</td>
      <td>59691410.0</td>
      <td>60632265.0</td>
      <td>...</td>
      <td>1.266668e+06</td>
      <td>3.209122e+07</td>
      <td>2.557824e+07</td>
      <td>2.403832e+07</td>
      <td>2.942454e+07</td>
      <td>3.166670e+07</td>
      <td>1.142392e+06</td>
      <td>5.711960e+06</td>
      <td>2.855980e+07</td>
      <td>1.427990e+08</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4559136.4</td>
      <td>4620790.8</td>
      <td>4661154.9</td>
      <td>4621416.8</td>
      <td>114506210.0</td>
      <td>113978410.0</td>
      <td>115519770.0</td>
      <td>...</td>
      <td>7.501556e+06</td>
      <td>1.554972e+08</td>
      <td>1.327353e+08</td>
      <td>1.557113e+08</td>
      <td>1.647450e+08</td>
      <td>1.875389e+08</td>
      <td>6.369821e+06</td>
      <td>3.184910e+07</td>
      <td>1.592455e+08</td>
      <td>7.962276e+08</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>131008.5</td>
      <td>87233.6</td>
      <td>93936.6</td>
      <td>96103.4</td>
      <td>2912167.5</td>
      <td>3275212.5</td>
      <td>2180840.0</td>
      <td>...</td>
      <td>9.500199e+04</td>
      <td>2.193602e+06</td>
      <td>2.295030e+06</td>
      <td>2.405054e+06</td>
      <td>2.218936e+06</td>
      <td>2.375050e+06</td>
      <td>9.190138e+04</td>
      <td>4.595069e+05</td>
      <td>2.297534e+06</td>
      <td>1.148767e+07</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>118003.0</td>
      <td>118003.0</td>
      <td>109463.8</td>
      <td>110895.1</td>
      <td>2864370.0</td>
      <td>2950075.0</td>
      <td>2950075.0</td>
      <td>...</td>
      <td>4.566914e+04</td>
      <td>1.248992e+06</td>
      <td>1.234446e+06</td>
      <td>1.360920e+06</td>
      <td>1.117475e+06</td>
      <td>1.141729e+06</td>
      <td>4.882850e+04</td>
      <td>2.441425e+05</td>
      <td>1.220712e+06</td>
      <td>6.103562e+06</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>326403.0</td>
      <td>323700.3</td>
      <td>322245.0</td>
      <td>320581.8</td>
      <td>8258827.5</td>
      <td>8160075.0</td>
      <td>8092507.5</td>
      <td>...</td>
      <td>2.332056e+05</td>
      <td>5.763662e+06</td>
      <td>5.710333e+06</td>
      <td>6.772337e+06</td>
      <td>3.870631e+06</td>
      <td>5.830141e+06</td>
      <td>2.235768e+05</td>
      <td>1.117884e+06</td>
      <td>5.589421e+06</td>
      <td>2.794710e+07</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>459003.1</td>
      <td>473745.3</td>
      <td>479362.7</td>
      <td>468378.9</td>
      <td>10920650.0</td>
      <td>11475077.5</td>
      <td>11843632.5</td>
      <td>...</td>
      <td>5.947277e+05</td>
      <td>1.238675e+07</td>
      <td>1.432925e+07</td>
      <td>1.129261e+07</td>
      <td>1.398153e+07</td>
      <td>1.486819e+07</td>
      <td>5.348666e+05</td>
      <td>2.674333e+06</td>
      <td>1.337166e+07</td>
      <td>6.685832e+07</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>163534.1</td>
      <td>158489.7</td>
      <td>154911.3</td>
      <td>153260.9</td>
      <td>4196555.0</td>
      <td>4088352.5</td>
      <td>3962242.5</td>
      <td>...</td>
      <td>1.327782e+05</td>
      <td>3.629695e+06</td>
      <td>3.186493e+06</td>
      <td>3.658056e+06</td>
      <td>3.233858e+06</td>
      <td>3.319455e+06</td>
      <td>1.362205e+05</td>
      <td>6.811023e+05</td>
      <td>3.405512e+06</td>
      <td>1.702756e+07</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>95630.0</td>
      <td>93940.7</td>
      <td>83333.6</td>
      <td>77005.5</td>
      <td>2370670.0</td>
      <td>2390750.0</td>
      <td>2348517.5</td>
      <td>...</td>
      <td>1.461058e+04</td>
      <td>4.152924e+05</td>
      <td>4.241102e+05</td>
      <td>2.920158e+05</td>
      <td>2.524186e+05</td>
      <td>3.652645e+05</td>
      <td>1.399281e+04</td>
      <td>6.996406e+04</td>
      <td>3.498203e+05</td>
      <td>1.749102e+06</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>121756.3</td>
      <td>84456.3</td>
      <td>111049.0</td>
      <td>102156.3</td>
      <td>3316000.0</td>
      <td>3043907.5</td>
      <td>2111407.5</td>
      <td>...</td>
      <td>8.476088e+04</td>
      <td>2.076407e+06</td>
      <td>2.529358e+06</td>
      <td>1.477960e+06</td>
      <td>2.254728e+06</td>
      <td>2.119022e+06</td>
      <td>8.365981e+04</td>
      <td>4.182990e+05</td>
      <td>2.091495e+06</td>
      <td>1.045748e+07</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1052287.7</td>
      <td>1087029.5</td>
      <td>1118850.0</td>
      <td>1083100.3</td>
      <td>26485240.0</td>
      <td>26307192.5</td>
      <td>27175737.5</td>
      <td>...</td>
      <td>1.256888e+06</td>
      <td>2.830206e+07</td>
      <td>3.227014e+07</td>
      <td>3.012923e+07</td>
      <td>3.431117e+07</td>
      <td>3.142221e+07</td>
      <td>1.251478e+06</td>
      <td>6.257392e+06</td>
      <td>3.128696e+07</td>
      <td>1.564348e+08</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>123232.8</td>
      <td>122656.3</td>
      <td>125238.5</td>
      <td>122453.8</td>
      <td>3048565.0</td>
      <td>3080820.0</td>
      <td>3066407.5</td>
      <td>...</td>
      <td>1.056287e+05</td>
      <td>2.643498e+06</td>
      <td>2.775123e+06</td>
      <td>2.778227e+06</td>
      <td>2.666313e+06</td>
      <td>2.640717e+06</td>
      <td>1.080310e+05</td>
      <td>5.401551e+05</td>
      <td>2.700775e+06</td>
      <td>1.350388e+07</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>142723.7</td>
      <td>162574.6</td>
      <td>153890.8</td>
      <td>156215.4</td>
      <td>3731555.0</td>
      <td>3568092.5</td>
      <td>4064365.0</td>
      <td>...</td>
      <td>1.164235e+05</td>
      <td>2.518697e+06</td>
      <td>1.666790e+06</td>
      <td>2.020325e+06</td>
      <td>2.300188e+06</td>
      <td>2.910588e+06</td>
      <td>9.133271e+04</td>
      <td>4.566635e+05</td>
      <td>2.283318e+06</td>
      <td>1.141659e+07</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>381361.8</td>
      <td>406083.3</td>
      <td>393404.2</td>
      <td>424755.1</td>
      <td>9588232.5</td>
      <td>9534045.0</td>
      <td>10152082.5</td>
      <td>...</td>
      <td>6.528548e+05</td>
      <td>1.213108e+07</td>
      <td>1.486480e+07</td>
      <td>1.343160e+07</td>
      <td>1.133074e+07</td>
      <td>1.632137e+07</td>
      <td>5.446368e+05</td>
      <td>2.723184e+06</td>
      <td>1.361592e+07</td>
      <td>6.807960e+07</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1524292.5</td>
      <td>1609862.5</td>
      <td>1606047.8</td>
      <td>1556225.8</td>
      <td>38945265.0</td>
      <td>38107312.5</td>
      <td>40246562.5</td>
      <td>...</td>
      <td>3.584550e+05</td>
      <td>8.580052e+06</td>
      <td>1.018389e+07</td>
      <td>9.592074e+06</td>
      <td>1.043803e+07</td>
      <td>8.961374e+06</td>
      <td>3.820433e+05</td>
      <td>1.910216e+06</td>
      <td>9.551082e+06</td>
      <td>4.775541e+07</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>83442.3</td>
      <td>84596.2</td>
      <td>83943.3</td>
      <td>82937.0</td>
      <td>2070582.5</td>
      <td>2086057.5</td>
      <td>2114905.0</td>
      <td>...</td>
      <td>9.655062e+04</td>
      <td>2.858041e+06</td>
      <td>2.294413e+06</td>
      <td>2.713641e+06</td>
      <td>2.165645e+06</td>
      <td>2.413765e+06</td>
      <td>9.956405e+04</td>
      <td>4.978202e+05</td>
      <td>2.489101e+06</td>
      <td>1.244551e+07</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1703327.7</td>
      <td>1714465.6</td>
      <td>1702989.1</td>
      <td>1553835.5</td>
      <td>38856350.0</td>
      <td>42583192.5</td>
      <td>42861640.0</td>
      <td>...</td>
      <td>1.305046e+06</td>
      <td>3.484495e+07</td>
      <td>4.452483e+07</td>
      <td>2.911748e+07</td>
      <td>2.291644e+07</td>
      <td>3.262615e+07</td>
      <td>1.312239e+06</td>
      <td>6.561194e+06</td>
      <td>3.280597e+07</td>
      <td>1.640298e+08</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>49838.3</td>
      <td>49991.2</td>
      <td>49414.1</td>
      <td>49152.0</td>
      <td>1145967.5</td>
      <td>1245957.5</td>
      <td>1249780.0</td>
      <td>...</td>
      <td>8.990870e+04</td>
      <td>1.966739e+06</td>
      <td>2.022287e+06</td>
      <td>2.176408e+06</td>
      <td>2.034538e+06</td>
      <td>2.247717e+06</td>
      <td>8.358152e+04</td>
      <td>4.179076e+05</td>
      <td>2.089538e+06</td>
      <td>1.044769e+07</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>438662.0</td>
      <td>336255.5</td>
      <td>412177.5</td>
      <td>350136.5</td>
      <td>9118200.0</td>
      <td>10966550.0</td>
      <td>8406387.5</td>
      <td>...</td>
      <td>1.691351e+05</td>
      <td>4.028310e+06</td>
      <td>4.046440e+06</td>
      <td>4.211999e+06</td>
      <td>4.143136e+06</td>
      <td>4.228377e+06</td>
      <td>1.652661e+05</td>
      <td>8.263305e+05</td>
      <td>4.131652e+06</td>
      <td>2.065826e+07</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1365173.8</td>
      <td>1360551.6</td>
      <td>1336231.2</td>
      <td>1318431.1</td>
      <td>34543610.0</td>
      <td>34129345.0</td>
      <td>34013790.0</td>
      <td>...</td>
      <td>1.269751e+06</td>
      <td>3.365033e+07</td>
      <td>3.709441e+07</td>
      <td>3.516092e+07</td>
      <td>3.293637e+07</td>
      <td>3.174377e+07</td>
      <td>1.364686e+06</td>
      <td>6.823432e+06</td>
      <td>3.411716e+07</td>
      <td>1.705858e+08</td>
    </tr>
  </tbody>
</table>
<p>23 rows × 31 columns</p>
</div>



### Calculate difference in Ch4 Tonnes Between the Estimates


```python
# Calculate Difference in tons
merged_df['CH4_diff_2015'] = merged_df[2015] - merged_df['tCH4_2015']
merged_df['CH4_diff_2016'] = merged_df[2016] - merged_df['tCH4_2016']
merged_df['CH4_diff_2017'] = merged_df[2017] - merged_df['tCH4_2017']
merged_df['CH4_diff_2018'] = merged_df[2018] - merged_df['tCH4_2018']
merged_df['CH4_diff_2019'] = merged_df[2019] - merged_df['tCH4_2019']
merged_df['CH4_diff_means'] = merged_df['Mean_CH4_FAOSTAT'] - merged_df['Mean_CH4_TRACE']
merged_df['CH4_diff_totals'] = merged_df['Total_CH4_FAOSTAT'] - merged_df['Total_CH4_TRACE']


```


```python
merged_df
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
      <th>country_name_FAOSTAT</th>
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>tCO2_2015_FAOSTAT</th>
      <th>tCO2_2016_FAOSTAT</th>
      <th>tCO2_2017_FAOSTAT</th>
      <th>...</th>
      <th>Total_CH4_TRACE</th>
      <th>Mean_CO2_TRACE</th>
      <th>Total_CO2_TRACE</th>
      <th>CH4_diff_2015</th>
      <th>CH4_diff_2016</th>
      <th>CH4_diff_2017</th>
      <th>CH4_diff_2018</th>
      <th>CH4_diff_2019</th>
      <th>CH4_diff_means</th>
      <th>CH4_diff_totals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1093480.4</td>
      <td>1154531.0</td>
      <td>1144591.0</td>
      <td>1144745.4</td>
      <td>28282335.0</td>
      <td>27337010.0</td>
      <td>28863275.0</td>
      <td>...</td>
      <td>1.093375e+07</td>
      <td>5.466875e+07</td>
      <td>2.733438e+08</td>
      <td>-1.213126e+06</td>
      <td>-1.184678e+06</td>
      <td>-9.444266e+05</td>
      <td>-9.966395e+05</td>
      <td>-9.262397e+05</td>
      <td>-1.053022e+06</td>
      <td>-5.265110e+06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>126278.2</td>
      <td>130322.9</td>
      <td>121615.2</td>
      <td>111084.8</td>
      <td>3472757.5</td>
      <td>3156955.0</td>
      <td>3258072.5</td>
      <td>...</td>
      <td>1.725134e+06</td>
      <td>8.625670e+06</td>
      <td>4.312835e+07</td>
      <td>-2.021130e+05</td>
      <td>-1.841407e+05</td>
      <td>-2.421944e+05</td>
      <td>-2.500878e+05</td>
      <td>-2.183865e+05</td>
      <td>-2.193845e+05</td>
      <td>-1.096923e+06</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5399920.0</td>
      <td>5400129.0</td>
      <td>5302173.1</td>
      <td>5214454.7</td>
      <td>135164847.5</td>
      <td>134998000.0</td>
      <td>135003225.0</td>
      <td>...</td>
      <td>2.936556e+07</td>
      <td>1.468278e+08</td>
      <td>7.341391e+08</td>
      <td>-7.270532e+05</td>
      <td>-4.596111e+05</td>
      <td>-9.549420e+05</td>
      <td>-1.117892e+05</td>
      <td>-3.888972e+05</td>
      <td>-5.284585e+05</td>
      <td>-2.642293e+06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>55073.1</td>
      <td>54232.4</td>
      <td>52925.0</td>
      <td>52098.5</td>
      <td>1377055.0</td>
      <td>1376827.5</td>
      <td>1355810.0</td>
      <td>...</td>
      <td>6.247300e+04</td>
      <td>3.123650e+05</td>
      <td>1.561825e+06</td>
      <td>4.366756e+04</td>
      <td>4.172507e+04</td>
      <td>4.205941e+04</td>
      <td>3.887090e+04</td>
      <td>4.061526e+04</td>
      <td>4.138764e+04</td>
      <td>2.069382e+05</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2387656.4</td>
      <td>2425290.6</td>
      <td>2405613.8</td>
      <td>2257604.3</td>
      <td>60198837.5</td>
      <td>59691410.0</td>
      <td>60632265.0</td>
      <td>...</td>
      <td>5.711960e+06</td>
      <td>2.855980e+07</td>
      <td>1.427990e+08</td>
      <td>1.124305e+06</td>
      <td>1.364527e+06</td>
      <td>1.463758e+06</td>
      <td>1.228632e+06</td>
      <td>9.909364e+05</td>
      <td>1.234432e+06</td>
      <td>6.172158e+06</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4559136.4</td>
      <td>4620790.8</td>
      <td>4661154.9</td>
      <td>4621416.8</td>
      <td>114506210.0</td>
      <td>113978410.0</td>
      <td>115519770.0</td>
      <td>...</td>
      <td>3.184910e+07</td>
      <td>1.592455e+08</td>
      <td>7.962276e+08</td>
      <td>-1.639638e+06</td>
      <td>-7.502765e+05</td>
      <td>-1.607660e+06</td>
      <td>-1.928643e+06</td>
      <td>-2.880139e+06</td>
      <td>-1.761271e+06</td>
      <td>-8.806357e+06</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>131008.5</td>
      <td>87233.6</td>
      <td>93936.6</td>
      <td>96103.4</td>
      <td>2912167.5</td>
      <td>3275212.5</td>
      <td>2180840.0</td>
      <td>...</td>
      <td>4.595069e+05</td>
      <td>2.297534e+06</td>
      <td>1.148767e+07</td>
      <td>2.874263e+04</td>
      <td>3.920729e+04</td>
      <td>-8.968572e+03</td>
      <td>5.179159e+03</td>
      <td>1.101412e+03</td>
      <td>1.305238e+04</td>
      <td>6.526191e+04</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>118003.0</td>
      <td>118003.0</td>
      <td>109463.8</td>
      <td>110895.1</td>
      <td>2864370.0</td>
      <td>2950075.0</td>
      <td>2950075.0</td>
      <td>...</td>
      <td>2.441425e+05</td>
      <td>1.220712e+06</td>
      <td>6.103562e+06</td>
      <td>6.461512e+04</td>
      <td>6.862515e+04</td>
      <td>6.356621e+04</td>
      <td>6.476478e+04</td>
      <td>6.522596e+04</td>
      <td>6.535944e+04</td>
      <td>3.267972e+05</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>326403.0</td>
      <td>323700.3</td>
      <td>322245.0</td>
      <td>320581.8</td>
      <td>8258827.5</td>
      <td>8160075.0</td>
      <td>8092507.5</td>
      <td>...</td>
      <td>1.117884e+06</td>
      <td>5.589421e+06</td>
      <td>2.794710e+07</td>
      <td>9.980661e+04</td>
      <td>9.798967e+04</td>
      <td>5.280682e+04</td>
      <td>1.674198e+05</td>
      <td>8.737617e+04</td>
      <td>1.010798e+05</td>
      <td>5.053990e+05</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>459003.1</td>
      <td>473745.3</td>
      <td>479362.7</td>
      <td>468378.9</td>
      <td>10920650.0</td>
      <td>11475077.5</td>
      <td>11843632.5</td>
      <td>...</td>
      <td>2.674333e+06</td>
      <td>1.337166e+07</td>
      <td>6.685832e+07</td>
      <td>-5.864384e+04</td>
      <td>-1.141667e+05</td>
      <td>2.204082e+04</td>
      <td>-7.989830e+04</td>
      <td>-1.263488e+05</td>
      <td>-7.140337e+04</td>
      <td>-3.570168e+05</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>163534.1</td>
      <td>158489.7</td>
      <td>154911.3</td>
      <td>153260.9</td>
      <td>4196555.0</td>
      <td>4088352.5</td>
      <td>3962242.5</td>
      <td>...</td>
      <td>6.811023e+05</td>
      <td>3.405512e+06</td>
      <td>1.702756e+07</td>
      <td>2.267438e+04</td>
      <td>3.607436e+04</td>
      <td>1.216747e+04</td>
      <td>2.555698e+04</td>
      <td>2.048269e+04</td>
      <td>2.339118e+04</td>
      <td>1.169559e+05</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>95630.0</td>
      <td>93940.7</td>
      <td>83333.6</td>
      <td>77005.5</td>
      <td>2370670.0</td>
      <td>2390750.0</td>
      <td>2348517.5</td>
      <td>...</td>
      <td>6.996406e+04</td>
      <td>3.498203e+05</td>
      <td>1.749102e+06</td>
      <td>7.821511e+04</td>
      <td>7.866559e+04</td>
      <td>8.226007e+04</td>
      <td>7.323685e+04</td>
      <td>6.239492e+04</td>
      <td>7.495451e+04</td>
      <td>3.747725e+05</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>121756.3</td>
      <td>84456.3</td>
      <td>111049.0</td>
      <td>102156.3</td>
      <td>3316000.0</td>
      <td>3043907.5</td>
      <td>2111407.5</td>
      <td>...</td>
      <td>4.182990e+05</td>
      <td>2.091495e+06</td>
      <td>1.045748e+07</td>
      <td>4.958374e+04</td>
      <td>2.058196e+04</td>
      <td>2.533789e+04</td>
      <td>2.085986e+04</td>
      <td>1.739542e+04</td>
      <td>2.675177e+04</td>
      <td>1.337589e+05</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1052287.7</td>
      <td>1087029.5</td>
      <td>1118850.0</td>
      <td>1083100.3</td>
      <td>26485240.0</td>
      <td>26307192.5</td>
      <td>27175737.5</td>
      <td>...</td>
      <td>6.257392e+06</td>
      <td>3.128696e+07</td>
      <td>1.564348e+08</td>
      <td>-7.267265e+04</td>
      <td>-2.385180e+05</td>
      <td>-1.181398e+05</td>
      <td>-2.535969e+05</td>
      <td>-1.737880e+05</td>
      <td>-1.713431e+05</td>
      <td>-8.567154e+05</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>123232.8</td>
      <td>122656.3</td>
      <td>125238.5</td>
      <td>122453.8</td>
      <td>3048565.0</td>
      <td>3080820.0</td>
      <td>3066407.5</td>
      <td>...</td>
      <td>5.401551e+05</td>
      <td>2.700775e+06</td>
      <td>1.350388e+07</td>
      <td>1.620268e+04</td>
      <td>1.222789e+04</td>
      <td>1.152724e+04</td>
      <td>1.858597e+04</td>
      <td>1.682512e+04</td>
      <td>1.507378e+04</td>
      <td>7.536891e+04</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>142723.7</td>
      <td>162574.6</td>
      <td>153890.8</td>
      <td>156215.4</td>
      <td>3731555.0</td>
      <td>3568092.5</td>
      <td>4064365.0</td>
      <td>...</td>
      <td>4.566635e+05</td>
      <td>2.283318e+06</td>
      <td>1.141659e+07</td>
      <td>4.851434e+04</td>
      <td>7.605209e+04</td>
      <td>8.176160e+04</td>
      <td>6.188328e+04</td>
      <td>3.979186e+04</td>
      <td>6.160063e+04</td>
      <td>3.080032e+05</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>381361.8</td>
      <td>406083.3</td>
      <td>393404.2</td>
      <td>424755.1</td>
      <td>9588232.5</td>
      <td>9534045.0</td>
      <td>10152082.5</td>
      <td>...</td>
      <td>2.723184e+06</td>
      <td>1.361592e+07</td>
      <td>6.807960e+07</td>
      <td>-1.017138e+05</td>
      <td>-2.132304e+05</td>
      <td>-1.311808e+05</td>
      <td>-5.982552e+04</td>
      <td>-2.280997e+05</td>
      <td>-1.468100e+05</td>
      <td>-7.340502e+05</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1524292.5</td>
      <td>1609862.5</td>
      <td>1606047.8</td>
      <td>1556225.8</td>
      <td>38945265.0</td>
      <td>38107312.5</td>
      <td>40246562.5</td>
      <td>...</td>
      <td>1.910216e+06</td>
      <td>9.551082e+06</td>
      <td>4.775541e+07</td>
      <td>1.214609e+06</td>
      <td>1.116937e+06</td>
      <td>1.226180e+06</td>
      <td>1.188527e+06</td>
      <td>1.197771e+06</td>
      <td>1.188805e+06</td>
      <td>5.944023e+06</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>83442.3</td>
      <td>84596.2</td>
      <td>83943.3</td>
      <td>82937.0</td>
      <td>2070582.5</td>
      <td>2086057.5</td>
      <td>2114905.0</td>
      <td>...</td>
      <td>4.978202e+05</td>
      <td>2.489101e+06</td>
      <td>1.244551e+07</td>
      <td>-3.149836e+04</td>
      <td>-8.334231e+03</td>
      <td>-2.394946e+04</td>
      <td>-2.682481e+03</td>
      <td>-1.361362e+04</td>
      <td>-1.601563e+04</td>
      <td>-8.007815e+04</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1703327.7</td>
      <td>1714465.6</td>
      <td>1702989.1</td>
      <td>1553835.5</td>
      <td>38856350.0</td>
      <td>42583192.5</td>
      <td>42861640.0</td>
      <td>...</td>
      <td>6.561194e+06</td>
      <td>3.280597e+07</td>
      <td>1.640298e+08</td>
      <td>1.604559e+05</td>
      <td>-7.766539e+04</td>
      <td>5.497665e+05</td>
      <td>7.863316e+05</td>
      <td>2.487897e+05</td>
      <td>3.335357e+05</td>
      <td>1.667678e+06</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>49838.3</td>
      <td>49991.2</td>
      <td>49414.1</td>
      <td>49152.0</td>
      <td>1145967.5</td>
      <td>1245957.5</td>
      <td>1249780.0</td>
      <td>...</td>
      <td>4.179076e+05</td>
      <td>2.089538e+06</td>
      <td>1.044769e+07</td>
      <td>-3.283086e+04</td>
      <td>-3.105319e+04</td>
      <td>-3.706514e+04</td>
      <td>-3.196741e+04</td>
      <td>-4.075670e+04</td>
      <td>-3.473466e+04</td>
      <td>-1.736733e+05</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>438662.0</td>
      <td>336255.5</td>
      <td>412177.5</td>
      <td>350136.5</td>
      <td>9118200.0</td>
      <td>10966550.0</td>
      <td>8406387.5</td>
      <td>...</td>
      <td>8.263305e+05</td>
      <td>4.131652e+06</td>
      <td>2.065826e+07</td>
      <td>2.035956e+05</td>
      <td>2.768044e+05</td>
      <td>1.677756e+05</td>
      <td>2.464521e+05</td>
      <td>1.810014e+05</td>
      <td>2.151258e+05</td>
      <td>1.075629e+06</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1365173.8</td>
      <td>1360551.6</td>
      <td>1336231.2</td>
      <td>1318431.1</td>
      <td>34543610.0</td>
      <td>34129345.0</td>
      <td>34013790.0</td>
      <td>...</td>
      <td>6.823432e+06</td>
      <td>3.411716e+07</td>
      <td>1.705858e+08</td>
      <td>3.573139e+04</td>
      <td>-1.186027e+05</td>
      <td>-4.588520e+04</td>
      <td>1.877621e+04</td>
      <td>4.868034e+04</td>
      <td>-1.226000e+04</td>
      <td>-6.129998e+04</td>
    </tr>
  </tbody>
</table>
<p>23 rows × 38 columns</p>
</div>



### Calculate difference in C02 Tonnes Between the Estimates


```python
# Calculate Difference in tons
merged_df['CO2_diff_2015'] = merged_df['tCO2_2015_FAOSTAT'] - merged_df['tCO2_2015_TRACE']
merged_df['CO2_diff_2016'] = merged_df['tCO2_2016_FAOSTAT'] - merged_df['tCO2_2016_TRACE']
merged_df['CO2_diff_2017'] = merged_df['tCO2_2017_FAOSTAT'] - merged_df['tCO2_2017_TRACE']
merged_df['CO2_diff_2018'] = merged_df['tCO2_2018_FAOSTAT'] - merged_df['tCO2_2018_TRACE']
merged_df['CO2_diff_2019'] = merged_df['tCO2_2019_FAOSTAT'] - merged_df['tCO2_2019_TRACE']
merged_df['CO2_diff_means'] = merged_df['Mean_CO2_FAOSTAT'] - merged_df['Mean_CO2_TRACE']
merged_df['CO2_diff_totals'] = merged_df['Total_CO2_FAOSTAT'] - merged_df['Total_CO2_TRACE']


```

### Calculating the CH4 Percent Differences Between the Estimates


```python
## Calculate Percent Differnces on this data set )*100
# With raw data i could have accomplished this with a groupby.aggregate(lambda x ), however the pivot tables given are not easy to apply #vectorized functions across time series
merged_df['CH4_abs_percent_diff_2015'] = ((abs(merged_df[2015] - merged_df['tCH4_2015']))/((merged_df[2015] + merged_df['tCH4_2015'])/2))*100
merged_df['CH4_abs_percent_diff_2016'] = ((abs((merged_df[2016] - merged_df['tCH4_2016']))/((merged_df[2016] + merged_df['tCH4_2016'])/2)))*100
merged_df['CH4_abs_percent_diff_2017'] = ((abs(merged_df[2017] - merged_df['tCH4_2017']))/((merged_df[2017] + merged_df['tCH4_2017'])/2))*100
merged_df['CH4_abs_percent_diff_2018'] = (abs((merged_df[2018] - merged_df['tCH4_2018']))/((merged_df[2018] + merged_df['tCH4_2018'])/2))*100
merged_df['CH4_abs_percent_diff_2019'] = (abs((merged_df[2019] - merged_df['tCH4_2019']))/((merged_df[2019] + merged_df['tCH4_2019'])/2))*100
merged_df['CH4_abs_percent_diff_means'] = (abs((merged_df['Mean_CH4_FAOSTAT'] - merged_df['Mean_CH4_TRACE']))/((merged_df['Mean_CH4_FAOSTAT'] + merged_df['Mean_CH4_TRACE'])/2))* 100
merged_df['CH4_abs_percent_diff_totals'] = (abs((merged_df['Total_CH4_FAOSTAT'] - merged_df['Total_CH4_TRACE']))/((merged_df['Total_CH4_TRACE'] + merged_df['Total_CH4_FAOSTAT'])/2))*100


merged_df['CH4_relative_percent_diff_2015'] = ((merged_df[2015] - merged_df['tCH4_2015'])/(merged_df[2015]))*100
merged_df['CH4_relative_percent_diff_2016'] = ((merged_df[2016] - merged_df['tCH4_2016'])/(merged_df[2016]))*100
merged_df['CH4_relative_percent_diff_2017'] = ((merged_df[2017] - merged_df['tCH4_2017'])/(merged_df[2017]))*100
merged_df['CH4_relative_percent_diff_2018'] = ((merged_df[2018] - merged_df['tCH4_2018'])/(merged_df[2018]))*100
merged_df['CH4_relative_percent_diff_2019'] = ((merged_df[2019] - merged_df['tCH4_2019'])/(merged_df[2019]))*100
merged_df['CH4_relative_percent_diff_means'] = ((merged_df['Mean_CH4_FAOSTAT'] - merged_df['Mean_CH4_TRACE'])/(merged_df["Mean_CH4_FAOSTAT"]))*100
merged_df['CH4_relative_percent_diff_totals'] = ((merged_df['Total_CH4_FAOSTAT'] - merged_df['Total_CH4_TRACE'])/(merged_df["Total_CH4_FAOSTAT"]))*100

```

### Calculate CO2 Differences 


```python
## Calculate Percent Differnces on this data set )*100
# With raw data i could have accomplished this with a groupby.aggregate(lambda x ), however the pivot tables given are not easy to apply #vectorized functions across time series
merged_df['CO2_abs_percent_diff_2015'] = (abs((merged_df['tCO2_2015_FAOSTAT'] - merged_df['tCO2_2015_TRACE']))/((merged_df['tCO2_2015_TRACE'] + merged_df['tCO2_2015_FAOSTAT'])/2))*100
merged_df['CO2_abs_percent_diff_2016'] = ((abs(merged_df['tCO2_2016_FAOSTAT'] - merged_df['tCO2_2016_TRACE']))/((merged_df['tCO2_2016_TRACE'] + merged_df['tCO2_2016_FAOSTAT'])/2))*100
merged_df['CO2_abs_percent_diff_2017'] = ((abs(merged_df['tCO2_2017_FAOSTAT'] - merged_df['tCO2_2017_TRACE']))/((merged_df['tCO2_2017_TRACE'] + merged_df['tCO2_2017_FAOSTAT'])/2))*100
merged_df['CO2_abs_percent_diff_2018'] = ((abs(merged_df['tCO2_2018_FAOSTAT'] - merged_df['tCO2_2018_TRACE']))/((merged_df['tCO2_2018_TRACE'] + merged_df['tCO2_2018_FAOSTAT'])/2))*100
merged_df['CO2_abs_percent_diff_2019'] = ((abs(merged_df['tCO2_2019_FAOSTAT'] - merged_df['tCO2_2019_TRACE']))/((merged_df['tCO2_2019_TRACE'] + merged_df['tCO2_2019_FAOSTAT'])/2))*100
merged_df['CO2_abs_percent_diff_means'] = ((abs(merged_df['Mean_CO2_FAOSTAT'] - merged_df['Mean_CO2_TRACE']))/((merged_df['Mean_CO2_FAOSTAT'] + merged_df['Mean_CO2_TRACE'])/2))* 100
merged_df['CO2_abs_percent_diff_totals'] = ((abs(merged_df['Total_CO2_FAOSTAT'] - merged_df['Total_CO2_TRACE']))/((merged_df['Total_CO2_TRACE'] + merged_df['Total_CO2_FAOSTAT'])/2))*100


merged_df['CO2_relative_percent_diff_2015'] = ((merged_df['tCO2_2015_FAOSTAT']  - merged_df['tCO2_2015_TRACE'])/(merged_df['tCO2_2015_FAOSTAT']))*100
merged_df['CO2_relative_percent_diff_2016'] = ((merged_df['tCO2_2016_FAOSTAT']  - merged_df['tCO2_2016_TRACE'])/(merged_df['tCO2_2016_FAOSTAT']))*100
merged_df['CO2_relative_percent_diff_2017'] = ((merged_df['tCO2_2017_FAOSTAT']  - merged_df['tCO2_2017_TRACE'])/(merged_df['tCO2_2017_FAOSTAT']))*100
merged_df['CO2_relative_percent_diff_2018'] = ((merged_df['tCO2_2018_FAOSTAT']  - merged_df['tCO2_2018_TRACE'])/(merged_df['tCO2_2018_FAOSTAT']))*100
merged_df['CO2_relative_percent_diff_2019'] = ((merged_df['tCO2_2019_FAOSTAT']  - merged_df['tCO2_2019_TRACE'])/(merged_df['tCO2_2019_FAOSTAT']))*100
merged_df['CO2_relative_percent_diff_means'] = ((merged_df["Mean_CO2_FAOSTAT"] - merged_df['Mean_CO2_TRACE'])/(merged_df["Mean_CO2_FAOSTAT"]))*100
merged_df['CO2_relative_percent_diff_totals'] = ((merged_df['Total_CO2_FAOSTAT'] - merged_df['Total_CO2_TRACE'])/(merged_df["Total_CO2_FAOSTAT"]))*100
```


```python
merged_df
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
      <th>country_name_FAOSTAT</th>
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>tCO2_2015_FAOSTAT</th>
      <th>tCO2_2016_FAOSTAT</th>
      <th>tCO2_2017_FAOSTAT</th>
      <th>...</th>
      <th>CO2_abs_percent_diff_2019</th>
      <th>CO2_abs_percent_diff_means</th>
      <th>CO2_abs_percent_diff_totals</th>
      <th>CO2_relative_percent_diff_2015</th>
      <th>CO2_relative_percent_diff_2016</th>
      <th>CO2_relative_percent_diff_2017</th>
      <th>CO2_relative_percent_diff_2018</th>
      <th>CO2_relative_percent_diff_2019</th>
      <th>CO2_relative_percent_diff_means</th>
      <th>CO2_relative_percent_diff_totals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1093480.4</td>
      <td>1154531.0</td>
      <td>1144591.0</td>
      <td>1144745.4</td>
      <td>28282335.0</td>
      <td>27337010.0</td>
      <td>28863275.0</td>
      <td>...</td>
      <td>57.606797</td>
      <td>63.425917</td>
      <td>63.425917</td>
      <td>-107.233570</td>
      <td>-108.340089</td>
      <td>-81.801753</td>
      <td>-87.073857</td>
      <td>-80.912284</td>
      <td>-92.881337</td>
      <td>-92.881337</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>126278.2</td>
      <td>130322.9</td>
      <td>121615.2</td>
      <td>111084.8</td>
      <td>3472757.5</td>
      <td>3156955.0</td>
      <td>3258072.5</td>
      <td>...</td>
      <td>99.141295</td>
      <td>93.222402</td>
      <td>93.222402</td>
      <td>-145.498958</td>
      <td>-145.821472</td>
      <td>-185.841820</td>
      <td>-205.638590</td>
      <td>-196.594424</td>
      <td>-174.610414</td>
      <td>-174.610414</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5399920.0</td>
      <td>5400129.0</td>
      <td>5302173.1</td>
      <td>5214454.7</td>
      <td>135164847.5</td>
      <td>134998000.0</td>
      <td>135003225.0</td>
      <td>...</td>
      <td>7.189945</td>
      <td>9.421813</td>
      <td>9.421813</td>
      <td>-13.447527</td>
      <td>-8.511442</td>
      <td>-17.683689</td>
      <td>-2.108366</td>
      <td>-7.458060</td>
      <td>-9.887609</td>
      <td>-9.887609</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>55073.1</td>
      <td>54232.4</td>
      <td>52925.0</td>
      <td>52098.5</td>
      <td>1377055.0</td>
      <td>1376827.5</td>
      <td>1355810.0</td>
      <td>...</td>
      <td>127.757634</td>
      <td>124.705066</td>
      <td>124.705066</td>
      <td>79.277072</td>
      <td>75.763074</td>
      <td>77.554025</td>
      <td>73.445258</td>
      <td>77.958601</td>
      <td>76.811284</td>
      <td>76.811284</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2387656.4</td>
      <td>2425290.6</td>
      <td>2405613.8</td>
      <td>2257604.3</td>
      <td>60198837.5</td>
      <td>59691410.0</td>
      <td>60632265.0</td>
      <td>...</td>
      <td>56.234955</td>
      <td>70.153790</td>
      <td>70.153790</td>
      <td>46.691296</td>
      <td>57.149216</td>
      <td>60.353916</td>
      <td>51.073546</td>
      <td>43.893273</td>
      <td>51.936188</td>
      <td>51.936188</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4559136.4</td>
      <td>4620790.8</td>
      <td>4661154.9</td>
      <td>4621416.8</td>
      <td>114506210.0</td>
      <td>113978410.0</td>
      <td>115519770.0</td>
      <td>...</td>
      <td>47.515394</td>
      <td>32.086209</td>
      <td>32.086209</td>
      <td>-35.798018</td>
      <td>-16.456550</td>
      <td>-34.791882</td>
      <td>-41.376939</td>
      <td>-62.321563</td>
      <td>-38.217479</td>
      <td>-38.217479</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>131008.5</td>
      <td>87233.6</td>
      <td>93936.6</td>
      <td>96103.4</td>
      <td>2912167.5</td>
      <td>3275212.5</td>
      <td>2180840.0</td>
      <td>...</td>
      <td>1.152675</td>
      <td>13.260902</td>
      <td>13.260902</td>
      <td>24.674600</td>
      <td>29.927285</td>
      <td>-10.281098</td>
      <td>5.513463</td>
      <td>1.146070</td>
      <td>12.436318</td>
      <td>12.436318</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>118003.0</td>
      <td>118003.0</td>
      <td>109463.8</td>
      <td>110895.1</td>
      <td>2864370.0</td>
      <td>2950075.0</td>
      <td>2950075.0</td>
      <td>...</td>
      <td>83.321649</td>
      <td>80.187551</td>
      <td>80.187551</td>
      <td>56.395576</td>
      <td>58.155426</td>
      <td>53.868303</td>
      <td>59.165480</td>
      <td>58.817707</td>
      <td>57.238482</td>
      <td>57.238482</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>326403.0</td>
      <td>323700.3</td>
      <td>322245.0</td>
      <td>320581.8</td>
      <td>8258827.5</td>
      <td>8160075.0</td>
      <td>8092507.5</td>
      <td>...</td>
      <td>31.555853</td>
      <td>36.874729</td>
      <td>36.874729</td>
      <td>30.212099</td>
      <td>30.021068</td>
      <td>16.313490</td>
      <td>51.954183</td>
      <td>27.255501</td>
      <td>31.134372</td>
      <td>31.134372</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>459003.1</td>
      <td>473745.3</td>
      <td>479362.7</td>
      <td>468378.9</td>
      <td>10920650.0</td>
      <td>11475077.5</td>
      <td>11843632.5</td>
      <td>...</td>
      <td>23.769728</td>
      <td>14.304565</td>
      <td>14.304565</td>
      <td>-13.424988</td>
      <td>-24.872761</td>
      <td>4.652461</td>
      <td>-16.667610</td>
      <td>-26.975760</td>
      <td>-15.406481</td>
      <td>-15.406481</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>163534.1</td>
      <td>158489.7</td>
      <td>154911.3</td>
      <td>153260.9</td>
      <td>4196555.0</td>
      <td>4088352.5</td>
      <td>3962242.5</td>
      <td>...</td>
      <td>14.321600</td>
      <td>15.813819</td>
      <td>15.813819</td>
      <td>13.507737</td>
      <td>22.059230</td>
      <td>7.677136</td>
      <td>16.497815</td>
      <td>13.364589</td>
      <td>14.655057</td>
      <td>14.655057</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>95630.0</td>
      <td>93940.7</td>
      <td>83333.6</td>
      <td>77005.5</td>
      <td>2370670.0</td>
      <td>2390750.0</td>
      <td>2348517.5</td>
      <td>...</td>
      <td>136.209544</td>
      <td>145.627378</td>
      <td>145.627378</td>
      <td>82.482067</td>
      <td>82.260369</td>
      <td>87.565950</td>
      <td>87.883944</td>
      <td>81.026578</td>
      <td>84.268427</td>
      <td>84.268427</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>121756.3</td>
      <td>84456.3</td>
      <td>111049.0</td>
      <td>102156.3</td>
      <td>3316000.0</td>
      <td>3043907.5</td>
      <td>2111407.5</td>
      <td>...</td>
      <td>18.612972</td>
      <td>27.569003</td>
      <td>27.569003</td>
      <td>37.382189</td>
      <td>16.904226</td>
      <td>30.001182</td>
      <td>18.784377</td>
      <td>17.028241</td>
      <td>24.229137</td>
      <td>24.229137</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1052287.7</td>
      <td>1087029.5</td>
      <td>1118850.0</td>
      <td>1083100.3</td>
      <td>26485240.0</td>
      <td>26307192.5</td>
      <td>27175737.5</td>
      <td>...</td>
      <td>14.853751</td>
      <td>14.697380</td>
      <td>14.697380</td>
      <td>-6.859731</td>
      <td>-22.666619</td>
      <td>-10.868129</td>
      <td>-22.665852</td>
      <td>-16.045425</td>
      <td>-15.863111</td>
      <td>-15.863111</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>123232.8</td>
      <td>122656.3</td>
      <td>125238.5</td>
      <td>122453.8</td>
      <td>3048565.0</td>
      <td>3080820.0</td>
      <td>3066407.5</td>
      <td>...</td>
      <td>14.753544</td>
      <td>13.043224</td>
      <td>13.043224</td>
      <td>13.287137</td>
      <td>9.922595</td>
      <td>9.398001</td>
      <td>14.840462</td>
      <td>13.739977</td>
      <td>12.244674</td>
      <td>12.244674</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>142723.7</td>
      <td>162574.6</td>
      <td>153890.8</td>
      <td>156215.4</td>
      <td>3731555.0</td>
      <td>3568092.5</td>
      <td>4064365.0</td>
      <td>...</td>
      <td>29.190154</td>
      <td>50.437328</td>
      <td>50.437328</td>
      <td>32.502761</td>
      <td>53.286238</td>
      <td>50.291743</td>
      <td>40.212459</td>
      <td>25.472433</td>
      <td>40.279401</td>
      <td>40.279401</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>381361.8</td>
      <td>406083.3</td>
      <td>393404.2</td>
      <td>424755.1</td>
      <td>9588232.5</td>
      <td>9534045.0</td>
      <td>10152082.5</td>
      <td>...</td>
      <td>42.334367</td>
      <td>31.154530</td>
      <td>31.154530</td>
      <td>-26.520489</td>
      <td>-55.912882</td>
      <td>-32.303912</td>
      <td>-15.207139</td>
      <td>-53.701452</td>
      <td>-36.903009</td>
      <td>-36.903009</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1524292.5</td>
      <td>1609862.5</td>
      <td>1606047.8</td>
      <td>1556225.8</td>
      <td>38945265.0</td>
      <td>38107312.5</td>
      <td>40246562.5</td>
      <td>...</td>
      <td>125.114417</td>
      <td>121.748165</td>
      <td>121.748165</td>
      <td>77.968948</td>
      <td>73.275770</td>
      <td>76.166725</td>
      <td>74.003201</td>
      <td>76.966391</td>
      <td>75.679166</td>
      <td>75.679166</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>83442.3</td>
      <td>84596.2</td>
      <td>83943.3</td>
      <td>82937.0</td>
      <td>2070582.5</td>
      <td>2086057.5</td>
      <td>2114905.0</td>
      <td>...</td>
      <td>15.169422</td>
      <td>17.492669</td>
      <td>17.492669</td>
      <td>-38.030793</td>
      <td>-9.988016</td>
      <td>-28.310326</td>
      <td>-3.195586</td>
      <td>-16.414407</td>
      <td>-19.169278</td>
      <td>-19.169278</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1703327.7</td>
      <td>1714465.6</td>
      <td>1702989.1</td>
      <td>1553835.5</td>
      <td>38856350.0</td>
      <td>42583192.5</td>
      <td>42861640.0</td>
      <td>...</td>
      <td>17.404685</td>
      <td>22.551331</td>
      <td>22.551331</td>
      <td>10.323662</td>
      <td>-4.559627</td>
      <td>32.066348</td>
      <td>46.173612</td>
      <td>16.011325</td>
      <td>20.266184</td>
      <td>20.266184</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>49838.3</td>
      <td>49991.2</td>
      <td>49414.1</td>
      <td>49152.0</td>
      <td>1145967.5</td>
      <td>1245957.5</td>
      <td>1249780.0</td>
      <td>...</td>
      <td>58.617135</td>
      <td>52.458032</td>
      <td>52.458032</td>
      <td>-71.622589</td>
      <td>-62.307893</td>
      <td>-74.143329</td>
      <td>-64.692890</td>
      <td>-82.919716</td>
      <td>-71.109302</td>
      <td>-71.109302</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>438662.0</td>
      <td>336255.5</td>
      <td>412177.5</td>
      <td>350136.5</td>
      <td>9118200.0</td>
      <td>10966550.0</td>
      <td>8406387.5</td>
      <td>...</td>
      <td>69.713577</td>
      <td>78.850049</td>
      <td>78.850049</td>
      <td>55.821215</td>
      <td>63.101978</td>
      <td>49.895259</td>
      <td>59.792699</td>
      <td>51.694526</td>
      <td>56.553728</td>
      <td>56.553728</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1365173.8</td>
      <td>1360551.6</td>
      <td>1336231.2</td>
      <td>1318431.1</td>
      <td>34543610.0</td>
      <td>34129345.0</td>
      <td>34013790.0</td>
      <td>...</td>
      <td>3.761740</td>
      <td>0.902428</td>
      <td>0.902428</td>
      <td>2.585962</td>
      <td>-8.687738</td>
      <td>-3.372544</td>
      <td>1.405162</td>
      <td>3.692293</td>
      <td>-0.906518</td>
      <td>-0.906518</td>
    </tr>
  </tbody>
</table>
<p>23 rows × 73 columns</p>
</div>



### Recalculate Means


```python
merged_df.loc['mean'] = merged_df.select_dtypes(np.number).mean()

```


```python
merged_df.at['mean','country_name_FAOSTAT'] = 'mean'
merged_df.at['mean','country_name_TRACE'] = 'mean'
```


```python
merged_df
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
      <th>country_name_FAOSTAT</th>
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>tCO2_2015_FAOSTAT</th>
      <th>tCO2_2016_FAOSTAT</th>
      <th>tCO2_2017_FAOSTAT</th>
      <th>...</th>
      <th>CO2_abs_percent_diff_2019</th>
      <th>CO2_abs_percent_diff_means</th>
      <th>CO2_abs_percent_diff_totals</th>
      <th>CO2_relative_percent_diff_2015</th>
      <th>CO2_relative_percent_diff_2016</th>
      <th>CO2_relative_percent_diff_2017</th>
      <th>CO2_relative_percent_diff_2018</th>
      <th>CO2_relative_percent_diff_2019</th>
      <th>CO2_relative_percent_diff_means</th>
      <th>CO2_relative_percent_diff_totals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1.093480e+06</td>
      <td>1.154531e+06</td>
      <td>1.144591e+06</td>
      <td>1.144745e+06</td>
      <td>28282335.0</td>
      <td>2.733701e+07</td>
      <td>2.886328e+07</td>
      <td>...</td>
      <td>57.606797</td>
      <td>63.425917</td>
      <td>63.425917</td>
      <td>-107.233570</td>
      <td>-108.340089</td>
      <td>-81.801753</td>
      <td>-87.073857</td>
      <td>-80.912284</td>
      <td>-92.881337</td>
      <td>-92.881337</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>1.262782e+05</td>
      <td>1.303229e+05</td>
      <td>1.216152e+05</td>
      <td>1.110848e+05</td>
      <td>3472757.5</td>
      <td>3.156955e+06</td>
      <td>3.258072e+06</td>
      <td>...</td>
      <td>99.141295</td>
      <td>93.222402</td>
      <td>93.222402</td>
      <td>-145.498958</td>
      <td>-145.821472</td>
      <td>-185.841820</td>
      <td>-205.638590</td>
      <td>-196.594424</td>
      <td>-174.610414</td>
      <td>-174.610414</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5.399920e+06</td>
      <td>5.400129e+06</td>
      <td>5.302173e+06</td>
      <td>5.214455e+06</td>
      <td>135164847.5</td>
      <td>1.349980e+08</td>
      <td>1.350032e+08</td>
      <td>...</td>
      <td>7.189945</td>
      <td>9.421813</td>
      <td>9.421813</td>
      <td>-13.447527</td>
      <td>-8.511442</td>
      <td>-17.683689</td>
      <td>-2.108366</td>
      <td>-7.458060</td>
      <td>-9.887609</td>
      <td>-9.887609</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>5.507310e+04</td>
      <td>5.423240e+04</td>
      <td>5.292500e+04</td>
      <td>5.209850e+04</td>
      <td>1377055.0</td>
      <td>1.376828e+06</td>
      <td>1.355810e+06</td>
      <td>...</td>
      <td>127.757634</td>
      <td>124.705066</td>
      <td>124.705066</td>
      <td>79.277072</td>
      <td>75.763074</td>
      <td>77.554025</td>
      <td>73.445258</td>
      <td>77.958601</td>
      <td>76.811284</td>
      <td>76.811284</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2.387656e+06</td>
      <td>2.425291e+06</td>
      <td>2.405614e+06</td>
      <td>2.257604e+06</td>
      <td>60198837.5</td>
      <td>5.969141e+07</td>
      <td>6.063226e+07</td>
      <td>...</td>
      <td>56.234955</td>
      <td>70.153790</td>
      <td>70.153790</td>
      <td>46.691296</td>
      <td>57.149216</td>
      <td>60.353916</td>
      <td>51.073546</td>
      <td>43.893273</td>
      <td>51.936188</td>
      <td>51.936188</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4.559136e+06</td>
      <td>4.620791e+06</td>
      <td>4.661155e+06</td>
      <td>4.621417e+06</td>
      <td>114506210.0</td>
      <td>1.139784e+08</td>
      <td>1.155198e+08</td>
      <td>...</td>
      <td>47.515394</td>
      <td>32.086209</td>
      <td>32.086209</td>
      <td>-35.798018</td>
      <td>-16.456550</td>
      <td>-34.791882</td>
      <td>-41.376939</td>
      <td>-62.321563</td>
      <td>-38.217479</td>
      <td>-38.217479</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>1.310085e+05</td>
      <td>8.723360e+04</td>
      <td>9.393660e+04</td>
      <td>9.610340e+04</td>
      <td>2912167.5</td>
      <td>3.275212e+06</td>
      <td>2.180840e+06</td>
      <td>...</td>
      <td>1.152675</td>
      <td>13.260902</td>
      <td>13.260902</td>
      <td>24.674600</td>
      <td>29.927285</td>
      <td>-10.281098</td>
      <td>5.513463</td>
      <td>1.146070</td>
      <td>12.436318</td>
      <td>12.436318</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>1.180030e+05</td>
      <td>1.180030e+05</td>
      <td>1.094638e+05</td>
      <td>1.108951e+05</td>
      <td>2864370.0</td>
      <td>2.950075e+06</td>
      <td>2.950075e+06</td>
      <td>...</td>
      <td>83.321649</td>
      <td>80.187551</td>
      <td>80.187551</td>
      <td>56.395576</td>
      <td>58.155426</td>
      <td>53.868303</td>
      <td>59.165480</td>
      <td>58.817707</td>
      <td>57.238482</td>
      <td>57.238482</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>3.264030e+05</td>
      <td>3.237003e+05</td>
      <td>3.222450e+05</td>
      <td>3.205818e+05</td>
      <td>8258827.5</td>
      <td>8.160075e+06</td>
      <td>8.092508e+06</td>
      <td>...</td>
      <td>31.555853</td>
      <td>36.874729</td>
      <td>36.874729</td>
      <td>30.212099</td>
      <td>30.021068</td>
      <td>16.313490</td>
      <td>51.954183</td>
      <td>27.255501</td>
      <td>31.134372</td>
      <td>31.134372</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>4.590031e+05</td>
      <td>4.737453e+05</td>
      <td>4.793627e+05</td>
      <td>4.683789e+05</td>
      <td>10920650.0</td>
      <td>1.147508e+07</td>
      <td>1.184363e+07</td>
      <td>...</td>
      <td>23.769728</td>
      <td>14.304565</td>
      <td>14.304565</td>
      <td>-13.424988</td>
      <td>-24.872761</td>
      <td>4.652461</td>
      <td>-16.667610</td>
      <td>-26.975760</td>
      <td>-15.406481</td>
      <td>-15.406481</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>1.635341e+05</td>
      <td>1.584897e+05</td>
      <td>1.549113e+05</td>
      <td>1.532609e+05</td>
      <td>4196555.0</td>
      <td>4.088352e+06</td>
      <td>3.962243e+06</td>
      <td>...</td>
      <td>14.321600</td>
      <td>15.813819</td>
      <td>15.813819</td>
      <td>13.507737</td>
      <td>22.059230</td>
      <td>7.677136</td>
      <td>16.497815</td>
      <td>13.364589</td>
      <td>14.655057</td>
      <td>14.655057</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>9.563000e+04</td>
      <td>9.394070e+04</td>
      <td>8.333360e+04</td>
      <td>7.700550e+04</td>
      <td>2370670.0</td>
      <td>2.390750e+06</td>
      <td>2.348518e+06</td>
      <td>...</td>
      <td>136.209544</td>
      <td>145.627378</td>
      <td>145.627378</td>
      <td>82.482067</td>
      <td>82.260369</td>
      <td>87.565950</td>
      <td>87.883944</td>
      <td>81.026578</td>
      <td>84.268427</td>
      <td>84.268427</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>1.217563e+05</td>
      <td>8.445630e+04</td>
      <td>1.110490e+05</td>
      <td>1.021563e+05</td>
      <td>3316000.0</td>
      <td>3.043908e+06</td>
      <td>2.111408e+06</td>
      <td>...</td>
      <td>18.612972</td>
      <td>27.569003</td>
      <td>27.569003</td>
      <td>37.382189</td>
      <td>16.904226</td>
      <td>30.001182</td>
      <td>18.784377</td>
      <td>17.028241</td>
      <td>24.229137</td>
      <td>24.229137</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1.052288e+06</td>
      <td>1.087030e+06</td>
      <td>1.118850e+06</td>
      <td>1.083100e+06</td>
      <td>26485240.0</td>
      <td>2.630719e+07</td>
      <td>2.717574e+07</td>
      <td>...</td>
      <td>14.853751</td>
      <td>14.697380</td>
      <td>14.697380</td>
      <td>-6.859731</td>
      <td>-22.666619</td>
      <td>-10.868129</td>
      <td>-22.665852</td>
      <td>-16.045425</td>
      <td>-15.863111</td>
      <td>-15.863111</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>1.232328e+05</td>
      <td>1.226563e+05</td>
      <td>1.252385e+05</td>
      <td>1.224538e+05</td>
      <td>3048565.0</td>
      <td>3.080820e+06</td>
      <td>3.066408e+06</td>
      <td>...</td>
      <td>14.753544</td>
      <td>13.043224</td>
      <td>13.043224</td>
      <td>13.287137</td>
      <td>9.922595</td>
      <td>9.398001</td>
      <td>14.840462</td>
      <td>13.739977</td>
      <td>12.244674</td>
      <td>12.244674</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>1.427237e+05</td>
      <td>1.625746e+05</td>
      <td>1.538908e+05</td>
      <td>1.562154e+05</td>
      <td>3731555.0</td>
      <td>3.568093e+06</td>
      <td>4.064365e+06</td>
      <td>...</td>
      <td>29.190154</td>
      <td>50.437328</td>
      <td>50.437328</td>
      <td>32.502761</td>
      <td>53.286238</td>
      <td>50.291743</td>
      <td>40.212459</td>
      <td>25.472433</td>
      <td>40.279401</td>
      <td>40.279401</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>3.813618e+05</td>
      <td>4.060833e+05</td>
      <td>3.934042e+05</td>
      <td>4.247551e+05</td>
      <td>9588232.5</td>
      <td>9.534045e+06</td>
      <td>1.015208e+07</td>
      <td>...</td>
      <td>42.334367</td>
      <td>31.154530</td>
      <td>31.154530</td>
      <td>-26.520489</td>
      <td>-55.912882</td>
      <td>-32.303912</td>
      <td>-15.207139</td>
      <td>-53.701452</td>
      <td>-36.903009</td>
      <td>-36.903009</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1.524292e+06</td>
      <td>1.609862e+06</td>
      <td>1.606048e+06</td>
      <td>1.556226e+06</td>
      <td>38945265.0</td>
      <td>3.810731e+07</td>
      <td>4.024656e+07</td>
      <td>...</td>
      <td>125.114417</td>
      <td>121.748165</td>
      <td>121.748165</td>
      <td>77.968948</td>
      <td>73.275770</td>
      <td>76.166725</td>
      <td>74.003201</td>
      <td>76.966391</td>
      <td>75.679166</td>
      <td>75.679166</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>8.344230e+04</td>
      <td>8.459620e+04</td>
      <td>8.394330e+04</td>
      <td>8.293700e+04</td>
      <td>2070582.5</td>
      <td>2.086058e+06</td>
      <td>2.114905e+06</td>
      <td>...</td>
      <td>15.169422</td>
      <td>17.492669</td>
      <td>17.492669</td>
      <td>-38.030793</td>
      <td>-9.988016</td>
      <td>-28.310326</td>
      <td>-3.195586</td>
      <td>-16.414407</td>
      <td>-19.169278</td>
      <td>-19.169278</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1.703328e+06</td>
      <td>1.714466e+06</td>
      <td>1.702989e+06</td>
      <td>1.553836e+06</td>
      <td>38856350.0</td>
      <td>4.258319e+07</td>
      <td>4.286164e+07</td>
      <td>...</td>
      <td>17.404685</td>
      <td>22.551331</td>
      <td>22.551331</td>
      <td>10.323662</td>
      <td>-4.559627</td>
      <td>32.066348</td>
      <td>46.173612</td>
      <td>16.011325</td>
      <td>20.266184</td>
      <td>20.266184</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>4.983830e+04</td>
      <td>4.999120e+04</td>
      <td>4.941410e+04</td>
      <td>4.915200e+04</td>
      <td>1145967.5</td>
      <td>1.245958e+06</td>
      <td>1.249780e+06</td>
      <td>...</td>
      <td>58.617135</td>
      <td>52.458032</td>
      <td>52.458032</td>
      <td>-71.622589</td>
      <td>-62.307893</td>
      <td>-74.143329</td>
      <td>-64.692890</td>
      <td>-82.919716</td>
      <td>-71.109302</td>
      <td>-71.109302</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>4.386620e+05</td>
      <td>3.362555e+05</td>
      <td>4.121775e+05</td>
      <td>3.501365e+05</td>
      <td>9118200.0</td>
      <td>1.096655e+07</td>
      <td>8.406388e+06</td>
      <td>...</td>
      <td>69.713577</td>
      <td>78.850049</td>
      <td>78.850049</td>
      <td>55.821215</td>
      <td>63.101978</td>
      <td>49.895259</td>
      <td>59.792699</td>
      <td>51.694526</td>
      <td>56.553728</td>
      <td>56.553728</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1.365174e+06</td>
      <td>1.360552e+06</td>
      <td>1.336231e+06</td>
      <td>1.318431e+06</td>
      <td>34543610.0</td>
      <td>3.412934e+07</td>
      <td>3.401379e+07</td>
      <td>...</td>
      <td>3.761740</td>
      <td>0.902428</td>
      <td>0.902428</td>
      <td>2.585962</td>
      <td>-8.687738</td>
      <td>-3.372544</td>
      <td>1.405162</td>
      <td>3.692293</td>
      <td>-0.906518</td>
      <td>-0.906518</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>NaN</td>
      <td>mean</td>
      <td>948478.0</td>
      <td>9.522272e+05</td>
      <td>9.590840e+05</td>
      <td>9.575896e+05</td>
      <td>9.316100e+05</td>
      <td>23711950.0</td>
      <td>2.380568e+07</td>
      <td>2.397710e+07</td>
      <td>...</td>
      <td>47.621862</td>
      <td>49.129925</td>
      <td>49.129925</td>
      <td>4.551116</td>
      <td>4.508756</td>
      <td>3.322003</td>
      <td>6.179080</td>
      <td>-1.533721</td>
      <td>3.599038</td>
      <td>3.599038</td>
    </tr>
  </tbody>
</table>
<p>24 rows × 73 columns</p>
</div>



### Recalculate Totals


```python
merged_df.loc['total'] = merged_df[merged_df['country_name_FAOSTAT'] != 'mean'].select_dtypes(np.number).sum()
```


```python
merged_df.at['total','country_name_FAOSTAT'] = 'total'
merged_df.at['total','country_name_TRACE'] = 'total'
```


```python
merged_df.reset_index(inplace=True, drop = True)
```


```python
merged_df
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
      <th>country_name_FAOSTAT</th>
      <th>2015</th>
      <th>2016</th>
      <th>2017</th>
      <th>2018</th>
      <th>2019</th>
      <th>tCO2_2015_FAOSTAT</th>
      <th>tCO2_2016_FAOSTAT</th>
      <th>tCO2_2017_FAOSTAT</th>
      <th>...</th>
      <th>CO2_abs_percent_diff_2019</th>
      <th>CO2_abs_percent_diff_means</th>
      <th>CO2_abs_percent_diff_totals</th>
      <th>CO2_relative_percent_diff_2015</th>
      <th>CO2_relative_percent_diff_2016</th>
      <th>CO2_relative_percent_diff_2017</th>
      <th>CO2_relative_percent_diff_2018</th>
      <th>CO2_relative_percent_diff_2019</th>
      <th>CO2_relative_percent_diff_means</th>
      <th>CO2_relative_percent_diff_totals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BGD</td>
      <td>Bangladesh</td>
      <td>1131293.4</td>
      <td>1.093480e+06</td>
      <td>1.154531e+06</td>
      <td>1.144591e+06</td>
      <td>1.144745e+06</td>
      <td>28282335.0</td>
      <td>2.733701e+07</td>
      <td>2.886328e+07</td>
      <td>...</td>
      <td>57.606797</td>
      <td>63.425917</td>
      <td>63.425917</td>
      <td>-107.233570</td>
      <td>-108.340089</td>
      <td>-81.801753</td>
      <td>-87.073857</td>
      <td>-80.912284</td>
      <td>-92.881337</td>
      <td>-92.881337</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BRA</td>
      <td>Brazil</td>
      <td>138910.3</td>
      <td>1.262782e+05</td>
      <td>1.303229e+05</td>
      <td>1.216152e+05</td>
      <td>1.110848e+05</td>
      <td>3472757.5</td>
      <td>3.156955e+06</td>
      <td>3.258072e+06</td>
      <td>...</td>
      <td>99.141295</td>
      <td>93.222402</td>
      <td>93.222402</td>
      <td>-145.498958</td>
      <td>-145.821472</td>
      <td>-185.841820</td>
      <td>-205.638590</td>
      <td>-196.594424</td>
      <td>-174.610414</td>
      <td>-174.610414</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CHN</td>
      <td>China</td>
      <td>5406593.9</td>
      <td>5.399920e+06</td>
      <td>5.400129e+06</td>
      <td>5.302173e+06</td>
      <td>5.214455e+06</td>
      <td>135164847.5</td>
      <td>1.349980e+08</td>
      <td>1.350032e+08</td>
      <td>...</td>
      <td>7.189945</td>
      <td>9.421813</td>
      <td>9.421813</td>
      <td>-13.447527</td>
      <td>-8.511442</td>
      <td>-17.683689</td>
      <td>-2.108366</td>
      <td>-7.458060</td>
      <td>-9.887609</td>
      <td>-9.887609</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ESP</td>
      <td>Spain</td>
      <td>55082.2</td>
      <td>5.507310e+04</td>
      <td>5.423240e+04</td>
      <td>5.292500e+04</td>
      <td>5.209850e+04</td>
      <td>1377055.0</td>
      <td>1.376828e+06</td>
      <td>1.355810e+06</td>
      <td>...</td>
      <td>127.757634</td>
      <td>124.705066</td>
      <td>124.705066</td>
      <td>79.277072</td>
      <td>75.763074</td>
      <td>77.554025</td>
      <td>73.445258</td>
      <td>77.958601</td>
      <td>76.811284</td>
      <td>76.811284</td>
    </tr>
    <tr>
      <th>4</th>
      <td>IDN</td>
      <td>Indonesia</td>
      <td>2407953.5</td>
      <td>2.387656e+06</td>
      <td>2.425291e+06</td>
      <td>2.405614e+06</td>
      <td>2.257604e+06</td>
      <td>60198837.5</td>
      <td>5.969141e+07</td>
      <td>6.063226e+07</td>
      <td>...</td>
      <td>56.234955</td>
      <td>70.153790</td>
      <td>70.153790</td>
      <td>46.691296</td>
      <td>57.149216</td>
      <td>60.353916</td>
      <td>51.073546</td>
      <td>43.893273</td>
      <td>51.936188</td>
      <td>51.936188</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IND</td>
      <td>India</td>
      <td>4580248.4</td>
      <td>4.559136e+06</td>
      <td>4.620791e+06</td>
      <td>4.661155e+06</td>
      <td>4.621417e+06</td>
      <td>114506210.0</td>
      <td>1.139784e+08</td>
      <td>1.155198e+08</td>
      <td>...</td>
      <td>47.515394</td>
      <td>32.086209</td>
      <td>32.086209</td>
      <td>-35.798018</td>
      <td>-16.456550</td>
      <td>-34.791882</td>
      <td>-41.376939</td>
      <td>-62.321563</td>
      <td>-38.217479</td>
      <td>-38.217479</td>
    </tr>
    <tr>
      <th>6</th>
      <td>IRN</td>
      <td>Iran (Islamic Republic of)</td>
      <td>116486.7</td>
      <td>1.310085e+05</td>
      <td>8.723360e+04</td>
      <td>9.393660e+04</td>
      <td>9.610340e+04</td>
      <td>2912167.5</td>
      <td>3.275212e+06</td>
      <td>2.180840e+06</td>
      <td>...</td>
      <td>1.152675</td>
      <td>13.260902</td>
      <td>13.260902</td>
      <td>24.674600</td>
      <td>29.927285</td>
      <td>-10.281098</td>
      <td>5.513463</td>
      <td>1.146070</td>
      <td>12.436318</td>
      <td>12.436318</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ITA</td>
      <td>Italy</td>
      <td>114574.8</td>
      <td>1.180030e+05</td>
      <td>1.180030e+05</td>
      <td>1.094638e+05</td>
      <td>1.108951e+05</td>
      <td>2864370.0</td>
      <td>2.950075e+06</td>
      <td>2.950075e+06</td>
      <td>...</td>
      <td>83.321649</td>
      <td>80.187551</td>
      <td>80.187551</td>
      <td>56.395576</td>
      <td>58.155426</td>
      <td>53.868303</td>
      <td>59.165480</td>
      <td>58.817707</td>
      <td>57.238482</td>
      <td>57.238482</td>
    </tr>
    <tr>
      <th>8</th>
      <td>JPN</td>
      <td>Japan</td>
      <td>330353.1</td>
      <td>3.264030e+05</td>
      <td>3.237003e+05</td>
      <td>3.222450e+05</td>
      <td>3.205818e+05</td>
      <td>8258827.5</td>
      <td>8.160075e+06</td>
      <td>8.092508e+06</td>
      <td>...</td>
      <td>31.555853</td>
      <td>36.874729</td>
      <td>36.874729</td>
      <td>30.212099</td>
      <td>30.021068</td>
      <td>16.313490</td>
      <td>51.954183</td>
      <td>27.255501</td>
      <td>31.134372</td>
      <td>31.134372</td>
    </tr>
    <tr>
      <th>9</th>
      <td>KHM</td>
      <td>Cambodia</td>
      <td>436826.0</td>
      <td>4.590031e+05</td>
      <td>4.737453e+05</td>
      <td>4.793627e+05</td>
      <td>4.683789e+05</td>
      <td>10920650.0</td>
      <td>1.147508e+07</td>
      <td>1.184363e+07</td>
      <td>...</td>
      <td>23.769728</td>
      <td>14.304565</td>
      <td>14.304565</td>
      <td>-13.424988</td>
      <td>-24.872761</td>
      <td>4.652461</td>
      <td>-16.667610</td>
      <td>-26.975760</td>
      <td>-15.406481</td>
      <td>-15.406481</td>
    </tr>
    <tr>
      <th>10</th>
      <td>KOR</td>
      <td>Korea (the Republic of)</td>
      <td>167862.2</td>
      <td>1.635341e+05</td>
      <td>1.584897e+05</td>
      <td>1.549113e+05</td>
      <td>1.532609e+05</td>
      <td>4196555.0</td>
      <td>4.088352e+06</td>
      <td>3.962243e+06</td>
      <td>...</td>
      <td>14.321600</td>
      <td>15.813819</td>
      <td>15.813819</td>
      <td>13.507737</td>
      <td>22.059230</td>
      <td>7.677136</td>
      <td>16.497815</td>
      <td>13.364589</td>
      <td>14.655057</td>
      <td>14.655057</td>
    </tr>
    <tr>
      <th>11</th>
      <td>LAO</td>
      <td>Lao People's Democratic Republic (the)</td>
      <td>94826.8</td>
      <td>9.563000e+04</td>
      <td>9.394070e+04</td>
      <td>8.333360e+04</td>
      <td>7.700550e+04</td>
      <td>2370670.0</td>
      <td>2.390750e+06</td>
      <td>2.348518e+06</td>
      <td>...</td>
      <td>136.209544</td>
      <td>145.627378</td>
      <td>145.627378</td>
      <td>82.482067</td>
      <td>82.260369</td>
      <td>87.565950</td>
      <td>87.883944</td>
      <td>81.026578</td>
      <td>84.268427</td>
      <td>84.268427</td>
    </tr>
    <tr>
      <th>12</th>
      <td>LKA</td>
      <td>Sri Lanka</td>
      <td>132640.0</td>
      <td>1.217563e+05</td>
      <td>8.445630e+04</td>
      <td>1.110490e+05</td>
      <td>1.021563e+05</td>
      <td>3316000.0</td>
      <td>3.043908e+06</td>
      <td>2.111408e+06</td>
      <td>...</td>
      <td>18.612972</td>
      <td>27.569003</td>
      <td>27.569003</td>
      <td>37.382189</td>
      <td>16.904226</td>
      <td>30.001182</td>
      <td>18.784377</td>
      <td>17.028241</td>
      <td>24.229137</td>
      <td>24.229137</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MMR</td>
      <td>Myanmar</td>
      <td>1059409.6</td>
      <td>1.052288e+06</td>
      <td>1.087030e+06</td>
      <td>1.118850e+06</td>
      <td>1.083100e+06</td>
      <td>26485240.0</td>
      <td>2.630719e+07</td>
      <td>2.717574e+07</td>
      <td>...</td>
      <td>14.853751</td>
      <td>14.697380</td>
      <td>14.697380</td>
      <td>-6.859731</td>
      <td>-22.666619</td>
      <td>-10.868129</td>
      <td>-22.665852</td>
      <td>-16.045425</td>
      <td>-15.863111</td>
      <td>-15.863111</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MYS</td>
      <td>Malaysia</td>
      <td>121942.6</td>
      <td>1.232328e+05</td>
      <td>1.226563e+05</td>
      <td>1.252385e+05</td>
      <td>1.224538e+05</td>
      <td>3048565.0</td>
      <td>3.080820e+06</td>
      <td>3.066408e+06</td>
      <td>...</td>
      <td>14.753544</td>
      <td>13.043224</td>
      <td>13.043224</td>
      <td>13.287137</td>
      <td>9.922595</td>
      <td>9.398001</td>
      <td>14.840462</td>
      <td>13.739977</td>
      <td>12.244674</td>
      <td>12.244674</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NPL</td>
      <td>Nepal</td>
      <td>149262.2</td>
      <td>1.427237e+05</td>
      <td>1.625746e+05</td>
      <td>1.538908e+05</td>
      <td>1.562154e+05</td>
      <td>3731555.0</td>
      <td>3.568093e+06</td>
      <td>4.064365e+06</td>
      <td>...</td>
      <td>29.190154</td>
      <td>50.437328</td>
      <td>50.437328</td>
      <td>32.502761</td>
      <td>53.286238</td>
      <td>50.291743</td>
      <td>40.212459</td>
      <td>25.472433</td>
      <td>40.279401</td>
      <td>40.279401</td>
    </tr>
    <tr>
      <th>16</th>
      <td>PAK</td>
      <td>Pakistan</td>
      <td>383529.3</td>
      <td>3.813618e+05</td>
      <td>4.060833e+05</td>
      <td>3.934042e+05</td>
      <td>4.247551e+05</td>
      <td>9588232.5</td>
      <td>9.534045e+06</td>
      <td>1.015208e+07</td>
      <td>...</td>
      <td>42.334367</td>
      <td>31.154530</td>
      <td>31.154530</td>
      <td>-26.520489</td>
      <td>-55.912882</td>
      <td>-32.303912</td>
      <td>-15.207139</td>
      <td>-53.701452</td>
      <td>-36.903009</td>
      <td>-36.903009</td>
    </tr>
    <tr>
      <th>17</th>
      <td>PHL</td>
      <td>Philippines (the)</td>
      <td>1557810.6</td>
      <td>1.524292e+06</td>
      <td>1.609862e+06</td>
      <td>1.606048e+06</td>
      <td>1.556226e+06</td>
      <td>38945265.0</td>
      <td>3.810731e+07</td>
      <td>4.024656e+07</td>
      <td>...</td>
      <td>125.114417</td>
      <td>121.748165</td>
      <td>121.748165</td>
      <td>77.968948</td>
      <td>73.275770</td>
      <td>76.166725</td>
      <td>74.003201</td>
      <td>76.966391</td>
      <td>75.679166</td>
      <td>75.679166</td>
    </tr>
    <tr>
      <th>18</th>
      <td>PRK</td>
      <td>Korea (the Democratic People's Republic of)</td>
      <td>82823.3</td>
      <td>8.344230e+04</td>
      <td>8.459620e+04</td>
      <td>8.394330e+04</td>
      <td>8.293700e+04</td>
      <td>2070582.5</td>
      <td>2.086058e+06</td>
      <td>2.114905e+06</td>
      <td>...</td>
      <td>15.169422</td>
      <td>17.492669</td>
      <td>17.492669</td>
      <td>-38.030793</td>
      <td>-9.988016</td>
      <td>-28.310326</td>
      <td>-3.195586</td>
      <td>-16.414407</td>
      <td>-19.169278</td>
      <td>-19.169278</td>
    </tr>
    <tr>
      <th>19</th>
      <td>THA</td>
      <td>Thailand</td>
      <td>1554254.0</td>
      <td>1.703328e+06</td>
      <td>1.714466e+06</td>
      <td>1.702989e+06</td>
      <td>1.553836e+06</td>
      <td>38856350.0</td>
      <td>4.258319e+07</td>
      <td>4.286164e+07</td>
      <td>...</td>
      <td>17.404685</td>
      <td>22.551331</td>
      <td>22.551331</td>
      <td>10.323662</td>
      <td>-4.559627</td>
      <td>32.066348</td>
      <td>46.173612</td>
      <td>16.011325</td>
      <td>20.266184</td>
      <td>20.266184</td>
    </tr>
    <tr>
      <th>20</th>
      <td>TWN</td>
      <td>Taiwan (Province of China)</td>
      <td>45838.7</td>
      <td>4.983830e+04</td>
      <td>4.999120e+04</td>
      <td>4.941410e+04</td>
      <td>4.915200e+04</td>
      <td>1145967.5</td>
      <td>1.245958e+06</td>
      <td>1.249780e+06</td>
      <td>...</td>
      <td>58.617135</td>
      <td>52.458032</td>
      <td>52.458032</td>
      <td>-71.622589</td>
      <td>-62.307893</td>
      <td>-74.143329</td>
      <td>-64.692890</td>
      <td>-82.919716</td>
      <td>-71.109302</td>
      <td>-71.109302</td>
    </tr>
    <tr>
      <th>21</th>
      <td>USA</td>
      <td>United States of America (the)</td>
      <td>364728.0</td>
      <td>4.386620e+05</td>
      <td>3.362555e+05</td>
      <td>4.121775e+05</td>
      <td>3.501365e+05</td>
      <td>9118200.0</td>
      <td>1.096655e+07</td>
      <td>8.406388e+06</td>
      <td>...</td>
      <td>69.713577</td>
      <td>78.850049</td>
      <td>78.850049</td>
      <td>55.821215</td>
      <td>63.101978</td>
      <td>49.895259</td>
      <td>59.792699</td>
      <td>51.694526</td>
      <td>56.553728</td>
      <td>56.553728</td>
    </tr>
    <tr>
      <th>22</th>
      <td>VNM</td>
      <td>Viet Nam</td>
      <td>1381744.4</td>
      <td>1.365174e+06</td>
      <td>1.360552e+06</td>
      <td>1.336231e+06</td>
      <td>1.318431e+06</td>
      <td>34543610.0</td>
      <td>3.412934e+07</td>
      <td>3.401379e+07</td>
      <td>...</td>
      <td>3.761740</td>
      <td>0.902428</td>
      <td>0.902428</td>
      <td>2.585962</td>
      <td>-8.687738</td>
      <td>-3.372544</td>
      <td>1.405162</td>
      <td>3.692293</td>
      <td>-0.906518</td>
      <td>-0.906518</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td>mean</td>
      <td>948478.0</td>
      <td>9.522272e+05</td>
      <td>9.590840e+05</td>
      <td>9.575896e+05</td>
      <td>9.316100e+05</td>
      <td>23711950.0</td>
      <td>2.380568e+07</td>
      <td>2.397710e+07</td>
      <td>...</td>
      <td>47.621862</td>
      <td>49.129925</td>
      <td>49.129925</td>
      <td>4.551116</td>
      <td>4.508756</td>
      <td>3.322003</td>
      <td>6.179080</td>
      <td>-1.533721</td>
      <td>3.599038</td>
      <td>3.599038</td>
    </tr>
    <tr>
      <th>24</th>
      <td>NaN</td>
      <td>total</td>
      <td>21814994.0</td>
      <td>2.190123e+07</td>
      <td>2.205893e+07</td>
      <td>2.202456e+07</td>
      <td>2.142703e+07</td>
      <td>545374850.0</td>
      <td>5.475306e+08</td>
      <td>5.514733e+08</td>
      <td>...</td>
      <td>1095.302835</td>
      <td>1129.988279</td>
      <td>1129.988279</td>
      <td>104.675658</td>
      <td>103.701389</td>
      <td>76.406059</td>
      <td>142.118831</td>
      <td>-35.275585</td>
      <td>82.777881</td>
      <td>82.777881</td>
    </tr>
  </tbody>
</table>
<p>25 rows × 73 columns</p>
</div>



### Merged Data to File


```python
outfile = "/Users/jnapolitano/Projects/wattime-takehome/wattime-takehome/data/MERGED_DATA.csv"

merged_df.to_csv(outfile)
```

### CO2 Difference Plots


```python
merged_df.plot(kind = "barh", x = 'country_name_FAOSTAT', y = ["CO2_diff_2015", "CO2_diff_2016",	"CO2_diff_2017", "CO2_diff_2018", "CO2_diff_2019"], xlabel = "Country Name", ylabel = "Tonnes CH4", figsize = (10,10))
```




    <AxesSubplot:ylabel='Country Name'>




    
![png](data_exploration_files/data_exploration_92_1.png)
    


### Percent Difference Plot


```python
merged_df.plot(kind = "barh", x = 'country_name_FAOSTAT', y = ["CO2_relative_percent_diff_2015", "CO2_relative_percent_diff_2016",	"CO2_relative_percent_diff_2017", "CO2_relative_percent_diff_2018", "CO2_relative_percent_diff_2019"], xlabel = "Country Name", ylabel = "Tonnes CH4", figsize=(10,10))
```




    <AxesSubplot:ylabel='Country Name'>




    
![png](data_exploration_files/data_exploration_94_1.png)
    

