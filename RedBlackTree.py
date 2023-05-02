

class Node:
    def __init__(self, value):
        self.color = "r"
        self.parent = None
        self.value = value
        self.left = None
        self.right = None


class RedBlackTree:
    def __init__(self, value):
        self.root = Node(value)
        self.root.color = "b"

    def left_rotation(self, grandparent):
        """Левый поворот"""
        new_grandparent = grandparent.right
        grandparent.right = new_grandparent.left
        if new_grandparent.left != None:
            new_grandparent.left.parent = grandparent
        new_grandparent.parent = grandparent.parent
        if grandparent.parent == None:
            self.root = new_grandparent
        elif grandparent == grandparent.parent.left:
            grandparent.parent.left = new_grandparent
        else:
            grandparent.parent.right = new_grandparent
        new_grandparent.left = grandparent
        grandparent.parent = new_grandparent
        new_grandparent.color = grandparent.color
        grandparent.color = "r"


    def right_rotation(self, grandparent):
        """Правый поворот"""
        new_grandparent = grandparent.left
        grandparent.left = new_grandparent.right
        if new_grandparent.right != None:
            new_grandparent.right.parent = grandparent
        new_grandparent.parent = grandparent.parent
        if grandparent.parent == None:
            self.root = new_grandparent
        elif grandparent == grandparent.parent.right:
            grandparent.parent.right = new_grandparent
        else:
            grandparent.parent.left = new_grandparent
        new_grandparent.right = grandparent
        grandparent.parent = new_grandparent
        new_grandparent.color = grandparent.color
        grandparent.color = "r"
    

    def swap_colors(self, node):
        # Смена цвета
        if node != self.root:   node.color = "r"
        else: node.color = "b"
        node.left.color = "b"
        node.right.color = "b"


    def color_correction(self, root):
        # Коррекция цвета при вливании боковых ветвей
        temp_node = root.left.left
        while temp_node != None:
            if temp_node.color != temp_node.parent.color:
                temp_node = temp_node.left
                continue
            else:
                if temp_node.color == "r":  temp_node.color = "b"
                else: temp_node.color = "r"
            

    def insert_node(self, value):
        # Вставка узла
        new_node = Node(value)
        temp_node = self.root
        parent = None

        while temp_node != None:
            parent = temp_node
            if value < temp_node.value:
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right

        new_node.parent = parent
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
        self.balancing_tree(new_node)

    
    def balancing_tree(self, node):
        parent = node.parent
        # parent == None отсутствие "отца" означает, что узел является корнем.
        if parent == None:
            node.color = "b"
            return
        grandparent = parent.parent
        # grandparent == None отсутствие "деда" означает, что "отец" является корнем.
        if grandparent == None:
            # Вставка узла слева от корня (справа узла нет)
            if parent.right == None and node == parent.left:
                return
            # вставка узла справа от корня (слева узла нет)
            if parent.left == None and node == parent.right:
                self.left_rotation(parent)
                return
            # вставка узла справа от корня (слева узел есть и он конечный)
            if parent.left != None and parent.left.left == None and node == parent.right:
                self.swap_colors(parent)
                return

        # "дед" корень
        if grandparent == self.root:
            # узел левый-левый от корня и нет "дяди"
            if grandparent.left == parent and parent.left == node and grandparent.right == None:
                self.right_rotation(grandparent)
                self.swap_colors(parent)
                return
            # узел левый-правый от корня и нет "дяди"
            if grandparent.left == parent and parent.right == node and grandparent.right == None:
                # self.right_rotation(parent)
                self.left_rotation(parent)
                self.balancing_tree(parent)
                return
            # "отец" слева от корня и есть "дядя"
            if grandparent.left == parent and parent.right == node and grandparent.right != None:
                if parent.left == None:
                    self.left_rotation(parent)
                else:
                    node.color = "b"
                return
        
        # "дед" не корень
        if grandparent.parent != None:
            # "отец" слева от "деда", "дед" левый потомок верхнего узла
            if grandparent.left == parent and grandparent.parent.left == grandparent:
                # "сын" слева от "отца" и "отец" красный
                if node == parent.left and parent.color == "r":
                    node.color = "b"
                    return
                # "сын" справа от "отца" и "отец" красный
                if node == parent.right and parent.color == "r":
                    self.left_rotation(parent)
                    node.color = "r"
                    parent.color = "b"
                    return
                # "сын" слева от "отца" и "отец" черный
                if  parent.left == node and parent.right == None and parent.color == "b":
                    return
                # "сын" справа от "отца" и "отец" черный
                if parent.right == node and parent.left == None and parent.color == "b":
                    self.left_rotation(parent)
                # "сын" справа от "отца" и уже есть узел слева от "отца"
                if node == parent.right and parent.color == "b" and parent.left != None:
                    node.color = "b"
                    return
            # "отец" слева от "деда", "дед" правый потомок верхнего узла
            if grandparent.left == parent and grandparent.parent.right == grandparent:
                # если "сын" справа от "отца", то сначала левый поворот
                if parent.right == node:
                    self.left_rotation(parent)
                    parent = grandparent.left
                # если "сын" слева от "отца"
                self.right_rotation(grandparent)
                self.swap_colors(parent)
                grandparent = parent.parent
                self.left_rotation(grandparent)
                self.color_correction(self.root)
                return
        # "отец" справа от "деда"
        if grandparent.right == parent:
            # "сын" слева от "отца" и "отец" черный
            if  parent.left == node and parent.right == None:
                return
            # "сын" справа от "отца" и "отец" черный
            if parent.right == node and parent.left == None:
                self.left_rotation(parent)
            # "сын" справа от "отца" и уже есть узел слева от "отца"
            if parent.right == node and parent.color == "b" and parent.left != None:
                self.swap_colors(parent)
                self.left_rotation(grandparent)
                self.color_correction(self.root)


    def print_tree(self, node, level):
        # Печать дерева
        if node != None:
            self.print_tree(node.right, level + 1)
            print(" "*10*level, end=' ')
            print(str(node.value) + " " + ("\033[1m\033[31m{}\033[0m".format("R") if node.color == "r" else 'B') + "\n")
            self.print_tree(node.left, level + 1)

