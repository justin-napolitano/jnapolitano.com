+++
title =  "Model Design and Logistic Regression in Python"
date = "2022-06-17T13:20:32.169Z"
description = "Designing a logistic regression model from randomized bioinformatics data."
author = "Justin Napolitano"
categories = ['Python','Tutorials', 'Quantitative Analysis']
tags = ['julia','numerical-computing','Logistic Regression','statistics']
images = ['feature-image.png']
series = ["Quantitative Analysis in Python"]
+++

# Model Design and Logistic Regression in Python

I recently modeled customer churn in Julia with logistic regression model.  It was interesting to be sure, but I want to extend my analysis skillset by modeling biostatistics data.  In this post, I design a logistic regression model of health predictors.

## Imports


```python
# load some default Python modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-whitegrid')
from google.cloud import bigquery
from pprint import pprint
from datetime import date, datetime
import contextily as cx
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

```

## Data


### Data  Description

Chinese Longitudinal Healthy Longevity Survey (CLHLS), Biomarkers Datasets, 2009, 2012, 2014 (ICPSR 37226)
Principal Investigator(s): Yi Zeng, Duke University, and Peking University; James W. Vaupel, Max Planck Institutes, and Duke University


```python
filename = "/Users/jnapolitano/Projects/biostatistics/data/37226-0003-Data.tsv"
df = pd.read_csv(filename, sep='\t')
```


```python
# read data in pandas dataframe


# list first few rows (datapoints)
df.head()
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
      <th>ID</th>
      <th>TRUEAGE</th>
      <th>A1</th>
      <th>ALB</th>
      <th>GLU</th>
      <th>BUN</th>
      <th>CREA</th>
      <th>CHO</th>
      <th>TG</th>
      <th>GSP</th>
      <th>...</th>
      <th>RBC</th>
      <th>HGB</th>
      <th>HCT</th>
      <th>MCV</th>
      <th>MCH</th>
      <th>MCHC</th>
      <th>PLT</th>
      <th>MPV</th>
      <th>PDW</th>
      <th>PCT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>32160008</td>
      <td>95</td>
      <td>2</td>
      <td>30.60000038147</td>
      <td>4.230000019073</td>
      <td>6.860000133514</td>
      <td>64.90000152588</td>
      <td>3.5</td>
      <td>.8799999952316</td>
      <td>232.89999389649</td>
      <td>...</td>
      <td>3.5</td>
      <td>104</td>
      <td>29.14999961853</td>
      <td>82.69999694825</td>
      <td>29.5</td>
      <td>357</td>
      <td>394</td>
      <td>8.60000038147</td>
      <td>14.30000019074</td>
      <td>.33000001311</td>
    </tr>
    <tr>
      <th>1</th>
      <td>32161008</td>
      <td>95</td>
      <td>2</td>
      <td>39.09999847413</td>
      <td>6.94000005722</td>
      <td>16.190000534058</td>
      <td>152.39999389649</td>
      <td>4.619999885559</td>
      <td>1.2799999713898</td>
      <td>264.20001220704</td>
      <td>...</td>
      <td>3.2999999523163</td>
      <td>101.3000030518</td>
      <td>28.930000305176</td>
      <td>88.90000152588</td>
      <td>31.10000038147</td>
      <td>350</td>
      <td>149</td>
      <td>9.10000038147</td>
      <td>15</td>
      <td>.12999999523</td>
    </tr>
    <tr>
      <th>2</th>
      <td>32162608</td>
      <td>87</td>
      <td>2</td>
      <td>44.79999923707</td>
      <td>5.550000190735</td>
      <td>5.679999828339</td>
      <td>78.5</td>
      <td>5.199999809265</td>
      <td>2.3900001049042</td>
      <td>276.20001220704</td>
      <td>...</td>
      <td>3.5999999046326</td>
      <td>111.3000030518</td>
      <td>31.159999847412</td>
      <td>87.59999847413</td>
      <td>31.29999923707</td>
      <td>357</td>
      <td>201</td>
      <td>8.30000019074</td>
      <td>12</td>
      <td>.15999999642</td>
    </tr>
    <tr>
      <th>3</th>
      <td>32163008</td>
      <td>90</td>
      <td>2</td>
      <td>41.29999923707</td>
      <td>5.269999980927</td>
      <td>5.949999809265</td>
      <td>75.80000305176</td>
      <td>4.25</td>
      <td>1.5499999523163</td>
      <td>264.20001220704</td>
      <td>...</td>
      <td>3.7000000476837</td>
      <td>113.9000015259</td>
      <td>32.900001525879</td>
      <td>89.69999694825</td>
      <td>31.10000038147</td>
      <td>346</td>
      <td>150</td>
      <td>9.89999961854</td>
      <td>16.79999923707</td>
      <td>.1400000006</td>
    </tr>
    <tr>
      <th>4</th>
      <td>32164908</td>
      <td>94</td>
      <td>2</td>
      <td>39.90000152588</td>
      <td>7.05999994278</td>
      <td>6.039999961853</td>
      <td>90.80000305176</td>
      <td>7.139999866486</td>
      <td>2.3399999141693</td>
      <td>237.69999694825</td>
      <td>...</td>
      <td>4.1999998092651</td>
      <td>131.1999969483</td>
      <td>36.689998626709</td>
      <td>88.5</td>
      <td>31.60000038147</td>
      <td>358</td>
      <td>163</td>
      <td>9.69999980927</td>
      <td>17.79999923707</td>
      <td>.15000000596</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 33 columns</p>
</div>




```python
df.describe()
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
      <th>ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2.546000e+03</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>4.069177e+07</td>
    </tr>
    <tr>
      <th>std</th>
      <td>4.367164e+06</td>
    </tr>
    <tr>
      <th>min</th>
      <td>3.216001e+07</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>3.743344e+07</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>4.135976e+07</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>4.430106e+07</td>
    </tr>
    <tr>
      <th>max</th>
      <td>4.611231e+07</td>
    </tr>
  </tbody>
