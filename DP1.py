__author__ = 'Superuser'

import pydecode
import numpy as np

n = 10
chart = np.zeros(10)
chart[0] = 0
chart[1] = chart[0] + 1
for item in range(2, n):
    chart[item] = chart[item-1] + chart[item-2]
chart

chart = pydecode.ChartBuilder(np.arange(10))
chart.init(0)
chart.set(1, [[0]], labels=[0])

for item in range(2, n):
    chart.set(item, [[item-1, item-2]])
graph = chart.finish()

weights = pydecode.transform(graph, np.array([1.0]))
inside = pydecode.inside(graph, weights)
inside

pydecode.draw(graph, np.array(["+"]*10), graph.node_labeling)
