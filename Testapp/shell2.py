__author__ = 'Superuser'

shell = 2

import pickle

with open('entry.pickle', 'rb') as f:
    entry = pickle.load(f)

print(entry)