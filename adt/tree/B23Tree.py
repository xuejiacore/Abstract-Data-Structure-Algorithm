"""
B-树 / 2-3树 / 多路搜索树
"""
import collections

from util.visualization.ColorPrint import color_format
from adt.tree.BasicTree import TreeNode


class B3TreeNode(TreeNode):
    """
    3-节点
    """

    def __init__(self, data, name=None):
        super().__init__(data, name=name)
        # 三节点附加一个关键值
        self.data2 = None
        # 三节点附加一个中子节点
        self.m_child = None

    def __str__(self):
        desc = color_format(
                '[l_data=>{}{}] '.format(self.data, ', r_data=>{}'.format(self.data2) if self.data2 else ''),
                fore='red', mode='bold') + \
               color_format('parent.data=>{}, '.format(self.parent.data if self.parent else None),
                            fore='yellow', mode='bold') + \
               color_format('[l_child.l_data=>{}, {}'.format(self.l_child.data if self.l_child else None,
                                                             'l_child.r_data=>{}| '.format(
                                                                     self.l_child.data2 if self.l_child.data2 else '') if self.l_child and self.l_child.data2 else ''),
                            fore='cyan', mode='bold') + \
               color_format('m_child.l_data=>{}, {}'.format(self.m_child.data if self.m_child else None,
                                                            'm_child.r_data=>{}| '.format(
                                                                    self.m_child.data2 if self.m_child.data2 else '') if self.m_child and self.m_child.data2 else ''),
                            fore='blue', mode='bold') + \
               color_format('r_child.l_data=>{}, {}'.format(self.r_child.data if self.r_child else None,
                                                            'r_child.r_data=>{}| '.format(
                                                                    self.r_child.data2 if self.r_child.data2 else '') if self.r_child and self.r_child.data2 else ''),
                            fore='purple', mode='bold')

        return '{} --> Name: {}, Tag: {}'.format(desc, color_format(self.name, mode='bold',
                                                                    fore='red') if self.name else None, self.tag)


