
# coding: utf-8

__version__ = '1.0'
__author__  = "Robert Matern (r.matern@stud.uni-hannover.de)"
__date__    = 'Sonntag, 16. August 2015 (MESZ)'
__copyright__ = "(C) 2015 Robert Matern"

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import graphviz as gv
import datetime


# Dynamisches Programm

def DP_Stock(solutions, conditions, products, resources, capacities, consumtions, times, revenues, probs, stocks, max_stocks):
    '''Berechnung der Erwartungswerte des Auftragsannahmeproblems inkl. Lagerhaltung.'''

    # Regeneration der Kapazitäten in dieser Rechnung nicht möglich!!!

    # Leere Wert für den Erwartungswert des aktuellen Systemzustands.
    value = 0

    #Aktueller Systemzustand wird generiert.
    condition = np.array(np.hstack((capacities[1:],stocks[1:],times[0])), dtype=np.int16)

    #Aktueller Systemzustand wird in dem 'np.array' aller möglichen Systemzustände gesucht.
    state = np.where((conditions == condition).all(axis=1))[0][0]

    # Memofunktion: Die Rechnung wird nur fortgeführt, sofern es nicht schon berechnet wurde.
    if state not in solutions:

        # Sofern es sich nicht um einen Endknoten des Entscheidungsbaums handelt,
        # werden folgende Schritte eingeleitet:
        if times[0]!=0:
            # Der Erwartungswert t-1 ohne Akeptanz wird ermittelt und im Wert 'reject' gespeichert.
            reject = DP_Stock(solutions, conditions, products, resources, capacities, consumtions, times[1:], revenues, probs, stocks, max_stocks)

            # Für die Aufträge wird ein Numpy-Array in der Länge der Anzahl an Produkten erstellt.
            max_order = np.zeros(shape=(len(products[1:])), dtype=np.float16)
            accept = np.zeros(shape=(len(products[1:])), dtype=np.float16)
            index_order = np.zeros(shape=(len(products)), dtype=np.uint8)
            oc_order = np.zeros(shape=(len(products[1:])), dtype=np.float16)

            reject_list = np.zeros(shape=(len(products[1:])), dtype=np.float16)


            # For-Schleife über alle Produkte, sofern die Kapazitäten keinen negativen Werte annehmen.
            product = (j for j in products[1:] if probs[j][times[0]] > 0)
            for j in product:

                change = capacities-consumtions[j]
                

                if np.all((change) >= np.float32(0)):
                    # Initialisierung der Rechnung für t-1 mit Akeptanz jeweils für ein Produkt j.
                    accept_j = DP_Stock(solutions, conditions, products, resources, change, consumtions, times[1:], revenues, probs, stocks, max_stocks)
                    oc = reject-accept_j
                    order = np.float32(revenues[j]-reject+accept_j)
                else:
                    # Erwartungswert für ein Produkt j enspricht
                    # der Grenzbedingung V(c,y,t)=-infinitely, falls c[j] < 0.
                    order = np.float16(0)
                    oc = np.float16(0)
                
                
                change_stock = np.cumsum(np.array(consumtions[j], dtype=np.uint8))
                decrease_stock = np.copy(stocks)
                decrease_stock = np.array(decrease_stock-change_stock, dtype=np.int16)

                if np.all((decrease_stock) >= np.float32(0)):
                    # Initialisierung der Rechnung für t-1 mit Akeptanz jeweils für ein Produkt j.
                    accept_stock_j = DP_Stock(solutions, conditions, products, resources, capacities, consumtions, times[1:], revenues, probs, decrease_stock, max_stocks)
                    oc_stock = reject-accept_stock_j
                    order_stock = np.float32(revenues[j]-reject+accept_stock_j)
                else:
                    # Erwartungswert für ein Produkt j enspricht
                    # der Grenzbedingung V(c,y,t)=-infinitely, falls c[j] < 0.
                    order_stock = np.float16(0)
                    oc_stock = np.float16(0)

                change_workup = np.cumsum(np.insert([np.array(consumtions[j], dtype=np.uint8)], 0, 0)[:-1])
                increase_stock = np.copy(stocks)
                increase_stock = np.array(increase_stock+change_workup, dtype=np.int16)

                if np.all((change) >= np.float32(0)) and np.all((increase_stock) <= (max_stocks)) and np.count_nonzero(change_workup)!=0:
                    # Initialisierung der Rechnung für t-1 mit Akeptanz jeweils für ein Produkt j.
                    accept_workup_j = DP_Stock(solutions, conditions, products, resources, change, consumtions, times[1:], revenues, probs, increase_stock, max_stocks)
                    oc_workup = reject-accept_workup_j
                    order_workup = np.float32(accept_workup_j-reject)
                    reject_list[j-1] = order_workup
                else:
                    # Erwartungswert für ein Produkt j enspricht
                    # der Grenzbedingung V(c,y,t)=-infinitely, falls c[j] < 0.
                    order_workup = np.float16(0)
                    oc_workup = np.float16(0)
                    reject_list[j-1] = order_workup

                list_order = np.hstack((0, order, order_stock, order_workup))
                max_order[j-1] = np.amax(list_order)
                index_order[j] = np.argmax(list_order)
                accept[j-1] = probs[j][times[0]]*max_order[j-1]
                list_oc = np.hstack((0, oc, oc_stock, oc_workup))
                oc_order[j-1] = list_oc[index_order[j]]

            # Sofern keine Anfrage eintrifft, kann ein beliebiger Bestand verwendet werden.
            list_reject = np.hstack((0, reject_list))
            max_reject = np.amax(list_reject)
            index_reject = np.argmax(list_reject)
            index_order[0] = index_reject

            # Summierung der Erwartungswerte ohne und mit Akzeptanz.
            value = np.float32(reject + np.sum(accept) + (probs[0][times[0]]*max_reject))
            # Einzelne Optionen werden nach ihrem erw. Ertrag indiziert.
            index = np.argmax(max_order)
            if np.all(max_order == 0):
                solutions[state] = [conditions[state], value, 0, 0, 0, index_order]
            else:
                solutions[state] = [conditions[state], value, index+1, index_order[index+1], revenues[index+1]-oc_order[index], index_order]
            print 'c[h]:', solutions[state][0][:len(resources)-1], '- y[h]:', solutions[state][0][len(resources)-1:-1], '- t:', solutions[state][0][-1], '- V(c,y,t):', solutions[state][1], '- d[0]:', solutions[state][5][:1], '- d[j]:', solutions[state][5][1:], '- j*:', solutions[state][2], '- OC[j*]:', solutions[state][4]
        # Sofern es sich um einen Endknoten handelt, werden folgende Schritte eingeleitet:
        else:
            # Erwartungswert enspricht der Grenzbedingung V(c,y,0)=0, für c >= 0.
            value = np.float32(0)
            # Ein Endzustand wird mit einem Erwartungswert 0 in das Dict "solutions" gespeichert.
            solutions[state] = [conditions[state], value, 0, 0, 0, np.zeros(len(products), dtype=np.uint8)]
            #print 'c[h]:', solutions[state][0][:len(resources)-1], '- y[h]:', solutions[state][0][len(resources)-1:-1], '- t:', solutions[state][0][-1], '- d(c,y,t):', solutions[state][5], '- V(c,y,t):', solutions[state][1], '- j*:', solutions[state][2], '- OC[j*]:', solutions[state][4]

    # Memofunktion: Sofern das Ergebnis breits berechnet wurde, wird der Wert aus dem Dict "solutions" verwendet.
    else:
        value = solutions[state][1]

    return value


