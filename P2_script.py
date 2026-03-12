#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:56:44 2026

@author: victoriaseale
"""

##PART ONE

import numpy as np

#Loading in the data
data = np.genfromtxt("/Users/victoriaseale/Users/victoriaseale/Git/assignments/P1/CTD_data.dat", skip_header=1, usecols=(2,3,4))

#Outlining the columns needed for each variable to be plotted
depth = data[:,0]
temperature = data[:,1]
salinity = data[:,2]

#Creating two panels sharing y-axis
fig, ax = plt.subplots(1, 2, sharey=True, figsize=(8,6))

#Temperature profile
ax[0].plot(temperature, depth, color='red')
ax[0].set_xlabel("Temperature (°C)")
ax[0].set_ylabel("Depth (m)")
ax[0].set_title("Temperature Profile")

#Salinity profile
ax[1].plot(salinity, depth, color='blue')
ax[1].set_xlabel("Salinity (PSU)")
ax[1].set_title("Salinity Profile")

#Swapping axis to make dpeth increase downwards
ax[0].invert_yaxis()

#%%
##PART TWO

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(
    "SAA2_WC_2017_metocean_10min_avg.csv",
    parse_dates=['TIME_SERVER'],
    index_col='TIME_SERVER'
)

#Checking for missing values
print(df.isna().sum())


#Time indexing from departure -> 4th of July
df_selected = df.loc[:'2017-07-04']

#Checking column names 
print(df.columns)

#Creating the timeseries using a gray scale format
plt.style.use('grayscale')

plt.figure(figsize=(10,5))
plt.plot(df_selected.index, df_selected['AIR_TEMPERATURE'])

plt.xlabel("Date")
plt.ylabel("Air Temperature (°C)")
plt.title("Air Temperature Time Series")

plt.savefig("temperature_timeseries.png")
plt.show()

#%%

#Histogram 

#Mkaing the background of the plot white instead of gray when saving 
plt.style.use('default')

bins = np.arange(30, 35.5, 0.5)

plt.figure()
plt.hist(df_selected['TSG_SALINITY'], bins=bins)

plt.xlabel("Salinity (PSU)")
plt.ylabel("Frequency")
plt.title("Salinity Distribution")

plt.show()

#%%
#Statistic summary table

stats = pd.DataFrame({
    "Mean": df_selected[['AIR_TEMPERATURE','TSG_SALINITY']].mean(),
    "Std Dev": df_selected[['AIR_TEMPERATURE','TSG_SALINITY']].std(),
    "IQR": df_selected[['AIR_TEMPERATURE','TSG_SALINITY']].quantile(0.75) -
           df_selected[['AIR_TEMPERATURE','TSG_SALINITY']].quantile(0.25)
})

print(stats)

#%%
#Scatterplot

plt.figure()

scatter = plt.scatter(
    df_selected['WIND_SPEED_TRUE'],
    df_selected['AIR_TEMPERATURE'],
    c=df_selected['LATITUDE'],
    cmap='plasma'
)

plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Air Temperature (°C)")
plt.title("Wind Speed vs Air Temperature")

plt.colorbar(scatter, label="Latitude")

plt.savefig("wind_temp_scatter.png", dpi=300)
plt.show()





