class B23TreeNode(B3TreeNode):
    def __init__(self, data, name=None, children=None):
        super().__init__(data, name=name)
        if children and isinstance(children, collections.Iterable):
            for d in children:
                self.deformation(d)

    def search(self, data):
        """
        查找2-3树
        :param data: 需要查找的数据
        :return: 如果找到，返回（树节点，数值，位置）元组，否则返回值为None
        """
        if data < self.data:
            return self.l_child.search(data) if self.l_child else None
        elif (self.is_3_node() and data > self.data2) or (self.is_2_node() and data > self.data):
            # 三节点且大于最右值，或者是二节点大于最右值
            return self.r_child.search(data) if self.r_child else None
        elif self.is_3_node() and self.data < data < self.data2:
            # 三节点且在左右两个值之间
            return self.m_child.search(data) if self.m_child else None
        else:
            return (self, self.data, -1) if data == self.data else (
                (self, self.data2, 1) if data == self.data2 else None)

    def middle_order_traversal(self, generate_tn=False):
        """
        生成中序遍历2-3树
        :param generate_tn: 如果为True，生成的内容为树节点，否则生成的为数据
        :return: 生成器生成的遍历数据
        """
        if self.l_child:
            for data in self.l_child.middle_order_traversal(generate_tn=generate_tn):
                yield data

        # 生成左端数据
        yield self if generate_tn else self.data

        if self.m_child:
            for data in self.m_child.middle_order_traversal(generate_tn=generate_tn):
                yield data

        # 如果有右端数据，那么生成右端数据
        if self.is_3_node():
            yield self if generate_tn else self.data2

        if self.r_child:
            for data in self.r_child.middle_order_traversal(generate_tn=generate_tn):
                yield data

    def deformation(self, harmful_data=None, harmful_node=None, name=None, from_child=False):
        """
        当有破坏性的数据节点将要哦插入到2-3-Tree的时候，对树的结构进行拆分-提升变形操作
        :param from_child: 是否从子树中传递上来的破坏节点
        :param harmful_data: 直接传入有破坏性的数据
        :param harmful_node: 传入有破坏性数据的节点
        :param name: 破坏数据节点的名称
        :return:
        """
        # TODO:破坏节点可能没有上下节点关系，此时是新数据，如果有上下文关系，那么是由于上一个节点的提升操作导致的提升操作
        h_node = harmful_node if harmful_node else B23TreeNode(harmful_data, name=name)
        real_parent = self.parent
        next_h_node = None
        if h_node.is_3_node():
            print("警告！！破坏节点是一个3-Node！！")
        # TODO:判断破坏数据节点的位置
        # 判断当前是否到达叶子
        if from_child or self.is_leaf():
            # 如果是叶子，开始判断当前节点的类型
            if self.is_2_node():
                # TODO:分支完成
                # 二节点类型，直接进行数据的插入
                if h_node.data < self.data:
                    # 作为左值
                    self.data, self.data2 = h_node.data, self.data
                elif h_node.data > self.data:
                    # 作为右值
                    self.data2 = h_node.data
                else:
                    # 数据冲突，返回失败
                    return False
            else:
                # TODO:--------------------------------------------------- 处理提升位置与保留提升值
                # 判断传递到父节点需要处理的破坏数据以及提升位置
                position = 0
                next_h_data = h_node.data
                if h_node.data < self.data:
                    # self.data提升
                    next_h_data = self.data
                    position = -1
                elif h_node.data > self.data2:
                    # self.data2提升
                    next_h_data = self.data2
                    position = 1

                # TODO:--------------------------------------------------- 处理破坏节点的嫁接
                if (from_child and self.is_root()) or self.is_leaf() and self.is_root():
                    if h_node.data < self.data:
                        cut_node = B23TreeNode(self.data2)
                        cut_node.l_child, cut_node.r_child = self.m_child, self.r_child
                        self.r_child.parent = self.m_child.parent = cut_node
                        h_node.parent = cut_node.parent = self
                        self.l_child, self.r_child = h_node, cut_node
                        self.data2 = None
                        self.m_child = None

                    elif h_node.data > self.data2:
                        cut_node = B23TreeNode(self.data)
                        h_node.parent = cut_node.parent = self
                        self.l_child, self.r_child = cut_node, h_node
                        self.data2, self.data = None, self.data2
                    else:
                        cut_l_node = B23TreeNode(self.data)
                        cut_r_node = B23TreeNode(self.data2)

                        cut_l_node.parent = cut_r_node.parent = self
                        self.l_child, self.r_child = cut_l_node, cut_r_node
                        self.data2, self.data = None, h_node.data

                elif self.is_leaf():
                    if position == -1:
                        # 将破坏节点挂在当前节点的父节点，作为父节点的中子树
                        h_node.parent = self.parent
                        self.parent.m_child = h_node
                        # 修改当前节点的节点值，转化为2-Node
                        self.data, self.data2 = self.data2, None
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    elif position == 1:
                        # 将破坏节点挂在当前节点的父节点，作为父节点的中子树
                        h_node.parent = self.parent
                        self.parent.m_child = h_node
                        # 修改当前节点的节点值，转化为2-Node
                        self.data2 = None
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    else:
                        # 破坏节点是中间，将当前3-Node拆分为两个节点，利用h_node作为另外一个节点

                        if self.data2 < real_parent.data:
                            # 创造一个新的节点，使其指向父节点
                            if self.parent.is_3_node():
                                next_h_node = B23TreeNode(next_h_data)
                                next_h_node.l_child = self
                                next_h_node.parent = self.parent
                                self.parent.l_child = next_h_node
                                real_parent = self.parent
                                self.parent = next_h_node
                                h_node.parent = next_h_node
                            else:
                                h_node.parent = self.parent
                                self.parent.m_child = h_node
                        elif self.data > real_parent.data:
                            if self.parent.is_3_node():
                                next_h_node = B23TreeNode(next_h_data)
                                next_h_node.l_child = self
                                next_h_node.parent = self.parent
                                self.parent.r_child = next_h_node
                                real_parent = self.parent
                                self.parent = next_h_node
                                h_node.parent = next_h_node
                            else:
                                # 二节点
                                pass

                        if self.data2 < real_parent.data:

                            # TODO:3-Node在父节点的左端
                            if next_h_node:
                                # 当前节点在父节点的左端
                                self.parent.r_child = h_node
                                next_h_node.data = h_node.data
                                h_node.data = self.data2
                            else:
                                h_node.data = self.data2
                                # 设置当前节点的右值为空
                            self.data2 = None
                        elif self.data > real_parent.data:
                            # TODO:3-Node在父节点的右端

                            if next_h_node:
                                # 当前节点在父节点的左端
                                self.parent.l_child = h_node
                                next_h_node.data = h_node.data
                                h_node.data = self.data
                            else:
                                h_node.data = self.data2
                                # 设置当前节点的右值为空
                            self.data, self.data2 = self.data2, None
                            pass

                if real_parent:
                    # TODO:判断父节点的类型，根据类型，对父节点进行提升
                    if real_parent.is_2_node() and next_h_data:
                        # TODO:父节点是2-Node
                        if next_h_data > real_parent.data:
                            real_parent.data2 = next_h_data
                        else:
                            real_parent.data, real_parent.data2 = next_h_data, real_parent.data
                    else:
                        # TODO:父节点是3-Node，继续拆分父节点
                        real_parent.deformation(harmful_data=None, harmful_node=next_h_node, name=name, from_child=True)
                        pass
                else:
                    pass

        else:
            # 如果不是叶子节点，根据孩子的情况进行破环点下钻
            if self.l_child and h_node.data < self.data:
                # 左下钻
                self.l_child.deformation(harmful_data, harmful_node, name)
                pass
            elif self.m_child and self.data < h_node.data < self.data2:
                # 中下钻
                self.m_child.deformation(harmful_data, harmful_node, name)
                pass
            elif self.r_child and (h_node.data > self.data2) if h_node.data2 else (h_node.data > self.data):
                # 右下钻
                self.r_child.deformation(harmful_data, harmful_node, name)
                pass

    def is_2_node(self):
        return self.data and not self.data2

    def is_3_node(self):
        return self.data and self.data2

    def is_leaf(self):
        return not (self.l_child or self.m_child or self.r_child)

    def is_root(self):
        return not self.parent


