import matplotlib.pyplot as plt
import networkx as nx


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


def inorder_traversal(root, graph, pos, speed):
    result = []
    direction = []

    def traverse(node):
        if node:
            traverse(node.left)
            result.append(node.val)
            direction.append(node.val)  # Capture direction
            highlight_node(graph, pos, node.val, speed)
            change_visited_nodes_color(graph, pos, result, speed)
            traverse(node.right)

    traverse(root)
    print(f"Inorder Traversal: {result}")
    return result


def highlight_node(graph, pos, node_val, speed):
    colors = ["lightblue" if node != node_val else "yellow" for node in graph.nodes]
    plt.clf()
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=900,
        font_size=18,
        font_weight="bold",
        edge_color="gray",
    )
    plt.pause(speed)


def change_visited_nodes_color(graph, pos, visited_nodes, speed):
    colors = [
        "lightgreen" if node in visited_nodes else "lightblue" for node in graph.nodes
    ]
    plt.clf()
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=900,
        font_size=18,
        font_weight="bold",
        edge_color="gray",
    )
    for i in range(len(visited_nodes) - 1):
        plt.arrow(
            pos[visited_nodes[i]][0],
            pos[visited_nodes[i]][1],
            pos[visited_nodes[i + 1]][0] - pos[visited_nodes[i]][0],
            pos[visited_nodes[i + 1]][1] - pos[visited_nodes[i]][1],
            shape="full",
            lw=0,
            length_includes_head=True,
            head_width=0.05,
            color="orange",
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

inorder_traversal(root, graph, pos, 1.5)  # Slower speed for better visualization
plt.ioff()
plt.show()
