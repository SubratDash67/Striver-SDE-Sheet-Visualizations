import matplotlib.pyplot as plt
import networkx as nx
import collections
import time


# Node structure for the binary tree
class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


# Solution class with boundary traversal and animation enhancements
class Solution:
    def isLeaf(self, root):
        return not root.left and not root.right

    def addLeftBoundary(self, root, res, G, pos, queue_ax, node_colors, ax):
        curr = root.left
        while curr:
            if not self.isLeaf(curr):
                res.append(curr.data)
                self.update_visual(
                    res, G, pos, queue_ax, node_colors, ax, curr.data, "blue"
                )
            curr = curr.left if curr.left else curr.right

    def addRightBoundary(self, root, res, G, pos, queue_ax, node_colors, ax):
        curr = root.right
        temp = []
        while curr:
            if not self.isLeaf(curr):
                temp.append(curr.data)
            curr = curr.right if curr.right else curr.left
        for data in reversed(temp):
            res.append(data)
            self.update_visual(res, G, pos, queue_ax, node_colors, ax, data, "red")

    def addLeaves(self, root, res, G, pos, queue_ax, node_colors, ax):
        if self.isLeaf(root):
            res.append(root.data)
            self.update_visual(
                res, G, pos, queue_ax, node_colors, ax, root.data, "yellow"
            )
        else:
            if root.left:
                self.addLeaves(root.left, res, G, pos, queue_ax, node_colors, ax)
            if root.right:
                self.addLeaves(root.right, res, G, pos, queue_ax, node_colors, ax)

    def printBoundary(self, root, G, pos, queue_ax, node_colors, ax):
        res = []
        if not self.isLeaf(root):
            res.append(root.data)
            self.update_visual(
                res, G, pos, queue_ax, node_colors, ax, root.data, "green"
            )
        self.addLeftBoundary(root, res, G, pos, queue_ax, node_colors, ax)
        self.addLeaves(root, res, G, pos, queue_ax, node_colors, ax)
        self.addRightBoundary(root, res, G, pos, queue_ax, node_colors, ax)
        return res

    def update_visual(
        self, queue, G, pos, queue_ax, node_colors, ax, current_node, color
    ):
        node_index = list(G.nodes()).index(current_node)
        node_colors[node_index] = color
        queue_ax.cla()
        queue_ax.text(
            0.5, 0.5, f"Queue: {' -> '.join(map(str, queue))}", fontsize=12, ha="center"
        )
        queue_ax.axis("off")

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
            edge_color=[
                "purple" if edge[0] == current_node else "black" for edge in G.edges()
            ],
            width=[2 if edge[0] == current_node else 1 for edge in G.edges()],
        )

        plt.pause(2)


def add_edges(G, node):
    if node.left:
        G.add_edge(node.data, node.left.data)
        add_edges(G, node.left)
    if node.right:
        G.add_edge(node.data, node.right.data)
        add_edges(G, node.right)


def hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def _hierarchy_pos(
    G,
    root,
    width=1.0,
    vert_gap=0.2,
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


def main():
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

    fig, ax = plt.subplots(figsize=(10, 8))
    queue_ax = fig.add_axes([0.1, 0.01, 0.8, 0.05])
    node_colors = ["lightgreen"] * len(G.nodes())

    solution = Solution()
    plt.ion()
    result = solution.printBoundary(root, G, pos, queue_ax, node_colors, ax)
    print(f"Boundary Traversal: {result}")
    plt.ioff()
    plt.show()


main()
