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
                self.insert(d)

    def insert(self, data, name=None):
        print("\n=========================当前插入值：{}=========================".format(data))
        print("当前点：{}".format(self))
        if self.is_2_node():
            print("往2-Node插入")
            # 判断新值与当前2节点值的大小关系
            if data < self.data:
                print("新值为左值")
                if self.l_child:
                    self.l_child.insert(data, name)
                else:
                    self.data, self.data2 = data, self.data
            elif data > self.data:
                print("新值为右值")
                if self.r_child:
                    self.r_child.insert(data, name)
                else:
                    self.data2 = data
            else:
                return None
        elif self.is_3_node():
            print("往3-Node插入")
            if self.is_root():
                print("单根3-Node节点")
                if data < self.data:
                    print("提升self左值")
                elif data > self.data2:
                    print("提升self右值")
                    self.upgrade(data, name=name)
                else:
                    print("提升新值 {}".format(data))
                    self.upgrade(data, name=name)
            else:
                print("非单根3-Node节点")
                self.upgrade(harmful_data=data, name=name)
                pass

        print("-------------------------插入程序完：{}-------------------------\n".format(data))

    def deformation(self, harmful_data=None, harmful_node=None, name=None):
        """
        当有破坏性的数据节点将要哦插入到2-3-Tree的时候，对树的结构进行拆分-提升变形操作
        :param harmful_data: 直接传入有破坏性的数据
        :param harmful_node: 传入有破坏性数据的节点
        :param name: 破坏数据节点的名称
        :return:
        """
        # TODO:破坏节点可能没有上下节点关系，此时是新数据，如果有上下文关系，那么是由于上一个节点的提升操作导致的提升操作
        h_node = harmful_node if harmful_node else B23TreeNode(harmful_data, name=name)
        if h_node.is_3_node():
            print("警告！！破坏节点是一个3-Node！！")
        # TODO:判断破坏数据节点的位置
        # 判断当前是否到达叶子
        if self.is_leaf():
            # 如果是叶子，开始判断当前节点的类型
            if self.is_2_node():
                # TODO:分支完成
                # 二节点类型，直接进行数据的插入
                if h_node.data < self.data:
                    # 作为左值
                    self.data2, self.data = self.data, h_node.data
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
                if position == -1:
                    # 将破坏节点挂在当前节点的父节点，作为父节点的中子树
                    h_node.parent = self.parent
                    self.parent.m_child = h_node
                    # 修改当前节点的节点值，转化为2-Node
                    self.data, self.data2 = self.data2, None
                elif position == 1:
                    # 将破坏节点挂在当前节点的父节点，作为父节点的中子树
                    h_node.parent = self.parent
                    self.parent.m_child = h_node
                    # 修改当前节点的节点值，转化为2-Node
                    self.data2 = None
                else:
                    # 破坏节点是中间，将当前3-Node拆分为两个节点，利用h_node作为另外一个节点
                    h_node.data2 = self.data2
                    self.data2 = None
                    h_node.parent = self.parent

                    if self.data2 < self.parent.data:
                        # 当前节点在父节点的左端
                        self.parent.m_child = h_node
                    elif self.data > self.parent.data:
                        # 当前节点在父节点的右端
                        self.parent.m_child = self
                        self.parent.r_child = h_node

                # TODO:判断父节点的类型，根据类型，对父节点进行提升
                if self.parent.is_2_node():
                    # TODO:父节点是2-Node
                    self.parent.data2 = next_h_data
                else:
                    # TODO:父节点是3-Node
                    pass
                pass

        else:
            # 如果不是叶子节点，根据孩子的情况进行破环点下钻
            if self.l_child:
                # 左下钻
                self.l_child.deformation(harmful_data, harmful_node, name)
                pass
            elif self.m_child:
                # 中下钻
                self.m_child.deformation(harmful_data, harmful_node, name)
                pass
            elif self.r_child:
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

    def upgrade(self, harmful_data=None, harmful_node=None, name=None):
        if self.is_2_node():
            print("无破坏点，判断失误!")
            return self
        # 有可能破坏树平衡的破坏节点
        h_node = harmful_node if harmful_node else B23TreeNode(harmful_data, name=name)
        # 破坏水平点
        harmful_position = 0 if h_node.data < self.data else (1 if self.data < h_node.data < self.data2 else 2)
        print("破坏水平点 {}".format(harmful_position))

        if harmful_position == 0:
            print("提升self.data:{}".format(self.data))

            # self.l_child, self.m_child, self.r_child = new_node, None, cut_r_val
            if self.l_child:
                self.l_child.insert(h_node.data, name=name)
                # self.l_child.upgrade(harmful_data=harmful_data, harmful_node=harmful_node, name=name)
            else:
                # 切下右子树，挂在self上
                print("切下右子树，挂在self上")
                cut_r_val = B23TreeNode(self.data2)
                cut_r_val.parent = self
                self.r_child = cut_r_val
                h_node.parent = self
                self.l_child = h_node
                self.parent.upgrade(harmful_node=self, name=name)

        elif harmful_position == 1:
            print("提升中间点")
            if self.m_child:
                self.m_child.insert(h_node.data, name=name)
            else:
                cut_l_node = B23TreeNode(self.data)
                cut_r_node = B23TreeNode(self.data2)

                cut_l_node.parent = cut_r_node.parent = self
                self.l_child, self.r_child = cut_l_node, cut_r_node

                self.data, self.data2 = h_node.data, None
                if self.parent:
                    if self.parent.is_root():
                        self.l_child.parent = self.parent
                        self.r_child.parent = self.parent
                        self.parent.data, self.parent.data2 = self.data, self.parent.data

                        self.parent.l_child, self.parent.m_child = self.l_child, self.r_child
                        pass
                    else:
                        self.parent.upgrade(harmful_node=harmful_node, name=name)
                else:
                    print("根节点:{}".format(self))
                    # self.l_child.l_child.parent = self
                    # self.l_child.r_child.parent = self
                    # self.data, self.data2 = self.l_child.data, self.data
                    #
                    # self.l_child, self.m_child = self.l_child.l_child, self.l_child.m_child
                    pass
        else:
            print("提升self.data2:{}".format(self.data2))
            if self.r_child:
                self.r_child.insert(h_node.data, name=name)
            else:
                # 切下左子树，挂在self上
                print("切下左子树，挂在self上")
                # cut_l_val = B23TreeNode(self.data)
                # self.parent.r_child = cut_l_val
                # cut_l_val.parent = self.parent
                #
                # cut_l_val.l_child = h_node
                #
                # self.data, self.data2 = self.data2, None
                # cut_l_val.r_child = self
                # self.parent = cut_l_val
                #
                # self.parent.upgrade(harmful_node=self.parent, name=name)
                # cut_l_val = B23TreeNode(self.data)
                # cut_l_val.parent = self
                # cut_l_val.l_child, cut_l_val.r_child = self.l_child, self.m_child
                # self.l_child, self.m_child = cut_l_val, None

        return None


class B2TreeNode(TreeNode):
    """
    2-节点
    """
    pass


if __name__ == '__main__':
    # 根节点插入左值
    # b23nd = B23TreeNode(77, children=[69])
    # 根节点插入右值
    # b23nd = B23TreeNode(77, children=[79])

    # 根2-节点插入新值，l
    b23nd = B23TreeNode(77, name='root', children=[69, 74, 82, 65, 67, 72, 76])

    # b23nd = B23TreeNode(77, children=[69, 74, 82, 65, 67, 72, 76, 80, 83, 88])
    # b23nd = B23TreeNode(77, 'root')
    # b23nd = B23TreeNode(77, children=[82, 78])
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
    print(b23nd.m_child)
    print(b23nd.r_child)
    # print(b23nd.r_child)
    # print(b23nd.r_child.r_child)
    # print(b23nd.r_child)
