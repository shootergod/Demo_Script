#
# dot2png('last')
# dot2png('previousUIPath')
# dot2png('')
#

import os, subprocess, json

# ============================================================
# Constant
# ============================================================
CWD = os.path.dirname(__file__)

CONF_FP = os.path.join(CWD, 'conf.json')

OPT_LAST_DOT = 'last_file'


# ============================================================
# Class
# ============================================================
class Config():
    def __init__(self, fp: str = None) -> None:
        if not os.path.isfile(fp):
            info = 'Config Init Failed @ {}'.format(fp)
            raise Exception(info)

        self.__fp = fp
        self.__conf: dict = None

        self.__read_conf()

    def __read_conf(self):
        with open(self.__fp, 'r', encoding='utf-8') as fid:
            self.__conf = json.load(fid)

    def __put_conf(self):
        with open(self.__fp, 'w', encoding='utf-8') as fid:
            json.dump(self.__conf, fid, indent=4, sort_keys=True, ensure_ascii=False)

    def get_opt(self, opt_name: str):
        return self.__conf.get(opt_name)

    def set_opt(self, opt_name: str, opt_val):
        if opt_name in self.__conf:
            self.__conf[opt_name] = opt_val

            self.__put_conf()
        else:
            info = 'Invalid Key: {}'.format(opt_name)
            raise Exception(info)


# ============================================================
# Functions
# ============================================================
def dot2png(dot_fp: str = '', mode: str = 'gui'):

    dotFileDir = 'E:\HuJi\WD\WDDot'

    if dot_fp.endswith('.dot'):
        mode = 'dot_path'

        last_dir = os.path.dirname(dot_fp)
        last_file = os.path.basename(dot_fp)

        conf = Config(fp=CONF_FP)
        conf.set_opt(opt_name='last_dir', opt_val=last_dir)
        conf.set_opt(opt_name='last_file', opt_val=last_file)

    if mode == 'last':
        conf = Config(fp=CONF_FP)
        last_dir = conf.get_opt(opt_name='last_dir')
        last_file = conf.get_opt(opt_name='last_file')

        dot_fp = os.path.join(last_dir, last_file)

    elif mode == 'dot_path':
        pass
    else:
        info = 'Unknown Mode: {}'.format(mode)
        raise Exception(info)

    print('Mode = {}'.format(mode))
    png_fp = dot_fp.replace('.dot', '.png')

    dot2png_cmd(dot_fp, png_fp)


# ============================================================
# dot2png_cmd
# ============================================================
def dot2png_cmd(dot_fp, png_fp):
    #  graphType = varargin{1}
    #  switch graphType
    #      case 'dot'
    #          cmd_line = ['dot -Tpng "', dot_fp, '" -o ', png_fp]
    #      otherwise
    #          cmd_line = ['neato -Tpng "', dot_fp, '" -o ', png_fp]
    #          cmd_line = ['twopi -Tpng "', dot_fp, '" -o ', png_fp]
    #  end
    #  cmd_line = ['neato -Tpng "', dot_fp, '" -o ', png_fp]
    #  cmd_line = ['twopi -Tpng "', dot_fp, '" -o ', png_fp]
    cmd_line = ''.join(['dot -Tpng "', dot_fp, '" -o ', png_fp])

    print(cmd_line)

    # create png from dot
    ret = subprocess.run(cmd_line, shell=True)

    if ret.returncode != 0:
        print(ret.stderr)
        print('Dot 2 PNG Failed!')
    else:
        cmd_line = ''.join(['explorer /select, "', png_fp, '"'])
        print(cmd_line)
        subprocess.run(cmd_line, shell=True)

        # cmd_line = png_fp
        # subprocess.run(cmd_line, shell=True)
        print('Dot 2 PNG Succeed!')


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
        dot2png(mode='last')

    def btn_sel_new():
        conf = Config(fp=CONF_FP)
        last_dir = conf.get_opt(opt_name='last_dir')
        if not os.path.isdir(last_dir):
            last_dir = 'D:/'

        fp = fd.askopenfilename(title='Select a *.doc file.',
                                initialdir=last_dir)
        if fp:
            dot2png(dot_fp=fp.replace('/', '\\'))

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

    # fp = 'C:\\Users\\user\\Desktop\\ttt\\Simpack_GUI.dot'
    # dot2png(dot_fp=fp)

    # dot2png(mode='last')
