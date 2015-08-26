
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
import matplotlib.pyplot as plt
import graphviz as gv
import datetime

# In[3]:

# Funktionen werden hinzugeladen.
from Parameter import Product, Resource, Capacity, Consumption, Revenue, Time, Prob, Against_Prob


# In[4]:

# Produkte
products = Product(4)

# Ressourcen
resources = Resource(3)

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
times = Time(30)

# Normalverteilung
from scipy.stats import norm

# Wahrscheinlichkeiten
probs = Prob(products, times)
probs[1][1:16] = 0.2
probs[2][1:16] = 0.2
probs[3][1:] = 0.2
probs[4][1:] = 0.2

# Gegenwahrscheinlichkeiten
against_probs = Against_Prob(probs)
probs[0] = against_probs

# Systemzustände (ohne Lagerhaltung)
# conditions = Condition(capacities, resources, times)


# In[5]:

# plt.plot(probs[1:].T)
# plt.show


# inkl. Lagerhaltung

# In[ ]:

# Funktionen werden hinzugeladen.
from Parameter import Stock_Resource, Max_Stock_Resource, Condition_Storage

#Lagerbestand
stock_resources = Stock_Resource(resources)

max_stock_resources = Max_Stock_Resource(resources)
for h in resources[1:]:
    max_stock_resources[h] = 2

# Systemzustände
condition_storages = Condition_Storage(capacities, resources, max_stock_resources, times)
# Bei der Modelformulierung mit Lagerproduktion wird der Parameter 'max_stocks' benötigt.

print('Start der Rechnungen...')

# In[6]:

from DynamicProgramm_Stock import DP_Stock, Structure_Stock, Opt_Politic_Stock


# In[192]:
a = datetime.datetime.now()

solutions={}

DP_Stock(solutions, condition_storages, products, resources, capacities, consumtions, times, revenues, probs, stock_resources, max_stock_resources)

b = datetime.datetime.now()
print (b-a)

# In[193]:

# graph = Structure_Stock(solutions, condition_storages, products, resources, consumtions, revenues, probs, stock_resources, max_stock_resources)


# In[194]:

Opt_Politic_Stock(solutions, resources, stock_resources, products)


# In[ ]:
