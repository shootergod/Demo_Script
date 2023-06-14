import os
# import pyperclip
# str_raw = pyperclip.paste()


# str_raw="""

# In summary, we should keep firmly in mind that the crucial step in any finite element 
# analysis is always choosing an appropriate mathematical model since a finite element 
# solution solves only this model. Furthermore, the mathematical model must depend on the 
# analysis questions asked and should be reliable and effective (as defined. earlier). In the 
# process of analysis, the engineer has to judge whether the chosen mathematical model has 
# been solved to a sufficient accuracy and whether the chosen mathematical model was 
# appropriate (i.e. reliable) for the questions asked. Choosing the mathematical model, 
# solving the model by appropriate finite element procedures, and judging the results are the 
# fundamental ingredients of an engineering analysis using finite element methods. 

# """

CWD = os.path.dirname(__file__)

fn = 'Test_Mulit_Lines_2_One_Line_Str.txt'

fp = os.path.join(CWD, fn)
with open(file=fp, mode='r', encoding='utf-8') as fid:
    str_raw = fid.read()

sep_line = "="*64

newline_num_0 = str_raw.count('\n')

# key proc start
str_fin = str_raw.replace('\n', ' ')

print(str_fin.count('  '))
while str_fin.count('  '):
    print(str_fin.count('  '))
    str_fin = str_fin.replace('  ', ' ')


sb_num = str_fin.count('"')
if sb_num % 2 == 1:
    info = 'Special Symbol -> " Counted: {}'.format(sb_num)
    raise Exception(info)


newline_num_1 = str_fin.count('\n')

cmd_str = 'echo ' + str_fin + ' | clip'
os.system(cmd_str)
print(sep_line)
print('New Line Symbol # {} -> {}'.format(newline_num_0, newline_num_1))
print(sep_line)
print(str_fin)
print(sep_line)

