def isIdentical(self, node1, node2):
    if node1 is None and node2 is None:
        return True
    if node1 is None or node2 is None:
        return False
    return (
        node1.data == node2.data
        and self.isIdentical(node1.left, node2.left)
        and self.isIdentical(node1.right, node2.right)
    )
