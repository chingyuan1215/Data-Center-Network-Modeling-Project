# CSE 6730 Data Center Network Modeling Project

## Introduction

This project aims to explore, simulate, and analyze various data center network (DCN) topologies using NetworkX. Our goal is to understand the performance implications of different user-defined network configurations and identify optimal routing that meet the demands of modern data centers. We will leverage Python to simulate these topologies and evaluate their performance metrics such as bandwidth and cost. By analyzing the results, we aim to provide insights into the design and optimization of DCNs for large-scale internet services.

## Project Overview

In the realm of cloud computing and large-scale internet services, the efficiency and scalability of data center networks play a pivotal role. This project focuses on modeling DCN topologies, simulating their behavior under different conditions.

## Setup Instructions

I use an Anaconda Python 3.11 virtual environment on a Windows 11 laptop to run this project. You may use other Python environments like `venv` or `pipenv` to run the project, but I recommend using Anaconda to avoid any dependency issues.

To run the project, you will need to install the following dependencies:

1. `NetworkX`
2. `Matplotlib`
3. `NumPy`
4. `SciPy`
5. `FFmpeg` (for animations)
6. `Graphviz` (for visualizing the network topology): Install with command `conda install -c conda-forge graphviz`
7. `PyGraphviz`: Install with command `conda install -c conda-forge pygraphviz`
8. `GurobiPy` (for optimization; license needed): Refer to [Gurobi official documentation](https://support.gurobi.com/hc/en-us/articles/14799677517585-Getting-Started-with-Gurobi-Optimizer) page for installation instructions

Or you may directly create the environment using the `environment.yml` file provided.

Please run `Simulation.py` to start the simulation!