</table>
</div>



The float collumns were not interpretted correctly by pandas. I'll fix that


```python
df.columns
```




    Index(['ID', 'TRUEAGE', 'A1', 'ALB', 'GLU', 'BUN', 'CREA', 'CHO', 'TG', 'GSP',
           'CRPHS', 'UA', 'HDLC', 'SOD', 'MDA', 'VD3', 'VITB12', 'UALB', 'UCR',
           'UALBBYUCR', 'WBC', 'LYMPH', 'LYMPH_A', 'RBC', 'HGB', 'HCT', 'MCV',
           'MCH', 'MCHC', 'PLT', 'MPV', 'PDW', 'PCT'],
          dtype='object')




```python
# check datatypesdf
df.dtypes
```




    ID            int64
    TRUEAGE      object
    A1           object
    ALB          object
    GLU          object
    BUN          object
    CREA         object
    CHO          object
    TG           object
    GSP          object
    CRPHS        object
    UA           object
    HDLC         object
    SOD          object
    MDA          object
    VD3          object
    VITB12       object
    UALB         object
    UCR          object
    UALBBYUCR    object
    WBC          object
    LYMPH        object
    LYMPH_A      object
    RBC          object
    HGB          object
    HCT          object
    MCV          object
    MCH          object
    MCHC         object
    PLT          object
    MPV          object
    PDW          object
    PCT          object
    dtype: object



Everything was read an object.  I'll cast everything to numeric... Thank you numpy




```python
# replace empty space with na
df = df.replace(" ", np.nan)
```

just to be safe, I'll replace all blank spaces with np.nan.


```python
# convert numeric objects to numeric data types.  I checked in the code book there will not be any false positives
df = df.apply(pd.to_numeric, errors='raise')
```


```python
# Recheck dictypes
df.dtypes
```




    ID             int64
    TRUEAGE      float64
    A1           float64
    ALB          float64
    GLU          float64
    BUN          float64
    CREA         float64
    CHO          float64
    TG           float64
    GSP          float64
    CRPHS        float64
    UA           float64
    HDLC         float64
    SOD          float64
    MDA          float64
    VD3          float64
    VITB12       float64
    UALB         float64
    UCR          float64
    UALBBYUCR    float64
    WBC          float64
    LYMPH        float64
    LYMPH_A      float64
    RBC          float64
    HGB          float64
    HCT          float64
    MCV          float64
    MCH          float64
    MCHC         float64
    PLT          float64
    MPV          float64
    PDW          float64
    PCT          float64
    dtype: object




