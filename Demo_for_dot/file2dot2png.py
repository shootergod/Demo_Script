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

OPT_DIR = 'last_file_dir'
OPT_FILE = 'last_file_file'

FILE_TYPES = ('.txt', '.md')

COLOR_SCHEME_0 = Config(fp=CS_FP).get_opt('COLOR_SCHEME_0')
COLOR_SCHEME_TRELLO = Config(fp=CS_FP).get_opt('COLOR_SCHEME_TRELLO')
COLOR_SCHEME_IOS = Config(fp=CS_FP).get_opt('COLOR_SCHEME_IOS')

COLOR_SCHEME_USE = COLOR_SCHEME_0


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
class DocGeneric(DocBase):
    LABEL_FIELD = 'label_define_field_'
    LINKAGE_FIELD = 'linkage_define_field_'

    def __init__(self, fp: str) -> None:

        self._fp = fp

        self._dot_data: list[str] = []

        self._data_raw: list[str] = []
        self._data_net: list[str] = []

        self._nodes: list[str] = []

        self._lvl_info: list[int] = []
        self._lvl_max: int = 0
        self._lvl_limit: int = 18

        self._tree: Tree = None

        ## set start level
        self.plot_start_level = 1

        ## make unique
        # - update identical elements
        self._make_unique = True

        # ========================================
        # init funcs
        # ========================================
        self._collect_init_info()
        # after collect, the rest of two steps handover to sub-class:
        # 1. make graph raw info clearn [sub-class must implemented].
        # 2. call 'create_graph' in base-class to create final graph.

    # ============================================================
    # phase 0 funcs
    # ============================================================

    # ==================================================
    # _get_dot_template
    # ==================================================
    def _get_dot_template(self):
        self._dot_data = self._file_2_list(
            fp=os.path.join(CWD, 'template_dot.txt'))

    # ==================================================
    # _get_graph_raw_data
    # ==================================================
    def _get_graph_raw_data(self):
        self._data_raw = self._file_2_list(fp=self._fp)

    # ==================================================
    # _collect_init_info
    # ==================================================
    def _collect_init_info(self):
        self._get_dot_template()
        self._get_graph_raw_data()

    # ============================================================
    # phase 3 funcs
    # ============================================================

    # ==================================================
    # _get_nodes
    # ==================================================
    def _get_nodes(self):
        self._nodes = [line.lstrip(' ') for line in self._data_net]

    # ==================================================
    # _make_node_unique
    # ==================================================
    def _make_node_unique(self) -> list[str]:
        nodes = self._nodes
        for i in range(len(nodes)):
            str0 = nodes[i]
            for j in range((i + 1), len(nodes)):
                str1 = nodes[j]
                if str0 == str1:
                    # add blank to make different
                    nodes[j] = nodes[j] + ' '

    # ==================================================
    # _add_double_quot
    # ==================================================
    def _add_double_quot(self) -> list[str]:
        nodes = self._nodes
        for i in range(len(nodes)):
            nodes[i] = '"' + nodes[i] + '"'

    # ==================================================
    # _get_lvl_info
    # ==================================================
    def _get_lvl_info(self) -> list[int]:
        self._lvl_info.clear()
        for line in self._data_net:
            bn = len(line) - len(line.lstrip(' '))
            tmp_lvl = int((bn + 4) / 4)
            self._lvl_info.append(tmp_lvl)

    # ==================================================
    # _get_lvl_max
    # ==================================================
    def _get_lvl_max(self):
        self._lvl_max = max(self._lvl_info)

    # ==================================================
    # _lvl_chk
    # ==================================================
    def _lvl_chk(self):
        if self._lvl_max > self._lvl_limit:
            info = 'lvl_max {} > lvl_limit {}'.format(self._lvl_max,
                                                      self._lvl_limit)
            raise Exception(info)

    # ==================================================
    # helpers
    # ==================================================
    def __get_nodes_by_level(self, level: int) -> list[str]:
        rst = []
        for lid, node in zip(self._lvl_info, self._nodes):
            if lid == level:
                rst.append(node)
        return rst

    def __add_node_prefix(self, node: str):
        return ' ' * 8 + node

    def __insert_content(self, loc: str, data: list[str]):
        lines = self._dot_data
        if loc in lines:
            rid = lines.index(loc)
            self._dot_data = lines[:rid] + data + lines[rid:]

    # ==================================================
    # _insert_node_to_each_level
    # ==================================================
    def _insert_node_to_each_level(self):
        # inset label of each level to target template
        for i in range(self.plot_start_level, self._lvl_max + 1):
            # - for each level find sub set
            nodes = self.__get_nodes_by_level(i)

            # - insert to content
            loc = DocGeneric.LABEL_FIELD + str(i)
            data = [self.__add_node_prefix(node) for node in nodes]

            self.__insert_content(loc=loc, data=data)

    # ==================================================
    # _create_graph_tree
    # ==================================================
    def _create_graph_tree(self) -> list[int]:
        root = None
        masters: list[Tree] = []
        for lvl, label in zip(self._lvl_info, self._nodes):
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

        self._tree = root

    # ==================================================
    # helpers
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
    # _insert_linkage_block_to_each_level
    # ==================================================
    def _insert_linkage_block_to_each_level(self):

        nodes = self._tree.traverse()
        for node in nodes:
            node_lvl = node.get_level()
            if node_lvl < self.plot_start_level:
                continue

            if node.has_children():
                label_m = [node.get_name()]
                label_s = [item.get_name() for item in node.get_children()]
                data = self.__create_linkage_block_4_dir_plot(node_m=label_m,
                                                              node_s=label_s)
                loc = DocGeneric.LINKAGE_FIELD + str(node_lvl)
                self.__insert_content(loc=loc, data=data)

    def _remove_bookmark(self):
        for ind, line in enumerate(self._dot_data):
            if line.startswith(DocGeneric.LABEL_FIELD) or line.startswith(
                    DocGeneric.LINKAGE_FIELD):
                self._dot_data[ind] = ''

    def _update_color_scheme(self):
        pat = "#[0-9a-f]{6}"
        color_len = len(COLOR_SCHEME_USE)
        color_counter = -1

        for ind, line in enumerate(self._dot_data):
            if re.search(pattern=pat, string=line):
                color_counter += 1
                color_tmp = COLOR_SCHEME_USE[color_counter % color_len]
                self._dot_data[ind] = re.sub(pattern=pat,
                                             repl=color_tmp,
                                             string=line)

    # ==================================================
    # write_dot_file
    # ==================================================
    def write_dot_file(self) -> str:

        self._get_nodes()
        if self._make_unique:
            self._make_node_unique()

        self._add_double_quot()

        self._get_lvl_info()
        self._get_lvl_max()
        self._lvl_chk()

        self._insert_node_to_each_level()
        self._create_graph_tree()
        self._insert_linkage_block_to_each_level()
        self._remove_bookmark()
        self._update_color_scheme()

        f_ext = os.path.splitext(os.path.basename(self._fp))[1]
        dot_fp = self._fp.replace(f_ext, '.dot')
        self._list_2_file(fp=dot_fp, data=self._dot_data)

        print('Md 2 Dot Succeed!')
        return dot_fp

    # ============================================================
    # Interface funcs
    # ============================================================

    # ==================================================
    # _get_useful_line
    # ==================================================
    def _get_useful_line(self) -> list[str]:
        raise NotImplementedError

    # ==================================================
    # _transform_to_std_model
    # ==================================================
    def _transform_to_std_model(self) -> list[int]:
        raise NotImplementedError


