# Node class for the binary tree
class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


# Solution class to find the diameter of the binary tree
class Solution:
    def diameterOfBinaryTree(self, root):
        # Initialize the variable to store the diameter of the tree
        diameter = [0]
        # Call the height function to traverse the tree and calculate diameter
        self.height(root, diameter)
        # Return the calculated diameter
        return diameter[0]

    # Function to calculate the height of the tree and update the diameter
    def height(self, node, diameter):
        # Base case: If the node is None, return 0 indicating the height of an empty tree
        if not node:
            return 0

        # Recursively calculate the height of left and right subtrees
        lh = self.height(node.left, diameter)
        rh = self.height(node.right, diameter)

        # Update the diameter with the maximum of current diameter or sum of left and right heights
        diameter[0] = max(diameter[0], lh + rh)

        # Return the height of the current node's subtree
        return 1 + max(lh, rh)


# Main function
if __name__ == "__main__":
    # Creating a sample binary tree
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.left.right.right = Node(6)
    root.left.right.right.right = Node(7)

    # Creating an instance of the Solution class
    solution = Solution()

    # Calculate the diameter of the binary tree
    diameter = solution.diameterOfBinaryTree(root)

    print("The diameter of the binary tree is:", diameter)
