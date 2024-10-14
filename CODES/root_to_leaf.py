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