# ============================================================
# Class
# ============================================================
class DocMd(DocGeneric):
    def __init__(self, fp: str) -> None:
        super().__init__(fp=fp)

        # ========================================
        # init funcs
        # ========================================
        self._get_useful_line()
        self._transform_to_std_model()

    # ==================================================
    # _get_useful_line
    # ==================================================
    def _get_useful_line(self) -> list[str]:
        # get the net info [remove unwanted lines]
        # - xmind to md will like:
        # # L1
        # ## L2
        # ### L3
        # - L4
        # 	- L5
        # 		- L6

        self._data_net.clear()

        pattern = '(^#+(\s))|((^\t*)(-\s))'
        for line in self._data_raw:
            if re.match(pattern=pattern, string=line):
                self._data_net.append(line)

    # ==================================================
    # _transform_to_std_model
    # ==================================================
    def _transform_to_std_model(self) -> list[int]:
        ptn_1 = '^#+(\s)'
        ptn_2 = '((^\t+)(-\s))|(^-\s)'

        for ind, line in enumerate(self._data_net):
            is_matched = False
            # case 1: level 1~3
            if re.match(pattern=ptn_1, string=line):
                matchStr = re.match(pattern=ptn_1, string=line).group()
                # '# ' '## ' '### '
                tmp_lvl = matchStr.count('#')
                is_matched = True

            # case 2: level 4~N
            if re.match(pattern=ptn_2, string=line):
                matchStr = re.match(pattern=ptn_2, string=line).group()
                # 0 tab will be level 4, so offset here
                tmp_lvl = matchStr.count('\t') + 4
                is_matched = True

            if is_matched:
                tmp_repl = ' ' * (4 * (tmp_lvl - 1))
                line = line.replace(matchStr, tmp_repl)
                self._data_net[ind] = line

        self._list_2_file(fp=self._fp + '.chk', data=self._data_net)


