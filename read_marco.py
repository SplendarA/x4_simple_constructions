import xml.etree.ElementTree as et
import os
import re
'''
独立脚本, 用于提取生成建筑模块的内部名称与中文对照
    1.对提取后的游戏文件的~/assets/structures下的
        buildmodule
        connectionmodules
		defence
		dock
		habitat
		processingmodule
		production
        storage
    进行查找, 获取其macros子文件夹下的所有XML文件
    例外: 
        buildmodule : 仅检测buildmodule+equip和buildmodule+ships开头的, 略过包含xen的
        defence     : 略过包含kha的
        dock        : 仅检测包含dockarea+station的, 和pier开头的
        
    2.获取其marco name与identification name
    3.marco_name即为内部模块名
    4.identification_name为"{表号.字串号}"形式的编号, 用于在~/t/0001-l086.xml中寻找对应翻译
    5.部分翻译可能仍为编号, 需要查找+拼接
'''
path_head = 'D:/X4mod/'
version_list = ['/', 'dlc_split/', 'dlc_terran/', 'dlc_pirate/']
dir_list = ['buildmodule', 'connectionmodules', 'defence', 'dock',
            'habitat', 'processingmodule', 'production', 'storage']
tfile_path = path_head + 't/0001-l086.xml'

class macros:
    macro = ''
    name = ''
    def __init__(self, macro_in, name_in):
        self.macro = macro_in
        self.name = name_in

def check_file_name(dirname, filename):
    '''
    检查是否读取该文件
    :param dirname: 上层目录名, 见dir_list
    :param filename: 要检查的文件名
    :return: True:读取 False:略过
    '''
    if dirname not in dir_list:
        return False
    if filename[-4:].lower() != '.xml':
        return False

    if dirname == 'buildmodule':
        pattern1 = '^buildmodule' + '.*' + 'equip' + '.*'
        pattern2 = '^buildmodule' + '.*' + 'ships' + '.*'
        if not re.match(pattern1, filename) and not re.match(pattern2, filename) or re.match('.*xen.*', filename):
            return False
    if dirname == 'defence':
        pattern1 = '.*' + 'kha' + '.*'
        if re.match(pattern1, filename):
            return False
    if dirname == 'dock':
        pattern1 = '^dockarea' + '.*' + 'station' + '.*'
        pattern2 = '^pier' + '.*'
        if not re.match(pattern1, filename) and not re.match(pattern2, filename):
            return False

    # 不符合条件的在之前已处理完毕
    return True

def loc_to_str(loc_in, t_path):
    '''
    将位标信息转化为可读字符串
    :param loc_in: 传入的坐标, 以"{表号.字串号}"形式组成
    :param t_path: t文件的路径
    :return:
    '''
    page_id = loc_in.split(',')[0][1:]
    str_id = loc_in.split(',')[1][:-1]
    tree1 = et.parse(t_path)
    root1 = tree1.getroot()
    for page in root1:
        if page.attrib['id'] == page_id:
            for ttt in page:
                if ttt.attrib['id'] == str_id:
                    return ttt.text


macro_list = []
for version in version_list:
    for dir_name in dir_list:
        # 拼接扫描路径
        scan_path = path_head + version + 'assets/structures/' +dir_name + '/macros'
        # 确认路径存在
        if not os.access(scan_path, os.F_OK):
            continue
        # 获取文件列表
        file_list = os.listdir(scan_path)
        # 遍历读取xml
        for file_name in file_list:
            file_path = scan_path + '/' + file_name
            # 检查文件是否符合规则
            if not check_file_name(dir_name, file_name):
                continue
            # 进行文件处理
            tree = et.parse(file_path)
            root = tree.getroot()
            # marco: root[0].attrib['name']
            # name: root[0][1][0].attrib['name']
            temp_macro = root[0].attrib['name']
            temp_name = root[0][1][0].attrib['name']

            # 需要循环转译
            while '{' in temp_name:
                # 去除括号内容, 提取{}内容
                temp_name = re.sub('\([\w\s]*\)', '', temp_name)
                loc_list = re.findall('{\d*.\d*}', temp_name)
                temp_str = ''
                for loc in loc_list:
                    temp_str = loc_to_str(loc, tfile_path)
                    temp_name = temp_name.replace(loc, temp_str)
            temp_name = re.sub('\(.*\)', '', temp_name)
            temp_macro = macros(temp_macro, temp_name)
            macro_list.append(temp_macro)

# 转换为xml
out_path = path_head + 'x4_xmlization_macros.xml'
out_root = et.Element('macros')
for i in range(len(macro_list)):
    et.SubElement(out_root, str(i), {'macro':macro_list[i].macro, 'name':macro_list[i].name})
with open(out_path, 'wb') as f_obj:
    f_obj.write(et.tostring(out_root, 'UTF-8', xml_declaration=True))