```python
# check statistics of the features
df.describe()
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
      <th>ID</th>
      <th>TRUEAGE</th>
      <th>A1</th>
      <th>ALB</th>
      <th>GLU</th>
      <th>BUN</th>
      <th>CREA</th>
      <th>CHO</th>
      <th>TG</th>
      <th>GSP</th>
      <th>...</th>
      <th>RBC</th>
      <th>HGB</th>
      <th>HCT</th>
      <th>MCV</th>
      <th>MCH</th>
      <th>MCHC</th>
      <th>PLT</th>
      <th>MPV</th>
      <th>PDW</th>
      <th>PCT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2.546000e+03</td>
      <td>2542.000000</td>
      <td>2542.000000</td>
      <td>2499.000000</td>
      <td>2499.000000</td>
      <td>2499.000000</td>
      <td>2499.000000</td>
      <td>2499.000000</td>
      <td>2499.000000</td>
      <td>2499.000000</td>
      <td>...</td>
      <td>2497.000000</td>
      <td>2497.000000</td>
      <td>2497.000000</td>
      <td>2497.000000</td>
      <td>2497.000000</td>
      <td>2497.000000</td>
      <td>2497.000000</td>
      <td>2487.000000</td>
      <td>2483.000000</td>
      <td>1711.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>4.069177e+07</td>
      <td>85.584972</td>
      <td>1.543273</td>
      <td>42.363345</td>
      <td>5.364794</td>
      <td>6.661321</td>
      <td>82.805642</td>
      <td>4.770340</td>
      <td>1.251369</td>
      <td>253.726811</td>
      <td>...</td>
      <td>4.165012</td>
      <td>127.684902</td>
      <td>38.664654</td>
      <td>94.532295</td>
      <td>31.033849</td>
      <td>323.221826</td>
      <td>195.033440</td>
      <td>9.322951</td>
      <td>16.114692</td>
      <td>0.244237</td>
    </tr>
    <tr>
      <th>std</th>
      <td>4.367164e+06</td>
      <td>12.061941</td>
      <td>0.498222</td>
      <td>4.367372</td>
      <td>1.802363</td>
      <td>2.355459</td>
      <td>29.246926</td>
      <td>1.010844</td>
      <td>0.757557</td>
      <td>38.658243</td>
      <td>...</td>
      <td>0.602123</td>
      <td>33.852642</td>
      <td>7.163306</td>
      <td>7.624568</td>
      <td>11.041158</td>
      <td>20.995983</td>
      <td>76.322382</td>
      <td>4.468129</td>
      <td>4.264532</td>
      <td>2.679986</td>
    </tr>
    <tr>
      <th>min</th>
      <td>3.216001e+07</td>
      <td>47.000000</td>
      <td>1.000000</td>
      <td>21.900000</td>
      <td>1.960000</td>
      <td>2.090000</td>
      <td>30.500000</td>
      <td>0.070000</td>
      <td>0.030000</td>
      <td>139.899994</td>
      <td>...</td>
      <td>1.910000</td>
      <td>13.000000</td>
      <td>0.280000</td>
      <td>54.799999</td>
      <td>15.900000</td>
      <td>3.900000</td>
      <td>9.000000</td>
      <td>0.000000</td>
      <td>5.500000</td>
      <td>0.020000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>3.743344e+07</td>
      <td>76.000000</td>
      <td>1.000000</td>
      <td>40.000000</td>
      <td>4.400000</td>
      <td>5.150000</td>
      <td>66.599998</td>
      <td>4.090000</td>
      <td>0.800000</td>
      <td>232.600006</td>
      <td>...</td>
      <td>3.780000</td>
      <td>115.000000</td>
      <td>35.400002</td>
      <td>91.300003</td>
      <td>29.500000</td>
      <td>317.000000</td>
      <td>150.000000</td>
      <td>8.200000</td>
      <td>15.300000</td>
      <td>0.140000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>4.135976e+07</td>
      <td>86.000000</td>
      <td>2.000000</td>
      <td>42.799999</td>
      <td>5.020000</td>
      <td>6.380000</td>
      <td>77.000000</td>
      <td>4.690000</td>
      <td>1.050000</td>
      <td>248.800003</td>
      <td>...</td>
      <td>4.160000</td>
      <td>127.000000</td>
      <td>39.000000</td>
      <td>95.400002</td>
      <td>31.200001</td>
      <td>325.000000</td>
      <td>189.000000</td>
      <td>9.300000</td>
      <td>16.000000</td>
      <td>0.170000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>4.430106e+07</td>
      <td>95.000000</td>
      <td>2.000000</td>
      <td>45.000000</td>
      <td>5.790000</td>
      <td>7.695000</td>
      <td>92.099998</td>
      <td>5.370000</td>
      <td>1.470000</td>
      <td>266.899994</td>
      <td>...</td>
      <td>4.540000</td>
      <td>140.000000</td>
      <td>42.700001</td>
      <td>98.900002</td>
      <td>32.500000</td>
      <td>333.000000</td>
      <td>229.000000</td>
      <td>10.300000</td>
      <td>16.799999</td>
      <td>0.210000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>4.611231e+07</td>
      <td>113.000000</td>
      <td>2.000000</td>
      <td>130.000000</td>
      <td>22.000000</td>
      <td>39.860001</td>
      <td>585.099976</td>
      <td>13.070000</td>
      <td>8.150000</td>
      <td>778.000000</td>
      <td>...</td>
      <td>7.210000</td>
      <td>1116.000000</td>
      <td>70.199997</td>
      <td>125.800003</td>
      <td>371.000000</td>
      <td>429.000000</td>
      <td>1514.000000</td>
      <td>107.000000</td>
      <td>153.000000</td>
      <td>111.000000</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 33 columns</p>
</div>



It is kind of odd that there are greater counts for some rows. I'll remove all na.

Checking for negative values and anything else I missed from the initial sql clean:


```python
df = df.dropna()
```


```python
df.describe()
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
      <th>ID</th>
      <th>TRUEAGE</th>
      <th>A1</th>
      <th>ALB</th>
      <th>GLU</th>
      <th>BUN</th>
      <th>CREA</th>
      <th>CHO</th>
      <th>TG</th>
      <th>GSP</th>
      <th>...</th>
      <th>RBC</th>
      <th>HGB</th>
      <th>HCT</th>
      <th>MCV</th>
      <th>MCH</th>
      <th>MCHC</th>
      <th>PLT</th>
      <th>MPV</th>
      <th>PDW</th>
      <th>PCT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1.561000e+03</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>...</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
      <td>1561.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>3.951369e+07</td>
      <td>84.782191</td>
      <td>1.534914</td>
      <td>42.445292</td>
      <td>5.334414</td>
      <td>6.898834</td>
      <td>84.107880</td>
      <td>4.806336</td>
      <td>1.243748</td>
      <td>254.537604</td>
      <td>...</td>
      <td>4.060587</td>
      <td>126.936387</td>
      <td>38.154004</td>
      <td>94.416284</td>
      <td>31.500461</td>
      <td>329.142217</td>
      <td>190.152082</td>
      <td>10.006560</td>
      <td>15.777220</td>
      <td>0.251365</td>
    </tr>
    <tr>
      <th>std</th>
      <td>4.702774e+06</td>
      <td>12.056596</td>
      <td>0.498939</td>
      <td>4.659920</td>
      <td>1.707653</td>
      <td>2.292577</td>
      <td>29.500260</td>
      <td>0.999193</td>
      <td>0.775910</td>
      <td>39.858537</td>
      <td>...</td>
      <td>0.589037</td>
      <td>39.956758</td>
      <td>5.261258</td>
      <td>7.701819</td>
      <td>11.723908</td>
      <td>16.978577</td>
      <td>71.839722</td>
      <td>4.453105</td>
      <td>5.142069</td>
      <td>2.805686</td>
    </tr>
    <tr>
      <th>min</th>
      <td>3.216101e+07</td>
      <td>48.000000</td>
      <td>1.000000</td>
      <td>21.900000</td>
      <td>1.960000</td>
      <td>2.140000</td>
      <td>30.500000</td>
      <td>0.340000</td>
      <td>0.070000</td>
      <td>139.899994</td>
      <td>...</td>
      <td>2.100000</td>
      <td>13.000000</td>
      <td>13.200000</td>
      <td>56.000000</td>
      <td>17.500000</td>
      <td>35.000000</td>
      <td>25.000000</td>
      <td>0.200000</td>
      <td>5.500000</td>
      <td>0.020000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>3.736671e+07</td>
      <td>76.000000</td>
      <td>1.000000</td>
      <td>39.900002</td>
      <td>4.400000</td>
      <td>5.370000</td>
      <td>67.000000</td>
      <td>4.120000</td>
      <td>0.780000</td>
      <td>231.600006</td>
      <td>...</td>
      <td>3.680000</td>
      <td>114.000000</td>
      <td>34.799999</td>
      <td>91.199997</td>
      <td>30.100000</td>
      <td>320.000000</td>
      <td>147.000000</td>
      <td>8.800000</td>
      <td>15.400000</td>
      <td>0.140000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>3.745741e+07</td>
      <td>85.000000</td>
      <td>2.000000</td>
      <td>42.900002</td>
      <td>4.990000</td>
      <td>6.610000</td>
      <td>77.599998</td>
      <td>4.730000</td>
      <td>1.040000</td>
      <td>249.800003</td>
      <td>...</td>
      <td>4.060000</td>
      <td>126.000000</td>
      <td>38.200001</td>
      <td>95.400002</td>
      <td>31.400000</td>
      <td>328.000000</td>
      <td>185.000000</td>
      <td>9.600000</td>
      <td>15.900000</td>
      <td>0.170000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>4.332561e+07</td>
      <td>94.000000</td>
      <td>2.000000</td>
      <td>45.099998</td>
      <td>5.780000</td>
      <td>7.960000</td>
      <td>93.199997</td>
      <td>5.420000</td>
      <td>1.460000</td>
      <td>268.899994</td>
      <td>...</td>
      <td>4.400000</td>
      <td>137.000000</td>
      <td>41.599998</td>
      <td>98.900002</td>
      <td>32.700001</td>
      <td>337.000000</td>
      <td>227.000000</td>
      <td>10.600000</td>
      <td>16.299999</td>
      <td>0.210000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>4.581641e+07</td>
      <td>113.000000</td>
      <td>2.000000</td>
      <td>130.000000</td>
      <td>20.760000</td>
      <td>23.549999</td>
      <td>392.000000</td>
      <td>8.490000</td>
      <td>8.150000</td>
      <td>778.000000</td>
      <td>...</td>
      <td>7.210000</td>
      <td>1116.000000</td>
      <td>70.199997</td>
      <td>125.800003</td>
      <td>371.000000</td>
      <td>408.000000</td>
      <td>1302.000000</td>
      <td>107.000000</td>
      <td>153.000000</td>
      <td>111.000000</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 33 columns</p>
