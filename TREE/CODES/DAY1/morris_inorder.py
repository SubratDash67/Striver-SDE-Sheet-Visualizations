def morris_inorder_traversal(root, graph, pos, speed):
    result = []
    cur = root

    while cur:
        if cur.left is None:
            result.append(cur.val)
            cur = cur.right
        else:
            prev = cur.left
            while prev.right and prev.right != cur:
                prev = prev.right
            if prev.right is None:
                prev.right = cur
                cur = cur.left
            else:
                prev.right = None
                result.append(cur.val)
                cur = cur.right

    print(f"Morris Inorder Traversal: {result}")
    return result
