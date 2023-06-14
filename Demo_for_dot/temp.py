import re


def md2dot2png():
    #     ## - define graph type
    #     listInfo = {
    #         'dot';
    #         'neato';
    #         'fdp';
    #         'sfdp';
    #         'twopi';
    #         };
    #     [selection, ok] = listdlg(...
    #         'Name', 'Graph Type Define:',...
    #         'PromptString', 'Select a Graph Type:',...
    #         'SelectionMode', 'single',...
    #         'ListString', listInfo);

    #     if ok == 0:
    #         warndlg('Please Define Plot Type');
    #         return;
    #     else:
    #         graphType = listInfo{selection}

    #     switch graphType
    #         case 'dot'
    #             dotContent = FuncGetTemplate4Doc();
    #         otherwise
    #             dotContent = FuncGetTemplate4NonDirStyle()
    #     end

    #     ## - use UI to get a file
    #     mdFileDir = 'E:\HuJi\WD\WDDot\20221108_广数复习题'
    #     FilterSpec = {...
    #         '*.md; *.mdx', 'MD Files (*.md, *.mdx)';
    #         };
    #     DialogTitle = 'Select A MD File'
    #     DefaultName = mdFileDir
    #     [FileName, PathName, FilterIndex] = uigetfile(FilterSpec, DialogTitle, DefaultName)

    #     if isnumeric(FileName)
    #         error('isnumeric(FileName)')

    #     mdFilePath = fullfile(PathName, FileName)

    # read *.md file




    dotContent = insert_node_to_each_level(dotContent, net_nodes, levelIDVector, plot_start_level, maxLevelNum)



#     ## Delete Marker
#     tfv = contains(dotContent, 'sytleDefineField') | contains(dotContent, 'streamFlow');
#     dotContent(tfv) = [];

#     ##  write 2 file
#     [~, ~, ext] = fileparts(mdFilePath);
#     oldPattern = ext;
#     newPattern = '.dot';
#     dotFilePath = strrep(mdFilePath, oldPattern, newPattern);
#     if exist(dotFilePath, 'file'):
#         delete(dotFilePath)

#     #  writing main procedure
#     fid = fopen(dotFilePath, 'w', 'n', 'UTF-8');
#     # fid = fopen(dotFilePath, 'w');
#     cellMat = dotContent;
#     for line = 1:length(cellMat)
#         tline = cellMat{line, 1};
#         fprintf(fid, '%s\r\n', tline)

#     fclose(fid);

#     ## png publish
#     optionStr = 'dotPath';
#     dot2png(optionStr, dotFilePath);

# ## insert to target
# def rst = FuncInsert2Content(sourceInfo, searchInfo, insertInfo):

#     tempTFV = strcmp(sourceInfo, char(searchInfo));
#     if sum(sum(tempTFV)) > 1:
#         error('sum(sum(tempTFV)) > 1')

#     k = find(tempTFV == true);
#     rst = [...
#         sourceInfo(1:(k - 1));...
#         insertInfo;...
#         sourceInfo(k:end);...
#         ];


## create linkage block
def FuncCreateLinkageBlock4Dot(masterInfo, slaveInfo):

    part01 = ['    {']

    part02 = ['    }', '    ->', '    {']

    part03 = ['    }[color = "black" arrowhead = "normal"];', '']

    # tfv = false(size(slaveInfo))
    # for i = 1:size(slaveInfo, 1):
    #     if isempty(slaveInfo{i, 1}):
    #         tfv(i, 1) = true

    # slaveInfo(tfv, :) = [];

    for i in range(len(slaveInfo)):
        slaveInfo[i] = ['        "', slaveInfo[i], '"']

    masterInfo[0] = ['        "' + masterInfo[0], '"']

    rst = part01 + masterInfo + part02 + slaveInfo + part03

    return rst


## create linkage block
def FuncCreateLinkageBlock4NonDirPlot(masterInfo, slaveInfo):

    rst = FuncCreateLinkageBlock4Dot(masterInfo, slaveInfo)
    rst = strrep(rst, '->', '--')
    return rst


















def get_node_set_by_level(nodes, level_vec, level):
    rst = []
    for lid, node in zip(level_vec, nodes):
        if lid == level:
            rst.append(node)
    return rst


def add_node_prefix(node: str):
    return ' ' * 8 + node


