
# coding: utf-8

# In[25]:

__version__ = '0.3'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = ''
__url__     = ''
__copyright__ = "(C) 2015 Robert Matern"


# In[26]:

import numpy as np
import datetime


# #Parameter

# ###Produkte
# Ein Produkt $j$ aus der Menge an Produkten $\mathcal{J}$:

# In[27]:

def Product(j):
    '''Produkte j aus J.'''
    return np.arange(j+1, dtype=np.uint8)

def Product(number):
    i = []
    for n in range(number+1):
        i = i + [n]
    return i
# ###Ressourcen
# 
# Es gibt $h$ Ressourcen aus der Menge an Ressourcen $\mathcal{H}$:

# In[28]:

def Resource(h):
    '''Ressourcen h aus H.'''
    return np.arange(h+1, dtype=np.uint8)


# ### Kapazität der Ressourcen
# 
# Für jeder Ressource $h \in \mathcal{H}$ gibt es eine vordefinierte Kapazität der Ressourcen $c_h$:

# In[29]:

def Capacity(h):
    ''' Kapazität der Ressourcen h aus H.'''
    matrix = np.zeros(shape=(len(h)), dtype=np.int8)
    return matrix


# ### Ressourcenverbrauch
# 
# Die Matrix $\textbf{A}$ zeigt für eine jede Anfrage nach einem Produkt $j \in \mathcal{J}$ den dafür notwendigen Ressourcenverbrauch. Ein Vektor $a_{j}$ zeigt für ein Produkt $j \in \mathcal{J}$ den jeweiligen Ressourcenverbrauch:

# In[30]:

def Consumption(j, h):
    ''' Matrix der Ressourcenverbräuche für die Produkte j aus J
    und die Ressourcen h aus H.'''
    matrix = np.zeros(shape=(len(j),len(h)), dtype=np.uint8)
    return matrix


# ### Ertrag (Revenue)
# 
# Jedes Produkt $j$ erzielt einen Ertrag $r_j$:

# In[31]:

def Revenue(j):
    '''Erträge der Produkte j aus J.'''
    vector = np.zeros(shape=(len(j)), dtype=np.uint8)
    return vector


# ### Buchungsperioden
# 
# Der Buchungshorizont wird durch den Paramter $T$ definiert. Die jeweilig betrachtete Periode entspricht dem Parameter $t \in \{0,1,...,T+1\}$. Dabei verläuft der Buchungshorizont rückwärts in der Zeit, so dass die erste Buchungsperiode $t=T$ und die letzte Buchungsperiode $t=0$ entspricht. Dabei ist die Startperiode $T+1$:

# In[32]:

def Time(t):
    '''Buchungshorizont "t".'''
    time = np.arange(t+1, dtype=np.uint16)
    time = time[::-1]
    return time


# ### Wahrscheinlichkeit der Anfrage nach einem Produkt $j$
# 
# Eine Anfragen nach einem Produkte $j$ zum Zeitpunkt $t$ hat eine bestimmte Eintrittfahrscheinlichkeit $p_j(t)$:

# In[33]:

def Prob(j, t):
    '''Wahrscheinlichkeit der Anfrage nach einem
    Produkt "j" im Buchungsverlauf "t". '''
    matrix = np.zeros(shape=(len(j),len(t)))
    return matrix


# ### Gegenwahrscheinlichkeit keiner Produktanfrage 
# 
# Die Wahrscheinlichkeit, dass keine Anfrage eintrifft entspricht $p_0(t)$

# In[34]:

def Against_Prob(prob):
    ''' Gegenwahrscheinlichkeit keiner Produktanfrage.
    Dabei entspricht der Paramter "prob"
    der Wahrscheinlichkeit der Produktanfragen.'''
    matrix = prob.T
    matrix2 = np.zeros(shape=(len(matrix)))
    for i in range(0, len(matrix)):
        matrix2[i] = 1-(matrix[i].sum())
    return matrix2


# ##Systemzustände
# 
# ### Mögliche Systemzustände
# 
# Die möglichen Systemzustände werden in Abhängigkeit der Kapazitäten der Ressourcen ermittelt. Es handelt sich um das Kartesisches Produkt der Ressourcenkapazitäten.
# 
# $$ T\cdot\prod_{n=1}^n \textbf{c}_n = \textbf{c}_1 \times \;... \times\; \textbf{c}_{n}$$
# 
# Siehe nachfolgende Funktion:

# In[2]:

def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.
    
    Quelle: http://stackoverflow.com/a/1235363/4913569
    
    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.
        """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    
    return out


def Condition(capacities, resources, times):
    '''Berechnung der möglichen Systemzustände eines Netzwerks
    mit c Kapazitäten, r Ressourcen und t Perioden.'''

    a = datetime.datetime.now()
    
    arrays = [range(i) for i in capacities[1:]+1]
    for i in arrays:
        np.append(arrays, np.array(i))
    
    scope = cartesian(arrays)
    
    conditions = [
        [subset.copy(), j]
        for subset in scope
        for j in times
    ]
    
    b = datetime.datetime.now()
    print (b-a)
    return conditions
    

    

    return conditions
# ###Enzeitpunkte:
# 
# Endzeitpunkte des Netzwerks:
def End_Time(conditions):
    '''Endzeutpunkte in Abhängigkeit der möglichen
    Systemzustände "conditions". '''
    end_times = []
    for i in range(len(conditions)):
        if conditions[i][1] == 0:
            end_times = end_times + [conditions[i]]
    return end_times