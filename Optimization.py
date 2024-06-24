"""
File: Optimization.py
Brief: This file contains the main optimization logic for the data center network simulation.
"""

import random
import gurobipy as gp
from gurobipy import *


def generate_mock_routing_info(network, active_user_indices):
    """
    This function is just for testing and needs to be replaced with a real routing algorithm!
    Generates mock routing information for the network.
    Each edge in the path from Data Center to Users through Hubs is assigned a random traffic intensity.
    :param network: the data center network object (NetworkX graph)
    :param active_user_indices: the list of active user indices
    """
    routing_info = {}
    for dc in network.data_centers:
        for hub in network.hubs:
            routing_info[(dc.name, hub.name)] = random.randint(0, 2)
            for user_index in active_user_indices:
                user_name = f"User_{user_index + 1}"
                if (hub.name, user_name) in network.graph.edges:
                    routing_info[(hub.name, user_name)] = random.randint(0, 3)
    return routing_info

def optimize_routing(network, active_user_indices):
    # print(active_user_indices)
    # print(network.users)
    ld = len(network.data_centers)
    lh = len(network.hubs)
    lu = len(active_user_indices)

    # in cases of zero dcs, hubs, or users, return empty dictionary
    if ld == 0 or lh == 0 or lu == 0:
        return {}

    optimization = gp.Model("Data Routing Optimization")

    # variable x_du is a binary variable that determines whether we pick datacenter d for user u
    x = {d: {u: optimization.addVar(vtype=GRB.BINARY) for u in range(lu)} for d in range(ld)}

    # variable y_hu is a binary variable that determines whether we pick hub h for user u
    y = {h: {u: optimization.addVar(vtype=GRB.BINARY) for u in range(lu)} for h in range(lh)}

    # must have 1 and only 1 datacenter and hub for each user
    for u in range(lu):
        optimization.addLConstr(gp.quicksum(x[d][u] for d in range(ld)), GRB.EQUAL, 1)
        optimization.addLConstr(gp.quicksum(y[h][u] for h in range(lh)), GRB.EQUAL, 1)

    # must not exceed each datacenter's pool size
    for d in range(ld):
        optimization.addLConstr(gp.quicksum(x[d][u] * network.users[u].need for u in range(lu)), GRB.LESS_EQUAL, network.data_centers[d].pool_size)

    # must not exceed each hub's bandwidth
    for h in range(lh):
        optimization.addLConstr(gp.quicksum(y[h][u] * network.users[u].need for u in range(lu)), GRB.LESS_EQUAL, network.hubs[h].bandwidth)

    # minimize the total cost
    optimization.setObjective(gp.quicksum(y[h][u] * network.hubs[h].cost for h in range(lh) for u in range(lu)), GRB.MINIMIZE)
    optimization.optimize()

    # print(GRB.OPTIMAL)

    # if model is infeasible return an empty dictionary
    if GRB.OPTIMAL == 3:
        return {}

    routing_info = {}
    choice = {}
    for u in range(lu):
        for h in range(lh):
            if y[h][u].x == 1:
                user_name = f"User_{active_user_indices[u] + 1}"
                hub_name = network.hubs[h].name
                routing_info[(hub_name, user_name)] = network.users[u].need
                choice[user_name] = hub_name

    for u in range(lu):
        for d in range(ld):
            if x[d][u].x == 1:
                user_name = f"User_{active_user_indices[u] + 1}"
                hub_name = choice[user_name]
                dc_name = network.data_centers[d].name
                if (dc_name, hub_name) not in routing_info:
                    routing_info[(dc_name, hub_name)] = network.users[u].need
                else:
                    routing_info[(dc_name, hub_name)] += network.users[u].need

    return routing_info
