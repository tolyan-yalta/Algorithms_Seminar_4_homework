from RedBlackTree import *
import random

tree = RedBlackTree(0)

list = [82, 19, 56, 9, 81, 35, 99, 27, 18, 64, 50, 10, 93, 17, 100, 49, 70, 44, 41, 83]

# while len(list) < 20:
#     temp = random.randint(1, 100)
#     if temp not in list:
#         list.append(temp)
# print(list)
for i in range(0, len(list)):
    tree.insert_node(list[i])

tree.print_tree(tree.root, 0)
