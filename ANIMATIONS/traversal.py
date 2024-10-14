import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation


# Node class for the binary tree
class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


# Function to get Preorder, Inorder, and Postorder traversals in one pass
def pre_in_post_traversal(root):
    pre, in_order, post = [], [], []  # Lists to store traversals
    if root is None:
        return pre, in_order, post

    stack = [(root, 1)]  # Stack to track nodes and their traversal states

    # Store each state of the traversal for animation
    traversal_states = []

    while stack:
        node, state = stack.pop()

        # Preorder part
        if state == 1:
            pre.append(node.data)  # Add to Preorder
            traversal_states.append((pre[:], in_order[:], post[:], "Pre", node.data))
            state = 2
            stack.append((node, state))
            if node.left:
                stack.append((node.left, 1))

        # Inorder part
        elif state == 2:
            in_order.append(node.data)  # Add to Inorder
            traversal_states.append((pre[:], in_order[:], post[:], "In", node.data))
            state = 3
            stack.append((node, state))
            if node.right:
                stack.append((node.right, 1))

        # Postorder part
        else:
            post.append(node.data)  # Add to Postorder
            traversal_states.append((pre[:], in_order[:], post[:], "Post", node.data))

    return pre, in_order, post, traversal_states


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


# Function to animate the traversal process
def animate_traversals(traversal_states, tree_root):
    fig, (ax_tree, ax_arrays) = plt.subplots(2, 1, figsize=(10, 12))

    # Create the tree graph
    tree = nx.DiGraph()
    add_edges(tree, tree_root, pos={})
    pos = nx.get_node_attributes(tree, "pos")

    # Function to update the animation frame-by-frame
    def update(frame):
        ax_tree.clear()
        ax_arrays.clear()

        # Unpack the current state
        pre, in_order, post, traversal_type, current_node = traversal_states[frame]

        # Draw the tree with the current node highlighted
        node_colors = ["lightblue"] * len(tree.nodes)
        if traversal_type == "Pre":
            color = "blue"
        elif traversal_type == "In":
            color = "green"
        else:
            color = "red"
        node_colors[list(tree.nodes).index(current_node)] = color

        nx.draw(
            tree,
            pos,
            ax=ax_tree,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
        )
        ax_tree.set_title(
            f"{traversal_type}order Traversal: Visiting Node {current_node}"
        )

        # Draw the Preorder, Inorder, and Postorder arrays
        ax_arrays.text(0.1, 0.9, "Preorder:", fontsize=12, ha="left")
        ax_arrays.text(0.1, 0.6, "Inorder:", fontsize=12, ha="left")
        ax_arrays.text(0.1, 0.3, "Postorder:", fontsize=12, ha="left")

        ax_arrays.text(
            0.3, 0.9, " -> ".join(map(str, pre)), fontsize=12, ha="left", color="blue"
        )
        ax_arrays.text(
            0.3,
            0.6,
            " -> ".join(map(str, in_order)),
            fontsize=12,
            ha="left",
            color="green",
        )
        ax_arrays.text(
            0.3, 0.3, " -> ".join(map(str, post)), fontsize=12, ha="left", color="red"
        )

        ax_arrays.axis("off")

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
    root.left.right = Node(5)

    # Get the traversals and their states for animation
    pre, in_order, post, traversal_states = pre_in_post_traversal(root)

    # Print the traversals in the console
    print("Preorder traversal:", pre)
    print("Inorder traversal:", in_order)
    print("Postorder traversal:", post)

    # Animate the traversal process
    animate_traversals(traversal_states, root)