</div>



We remove about 4/5 of our data.  The counts are now equivalent. Everything is in the correct data type.

#### Visualizing Age Distribution

I am curious what the age spread looks like. An even spread could be used to determine health outcomes.


```python
# plot histogram of fare
df.TRUEAGE.hist(figsize=(14,3))
plt.xlabel('Age')
plt.title('Histogram');
```


    
![png](logistic_regression_files/logistic_regression_24_0.png)
    


Unfortunately, the spread is not evenly distributed. 

#### Visualizing Age to Triglyceride Levels

A predictive model relating health factors to longevity is probably possible.   Certain factors must be met, but I'll assume they are for the sake of this mockup.  


```python
#idx = (df.trip_distance < 3) & (gdf.fare_amount < 100)
plt.scatter(df.TRUEAGE, df.TG)
plt.xlabel('True Age')
plt.ylabel('Triglyceride, mmol/L')

# theta here is estimated by hand
plt.show()
```


    
![png](logistic_regression_files/logistic_regression_26_0.png)
    


## Filter Examples

The data above doesn't really need to be filtered.  To demonstrate how it could be, I include some randomized columns that are then filtered according to specific conditions.

To fit the specificities of the conditions in the training video I'll add some randomized columns.  


```python
n = df.shape[0]
lower_bound = 0 #inclusive
upper_bound = 2 # exclusive
emergency_department =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["EMERGENCY"] = emergency_department

```


```python
n = df.shape[0]
lower_bound = 0 #inclusive
upper_bound = 100 # exclusive
cancer_care =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["CANCER_TYPE"] = cancer_care
```


```python
n = df.shape[0]
lower_bound = 0 #inclusive 
#0 = no
#1 = ICPI
# 2 MONO 
upper_bound = 3 # exclusive
icpi_history =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["ICPI_HIST"] = icpi_history
```


```python
n = df.shape[0]
lower_bound = 0 #inclusive
upper_bound = 2# exclusive
# Spanish = 0
# English = 1
# Arbitrarily chosen. 
language =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["LANG"] = language
```


```python
n = df.shape[0]
lower_bound = 0 #inclusive
upper_bound = 2 # exclusive
follow_up =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["FOLLOW_UP"] = follow_up
```


```python
n = df.shape[0]
lower_bound = 0 #inclusive
upper_bound = 2 # exclusive
# 0 = no
# 1 = Yes
cons =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["CONSENT"] = cons
```


