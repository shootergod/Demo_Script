# ============================================================
# Import
# ============================================================
import os, subprocess
from conf import Config

# ============================================================
# Constant
# ============================================================
CWD = os.path.dirname(__file__)



# ============================================================
# Functions
# ============================================================
def dot2png(dot_fp: str = '', mode: str = ''):

    # case 01: 
    if dot_fp.endswith('.dot'):
        mode = 'dot_path'

        last_dot_dir = os.path.dirname(dot_fp)
        last_dot_file = os.path.basename(dot_fp)
        # take record
        conf = Config()
        conf.set_opt(opt_name='last_dot_dir', opt_val=last_dot_dir)
        conf.set_opt(opt_name='last_dot_file', opt_val=last_dot_file)

    # case 02: resume last
    if mode == 'last':
        # take record
        conf = Config()
        last_dot_dir = conf.get_opt(opt_name='last_dot_dir')
        last_dot_file = conf.get_opt(opt_name='last_dot_file')

        dot_fp = os.path.join(last_dot_dir, last_dot_file)

    elif mode == 'dot_path':
        pass

    else:
        info = 'Unknown Mode: {}'.format(mode)
        raise Exception(info)

    # print('Mode = {}'.format(mode))
    png_fp = dot_fp.replace('.dot', '.png')

    console(dot_fp, png_fp)


# ============================================================
# console
# ============================================================
def console(dot_fp, png_fp):
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
    cmd_line = ''.join(['dot -Tpng "', dot_fp, '" -o "', png_fp, '"'])

    # print(cmd_line)

    # create png from dot
    ret = subprocess.run(cmd_line, shell=True)

    if ret.returncode != 0:
        print(ret.stderr)
        print('Dot 2 PNG Failed!')
    else:
        cmd_line = ''.join(['explorer /select, "', png_fp, '"'])
        # print(cmd_line)
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
        conf = Config()
        last_dot_dir = conf.get_opt(opt_name='last_dot_dir')
        if not os.path.isdir(last_dot_dir):
            last_dot_dir = 'D:/'

        fp = fd.askopenfilename(title='Select a *.dot file.',
                                initialdir=last_dot_dir)
        if fp and fp.endswith('.dot'):
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

    # commad line 01:
    # fp = 'C:\\Users\\user\\Desktop\\ttt\\Simpack_GUI.dot'
    # dot2png(dot_fp=fp)

    # commad line 01:
    # dot2png(mode='last')
