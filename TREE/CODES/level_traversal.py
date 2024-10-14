from collections import deque


def level_order_traversal(root):
    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    print(f"Level Order Traversal: {result}")
    return result
