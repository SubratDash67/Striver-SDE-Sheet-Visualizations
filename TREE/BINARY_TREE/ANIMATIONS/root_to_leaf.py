import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.animation import FuncAnimation


# Node structure for the binary tree
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# Function to build a binary tree from a list (level-order input)
def buildTree(values):
    if not values or values[0] == -1:
        return None

    root = Node(values[0])
    queue = deque([root])
    index = 1

    while queue and index < len(values):
        current = queue.popleft()

        # Process left child
        if values[index] != -1:
            current.left = Node(values[index])
            queue.append(current.left)
        index += 1

        if index >= len(values):
            break

        # Process right child
        if values[index] != -1:
            current.right = Node(values[index])
            queue.append(current.right)
        index += 1

    return root


class Solution:
    def __init__(self):
        self.path_states = []  # Store traversal states for animation

    def getPath(self, root, path, target):
        if not root:
            return False

        # Add current node to the path
        path.append(root.val)
        self.path_states.append(list(path))  # Save current state for animation

        # If we find the target node, return True
        if root.val == target:
            return True

        # Recursively search left and right children
        if self.getPath(root.left, path, target) or self.getPath(
            root.right, path, target
        ):
            return True

        # Backtrack if target not found in this path
        path.pop()
        self.path_states.append(list(path))  # Save backtrack state
        return False

    def solve(self, root, target):
        path = []
        if not root:
            return path
        self.getPath(root, path, target)
        return path


# Function to add edges to the tree graph for visualization
def add_edges(graph, root, pos, x=0, y=0, layer=1):
    if root is None:
        return
    graph.add_node(root.val, pos=(x, y))
    if root.left:
        graph.add_edge(root.val, root.left.val)
        add_edges(graph, root.left, pos, x - 1 / layer, y - 1, layer + 1)
    if root.right:
        graph.add_edge(root.val, root.right.val)
        add_edges(graph, root.right, pos, x + 1 / layer, y - 1, layer + 1)


# Function to animate the root-to-node path traversal
def animate_path_traversal(path_states, tree_root):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the tree graph
    tree = nx.DiGraph()
    add_edges(tree, tree_root, pos={})
    pos = nx.get_node_attributes(tree, "pos")

    # Update function for the animation
    def update(frame):
        ax.clear()

        # Get the current path state
        current_path = path_states[frame]

        # Highlight nodes that are part of the current path
        node_colors = ["lightblue"] * len(tree.nodes)
        for node in current_path:
            node_colors[list(tree.nodes).index(node)] = "orange"

        # Draw the tree with the highlighted path
        nx.draw(
            tree,
            pos,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
        )
        ax.set_title(f"Current Path: {' -> '.join(map(str, current_path))}")

    # Create the animation
    ani = FuncAnimation(
        fig, update, frames=len(path_states), interval=1000, repeat=False
    )
    plt.show()


# Main function to run the animation
if __name__ == "__main__":
    # Input: Binary tree in level order
    values = [1, 2, 3, 4, -1, 9, 11, -1, 5, -1, -1, 10, -1, -1, 6]

    # Build the binary tree
    root = buildTree(values)

    # Target node value to find the path
    target_leaf_value = 6

    # Solve and get the path
    solution = Solution()
    path = solution.solve(root, target_leaf_value)

    # Print the final path
    print(
        f"Path from root to node with value {target_leaf_value}: {' -> '.join(map(str, path))}"
    )

    # Animate the path traversal
    animate_path_traversal(solution.path_states, root)
