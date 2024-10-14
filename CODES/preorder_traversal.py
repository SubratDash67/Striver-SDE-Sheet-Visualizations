def preorder_traversal(root, graph, pos, speed):
    result = []

    def traverse(node):
        if node:
            result.append(node.val)
            traverse(node.left)
            traverse(node.right)

    traverse(root)
    print(f"Preorder Traversal: {result}")
    return result
