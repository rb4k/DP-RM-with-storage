
# coding: utf-8

# In[1]:

__version__ = '0.3'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = ''
__url__     = ''
__copyright__ = "(C) 2015 Robert Matern"


# # Beispieldaten: Normalverteil und keine Verteilung

# In[2]:

import numpy as np
import pandas as pd
import matplotlib as plt
import sys

print 'Python Version ' + sys.version
print 'Numpy Version ' + np.__version__
print 'Matplotlib Version ' + plt.__version__
print 'Pandas Version ' + pd.__version__

import networkx as nx
import graphviz as gv
import datetime


# In[3]:

# Funktionen werden hinzugeladen.
from Parameter import Product, Resource, Capacity, Consumption, Revenue, Time, Prob, Against_Prob


# In[8]:

# Produkte
products = Product(10)

# Ressourcen
resources = Resource(5)

#Kapazität
capacities = Capacity(resources)
for h in resources[1:]:
    capacities[h] = 1

# Ressourcenverbrauch
consumtions = Consumption(products, resources)
index = 0
for j in range(1, len(products), 2):
    consumtions[j][1+index] = 1
    consumtions[j+1][1+index] = 1
    index = index + 1
del index


# Erträge
revenues = Revenue(products)
for j in range(1, len(products), 2):
    revenues[j] = 100
    revenues[j+1] = 1000

# Buchungsperioden
times = Time(100)

# Normalverteilung
from scipy.stats import norm

# Wahrscheinlichkeiten
probs = Prob(products, times)
probs[1][81:101] = 5*norm.pdf(np.arange(81, 101), 90, 5)
probs[2][81:101] = 5*norm.pdf(np.arange(81, 101), 90, 5)
probs[3][61:101] = 5*norm.pdf(np.arange(61, 101), 70, 5)
probs[4][61:101] = 5*norm.pdf(np.arange(61, 101), 70, 5)
probs[5][41:101] = 5*norm.pdf(np.arange(41, 101), 50, 5)
probs[6][41:101] = 5*norm.pdf(np.arange(41, 101), 50, 5)
probs[7][21:101] = 5*norm.pdf(np.arange(21, 101), 30, 5)
probs[8][21:101] = 5*norm.pdf(np.arange(21, 101), 30, 5)
probs[9][1:101] = 5*norm.pdf(np.arange(1, 101), 10, 5)
probs[10][1:101] = 5*norm.pdf(np.arange(1, 101), 10, 5)

# Gegenwahrscheinlichkeiten
against_probs = Against_Prob(probs)
probs[0] = against_probs


# In[6]:

from Parameter import Stock_Resource, Max_Stock_Resource, Condition_Storage


# inkl. Lagerhaltung

# In[7]:

#Lagerbestand
stock_resources = Stock_Resource(resources)
stock_resources[1] = 0

max_stock_resources = Max_Stock_Resource(resources)
for h in resources[1:]:
    max_stock_resources[h] = 2

# Systemzustände
condition_storages = Condition_Storage(capacities, resources, max_stock_resources, times)
# Bei der Modelformulierung mit Lagerproduktion wird der Parameter 'max_stocks' benötigt.


# In[112]:

from DynamicProgramm_Stock import DP_Stock, Structure_Stock, Opt_Politic_Stock


# In[113]:

solutions={}

a = datetime.datetime.now()

DP_Stock(solutions, condition_storages, products, resources, capacities, consumtions, times, revenues, probs, stock_resources, max_stock_resources)

b = datetime.datetime.now()
print 'Rechenezeit DP:', (b-a)


# In[ ]:

graph = Structure_Stock(solutions, condition_storages, products, resources, consumtions, revenues, probs, stock_resources, max_stock_resources)


# In[ ]:

Opt_Politic_Stock(solutions, resources, stock_resources, products)

