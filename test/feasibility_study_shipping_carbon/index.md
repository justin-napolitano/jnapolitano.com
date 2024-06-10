+++
title =  "Feasibility of Transatlantic Carbon Shipping"
date = "2022-05-07T18:40:32.169Z"
description = "A feasibility study of shipping carbon from Europe to the United States"
author = "Justin Napolitano"
image = "post-image.jpeg"
featuredimage = "post-image.jpeg"
categories = ['Python', 'Energy Sector', 'Carbon Capture', 'Economic Modeling', 'Shipping', 'EuroZone', 'Statistical Analysis', 'Economic Projections']
tags = ['energy','lng', 'carbon-capture','python',]
series =['Transatlantic Shipping']
+++

# Feasibility of Shipping Carbon Across the Atlantic


## Methodology

Please review the my [previous post](https://blog.jnapolitano.io/carbon-shipping-projections/) which details the design of my model.  

The major difference in this report is the sampling of the mean price per voyage.

The conversion error has been corrected.

## Findings

### Distance of Transport

The standard deviation in mean price per voyage was found to be less than 0.  This suggests that the distance of travel within Europe is marginal.  The major obstacle is crossing the Atlantic to access the Gulf of Mexico.  It is possible that an import/export port located in the Chesapeake, New England, Willmington, or Savannah could reduce the cost of navigating through the Caribbean to access Gulf based ports.  

This would present a secondary problem piping the co2 to the interior of the Country to access the spent wells located in the Rust Belt. 

### Price of Transport

The price of transport is fixed at $12.00 USD per 100 km per tonne as suggested by this [source](https://ieaghg.org/docs/General_Docs/Reports/PH4-30%20Ship%20Transport.pdf).  A rough estimate for the total cost per tonne from London to Houston is about USD $936.00. For reference the cost to transport standard freight from China to the United States ranges from $5,000 to $8,000 USD in total per tonne; or $5.00 to $8.00 USD per kilo in total.     

### Industrial Applications 

Another study must be completed to calculate value of super critical CO2 to industrial applications in order to attempt to justify shipping CO2 such large distances.  Shipping large quantities of CO2 to  store is most likely unreasonable, however, at only about $316,665 USD average cost per voyage it is a reasonable figure if proper incentives are in place.  

### Carbon Storage

Based on this model, it is somewhat reasonable to transport CO2, especially if the US incentivises companies that do so.  Nonetheless, at $50-$60 carbon tax credits per tonne captured (verify this data), it would be unfeasible to account for the estimated 936 per tonne cost of shipping across the Atlantic under current programs.

## Limitations of the Model

### Accounting for the Return Trip to Port
 
It is important to note that I did not account for the differential costs for the return trip to a european port.  Though, the cost of shipping per ton was fixed at 12.00 USD, doubling distance of travel may double pricing. That said, it would be unlikely for ships to return to port empty. I would expect tankers to be refilled with LNG for return.  Nonetheless, this is a slight methodological issue that should be improved upon.  

### Cost to Transport

The cost to transport per 100 km is fixed at 12.00 USD as suggested by this [source](https://ieaghg.org/docs/General_Docs/Reports/PH4-30%20Ship%20Transport.pdf).  It accounts for the cost of liquification, shipping costs, and port fees.  The source however, was published in 2004.  The costs may have been reduced by technological advance and demand for super critical CO2.

### Volumes of Transport

I simply converted the volumes of standard LNG ships to liquifed CO2.  There may be data available for tankers dedicated to carbon, but I was not aware of any when performing this analysis.  Tankers may also not completely dedicate their capacity to CO2.  Armed with a proper probability distribution, I could improve the model by randomly choosing volumes based on historical data.  

## Conclusion

It is unlikely that CO2 will be shipped to the United States simply for storage unless companies are incentivized to do so. A transatlantic trade may develop, but I would assume in order to meet demands for the industrial applications of super critical CO2.

## Mean Voyage Data Analysis


```python
mean_price_per_cycle_df.describe()
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
      <th>Voyage Cost USD</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>5.000000e+02</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>3.166652e+05</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.165319e-10</td>
    </tr>
    <tr>
      <th>min</th>
      <td>3.166652e+05</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>3.166652e+05</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>3.166652e+05</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>3.166652e+05</td>
    </tr>
    <tr>
      <th>max</th>
      <td>3.166652e+05</td>
    </tr>
  </tbody>
</table>
</div>



### Calculating the Confidence Interval For Mean Voyage

The data is nearly normal.  I could test for normality, but that would be beyond the scope of this analysis.  Also, by design the Monte Carlo model should produce a normal distribution with sufficient samples.  


```python

st.norm.interval(alpha=0.90, loc=np.mean(mean_price_per_cycle_df['Voyage Cost USD']), scale=st.sem(mean_price_per_cycle_df['Voyage Cost USD']))
```




    (316665.2057796428, 316665.2057796428)



It is safe to assume that 90 percent of the time we would see an annual cost 316,665 dollars USD with the assumptions of the model taken into account.  As the price per 100 km is fixed, the standard deviations is minimal.  The distances as well to port seem to be fairly consistent.  The cost of transport through Europe is minimal.

### Histogram of Mean Voyage Price Samples

The price does not deviate.  It is so concentrated in fact, that I worry that the model is not correctly randomizing European ports of origin.  If the model is operating correctly, then it is apparent that the Atlantic is the only barrier to trade.  Partners such as the UK, France, Portugal, The Netherlands, Spain, or any other nation relatively close to the United States are equally unlikely.  


```python
mean_price_per_cycle_df.plot.hist(grid=True, bins=20, rwidth=0.9,
                   color='#607c8e')
plt.title('Mean Price Distribution Per Voyage')
plt.xlabel('Mean Voyage Price USD')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
```


    
![png](shipping_carbon_feasibility_files/shipping_carbon_feasibility_8_0.png)
    


## Annual Data Analysis

This is a reprint of the findings from [my previous report](https://blog.jnapolitano.io/carbon-shipping-projections/)


```python
annual_price_samples_df.describe()
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
      <th>cost_in_usd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>5.000000e+02</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>5.744043e+07</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.160779e+06</td>
    </tr>
    <tr>
      <th>min</th>
      <td>5.408210e+07</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>5.660839e+07</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>5.737843e+07</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>5.819101e+07</td>
    </tr>
    <tr>
      <th>max</th>
      <td>6.092949e+07</td>
    </tr>
  </tbody>
</table>
</div>



## Calculating the Confidence Interval

The data is nearly normal.  I could test for normality, but that would be beyond the scope of this analysis.  Also, by design the Monte Carlo model should produce a normal distribution with sufficient samples.  


```python

st.norm.interval(alpha=0.90, loc=np.mean(annual_price_samples_df['cost_in_usd']), scale=st.sem(annual_price_samples_df['cost_in_usd']))
```




    (57355047.61667279, 57525821.6547037)



It is safe to assume that 90 percent of the time we would see an annual cost of 57.36 to 57.52 million dollars USD with the assumptions of the model taken into account.  

### Histogram of Annual Price Distribution


```python
annual_price_samples_df.plot.hist(grid=True, bins=20, rwidth=0.9,
                   color='#607c8e')
plt.title('Annual Price Distribution for Shipping Carbon')
plt.xlabel('Annual Price in USD')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
```


    
![png](shipping_carbon_feasibility_files/shipping_carbon_feasibility_15_0.png)
    


## Data Imports and Manipulation

### The Shipping Dataframe

The shipping dataframe is the basis of the simulation.  It is used to tabulate total cost and to record the values of variables.

#### Capacity Distribution and Number of Ships Calculation


```python
# Capacity range
# 40,000 m3 71,500 to 210,000

#Susanna Dorigoni, Luigi Mazzei, Federico Pontoni, and Antonio Sileo
#IEFE – Centre for Research on Energy and Environmental Economics and Policy,
#Università Bocconi, Milan, Italy

# I'm sure a better report is available but this is a start
# cubic meters unit

### a rough estimate of global suplly dedicated to co2 shipping

# I will probably need a better metric but this is a good start that can be modified later when necessary

ships = int(63*.25)
ships


conversion_factor = 2.21/2.65
conversion_factor

lower_bound = int(40000 * conversion_factor)
upper_bound = int(210000 * conversion_factor)

median = 137564 * conversion_factor
standard_dev = 6.63 * conversion_factor  #file:///Users/jnapolitano/Downloads/LNG_Shipping_a_Descriptive_Analysis.pdf

cap_range = range(lower_bound, upper_bound)

cap_distribution = np.random.normal(loc=median , scale=standard_dev, size=ships)


```

#### The Shipping Df


```python
shipping_df = pd.DataFrame(cap_distribution, columns=['co2_capacity_cubic_meters'])
shipping_df['days_to_port'] = 0
shipping_df['europe_port'] = ''
shipping_df["us_port"] =''
shipping_df['distance'] =''
shipping_df['price'] = 0
shipping_df['cost_per_day'] = 0
shipping_df['co2_capacity_tonnes'] = shipping_df['co2_capacity_cubic_meters']/544.66 ## Verify this factor.  It seems to high
shipping_df
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
      <th>co2_capacity_cubic_meters</th>
      <th>days_to_port</th>
      <th>europe_port</th>
      <th>us_port</th>
      <th>distance</th>
      <th>price</th>
      <th>cost_per_day</th>
      <th>co2_capacity_tonnes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>114720.479228</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.627693</td>
    </tr>
    <tr>
      <th>1</th>
      <td>114722.019258</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.630520</td>
    </tr>
    <tr>
      <th>2</th>
      <td>114717.260040</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.621782</td>
    </tr>
    <tr>
      <th>3</th>
      <td>114715.555903</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.618654</td>
    </tr>
    <tr>
      <th>4</th>
      <td>114711.076224</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.610429</td>
    </tr>
    <tr>
      <th>5</th>
      <td>114717.940270</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.623031</td>
    </tr>
    <tr>
      <th>6</th>
      <td>114721.291722</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.629185</td>
    </tr>
    <tr>
      <th>7</th>
      <td>114723.060928</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.632433</td>
    </tr>
    <tr>
      <th>8</th>
      <td>114724.416053</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.634921</td>
    </tr>
    <tr>
      <th>9</th>
      <td>114730.832971</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.646702</td>
    </tr>
    <tr>
      <th>10</th>
      <td>114727.128385</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.639901</td>
    </tr>
    <tr>
      <th>11</th>
      <td>114723.001878</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.632325</td>
    </tr>
    <tr>
      <th>12</th>
      <td>114715.038614</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.617704</td>
    </tr>
    <tr>
      <th>13</th>
      <td>114721.502327</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.629571</td>
    </tr>
    <tr>
      <th>14</th>
      <td>114722.089811</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>0</td>
      <td>210.630650</td>
    </tr>
  </tbody>
</table>
</div>



### The European Ports Df


```python

gisfilepath = "/Users/jnapolitano/Projects/data/energy/PORT_2013_SH/Data/PORT_PT_2013.shp"


ports_df = gpd.read_file(gisfilepath)

ports_df = ports_df.to_crs(epsg=3857)
```

### Filtered Wells DataFrame


```python
## Importing our DataFrames

gisfilepath = "/Users/jnapolitano/Projects/data/energy/filtered-wells.geojson"


filtered_df = gpd.read_file(gisfilepath)

filtered_df = filtered_df.to_crs(epsg=3857)


```

#### Getting Map Conditions for Us Port Filtering



```python
map_conditions = filtered_df.TERMID.unique().tolist()
```

### US Ports Dataframes


```python
## Importing our DataFrames

gisfilepath = "/Users/jnapolitano/Projects/data/energy/Liquified_Natural_Gas_Import_Exports_and_Terminals.geojson"


terminal_df = gpd.read_file(gisfilepath)

terminal_df = terminal_df.to_crs(epsg=3857)


```


```python
terminal_df.drop(terminal_df[terminal_df['STATUS'] == 'SUSPENDED'].index, inplace = True)
terminal_df.rename(columns={"NAME": "TERMINAL_NAME"})
terminal_df['TERMINAL_GEO'] = terminal_df['geometry'].copy()

```


```python
port_terminals_df = terminal_df.query('TERMID in @map_conditions').copy()
port_terminals_df['co2_capacity_mmta'] = port_terminals_df['CURRENTCAP'] * conversion_factor
port_terminals_df['co2_capacity_metric_tons'] = port_terminals_df['co2_capacity_mmta'] * 1000000
port_terminals_df['available'] = True
```

## Random Distribution, Distance and Pricing Functions 

### Accounting for Random Days at Sea

As days at sea is variable I created a range between 20 and 40 days to account for a round trip to every major port in Europe.  


```python

def random_day():
    lower_bound = 20
    upper_bound = 40

    median = 30
    standard_dev = 2

    days_range = range(lower_bound, upper_bound)

    days_distribution = np.random.normal(loc=median , scale=standard_dev, size=ships)


    days_randomized = np.random.choice(days_distribution, size=1)


    return (days_randomized[0].astype(np.int64))

```

### Accounting for Random European Ports

 I randomized the port selection process with the following function.  The data provided by EuroStat did not filter according to type of port.  Nonetheless, the distance recorded should be very similiar to those of actual LNG ports.  A better data set could be substituded directly into the function.


```python

def random_europe_port():
    #select a random number along the index of the ports df.  Return the value of hte geometry at the index.  
    #select indices from the dataframe that are valid.  ie capacity has not yet been met.  
    ports_randomized = np.random.choice(ports_df.index, size=1)
    index_location = ports_randomized[0]
    return ports_df.geometry[index_location]

```

### Accounting for Random US Ports

I was able to filter import/export ports in the United States in to a dataset of about 15.  Like the European dataset, I randomized selection.


```python

def random_us_port():
    #select a random number along the index of the ports df.  Return the value of hte geometry at the index.  

    ports_randomized = np.random.choice(port_terminals_df.index, size=1)
    index_location = ports_randomized[0]
    return port_terminals_df.geometry[index_location]

```

### Calculating Distance Between Ports

I calculated the shortest distance between ports based on their geographic locations with the shapley.distance function.  It returns distance in meters.  I divide by 1000 to convert into Km.   The algorithm could be improved by using official shipping data to randomize a distribution of distances between ports.  Unfortunately, I do not have that data available to me. 


```python

def geo_distance(dist1,dist2):
    # return distance in km
    distance = dist1.distance(dist2)/1000
    return(distance)

    

```

### Calculating Price of Transport


The cost of transport accounts for port fees, liquification, and transport.   Unfortunately, my data is from a paper published in 2004.  I would like to find a more recent paper.   I did not convert the value of 2004 USD to 2022 because I am not sure of the validity of the conversion factors available online.  I would need a better source to correctly model the true cost of transport.  

[source](https://ieaghg.org/docs/General_Docs/Reports/PH4-30%20Ship%20Transport.pdf)


```python

def price_to_transport(distance,tonnes):
    price = (distance/100) * 12 * tonnes
    return price

```

### Calculating Cost Per Day


```python
def cost_per_day(price,distance):
    return price/distance
```

## Costs Per Annum Algorithm

The algorithm I used calculates the daily status of ships transporting CO2 across the Atlantic from a random European port to a random port in the United States.  It will run for 365 iterations or until the total carbon capacity of the US ports is reached.  This value could and probably should be dynamically allocated via a similiar algorithm, but I do not yet have historical probability distributions of carbon imports to determime a valid price allocation function.  

When the daily counter reaches zero for a tanker:
* The capacity is refilled to full.
* A random us port is assigned.
* A random European port is assigned.
* The distance between ports is calculated.
* The cost of transport over that distance is calculated per 100 km.
* The total shipping price of that cycle is tabulated.
* The total tonnage of that cycle is tabulated.
* The mean price per voyage is tabulated





```python

days = 365
day_counter = 0 
carbon_total_millions_metric_tons = 300000000
total_tons_shipped = 0
total_price = 0
cycle_mean_price_samples = np.zeros(shape=days)

#deduction = capacity of empty ships
for day in range(days):
    if carbon_total_millions_metric_tons >= 0:
        # must use apply to account for multiple 0 conditions.  If i simply vectorized the function across the dataframe in a single call i would assign the the same values each day 
        shipping_df['days_to_port'] = shipping_df['days_to_port'] - 1
        shipping_df['us_port'] = shipping_df.apply(lambda x:  random_us_port() if x['days_to_port']<=0 else x['us_port'], axis=1)
        shipping_df['europe_port'] = shipping_df.apply(lambda x:  random_europe_port() if x['days_to_port']<=0 else x['europe_port'], axis=1)
        shipping_df['distance'] = shipping_df.apply(lambda x:  geo_distance(x['us_port'], x['europe_port']) if x['days_to_port']<=0 else x['distance'], axis=1)
        shipping_df['price'] = shipping_df.apply(lambda x:  price_to_transport(x['distance'],x['co2_capacity_tonnes']) if x['days_to_port']<=0 else x['price'], axis=1)
        #calculate cost per day for fun...
        # query all that are = o.  Summate the capacities deduct the total 
        tmp_df=shipping_df.loc[shipping_df['days_to_port'] <= 0]
        sum_of_capacity = tmp_df['co2_capacity_tonnes'].sum()
        sum_of_price = tmp_df['price'].sum()
        mean_of_price = tmp_df['price'].mean()
        cycle_mean_price_samples[day] = mean_of_price
        shipping_df['days_to_port'] = shipping_df['days_to_port'].apply(lambda x: random_day() if x<=0 else x)
        total_tons_shipped = total_tons_shipped + sum_of_capacity
        total_price = total_price + sum_of_price
        carbon_total_millions_metric_tons = carbon_total_millions_metric_tons - sum_of_capacity
        #print(carbon_total_millions_metric_tons)
        day_counter = day_counter+1
    else: 
        break

    
    
print(day_counter)
print(total_tons_shipped)
print(total_price)
#Drop the nan, ie empty samples
cycle_mean_price = cycle_mean_price_samples[np.logical_not(np.isnan(cycle_mean_price_samples))]
#Calculate mean price of filling a ship (around a billion according to the data i have if filled to capacity.  Ridiculous.)
cycle_mean_price = cycle_mean_price.mean()
print(cycle_mean_price)

```

    365
    41072.53151865029
    62067313.75358563
    316665.2057796429


## Monte Carlo Simulation with 500 Iterations

The annual rate of shipping can be variable according to shifting dynamics. I account for that by modeling the per annum algorithm 500 times.  Modeling would improve as n increases, but for the sake of time I limited the computation to 500 iterations

The only difference between this algorithm and the previous one is an extra for loop.  The algorithmic efficiency is surprisingly good as the I was able to vectorize tabulations with lambda functions across the dataframes.  On my laptop, I was able to complete the algorithm in about 16 minutes of run time.




```python

nsamples = 500
price_samples = np.zeros(shape=nsamples)
cycle_mean_price_annual_samples = np.zeros(shape=nsamples)

for sample in range(nsamples):

    days = 365
    day_counter = 0 
    carbon_total_millions_metric_tons = 300000000 # could randomize.  Need a probability distribution based on historial data. 
    total_tons_shipped = 0
    total_price = 0
    cycle_mean_price_daily_samples = np.zeros(shape=days)


    #deduction = capacity of empty ships
    for day in range(days):
        if carbon_total_millions_metric_tons >= 0:
            # must use apply to account for multiple 0 conditions.  If i simply vectorized the function across the dataframe in a single call i would assign the the same values each day 
            shipping_df['days_to_port'] = shipping_df['days_to_port'] - 1
            shipping_df['us_port'] = shipping_df.apply(lambda x:  random_us_port() if x['days_to_port']<=0 else x['us_port'], axis=1)
            shipping_df['europe_port'] = shipping_df.apply(lambda x:  random_europe_port() if x['days_to_port']<=0 else x['europe_port'], axis=1)
            shipping_df['distance'] = shipping_df.apply(lambda x:  geo_distance(x['us_port'], x['europe_port']) if x['days_to_port']<=0 else x['distance'], axis=1)
            shipping_df['price'] = shipping_df.apply(lambda x:  price_to_transport(x['distance'], x['co2_capacity_tonnes']) if x['days_to_port']<=0 else x['price'], axis=1)
            # query all that are = o.  Summate the capacities deduct the total 
            tmp_df=shipping_df.loc[shipping_df['days_to_port'] == 0]
            sum_of_capacity = tmp_df['co2_capacity_tonnes'].sum()
            sum_of_price = tmp_df['price'].sum()
            mean_of_price = tmp_df['price'].mean()
            cycle_mean_price_daily_samples[day] = mean_of_price
            shipping_df['days_to_port'] = shipping_df['days_to_port'].apply(lambda x: random_day() if x<=0 else x)
            total_tons_shipped = total_tons_shipped + sum_of_capacity
            total_price = total_price + sum_of_price
            carbon_total_millions_metric_tons = carbon_total_millions_metric_tons - sum_of_capacity
            #print(carbon_total_millions_metric_tons)
            day_counter = day_counter+1
        else: 
            break

    #Drop the nan, ie empty samples
    cycle_mean_price = cycle_mean_price_samples[np.logical_not(np.isnan(cycle_mean_price_samples))]
    #Calculate mean price of filling a ship (around a billion according to the data i have if filled to capacity.  Ridiculous.)
    cycle_mean_price = cycle_mean_price.mean()
    cycle_mean_price_annual_samples[sample] =cycle_mean_price
        
    

    price_samples[sample] = total_price

        

```

### Creating the Annual Price Samples DF


```python
annual_price_samples_df = pd.DataFrame(price_samples, columns=['cost_in_usd'])
```


```python
annual_price_samples_df['cost_in_usd'] = annual_price_samples_df.cost_in_usd

```

### Creating the Mean Price Per Round Trip Df


```python
mean_price_per_cycle_df = pd.DataFrame(cycle_mean_price_annual_samples, columns=['Voyage Cost USD'])
mean_price_per_cycle_df['Voyage Cost USD'] = mean_price_per_cycle_df['Voyage Cost USD'] 

```

## Imports


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
import scipy.stats as st
from shapely.geometry import Point
from haversine import Unit
from geopy.distance import distance

import warnings

warnings.filterwarnings('ignore')

```

    /Users/jnapolitano/venvs/finance/lib/python3.9/site-packages/geopandas/_compat.py:111: UserWarning: The Shapely GEOS version (3.10.2-CAPI-1.16.0) is incompatible with the GEOS version PyGEOS was compiled with (3.10.1-CAPI-1.16.0). Conversions between both will be slow.
      warnings.warn(



```python

```
