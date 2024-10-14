import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from collections import defaultdict
from queue import Queue


# Node class to represent the binary tree
class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


# Function to add nodes to the graph for visualization
def add_edges(graph, root, pos, x=0, y=0, layer=1):
    if root is None:
        return
    graph.add_node(root.data, pos=(x, y))
    if root.left:
        graph.add_edge(root.data, root.left.data)
        add_edges(graph, root.left, pos, x - 1 / layer, y - 1, layer + 1)
    if root.right:
        graph.add_edge(root.data, root.right.data)
        add_edges(graph, root.right, pos, x + 1 / layer, y - 1, layer + 1)


# Corrected Bottom View function
class Solution:
    def bottomView(self, root):
        if root is None:
            return []

        mpp = defaultdict(int)  # Store node data for each vertical index
        q = Queue()  # Perform BFS
        q.put((root, 0))  # (node, vertical index)

        # Store queue states for visualization
        queue_states = []

        while not q.empty():
            # Capture the current queue state before processing
            queue_states.append(list(q.queue))

            node, line = q.get()

            # Always update with the latest (bottom-most) node at this line
            mpp[line] = node.data

            if node.left:
                q.put((node.left, line - 1))
            if node.right:
                q.put((node.right, line + 1))

        # Extract bottom view nodes in order of their vertical indices
        bottom_view = [mpp[key] for key in sorted(mpp)]
        return bottom_view, mpp, queue_states


# Function to animate the queue and tree traversal
def animate_bottom_view_with_queue(bottom_view_map, queue_states, tree_root):
    fig, (ax_tree, ax_queue) = plt.subplots(2, 1, figsize=(8, 10))
    tree = nx.DiGraph()

    # Add edges to the tree graph
    add_edges(tree, tree_root, pos={})
    pos = nx.get_node_attributes(tree, "pos")

    visited_bottom_view = []

    def update(frame):
        ax_tree.clear()
        ax_queue.clear()

        # Draw the base tree
        nx.draw(
            tree,
            pos,
            ax=ax_tree,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_size=10,
        )
        ax_tree.set_title("Tree Traversal")

        # Highlight the visited nodes in the bottom view
        if frame < len(bottom_view_map):
            visited_bottom_view.append(list(bottom_view_map.values())[frame])

        nx.draw_networkx_nodes(
            tree,
            pos,
            nodelist=visited_bottom_view,
            node_color="orange",
            node_size=700,
            ax=ax_tree,
        )

        # Display the current queue state
        current_queue = queue_states[frame]
        queue_text = "Queue: " + " -> ".join(
            [f"({node.data}, {line})" for node, line in current_queue]
        )
        ax_queue.text(0.5, 0.5, queue_text, fontsize=12, ha="center", va="center")
        ax_queue.axis("off")

    # Create the animation
    ani = FuncAnimation(
        fig, update, frames=len(queue_states), interval=1000, repeat=False
    )
    plt.show()


# Creating the binary tree
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.right.left = Node(9)
root.right.right = Node(11)
root.left.left.right = Node(5)
root.right.right.left = Node(10)
root.left.left.right.right = Node(6)

# Creating a Solution object
solution = Solution()

# Get the Bottom View traversal and queue states
bottom_view, bottom_view_map, queue_states = solution.bottomView(root)

# Print the result in the command line
print("Bottom View Traversal:", bottom_view)

# Animate the traversal with queue visualization
animate_bottom_view_with_queue(bottom_view_map, queue_states, root)
