class Tree:
    def __init__(self):
        self.left = []
        self.right = []
        self.data = []


def inorderTraverse(tree, pointer):
    if tree.left[pointer] != -1:
        inorderTraverse(tree, tree.left[pointer])
    print(tree.data[pointer], end=" ")
    if tree.right[pointer] != -1:
        inorderTraverse(tree, tree.right[pointer])


def postorderTraverse(tree, pointer):
    if tree.left[pointer] != -1:
        postorderTraverse(tree, tree.left[pointer])
    if tree.right[pointer] != -1:
        postorderTraverse(tree, tree.right[pointer])
    print(tree.data[pointer], end=" ")


def preorderTraverse(tree, pointer):
    print(tree.data[pointer], end=" ")
    if tree.left[pointer] != -1:
        preorderTraverse(tree, tree.left[pointer])
    if tree.right[pointer] != -1:
        preorderTraverse(tree, tree.right[pointer])


tree = Tree()
tree.left = [1, 3, 5, -1, -1, -1, -1]
tree.data = ["+", "*", "/", "a", "b", "c", "d"]
tree.right = [2, 4, 6, -1, -1, -1, -1]
inorderTraverse(tree, 0)
preorderTraverse(tree, 0)
postorderTraverse(tree, 0)
