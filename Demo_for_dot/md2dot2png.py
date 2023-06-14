# ============================================================
# Doc Info
# ============================================================
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   md2dot2png.py
@Time    :   2023/06/20 09:14:41
@Author  :   HuJi
@Contact :   shootergod@forxmail.com
@Version :   1.0
@Desc    :   None
'''

# ============================================================
# Import
# ============================================================
import os, re
from tree import Tree
from conf import Config
from dot2png import dot2png

# ============================================================
# Constant
# ============================================================
CWD = os.path.dirname(__file__)

# conf path of prog param
CONF_FP = os.path.join(CWD, 'conf.json')
# conf path of color scheme
CS_FP = os.path.join(CWD, 'color_scheme.json')

OPT_DIR = 'last_md_dir'
OPT_FILE = 'last_md_file'

COLOR_SCHEME_0 = Config(fp=CS_FP).get_opt('COLOR_SCHEME_0')
COLOR_SCHEME_TRELLO = Config(fp=CS_FP).get_opt('COLOR_SCHEME_TRELLO')
COLOR_SCHEME_IOS = Config(fp=CS_FP).get_opt('COLOR_SCHEME_IOS')

COLOR_SCHEME_USE = COLOR_SCHEME_IOS



# ============================================================
# class
# ============================================================
class DocBase():
    # ==================================================
    # __init__
    # ==================================================
    def __init__(self) -> None:
        pass

    # ==================================================
    # _file_2_list
    # ==================================================
    def _file_2_list(self,
                     fp: str,
                     encoding='utf-8',
                     verbose=True) -> list[str]:
        if verbose:
            print('Reading Txt File: {}'.format(fp))
        with open(file=fp, mode='r', encoding=encoding) as fid:
            # file_data = fid.readlines()
            return fid.read().splitlines()

    # ==================================================
    # _list_2_file
    # ==================================================
    def _list_2_file(self,
                     fp: str,
                     data: list,
                     mode='w',
                     encoding='utf-8',
                     newline='\n',
                     verbose=True):
        if verbose:
            print('Writing Txt File: {}'.format(fp))
        with open(file=fp, mode=mode, encoding=encoding,
                  newline=newline) as fid:
            fid.write('\n'.join(data))


# ============================================================
# Class
# ============================================================
class DocMd(DocBase):
    LABEL_FIELD = 'label_define_field_'
    LINKAGE_FIELD = 'linkage_define_field_'

    def __init__(self, fp: str) -> None:

        self.__md_fp = fp

        self.__dot_data: list[str] = []

        self.__data_raw: list[str] = []
        self.__data_net: list[str] = []

        self.__nodes: list[str] = []

        self.__lvl_info: list[int] = []
        self.__lvl_max: int = 0
        self.__lvl_limit: int = 18

        self.__tree: Tree = None

        # ========================================
        # init funcs
        # ========================================
        self.__get_dot_template()
        self.__get_md_data()
        self.__get_useful_line()
        self.__get_nodes()

        ## make unique
        # - update identical elements
        make_unique = False
        if make_unique:
            self.__make_node_unique()

        self.__add_double_quot()

        self.__get_lvl_info()
        self.__get_lvl_max()
        self.__lvl_chk()

        ## set start level
        self.plot_start_level = 1

        self.__insert_node_to_each_level()

        self.__create_graph_tree()

        self.__insert_linkage_block_to_each_level()

        self.__remove_bookmark()

        self.__update_color_scheme()

    # ==================================================
    # __get_doc_template
    # ==================================================
    def __get_dot_template(self):
        self.__dot_data = self._file_2_list(
            fp=os.path.join(CWD, 'template_dot.txt'))

    # ==================================================
    # __get_md_data
    # ==================================================
    def __get_md_data(self):
        self.__data_raw = self._file_2_list(fp=self.__md_fp)

    # ==================================================
    # __get_useful_line
    # ==================================================
    def __get_useful_line(self) -> list[str]:
        # get the net info [remove unwanted lines]
        # - xmind to md will like:
        # # L1
        # ## L2
        # ### L3
        # - L4
        # 	- L5
        # 		- L6

        self.__data_net.clear()

        pattern = '(^#+(\s))|((^\t*)(-\s))'

        for line in self.__data_raw:
            if re.match(pattern=pattern, string=line):
                self.__data_net.append(line)

    # ==================================================
    # __get_node_text
    # ==================================================
    def __get_node_text(self, node: str) -> str:
        pattern = '(^#+(\s))|((^\t*)(-\s))'
        return re.sub(pattern=pattern, repl='', string=node)

    # ==================================================
    # __get_nodes
    # ==================================================
    def __get_nodes(self):
        self.__nodes = [self.__get_node_text(node) for node in self.__data_net]

    # ==================================================
    # __make_node_unique
    # ==================================================
    def __make_node_unique(self) -> list[str]:
        nodes = self.__nodes
        for i in range(len(nodes)):
            str0 = nodes[i]
            for j in range((i + 1), len(nodes)):
                str1 = nodes[j]
                if str0 == str1:
                    # add blank to make different
                    nodes[j] = nodes[j] + ' '

    # ==================================================
    # __add_double_quot
    # ==================================================
    def __add_double_quot(self) -> list[str]:
        nodes = self.__nodes
        for i in range(len(nodes)):
            nodes[i] = '"' + nodes[i] + '"'

    # ==================================================
    # __get_lvl_info
    # ==================================================
    def __get_lvl_info(self) -> list[int]:
        self.__lvl_info.clear()

        ptn_1 = '^#+(\s)'
        ptn_2 = '((^\t+)(-\s))|(^-\s)'

        for line in self.__data_net:

            # case 1: level 1~3
            if re.match(pattern=ptn_1, string=line):
                matchStr = re.match(pattern=ptn_1, string=line).group()

                tmp_lvl = matchStr.count('#')

            # case 2: level 4~N
            if re.match(pattern=ptn_2, string=line):
                matchStr = re.match(pattern=ptn_2, string=line).group()
                # 0 tab will be level 4, so offset here
                tmp_lvl = matchStr.count('\t') + 4

            self.__lvl_info.append(tmp_lvl)

    # ==================================================
    # __get_lvl_max
    # ==================================================
    def __get_lvl_max(self):
        self.__lvl_max = max(self.__lvl_info)

    # ==================================================
    # __lvl_chk
    # ==================================================
    def __lvl_chk(self):
        if self.__lvl_max > self.__lvl_limit:
            info = 'lvl_max {} > lvl_limit {}'.format(self.__lvl_max,
                                                      self.__lvl_limit)
            raise Exception(info)

    # ==================================================
    # __get_nodes_by_level
    # ==================================================
    def __get_nodes_by_level(self, level: int) -> list[str]:
        rst = []
        for lid, node in zip(self.__lvl_info, self.__nodes):
            if lid == level:
                rst.append(node)
        return rst

    def __add_node_prefix(self, node: str):
        return ' ' * 8 + node

    def __insert_content(self, loc: str, data: list[str]):
        lines = self.__dot_data
        if loc in lines:
            rid = lines.index(loc)
            self.__dot_data = lines[:rid] + data + lines[rid:]

    # ==================================================
    # __insert_node_to_each_level
    # ==================================================
    def __insert_node_to_each_level(self):
        # inset label of each level to target template
        for i in range(self.plot_start_level, self.__lvl_max + 1):
            # - for each level find sub set
            nodes = self.__get_nodes_by_level(i)

            # - insert to content
            loc = DocMd.LABEL_FIELD + str(i)
            data = [self.__add_node_prefix(node) for node in nodes]

            self.__insert_content(loc=loc, data=data)

    # ==================================================
    # __create_graph_tree
    # ==================================================
    def __create_graph_tree(self) -> list[int]:
        root = None
        masters: list[Tree] = []
        for lvl, label in zip(self.__lvl_info, self.__nodes):
            if lvl == 1:
                # case 01: special for 1st node [root node]
                # add node
                root = Tree(data=label)
                # update master
                if len(masters) < lvl:
                    masters.append(None)
                masters[lvl - 1] = root
            else:
                # case 02: normal nodes
                # get parent node
                master_lvl = lvl - 2
                cur_master = masters[master_lvl]
                # add node
                tmp_node = Tree(data=label)
                cur_master.add_node(tmp_node)
                # update master
                if len(masters) < lvl:
                    masters.append(None)
                masters[lvl - 1] = tmp_node

        self.__tree = root

    # ==================================================
    # __create_linkage_block_4_dir_plot
    # ==================================================
    def __create_linkage_block_4_dir_plot(self, node_m, node_s) -> list[str]:
        part01 = ['    {']
        part02 = ['    }' + '    ->' + '    {']
        part03 = ['    }[color = "black" arrowhead = "normal"];']

        for i in range(len(node_s)):
            node_s[i] = ' ' * 8 + node_s[i]
        node_m[0] = ' ' * 8 + node_m[0]

        rst = part01 + node_m + part02 + node_s + part03
        return rst

    def __create_linkage_block_4_non_dir_plot(self, node_m,
                                              node_s) -> list[str]:
        rst = self.__create_linkage_block_4_dir_plot(node_m, node_s)
        rst = [line.replace('->', '--') for line in rst]
        return rst

    # ==================================================
    # __insert_linkage_block_to_each_level
    # ==================================================
    def __insert_linkage_block_to_each_level(self):

        nodes = self.__tree.traverse()
        for node in nodes:
            node_lvl = node.get_level()
            if node_lvl < self.plot_start_level:
                continue

            if node.has_children():
                label_m = [node.get_name()]
                label_s = [item.get_name() for item in node.get_children()]
                data = self.__create_linkage_block_4_dir_plot(node_m=label_m,
                                                              node_s=label_s)
                loc = DocMd.LINKAGE_FIELD + str(node_lvl)
                self.__insert_content(loc=loc, data=data)

    def __remove_bookmark(self):
        for ind, line in enumerate(self.__dot_data):
            if line.startswith(DocMd.LABEL_FIELD) or line.startswith(
                    DocMd.LINKAGE_FIELD):
                self.__dot_data[ind] = ''

    def __update_color_scheme(self):
        pat = "#[0-9a-f]{6}"
        color_len = len(COLOR_SCHEME_USE)
        color_counter = -1

        for ind, line in enumerate(self.__dot_data):
            if re.search(pattern=pat, string=line):
                color_counter += 1
                color_tmp = COLOR_SCHEME_USE[color_counter % color_len]
                self.__dot_data[ind] = re.sub(pattern=pat,
                                              repl=color_tmp,
                                              string=line)

    def write_dot_file(self) -> str:
        dot_fp = self.__md_fp.replace('.md', '.dot')
        self._list_2_file(fp=dot_fp, data=self.__dot_data)
        return dot_fp


# ============================================================
# md2dot2png
# ============================================================
def md2dot2png(md_fp: str = '', mode: str = ''):

    # case 01:
    if md_fp.endswith('.md'):
        mode = 'md_path'

        last_md_dir = os.path.dirname(md_fp)
        last_md_file = os.path.basename(md_fp)
        # take record
        conf = Config(fp=CONF_FP)
        conf.set_opt(opt_name=OPT_DIR, opt_val=last_md_dir)
        conf.set_opt(opt_name=OPT_FILE, opt_val=last_md_file)

    # case 02: resume last
    if mode == 'last':
        # take record
        conf = Config(fp=CONF_FP)
        last_md_dir = conf.get_opt(opt_name=OPT_DIR)
        last_md_file = conf.get_opt(opt_name=OPT_FILE)

        md_fp = os.path.join(last_md_dir, last_md_file)

    elif mode == 'md_path':
        pass

    else:
        info = 'Unknown Mode: {}'.format(mode)
        raise Exception(info)

    # md -> dot -> png
    md_obj = DocMd(fp=md_fp)
    dot_fp = md_obj.write_dot_file()

    dot2png(dot_fp=dot_fp)


# ============================================================
# gui_launcher
# ============================================================
def gui_launcher():
    import tkinter.filedialog as fd
    import tkinter as tk
    import tkinter.font as tkFont

    # ==================================================
    # callbacks
    # ==================================================
    def btn_run_last():
        md2dot2png(mode='last')

    def btn_sel_new():
        conf = Config(fp=CONF_FP)
        last_md_dir = conf.get_opt(opt_name=OPT_DIR)
        if not os.path.isdir(last_md_dir):
            last_md_dir = 'D:/'

        fp = fd.askopenfilename(title='Select a *.md file.',
                                initialdir=last_md_dir)
        if fp and fp.endswith('.md'):
            md2dot2png(md_fp=fp.replace('/', '\\'))

    # ==================================================
    # gui_launcher
    # ==================================================
    root = tk.Tk()
    sc_w = root.winfo_screenwidth()
    sc_h = root.winfo_screenheight()
    win_w = 400
    win_h = 300
    x = int((sc_w - win_w) / 2)
    y = int((sc_h - win_h) / 2)
    win_pos = '{}x{}+{}+{}'.format(win_w, win_h, x, y)
    root.geometry(win_pos)

    fontStyle = tkFont.Font(family="Calibri", size=48)

    # ==================================================
    # components
    # ==================================================
    blue = '#0099e5'
    red = '#ff4c4c'

    btn_0 = tk.Button(root,
                      text='Run Last',
                      bg=blue,
                      command=btn_run_last,
                      font=fontStyle)
    btn_1 = tk.Button(root,
                      text='Select New',
                      bg=red,
                      command=btn_sel_new,
                      font=fontStyle)
    btn_0.pack(fill=tk.X)
    btn_1.pack(fill=tk.BOTH, expand=tk.TRUE)

    btn_0.focus()

    # ==================================================
    # loop
    # ==================================================
    root.mainloop()


# ============================================================
# Test
# ============================================================
if __name__ == '__main__':
    gui_launcher()

    # # command line:
    # md_fp = r'C:\Users\user\Desktop\ttt\积分器设置.md'
    # md_obj = DocMd(fp=md_fp)
    # dot_fp = md_obj.write_dot_file()
    # dot2png(dot_fp=dot_fp)