def insert_node_to_each_level(dotContent, nodes, level_vec, plot_start_level, maxLevelNum):
    ## inset label of each level to target template
    for i in range(plot_start_level, maxLevelNum + 1):
        # - for each level find sub set
        sourceCellMatrixSubSet = get_node_set_by_level(nodes, level_vec, i)

        # - insert to content
        sourceInfo = dotContent
        searchInfo = 'sytleDefineField' + str(i)
        insertInfo = [add_node_prefix(node) for node in sourceCellMatrixSubSet]
        dotContent = FuncInsert2Content(sourceInfo, searchInfo, insertInfo)

    return dotContent



def xxxxxxxxxx(levelIDVector, nodes, level_vec, maxLevelNum):
    ## insert linkage info to template
    # - end by row[n - 1]
    for i in range(1, maxLevelNum):

        tmp_master_nodes = get_node_set_by_level(nodes, level_vec, i)

        # # - init master-slave vector
        # tempMasterVector = false(size(levelIDVector))
        # tempSlaveVector = false(size(levelIDVector))

        # # - set master vector
        # tempMasterVector(i, 1) = true

        # # - figure out the slave vector
        # tempMasterVaule = levelIDVector(i)

        # if tempMasterVaule < plot_start_level:
        #     continue

        # for j = (i + 1):size(levelIDVector, 1):
        #     tempSlaveVaule = levelIDVector(j);

        #     if tempSlaveVaule == tempMasterVaule:
        #         # - if reach the next parallel master level or reach the end, break
        #         break;
        #     elif tempSlaveVaule == tempMasterVaule + 1:
        #         tempSlaveVector(j, 1) = true

        # ##
        # masterInfo = net_nodes(tempMasterVector);
        # slaveInfo = net_nodes(tempSlaveVector);

        # if ~isempty(slaveInfo):
        #     # -
        #     switch graphType
        #         case 'dot'
        #             tempBlock = FuncCreateLinkageBlock4Dot(masterInfo, slaveInfo);
        #         otherwise
        #             tempBlock = FuncCreateLinkageBlock4NonDirPlot(masterInfo, slaveInfo);
        #     end

        #     sourceInfo = dotContent
        #     searchInfo = 'streamFlow' + str(tempMasterVaule)
        #     insertInfo = tempBlock
        #     dotContent = FuncInsert2Content(sourceInfo, searchInfo, insertInfo)





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

class DocMd(DocBase):
    def __init__(self, fp:str) -> None:
        
        
        self.__data_raw:list[str] = self._file_2_list(fp=fp)

        self.__data_net:list[str] = []
        self.__lvl_info:list[int] = []


        self.__get_useful_line()
        self.__get_level_info()

        self.__lvl_max:int = max(self.__lvl_info)

        self.__lvl_limit = 18

        self.__lvl_chk()


        # remove the prefix
        self.__nodes = [self.__get_node_text(node) for node in self.__data_net]

        ## set start level
        plot_start_level = 1

        

        ## make unique
        # - update identical elements
        make_unique = True

        if make_unique:
            self.__make_node_unique()

    # ==================================================
    # __make_node_unique
    # ==================================================
    def __make_node_unique(self) -> list[str]:
        nodes = self.__nodes
        for i in range(len(nodes)):
            str0 = self.__get_node_text(nodes[i])
            for j in range((i + 1), len(nodes)):
                str1 = self.__get_node_text(nodes[j])
                if str0 == str1:
                    # add blank to make different
                    nodes[j] = nodes[j]+ ' '

    # ==================================================
    # __lvl_chk
    # ==================================================
    def __lvl_chk(self):
        if self.__lvl_max > self.__lvl_limit:
            info = 'lvl_max {} > lvl_limit {}'.format(self.__lvl_max, self.__lvl_limit)
            raise Exception('lvl_max > lvl_limit')

    # ==================================================
    # __lvl_chk
    # ==================================================
    def __get_node_text(self, node: str) -> str:
        pattern = '(^#+(\s))|((^\t*)(-\s))'
        return re.sub(pattern=pattern, repl='')

    # ==================================================
    # __get_useful_line
    # ==================================================
    def __get_useful_line(self)->list[str]:
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
    # __get_level_info
    # ==================================================
    def __get_level_info(self)->list[int]:
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




# ============================================================
# Test
# ============================================================

if __name__ == '__main__':

    md2dot2png()