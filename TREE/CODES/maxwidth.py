from queue import Queue
from collections import deque


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.levels = []

    def widthOfBinaryTree(self, root: TreeNode) -> int:
        if not root:
            return 0

        max_width = 0
        q = Queue()
        q.put((root, 0))

        while not q.empty():
            size = q.qsize()
            mmin = q.queue[0][1]
            first, last = None, None

            current_level = []

            for i in range(size):
                node, index = q.get()
                cur_id = index - mmin

                if i == 0:
                    first = cur_id
                if i == size - 1:
                    last = cur_id

                current_level.append(node.val)

                if node.left:
                    q.put((node.left, cur_id * 2 + 1))
                if node.right:
                    q.put((node.right, cur_id * 2 + 2))

            self.levels.append(current_level)

            max_width = max(max_width, last - first + 1)

        return max_width
