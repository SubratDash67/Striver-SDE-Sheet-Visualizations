from queue import Queue


# Node class for the binary tree
class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    # Function to find the
    # maximum depth of a binary tree
    # using level order traversal
    def maxDepth(self, root):
        # If the root is NULL
        # (empty tree), depth is 0
        if root is None:
            return 0

        # Create a queue for
        # level order traversal
        q = Queue()
        level = 0

        # Push the root node into the queue
        q.put(root)

        # While there are nodes in the queue
        while not q.empty():
            # Get the number of nodes
            # at the current level
            size = q.qsize()

            # Process all nodes
            # at the current level
            for i in range(size):
                # Get the front node in the queue
                front = q.get()

                # Enqueue left child if exists
                if front.left is not None:
                    q.put(front.left)

                # Enqueue right child if exists
                if front.right is not None:
                    q.put(front.right)

            # Increment level to
            # move to the next level
            level += 1

        # Return the level, which represents
        # the maximum depth of the tree
        return level


# Creating a sample binary tree
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.left.right.right = Node(6)
root.left.right.right.right = Node(7)

solution = Solution()
depth = solution.maxDepth(root)

print("Maximum depth of the binary tree:", depth)