# Erstellung der Datenstruktur als NetworkX-Graph

def Structure_Stock(solutions, conditions, products, resources, consumtions, revenues, probs, stocks, max_stocks):
    '''Generierung der Stuktur der Problemstellung.'''

    if len(solutions) < 100:
        # MultiDiGraph erstellen.
        graph=nx.MultiDiGraph()

        # Knoten für alle Lösungen (solutions) erstellen.
        for key in solutions.iterkeys():
            graph.add_node(key, label=solutions[key][0], value=solutions[key][1],
                       capacity=solutions[key][0][:(len(resources)-1)], time=solutions[key][0][-1],
                          stock=solutions[key][0][(len(resources)-1):-1])

        # Endknoten zur Nutzung der NetworkX-Algorithmen anlegen.
        graph.add_node("end", label='end', op=0, value=0,
                       capacity=0, stock=0, time=0)

        # Kanten erstellen.
        # Schleife über alle Lösungen.
        for i in solutions.iterkeys():
            # Handelt es sich um einen Zeitpunkt 0, dann wird der Systemzustand mit dem 'end'-Knoten verbunden.
            if solutions[i][0][-1] == 0:
                graph.add_edge(i, "end", key=0, modus=0, weight=0, revenue=0, time=0)
            # Sonst führe die Schleife aus.
            else:
                # Aufgrund der differenzierten Auftragsannahme erfolgt eine Schleife über alle Produkte.
                for j in products:
                    # Kapazitätsveränderung aufgrund der Anfragen nach Produkt 'j' wird erfasst.
                    change = np.copy(solutions[i][0][:len(resources)-1])
                    change = change-consumtions[j][1:]

                    # Zielzustand zur Ermittlung der Opportunitätskosten wird ermittelt.
                    no_reduction = np.append(solutions[i][0][:-1], solutions[i][0][-1]-1)
                    reject = np.where((conditions == no_reduction).all(axis=1))[0][0]

                    if j == 0:
                        graph.add_edge(i, reject, key='KA', modus='KA', label='KA', weight=0, weight_goal=solutions[reject][1], revenue=0, goal=solutions[reject][0], time=solutions[i][0][-1])
                    else:
                        # Keine negativen Kapazitätsbestände möglich.
                        if np.all((change) >= np.float32(0)):
                                # Zielzustand wird ermittelt.
                                reduction = np.hstack((change,solutions[i][0][len(resources)-1:-1],solutions[i][0][-1]-1))
                                state = np.where((conditions == reduction).all(axis=1))[0][0]
                                # Prüfung und Verknüpfung der Anfragen
                                if probs[j][solutions[i][0][-1]] > 0:
                                    # Abfrage, ob die Kante der optimalen Politik entspricht.
                                    if solutions[i][5][j]==1:
                                        graph.add_edge(i, state, key=str(j)+'-AA', modus='AA', label=str(j)+'-AA', weight=revenues[j]-solutions[reject][1]+solutions[state][1], weight_goal=solutions[state][1], revenue=revenues[j], goal=solutions[state][0], time=solutions[i][0][-1])
                                    else:
                                        graph.add_edge(i, state, key=str(j)+'-AA', modus='AA', label=str(j)+'-AA', style="dotted", weight=0, weight_goal=solutions[state][1], revenue=0, goal=solutions[state][0], time=solutions[i][0][-1])

                        # Lagerveränderung aufgrund der Anfragen nach Produkt 'j' wird erfasst.
                        change_stock = np.cumsum(np.array(consumtions[j][1:], dtype=np.uint8))
                        decrease_stock = np.copy(solutions[i][0][(len(resources)-1):-1])
                        decrease_stock = decrease_stock-change_stock
                        if np.all((decrease_stock) >= np.float32(0)):
                                # Zielzustand wird ermittelt.
                                reduction_stock = np.hstack((solutions[i][0][:len(resources)-1],decrease_stock,solutions[i][0][-1]-1))
                                state_stock = np.where((conditions == reduction_stock).all(axis=1))[0][0]
                                # Prüfung und Verknüpfung der Anfragen
                                if probs[j][solutions[i][0][-1]] > 0:
                                    # Abfrage, ob die Kante der optimalen Politik entspricht.
                                    if solutions[i][5][j]==2:
                                        graph.add_edge(i, state_stock, key=str(j)+'-LE', modus='LE', label=str(j)+'-LE', weight=revenues[j]-solutions[reject][1]+solutions[state_stock][1], weight_goal=solutions[state_stock][1], revenue=revenues[j], goal=solutions[state_stock][0], time=solutions[i][0][-1])
                                    else:
                                        graph.add_edge(i, state_stock, key=str(j)+'-LE', modus='LE', label=str(j)+'-LE', style="dotted", weight=0, weight_goal=solutions[state_stock][1], revenue=0, goal=solutions[state_stock][0], time=solutions[i][0][-1])

                        # Lagererhöhung aufgrund der Anfragen nach Produkt 'j' wird erfasst.
                        change_workup = np.cumsum(np.insert(np.array(consumtions[j][1:]), 0, 0)[:-1])
                        increase_stock = np.copy(solutions[i][0][(len(resources)-1):-1])
                        increase_stock = increase_stock+change_workup
                        if np.all((change) >= np.float32(0)) and np.all((increase_stock) <= (max_stocks[1:])) and np.count_nonzero(change_workup)!=0:
                            # Zielzustand wird ermittelt.
                            propagation_stock = np.hstack((change,increase_stock,solutions[i][0][-1]-1))
                            state_storage = np.where((conditions == propagation_stock).all(axis=1))[0][0]
                            # Prüfung und Verknüpfung der Anfragen
                            if probs[j][solutions[i][0][-1]] > 0:
                                # Abfrage, ob die Kante der optimalen Politik entspricht.
                                if solutions[i][5][j]==3:
                                    graph.add_edge(i, state_storage, key=str(j)+'-LP', modus='LP', label=str(j)+'-LP', weight=solutions[state_storage][1]-solutions[reject][1], weight_goal=solutions[state_storage][1], revenue=0, goal=solutions[state_storage][0], time=solutions[i][0][-1])
                                else:
                                    graph.add_edge(i, state_storage, key=str(j)+'-LP', modus='LP', label=str(j)+'-LP', style="dotted", weight=0, weight_goal=solutions[state_storage][1], revenue=0, goal=solutions[state_storage][0], time=solutions[i][0][-1])
                                # Kante für LP ohne Auftrag.
                                if probs[0][solutions[i][0][-1]] > 0:
                                    if solutions[i][5][0]==j:
                                        graph.add_edge(i, state_storage, key='0-LP('+str(j)+')', modus='LP', label='0-LP('+str(j)+')', weight=solutions[state_storage][1]-solutions[reject][1], weight_goal=solutions[state_storage][1], revenue=0, goal=solutions[state_storage][0], time=solutions[i][0][-1])
                                    else:
                                        graph.add_edge(i, state_storage, key='0-LP('+str(j)+')', modus='LP', label='0-LP('+str(j)+')', style="dotted", weight=0, weight_goal=solutions[state_storage][1], revenue=0, goal=solutions[state_storage][0], time=solutions[i][0][-1])

        draw = graph.copy()
        draw.remove_node('end')
                # Quelle: http://stackoverflow.com/a/11484144/4913569
                # ----
                # write dot file to use with graphviz
                # run "dot -Tpng test.dot >test.png"
        nx.write_dot(draw,'graph.dot')
        dot = gv.Source(nx.to_agraph(draw), filename='graph.gv')

            # same layout using matplotlib with no labels
            #pos=nx.graphviz_layout(draw,prog='dot')
            #plt.figure(figsize=(20,20))
            #plt.title("Entscheidungsbaum")
            #nx.draw(draw,pos,with_labels=True, node_size=500)
            #plt.savefig('Graph.png')
        return graph
    else:
        print 'Graph hat %i Knoten. Datenstruktur durch NetworkX ist nicht erstellt.' % len(solutions)


# Optimalen Politik als Datenbank speichern.

def Opt_Politic_Stock(solutions, resources, stocks, products):

    db = pd.DataFrame(index=solutions)

    db_res = []
    db_sto = []
    db_time = []
    db_sol = []
    db_op = []

    #array = np.array(solutions.values()).T
    #print array[0].T

    # Spalten für die Ressourcenkapazitäten erstellen.
    for res in resources[1:]:
        db_res.append('$c^{'+str(res)+'}$')
    db_cap = []
    for c in range(len(db_res)):
        cap = []
        for s in solutions:
            cap.append(solutions[s][0][c])
        db_cap.append(cap)

    # Spalten für die Lagerbestände erstellen.
    for sto in range(len(stocks[1:])):
        db_sto.append('$y^{'+str(sto+1)+'}$')
    db_stos = []
    for i in range(len(db_sto)):
        stos = []
        for s in solutions:
            stos.append(solutions[s][0][i+len(resources[1:])])
        db_stos.append(stos)

    for s in solutions:
        db_time.append(solutions[s][0][-1])
        db_sol.append(solutions[s][1])

    # Spalten für die optimale Politik.
    for j in range(len(products)):
        db_op.append('$d_{'+str(j)+'}$')
    db_ops = []
    for i in range(len(products)):
        ops = []
        for s in solutions:
            ops.append(solutions[s][5][i]*1)
        db_ops.append(ops)

    for i, res in enumerate(db_res):
        db[res] = db_cap[i]
    for k, sto in enumerate(db_sto):
        db[sto] = db_stos[k]
    db['$t$'] = db_time
    db['ExpValue'] = db_sol
    for i, op in enumerate(db_op):
        db[op] = db_ops[i]

    # Tabelle ausgeben.
    db = db.sort(['$t$'], ascending=0)
    db = db[db['$t$'] != 0]
    db.to_csv('Table_Optimal'+str(datetime.datetime.now())+'.csv', index=0)

    return db
