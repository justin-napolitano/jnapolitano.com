+++
title =  "Potential Carbon and Hydrogen Storage Wells Near Pipelines"
date = "2022-05-06T05:30:32.169Z"
description = "Identifying potential carbon and hydrogen storage facilities from spent well data."
author = "Justin Napolitano"
image = "post-image.png"
featuredimage = "post-image.png"
categories = ['Carbon Markets', 'Carbon Capture', 'Hydrogen Markets', 'Energy Sector', 'Geographic Information Systems', 'Liquified Natural Gas Markets', 'Economic Modeling']
tags = ['carbon', 'hydrogen', 'gis', 'lng', 'python', 'carbon']
series = ['North American Energy']
+++

# Potential Carbon Storage Wells Near Pipelines

## Import and Procedural Functions


```python
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import contextily as cx
import rtree
from zlib import crc32
import hashlib
from shapely.geometry import Point, LineString, Polygon
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point
from haversine import Unit
from geopy.distance import distance
```

## Query Plan

### Restrictions
* Must be near a pipeline terminal

### Imports 

* Pipeline Data
* Well Data

### Filtering

* For each well calculate nearest pipeline

* For each well calculate geographic distance from pipeline

* eliminate wells further than 2 km from a pipeline


## Data Frame Import

### Wells Dataframe


```python
## Importing our DataFrames

gisfilepath = "/Users/jnapolitano/Projects/data/energy/non-active-wells.geojson"


wells_df = gpd.read_file(gisfilepath)

wells_df = wells_df.to_crs(epsg=3857)
```


```python
wells_df.columns
```




    Index(['index', 'OBJECTID', 'ID', 'NAME', 'STATE', 'TYPE', 'STATUS', 'COUNTY',
           'COUNTYFIPS', 'COUNTRY', 'LATITUDE', 'LONGITUDE', 'NAICS_CODE',
           'NAICS_DESC', 'SOURCE', 'SOURCEDATE', 'VAL_METHOD', 'VAL_DATE',
           'WEBSITE', 'WELLIDNO', 'API', 'PERMITNO', 'OPERATOR', 'OPERATORID',
           'PRODTYPE', 'COORDTYPE', 'SURF_LAT', 'SURF_LONG', 'BOT_LAT', 'BOT_LONG',
           'POSREL', 'FIELD', 'COMPDATE', 'TOTDEPTH', 'STAUTS_CAT', 'geometry'],
          dtype='object')



### Pipeline DataFrame


```python
## Importing Pipeline Dataframe

gisfilepath = "/Users/jnapolitano/Projects/data/energy/Natural_Gas_Pipelines.geojson"


pipeline_df = gpd.read_file(gisfilepath)

pipeline_df = pipeline_df.to_crs(epsg=3857)
```

#### Removing Gathering Pipes from the Data


```python
pipeline_df.drop(pipeline_df[pipeline_df['TYPEPIPE'] == 'Gathering'].index, inplace = True)
```

#### Adding PipeGeometry Column


```python
pipeline_df['PipeGeometry'] = pipeline_df['geometry'].copy()
```


```python
pipeline_df.columns
```




    Index(['FID', 'TYPEPIPE', 'Operator', 'Shape_Leng', 'Shape__Length',
           'geometry', 'PipeGeometry'],
          dtype='object')



## Joining Well and Pipeline Data


```python
nearest_wells_df= wells_df.sjoin_nearest(pipeline_df, how = 'left', distance_col="distance_euclidian")
nearest_wells_df.columns

```




    Index(['index', 'OBJECTID', 'ID', 'NAME', 'STATE', 'TYPE', 'STATUS', 'COUNTY',
           'COUNTYFIPS', 'COUNTRY', 'LATITUDE', 'LONGITUDE', 'NAICS_CODE',
           'NAICS_DESC', 'SOURCE', 'SOURCEDATE', 'VAL_METHOD', 'VAL_DATE',
           'WEBSITE', 'WELLIDNO', 'API', 'PERMITNO', 'OPERATOR', 'OPERATORID',
           'PRODTYPE', 'COORDTYPE', 'SURF_LAT', 'SURF_LONG', 'BOT_LAT', 'BOT_LONG',
           'POSREL', 'FIELD', 'COMPDATE', 'TOTDEPTH', 'STAUTS_CAT', 'geometry',
           'index_right', 'FID', 'TYPEPIPE', 'Operator', 'Shape_Leng',
           'Shape__Length', 'PipeGeometry', 'distance_euclidian'],
          dtype='object')




