import xml.etree.ElementTree as et
import xml_modu
import os
import re

'''
WIP!!!!

'''
# xml_path = 'D:/X4mod/t/0001-l086.xml'
# tree = et.parse(xml_path)
# f_root = tree.getroot()
# plan0 = f_root[0]
# print(plan0[0].attrib['id'])
# print(plan0[0].text)
# os.chdir('D:/X4mod/assets/structures/')
# print(os.access('D:/X4mod/assets/structuresd/', os.F_OK))

str1 = 'buildmodule_xen_equip_macro.xml'
pattern1 = '.*xen.*'
pattern2 = 'buildmodule' + '.*' + 'ships'
print(re.match(pattern1, str1))