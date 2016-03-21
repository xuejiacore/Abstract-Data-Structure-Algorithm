"""
ADT-TREE
"""
import collections

from util.visualization.ColorPrint import color_format


class TreeNode(object):
    """
    The abstract data structure of tree node.
    """

    def __init__(self, data, name=None):
        """
        To initializing a tree node.
        :param data: the data of tree node
        :param name: the name of tree node
        :return: the instance of tree node
        """
        # The data of the node.
        self.data = data
        # left-child node
        self.l_child = None
        # right-child node
        self.r_child = None
        # parent node
        self.parent = None
        # tag of the node
        self.tag = None
        self.name = name

    def __str__(self):
        desc = color_format('data=>{}, '.format(self.data), fore='cyan', mode='bold') + \
               color_format('parent.data=>{}, '.format(self.parent.data if self.parent else None),
                            fore='yellow', mode='bold') + \
               color_format('[l_child.data=>{}, '.format(self.l_child.data if self.l_child else None),
                            fore='yellow', mode='bold') + \
               color_format('r_child.data=>{}]'.format(self.r_child.data if self.r_child else None),
                            fore='purple', mode='bold')

        return '{} --> name: {}, tag: {}'.format(desc, self.name, self.tag)


class BinaryTreeNode(TreeNode):
    """
    Binary tree，regulation is Middle Order Traversal
    """

    def __init__(self, data, name=None, children=None):
        """
        Initialize a tree node.
        :param data: Value of current node.
        :param name: Name of current node.
        :param children: Child of current node.
        :return:
        """
        super().__init__(data, name)
        if children and isinstance(children, collections.Iterable):
            for d in children:
                self.insert(d)

    def insert(self, data, tag=None):
        """
        To insert a new tree node.
        :param tag: the description of tree node
        :param data: the data that will be inserted
        :return: will return the current node if operation is success otherwise will be none
        """
        if data < self.data:
            if self.l_child:
                return self.l_child.insert(data, tag)
            else:
                _node = BinaryTreeNode(data, tag)
                _node.parent = self
                self.l_child = _node
                return _node
        elif data > self.data:
            if self.r_child:
                return self.r_child.insert(data, tag)
            else:
                _node = BinaryTreeNode(data, tag)
                _node.parent = self
                self.r_child = _node
                return _node
        else:
            return None

    def remove(self, data=None, node=None):
        """
        To remove a tree node.
        :param node:
        :param data: the data that will be remove
        The current node instance will be delete if the parameter 'data' is none,
        otherwise will search tree node by data first and then remove the node.
        :return: will return the data of node that had been removed otherwise will be none
        """
        if not (data or node):
            node = self

        search_node = self.search(data) if data else node

        if not search_node:
            # Will return none if the value is not exist.
            return None
        del_data = search_node.data
        if search_node.is_leaf():
            # Delete the current node which node is leaf, and then make it's parent as none.
            if search_node.is_left_child():
                search_node.parent.l_child = None
            else:
                search_node.parent.r_child = None
            del search_node

        elif search_node.l_child and search_node.r_child:
            # Delete it's successor (must not exist left-child), and then replace the value that want to delete.
            successor_node = search_node.successor()
            search_node.data = successor_node.remove(node=successor_node)
        elif search_node.l_child and not search_node.r_child:
            # Only left subtree
            if search_node.is_left_child():
                search_node.parent.l_child = search_node.l_child
            else:
                search_node.parent.r_child = search_node.l_child
            # Associate
            search_node.l_child.parent = search_node.parent
        elif search_node.r_child and not search_node.l_child:
            # Only right subtree
            if search_node.is_right_child():
                search_node.parent.r_child = search_node.r_child
            else:
                search_node.parent.l_child = search_node.r_child
            search_node.r_child.parent = search_node.parent
        return del_data

    def search(self, data):
        """
        To find a node via provided parameter.
        :param data: the data which will be found
        :return: will return the node if found it otherwise will be none
        """
        if data == self.data:
            # Found the data and return.
            self.tag = 'search'
            return self
        elif self.l_child and data < self.data:
            # The data is lower than the current node, to find the left subtree (if the left subtree exists)
            self.tag = 'search'
            return self.l_child.search(data)
        elif self.r_child and data > self.data:
            # The data is greater than the current node, to find the right subtree (if the right subtree exists)
            self.tag = 'search'
            return self.r_child.search(data)
        else:
            # Node not found, return None
            return None

    def max(self, ignore_right=False):
        """
        To finding a maximum node.
        :param ignore_right: whether ignore the right sub-tree
        :return: the maximum node
        """
        if not ignore_right and self.r_child:
            return self.r_child.max()
        else:
            self.tag = 'max'
            return self

    def min(self, ignore_left=False):
        """
        To finding a minimum node.
        :param ignore_left: whether ignore the left sub-tree.
        :return: the minimum node
        """
        if not ignore_left and self.l_child:
            return self.l_child.min()
        else:
            self.tag = 'min'
            return self

    def is_leaf(self):
        """
        To determine whether the leaf node.
        :return: will return True if it is otherwise will return False.
        """
        return not (self.l_child or self.r_child)

    def is_root(self):
        """
        To determine whether the root node.
        :return: will return True if it is otherwise will return False.
        """
        return self.parent is None

    def depth(self):
        """
        Calculate the depth of the tree.
        :return: the depth of the tree
        """
        if not (self.l_child or self.r_child):
            return 1
        if self.l_child and self.r_child:
            return 1 + max(self.l_child.depth(), self.r_child.depth())
        elif self.l_child and not self.r_child:
            return 1 + self.l_child.depth()
        else:
            return 1 + self.r_child.depth()

    def predecessor(self):
        """
        To search the predecessor of the current node.
        :return: the predecessor node while current node exist, otherwise, will be none
        """
        if self.l_child:
            # If the current node contains the left child tree,
            # the predecessor of the sequence traversal is the largest one in the left tree.
            p_node = self.l_child.max()
            p_node.tag = 'predecessor'
            return p_node
        else:
            if self.is_left_child():
                # If the current node is left, it always has to go back to the parent node,
                # until a parent node is the right one.
                current_node = self
                while current_node.is_left_child():
                    current_node = current_node.parent
                current_node.tag = 'predecessor'
                return None if current_node.is_root() else current_node
            else:
                # If the current node is the right node, the parent node is the precursor of the current node.
                self.tag = 'predecessor'
                return self.parent

    def successor(self):
        """
        To search the successor of the current node.
        :return: the successor node while current node exist, otherwise, will be none
        """
        if self.r_child:
            s_node = self.r_child.min()
            s_node.tag = 'successor'
            return s_node
        else:
            if self.is_right_child():
                # If the current node is the right node, it has been an iterative backtracking parent node,
                # knowing that the identity of the parent node is left.
                current_node = self
                while current_node.is_right_child():
                    current_node = current_node.parent
                if not current_node.parent:
                    return None
                current_node.parent.tag = 'successor'
                return current_node.parent
            else:
                # If the current node is left node, the parent node is the successor node of the current node.
                self.parent.tag = 'successor'
                return self.parent

    def is_left_child(self):
        """
        To determine whether current node is left-child related by it's parent.
        :return: will return True if it is, otherwise, will be False
        """
        return self.parent and self.parent.l_child.data == self.data

    def is_right_child(self):
        """
        To determine whether current node is right-child related by it's parent.
        :return: will return True if it is, otherwise, will be False
        """
        return self.parent and self.parent.r_child.data == self.data

    def pre_order_traversal(self):
        """
        Pre-order traversal the binary tree.
        :return:
        """
        yield self
        if self.l_child:
            for l_node in self.l_child.pre_order_traversal():
                yield l_node
        if self.r_child:
            for r_node in self.r_child.pre_order_traversal():
                yield r_node

    def middle_order_traversal(self):
        """
        Middle-order traversal the binary tree.
        :return:
        """
        if self.l_child:
            for l_node in self.l_child.middle_order_traversal():
                yield l_node
        yield self
        if self.r_child:
            self.r_child.pre_order_traversal()
            for r_node in self.r_child.middle_order_traversal():
                yield r_node

    def after_order_traversal(self):
        """
        After-order traversal the binary tree.
        :return:
        """
        if self.l_child:
            for l_node in self.l_child.after_order_traversal():
                yield l_node
        if self.r_child:
            for r_node in self.r_child.after_order_traversal():
                yield r_node
        yield self


if __name__ == '__main__':
    rootNode = BinaryTreeNode(15, name='root', children=[6, 3, 2, 4, 7, 13, 18, 16, 20])
    # rootNode.insert(6)
    # rootNode.insert(3)
    # rootNode.insert(2)
    # rootNode.insert(4)
    # rootNode.insert(7)
    # rootNode.insert(13)
    # rootNode.insert(18)
    # rootNode.insert(16)
    # rootNode.insert(20)

    print([node.data for node in rootNode.middle_order_traversal()])
    print(rootNode.search(18))
    print(rootNode)