```python
nearest_wells_df
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
      <th>index</th>
      <th>OBJECTID</th>
      <th>ID</th>
      <th>NAME</th>
      <th>STATE</th>
      <th>TYPE</th>
      <th>STATUS</th>
      <th>COUNTY</th>
      <th>COUNTYFIPS</th>
      <th>COUNTRY</th>
      <th>...</th>
      <th>STAUTS_CAT</th>
      <th>geometry</th>
      <th>index_right</th>
      <th>FID</th>
      <th>TYPEPIPE</th>
      <th>Operator</th>
      <th>Shape_Leng</th>
      <th>Shape__Length</th>
      <th>PipeGeometry</th>
      <th>distance_euclidian</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>720167</td>
      <td>720168</td>
      <td>W560039024</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>NON-ACTIVE WELL</td>
      <td>JOHNSON</td>
      <td>56019</td>
      <td>USA</td>
      <td>...</td>
      <td>1</td>
      <td>POINT (-11831144.797 5549191.441)</td>
      <td>30227</td>
      <td>30228</td>
      <td>Interstate</td>
      <td>Bison Pipeline</td>
      <td>1.278462</td>
      <td>173030.322980</td>
      <td>LINESTRING (-11790336.630 5494422.424, -117865...</td>
      <td>44625.275370</td>
    </tr>
    <tr>
      <th>1</th>
      <td>708507</td>
      <td>708508</td>
      <td>W560027364</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>NON-ACTIVE WELL</td>
      <td>CARBON</td>
      <td>56007</td>
      <td>USA</td>
      <td>...</td>
      <td>1</td>
      <td>POINT (-11976297.510 5042534.715)</td>
      <td>31358</td>
      <td>31359</td>
      <td>Interstate</td>
      <td>Questar Pipeline Co.</td>
      <td>0.268145</td>
      <td>30447.011086</td>
      <td>LINESTRING (-11984506.320 5012658.646, -119851...</td>
      <td>30816.842943</td>
    </tr>
    <tr>
      <th>2</th>
      <td>715428</td>
      <td>715429</td>
      <td>W560034285</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>NON-ACTIVE WELL</td>
      <td>FREMONT</td>
      <td>56013</td>
      <td>USA</td>
      <td>...</td>
      <td>1</td>
      <td>POINT (-12044048.444 5207896.951)</td>
      <td>27131</td>
      <td>27132</td>
      <td>Interstate</td>
      <td>Southern Star Central Gas PL Co.</td>
      <td>0.076245</td>
      <td>9557.779719</td>
      <td>LINESTRING (-12038734.497 5151818.779, -120317...</td>
      <td>50999.469183</td>
    </tr>
    <tr>
      <th>3</th>
      <td>708591</td>
      <td>708592</td>
      <td>W560027448</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>NON-ACTIVE WELL</td>
      <td>CARBON</td>
      <td>56007</td>
      <td>USA</td>
      <td>...</td>
      <td>1</td>
      <td>POINT (-11992810.532 5106126.430)</td>
      <td>27138</td>
      <td>27139</td>
      <td>Interstate</td>
      <td>Southern Star Central Gas PL Co.</td>
      <td>0.114048</td>
      <td>12695.765286</td>
      <td>LINESTRING (-11980997.975 5107748.211, -119936...</td>
      <td>1621.781149</td>
    </tr>
    <tr>
      <th>4</th>
      <td>715495</td>
      <td>715496</td>
      <td>W560034352</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>NON-ACTIVE WELL</td>
      <td>FREMONT</td>
      <td>56013</td>
      <td>USA</td>
      <td>...</td>
      <td>1</td>
      <td>POINT (-12008860.576 5221474.537)</td>
      <td>30360</td>
      <td>30361</td>
      <td>Interstate</td>
      <td>Tallgrass Interstate Gas Transmission</td>
      <td>0.141284</td>
      <td>17069.395563</td>
      <td>LINESTRING (-12038891.235 5265881.681, -120248...</td>
      <td>53608.161741</td>
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
      <th>160441</th>
      <td>681337</td>
      <td>681338</td>
      <td>W560000194</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>STORAGE WELL/MAINTENANCE WELL/OBSERVATION WELL</td>
      <td>HOT SPRINGS</td>
      <td>56017</td>
      <td>USA</td>
      <td>...</td>
      <td>4</td>
      <td>POINT (-12088044.133 5432638.661)</td>
      <td>27457</td>
      <td>27458</td>
      <td>Interstate</td>
      <td>Williston Basin Interstate PL Co.</td>
      <td>0.122880</td>
      <td>13678.939029</td>
      <td>LINESTRING (-12027891.088 5426896.907, -120415...</td>
      <td>46827.452302</td>
    </tr>
    <tr>
      <th>160442</th>
      <td>681764</td>
      <td>681765</td>
      <td>W560000621</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>STORAGE WELL/MAINTENANCE WELL/OBSERVATION WELL</td>
      <td>NATRONA</td>
      <td>56025</td>
      <td>USA</td>
      <td>...</td>
      <td>4</td>
      <td>POINT (-11835017.602 5370182.897)</td>
      <td>13162</td>
      <td>13163</td>
      <td>Interstate</td>
      <td>MIGC Pipeline System</td>
      <td>0.336895</td>
      <td>38635.742298</td>
      <td>LINESTRING (-11751892.222 5349172.198, -117585...</td>
      <td>55995.518283</td>
    </tr>
    <tr>
      <th>160443</th>
      <td>681344</td>
      <td>681345</td>
      <td>W560000201</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>STORAGE WELL/MAINTENANCE WELL/OBSERVATION WELL</td>
      <td>HOT SPRINGS</td>
      <td>56017</td>
      <td>USA</td>
      <td>...</td>
      <td>4</td>
      <td>POINT (-12094765.493 5453280.825)</td>
      <td>3383</td>
      <td>3384</td>
      <td>Interstate</td>
      <td>Colorado Interstate Gas Co.</td>
      <td>0.417645</td>
      <td>59503.770559</td>
      <td>LINESTRING (-12026665.683 5436962.405, -120527...</td>
      <td>54038.158553</td>
    </tr>
    <tr>
      <th>160444</th>
      <td>681331</td>
      <td>681332</td>
      <td>W560000188</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>STORAGE WELL/MAINTENANCE WELL/OBSERVATION WELL</td>
      <td>HOT SPRINGS</td>
      <td>56017</td>
      <td>USA</td>
      <td>...</td>
      <td>4</td>
      <td>POINT (-12083043.216 5431486.077)</td>
      <td>27457</td>
      <td>27458</td>
      <td>Interstate</td>
      <td>Williston Basin Interstate PL Co.</td>
      <td>0.122880</td>
      <td>13678.939029</td>
      <td>LINESTRING (-12027891.088 5426896.907, -120415...</td>
      <td>41726.321721</td>
    </tr>
    <tr>
      <th>160445</th>
      <td>681763</td>
      <td>681764</td>
      <td>W560000620</td>
      <td>NOT AVAILABLE</td>
      <td>WY</td>
      <td>OIL &amp; NATURAL GAS WELL</td>
      <td>STORAGE WELL/MAINTENANCE WELL/OBSERVATION WELL</td>
      <td>NATRONA</td>
      <td>56025</td>
      <td>USA</td>
      <td>...</td>
      <td>4</td>
      <td>POINT (-11830168.303 5377425.322)</td>
      <td>22703</td>
      <td>22704</td>
      <td>Interstate</td>
      <td>Panhandle Eastern Pipe Line Co.</td>
      <td>0.088576</td>
      <td>13582.091630</td>
      <td>LINESTRING (-11775058.698 5373947.818, -117750...</td>
      <td>55109.604473</td>
    </tr>
  </tbody>
</table>
<p>172851 rows × 44 columns</p>
</div>



###  Adding a Distance Km Column


```python
nearest_wells_df['distance_km'] = nearest_wells_df.distance_euclidian.apply(lambda x: x / 1000)
```


```python
filtered_wells = nearest_wells_df.loc[nearest_wells_df['distance_km'] < 2].copy()
```


```python
filtered_wells.describe()
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
      <th>index</th>
      <th>OBJECTID</th>
      <th>LATITUDE</th>
      <th>LONGITUDE</th>
      <th>PERMITNO</th>
      <th>OPERATORID</th>
      <th>SURF_LAT</th>
      <th>SURF_LONG</th>
      <th>BOT_LAT</th>
      <th>BOT_LONG</th>
      <th>TOTDEPTH</th>
      <th>STAUTS_CAT</th>
      <th>index_right</th>
      <th>FID</th>
      <th>Shape_Leng</th>
      <th>Shape__Length</th>
      <th>distance_euclidian</th>
      <th>distance_km</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>5.891600e+04</td>
      <td>5.891600e+04</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>5.891600e+04</td>
      <td>5.891600e+04</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>58909.000000</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>58916.000000</td>
      <td>5.891600e+04</td>
      <td>5.891600e+04</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2.876220e+05</td>
      <td>2.876230e+05</td>
      <td>35.675314</td>
      <td>-88.211450</td>
      <td>2.065160e+06</td>
      <td>4.079539e+07</td>
      <td>-27.605657</td>
      <td>-143.441562</td>
      <td>-949.945779</td>
      <td>-956.106183</td>
      <td>-593.200370</td>
      <td>1.297423</td>
      <td>13100.924299</td>
      <td>13101.924299</td>
      <td>0.400372</td>
      <td>32272.035793</td>
      <td>8.929434e+02</td>
      <td>8.929434e-01</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2.748624e+05</td>
      <td>2.748624e+05</td>
      <td>4.333618</td>
      <td>7.353183</td>
      <td>3.172222e+06</td>
      <td>2.010973e+08</td>
      <td>247.667329</td>
      <td>218.214976</td>
      <td>219.595052</td>
      <td>192.030681</td>
      <td>1681.248786</td>
      <td>0.896562</td>
      <td>10088.240669</td>
      <td>10088.240669</td>
      <td>11.655711</td>
      <td>46825.746281</td>
      <td>5.765039e+02</td>
      <td>5.765039e-01</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000e+00</td>
      <td>1.000000e+00</td>
      <td>26.047093</td>
      <td>-112.512950</td>
      <td>-9.990000e+02</td>
      <td>-9.990000e+02</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>1.000000</td>
      <td>40.000000</td>
      <td>41.000000</td>
      <td>0.000171</td>
      <td>19.334435</td>
      <td>1.303852e-08</td>
      <td>1.303852e-11</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>7.534850e+04</td>
      <td>7.534950e+04</td>
      <td>31.968007</td>
      <td>-93.497915</td>
      <td>-9.990000e+02</td>
      <td>-9.990000e+02</td>
      <td>30.274497</td>
      <td>-93.594670</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>1.000000</td>
      <td>4044.000000</td>
      <td>4045.000000</td>
      <td>0.079792</td>
      <td>10390.421353</td>
      <td>3.809142e+02</td>
      <td>3.809142e-01</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>3.010045e+05</td>
      <td>3.010055e+05</td>
      <td>37.754454</td>
      <td>-89.423060</td>
      <td>-9.990000e+02</td>
      <td>-9.990000e+02</td>
      <td>33.945500</td>
      <td>-89.776840</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>1.000000</td>
      <td>8744.000000</td>
      <td>8745.000000</td>
      <td>0.155083</td>
      <td>19537.126396</td>
      <td>8.395529e+02</td>
      <td>8.395529e-01</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>3.368862e+05</td>
      <td>3.368872e+05</td>
      <td>39.104642</td>
      <td>-80.997557</td>
      <td>3.502876e+06</td>
      <td>-9.990000e+02</td>
      <td>39.092723</td>
      <td>-80.998595</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>-999.000000</td>
      <td>1.000000</td>
      <td>23176.000000</td>
      <td>23177.000000</td>
      <td>0.291804</td>
      <td>35669.491995</td>
      <td>1.374844e+03</td>
      <td>1.374844e+00</td>
    </tr>
    <tr>
      <th>max</th>
      <td>1.505594e+06</td>
      <td>1.505595e+06</td>
      <td>48.991730</td>
      <td>-76.216780</td>
      <td>2.012020e+07</td>
      <td>1.044755e+09</td>
      <td>48.991730</td>
      <td>-76.216780</td>
      <td>45.158000</td>
      <td>-79.282180</td>
      <td>21475.000000</td>
      <td>4.000000</td>
      <td>33798.000000</td>
      <td>33799.000000</td>
      <td>1000.000000</td>
      <td>704127.420619</td>
      <td>1.999965e+03</td>
      <td>1.999965e+00</td>
    </tr>
  </tbody>
</table>
</div>



## Wells Base Map


```python
well_map_ax = filtered_wells.plot(figsize=(15, 15), alpha=0.5, edgecolor='k', markersize = .5)
cx.add_basemap(well_map_ax, zoom=6)
#filtered_wells.plot()
```


    
![png](wells_near_pipelines_files/wells_near_pipelines_23_0.png)
    


## Pipelines Base Map


```python
pipeline_map = pipeline_df.plot(figsize = (15,15), alpha=0.5,)
cx.add_basemap(pipeline_map, zoom=6)
```


    
![png](wells_near_pipelines_files/wells_near_pipelines_25_0.png)
    


## Pipeline and Potential Carbon Storage Well Map


```python
combined_map = wells_df.plot(ax = pipeline_map, alpha=0.5, figsize = (20,20), edgecolor='k', markersize = .5)

#cx.add_basemap(well_map, zoom=6)
#plt.show()
```


    <Figure size 432x288 with 0 Axes>



```python
combined_map.figure
```




    
![png](wells_near_pipelines_files/wells_near_pipelines_28_0.png)
    


