# ================================================================================
# This script generate the file list [file_index.txt] of E:\Video_Class
# ================================================================================
import os
import sys

ScriptPath = os.path.abspath(__file__)
ScriptDir = os.path.dirname(ScriptPath)

# import time
# for i in range(10):
#     time.sleep(0.5)
#     # print('\r', 'count:' + str(i), end='', flush=True)
#     sys.stdout.write('\rcount:' + str(i))

# ============================================================
# string list sort
# ============================================================


def StrListSort(str_list: list, dic_py: dict = None, dic_bh: dict = None):

    # Dict Init
    def dic_init(ref_fp: str) -> dict:
        dic = dict()
        with open(file=ref_fp, mode='r', encoding='UTF-8') as fh:
            lines = fh.read().splitlines()
            n = len(lines)
            for i in range(0, n - 1):
                # split and take record to dictionary
                tmpKey, tmpVal = lines[i].split('\t', 1)
                dic[tmpKey] = tmpVal

        return dic

    # Dict Search
    def dic_search(dic: dict, uchar: str) -> str:

        # find within ref list
        # if no item matches,
        # it should be an 0-9 or a-z char, keep original
        value = dic.get(uchar)
        if value == None:
            value = uchar
        return value

    # ==================================================
    # char compare
    # ==================================================
    def comp_char(charA: str, charB: str) -> int:
        if charA == charB:
            return -1
        pyA = dic_search(dic_py, charA)
        pyB = dic_search(dic_py, charB)
        if pyA > pyB:
            # charA > charB [order A > order B]
            return 1
        elif pyA < pyB:
            # charA < charB
            return 0
        else:
            bhA = dic_search(dic_bh, charA)
            bhB = dic_search(dic_bh, charB)
            if bhA >= bhB:
                return 1
            elif bhA < bhB:
                return 0

    # ==================================================
    # string compare
    # ==================================================
    def comp_str(strA: str, strB: str) -> int:
        # strA = A.encode('utf-8').decode('utf-8')
        # strB = B.encode('utf-8').decode('utf-8')

        n = min(len(strA), len(strB))
        i = 0
        while i < n:
            rst = comp_char(strA[i], strB[i])
            if rst == -1:
                # case for first N identical chars charA[i] == charB[i]
                i = i + 1
                if i == n:
                    if len(strA) > len(strB):
                        # strA > strB  [order A > order B]
                        rst = 1
                    else:
                        # strA < strB
                        rst = 0
            else:
                # case for first different
                # rst will be 1 charA[i] >= charB[i]
                #          or 0 charA[i] <  charB[i]
                break
        return rst

    #
    # Main Prog Start Here
    #

    # init two dicts
    if dic_py is None:
        fp = os.path.join(ScriptDir, 'ref_py.dat')
        dic_py = dic_init(ref_fp=fp)
    if dic_bh is None:
        fp = os.path.join(ScriptDir, 'ref_bh.dat')
        dic_bh = dic_init(ref_fp=fp)

    # sort and loop to each string
    # check each string from 2nd one
    # figure out if them can pop to from one by one
    n = len(str_list)
    disp_num = 100
    disp_interval = n/disp_num
    if disp_interval < 1:
        disp_interval = int(1)
    else:
        disp_interval = int(disp_interval)
    for i in range(1, n):
        if i % disp_interval == 0:
            sys.stdout.write(
                '\r -->> so far: {:5.2f}% {}/{}'.format(i/n*100, i, n))

        # main sort code
        tmp = str_list[i]
        j = i
        # jump out when first strList[j - 1] < tmp meet
        while j > 0 and comp_str(str_list[j - 1], tmp):
            # move all strings one step right when strList[j - 1] > tmp
            str_list[j] = str_list[j - 1]
            j -= 1
        # let tmp as the Nth string,
        # after while loop break:
        # case 1: tmp > str_list[j - 1], indicates [tmp] > some string original
        #         placed in front of her
        # case 2: j == 0, indicates: [tmp] is minimal than all her pioneers
        #
        # when whie bread, put current [tmp] to the new loc
        str_list[j] = tmp

    sys.stdout.write('\r -->> so far: {:5.2f}% {}/{}\n'.format(100, n, n))
    return str_list

# ============================================================
# test block
# ============================================================
if __name__ == '__main__':
    pc_path = 'E:\Video_Class'
    start_path = 'F:\D4T_to_D2T\Video_Class'

    rst_fp = os.path.join(pc_path, 'file_index.txt')

    item_lists = []

    for root, dirs, files in os.walk(top=start_path):
        for dir in dirs:
            # print(' Dir : {}'.format(os.path.join(root, dir)))
            item_lists.append(os.path.join(root, dir))
        for file in files:
            # print(' File: {}'.format(os.path.join(root, file)))
            item_lists.append(os.path.join(root, file))

    StrListSort(item_lists)

    with open(rst_fp, 'w', encoding='utf-8') as fp:
        fp.writelines('\n'.join(item_lists))


    print('ok')

    # for root, dirs, files in os.walk(top=start_path):
    #     for name in dirs:
    #         tempName = name
    #         if tempName in dirs_4_del:
    #             dirpath = os.path.join(root, name)
    #             tempStr = ' -> Del Dir: ' + dirpath
    #             print(tempStr)
    #             if not debug_mode:
    #                 shutil.rmtree(path=dirpath)
