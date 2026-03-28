#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:10:49 2026

@author: victoriaseale
"""
#Importing the necessary packages 
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# %% Loading the datasets 

#Chlorophyll datasets from the climatology dataset
chl = xr.open_dataset(
    "/Users/victoriaseale/Desktop/P4/ESACCI-OC-MAPPED-CLIMATOLOGY-1M_MONTHLY_4km_PML_CHL-fv5.0.nc"
)

#Bathymetry data set from the map tool
bathy = xr.open_dataset(
    "/Users/victoriaseale/Desktop/P4/GMRTv4_4_1_20260326topo.grd",
    engine="netcdf4" #usign an engine command because the file was a .grd
)

# %% Defining the Agulhas region
lon_min, lon_max = 20, 35
lat_min, lat_max = -40, -30

#Subsetting chlorophyll
chl_region = chl.sel(
    lon=slice(lon_min, lon_max),
    lat=slice(lat_max, lat_min)  
)

#Subsetting bathymetry 
bathy_region = bathy.sel(
    lon=slice(lon_min, lon_max),
    lat=slice(lat_min, lat_max)
)

#%% Plotting the Bathymetry of the Agulhas region

plt.figure(figsize=(10,8))

ax = plt.axes(projection=ccrs.PlateCarree())

#Bathymetry
mesh = ax.pcolormesh(
    bathy_region['lon'],
    bathy_region['lat'],
    bathy_region['altitude'],
    cmap='terrain',
    transform=ccrs.PlateCarree()
)

#Adding a boundary line to distinguish the land
ax.coastlines(resolution='10m', color='black', linewidth=1) #Adding a coast line boundary line

gl = ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--') #Adding grid lines for lat and lon co-ordinates

gl.top_labels = False
gl.right_labels = False #Removing top and right labels

#Adding a colour bar
plt.colorbar(mesh, ax=ax, label='Depth (m)') 

#Titles and labels
plt.title('Bathymetry map of the Agulhas Region',
          fontsize=20,
          fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.savefig("bathy_map.png", dpi=300)
plt.show()

#%% Plotting the chlorophyll mean data

chl_var = 'chlor_a' #renaming the chlorophyll variable from the dataset

#Mean over time
chl_mean = chl_region[chl_var].mean(dim='time')

plt.figure(figsize=(10,8))
ax = plt.axes(projection=ccrs.PlateCarree())

#Creating the log scale
mesh = ax.pcolormesh(
    chl_region['lon'],
    chl_region['lat'],
    chl_mean,
    cmap='viridis',
    norm=LogNorm(vmin=0.05, vmax=10),
    transform=ccrs.PlateCarree()
)

#Distinguishing the land
ax.coastlines(resolution='10m', linewidth=1)
ax.add_feature(cfeature.LAND, facecolor='lightgrey')

#Gridlines with labels - co-ordinates
gl = ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

#Creating the Colourbar (log scale ticks)
cbar = plt.colorbar(mesh, ax=ax, pad=0.02)
cbar.set_label('Chlorophyll (mg m⁻³)', fontsize=12)

plt.title('Mean Annual Chlorophyll\n(Log Scale, mg m$^{-3}$) in the Agulhas Region',
          fontsize=20,
          fontweight='bold',
          pad=20)

plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.savefig("chl_mean.png", dpi=300)
plt.show()

#%% Plotting the monthly mean chlorophyll data for each month

fig, axes = plt.subplots(3, 4, figsize=(16,10)) #Specifying the subplot parameters and layout

for i, ax in enumerate(axes.flat):
    data = chl_region[chl_var].isel(time=i)

    im = ax.pcolormesh(
        chl_region['lon'],
        chl_region['lat'],
        data,
        cmap='viridis',
        norm=LogNorm(vmin=0.05, vmax=10)
    )

import calendar #To use for month names 

for i, ax in enumerate(axes.flat):         #Using a loop to create calendar month labels for each subplot 
    ax.set_title(calendar.month_name[i+1])

fig.colorbar(im, ax=axes.ravel().tolist(), label='Chlorophyll (mg/m³)')

plt.suptitle("Monthly Chlorophyll Climatology of the Agulhas Region",
             fontsize=20,
             fontweight='bold')

plt.savefig("chl_monthly.png", dpi=300)
plt.show()

#%% Plotting the timeseries through the months 

#Getting the regional mean
regional_ts = chl_region[chl_var].mean(dim=['lat','lon'])

#Selecting the highest ("nearest") mean point 
point = chl_region.sel(lon=23, lat=-34.5, method='nearest')
point_ts = point[chl_var]

regional_ts = regional_ts.where(regional_ts > 0)
point_ts = point_ts.where(point_ts > 0) #masking for plotting

months_idx = np.arange(12)
months_labels = list(calendar.month_abbr)[1:]  #Monthly labels

plt.figure(figsize=(10,5))

#Plotting the regional mean point
plt.plot(months_idx, regional_ts, label='Regional Mean', color='blue', linewidth=2, marker='o')

#Single-point line
plt.plot(months_idx, point_ts, label='Agulhas Bank Point', color='green', linewidth=2, marker='s')

#Plotting the y-scale in log form 
plt.yscale('log')

#Seasonal shading on the graph- to read seasons easily 
season_colors = {'DJF':'#ffebcc', 'MAM':'#ccffeb', 'JJA':'#cce5ff', 'SON':'#ffcccc'}
season_months = {'DJF':[11,0,1], 'MAM':[2,3,4], 'JJA':[5,6,7], 'SON':[8,9,10]}

for season, months in season_months.items():
    plt.axvspan(min(months), max(months)+1, color=season_colors[season], alpha=0.3, label='_nolegend_')

plt.legend(loc='upper right') #Legend placement

#Plot labels and titles
plt.title("Seasonal Chlorophyll Cycle\nAgulhas Region (mg m$^{-3}$)",
          fontsize=18,
          fontweight='bold',
          pad=15)
plt.xlabel("Month")
plt.ylabel("Chlorophyll (mg m$^{-3}$)")

plt.xticks(ticks=months_idx, labels=months_labels)
plt.xlim(0, 11) #Remove excess space on the graph
plt.grid(True, which="both", linestyle="--", linewidth=0.5) #Adding grid lines


plt.tight_layout()
plt.savefig("chl_timeseries_region_vs_point.png", dpi=300)
plt.show()
