__author__ = 'robertv'
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 05 11:10:13 2013

@author: Ivo
"""

import pandas as pd
from matplotlib.pylab import figure, grid, savefig, xlim, ylim, colorbar
from matplotlib.pylab import title, tight_layout, close, xlabel, ylabel
from itertools import combinations
import networkx as nx

# Load data
train 	= pd.read_csv('Data/train.csv')
si    	= pd.read_csv('Data/station_info.csv')

# Change index and longitude for station
si.index 	= si.stid
si.elon 	= si.elon+360

# Compute the correlation matrix
# Discard int_time
c = train[train.columns[1:]].corr()

# Build the correlation graph
g = nx.Graph()
threshold = 0.95
for node1, node2 in combinations(si.index, 2):
	if c[node1][node2]>threshold:
		g.add_edge(node1, node2)

# Build the position dict from station info
position = {}
for idx, row in si.iterrows():
	position[row['stid']] = (row['elon'],row['nlat'])

# Get the elevations for each station
elevation 	= si.elev.to_dict()

# Let the elevation be your node's color attribute
node_colors = [elevation[n] for n in g.nodes()]

# Draw that figure
figure(figsize=(600,400))

# Give it a title
title('MESONET stations colorcoded by elevation, connected if corr(s1,s2)>0.95')

# Draw that neat graph
nx.draw_networkx(
	g,position,	alpha=0.75,
	node_size=800,node_color=node_colors,
	node_shape='o',linewidths=0,font_size=10)

# Add the fancy colorbar
colorbar(orientation='horizontal')

# Add axis labels
xlabel('Longitude')
ylabel('Latitude')

# Adjust padding as needed
padding  = 0.3
xmax = si.elon.max()+padding
xmin = si.elon.min()-padding
ymax = si.nlat.max()+padding
ymin = si.nlat.min()-padding
xlim(xmin,xmax)
ylim(ymin,ymax)

# Awesome grid
grid()

tight_layout()

# Save that plot!
savefig('el_plot.png')

close()