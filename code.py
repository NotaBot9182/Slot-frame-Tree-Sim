import random
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

# --- Simulation Parameters from Problem Description ---
TOTAL_NODES = 50
MAX_DEPTH = 6
BUFFER_SIZE = 64
PACKET_GEN_MIN = 1
PACKET_GEN_MAX = 3
SIMULATION_DURATION = 2000 # Run for 2000 slotframes
# Slotframe lengths to test (for plotting)
SLOTFRAME_LENGTHS_TO_TEST = [31, 53, 101, 151, 211]

# --- Note: Autonomous Algorithm Parameters are NOT USED ---
# BUFFER_THRESHOLD_1 = 10
# BUFFER_THRESHOLD_2 = 25
# BUFFER_THRESHOLD_3 = 40

class Node:
    """Represents a single node in the tree.

    (Simplified for the parent-controlled logic)
    """

    def __init__(self, node_id, depth):
        self.id = node_id
        self.parent = None
        self.children = []
        self.depth = depth
        # Buffer for packets, max size 64
        self.buffer = deque(maxlen=BUFFER_SIZE)
        # Round-robin pointer for parent scheduling
        self.next_child_index = 0
        # --- Statistics ---
        self.packets_generated = 0
        self.packets_received_from_children = 0
        self.packets_forwarded_to_parent = 0
        self.packets_dropped_buffer_full = 0
        self.total_buffer_occupancy_sum = 0
        self.buffer_measurement_count = 0

    def reset_stats_for_new_run(self):
        """Resets all stats for a new simulation run."""
        self.buffer.clear()
        self.next_child_index = 0
        self.packets_generated = 0
        self.packets_received_from_children = 0
        self.packets_forwarded_to_parent = 0
        self.packets_dropped_buffer_full = 0
        self.total_buffer_occupancy_sum = 0
        self.buffer_measurement_count = 0

    def add_child(self, child_node):
        """Adds a child node and sets its parent."""
        self.children.append(child_node)
        child_node.parent = self

    def generate_packets(self):
        """Generate new packets (1-3) and add them to the buffer."""
        num_new_packets = random.randint(PACKET_GEN_MIN, PACKET_GEN_MAX)
        self.packets_generated += num_new_packets
        for _ in range(num_new_packets):
            packet = "pkt"
            if len(self.buffer) < BUFFER_SIZE:
                self.buffer.append(packet)
            else:
                self.packets_dropped_buffer_full += 1

    def receive_packet(self, packet):
        """Receive a packet from a child and add it to the buffer."""
        self.packets_received_from_children += 1
        if len(self.buffer) < BUFFER_SIZE:
            self.buffer.append(packet)
        else:
            self.packets_dropped_buffer_full += 1

    def get_avg_buffer_occupancy(self):
        """Calculates the average buffer occupancy for this node."""
        if self.buffer_measurement_count == 0:
            return 0
        return self.total_buffer_occupancy_sum / self.buffer_measurement_count

    def update_buffer_stats(self):
        """Call this once per slotframe to track average occupancy."""
        self.total_buffer_occupancy_sum += len(self.buffer)
        self.buffer_measurement_count += 1

    def __repr__(self):
        return (
            f"Node(id={self.id}, depth={self.depth}, children={len(self.children)}, "
            f"buffer_size={len(self.buffer)})"
        )


def create_random_tree(num_nodes, max_depth):
    """Generates a random tree topology, per problem description."""
    all_nodes = []
    root = Node(node_id=0, depth=0)
    all_nodes.append(root)
    potential_parents = [root]
    node_id_counter = 1

    while node_id_counter < num_nodes:
        if not potential_parents:
            parent = root
        else:
            parent_index = random.randint(0, len(potential_parents) - 1)
            parent = potential_parents[parent_index]

        new_depth = parent.depth + 1
        new_node = Node(node_id=node_id_counter, depth=new_depth)
        parent.add_child(new_node)
        all_nodes.append(new_node)
        node_id_counter += 1

        if new_depth < max_depth:
            potential_parents.append(new_node)

        if parent.depth >= max_depth - 1 and parent in potential_parents:
            potential_parents.remove(parent)

    return root, all_nodes

