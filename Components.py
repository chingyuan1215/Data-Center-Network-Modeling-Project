"""
File: Components.py
Brief: This file contains the main classes for the data center, hub and user (a.k.a. receiver).
"""


class DataCenter:
    """
    Data center class
    :param name: name of the data center
    :param pool_size: available pool size (in MB) of the data center
    """

    def __init__(self, name, pool_size):
        self.name = name
        self.pool_size = pool_size


class Hub:
    def __init__(self, name, cost, bandwidth):
        """
        Hub class
        :param name: name of the hub
        :param cost: cost to use the hub
        :param bandwidth: maximum bandwidth (in MB) of the hub
        """
        self.name = name
        self.cost = cost
        self.bandwidth = bandwidth


class User:
    """
    User class
    :param name: name of the user
    :param need: data need of the user (in MB)
    """

    def __init__(self, name, need):
        self.name = name
        self.need = need
