import matplotlib.pyplot as plt
import networkx as nx
import collections


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


def add_edges(G, node):
    if node.left:
        G.add_edge(node.data, node.left.data)
        add_edges(G, node.left)
    if node.right:
        G.add_edge(node.data, node.right.data)
        add_edges(G, node.right)


def find_longest_path(root):
    if not root:
        return [], 0
    left_path, left_depth = find_longest_path(root.left)
    right_path, right_depth = find_longest_path(root.right)
    return (
        ([root.data] + left_path, left_depth + 1)
        if left_depth > right_depth
        else ([root.data] + right_path, right_depth + 1)
    )


def plot_tree_step_by_step(root, longest_path):
    G = nx.DiGraph()
    add_edges(G, root)
    pos = hierarchy_pos(G, root.data)
    queue = collections.deque([root])
    node_colors = ["lightgreen"] * len(G.nodes())

    fig, (ax_tree, ax_info) = plt.subplots(
        2, 1, figsize=(8, 8), gridspec_kw={"height_ratios": [5, 1]}
    )
    plt.subplots_adjust(hspace=0.3)
    current_height = 0

    while queue:
        current_height += 1
        for _ in range(len(queue)):
            current_node = queue.popleft()
            node_idx = list(G.nodes()).index(current_node.data)
            node_colors[node_idx] = "red"

            ax_tree.clear()
            ax_info.clear()

            nx.draw(
                G,
                pos,
                with_labels=True,
                node_size=800,
                node_color=node_colors,
                font_size=10,
                font_weight="bold",
                arrows=False,
                ax=ax_tree,
            )

            ax_tree.set_title(f"Exploring Node: {current_node.data}", fontsize=14)
            ax_info.text(
                0.5,
                0.5,
                f"Current Height: {current_height}",
                ha="center",
                va="center",
                fontsize=12,
                transform=ax_info.transAxes,
            )

            plt.pause(0.8)

            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

    ax_info.text(
        0.5,
        0.5,
        f"Longest Path: {longest_path}",
        ha="center",
        va="center",
        fontsize=12,
        transform=ax_info.transAxes,
    )
    plt.show()


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

    longest_path, max_depth = find_longest_path(root)
    print(f"Maximum Depth: {max_depth}")
    print(f"Longest Path: {longest_path}")

    plt.ion()
    plot_tree_step_by_step(root, longest_path)
    plt.ioff()


main()
