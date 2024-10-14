from queue import Queue
from collections import deque, defaultdict


class Solution:
    def bottomView(self, root):

        ans = []

        if root is None:
            return ans
        mpp = defaultdict(int)

        q = Queue()
        q.put((root, 0))

        while not q.empty():

            it = q.get()
            node, line = it[0], it[1]

            mpp[line] = node.data

            if node.left:

                q.put((node.left, line - 1))

            if node.right:

                q.put((node.right, line + 1))

        for key, value in sorted(mpp.items()):
            ans.append(value)

        return ans
