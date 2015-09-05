
# coding: utf-8

# In[1]:

__version__ = '1.0'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = 'Sonntag, 16. August 2015 (MESZ)'
__copyright__ = "(C) 2015 Robert Matern"


# In[2]:

import numpy as np
import datetime


# #Parameter

# ## Parameter für das Grundmodell
# ###Produktanfrage
# Eine Produktanfrage $j$ aus der Menge an Produktanfragen $\mathcal{J}$:

# In[3]:

def Product(j):
    '''Produkte 'j' aus 'J'.'''
    return np.arange(j+1, dtype=np.uint16)


# ###Ressourcen
# 
# Eine Ressourcen $h$ aus der Menge an Ressourcen $\mathcal{H}$:

# In[4]:

def Resource(h):
    '''Ressourcen 'h' aus 'H'.'''
    return np.arange(h+1, dtype=np.uint16)


# ### Kapazität der Ressourcen
# 
# Für jeder Ressource $h \in \mathcal{H}$ gibt es eine vordefinierte Kapazität $c_h$:

# In[5]:

def Capacity(h):
    '''Kapazität 'c[h]' der Ressourcen 'h' aus 'H'.'''
    matrix = np.zeros(shape=(len(h)), dtype=np.int16)
    return matrix


# ### Ressourcenverbrauch
# 
# Die Matrix $\textbf{A}$ zeigt für eine jede Produktanfrage $j \in \mathcal{J}$ den dafür notwendigen Ressourcenverbrauch. Ein Vektor $\textbf{a}_{j}$ zeigt für eine Produktanfrage $j \in \mathcal{J}$ den jeweiligen Ressourcenverbrauch:

# In[6]:

def Consumption(j, h):
    '''Matrix 'A' mit den Parametern der Ressourcen-
    verbräuchen 'a[j,h]' für die Produkte 'j' aus 'J'
    und die Ressourcen 'h' aus 'H'.'''
    matrix = np.zeros(shape=(len(j),len(h)), dtype=np.uint16)
    return matrix


# ### Ertrag (Revenue)
# 
# Jede Produktanfrage $j\in\mathcal{J}$ erzielt einen Ertrag $r_j$:

# In[7]:

def Revenue(j):
    '''Erträge 'r[j]' der Produkte 'j' aus 'J'.'''
    vector = np.zeros(shape=(len(j)), dtype=np.uint16)
    return vector


# ### Buchungsperioden
# 
# Der Buchungshorizont wird durch den Paramter $T$ definiert. Die jeweilig betrachtete Periode entspricht dem Parameter $t$. Dabei verläuft der Buchungshorizont rückwärts in der Zeit, so dass die erste Buchungsperiode $t=T$ und die letzte Buchungsperiode $t=0$ entspricht:

# In[8]:

def Time(t):
    '''Buchungshorizont 'T' mit einem Buchungs-
    zeitpunkt 't'.'''
    time = np.arange(t+1, dtype=np.uint16)
    time = time[::-1]
    return time


# ### Wahrscheinlichkeit der Produktanfrage $j$
# 
# Eine Produktanfrage $j$ zum Zeitpunkt $t$ hat eine bestimmte Eintrittfahrscheinlichkeit $p_j(t)$:

# In[9]:

def Prob(j, t):
    '''Matrix 'Prob' mit den Parametern 'p[j,t]', die
    den Wahrscheinlichkeiten der Nachfrage nach einem
    Produkt 'j' in der Buchungsperiode 't' entspricht.
    --------------------------------------------------
    ACHTUNG: Perioden aufsteigend sortiert!!!
    --------------------------------------------------'''
    matrix = np.zeros(shape=(len(j),len(t)))
    return matrix


# ### Gegenwahrscheinlichkeit keiner Produktanfrage 
# 
# Die Wahrscheinlichkeit, dass keine Anfrage eintrifft entspricht $p_0(t)$

# In[10]:

def Against_Prob(prob):
    ''' Gegenwahrscheinlichkeit keiner Produktanfrage.
    Dabei entspricht der Paramter 'prob'
    der Wahrscheinlichkeit der Produktanfragen.'''
    matrix = prob.T
    matrix2 = np.zeros(shape=(len(matrix)), dtype=np.float32)
    for i in range(0, len(matrix)):
        if matrix[i].sum() > np.float32(1.0):
            raise ValueError('Wahrscheinlichkeit ist > 1 in der Buchungsperiode %i.' % i)
        else:
            matrix2[i] = np.float32(1.0)-np.float32(matrix[i].sum())
    return matrix2


# ## Parameter für die Memofunktion
# ### Mögliche Systemzustände
# 
# Die möglichen Systemzustände werden in Abhängigkeit der Kapazitäten der Ressourcen ermittelt. Es handelt sich um das Kartesisches Produkt der Ressourcenkapazitäten.

# In[11]:

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
    arrays.append(times)
    for i in arrays:
        np.append(arrays, np.array(i))
    
    conditions = cartesian(arrays)
    
    b = datetime.datetime.now()
    print (b-a)
    return conditions[::-1]


# ### Mögliche Systemzustände inkl. Lagerhaltung
# 
# Die möglichen Systemzustände werden bei der Auftragsannahme mit Lagerhaltung in Abhängigkeit der Kapazitäten der Ressourcen und des Lagerbestands ermittelt. Es handelt sich um das Kartesisches Produkt der Ressourcenkapazitäten.

# In[12]:

def Condition_Storage(capacities, resources, stocks, times):
    '''Berechnung der möglichen Systemzustände eines Netzwerks
    mit c Kapazitäten, r Ressourcen und t Perioden.'''

    a = datetime.datetime.now()
    
    arrays = [range(i) for i in capacities[1:]+1]
    stock_arrays = [range(i) for i in stocks[1:]+1]
    for i in stock_arrays:
        arrays.append(i)
    arrays.append(times)
    conditions = cartesian(arrays)
    
    b = datetime.datetime.now()
    print (b-a)
    return conditions[::-1]


# ## Parameter für die Lagerhaltung
# ###Lagerbestand
# Es existiert ein Lagerbestand $y_{h}$ an bereits reparierten Produkten. Dabei sind die Produkte mit den jeweiligen Ressourcen substituierbar. Die Lagerbestände lassen sich in Vektorschreibweise als $\textbf{y}$ schreiben:

# In[16]:

def Stock_Resource(h):
    '''Lagerbestand 'y[h]' der Ressource 'h' aus 'H'.'''
    vector = np.zeros(shape=(len(h)), dtype=np.int16)
    return vector


# ###Maximal möglicher Lagerbestand
# 
# Es existiert für ein jedes bereits repariertes Produkt ein maximal möglicher Lagerbestand $y_{h}^{max}$. Die Lagerbestände aller reparierten Produkte lassen sich in Vektorschreibweise als $\textbf{y}^{max}$ schreiben:

# In[17]:

def Max_Stock_Resource(h):
    '''Max. Lagerbestand 'ymax[h]' der Ressource 'h' aus 'H'.'''
    vector = np.zeros(shape=(len(h)), dtype=np.int16)
    return vector

