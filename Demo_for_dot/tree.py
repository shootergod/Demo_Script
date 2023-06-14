# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : tree.py
@Time    : 2023/06/20 10:22:32
@Author  : HuJi
@Contact : shootergod@forxmail.com
@Version : 0.1
@Desc    : None
'''

# ============================================================
# Import
# ============================================================



# ============================================================
# Class
# ============================================================
class Tree():
    # ==================================================
    # Constant
    # ==================================================
    DFS = 'dfs'
    BFS = 'bfs'

    # ==================================================
    # Init
    # ==================================================
    def __init__(self, parent=None, data=None):
        self.__parent: Tree = parent
        self.__children: list[Tree] = []
        self.__data = data

        self.__level: int = 1

    # ==================================================
    # Private Group
    # ==================================================
    def __print_title(self, data: str, max_w: int = 64) -> str:
        str_w = max_w - 10
        str_mid = ' ... '
        blank = ' '
        str_tpl = '{:-^' + str(max_w) + 's}'
        if len(data) > str_w:
            ind_0 = int(str_w / 2 - len(str_mid))
            ind_2 = int(-str_w / 2)
            tmp_str = blank + data[:ind_0] + str_mid + data[ind_2:] + blank
        else:
            tmp_str = blank + data + blank

        print(str_tpl.format(tmp_str))

    # ==================================================
    # Private Group
    # ==================================================


    def __is_root(self):
        return True if self.__parent is None else False

    def __is_last_node(self):
        return True if self is self.__parent.__children[-1] else False

    def __update_level(self):
        node = self
        while node.__parent:
            self.__level += 1
            node = node.__parent

    def __bfs(self):
        queue: list[Tree] = [self]
        rst: list[Tree] = []
        while queue != []:
            node = queue.pop(0)
            rst.append(node)
            for child in node.__children:
                queue.append(child)
        return rst

    def __dfs(self):
        queue: list[Tree] = [self]
        rst: list[Tree] = []
        while queue != []:
            node = queue.pop()
            rst.append(node)
            for child in reversed(node.__children):
                queue.append(child)
        return rst

    def __print_map(self):
        info_master = self.get_name()
        info_slave = ', '.join([node.get_name() for node in self.__children])
        info = '{} -> [{}]'.format(info_master, info_slave)
        print(info)

    def __search_node(self, key, verbose: bool = False):
        if verbose:
            print('Search Node: |{}|'.format(self.get_name()))

        # self-test
        if self.get_name() == key:
            if verbose:
                print('|{}| -> Yes! from Main.'.format(self.get_name()))
            return self
        else:
            if verbose:
                print('|{}| ->  No! from Main.'.format(self.get_name()))

        # goto children
        for child in self.__children:
            if verbose:
                print('Go To Children Loop by Caller: |{}| -> |{}|'.format(
                    child.__parent.get_name(), child.get_name()))
            temp: Tree = child.__search_node(key, verbose=verbose)
            if temp is not None:
                if verbose:
                    print(
                        '|{}| -> Yes! from Children Loop - within Loop Caller: |{}|'
                        .format(temp.get_name(), temp.__parent.get_name()))
                return temp

        if verbose:
            print('|{}| -> Not Found from Main.'.format(self.get_name()))
        return None

    # ==================================================
    # Public Group
    # ==================================================
    def set_root(self, data):
        self.__data = data

    def detach(self):
        self.__parent.__children.remove(self)
        self.__parent = None

    def detach_r(self):
        nodes = self.__bfs()
        for node in nodes:
            node.detach()

    def remove_node(self, tgt_node=None):
        # if user set tgt_node -> remove tgt_node
        # or remove itself
        if tgt_node:
            this_node = self.__search_node(tgt_node)
        else:
            this_node = self

        # reset all children
        nodes = this_node.__bfs()
        for node in nodes:
            node.detach()

        if this_node.__parent is None:
            # case: it is root -> just set to None
            this_node = None
        else:
            # detach from the parent
            parent = this_node.__parent
            parent.__children.remove(this_node)

    # ==================================================
    # Public Group - OK
    # ==================================================
    def get_name(self):
        return str(self.__data)

    def has_children(self):
        return True if self.__children else False

    def get_children(self):
        return self.__children

    def get_name(self):
        return str(self.__data)

    def has_children(self):
        return True if self.__children else False

    def get_children(self):
        return self.__children

    def get_level(self):
        self.__update_level()
        return self.__level

    def add_node(self, node):
        node.__parent = self
        self.__children.append(node)

    def search_node(self, key, verbose: bool = False):
        node_name = str(key)
        self.__print_title('Search Start ... Target: {}'.format(node_name))
        rst = self.__search_node(node_name, verbose=verbose)
        if rst:
            print('|{}| has been found!'.format(node_name))
        else:
            print('|{}| has not  found!'.format(node_name))
        self.__print_title('Search Finish ... Target: {}'.format(node_name))
        return rst



    def traverse(self, walk_type: str=BFS):
        if walk_type == Tree.BFS:
            nodes = self.__bfs()
        elif walk_type == Tree.DFS:
            nodes = self.__dfs()
        else:
            raise Exception('Unknown Type: {}'.format(walk_type))
        return nodes

    def disp_map(self, walk_type: str = BFS):
        self.__print_title('Map View in {}'.format(walk_type))
        nodes = self.traverse(walk_type=walk_type)
        for node in nodes:
            node.__print_map()

    def disp_tree(self):
        self.__print_title('Tree View')

        space = '   '
        branch = '│  '
        tee = '├─ '
        last = '└─ '

        nodes = self.__dfs()
        tree_info: list[str] = []

        for node in nodes:
            # special for root node
            if node.__is_root():
                tree_info += [str(node.__data)]
                continue

            # other normal nodes
            if node.__is_last_node():
                line_p2 = last + str(node.__data)
            else:
                line_p2 = tee + str(node.__data)

            # get correct branch line info
            tmp_node = node
            line_p1 = ''
            while tmp_node.__parent:
                if tmp_node.__parent.__is_root():
                    break
                else:
                    if tmp_node.__parent.__is_last_node():
                        # no crossing at upper level, so no branch line
                        line_p1 = space + line_p1
                    else:
                        # crossing at upper level, so use branch line
                        line_p1 = branch + line_p1
                tmp_node = tmp_node.__parent

            line = line_p1 + line_p2
            tree_info += [line]

        print('\n'.join(tree_info))

    def print_level(self):
        self.__print_title('Node Level')
        nodes = self.__bfs()
        levels = [node.get_level() for node in nodes]
        print(levels)


# ============================================================
# Test
# ============================================================
def test():
    import os
    cwd = os.path.dirname(__file__)
    tm_fn = 'tree_model.txt'
    tm_fp = os.path.join(cwd, tm_fn)
    with open(file=tm_fp, mode='r', encoding='utf-8') as fid:
        content = fid.read().splitlines()

    # 1st: create tree depend on the *.txt info
    masters: list[Tree] = []

    for ind, line in enumerate(content):
        tmp_str = line.strip()
        tmp_lvl = int(line.count(' ') / 4)

        if ind == 0:
            # case 01: special for 1st node [root node]
            # add node
            root = Tree(data=tmp_str)
            # update master
            if len(masters) < tmp_lvl + 1:
                masters.append(None)
            masters[tmp_lvl] = root
        else:
            # case 02: normal nodes
            # get parent node
            master_lvl = tmp_lvl - 1
            cur_master = masters[master_lvl]
            # add node
            tmp_node = Tree(data=tmp_str)
            cur_master.add_node(tmp_node)
            # update master
            if len(masters) < tmp_lvl + 1:
                masters.append(None)
            masters[tmp_lvl] = tmp_node

    s_node = root.search_node('302', verbose=False)

    root.disp_map(walk_type=Tree.BFS)
    root.disp_map(walk_type=Tree.DFS)
    root.disp_tree()
    root.print_level()


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    test()
