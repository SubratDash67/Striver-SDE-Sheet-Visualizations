def pre_in_post_traversal(root):
    pre, in_order, post = [], [], []
    if root is None:
        return pre, in_order, post

    stack = [(root, 1)]

    traversal_states = []

    while stack:
        node, state = stack.pop()

        if state == 1:
            pre.append(node.data)
            traversal_states.append((pre[:], in_order[:], post[:], "Pre", node.data))
            state = 2
            stack.append((node, state))
            if node.left:
                stack.append((node.left, 1))

        elif state == 2:
            in_order.append(node.data)
            traversal_states.append((pre[:], in_order[:], post[:], "In", node.data))
            state = 3
            stack.append((node, state))
            if node.right:
                stack.append((node.right, 1))

        else:
            post.append(node.data)
            traversal_states.append((pre[:], in_order[:], post[:], "Post", node.data))

    return pre, in_order, post, traversal_states
