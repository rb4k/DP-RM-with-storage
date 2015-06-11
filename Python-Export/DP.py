
# coding: utf-8

# In[1]:

__version__ = '0.3'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = ''
__url__     = ''
__copyright__ = "(C) 2015 Robert Matern"


# In[2]:

# import pandas as pd
import numpy as np
#import multiprocessing


# In[3]:

#import matplotlib.pyplot as plt
#get_ipython().magic(u'matplotlib inline')


# #Dynamisches Programm

# Die normale Modellformulierung des Auftragsannahmeproblems im Revenue Management von Instandhaltungsprozessen:
# 
# $$V(\textbf{c}, t) = \sum_{j \in \mathcal{J}}p_{j}(t)\max[V(\textbf{c}, t-1), r_{j} + V(\textbf{c}-\textbf{a}_j, t-1)] + p_{0}(t)V(\textbf{c}, t-1) $$
# 
# $$= V(\textbf{c}, t-1) + \sum_{j \in \mathcal{J}}p_{j}(t) \max[r_j - V(\textbf{c}, t-1) + V(\textbf{c}-\textbf{a}_j, t-1), 0]$$

# ## Algorithmus

# In[4]:

solutions = {}

def DP(solutions, conditions, products, resources, capacities, consumtions, times):
    '''Berechnung des maximal möglichen Erwartungswertes eines Auftragsannahmeproblems.'''
    
    # Leere Integer für den Erwartungswert
    value = 0
    
    # Über eine Schleife und einer If-Bedingung wird der aktuelle Systemzustand ermittelt.
    for g in range(len(conditions)):
        if np.array_equal(np.asarray(conditions[g][0]), capacities[1:]) and np.asarray(conditions[g][1]) == times[0]:
            
            # Memofunktion: Das DP wird nur fortgeführt, sofern es nicht schon berechnet wurde.
            if g not in solutions:
                
                # Sofern es sich nicht um einen Endknoten des Entscheidungsbaums handelt,
                # werden folgende Schritte eingeleitet:
                if times[0]!=0:
                    # Das DP(t-1) ohne Akeptanz wird gelöst und im Wert "value2" gespeichert.
                    value2 = (DP(solutions, conditions, products, resources, capacities, consumtions, times[1:]))
                    # Für das DP(t-1) mit Akzeptanz wird ein Numpy-Array in der Länge der Anzahl an Produkten erstellt.
                    value3 = np.zeros(shape=(len(products[1:])), dtype=np.float16)
                    # For-Schleife über alle Produkte, sofern die Kapazitäten keinen negativen Werte annehmen.
                    for j in products[1:]:
                        if np.all((capacities-consumtions[j]) >= 0):
                            # Initialisierung des DP(t-1) mit Akeptanz jeweils für ein Produkt j.
                            value3[j-1] = probs[j][0]*max(revenues[j]-
                                                          DP(solutions, conditions, products, resources, capacities, consumtions, times[1:])
                                                          +DP(solutions, conditions, products, resources, capacities-consumtions[j], consumtions, times[1:]),
                                                          0)
                        else:    
                            # Erwartungswert für ein Produkt j enspricht
                            # der Grenzbedingung V(c,t)=-∞, falls n[j] < 0.
                            value3[j-1] = 0
                    # Summierung des DP(t-1) ohne Akzeptanz sowie den Numpy-Array DP(t-1) mit Akzeptanz.
                    value = value2 + np.sum(value3)
                    # Für den aktuellen Systemzustand wird der Ertragswert in das Dict "solutions" gespeichert.
                    solutions[g] = [conditions[g], value]

                # Sofern es sich um einen Endknoten des Entscheidungsbaums handelt, werden folgende Schritte eingeleitet:
                else:
                    # Erwartungswert enspricht der Grenzbedingung V(c,0)=0, für n >= 0.
                    value = 0.0
                    # Ein Endzustand wird mit einem Erwartungswert 0 in das Dict "solutions" gespeichert.
                    solutions[g] = [conditions[g], value]
                    return value        
            
            # Memofunktion: Sofern das Ergebnis breits berechnet wurde, wird der Wert aus dem Dict "solutions" verwendet.
            else:
                value = solutions[g][1]
    
    return value


# ## Erstellung der Struktur als NetworkX-Graph

# In[ ]: