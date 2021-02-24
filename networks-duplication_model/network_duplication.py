#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
network_duplication.py

We will study an important class of network models that reproduces the power-law
degree distribution. This so-called “duplication model” is based on the
tinkering rule underlying many evolutionary processes (Solé and Valverde, 2020).

This model grows a network by introducing one single node at a time. At each
step, one newly introduced node (see Figure 1) randomly selects m target node(s)
and links to it with probability p, as well as to all ancestor nodes of the
target node, with probability q.

See network_model.pdf.

Version: 1.0
Author: Francisco Martinez Pico

Fecha: 1/12/2020
"""
import networkx as nx
import matplotlib.pyplot as plt
import random as rnd

def draw_network(graph):
    """
    Creates and shows the plot of our graph/network.

    ARGS:
        - graph (DiGraph): instance of the direceted graph class of
        Networkx module.
    """
    nx.draw(graph, with_labels=True, font_weight='bold')

    plt.show()

def get_seed_network():
    """
    Creates seed network to start our growth model by duplicaction. This seed
    will always be a network with two nodes (labelled as 1 and 2). Node 2 is
    linked to node 1.

    RETURNS:
        - DG (DiGraph): directed graph from networkx.
    """
    # Creating empty network:
    DG = nx.DiGraph()

    # Start form a seed netwrok with m nodes:
    DG.add_node(1)

    # Note that node labels indicate time/number of iteration.

    # Adding second node and linking:
    DG.add_node(2)

    # 'add_weighted_edes_from()' uses a list of tuples.
    # Create links form 1 to 2 with value = 1.
    DG.add_weighted_edges_from([(2, 1, 1)])

    return DG

def create_model(N, m, p, q):
    """
    Creates the model by duplication growth. Check the paper for more info about
    this tyoe of growht.

    INPUTS:
        - N (integer): number of nodes.
        - m (integer): number of targeted old nodes randomly selected.
        - p (integer): probability of linking to randomly-selected old nodes.
        - q (integer): probability of linking to ancesters of randomly-selected
        old nodes.

    RETURN:
        - DG (DiGraph): directed graph from Networkx module.
    """
    DG = get_seed_network()

    for new_node in range(3, N + 1): # starts 3 since already added 2 nodes.

        # As it is not specified, we randomly selects nodes without replacement.
        try: # Error while less than 4 nodes.
            selected_nodes = rnd.sample(list(DG.nodes), k = m)

        except: # While less than m nodes we take all in each iteration.
            selected_nodes = rnd.sample(list(DG.nodes), k = len(DG.nodes))

        # Create new node:
        DG.add_node(new_node)

        # Linking new node to randomly selected nodes:
        for old_node in selected_nodes:
            if p >= rnd.random():
                DG.add_weighted_edges_from([(new_node, old_node, 1)])

        # Linking new node to ancestors of randomly selected nodes:
        for old_node in selected_nodes:
            for succesor in DG.successors(old_node):
                if q >= rnd.random():
                    DG.add_weighted_edges_from([(new_node, succesor, 1)])

    return DG

def plot_degree(DG):
    """
    Recieves a graph and creates a plot showing P(k) among time (represented as
    node number simulating network growth).

    Task 1.

    INPUTS:
        - DG (DiGraph): directed graph from Networkx module.
    """
    fig = plt.figure() # Create figure
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # dim [left, bottom, width, height]
    net_nodes = DG.nodes # x bar of plot
    degree = list() # y bar of plot

    for i in net_nodes:
        degree.append(DG.degree(i))

    # Labels:
    ax.set_xlabel('Node')
    ax.set_ylabel('P(k)')
    ax.set_title('Distribution of P(k) according to node number')

    # Axes boundaries:
    plt.xlim([0, 100])
    plt.ylim([0, 100])

    # Barplot:
    ax.bar(net_nodes, degree)

    plt.show()

def plot_link(DG):
    """
    Plots number of links in our network model among time. Time is represented
    as node number.

    Task 2.

    INPUTS:
        - DG (DiGraph): directed graph from Networkx module.
    """
    fig = plt.figure() # Create figure
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # dim [left, bottom, width, height]
    time = DG.nodes # x bar of plot
    link_values = list # y bar of plot

    links_values = []

    for i in time:
        links_values.append(len(DG.out_edges(i)))

    # Labels:
    ax.set_xlabel('Time')
    ax.set_ylabel('L(N)')
    ax.set_title('Number of links among time')

    # Axes boundaries:
    plt.xlim([0, 100])
    plt.ylim([0, 100])

    # Barplot:
    ax.bar(time, links_values)

    plt.show()

def main():
    """
    Main program.
    """
    # Parameters:
    N = 100 # number of nodes
    m = 20 # randomly selected target node(s)
    p = 1 # probability of linking to target node
    q = 0.05 # probability of linking to ancestors of target node

    DG = create_model(N, m, p, q)

    # draw_network(DG)

    # plot_degree(DG)

    # plot_link(DG)

if __name__ == '__main__':
    main()