```python
n = df.shape[0]
lower_bound = 0 #inclusive
upper_bound = 2 # exclusive
# 0 = no
# 1 = Yes
prego =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["PREGNANT"] = prego
```


```python
df
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
      <th>ID</th>
      <th>TRUEAGE</th>
      <th>A1</th>
      <th>ALB</th>
      <th>GLU</th>
      <th>BUN</th>
      <th>CREA</th>
      <th>CHO</th>
      <th>TG</th>
      <th>GSP</th>
      <th>...</th>
      <th>MPV</th>
      <th>PDW</th>
      <th>PCT</th>
      <th>EMERGENCY</th>
      <th>CANCER_TYPE</th>
      <th>ICPI_HIST</th>
      <th>LANG</th>
      <th>FOLLOW_UP</th>
      <th>CONSENT</th>
      <th>PREGNANT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>32161008</td>
      <td>95.0</td>
      <td>2.0</td>
      <td>39.099998</td>
      <td>6.94</td>
      <td>16.190001</td>
      <td>152.399994</td>
      <td>4.62</td>
      <td>1.28</td>
      <td>264.200012</td>
      <td>...</td>
      <td>9.1</td>
      <td>15.000000</td>
      <td>0.13</td>
      <td>1</td>
      <td>20</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>32162608</td>
      <td>87.0</td>
      <td>2.0</td>
      <td>44.799999</td>
      <td>5.55</td>
      <td>5.680000</td>
      <td>78.500000</td>
      <td>5.20</td>
      <td>2.39</td>
      <td>276.200012</td>
      <td>...</td>
      <td>8.3</td>
      <td>12.000000</td>
      <td>0.16</td>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>32163008</td>
      <td>90.0</td>
      <td>2.0</td>
      <td>41.299999</td>
      <td>5.27</td>
      <td>5.950000</td>
      <td>75.800003</td>
      <td>4.25</td>
      <td>1.55</td>
      <td>264.200012</td>
      <td>...</td>
      <td>9.9</td>
      <td>16.799999</td>
      <td>0.14</td>
      <td>0</td>
      <td>36</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>32166108</td>
      <td>89.0</td>
      <td>2.0</td>
      <td>45.000000</td>
      <td>8.80</td>
      <td>13.170000</td>
      <td>147.000000</td>
      <td>3.19</td>
      <td>1.72</td>
      <td>336.399994</td>
      <td>...</td>
      <td>8.2</td>
      <td>12.300000</td>
      <td>0.12</td>
      <td>1</td>
      <td>84</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>32167608</td>
      <td>100.0</td>
      <td>2.0</td>
      <td>40.099998</td>
      <td>4.34</td>
      <td>5.950000</td>
      <td>76.000000</td>
      <td>5.67</td>
      <td>1.44</td>
      <td>223.300003</td>
      <td>...</td>
      <td>10.8</td>
      <td>16.400000</td>
      <td>0.20</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2265</th>
      <td>45816014</td>
      <td>98.0</td>
      <td>2.0</td>
      <td>37.000000</td>
      <td>6.04</td>
      <td>5.010000</td>
      <td>59.299999</td>
      <td>3.84</td>
      <td>0.95</td>
      <td>195.300003</td>
      <td>...</td>
      <td>9.9</td>
      <td>16.200001</td>
      <td>0.26</td>
      <td>0</td>
      <td>6</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2266</th>
      <td>45816114</td>
      <td>69.0</td>
      <td>1.0</td>
      <td>46.299999</td>
      <td>5.99</td>
      <td>5.030000</td>
      <td>85.500000</td>
      <td>4.43</td>
      <td>1.44</td>
      <td>224.000000</td>
      <td>...</td>
      <td>10.4</td>
      <td>16.000000</td>
      <td>0.23</td>
      <td>1</td>
      <td>31</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2267</th>
      <td>45816214</td>
      <td>93.0</td>
      <td>2.0</td>
      <td>42.599998</td>
      <td>5.53</td>
      <td>6.320000</td>
      <td>85.500000</td>
      <td>4.03</td>
      <td>0.92</td>
      <td>249.800003</td>
      <td>...</td>
      <td>11.1</td>
      <td>16.299999</td>
      <td>0.14</td>
      <td>1</td>
      <td>39</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2268</th>
      <td>45816314</td>
      <td>91.0</td>
      <td>2.0</td>
      <td>43.400002</td>
      <td>5.82</td>
      <td>7.770000</td>
      <td>72.099998</td>
      <td>4.29</td>
      <td>1.08</td>
      <td>259.299988</td>
      <td>...</td>
      <td>10.0</td>
      <td>15.900000</td>
      <td>0.20</td>
      <td>1</td>
      <td>57</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2269</th>
      <td>45816414</td>
      <td>93.0</td>
      <td>2.0</td>
      <td>42.900002</td>
      <td>5.10</td>
      <td>5.010000</td>
      <td>59.799999</td>
      <td>4.94</td>
      <td>1.82</td>
      <td>236.399994</td>
      <td>...</td>
      <td>8.7</td>
      <td>16.299999</td>
      <td>0.21</td>
      <td>1</td>
      <td>32</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>1561 rows × 40 columns</p>
</div>



### Writing the Filter

Writing a quick filter to ensure eligibiity.  This could, and probably should be written functionally, but so it goes.


```python
# Greater than 18
# CANCER TYPE IS NOT equal to a non-malanoma skin cancer ie 5 arbitrarily chosen 
# Patient Seeking care in emergency department is true
# History is not equal to 0. Ie not recieving either.  IDK how it would be provided.  It could also possibly be written as equal to 1 or 2
# Lang is either english or spanish
# Patient Agrees to Follow Up
# Patient Consents
# Patient is Not Pregnant

