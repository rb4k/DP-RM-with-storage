# coding: utf-8

__version__ = '1.0'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = 'Sonntag, 16. August 2015 (MESZ)'
__copyright__ = "(C) 2015 Robert Matern"


import numpy as np
import datetime


# Parameter

def Product(j):
    '''Produkte 'j' aus 'J'.'''
    return np.arange(j+1, dtype=np.uint16)


def Resource(h):
    '''Ressourcen 'h' aus 'H'.'''
    return np.arange(h+1, dtype=np.uint16)


def Capacity(h):
    '''Kapazität 'c[h]' der Ressourcen 'h' aus 'H'.'''
    matrix = np.zeros(shape=(len(h)), dtype=np.int16)
    return matrix


def Consumption(j, h):
    '''Matrix 'A' mit den Parametern der Ressourcen-
    verbräuchen 'a[j,h]' für die Produkte 'j' aus 'J'
    und die Ressourcen 'h' aus 'H'.'''
    matrix = np.zeros(shape=(len(j),len(h)), dtype=np.uint16)
    return matrix


def Revenue(j):
    '''Erträge 'r[j]' der Produkte 'j' aus 'J'.'''
    vector = np.zeros(shape=(len(j)), dtype=np.uint16)
    return vector


def Time(t):
    '''Buchungshorizont 'T' mit einem Buchungs-
    zeitpunkt 't'.'''
    time = np.arange(t+1, dtype=np.uint16)
    time = time[::-1]
    return time


def Prob(j, t):
    '''Matrix 'Prob' mit den Parametern 'p[j,t]', die
    den Wahrscheinlichkeiten der Nachfrage nach einem
    Produkt 'j' in der Buchungsperiode 't' entspricht.
    --------------------------------------------------
    ACHTUNG: Perioden aufsteigend sortiert!!!
    --------------------------------------------------'''
    matrix = np.zeros(shape=(len(j),len(t)), dtype=np.float32)
    return matrix


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


# Mögliche Systemzustände

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


# Lagerparameter

def Stock_Resource(h):
    '''Lagerbestand 'y[h]' der Ressource 'h' aus 'H'.'''
    vector = np.zeros(shape=(len(h)), dtype=np.int16)
    return vector


def Max_Stock_Resource(h):
    '''Max. Lagerbestand 'ymax[h]' der Ressource 'h' aus 'H'.'''
    vector = np.zeros(shape=(len(h)), dtype=np.int16)
    return vector


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


# Leistungsperioden

def Performance_Time(times, resources):
    array = np.split(times[:-1], len(resources[:-1]))
    return array
