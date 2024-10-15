import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from matplotlib.patches import Patch
import time


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.G = nx.DiGraph()
        self.pos = {}
        self.node_labels = {}
        self.node_colors = []
        self.anim_queue = []
        self.weights = {}
        self.node_sizes = []
        self.edge_colors = []

    def add_to_graph(self, root, pos=(0, 0), level=0, x_offset=1.5):
        if root is None:
            return
        self.G.add_node(root.data, pos=pos)
        self.pos[root.data] = pos
        self.node_labels[root.data] = str(root.data)
        self.node_colors.append("lightblue")
        self.node_sizes.append(1000)

        # Add children to the graph
        if root.left:
            self.G.add_edge(root.data, root.left.data)
            self.add_to_graph(
                root.left,
                (pos[0] - x_offset / (level + 1), pos[1] - 1),
                level + 1,
                x_offset,
            )
        if root.right:
            self.G.add_edge(root.data, root.right.data)
            self.add_to_graph(
                root.right,
                (pos[0] + x_offset / (level + 1), pos[1] - 1),
                level + 1,
                x_offset,
            )
        self.edge_colors = ["black"] * len(self.G.edges)

    def isBalanced(self, root):
        is_balanced = self.dfsHeight(root)
        self.anim_queue.append(
            ("Result", "Balanced" if is_balanced != -1 else "Not Balanced")
        )
        return is_balanced != -1

    def dfsHeight(self, root):
        if not root:
            return 0

        self.anim_queue.append(("Traverse", root.data))
        left_height = self.dfsHeight(root.left)
        right_height = self.dfsHeight(root.right)

        balance_factor = left_height - right_height
        self.weights[root.data] = balance_factor

        if left_height == -1 or right_height == -1 or abs(balance_factor) > 1:
            self.anim_queue.append(("Balance", root.data, balance_factor, False))
            return -1

        self.anim_queue.append(("Balance", root.data, balance_factor, True))
        return max(left_height, right_height) + 1

    def update(self, frame):
        event_type = self.anim_queue[frame][0]

        if event_type == "Traverse":
            node = self.anim_queue[frame][1]
            idx = list(self.node_labels.keys()).index(node)
            self.node_colors[idx] = "yellow"
            self.node_sizes[idx] = 1500
            self.highlight_edges(node)

        elif event_type == "Balance":
            node, balance_factor, balanced = self.anim_queue[frame][1:]
            idx = list(self.node_labels.keys()).index(node)
            self.node_colors[idx] = "green" if balanced else "red"
            self.node_labels[node] = f"{node} ({balance_factor})"
            self.node_sizes[idx] = 1200 if balanced else 1800

        elif event_type == "Result":
            result = self.anim_queue[frame][1]
            self.ax.set_title(
                f"Tree is {result}",
                fontsize=20,
                color="blue" if result == "Balanced" else "red",
            )

        self.ax.clear()
        nx.draw(
            self.G,
            pos=self.pos,
            with_labels=True,
            labels=self.node_labels,
            node_color=self.node_colors,
            node_size=self.node_sizes,
            edge_color=self.edge_colors,
            ax=self.ax,
            font_size=12,
            font_color="white",
            width=2,
        )

        legend_elements = [
            Patch(facecolor="lightblue", edgecolor="black", label="Not Visited"),
            Patch(facecolor="yellow", edgecolor="black", label="Current Node"),
            Patch(facecolor="green", edgecolor="black", label="Balanced"),
            Patch(facecolor="red", edgecolor="black", label="Unbalanced"),
        ]
        self.ax.legend(handles=legend_elements, loc="upper left")

    def highlight_edges(self, node):
        for i, (u, v) in enumerate(self.G.edges):
            self.edge_colors[i] = "purple" if u == node else "black"

    def animate(self):
        ani = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=len(self.anim_queue),
            interval=1500,
            repeat=False,
        )
        plt.show()


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.left.right.right = Node(6)
root.left.right.right.right = Node(7)

solution = Solution()
solution.add_to_graph(root)

solution.isBalanced(root)

solution.animate()
