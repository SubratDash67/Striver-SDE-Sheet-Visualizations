import matplotlib.pyplot as plt
import networkx as nx
from queue import Queue
from collections import deque
from matplotlib.animation import FuncAnimation


# TreeNode structure
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# Function to build the tree from level-order input
def buildTree(values):
    if not values or values[0] == -1:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    index = 1

    while queue and index < len(values):
        current = queue.popleft()

        if values[index] != -1:
            current.left = TreeNode(values[index])
            queue.append(current.left)
        index += 1

        if index >= len(values):
            break

        if values[index] != -1:
            current.right = TreeNode(values[index])
            queue.append(current.right)
        index += 1

    return root


# Solution class to calculate the maximum width
class Solution:
    def __init__(self):
        self.levels = []  # Store nodes at each level for animation

    def widthOfBinaryTree(self, root: TreeNode) -> int:
        if not root:
            return 0

        max_width = 0
        q = Queue()
        q.put((root, 0))  # (node, index)

        while not q.empty():
            size = q.qsize()
            mmin = q.queue[0][1]  # Minimum index at the current level
            first, last = None, None

            current_level = []  # Store nodes for animation

            for i in range(size):
                node, index = q.get()
                cur_id = index - mmin  # Normalize index for the level

                if i == 0:
                    first = cur_id
                if i == size - 1:
                    last = cur_id

                current_level.append(node.val)

                if node.left:
                    q.put((node.left, cur_id * 2 + 1))
                if node.right:
                    q.put((node.right, cur_id * 2 + 2))

            # Save the current level for animation
            self.levels.append(current_level)

            # Update max width
            max_width = max(max_width, last - first + 1)

        return max_width


# Function to add edges for visualization
def add_edges(graph, root, pos, x=0, y=0, layer=1):
    if not root:
        return
    graph.add_node(root.val, pos=(x, y))
    if root.left:
        graph.add_edge(root.val, root.left.val)
        add_edges(graph, root.left, pos, x - 1 / layer, y - 1, layer + 1)
    if root.right:
        graph.add_edge(root.val, root.right.val)
        add_edges(graph, root.right, pos, x + 1 / layer, y - 1, layer + 1)


# Function to animate the width calculation
def animate_width_calculation(levels, tree_root):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the tree graph
    tree = nx.DiGraph()
    add_edges(tree, tree_root, pos={})
    pos = nx.get_node_attributes(tree, "pos")

    def update(frame):
        ax.clear()
        current_level = levels[frame]

        # Color nodes at the current level
        node_colors = ["lightblue"] * len(tree.nodes)
        for node in current_level:
            node_colors[list(tree.nodes).index(node)] = "orange"

        # Draw the tree with the highlighted nodes
        nx.draw(
            tree,
            pos,
            ax=ax,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
        )
        ax.set_title(f"Processing Level {frame + 1}")

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(levels), interval=1000, repeat=False)
    plt.show()


# Main function to run the animation
def main():
    values = [1, 2, 3, 4, -1, 9, 11, -1, 5, -1, -1, 10, -1, -1, 6]

    # Build the tree
    root = buildTree(values)

    # Calculate maximum width
    solution = Solution()
    maxWidth = solution.widthOfBinaryTree(root)
    print(f"Maximum width of the binary tree is: {maxWidth}")

    # Animate the width calculation
    animate_width_calculation(solution.levels, root)


if __name__ == "__main__":
    main()
