import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.animation import FuncAnimation


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def buildTree(values):
    if not values or values[0] == -1:
        return None

    root = Node(values[0])
    queue = deque([root])
    index = 1

    while queue and index < len(values):
        current = queue.popleft()

        if values[index] != -1:
            current.left = Node(values[index])
            queue.append(current.left)
        index += 1

        if index >= len(values):
            break

        if values[index] != -1:
            current.right = Node(values[index])
            queue.append(current.right)
        index += 1

    return root


class Solution:
    def __init__(self):
        self.path_states = []

    def getPath(self, root, path, target):
        if not root:
            return False

        path.append(root.val)
        self.path_states.append(list(path))

        if root.val == target:
            return True

        if self.getPath(root.left, path, target) or self.getPath(
            root.right, path, target
        ):
            return True

        path.pop()
        self.path_states.append(list(path))
        return False

    def solve(self, root, target):
        path = []
        if not root:
            return path
        self.getPath(root, path, target)
        return path


def add_edges(graph, root, pos, x=0, y=0, layer=1):
    if root is None:
        return
    graph.add_node(root.val, pos=(x, y))
    if root.left:
        graph.add_edge(root.val, root.left.val)
        add_edges(graph, root.left, pos, x - 1 / layer, y - 1, layer + 1)
    if root.right:
        graph.add_edge(root.val, root.right.val)
        add_edges(graph, root.right, pos, x + 1 / layer, y - 1, layer + 1)


def animate_path_traversal(path_states, tree_root):
    fig, ax = plt.subplots(figsize=(10, 6))

    tree = nx.DiGraph()
    add_edges(tree, tree_root, pos={})
    pos = nx.get_node_attributes(tree, "pos")

    def update(frame):
        ax.clear()
        current_path = path_states[frame]
        node_colors = ["lightblue"] * len(tree.nodes)

        for i, node in enumerate(current_path):
            node_colors[list(tree.nodes).index(node)] = (
                "orange" if i < len(current_path) - 1 else "yellow"
            )

        for node in path_states[frame]:
            if node == current_path[-1]:
                node_colors[list(tree.nodes).index(node)] = "green"

        nx.draw(
            tree,
            pos,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            arrows=True,
            arrowstyle="->",
            arrowsize=20,
        )
        ax.set_title(f"Current Path: {' -> '.join(map(str, current_path))}")

    ani = FuncAnimation(
        fig, update, frames=len(path_states), interval=1500, repeat=False
    )
    plt.show()


if __name__ == "__main__":
    values = [1, 2, 3, 4, -1, 9, 11, -1, 5, -1, -1, 10, -1, -1, 6]
    root = buildTree(values)
    target_leaf_value = 6
    solution = Solution()
    path = solution.solve(root, target_leaf_value)

    print(
        f"Path from root to node with value {target_leaf_value}: {' -> '.join(map(str, path))}"
    )

    animate_path_traversal(solution.path_states, root)
