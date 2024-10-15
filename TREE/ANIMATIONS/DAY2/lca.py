import matplotlib.pyplot as plt
import networkx as nx
import collections


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left if left else right


def add_edges(G, node):
    if node.left:
        G.add_edge(node.data, node.left.data)
        add_edges(G, node.left)
    if node.right:
        G.add_edge(node.data, node.right.data)
        add_edges(G, node.right)


def plot_lca_animation(root, p, q):
    G = nx.DiGraph()
    add_edges(G, root)
    pos = hierarchy_pos(G, root.data)

    fig, ax = plt.subplots(figsize=(10, 10))
    node_colors = ["lightgreen"] * len(G.nodes())
    queue = collections.deque([root])

    solution = Solution()
    lca = solution.lowestCommonAncestor(root, p, q)

    while queue:
        current_node = queue.popleft()
        idx = list(G.nodes()).index(current_node.data)
        node_colors[idx] = "red"

        ax.cla()
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
        ax.set_title(f"Current Node: {current_node.data}", fontsize=16)

        plt.pause(1)

        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)

    node_colors = ["lightgreen"] * len(G.nodes())
    node_colors[list(G.nodes()).index(p.data)] = "orange"
    node_colors[list(G.nodes()).index(q.data)] = "orange"
    node_colors[list(G.nodes()).index(lca.data)] = "cyan"

    ax.cla()
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
    ax.set_title(f"LCA of {p.data} and {q.data} is: {lca.data}", fontsize=18)
    plt.pause(3)
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
    root.right.left = Node(6)
    root.right.right = Node(7)

    p = root.left.left
    q = root.left.right

    solution = Solution()
    lca = solution.lowestCommonAncestor(root, p, q)
    print(f"The Lowest Common Ancestor of {p.data} and {q.data} is: {lca.data}")

    plt.ion()
    plot_lca_animation(root, p, q)
    plt.ioff()


main()
