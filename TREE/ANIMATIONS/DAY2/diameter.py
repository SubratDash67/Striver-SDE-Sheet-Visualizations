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
    def diameterOfBinaryTree(self, root):
        diameter = [0]
        self.height(root, diameter)
        return diameter[0]

    def height(self, node, diameter):
        if not node:
            return 0
        lh = self.height(node.left, diameter)
        rh = self.height(node.right, diameter)
        diameter[0] = max(diameter[0], lh + rh)
        return 1 + max(lh, rh)


def add_edges(G, node):
    if node.left:
        G.add_edge(node.data, node.left.data)
        add_edges(G, node.left)
    if node.right:
        G.add_edge(node.data, node.right.data)
        add_edges(G, node.right)


def plot_diameter_animation(root, diameter):
    G = nx.DiGraph()
    add_edges(G, root)
    pos = hierarchy_pos(G, root.data)

    queue = collections.deque([(root, 0, 0)])
    node_colors = ["lightblue"] * len(G.nodes())

    fig, (ax_tree, ax_info) = plt.subplots(
        2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [5, 1]}
    )

    current_diameter = diameter[0]

    while queue:
        current_node, lh, rh = queue.popleft()
        node_idx = list(G.nodes()).index(current_node.data)

        # Color change with smooth transition
        for _ in range(10):
            color = (1, 0.6 - 0.06 * _, 0.6 - 0.06 * _)  # Gradient red to pink
            node_colors[node_idx] = color
            redraw_tree(ax_tree, G, pos, node_colors, current_node.data)
            plt.pause(0.05)

        ax_info.cla()
        ax_info.text(
            0.25,
            0.5,
            f"Diameter: {current_diameter}",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=14,
            transform=ax_info.transAxes,
        )
        ax_info.text(
            0.75,
            0.5,
            f"Left Height: {lh} | Right Height: {rh}",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=14,
            transform=ax_info.transAxes,
        )
        ax_info.set_xticks([]), ax_info.set_yticks([])
        ax_info.set_title("Diameter and Heights")

        time.sleep(1)  # Slow down the animation

        if current_node.left:
            left_height = Solution().height(current_node.left, [current_diameter])
            queue.append((current_node.left, left_height, rh))
        if current_node.right:
            right_height = Solution().height(current_node.right, [current_diameter])
            queue.append((current_node.right, lh, right_height))

        current_diameter = max(current_diameter, lh + rh)

        # Reset node color
        node_colors[node_idx] = "lightblue"

    plt.show()


def redraw_tree(ax, G, pos, node_colors, current_node):
    ax.cla()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1000,
        node_color=node_colors,
        font_size=12,
        font_color="black",
        font_weight="bold",
        arrows=False,
        ax=ax,
        edge_color=[
            "red" if edge[0] == current_node else "black" for edge in G.edges()
        ],
        width=[2 if edge[0] == current_node else 1 for edge in G.edges()],
    )
    ax.set_title(f"Current Node: {current_node}")


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
    root.left.right.right = Node(6)
    root.left.right.right.right = Node(7)

    solution = Solution()
    diameter = solution.diameterOfBinaryTree(root)
    print("The diameter of the binary tree is:", diameter)

    plt.ion()
    plot_diameter_animation(root, [diameter])
    plt.ioff()


main()
