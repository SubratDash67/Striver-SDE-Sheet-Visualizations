from collections import defaultdict, deque


def findVertical(self, root):
    nodes = defaultdict(
        lambda: defaultdict(set)
    )  # Map for nodes based on vertical & level
    todo = deque([(root, (0, 0))])  # Queue for BFS traversal with (node, (x, y))
    traversal_states = []  # Store states for animation

    while todo:
        temp, (x, y) = todo.popleft()  # Dequeue the current node and its coordinates
        nodes[x][y].add(temp.data)  # Add the node to the map

        # Save the current state for animation
        traversal_states.append((x, y, temp.data, dict(nodes)))

        # Process left and right children
        if temp.left:
            todo.append((temp.left, (x - 1, y + 1)))  # Left child: x-1, y+1
        if temp.right:
            todo.append((temp.right, (x + 1, y + 1)))  # Right child: x+1, y+1

    # Prepare the final result in a 2D list from the map
    ans = []
    for x in sorted(nodes):
        col = []
        for y in sorted(nodes[x]):
            col.extend(sorted(nodes[x][y]))  # Add sorted values to the column
        ans.append(col)

    return ans, traversal_states  # Return result and states for animation
