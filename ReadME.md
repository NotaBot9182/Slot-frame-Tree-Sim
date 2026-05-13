python simulation.py
   Here is a comprehensive and professionally formatted `README.md` file for your GitHub repository.
```md
# Tree Network Simulation: Parent-Controlled Scheduling

This repository contains a Python-based simulator for evaluating the performance of a tree-topology network using a **Parent-Controlled Round-Robin** scheduling algorithm. It simulates packet generation, buffering, and forwarding across multiple nodes to analyze network metrics like Packet Delivery Ratio (PDR), buffer occupancy, and packet loss across different slotframe lengths.

## 🚀 Features

* **Random Tree Topology Generation:** Automatically generates a random tree network with configurable constraints (e.g., 50 nodes, maximum depth of 6).
* **Parent-Controlled Scheduling:** Implements a strict round-robin polling mechanism where parent nodes sequentially allocate transmission slots to their children.
* **Buffer Management:** Simulates realistic node behavior with finite buffer sizes (64 packets) and packet drop mechanics on overflow.
* **Multi-Scenario Testing:** Automatically runs the simulation across multiple slotframe lengths (31, 53, 101, 151, 211) to compare performance.
* **Built-in Visualizations:** 
  * Uses `NetworkX` to draw and display the generated network topology.
  * Uses `Matplotlib` to generate performance graphs (PDR, Packet Loss, Buffer Occupancy) at the end of the simulation.

## 📋 Prerequisites

Ensure you have Python 3.7+ installed. You will need the following Python packages to run the simulation and view the graphs:

```bash
pip install matplotlib networkx