idx_spanish = (df.TRUEAGE > 18) & (df.CANCER_TYPE != 5) & (df.EMERGENCY == 1) & \
        (df.ICPI_HIST == 0) & (df.LANG == 0) & (df.FOLLOW_UP == 1) & (df.CONSENT == 1) & (df.PREGNANT == 0)

# Ideally the english and spanish speakers would have been filtered prior to this, but for the sake of exploration this will work. 
idx_english = (df.TRUEAGE > 18) & (df.CANCER_TYPE != 5) & (df.EMERGENCY == 1) & \
        (df.ICPI_HIST == 0) & (df.LANG == 1) & (df.FOLLOW_UP == 1) & (df.CONSENT == 1) & (df.PREGNANT == 0)

```

I created spanish and english dataframes for the sake of data manipulation.  It is not realy necessary, but it would permit modifying and recoding the data if it were formatted differently.


```python

filtered_df = pd.concat([df[idx_english], df[idx_spanish]], ignore_index=True)
```

the filtered df is a concattenation of the english and spanish filtered data.


```python
filtered_df.describe()
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
      <th>ID</th>
      <th>TRUEAGE</th>
      <th>A1</th>
      <th>ALB</th>
      <th>GLU</th>
      <th>BUN</th>
      <th>CREA</th>
      <th>CHO</th>
      <th>TG</th>
      <th>GSP</th>
      <th>...</th>
      <th>MPV</th>
      <th>PDW</th>
      <th>PCT</th>
      <th>EMERGENCY</th>
      <th>CANCER_TYPE</th>
      <th>ICPI_HIST</th>
      <th>LANG</th>
      <th>FOLLOW_UP</th>
      <th>CONSENT</th>
      <th>PREGNANT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>3.300000e+01</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>...</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.000000</td>
      <td>33.0</td>
      <td>33.000000</td>
      <td>33.0</td>
      <td>33.000000</td>
      <td>33.0</td>
      <td>33.0</td>
      <td>33.0</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>4.023138e+07</td>
      <td>85.000000</td>
      <td>1.636364</td>
      <td>41.563636</td>
      <td>5.139697</td>
      <td>6.289394</td>
      <td>83.718182</td>
      <td>4.893030</td>
      <td>1.168788</td>
      <td>244.539395</td>
      <td>...</td>
      <td>9.715151</td>
      <td>14.945455</td>
      <td>0.202424</td>
      <td>1.0</td>
      <td>49.969697</td>
      <td>0.0</td>
      <td>0.575758</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>std</th>
      <td>4.523359e+06</td>
      <td>12.080459</td>
      <td>0.488504</td>
      <td>5.748577</td>
      <td>1.516953</td>
      <td>1.695724</td>
      <td>28.692055</td>
      <td>1.158084</td>
      <td>0.510090</td>
      <td>30.776044</td>
      <td>...</td>
      <td>1.466953</td>
      <td>1.866161</td>
      <td>0.080856</td>
      <td>0.0</td>
      <td>26.886898</td>
      <td>0.0</td>
      <td>0.501890</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>min</th>
      <td>3.244411e+07</td>
      <td>64.000000</td>
      <td>1.000000</td>
      <td>29.600000</td>
      <td>3.350000</td>
      <td>3.550000</td>
      <td>43.700001</td>
      <td>3.160000</td>
      <td>0.410000</td>
      <td>196.600006</td>
      <td>...</td>
      <td>7.400000</td>
      <td>9.800000</td>
      <td>0.070000</td>
      <td>1.0</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>3.744541e+07</td>
      <td>75.000000</td>
      <td>1.000000</td>
      <td>36.900002</td>
      <td>4.360000</td>
      <td>4.660000</td>
      <td>64.500000</td>
      <td>3.940000</td>
      <td>0.800000</td>
      <td>226.800003</td>
      <td>...</td>
      <td>8.800000</td>
      <td>15.100000</td>
      <td>0.160000</td>
      <td>1.0</td>
      <td>33.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>4.222571e+07</td>
      <td>85.000000</td>
      <td>2.000000</td>
      <td>42.700001</td>
      <td>4.750000</td>
      <td>6.310000</td>
      <td>78.900002</td>
      <td>4.730000</td>
      <td>1.150000</td>
      <td>235.399994</td>
      <td>...</td>
      <td>9.600000</td>
      <td>15.700000</td>
      <td>0.180000</td>
      <td>1.0</td>
      <td>55.000000</td>
      <td>0.0</td>
      <td>1.000000</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>4.460501e+07</td>
      <td>94.000000</td>
      <td>2.000000</td>
      <td>46.200001</td>
      <td>5.210000</td>
      <td>7.250000</td>
      <td>100.199997</td>
      <td>5.800000</td>
      <td>1.410000</td>
      <td>273.600006</td>
      <td>...</td>
      <td>10.600000</td>
      <td>16.100000</td>
      <td>0.240000</td>
      <td>1.0</td>
      <td>69.000000</td>
      <td>0.0</td>
      <td>1.000000</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>max</th>
      <td>4.581561e+07</td>
      <td>102.000000</td>
      <td>2.000000</td>
      <td>50.299999</td>
      <td>11.350000</td>
      <td>10.000000</td>
      <td>151.699997</td>
      <td>7.220000</td>
      <td>2.770000</td>
      <td>310.899994</td>
      <td>...</td>
      <td>14.300000</td>
      <td>16.799999</td>
      <td>0.440000</td>
      <td>1.0</td>
      <td>91.000000</td>
      <td>0.0</td>
      <td>1.000000</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 40 columns</p>
