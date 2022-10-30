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

class blocks:
    """
    区块类, 用于在程序活动期间记录蓝图位置信息
    区块包括:
        prod, pier, dock, xl, l
    """
    class gen_block:
        type = ''  # 区块类型
        cent_loc = {'x': 0, 'y': 0, 'z': 0}  # 区块中心点坐标
        rotation = {'yaw': 0, 'roll': 0, 'pitch': 0}  # 区块内建筑模块需要的偏转角
        inner_loc = {'row': 0, 'col': 0, 'layer': 0}  # 内部行列
        macro = []  # 区块下属建筑模块, 大部分具有排他性, 除prod外
        def __init__(self, **kwargs):
            self.type = kwargs['type']
            self.cent_loc = kwargs['cent_loc'].copy()
            self.rotation = kwargs['rotation'].copy()
            self.inner_loc = kwargs['inner_loc'].copy()

    prod_blocks = []
    pier_blocks = []
    dock_blocks = []
    xl_blocks = []
    l_blocks = []
    # pier模块行列号与旋转角度的映射表
    ref_pier_yaw = {'00': 90, '01': 90, '10': 0, '20': 0, '11': 180, '21': 180, '30': 270, '31': 270}
    def __init__(self):
        """
        主要完成预设区块的初始化
        """
        # 初始化prod生产区块
        self.prod_blocks.append(self.gen_block(type='prod', cent_loc={'x': 0, 'y': -8400, 'z': 0},
                                               rotation={'yaw': 0, 'roll': 0, 'pitch': 0},
                                               inner_loc={'row': 0, 'col': 0, 'layer': 0}))

        # 初始化pier泊位区块
        tmp_type = 'pier'
        tmp_cent_loc = {}
        tmp_rotation = {}
        tmp_layer = 0
        for layer in range(4):
            for row in range(4):
                for col in range(2):
                    if row % 3 == 0:  # 0和3
                        tmp_cent_loc['x'] = (2 * col - 1) * 5000
                        tmp_cent_loc['z'] = (1 - row // 3 * 2) * 9200
                    else:  # 1和2
                        tmp_cent_loc['x'] = (2 * col - 1) * 9200
                        tmp_cent_loc['z'] = (3 - 2 * row) * 5000
                    tmp_cent_loc['y'] = -9800 + layer * 2200

                    tmp_yaw = self.ref_pier_yaw[str(row) + str(col)]
                    tmp_rotation['yaw'] = tmp_yaw
                    tmp_rotation['roll'] = 0
                    tmp_rotation['pitch'] = 0

                    tmp_inner_loc = {'row': row, 'col': col, 'layer': tmp_layer}

                    tmp_layer = layer

                    self.pier_blocks.append(self.gen_block(type=tmp_type, cent_loc=tmp_cent_loc,
                                                           rotation=tmp_rotation,
                                                           inner_loc=tmp_inner_loc))

        # 初始化dock小型泊位模块(包含同级建造维护模块)
        tmp_type = 'dock'
        tmp_cent_loc = {}
        tmp_rotation = {'yaw': 0, 'roll': 0, 'pitch': 0}
        tmp_layer = 0
        for row in range(21):
            for col in range(21):
                tmp_cent_loc['x'] = -8000 + row * 800
                tmp_cent_loc['z'] = 8000 - row * 800
                tmp_cent_loc['y'] = -7200

                tmp_inner_loc = {'row': row, 'col': col, 'layer': tmp_layer}
        self.dock_blocks.append(self.gen_block(type=tmp_type, cent_loc=tmp_cent_loc,
                                               rotation=tmp_rotation,
                                               inner_loc=tmp_inner_loc))

        # 初始化xl模块
        tmp_type = 'xl'
        tmp_cent_loc = {}
        tmp_rotation = {}
        tmp_layer = 0
        for layer in range(2):
            for row in range(5):
                for col in range(5):
                    if row == 0 and col < 4:
                        tmp_cent_loc['x'] = -8200 + col * 3600
                        tmp_cent_loc['z'] = 9000
                        tmp_cent_loc['y'] = 8900 - layer * 2200
                        tmp_rotation = {'yaw': 0, 'roll': 0, 'pitch': 0}
                    elif row > 0 and col == 4:
                        tmp_cent_loc['x'] = 9000
                        tmp_cent_loc['z'] = -8200 + (4 - row) * 3600
                        tmp_cent_loc['y'] = 8900 - layer * 2200
                        tmp_rotation = {'yaw': 90, 'roll': 0, 'pitch': 0}
                    else:
                        continue

                    tmp_inner_loc = {'row': row, 'col': col, 'layer': layer}
                    self.xl_blocks.append(self.gen_block(type=tmp_type, cent_loc=tmp_cent_loc,
                                                         rotation=tmp_rotation,
                                                         inner_loc=tmp_inner_loc))

        # 初始化l模块
        tmp_type = 'l'
        tmp_cent_loc = {}
        tmp_rotation = {}
        tmp_layer = 0
        for layer in range(2):
            for row in range(10):
                for col in range(10):
                    if row == 0 and col < 9:
                        tmp_cent_loc['x'] = -9200 + col * 1600
                        tmp_cent_loc['z'] = 9000
                        tmp_cent_loc['y'] = 5200 - layer * 800
                        tmp_rotation = {'yaw': 0, 'roll': 0, 'pitch': 0}
                    elif row > 0 and col == 9:
                        tmp_cent_loc['x'] = 9200
                        tmp_cent_loc['z'] = -9200 + (9 - row) * 1600
                        tmp_cent_loc['y'] = 5200 - layer * 800
                        tmp_rotation = {'yaw': 90, 'roll': 0, 'pitch': 0}
                    else:
                        continue

                    tmp_inner_loc = {'row': row, 'col': col, 'layer': layer}
                    self.xl_blocks.append(self.gen_block(type=tmp_type, cent_loc=tmp_cent_loc,
                                                         rotation=tmp_rotation,
                                                         inner_loc=tmp_inner_loc))

class entry:
    index = ''
    macro = ''
    position = {'x': '0', 'y': '0', 'z': '0'}
    rotation = {'yaw': '0'}

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
        """
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





        """
        pass


