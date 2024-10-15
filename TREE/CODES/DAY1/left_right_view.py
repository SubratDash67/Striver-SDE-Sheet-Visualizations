def recursionLeft(root, level, res, visited_nodes):
    if not root:
        return
    if len(res) == level:
        res.append(root.data)
        visited_nodes.append(root.data)
    recursionLeft(root.left, level + 1, res, visited_nodes)
    recursionLeft(root.right, level + 1, res, visited_nodes)


def recursionRight(root, level, res, visited_nodes):
    if not root:
        return
    if len(res) == level:
        res.append(root.data)
        visited_nodes.append(root.data)
    recursionRight(root.right, level + 1, res, visited_nodes)
    recursionRight(root.left, level + 1, res, visited_nodes)