</div>




```python
filtered_df.shape[0]
#only 33 left following the filter. 
```




    33



Following the filter only 35 data are left in the set.  A workflow similiar to this could be used to identify possible survey recruits from aggregated chart data.  

## Logistic Regression Sample

I am surpirsed by the low level of samples left following the filter.  To avoid a small n, I will use the initial dataset. 



```python
filename = "/Users/jnapolitano/Projects/biostatistics/data/37226-0003-Data.tsv"
df = pd.read_csv(filename, sep='\t')

# replace empty space with na
df = df.replace(" ", np.nan)

# convert numeric objects to numeric data types.  I checked in the code book there will not be any false positives
df = df.apply(pd.to_numeric, errors='raise')
df = df.dropna()
```


```python
df
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
      <th>ID</th>
      <th>TRUEAGE</th>
      <th>A1</th>
      <th>ALB</th>
      <th>GLU</th>
      <th>BUN</th>
      <th>CREA</th>
      <th>CHO</th>
      <th>TG</th>
      <th>GSP</th>
      <th>...</th>
      <th>RBC</th>
      <th>HGB</th>
      <th>HCT</th>
      <th>MCV</th>
      <th>MCH</th>
      <th>MCHC</th>
      <th>PLT</th>
      <th>MPV</th>
      <th>PDW</th>
      <th>PCT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>32161008</td>
      <td>95.0</td>
      <td>2.0</td>
      <td>39.099998</td>
      <td>6.94</td>
      <td>16.190001</td>
      <td>152.399994</td>
      <td>4.62</td>
      <td>1.28</td>
      <td>264.200012</td>
      <td>...</td>
      <td>3.30</td>
      <td>101.300003</td>
      <td>28.930000</td>
      <td>88.900002</td>
      <td>31.100000</td>
      <td>350.0</td>
      <td>149.0</td>
      <td>9.1</td>
      <td>15.000000</td>
      <td>0.13</td>
    </tr>
    <tr>
      <th>2</th>
      <td>32162608</td>
      <td>87.0</td>
      <td>2.0</td>
      <td>44.799999</td>
      <td>5.55</td>
      <td>5.680000</td>
      <td>78.500000</td>
      <td>5.20</td>
      <td>2.39</td>
      <td>276.200012</td>
      <td>...</td>
      <td>3.60</td>
      <td>111.300003</td>
      <td>31.160000</td>
      <td>87.599998</td>
      <td>31.299999</td>
      <td>357.0</td>
      <td>201.0</td>
      <td>8.3</td>
      <td>12.000000</td>
      <td>0.16</td>
    </tr>
    <tr>
      <th>3</th>
      <td>32163008</td>
      <td>90.0</td>
      <td>2.0</td>
      <td>41.299999</td>
      <td>5.27</td>
      <td>5.950000</td>
      <td>75.800003</td>
      <td>4.25</td>
      <td>1.55</td>
      <td>264.200012</td>
      <td>...</td>
      <td>3.70</td>
      <td>113.900002</td>
      <td>32.900002</td>
      <td>89.699997</td>
      <td>31.100000</td>
      <td>346.0</td>
      <td>150.0</td>
      <td>9.9</td>
      <td>16.799999</td>
      <td>0.14</td>
    </tr>
    <tr>
      <th>6</th>
      <td>32166108</td>
      <td>89.0</td>
      <td>2.0</td>
      <td>45.000000</td>
      <td>8.80</td>
      <td>13.170000</td>
      <td>147.000000</td>
      <td>3.19</td>
      <td>1.72</td>
      <td>336.399994</td>
      <td>...</td>
      <td>3.00</td>
      <td>92.599998</td>
      <td>26.340000</td>
      <td>88.500000</td>
      <td>31.100000</td>
      <td>352.0</td>
      <td>157.0</td>
      <td>8.2</td>
      <td>12.300000</td>
      <td>0.12</td>
    </tr>
    <tr>
      <th>7</th>
      <td>32167608</td>
      <td>100.0</td>
      <td>2.0</td>
      <td>40.099998</td>
      <td>4.34</td>
      <td>5.950000</td>
      <td>76.000000</td>
      <td>5.67</td>
      <td>1.44</td>
      <td>223.300003</td>
      <td>...</td>
      <td>3.76</td>
      <td>114.000000</td>
      <td>35.400002</td>
      <td>94.099998</td>
      <td>30.299999</td>
      <td>322.0</td>
      <td>193.0</td>
      <td>10.8</td>
      <td>16.400000</td>
      <td>0.20</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2265</th>
      <td>45816014</td>
      <td>98.0</td>
      <td>2.0</td>
      <td>37.000000</td>
      <td>6.04</td>
      <td>5.010000</td>
      <td>59.299999</td>
      <td>3.84</td>
      <td>0.95</td>
      <td>195.300003</td>
      <td>...</td>
      <td>4.31</td>
      <td>122.000000</td>
      <td>38.900002</td>
      <td>90.300003</td>
      <td>28.299999</td>
      <td>313.0</td>
      <td>267.0</td>
      <td>9.9</td>
      <td>16.200001</td>
      <td>0.26</td>
    </tr>
    <tr>
      <th>2266</th>
      <td>45816114</td>
      <td>69.0</td>
      <td>1.0</td>
      <td>46.299999</td>
      <td>5.99</td>
      <td>5.030000</td>
      <td>85.500000</td>
      <td>4.43</td>
      <td>1.44</td>
      <td>224.000000</td>
      <td>...</td>
      <td>4.46</td>
      <td>133.000000</td>
      <td>42.200001</td>
      <td>94.599998</td>
      <td>29.799999</td>
      <td>315.0</td>
      <td>230.0</td>
      <td>10.4</td>
      <td>16.000000</td>
      <td>0.23</td>
    </tr>
    <tr>
      <th>2267</th>
      <td>45816214</td>
      <td>93.0</td>
      <td>2.0</td>
      <td>42.599998</td>
      <td>5.53</td>
      <td>6.320000</td>
      <td>85.500000</td>
      <td>4.03</td>
      <td>0.92</td>
      <td>249.800003</td>
      <td>...</td>
      <td>4.60</td>
      <td>137.000000</td>
      <td>43.799999</td>
      <td>95.199997</td>
      <td>29.799999</td>
      <td>313.0</td>
      <td>129.0</td>
      <td>11.1</td>
      <td>16.299999</td>
      <td>0.14</td>
    </tr>
    <tr>
      <th>2268</th>
      <td>45816314</td>
      <td>91.0</td>
      <td>2.0</td>
      <td>43.400002</td>
      <td>5.82</td>
      <td>7.770000</td>
      <td>72.099998</td>
      <td>4.29</td>
      <td>1.08</td>
      <td>259.299988</td>
      <td>...</td>
      <td>4.14</td>
      <td>122.000000</td>
      <td>39.000000</td>
      <td>94.300003</td>
      <td>29.500000</td>
      <td>312.0</td>
      <td>200.0</td>
      <td>10.0</td>
      <td>15.900000</td>
      <td>0.20</td>
    </tr>
    <tr>
      <th>2269</th>
      <td>45816414</td>
      <td>93.0</td>
      <td>2.0</td>
      <td>42.900002</td>
      <td>5.10</td>
      <td>5.010000</td>
      <td>59.799999</td>
      <td>4.94</td>
      <td>1.82</td>
      <td>236.399994</td>
      <td>...</td>
      <td>4.50</td>
      <td>128.000000</td>
      <td>40.900002</td>
      <td>90.800003</td>
      <td>28.400000</td>
      <td>313.0</td>
      <td>240.0</td>
      <td>8.7</td>
      <td>16.299999</td>
      <td>0.21</td>
    </tr>
  </tbody>
</table>
<p>1561 rows × 33 columns</p>
</div>



### The Model

There is strong suspicion that biomarkers can determine whether a patient should be admitted for emergency care.  In this simplified model, I will randomly distribute proper disposition across the dataset. 


```python
n = df.shape[0]
lower_bound = 0 #inclusive
upper_bound = 2 # exclusive
# 0 = no
# 1 = Yes
tmp =  np.random.randint(low=lower_bound , high = upper_bound, size = n)
df["PROP_DISPOSITION"] = tmp
```

### Create Test and Train Set

This could be randomly sampled as well...

#### Random Sample


```python
# copy in memory to avoid errors.  This could be done from files or in other ways if memory is limited.  
master_table = df.copy()
```

### Test Sample Set with 10,000 Randomly Selected from the Master with Replacement


```python
test_sample = master_table.sample(n=20000,replace=True)

