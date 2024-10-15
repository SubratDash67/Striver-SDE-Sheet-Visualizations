import matplotlib.pyplot as plt
import networkx as nx
import collections
import time


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def isIdentical(self, node1, node2):
        if node1 is None and node2 is None:
            return True
        if node1 is None or node2 is None:
            return False
        return (
            node1.data == node2.data
            and self.isIdentical(node1.left, node2.left)
            and self.isIdentical(node1.right, node2.right)
        )


def add_edges(G, node):
    if node.left:
        G.add_edge(node.data, node.left.data)
        add_edges(G, node.left)
    if node.right:
        G.add_edge(node.data, node.right.data)
        add_edges(G, node.right)


def plot_identical_trees_animation(root1, root2):
    G1 = nx.DiGraph()
    G2 = nx.DiGraph()
    add_edges(G1, root1)
    add_edges(G2, root2)

    pos1 = hierarchy_pos(G1, root1.data)
    pos2 = hierarchy_pos(G2, root2.data)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
    node_colors1 = ["lightblue"] * len(G1.nodes())
    node_colors2 = ["lightblue"] * len(G2.nodes())

    queue = collections.deque([(root1, root2)])

    while queue:
        current_node1, current_node2 = queue.popleft()
        if current_node1 and current_node2:
            idx1 = list(G1.nodes()).index(current_node1.data)
            idx2 = list(G2.nodes()).index(current_node2.data)
            node_colors1[idx1] = "orange"
            node_colors2[idx2] = "orange"

        ax1.cla()
        ax2.cla()

        draw_tree(G1, pos1, node_colors1, ax1, "Tree 1")
        draw_tree(G2, pos2, node_colors2, ax2, "Tree 2")

        plt.pause(1.0)  # Slightly slower animation

        if current_node1 and current_node2 and current_node1.data == current_node2.data:
            if current_node1.left or current_node2.left:
                queue.append((current_node1.left, current_node2.left))
            if current_node1.right or current_node2.right:
                queue.append((current_node1.right, current_node2.right))

        node_colors1[idx1] = "lightblue"
        node_colors2[idx2] = "lightblue"

    identical_message(
        root1, root2, node_colors1, node_colors2, G1, G2, pos1, pos2, ax1, ax2, fig
    )


def identical_message(
    root1, root2, node_colors1, node_colors2, G1, G2, pos1, pos2, ax1, ax2, fig
):
    solution = Solution()
    identical = solution.isIdentical(root1, root2)

    # Set final node colors
    final_color = "green" if identical else "red"
    node_colors1 = [final_color] * len(G1.nodes())
    node_colors2 = [final_color] * len(G2.nodes())

    ax1.cla()
    ax2.cla()

    draw_tree(G1, pos1, node_colors1, ax1, "Tree 1 - Final")
    draw_tree(G2, pos2, node_colors2, ax2, "Tree 2 - Final")

    title = "Trees are IDENTICAL" if identical else "Trees are NOT IDENTICAL"
    fig.suptitle(title, fontsize=20, color=final_color, fontweight="bold")

    plt.pause(3)  # Pause to display the result
    plt.show()


def draw_tree(G, pos, node_colors, ax, title):
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1200,
        node_color=node_colors,
        font_size=12,
        font_color="black",
        font_weight="bold",
        arrows=False,
        ax=ax,
    )
    ax.set_title(title, fontsize=16)


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
    root1 = Node(1)
    root1.left = Node(2)
    root1.right = Node(3)
    root1.left.left = Node(4)

    root2 = Node(1)
    root2.left = Node(2)
    root2.right = Node(3)
    root2.left.left = Node(4)

    solution = Solution()
    identical = solution.isIdentical(root1, root2)
    print(
        "The binary trees are identical."
        if identical
        else "The binary trees are not identical."
    )

    plt.ion()
    plot_identical_trees_animation(root1, root2)
    plt.ioff()


main()
