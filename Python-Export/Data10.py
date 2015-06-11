
# coding: utf-8

# In[15]:

__version__ = '0.3'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = ''
__url__     = ''
__copyright__ = "(C) 2015 Robert Matern"


# #Beispieldaten Nr. 10

import Parameter


# In[17]:

# Produkte
products = Parameter.Product(5)

# Ressourcen
resources = Parameter.Resource(4)

#Kapazität
capacities = Parameter.Capacity(resources)
capacities[1] = 20
capacities[2] = 20
capacities[3] = 20
capacities[4] = 20
#capacities[5] = 5
#capacities[6] = 5
#capacities[7] = 5
#capacities[8] = 5
#capacities[9] = 5
#capacities[10] = 5
#capacities[11] = 5
#capacities[12] = 5
#capacities[13] = 5

# Ressourcenverbrauch
consumtions = Parameter.Consumption(products, resources)
consumtions[1] = [0,1,0,1,0]#,1,1,0,1,1,1,1,0,1]
consumtions[2] = [0,0,1,0,1]#,1,0,0,1,1,0,1,1,0]
consumtions[3] = [0,1,1,1,0]#,0]#,1,1,0,0,0,1,0,0]
consumtions[4] = [0,1,1,0,1]#,1]#,1,0,1,1,0,0,0,0]
consumtions[5] = [0,0,1,1,0]#,0]#,0,0,1,1,1,1,0,1]

# Erträge
revenues = Parameter.Revenue(products)
revenues[1] = 100
revenues[2] = 200
revenues[3] = 200
revenues[4] = 220
revenues[5] = 150

# Buchungshorizont
times = Parameter.Time(16)

# Wahrscheinlichkeiten
probs = Parameter.Prob(products, times)
#import random as rd
#for t in range(len(times)-1):
#    random = 0
#    for i in products[1:]:
#        i_random = rd.uniform(random, 10.0)
#        probs[i][t] = i_random/10.0
#        random = i_random
probs[1] = [0.5, 0.3, 0.1, 0.2, 0.1, 0.3, 0.2, 0.1, 0.2, 0.3, 0.1, 0.1, 0.1, 0.1, 0.2, 0.0, 0]
probs[2] = [0.2, 0.2, 0.1, 0.5, 0.1, 0.3, 0.2, 0.1, 0.2, 0.3, 0.0, 0.1, 0.1, 0.3, 0.2, 0.0, 0]
probs[3] = [0.1, 0.3, 0.2, 0.2, 0.1, 0.3, 0.1, 0.1, 0.2, 0.0, 0.3, 0.2, 0.3, 0.4, 0.0, 0.1, 0]
probs[4] = [0.0, 0.1, 0.1, 0.0, 0.6, 0.1, 0.2, 0.1, 0.1, 0.1, 0.3, 0.1, 0.2, 0.1, 0.5, 0.1, 0]
probs[5] = [0.1, 0.1, 0.2, 0.1, 0.1, 0.0, 0.2, 0.2, 0.2, 0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0]

# Gegenwahrscheinlichkeiten
#against_probs = Against_Prob(probs)

# Systemzustände
conditions = Parameter.Condition(capacities, resources, times)

# Endzeitpunkte
#end_times = End_Time(conditions)


# In[18]:

#len(conditions)


# In[ ]:

#get_ipython().magic(u'pdb')
#import datetime
#a = datetime.datetime.now()
#print DP.DP(solutions, conditions, products, resources, capacities, consumtions, times)
#print datetime.datetime.now()-a


# In[ ]:

# Erstellung der Struktur als NetworkX-Graph
#graph = Structure(solutions, products, consumtions, revenues)

# Ermittlung der besten Politik (Dijkstra Algorithmus)
#best_politic = Best_Politic(graph, times)

#for index in enumerate(best_politic[:-1]):
#    print "Für den Zeitpung %i ist die Annahme des Auftrags %i die beste Politik." % (times[index[0]], graph.edge[index[1]][best_politic[index[0]+1]]['adoption'])

