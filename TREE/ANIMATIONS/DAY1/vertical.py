import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque
from matplotlib.animation import FuncAnimation


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def findVertical(self, root):
        nodes = defaultdict(lambda: defaultdict(set))
        todo = deque([(root, (0, 0))])
        traversal_states = []

        while todo:
            temp, (x, y) = todo.popleft()
            nodes[x][y].add(temp.data)
            traversal_states.append((x, y, temp.data, dict(nodes)))
            if temp.left:
                todo.append((temp.left, (x - 1, y + 1)))
            if temp.right:
                todo.append((temp.right, (x + 1, y + 1)))

        ans = []
        for x in sorted(nodes):
            col = []
            for y in sorted(nodes[x]):
                col.extend(sorted(nodes[x][y]))
            ans.append(col)

        return ans, traversal_states


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


def animate_vertical_order(traversal_states, tree_root):
    fig, (ax_tree, ax_result) = plt.subplots(2, 1, figsize=(10, 12))
    tree = nx.DiGraph()
    add_edges(tree, tree_root, pos={})
    pos = nx.get_node_attributes(tree, "pos")

    def update(frame):
        ax_tree.clear()
        ax_result.clear()
        x, y, node_value, nodes_map = traversal_states[frame]
        node_colors = ["lightblue"] * len(tree.nodes)
        node_colors[list(tree.nodes).index(node_value)] = "orange"
        nx.draw(
            tree,
            pos,
            ax=ax_tree,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
        )
        ax_tree.set_title(f"Processing Node {node_value} at (x={x}, y={y})")

        ax_result.set_title("Vertical Order Traversal")
        columns = sorted(nodes_map.items())
        for i, (x, y_vals) in enumerate(columns):
            col_values = []
            for y in sorted(y_vals):
                col_values.extend(sorted(y_vals[y]))
            ax_result.text(i * 0.1, 0.5, f"{col_values}", fontsize=12, ha="center")
        ax_result.axis("off")

    ani = FuncAnimation(
        fig, update, frames=len(traversal_states), interval=1500, repeat=False
    )
    plt.show()


if __name__ == "__main__":
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.right.left = Node(9)
    root.right.right = Node(11)
    root.left.left.right = Node(5)
    root.right.right.left = Node(10)
    root.left.left.right.right = Node(6)
    solution = Solution()
    verticalTraversal, traversal_states = solution.findVertical(root)

    print("Vertical Traversal:")
    for col in verticalTraversal:
        print(col)

    animate_vertical_order(traversal_states, root)
