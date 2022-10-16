import xml.etree.ElementTree as et
import xml_modu
import os
import re



'''
WIP!!!!
根据蓝图文件, 蓝图结构如下:
    root: plans
        plan: id, name, description                 # id需要随机生成, name由玩家指定, description随意, plan可有多个
            patches:                                # 无需手动添加
                patch: extension, version, name     
            entry: index, macro                     # 模块实体, 需要生成的部分
                offset: x, y, z
                rotation: yaw, roll, pitch
'''




class entry:
    index = ''
    macro = ''
    position = {'x':'0', 'y':'0', 'z':'0'}
    rotation = {'yaw':'0'}

class plan:
    plan_id = ''
    plan_name = ''
    plan_description = ''
    entry_list = []

    def __init__(self, id='', name='', description=''):
        self.plan_id = id
        self.plan_name = name
        self.plan_description = description

    # 添加模块, 需要根据不同情况调用不同添加方式
    def add_entry(self, entry_to_be_added):
        '''
        不同模块的处理逻辑:
            entry.macro以'_'做split, 取[0]用以辨别:

            添加至中心点:
                模块: connectionmodules, defence, habitat, processingmodule, production, storage
            四周分布:
                模块: dock(pier)
                特征: [0] == pier, 名字中有1x或2x
                处理: 仅允许E型泊位4X2摆放, 一次摆放一层
                     摆放逻辑:
                        preset_xzyaw = [{'x':'-9200', 'z':'-5400', 'yaw':'0'},
                                        {'x':'-9200', 'z':'5400', 'yaw':'0'},
                                        {'x':'-5400', 'z':'9200', 'yaw':'90'},
                                        {'x':'5400', 'z':'9200', 'yaw':'90'},
                                        {'x':'9200', 'z':'5400', 'yaw':'180'},
                                        {'x':'9200', 'z':'-5400', 'yaw':'180'},
                                        {'x':'5400', 'z':'-9200', 'yaw':'270'},
                                        {'x':'-5400', 'z':'-9200', 'yaw':'270'},
                        ]
                        按照如上preset进行摆放, 由底边y = -9800开始, 按2200的间距逐层摆放
            内环分布:
                模块: dock(S/M停机坪), buildmodules(S/M建造维护模块)
                特征: [0] == pier, [2] == m
                     [0] == buildmodules, [3] == s/m
                处理: 均按照s/m制造港的长宽摆放
                     摆放逻辑:
                        将单个模块摆放区域试做一个800*800*800的区域, 在各轴|1600| ~ |8000|范围内摆放
                        最终分为20*20-4=396个单元, 仅提供y='-9600'一层用作摆放, 已完全可以满足需求
            横排分布:
                模块: buildmodule(l及xl)
                特征: [0] == buildmodules, [3] == l/xl





        '''
        pass


