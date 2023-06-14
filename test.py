import os  
import glob  
  
# 指定要处理的文件夹路径  
folder_path = r'C:\Users\user\Desktop\nes_wudi_itmop.com\无敌nes游戏精选'  
  
# 指定要添加的前缀  
prefix = 'huji_'  
  
# 使用glob模块遍历文件夹下的所有文件 
count = 0 
for filename in glob.glob(os.path.join(folder_path, '*')):  
    # 获取文件名（不包括路径）  
    filename = os.path.basename(filename)  
    # 添加前缀并重命名文件  
    count += 1
    if len(str(count)) == 1:
        ind = '00' + str(count) + '_'
    elif len(str(count)) == 2:
        ind = '0' + str(count) + '_'
    fp0 = os.path.join(folder_path, filename)
    fp1 = os.path.join(folder_path, prefix + ind + filename)
    os.rename(fp0, fp1)