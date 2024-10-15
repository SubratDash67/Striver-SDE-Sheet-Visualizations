import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.patches import Patch


# Node class for the binary tree
class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def ZigZagLevelOrder(self, root, G, pos, traversal_ax, queue_ax, node_colors, ax):
        result = []
        if not root:
            return result

        nodesQueue = deque([root])
        leftToRight = True

        # Continue until the queue is empty
        while nodesQueue:
            size = len(nodesQueue)
            row = [0] * size

            # Traverse the current level
            for i in range(size):
                node = nodesQueue.popleft()
                index = i if leftToRight else (size - 1 - i)
                row[index] = node.data

                if node.left:
                    nodesQueue.append(node.left)
                if node.right:
                    nodesQueue.append(node.right)

                # Update the visualization
                self.update_visual(
                    G,
                    pos,
                    traversal_ax,
                    queue_ax,
                    node_colors,
                    ax,
                    node.data,
                    nodesQueue,
                    result + [row],
                    leftToRight,
                )

            leftToRight = not leftToRight
            result.append(row)

        return result

    def update_visual(
        self,
        G,
        pos,
        traversal_ax,
        queue_ax,
        node_colors,
        ax,
        current_node,
        nodesQueue,
        traversal,
        leftToRight,
    ):
        # Update the queue display
        queue_ax.cla()
        queue_text = "Queue: " + " -> ".join([str(node.data) for node in nodesQueue])
        queue_ax.text(0.5, 0.5, queue_text, fontsize=10, ha="center", va="center")
        queue_ax.axis("off")

        # Update the traversal direction and progress display
        traversal_ax.cla()
        direction = "Left to Right" if leftToRight else "Right to Left"
        traversal_text = f"Traversal Direction: {direction}\n" + "\n".join(
            [str(level) for level in traversal]
        )
        traversal_ax.text(
            0.5, 0.5, traversal_text, fontsize=10, ha="center", va="center"
        )
        traversal_ax.axis("off")

        # Update node color in the tree
        node_colors[list(G.nodes()).index(current_node)] = "orange"

        # Redraw the tree
        ax.cla()
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=1000,
            node_color=node_colors,
            font_size=10,
            font_color="black",
            font_weight="bold",
            arrows=False,
            ax=ax,
        )

        # Add a legend for node color meanings
        legend_elements = [
            Patch(facecolor="lightgreen", edgecolor="black", label="Not Visited"),
            Patch(facecolor="orange", edgecolor="black", label="Current Node"),
        ]
        ax.legend(handles=legend_elements, loc="upper left")

        plt.pause(1.5)  # Pause for animation effect


# Helper to add edges to the graph for visualization
def add_edges(G, node):
    if node.left:
        G.add_edge(node.data, node.left.data)
        add_edges(G, node.left)
    if node.right:
        G.add_edge(node.data, node.right.data)
        add_edges(G, node.right)


# Helper function to compute tree hierarchy position for visualization
def hierarchy_pos(G, root, width=1.5, vert_gap=0.5, vert_loc=0, xcenter=0.5):
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def _hierarchy_pos(
    G,
    root,
    width=1.5,  # Increased width for more horizontal space
    vert_gap=0.5,  # Increased vertical gap
    vert_loc=0,
    xcenter=0.5,
    pos=None,
    parent=None,
    parsed=None,
):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    if parsed is None:
        parsed = {root}
    else:
        parsed.add(root)
    neighbors = list(G.neighbors(root))
    if not neighbors:
        return pos
    dx = width / len(neighbors)
    nextx = xcenter - width / 2 - dx / 2
    for neighbor in neighbors:
        nextx += dx
        if neighbor not in parsed:
            pos = _hierarchy_pos(
                G,
                neighbor,
                width=dx,
                vert_gap=vert_gap,
                vert_loc=vert_loc - vert_gap,
                xcenter=nextx,
                pos=pos,
                parent=root,
                parsed=parsed,
            )
    return pos


# Main function
def main():
    # Create a sample binary tree
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)

    G = nx.DiGraph()
    add_edges(G, root)
    pos = hierarchy_pos(G, root.data)

    # Set up a figure with subplots for the tree and the info panels
    fig = plt.figure(figsize=(12, 6))

    # Tree subplot occupies the left half
    ax = fig.add_axes([0.05, 0.1, 0.5, 0.8])  # Left half for the tree animation

    # Traversal direction and queue will be stacked on the right half
    traversal_ax = fig.add_axes([0.6, 0.6, 0.35, 0.3])  # Top-right for traversal
    queue_ax = fig.add_axes([0.6, 0.2, 0.35, 0.3])  # Bottom-right for queue

    node_colors = ["lightgreen"] * len(G.nodes())  # Initial colors of the nodes

    solution = Solution()
    plt.ion()  # Enable interactive mode
    result = solution.ZigZagLevelOrder(
        root, G, pos, traversal_ax, queue_ax, node_colors, ax
    )  # Perform Zigzag Traversal
    print(f"Zigzag Traversal: {result}")  # Print final zigzag traversal
    plt.ioff()  # Disable interactive mode
    plt.show()  # Show the plot


main()
