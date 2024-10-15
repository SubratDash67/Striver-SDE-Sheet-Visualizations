import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


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


def recursionLeft(root, level, res, visited_nodes):
    if not root:
        return
    if len(res) == level:
        res.append(root.data)
        visited_nodes.append(root.data)
    recursionLeft(root.left, level + 1, res, visited_nodes)
    recursionLeft(root.right, level + 1, res, visited_nodes)


def recursionRight(root, level, res, visited_nodes):
    if not root:
        return
    if len(res) == level:
        res.append(root.data)
        visited_nodes.append(root.data)
    recursionRight(root.right, level + 1, res, visited_nodes)
    recursionRight(root.left, level + 1, res, visited_nodes)


def animate_trees(left_view_nodes, right_view_nodes):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
    tree_left = nx.DiGraph()
    tree_right = nx.DiGraph()
    add_edges(tree_left, root_left, pos={})
    add_edges(tree_right, root_right, pos={})

    pos_left = nx.get_node_attributes(tree_left, "pos")
    pos_right = nx.get_node_attributes(tree_right, "pos")

    nx.draw(
        tree_left,
        pos_left,
        ax=ax1,
        with_labels=True,
        node_color="lightblue",
        node_size=600,
        font_size=12,
    )
    nx.draw(
        tree_right,
        pos_right,
        ax=ax2,
        with_labels=True,
        node_color="lightblue",
        node_size=600,
        font_size=12,
    )

    ax1.set_title("Left View Traversal", fontsize=16, fontweight="bold")
    ax2.set_title("Right View Traversal", fontsize=16, fontweight="bold")

    visited_left = []
    visited_right = []

    def update(frame):
        ax1.clear()
        ax2.clear()

        nx.draw(
            tree_left,
            pos_left,
            ax=ax1,
            with_labels=True,
            node_color="lightblue",
            node_size=600,
            font_size=12,
        )
        nx.draw(
            tree_right,
            pos_right,
            ax=ax2,
            with_labels=True,
            node_color="lightblue",
            node_size=600,
            font_size=12,
        )

        if frame < len(left_view_nodes):
            visited_left.append(left_view_nodes[frame])
        if frame < len(right_view_nodes):
            visited_right.append(right_view_nodes[frame])

        nx.draw_networkx_nodes(
            tree_left,
            pos_left,
            nodelist=visited_left,
            node_color="orange",
            node_size=800,
            ax=ax1,
        )
        nx.draw_networkx_nodes(
            tree_right,
            pos_right,
            nodelist=visited_right,
            node_color="orange",
            node_size=800,
            ax=ax2,
        )

        for node in visited_left:
            ax1.text(
                pos_left[node][0],
                pos_left[node][1] + 0.1,
                f"{node}",
                fontsize=12,
                ha="center",
                color="darkred",
                fontweight="bold",
            )
        for node in visited_right:
            ax2.text(
                pos_right[node][0],
                pos_right[node][1] + 0.1,
                f"{node}",
                fontsize=12,
                ha="center",
                color="darkred",
                fontweight="bold",
            )

    ani = FuncAnimation(
        fig,
        update,
        frames=max(len(left_view_nodes), len(right_view_nodes)),
        interval=1500,
        repeat=False,
    )
    plt.tight_layout()
    plt.show()


root_left = Node(1)
root_left.left = Node(2)
root_left.left.left = Node(4)
root_left.left.right = Node(10)
root_left.left.left.right = Node(5)
root_left.left.left.right.right = Node(6)
root_left.right = Node(3)
root_left.right.left = Node(9)

root_right = Node(1)
root_right.left = Node(2)
root_right.right = Node(3)
root_right.right.right = Node(10)
root_right.left.left = Node(4)
root_right.left.left.right = Node(5)

left_view_nodes = []
right_view_nodes = []
recursionLeft(root_left, 0, [], left_view_nodes)
recursionRight(root_right, 0, [], right_view_nodes)

print("Left View Traversal:", left_view_nodes)
print("Right View Traversal:", right_view_nodes)

animate_trees(left_view_nodes, right_view_nodes)
