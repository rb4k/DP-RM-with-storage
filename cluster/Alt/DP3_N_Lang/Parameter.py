# coding: utf-8


__version__ = '0.3'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = ''
__url__     = ''
__copyright__ = "(C) 2015 Robert Matern"


import numpy as np
import datetime


# #Parameter

# ###Produkte
# Ein Produkt $j$ aus der Menge an Produkten $\mathcal{J}$:

def Product(j):
    '''Produkte 'j' aus 'J'.'''
    return np.arange(j+1, dtype=np.uint16)

def Product(number):
    i = []
    for n in range(number+1):
        i = i + [n]
    return i

# ###Ressourcen
# Es gibt $h$ Ressourcen aus der Menge an Ressourcen $\mathcal{H}$:

def Resource(h):
    '''Ressourcen 'h' aus 'H'.'''
    return np.arange(h+1, dtype=np.uint16)


# ### Kapazität der Ressourcen
#
# Für jeder Ressource $h \in \mathcal{H}$ gibt es eine vordefinierte Kapazität der Ressourcen $c_h$:

def Capacity(h):
    '''Kapazität 'c[h]' der Ressourcen 'h' aus 'H'.'''
    matrix = np.zeros(shape=(len(h)), dtype=np.int16)
    return matrix


# ### Ressourcenverbrauch
#
# Die Matrix $\textbf{A}$ zeigt für eine jede Anfrage nach einem Produkt $j \in \mathcal{J}$ den dafür notwendigen Ressourcenverbrauch. Ein Vektor $a_{j}$ zeigt für ein Produkt $j \in \mathcal{J}$ den jeweiligen Ressourcenverbrauch:

def Consumption(j, h):
    '''Matrix 'A' mit den Parametern der Ressourcen-
    verbräuchen 'a[j,h]' für die Produkte 'j' aus 'J'
    und die Ressourcen 'h' aus 'H'.'''
    matrix = np.zeros(shape=(len(j),len(h)), dtype=np.uint16)
    return matrix


# ### Ertrag (Revenue)
#
# Jedes Produkt $j$ erzielt einen Ertrag $r_j$:

def Revenue(j):
    '''Erträge 'r[j]' der Produkte 'j' aus 'J'.'''
    vector = np.zeros(shape=(len(j)), dtype=np.uint16)
    return vector


# ### Buchungsperioden
#
# Der Buchungshorizont wird durch den Paramter $T$ definiert. Die jeweilig betrachtete Periode entspricht dem Parameter $t \in \{0,1,...,T+1\}$. Dabei verläuft der Buchungshorizont rückwärts in der Zeit, so dass die erste Buchungsperiode $t=T$ und die letzte Buchungsperiode $t=0$ entspricht. Dabei ist die Startperiode $T+1$:

def Time(t):
    '''Buchungshorizont 'T' mit einem Buchungs-
    zeitpunkt 't'.'''
    time = np.arange(t+1, dtype=np.uint16)
    time = time[::-1]
    return time


# ### Wahrscheinlichkeit der Anfrage nach einem Produkt $j$
#
# Eine Anfragen nach einem Produkte $j$ zum Zeitpunkt $t$ hat eine bestimmte Eintrittfahrscheinlichkeit $p_j(t)$:

def Prob(j, t):
    '''Matrix 'Prob' mit den Parametern 'p[j,t]', die
    den Wahrscheinlichkeiten der Nachfrage nach einem
    Produkt 'j' in der Buchungsperiode 't' entspricht.
    --------------------------------------------------
    ACHTUNG: Perioden aufsteigend sortiert!!!
    --------------------------------------------------'''
    matrix = np.zeros(shape=(len(j),len(t)), dtype=np.float32)
    return matrix


# ### Gegenwahrscheinlichkeit keiner Produktanfrage
#
# Die Wahrscheinlichkeit, dass keine Anfrage eintrifft entspricht $p_0(t)$

def Against_Prob(prob):
    ''' Gegenwahrscheinlichkeit keiner Produktanfrage.
    Dabei entspricht der Paramter 'prob'
    der Wahrscheinlichkeit der Produktanfragen.'''
    matrix = prob.T
    matrix2 = np.zeros(shape=(len(matrix)), dtype=np.float32)
    for i in range(0, len(matrix)):
        if np.greater(np.sum(matrix[i]), np.float32(1.0)):
            raise ValueError('Wahrscheinlichkeit ist > 1 in der Buchungsperiode %i.' % i)
        else:
            matrix2[i] = np.subtract(np.float32(1.0), np.float32(np.sum(matrix[i])))
    return matrix2


# ### Tatsächlich eintreffende Nachfrage nach einem Produkt $j$
# Zur Ermittlung des Ertrags eines Beispielszenarios wird ein Vektor der tatsächlich eintreffenden Nachfrage nach einem Produkt $j\in \mathcal{J}$ zum Zeitpunkt $t\in T$ benötigt:

