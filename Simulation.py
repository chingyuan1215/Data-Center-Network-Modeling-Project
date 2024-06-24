"""
File: Simulation.py
Brief: This file contains the main simulation logic for the data center network simulation.
Code execution starts from this file.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import random
import json
from Optimization import *
from DCNetwork import DataCenterNetwork


def update_network(frame, network, max_users, ani_fig, max_seconds):
    plt.cla()  # Clear the current axes
    plt.axis('off')  # Ensure axis remains off for each frame

    # Determine active users randomly
    active_user_indices = sorted(random.sample(range(max_users), k=random.randint(1, max_users)))
    network.update_users(active_user_indices)

    # Generate and apply mock routing info
    routing_info = optimize_routing(network, active_user_indices)
    # routing_info = generate_mock_routing_info(network, active_user_indices)
    network.simulate_backend_communication(routing_info)

    # Visualize the network with the current routing
    network.visualize_routing()

    # Update the title to reflect the current simulation time correctly
    time_passed = frame if frame < max_seconds else max_seconds
    plt.title(f"Time: {time_passed + 1}s", fontsize=16)


with open("./Config.json", "r") as json_file:
    config = json.load(json_file)

dc_attrs = config["dc_attrs"]
hub_attrs = config["hub_attrs"]
max_users_attrs = config["max_users_attrs"]
max_seconds = config["max_seconds"]

network = DataCenterNetwork(dc_attrs, hub_attrs, max_users_attrs)
network.build_network()

fig = plt.figure(figsize=(12, 9))
ani = animation.FuncAnimation(fig, update_network, frames=range(max_seconds),
                              fargs=(network, len(max_users_attrs), fig, max_seconds),
                              interval=1000, repeat=False)

# Save the animation (optional)
# gif_writer = FFMpegWriter(fps=1)
# ani.save("./Sample.gif", writer=gif_writer)

plt.show()
