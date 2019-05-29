#%%
# Working with Python and Pandas
#  - Importing csv Files
#  - DateTime Objects
#  - Plotting and Charting
#  - Maps
#%%
import numpy as np
import pandas as pd
import re
import json
import gmaps
import matplotlib.pyplot as plt
%matplotlib inline

#%%
#  Importing csv Files
ems = pd.read_csv('data/ems.csv')
ems.head()

#%%
# Changing to a DateTime Object
ems['datetime'] = pd.to_datetime(ems['Incident Time'])
ems['datetime'].head()

#%%
# Extract the day of the week from the date using .dt.dayofweek
ems['datetime'].dt.dayofweek.head(15)

#%%
# Converting those day-of-week numbers into string values with dictionaries and .apply()
week_lookup = {
    0 : 'Mon',
    1 : 'Tue',
    2 : 'Wed',
    3 : 'Thurs',
    4 : 'Fri',
    5 : 'Sat',
    6 : 'Sun'
}
# Using our dictionary, we can 'look up' our weekdays by our numbers
ems.groupby(ems['datetime'].dt.dayofweek.apply(lambda x: week_lookup[x]), sort=False).size()
ebd = ems.groupby(ems['datetime'].dt.dayofweek, sort=True).size()
ebd

#%%
# Next, let's get our events by hour
ebh = ems.groupby(ems['datetime'].dt.hour).size().to_dict()
ebh

#%%
# Here's a helper function which fills any any nulls for hours with zeroes and returns a list.
# make an empty dict of zeroes
ebh_dict = dict()
for i in range(0,24):
    ebh_dict[i] = 0

# fill in the dict with our events by hour
for k,v in ebh.items():
    ebh_dict[k] = v
    
# make a tidy list of events by hour
ebh = list(ebh_dict.values())

#cleanup
ebh_dict = None

# final events by hour list
print(ebh)

#%%
# Plotting within a notebook
fig, axes = plt.subplots(nrows=1, ncols=2)
fig.set_figwidth(10)

for i, ax in enumerate(axes):
    # graph on the left
    if i == 0:
        ax = plt.subplot(121, polar=True)
        equals = np.linspace(0, 360, 24, endpoint=False)
        ones = np.ones(24)
        ax.plot(np.linspace(0,2*np.pi,num=24), ebh)    

        # Set the circumference labels
        ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))
        ax.set_xticklabels(range(24))      

        # Make the labels go clockwise
        ax.set_theta_direction(-1)       

        # Place 0 at the top
        ax.set_theta_offset(np.pi/2.0) 
        ax.set_title('SXSW EMS Incidents by Hour', va='bottom')
    # graph on the right:
    if i == 1:
        ax.set_title('SXSW EMS Incidents by Day')
        ax.bar(ebd.index.tolist(), ebd.values.tolist())
        ax.set_xticklabels(['foo'] + [week_lookup[x] for x in ebd.index.tolist()])
plt.plot()

#%%
# Charting Stuff on a Map
with open("./secrets.json") as f:
    data = f.read()
    api_key = json.loads(data)['key']

gmaps.configure(api_key=api_key)
fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(ems[['Location Latitude', 'Location Longitude']], weights=ems['Total Patients']))
fig

#%%
fig = gmaps.figure()
drawing = gmaps.drawing_layer(features=[
     gmaps.Line((46.23, 5.86), (46.44, 5.24), stroke_weight=3.0),
     gmaps.Marker((46.88, 5.45), label='D'),
     gmaps.Polygon(
         [(46.72, 6.06), (46.48, 6.49), (46.79, 6.91)],
         fill_color='red'
     )
])
fig.add_layer(drawing)
fig


#%%
gmaps.__version__

#%%
