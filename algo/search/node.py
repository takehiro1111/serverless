class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left = None
        self.right = None


def insert(node: Node, value: int) -> Node:
    if node is None:
        return Node(value)

    if value < node.value:
        node.left = insert(node.left, value)
    else:
        node.right = insert(node.right, value)

    print("node", node.value)
    return node


def inorder(node: Node):
    """
    InOrder Left -> Root -> Right

    OreOrder Root -> Left -> Right

    PostOrder Left -> Right -> Root
    """

    if node is not None:
        inorder(node.left)
        print(node.value)
        inorder(node.right)


def search(node: Node, value: int):
    if node is None:
        return False

    if node.value == value:
        return True
    elif node.value > value:
        return search(node.left, value)
    elif node.value < value:
        return search(node.right, value)


def remove(node: Node, value: int):
    if node is None:
        return node

    if node.value > value:
        node.left = remove(node.left, value)

    elif node.value < value:
        node.right = remove(node.right, value)

    else:
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left


if __name__ == "__main__":
    root = None
    root = insert(root, 3)
    root = insert(root, 2)
    root = insert(root, 1)
    root = insert(root, 6)
    root = insert(root, 5)
    root = insert(root, 7)
    root = insert(root, 8)
    print("root.value", root.value)
    print("root.right.value", root.right.value)
    print("root.right.left.value", root.right.left.value)
    print("root.right.right.value", root.right.right.value)
    print("root.right.right.value", root.right.right.right.value)
    inorder(root)

    # 木構造のてっぺんのtootは3
    print(search(root, 9))