class B2TreeNode(TreeNode):
    """
    2-节点
    """
    pass


if __name__ == '__main__':
    # 根节点插入左值
    # b23nd = B23TreeNode(77, name='root', children=[82, 78])
    # 根节点插入右值
    # b23nd = B23TreeNode(77, children=[79])

    # 根2-节点插入新值，l
    # b23nd = B23TreeNode(77, name='root', children=[69, 74, 82, 65, 67, 72, 76])

    # b23nd = B23TreeNode(77, children=[69, 74, 82, 65, 67, 72, 76, 80, 83, 88])
    # b23nd = B23TreeNode(77, 'root')

    b23nd = B23TreeNode(77, name='root', children=[82, 78, 74, 90, 85, 80, 88, 75, 60, 65])
    # b23nd = B23TreeNode(77, name='root', children=[82, 78, 74, 90, 85, 81, 88, 89])u
    # b23nd.insert(69)
    # b23nd.insert(74)
    # b23nd.insert(82)
    # b23nd.insert(78)
    # b23nd.insert(79)
    # b23nd.insert(80)
    # b23nd.insert(81)
    # b23nd.insert(65)
    # b23nd.insert(82)
    # b23nd.insert(74)
    print(b23nd)
    print(b23nd.l_child)
    print(b23nd.l_child.l_child)
    print(b23nd.m_child)
    print(b23nd.r_child)



    # print([i for i in b23nd.middle_order_traversal()])
    #
    # for node in b23nd.middle_order_traversal(generate_tn=True):
    #     print(node)
    # print(b23nd.r_child)
    # print(b23nd.r_child.r_child)
    # print(b23nd.r_child)
