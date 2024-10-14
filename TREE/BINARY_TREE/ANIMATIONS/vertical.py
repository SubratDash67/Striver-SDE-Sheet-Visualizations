import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque
from matplotlib.animation import FuncAnimation


# Node structure for the binary tree
class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    # Function to perform vertical order traversal
    # and return traversal states for animation
    def findVertical(self, root):
        nodes = defaultdict(
            lambda: defaultdict(set)
        )  # Map for nodes based on vertical & level
        todo = deque([(root, (0, 0))])  # Queue for BFS traversal with (node, (x, y))
        traversal_states = []  # Store states for animation

        while todo:
            temp, (x, y) = (
                todo.popleft()
            )  # Dequeue the current node and its coordinates
            nodes[x][y].add(temp.data)  # Add the node to the map

            # Save the current state for animation
            traversal_states.append((x, y, temp.data, dict(nodes)))

            # Process left and right children
            if temp.left:
                todo.append((temp.left, (x - 1, y + 1)))  # Left child: x-1, y+1
            if temp.right:
                todo.append((temp.right, (x + 1, y + 1)))  # Right child: x+1, y+1

        # Prepare the final result in a 2D list from the map
        ans = []
        for x in sorted(nodes):
            col = []
            for y in sorted(nodes[x]):
                col.extend(sorted(nodes[x][y]))  # Add sorted values to the column
            ans.append(col)

        return ans, traversal_states  # Return result and states for animation


# Function to add edges to the graph for visualization
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


# Function to animate the vertical order traversal
def animate_vertical_order(traversal_states, tree_root):
    fig, (ax_tree, ax_result) = plt.subplots(2, 1, figsize=(10, 12))

    # Create the tree graph
    tree = nx.DiGraph()
    add_edges(tree, tree_root, pos={})
    pos = nx.get_node_attributes(tree, "pos")

    # Function to update the animation frame-by-frame
    def update(frame):
        ax_tree.clear()
        ax_result.clear()

        # Unpack the current state
        x, y, node_value, nodes_map = traversal_states[frame]

        # Draw the tree with the current node highlighted
        node_colors = ["lightblue"] * len(tree.nodes)
        node_colors[list(tree.nodes).index(node_value)] = (
            "orange"  # Highlight the current node
        )

        nx.draw(
            tree,
            pos,
            ax=ax_tree,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
        )
        ax_tree.set_title(f"Processing Node {node_value} at (x={x}, y={y})")

        # Draw the vertical order columns being built
        ax_result.set_title("Vertical Order Traversal")
        columns = sorted(nodes_map.items())  # Sort by vertical coordinate (x)
        for i, (x, y_vals) in enumerate(columns):
            col_values = []
            for y in sorted(y_vals):
                col_values.extend(sorted(y_vals[y]))  # Collect values in sorted order
            ax_result.text(i * 0.1, 0.5, f"{col_values}", fontsize=12, ha="center")

        ax_result.axis("off")

    # Create the animation
    ani = FuncAnimation(
        fig, update, frames=len(traversal_states), interval=1000, repeat=False
    )
    plt.show()


# Main function to run the animation
if __name__ == "__main__":
    # Create a sample binary tree
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.right.left = Node(9)
    root.right.right = Node(11)
    root.left.left.right = Node(5)
    root.right.right.left = Node(10)
    root.left.left.right.right = Node(6)
    solution = Solution()

    # Get the vertical traversal result and states for animation
    verticalTraversal, traversal_states = solution.findVertical(root)

    # Print the final vertical order traversal result
    print("Vertical Traversal:")
    for col in verticalTraversal:
        print(col)

    # Animate the vertical order traversal process
    animate_vertical_order(traversal_states, root)