def Demand(j, t):
    '''Matrix 'Demand' der Tatsächlich eintreffende Anfragen
    nach einem Produkt 'j' in der Buchungsperiode 't'. Ein
    Eintrag entspricht dem Parameter dm[j,t], Element von {0,1}.
    ----------------------------------------------------------
    ACHTUNG: Perioden aufsteigend sortiert!!!
    ----------------------------------------------------------'''
    matrix = np.zeros(shape=(len(j),len(t)), dtype=np.bool_)
    return matrix

# ### Mögliche Systemzustände
# Die möglichen Systemzustände werden in Abhängigkeit der Kapazitäten der Ressourcen ermittelt. Es handelt sich um das Kartesisches Produkt der Ressourcenkapazitäten.

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


# ###Lagerbestand an Produkten
# Für ein Produkt $j$ aus der Menge an Produkten $\mathcal{J}$ existiert ein Lagerbestand $y_{j}$. Die Lagerbestände aller Produkte lassen sich in Vektorschreibweise als $\textbf{y}$ schreiben:

def Stock(j):
    '''Lagerbestand 'y[j]' des Produkts 'j' aus 'J'.'''
    vector = np.zeros(shape=(len(j)), dtype=np.int16)
    return vector


# ###Maximal möglicher Lagerbestand an Produkten
# Für ein Produkt $j$ aus der Menge an Produkten $\mathcal{J}$ existiert ein maximal möglicher Lagerbestand $y_{j}^{max}$. Die Lagerbestände aller Produkte lassen sich in Vektorschreibweise als $\textbf{y}^{max}$ schreiben:

def Max_Stock(j):
    '''Max. Lagerbestand 'ymax[j]' des Produkts 'j' aus 'J'.'''
    vector = np.zeros(shape=(len(j)), dtype=np.int16)
    return vector


# ###Lagerbestandsveränderung für das Produktlager
# Für ein Produkt $j$ aus der Menge an Produkten $\mathcal{J}$ existiert ein Vektor $\textbf{s}_{j}$, der die Veränderung des Lagerbestand definiert. Die Lagerbestandsveränderungen aller Produkte lassen sich in Matrixschreibweise als $\textbf{S}$ schreiben (Einheitsmatrix):

def Shift(j):
    '''Lagerbestandsveränderung 's[j]' des Produkts 'j' aus 'J'.'''
    matrix = np.identity(len(j), dtype=np.int16)
    return matrix


# ###Lagerbestand an Ressourcen
# Für eine Ressource $h$ aus der Menge der Ressourcen $\mathcal{H}$ existiert ein Lagerbestand $y_{h}^{res}$. Die Lagerbestände aller Ressourcen lassen sich in Vektorschreibweise als $\textbf{y}^{res}$ schreiben:

def Stock_Resource(h):
    '''Lagerbestand 'y[h]' der Ressource 'h' aus 'H'.'''
    vector = np.zeros(shape=(len(h)), dtype=np.int16)
    return vector


# ###Maximal möglicher Lagerbestand an Ressourcen
# Für eine Ressource $h$ aus der Menge an Produkten $\mathcal{H}$ existiert ein maximal möglicher Lagerbestand $y_{h}^{max,res}$. Die Lagerbestände aller Produkte lassen sich in Vektorschreibweise als $\textbf{y}^{max,res}$ schreiben:

def Max_Stock_Resource(h):
    '''Max. Lagerbestand 'ymax[h]' der Ressource 'h' aus 'H'.'''
    vector = np.zeros(shape=(len(h)), dtype=np.int16)
    return vector


# ###Regenerationsperiode
# Für eine jede Buchungsperiode t existiert ein Parameter $\tilde{t}$. Der Parameter $\tilde{t}$ entspricht der Regenerationsperiode, wobei er den Wert $\tilde{t}$=1 annimmt, sofern zu der Buchungsperiode $t$ die Kapaziäten $c_h$ der Ressourcen $h\in\mathcal{H}$ regeneriert werden, und sonst $\tilde{t}=0$.

def Time_Regeneration(t):
    '''Regenerationshorizont 'T-Tilde' mit einem Regenerations-
    zeitpunkt 't-Tilde'.'''
    vector = np.zeros(shape=(len(t)), dtype=np.bool_)
    return vector


# ### Mögliche Systemzustände inkl. Lagerhaltung
# Die möglichen Systemzustände werden bei der Auftragsannahme mit Lagerhaltung in Abhängigkeit der Kapazitäten der Ressourcen und des Lagerbestands ermittelt. Es handelt sich um das Kartesisches Produkt der Ressourcenkapazitäten.

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
    print 'Rechenzeit für Systemzustände:', (b-a)
    return conditions[::-1]


# ### Leistungsperioden

def Performance_Time(times, resources):
    array = np.split(times[:-1], len(resources[:-1]))
    return array