# --- Hash function is no longer used for scheduling ---
# def hash_func(node_id):
# ...

def visualize_tree(root_node):
    """Uses NetworkX and Matplotlib to draw the tree topology."""
    G = nx.Graph()
    labels = {}
    queue = deque([root_node])

    while queue:
        current_node = queue.popleft()
        G.add_node(current_node.id)
        labels[current_node.id] = f"{current_node.id}\n(D:{current_node.depth})"
        for child in current_node.children:
            G.add_node(child.id)
            G.add_edge(current_node.id, child.id)
            queue.append(child)

    print("\nVisualizing tree... Close the plot window to continue simulation.")
    try:
        pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
    except ImportError:
        print("pydot library not found. Falling back to spring layout.")
        print("For a better tree layout, run: pip install pydot")
        pos = nx.spring_layout(G, k=0.3)

    plt.figure(figsize=(16, 10))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_size=1000,
        node_color="lightblue",
        font_size=8,
        font_weight="bold",
        edge_color="gray",
    )
    plt.title(f"Random Tree Topology (50 Nodes, Max Depth 6)", fontsize=16)
    plt.show()


class Simulation:
    """Manages the entire network simulation over time."""

    def __init__(self, root_node, all_nodes, slotframe_length):
        self.root = root_node
        self.all_nodes = all_nodes
        self.slotframe_length = slotframe_length
        self.all_parents = [n for n in all_nodes if n.children]

        for node in self.all_nodes:
            node.reset_stats_for_new_run()

        self.total_packets_delivered_to_root = 0

    def run_one_slotframe(self):
        """Simulates a single slotframe using parent-controlled round-robin logic."""
        for node in self.all_nodes:
            if node != self.root:
                node.generate_packets()

        packets_in_transit = {}

        for _ in range(self.slotframe_length):
            for parent in self.all_parents:
                if not parent.children:
                    continue

                child = parent.children[parent.next_child_index]
                parent.next_child_index = (parent.next_child_index + 1) % len(parent.children)

                if child.buffer:
                    packet = child.buffer.popleft()
                    child.packets_forwarded_to_parent += 1
                    if parent not in packets_in_transit:
                        packets_in_transit[parent] = []
                    packets_in_transit[parent].append(packet)

        for parent, packet_list in packets_in_transit.items():
            for packet in packet_list:
                if parent == self.root:
                    self.total_packets_delivered_to_root += 1
                else:
                    parent.receive_packet(packet)

        for node in self.all_nodes:
            node.update_buffer_stats()

    def run_simulation(self, num_slotframes):
        """Runs the simulation for a fixed duration."""
        print(f"Running simulation for {num_slotframes} slotframes...")
        progress_interval = max(1, num_slotframes // 10)

        for i in range(num_slotframes):
            if i % progress_interval == 0:
                print(f" ...Slotframe {i}/{num_slotframes}")
            self.run_one_slotframe()
        print("Simulation complete.")

    def collect_and_print_stats(self):
        """Gathers all stats and prints the final report."""
        total_packets_generated_network_wide = 0
        total_packets_dropped_network_wide = 0
        total_buffer_occupancy_all_nodes = 0
        total_buffer_measurements_all_nodes = 0

        for node in self.all_nodes:
            total_packets_generated_network_wide += node.packets_generated
            total_packets_dropped_network_wide += node.packets_dropped_buffer_full
            total_buffer_occupancy_all_nodes += node.total_buffer_occupancy_sum
            total_buffer_measurements_all_nodes += node.buffer_measurement_count

        pdr = 0
        if total_packets_generated_network_wide > 0:
            pdr = self.total_packets_delivered_to_root / total_packets_generated_network_wide

        avg_buffer = 0
        if total_buffer_measurements_all_nodes > 0:
            avg_buffer = total_buffer_occupancy_all_nodes / total_buffer_measurements_all_nodes

        print("\n" + "=" * 50)
        print(f"PERFORMANCE REPORT (Slotframe Length: {self.slotframe_length})")
        print("=" * 50)
        print("\n--- Packet Delivery ---")
        print(f"Total Packets Generated (Network): {total_packets_generated_network_wide}")
        print(f"Total Packets Delivered (Root): {self.total_packets_delivered_to_root}")
        print(f"Packet Delivery Ratio (PDR): {pdr:.4f} ({pdr * 100:.2f}%)")

        print("\n--- Packet Loss ---")
        print(f"Total Dropped Packets (Buffer): {total_packets_dropped_network_wide}")
        print("\n--- Buffer Performance ---")
        print(f"Avg. Buffer Occupancy (Network): {avg_buffer:.2f} packets")
        print("=" * 50 + "\n")

        return {
            "slotframe_length": self.slotframe_length,
            "pdr": pdr,
            "avg_buffer_occupancy": avg_buffer,
            "dropped_packets": total_packets_dropped_network_wide,
            "total_generated": total_packets_generated_network_wide,
            "total_delivered": self.total_packets_delivered_to_root,
        }


# *** NEW FUNCTION TO PLOT RESULTS ***
def plot_simulation_results(plot_data):
    """Generates and displays plots for the simulation results."""
    print("Generating plots...")

    lengths = [d["slotframe_length"] for d in plot_data]
    pdr = [d["pdr"] for d in plot_data]
    avg_buffer = [d["avg_buffer_occupancy"] for d in plot_data]
    dropped = [d["dropped_packets"] for d in plot_data]
    generated = [d["total_generated"] for d in plot_data]
    delivered = [d["total_delivered"] for d in plot_data]
    loss_ratio = [
        d["dropped_packets"] / d["total_generated"] if d["total_generated"] > 0 else 0
        for d in plot_data
    ]

    plt.figure(figsize=(10, 6))
    plt.plot(lengths, generated, "o-", label="Total Generated")
    plt.plot(lengths, delivered, "s-", label="Total Delivered (Received by Root)")
    plt.plot(lengths, dropped, "x-", label="Total Dropped (Buffer Overflow)")
    plt.title("Packet Counts vs. Slotframe Length")
    plt.xlabel("Slotframe Length")
    plt.ylabel("Total Packets")
    plt.legend()
    plt.grid(True)
    plt.xticks(lengths)

    plt.figure(figsize=(10, 6))
    plt.plot(lengths, pdr, "o-", label="Packet Delivery Ratio (PDR)")
    plt.plot(lengths, loss_ratio, "x-", label="Packet Loss Ratio")
    plt.title("Network Ratios vs. Slotframe Length")
    plt.xlabel("Slotframe Length")
    plt.ylabel("Ratio (0.0 - 1.0)")
    plt.ylim(0, 1.0)
    plt.legend()
    plt.grid(True)
    plt.xticks(lengths)

    plt.figure(figsize=(10, 6))
    plt.plot(lengths, avg_buffer, "s-", label="Average Buffer Occupancy", color="purple")
    plt.title("Average Buffer Occupancy vs. Slotframe Length")
    plt.xlabel("Slotframe Length")
    plt.ylabel("Average Packets in Buffer")
    plt.legend()
    plt.grid(True)
    plt.xticks(lengths)

    print("Displaying plots... Close all plot windows to exit.")
    plt.show()


# --- Main execution ---
def main():
    print("Starting *** Parent-Controlled Priority *** Simulation...")
    plot_data = []
    print("Generating random tree topology...")
    root, all_nodes = create_random_tree(TOTAL_NODES, MAX_DEPTH)
    visualize_tree(root)

    for s_len in SLOTFRAME_LENGTHS_TO_TEST:
        sim = Simulation(root, all_nodes, s_len)
        sim.run_simulation(SIMULATION_DURATION)
        stats = sim.collect_and_print_stats()
        plot_data.append(stats)

    plot_simulation_results(plot_data)


if __name__ == "__main__":
    main()
