# Tree Network Simulation: Parent-Controlled Scheduling

A Python-based simulator for evaluating the performance of a tree-topology network using a **Parent-Controlled Round-Robin** scheduling algorithm. This project simulates packet generation, buffering, and forwarding across multiple nodes to analyze network metrics like Packet Delivery Ratio (PDR), buffer occupancy, and packet loss across different slotframe lengths.

## 🌳 Overview

This simulator models an IoT tree network where:
- Parent nodes control and schedule transmission slots for their child nodes
- Packets are generated randomly at each node and forwarded toward the root
- Finite buffers (64 packets per node) with packet drop mechanics simulate realistic network behavior
- Performance is evaluated across multiple slotframe configurations

## ✨ Features

- **Random Tree Topology Generation:** Automatically generates a random tree network with configurable constraints (e.g., 50 nodes, maximum depth of 6)
- **Parent-Controlled Scheduling:** Implements a strict round-robin polling mechanism where parent nodes sequentially allocate transmission slots to their children
- **Buffer Management:** Simulates realistic node behavior with finite buffer sizes (64 packets) and packet drop mechanics on overflow
- **Multi-Scenario Testing:** Automatically runs the simulation across multiple slotframe lengths (31, 53, 101, 151, 211) to compare performance
- **Built-in Visualizations:** 
  - Uses `NetworkX` to draw and display the generated network topology
  - Uses `Matplotlib` to generate performance graphs (PDR, Packet Loss, Buffer Occupancy) at the end of the simulation

## 📋 Prerequisites

Ensure you have **Python 3.7+** installed. Install the required dependencies:

```bash
pip install matplotlib networkx
```

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/NotaBot9182/Slot-frame-Tree-Sim.git
cd Slot-frame-Tree-Sim
```

2. Run the simulation:
```bash
python main.py
```

3. View the results:
   - Network topology visualization appears in a NetworkX window
   - Performance graphs are generated and displayed using Matplotlib

## 📊 Simulation Output

The simulator produces the following metrics:

| Metric | Description |
|--------|-------------|
| **PDR (Packet Delivery Ratio)** | Percentage of packets successfully delivered to the root node |
| **Packet Loss** | Number and percentage of packets dropped due to buffer overflow |
| **Buffer Occupancy** | Average buffer utilization across all nodes |
| **Slotframe Efficiency** | Performance comparison across different slotframe lengths |

## 🔧 Configuration

You can customize the simulation by modifying parameters in the main simulation file:

- **Number of nodes:** Adjust the network size
- **Maximum tree depth:** Control network hierarchy
- **Buffer size:** Change per-node buffer capacity (default: 64 packets)
- **Packet generation rate:** Modify traffic intensity
- **Slotframe lengths:** Test different scheduling configurations

Example:
```python
# Customize these parameters
NUM_NODES = 50
MAX_DEPTH = 6
BUFFER_SIZE = 64
SLOTFRAME_LENGTHS = [31, 53, 101, 151, 211]
```

## 📈 How It Works

1. **Topology Generation:** Random tree structure is created with the root node at level 0
2. **Scheduling:** Parent nodes maintain a round-robin queue of child nodes for slot allocation
3. **Packet Flow:** 
   - Packets are generated at each node with configurable probability
   - Packets are stored in node buffers
   - Parent nodes transmit on behalf of children during allocated slots
4. **Performance Analysis:** Metrics are collected at each time step and aggregated for reporting

## 📁 Project Structure

```
Slot-frame-Tree-Sim/
├── README.md                 # This file
├── main.py                   # Main simulation entry point
├── simulation.py             # Core simulation logic
├── network.py                # Network topology and node definitions
├── scheduler.py              # Parent-controlled scheduling implementation
└── visualization.py          # Graph generation and topology display
```

## 🧪 Example Use Cases

- **Network Planning:** Evaluate optimal slotframe lengths for different network sizes
- **Buffer Analysis:** Determine adequate buffer sizes for various traffic conditions
- **Protocol Evaluation:** Compare parent-controlled scheduling with other algorithms
- **IoT Deployment:** Predict performance characteristics before live deployment

## 📝 Performance Considerations

- Larger slotframes reduce scheduling overhead but increase latency
- Smaller buffers limit queue depth but increase packet loss
- Tree depth affects end-to-root delivery latency
- Traffic load significantly impacts buffer occupancy and PDR

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Suggest optimizations or new metrics to track

## 📄 License

This project is open source. Feel free to use it for research, education, and development purposes.

## 📞 Questions or Support

If you encounter any issues or have questions about the simulation:
1. Check the code comments for detailed explanations
2. Review the example configurations
3. Open an issue on the repository

## 🔗 Related Work

This simulator implements concepts from tree-based scheduling protocols used in:
- Wireless Sensor Networks (WSN)
- Low-Power Wide-Area Networks (LPWAN)
- IoT mesh network protocols

---

**Happy simulating! 🚀**