```


```python
targets = test_sample.pop("PROP_DISPOSITION")
```

#### Seperate Train and Test Sets


```python
x_train, x_test, y_train, y_test = train_test_split(test_sample, targets, test_size=0.2, random_state=0)
```

#### Data Standardization

Calculate the mean and standard deviation for each column.
Subtract the corresponding mean from each element.
Divide the obtained difference by the corresponding standard deviation.


Thankfully this is built into SKLearn.  


```python
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
```

### Create the Model


```python
model = LogisticRegression(solver='liblinear', C=0.05, multi_class='ovr',
                           random_state=0)
model.fit(x_train, y_train)
```




    LogisticRegression(C=0.05, multi_class='ovr', random_state=0,
                       solver='liblinear')



### Evaluate Model


```python
x_test = scaler.transform(x_test)
```


```python
y_pred = model.predict(x_test)
```

### Model Scoring

With completely randomized values the score should be about 50%. If it is significantly greater than there is probably a problem with the model.  


```python
model.score(x_train, y_train)

```




    0.5676875




```python
model.score(x_test, y_test)
```




    0.55825



Results are expected

### Confusion matrix


```python
cm = confusion_matrix(y_test, y_pred)
font_size = 10

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(cm)
ax.grid(False)
ax.set_xlabel('Predicted outputs', color='purple')
ax.set_ylabel('Actual outputs', color='purple')
ax.xaxis.set(ticks=range(len(cm)))
ax.yaxis.set(ticks=range(len(cm)))
#ax.set_ylim(0, 1)
for i in range(len(cm)):
    for j in range(len(cm)):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='purple')
plt.show()
```


    
![png](logistic_regression_files/logistic_regression_71_0.png)
    


Because the data is randomized it makes the model is accurate about 50% of the time.  

### Printing the Classification Report


```python
print(classification_report(y_test, y_pred))
```

                  precision    recall  f1-score   support
    
               0       0.55      0.47      0.51      1927
               1       0.56      0.64      0.60      2073
    
        accuracy                           0.56      4000
       macro avg       0.56      0.56      0.55      4000
    weighted avg       0.56      0.56      0.55      4000
    