# ============================================================
# Class
# ============================================================
class DocTxt(DocGeneric):
    def __init__(self, fp: str) -> None:
        super().__init__(fp=fp)

        # ========================================
        # init funcs
        # ========================================
        self._get_useful_line()
        self._transform_to_std_model()

    # ==================================================
    # _get_useful_line
    # ==================================================
    def _get_useful_line(self) -> list[str]:
        # txt is alway treated as std model, so nothing to do here
        self._data_net.clear()
        self._data_net = self._data_raw.copy()

    # ==================================================
    # _transform_to_std_model
    # ==================================================
    def _transform_to_std_model(self) -> list[int]:
        # txt is alway treated as std model, so nothing to do here
        self._list_2_file(fp=self._fp + '.chk', data=self._data_net)


# ============================================================
# file2dot2png
# ============================================================
def file2dot2png(fp: str = '', mode: str = ''):

    # case: resume last -> get the last file info
    if mode == 'last':
        # get record
        conf = Config(fp=CONF_FP)
        last_md_dir = conf.get_opt(opt_name=OPT_DIR)
        last_md_file = conf.get_opt(opt_name=OPT_FILE)
        fp = os.path.join(last_md_dir, last_md_file)

    # check if is a right type
    if fp.endswith(FILE_TYPES):
        # take record
        last_md_dir = os.path.dirname(fp)
        last_md_file = os.path.basename(fp)

        conf = Config(fp=CONF_FP)
        conf.set_opt(opt_name=OPT_DIR, opt_val=last_md_dir)
        conf.set_opt(opt_name=OPT_FILE, opt_val=last_md_file)
    else:
        info = 'Unknown File Type: {}'.format(fp)
        raise Exception(info)

    # md -> dot
    if fp.endswith('.txt'):
        doc_obj = DocTxt(fp=fp)
    elif fp.endswith('.md'):
        doc_obj = DocMd(fp=fp)

    # dot -> png
    dot_fp = doc_obj.write_dot_file()

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
        file2dot2png(mode='last')

    def btn_sel_new():
        conf = Config(fp=CONF_FP)
        last_md_dir = conf.get_opt(opt_name=OPT_DIR)
        if not os.path.isdir(last_md_dir):
            last_md_dir = 'D:/'

        t_info = 'Select a *.' + str(FILE_TYPES) + ' file.'
        fp = fd.askopenfilename(title=t_info,
                                initialdir=last_md_dir)
        if fp and fp.endswith(FILE_TYPES):
            file2dot2png(fp=fp.replace('/', '\\'))

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

    unique_v = tk.IntVar()
    chk_0 = tk.Checkbutton(root,
                           text='Unique',
                           bg=blue,
                           variable=unique_v,
                           font=fontStyle)

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

    chk_0.pack()
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