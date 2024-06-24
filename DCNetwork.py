"""
File: DCNetwork.py
Brief: This file creates a data center network (DCN) structure and implements the visualization logic.
"""

import networkx as nx
import random
import matplotlib.pyplot as plt
from Components import *


class DataCenterNetwork:
    def __init__(self, data_centers_attrs, hubs_attrs, max_users_attrs):
        """
        Creates a multi-tier directed network structure with Data Centers, Hubs, and Users
        :param data_centers_attrs: the attribute list of data centers
        :param hubs_attrs: the attribute list of hubs
        :param max_users_attrs: the attribute list of users
        """
        self.data_centers_attrs = data_centers_attrs
        self.hubs_attrs = hubs_attrs
        self.max_users_attrs = max_users_attrs
        self.graph = nx.DiGraph()  # Directed graph (a NetworkX object)
        self.data_centers = []
        self.hubs = []
        self.users = []

    def generate_nodes(self):
        """
        generate nodes for the graph initially
        :return null
        """
        # Generate Data Centers with external attributes
        for i, attrs in enumerate(self.data_centers_attrs):
            dc = DataCenter(f"DC_{i + 1}", **attrs)
            self.data_centers.append(dc)
            self.graph.add_node(dc.name, type='Data Center', **attrs)

        # Generate Hubs with external attributes
        for i, attrs in enumerate(self.hubs_attrs):
            hub = Hub(f"Hub_{i + 1}", **attrs)
            self.hubs.append(hub)
            self.graph.add_node(hub.name, type='Hub', **attrs)

        # Users are dynamically managed, so not generated here
        # Generate Users with external attributes
        # for i, attrs in enumerate(self.max_users_attrs):
        #     user = User(f"User_{i + 1}", **attrs)
        #     self.users.append(user)
        #     self.graph.add_node(user.name, type='User', **attrs)

    def update_users(self, active_user_indices):
        """
        update the current network structure based on the current active users
        :param active_user_indices: current active user indices
        :return: null
        """
        # Remove all current users and their edges
        self.users = []
        self.graph.remove_nodes_from([n for n, d in self.graph.nodes(data=True) if d.get('type') == 'User'])

        # Add new users based on active indices
        for i in active_user_indices:
            if i < len(self.max_users_attrs):
                attrs = self.max_users_attrs[i]
                user = User(f"User_{i + 1}", **attrs)
                self.users.append(user)
                self.graph.add_node(user.name, type='User', **attrs)

        # Re-generate edges from Hubs to new Users
        for hub in self.hubs:
            for user in self.users:
                self.graph.add_edge(hub.name, user.name)

    def generate_edges(self):
        """
        initial edge generation
        :return: null
        """
        # Initial edge generation is for Data Centers to Hubs only
        for dc in self.data_centers:
            for hub in self.hubs:
                self.graph.add_edge(dc.name, hub.name)

        # for hub in self.hubs:
        #     for user in self.users:
        #         self.graph.add_edge(hub.name, user.name)

    def build_network(self):
        """
        Initial data center network generation
        :return: null
        """
        self.generate_nodes()
        self.generate_edges()

    def simulate_backend_communication(self, routing_info):
        """
        Simulate the communication with the backend to get the routing information.
        For this example, routing_info is a dict where keys are edge tuples and values are traffic intensities.
        """
        nx.set_edge_attributes(self.graph, 0, 'traffic_intensity')  # Reset all to 0
        nx.set_edge_attributes(self.graph, routing_info, 'traffic_intensity')  # Update with new routing info

    def visualize_routing(self):
        # fig, ax = plt.subplots(figsize=(15, 10))
        # ax.axis('off')
        pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot')
        edges = self.graph.edges(data=True)
        non_zero_edges = [(u, v) for u, v, d in edges if d['traffic_intensity'] > 0]
        edge_colors = [self.graph[u][v]['traffic_intensity'] for u, v in non_zero_edges]

        min_width = 1
        max_width = 10
        max_weight = max(edge_colors)
        min_weight = min(edge_colors)

        scaled_weights = [
            min_width + (max_width - min_width) * (weight - min_weight) / (max_weight - min_weight + 1e-9)
            for weight in edge_colors
        ]

        # Separate nodes by type
        data_center_nodes = [node for node, attr in self.graph.nodes(data=True) if attr['type'] == 'Data Center']
        hub_nodes = [node for node, attr in self.graph.nodes(data=True) if attr['type'] == 'Hub']
        user_nodes = [node for node, attr in self.graph.nodes(data=True) if attr['type'] == 'User']

        # Draw nodes with different colors for each type
        nx.draw_networkx_nodes(self.graph, pos, nodelist=data_center_nodes,
                               node_color='skyblue', node_size=1000, label='Data Centers')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=hub_nodes,
                               node_color='lightgreen', node_size=1000, label='Hubs')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=user_nodes,
                               node_color='salmon', node_size=1000, label='Users')

        nx.draw_networkx_labels(self.graph, pos=pos, font_family='Georgia', verticalalignment='baseline')
        nx.draw_networkx_edges(self.graph, pos, edgelist=non_zero_edges,
                               width=scaled_weights, edge_color='m', alpha=0.6)
        plt.axis('off')
        # plt.show()


# just for testing
# dc_attrs = [{'pool_size': 5000}, {'pool_size': 6000}]
# hub_attrs = [{'cost': 20, 'bandwidth': 500}, {'cost': 25, 'bandwidth': 600}]
# max_users_attrs = [{'need': 100}, {'need': 150}, {'need': 200}, {'need': 250}, {'need': 300}, {'need': 350}]
# network = DataCenterNetwork(dc_attrs, hub_attrs, max_users_attrs)
# network.build_network()

# just for testing
# active_users = [0, 1, 3]  # Active users are "User_1", "User_2", and "User_4"
# network.update_users(active_users)
# mock_routing_info = {('Hub_1', 'User_1'): 5, ('Hub_1', 'User_2'): 3, ('Hub_2', 'User_4'): 4}  # Example routing info
# network.simulate_backend_communication(mock_routing_info)
# network.visualize_routing()
