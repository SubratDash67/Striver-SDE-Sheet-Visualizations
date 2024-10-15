import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(nodes, index=0):
    if index < len(nodes) and nodes[index] is not None:
        node = TreeNode(nodes[index])
        node.left = build_tree(nodes, 2 * index + 1)
        node.right = build_tree(nodes, 2 * index + 2)
        return node
    return None


def level_order_traversal(root, graph, pos, speed):
    result, queue = [], deque([(root, None)])  # Store (node, parent) pairs
    path = []

    while queue:
        node, parent = queue.popleft()
        if node:
            result.append(node.val)
            path.append(node.val)
            update_graph(graph, pos, node.val, path, speed)
            queue.append((node.left, node))
            queue.append((node.right, node))

    print(f"Level Order Traversal: {result}")
    return result


def update_graph(graph, pos, node_val, path, speed):
    colors = ["lightblue" if node != node_val else "yellow" for node in graph.nodes]
    edge_colors = [
        "red" if (u in path and v in path) else "black" for u, v in graph.edges
    ]

    plt.clf()
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=colors,
        edge_color=edge_colors,
        node_size=800,
        font_size=16,
        font_weight="bold",
    )
    plt.pause(speed)


def build_graph_from_tree(root):
    graph = nx.DiGraph()
    add_edges(graph, root)
    pos = hierarchy_pos(graph, root.val)
    return graph, pos


def add_edges(graph, node):
    if node:
        if node.left:
            graph.add_edge(node.val, node.left.val)
            add_edges(graph, node.left)
        if node.right:
            graph.add_edge(node.val, node.right.val)
            add_edges(graph, node.right)


def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


def _hierarchy_pos(
    G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None
):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)

    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)

    if children:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(
                G,
                child,
                width=dx,
                vert_gap=vert_gap,
                vert_loc=vert_loc - vert_gap,
                xcenter=nextx,
                pos=pos,
                parent=root,
            )
    return pos


nodes = [1, 2, 3, 4, 5, 6, 7]
root = build_tree(nodes)
graph, pos = build_graph_from_tree(root)

plt.ion()
fig, ax = plt.subplots(figsize=(10, 8))

level_order_traversal(root, graph, pos, 1.0)
plt.ioff()
plt.show()
