def postorder_traversal(root):
    result = []

    def traverse(node):
        if node:
            traverse(node.left)
            traverse(node.right)
            result.append(node.val)

    traverse(root)
    print(f"Postorder Traversal: {result}")
    return result
