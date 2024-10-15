def lowestCommonAncestor(self, root, p, q):
    if root is None or root == p or root == q:
        return root
    left = self.lowestCommonAncestor(root.left, p, q)
    right = self.lowestCommonAncestor(root.right, p, q)
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return root
