# encodings: utf-8
import json
import os.path

import yaml

from Utils.dataClass import DancePicGrey, DancePicGreen, DmDll, GhostDll, DancePicWhz, BackpackItem, GoodsOptStatus, \
    MapPic, TruckCarReceiveTask, TruckCarPic, FindTruckCarTaskNPC, Team, PersonStatusAndBuff, MapPointNum, MyFight
from Utils.projectPath import PathUtil


def _get_dir_path() -> str:
    """
    获取项目目录
    :return:
    """
    # return PathUtil().get_path_from_resources("../Resources/config.yaml")
    return PathUtil().get_path_from_resources("FilePath.yaml")


def _get_project_path() -> str:
    """
    项目目录
    :return:
    """
    return PathUtil().get_root_path()


def _get_dir_map_goods_point_path() -> str:
    """
    地图采集物坐标list
    """
    return PathUtil().get_path_from_resources("mapGoodsPointList.json")


def update_map_goods_point_list(content_list: list):
    """
    更新地图采集物坐标配置文件
    :param content_list
    :return:
    """

    if len(content_list) == 0:
        return None
    if not os.path.exists(_get_dir_map_goods_point_path()):
        file = open(_get_dir_map_goods_point_path(), "w")
        file.close()
    with open(_get_dir_map_goods_point_path(), 'w', encoding="gbk") as file:
        json.dump(content_list, file, ensure_ascii=False, indent=4)


def get_map_goods_point_list() -> list:
    """
    获取地图资源坐标
    """
    with open(_get_dir_map_goods_point_path(), 'r', encoding="gbk") as f:
        fs = f.read()
        res = json.loads(fs)
        return res


def get_map_goods_point_list_by_selected() -> list:
    """
    查询已经选中的地图路线
    """
    _res: list = get_map_goods_point_list()
    map_point_list = []
    _first_line_point_list: list = []
    for pp in _res:
        is_selected: bool = pp.get("selected")
        _first_line_point_list = pp.get("map_point")
        if is_selected is False:
            continue
        map_point_list: list = pp.get("map_point")
    if len(map_point_list) == 0:
        # 如果没有设置采集路线，那么默认那第一个
        map_point_list = _first_line_point_list
    return map_point_list


def _get_dir_skill_group() -> str:
    """
    获取技能组
    """
    return PathUtil().get_path_from_resources("SkillSetting.json")


def get_skill_group_list() -> dict:
    """
    获取技能组
    """
    with open(_get_dir_skill_group(), 'r', encoding="gbk") as f:
        fs = f.read()
        res = json.loads(fs)
        return res


def update_skill_group_list(*args, **kwargs):
    """
    更新配置文件
    :param kwargs: dance_threshold, whz_dance_threshold, is_debug
    :return:
    """
    dict_skill: dict = {}
    with open(_get_dir_skill_group(), 'w', encoding="gbk") as file:
        dict_skill["打怪套路"] = kwargs.get("_skill_dict")
        json.dump(dict_skill, file, ensure_ascii=False, indent=4)


class GetConfig:
    def __init__(self):
        self.fs = open(_get_dir_path(), encoding="UTF-8")
        self.__datas = yaml.load(self.fs, Loader=yaml.FullLoader)  # 添加后就不警告了
        self.project_dir: str = _get_project_path()

    def __del__(self):
        self.fs.close()

    def get_dll_dm(self) -> DmDll:
        """
        大漠驱动的dll
        :return:
        """
        dll_dm = DmDll()
        dll_dm.dll_dm = self.project_dir + self.__datas["keyBoardMouseDll"]["dmDll"]["dm"]
        dll_dm.dll_dm_reg = self.project_dir + self.__datas["keyBoardMouseDll"]["dmDll"]["dm_reg"]
        return dll_dm

    def get_dll_ghost(self) -> GhostDll:
        """
        幽灵键鼠的dll
        :return:
        """
        ghost_dm = GhostDll()
        ghost_dm.dll_ghost = self.project_dir + self.__datas["keyBoardMouseDll"]["ghostDll"]["ghost_dll"]
        return ghost_dm

    def get_dance_grey_pic(self) -> DancePicGrey:
        """
        团练授业按钮图标
        :return:
        """
        pic_dance: DancePicGrey = DancePicGrey()
        pic_dance.dance_J = self.project_dir + self.__datas["DanceGrey"]["j"]
        pic_dance.dance_K = self.project_dir + self.__datas["DanceGrey"]["k"]
        pic_dance.dance_Up = self.project_dir + self.__datas["DanceGrey"]["up"]
        pic_dance.dance_Down = self.project_dir + self.__datas["DanceGrey"]["down"]
        pic_dance.dance_Left = self.project_dir + self.__datas["DanceGrey"]["left"]
        pic_dance.dance_Right = self.project_dir + self.__datas["DanceGrey"]["right"]
        return pic_dance

    def get_dance_green_pic(self) -> DancePicGreen:
        """
        绿色的上下左右，用于漠西风涛
        :return:
        """
        dance_green: DancePicGreen = DancePicGreen()
        # 赋值
        dance_green.dance_Left = self.project_dir + self.__datas["DanceGreen"]["left"]
        dance_green.dance_Right = self.project_dir + self.__datas["DanceGreen"]["right"]
        dance_green.dance_Up = self.project_dir + self.__datas["DanceGreen"]["up"]
        dance_green.dance_Down = self.project_dir + self.__datas["DanceGreen"]["down"]
        return dance_green

    def get_dance_whz_pic(self) -> DancePicWhz:
        """
        绿色的上下左右，用于挖宝、隐士、势力任务
        :return:
        """
        dance_whz: DancePicWhz = DancePicWhz()
        # 赋值
        dance_whz.dance_whz_Left = self.project_dir + self.__datas["WhzDance"]["left"]
        dance_whz.dance_whz_Right = self.project_dir + self.__datas["WhzDance"]["right"]
        dance_whz.dance_whz_Up = self.project_dir + self.__datas["WhzDance"]["up"]
        dance_whz.dance_whz_Down = self.project_dir + self.__datas["WhzDance"]["down"]
        return dance_whz

    def get_backpack_item_pic(self) -> BackpackItem:
        """
        获取背包中的物品
        :return:
        """
        _back_item: BackpackItem = BackpackItem()
        _back_item.goods_bag_tag_clickable = self.project_dir + self.__datas["ItemBackpack"]["backPack_unclick_status"]
        _back_item.goods_bag_tag_clicked = self.project_dir + self.__datas["ItemBackpack"]["backPack_clicked_status"]
        _back_item.gift_card = self.project_dir + self.__datas["ItemBackpack"]["gift_card"]
        _back_item.run_goods = self.project_dir + self.__datas["ItemBackpack"]["yu_feng_shen_shui"]
        return _back_item

    def get_goods_opt_status(self) -> GoodsOptStatus:
        """
        获取物品操作的状态
        :return:
        """
        _goods_opt_status: GoodsOptStatus = GoodsOptStatus()
        _goods_opt_status.open_loading = self.project_dir + self.__datas["OptStatus"]["item_open_loading"]  # 打开中、使用中
        _goods_opt_status.get_all_goods = self.project_dir + self.__datas["OptStatus"]["get_all_goods"]  # 获取所有
        return _goods_opt_status

    def get_map_pic(self) -> MapPic:
        """
        地图
        :return:
        """
        _map: MapPic = MapPic()
        _map.pos_x = self.project_dir + self.__datas["Map"]["point_x"]
        _map.pos_y = self.project_dir + self.__datas["Map"]["point_y"]
        _map.plus_map = self.project_dir + self.__datas["Map"]["map_plus_max"]
        _map.search_pos = self.project_dir + self.__datas["Map"]["search_pos"]
        _map.result_point = self.project_dir + self.__datas["Map"]["search_pos_result"]
        return _map

    def get_team(self):
        """
        队伍
        """
        team = Team()
        team.create_team = self.project_dir + self.__datas["team"]["create_team"]
        team.leave_team = self.project_dir + self.__datas["team"]["leave_team"]
        team.flag_team = self.project_dir + self.__datas["team"]["flag_team"]
        team.flag_team_status = self.project_dir + self.__datas["team"]["flag_team_status"]
        return team

    def get_track_car(self):
        """
        获取镖车的目的地
        """
        get_track_car = TruckCarReceiveTask()
        # 寻找NPC并对话
        get_track_car.receive_task_talk = self.project_dir + self.__datas["PicTruckCar"]["receive_task_talk"]
        # 选择目的地和镖车类型
        get_track_car.receive_task = self.project_dir + self.__datas["PicTruckCar"]["receive_task"]
        get_track_car.receive_task_confirm = self.project_dir + self.__datas["PicTruckCar"]["receive_task_confirm"]
        # 成都
        get_track_car.task_chengdu_GaiBang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["chengdu"]["GaiBang"]
        get_track_car.task_chengdu_NanGongShiJia = self.project_dir + self.__datas["PicTruckCar"]["Area"]["chengdu"]["NanGong"]
        get_track_car.task_chengdu_QianDengZheng = self.project_dir + self.__datas["PicTruckCar"]["Area"]["chengdu"]["QianDengZheng"]
        get_track_car.task_chengdu_ShenJiaBao = self.project_dir + self.__datas["PicTruckCar"]["Area"]["chengdu"]["ShenJiaBao"]
        # 燕京
        get_track_car.task_yanjing_DongFangShiJia = self.project_dir + self.__datas["PicTruckCar"]["Area"]["YanJin"]["DongFang"]
        get_track_car.task_yanjing_JiMingYi = self.project_dir + self.__datas["PicTruckCar"]["Area"]["YanJin"]["JiMingYi"]
        get_track_car.task_yanjing_JunMaChang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["YanJin"]["JunMaChang"]
        get_track_car.task_yanjing_YiRenZhuang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["YanJin"]["YiRenZhuang"]
        # 苏州
        get_track_car.task_suzhou_YongCuiShanZhuang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["SuZhou"]["YongCuiShanZhuang"]
        get_track_car.task_suzhou_WuWangMu = self.project_dir + self.__datas["PicTruckCar"]["Area"]["SuZhou"]["WuWangMu"]
        get_track_car.task_suzhou_CaiShiChang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["SuZhou"]["CaiShiChang"]
        get_track_car.task_suzhou_BaoChuanChang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["SuZhou"]["BaoChuanChang"]
        # 金陵
        get_track_car.task_jinlin_MeiHuaMen = self.project_dir + self.__datas["PicTruckCar"]["Area"]["JinLing"]["MeiHuaMen"]
        get_track_car.task_jinlin_HuangJiaLieChang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["JinLing"]["HuangJiaLieChang"]
        get_track_car.task_jinlin_MoChouHu = self.project_dir + self.__datas["PicTruckCar"]["Area"]["JinLing"]["MoChouHu"]
        # 洛阳
        get_track_car.task_luoyang_BaoDuZhai = self.project_dir + self.__datas["PicTruckCar"]["Area"]["LuoYang"]["BaoDuZhai"]
        get_track_car.task_luoyang_YanMenShiJia = self.project_dir + self.__datas["PicTruckCar"]["Area"]["LuoYang"]["YanMenShiJia"]
        get_track_car.task_luoyang_QinWangFu = self.project_dir + self.__datas["PicTruckCar"]["Area"]["LuoYang"]["QinWangFu"]
        # 车型
        get_track_car.car_type_little = self.project_dir + self.__datas["PicTruckCar"]["car_type_little"]
        get_track_car.car_type_medium = self.project_dir + self.__datas["PicTruckCar"]["car_type_medium"]
        get_track_car.car_type_big = self.project_dir + self.__datas["PicTruckCar"]["car_type_big"]
        # npc对话
        get_track_car.break_npc_talk = self.project_dir + self.__datas["PicTruckCar"]["break_npc_talk"]
        return get_track_car

    def truck_task(self):
        truck = TruckCarPic()
        truck.car_flag = self.project_dir + self.__datas["TruckCarPic"]["car_flag"]
        truck.task_flag_status = self.project_dir + self.__datas["TruckCarPic"]["task_flag_status"]
        truck.task_flags_yellow_car = self.project_dir + self.__datas["TruckCarPic"]["task_flags_yellow_car"]
        truck.task_star_mode = self.project_dir + self.__datas["TruckCarPic"]["task_star_mode"]
        truck.task_monster_fight = self.project_dir + self.__datas["TruckCarPic"]["task_monster_fight"]
        truck.task_monster_target = self.project_dir + self.__datas["TruckCarPic"]["task_monster_target"]
        truck.task_monster_target_skil = self.project_dir + self.__datas["TruckCarPic"]["task_monster_target_skill"]
        truck.task_car_selected = self.project_dir + self.__datas["TruckCarPic"]["task_car_selected"]
        truck.fight_other_truck_car = self.project_dir + self.__datas["TruckCarPic"]["fight_other_truck_car"]
        return truck

    def find_track_car_task(self):
        """
        寻找地图上的接镖NPC
        """
        truck_car_task = FindTruckCarTaskNPC()
        truck_car_task.qin_xiu = self.project_dir + self.__datas["PicTruckCar"]["qin_xiu"]
        truck_car_task.qin_xiu_activity_list = self.project_dir + self.__datas["PicTruckCar"]["qin_xiu_activity_list"]
        truck_car_task.qin_xiu_truck_car_task = self.project_dir + self.__datas["PicTruckCar"]["qin_xiu_truck_car_task"]
        truck_car_task.bang_hui = self.project_dir + self.__datas["PicTruckCar"]["bang_hui"]

        # 成都
        truck_car_task.task_point_chengdu = self.project_dir + self.__datas["PicTruckCar"]["Area"]["chengdu"]["address"]
        truck_car_task.task_point_chengdu_npc = self.project_dir + self.__datas["PicTruckCar"]["Area"]["chengdu"]["npc"]
        # 燕京
        truck_car_task.task_point_yanjing = self.project_dir + self.__datas["PicTruckCar"]["Area"]["YanJin"]["address"]
        truck_car_task.task_point_yanjing_npc = self.project_dir + self.__datas["PicTruckCar"]["Area"]["YanJin"]["npc"]
        # 金陵
        truck_car_task.task_point_jinling = self.project_dir + self.__datas["PicTruckCar"]["Area"]["JinLing"]["address"]
        truck_car_task.task_point_jinling_npc = self.project_dir + self.__datas["PicTruckCar"]["Area"]["JinLing"]["npc"]
        # 苏州
        truck_car_task.task_point_suzhou = self.project_dir + self.__datas["PicTruckCar"]["Area"]["SuZhou"]["address"]
        truck_car_task.task_point_suzhou_npc = self.project_dir + self.__datas["PicTruckCar"]["Area"]["SuZhou"]["npc"]
        # 洛阳
        truck_car_task.task_point_luoyang = self.project_dir + self.__datas["PicTruckCar"]["Area"]["LuoYang"]["address"]
        truck_car_task.task_point_luoyang_npc = self.project_dir + self.__datas["PicTruckCar"]["Area"]["LuoYang"]["npc"]
        return truck_car_task

    def find_person_buff(self) -> PersonStatusAndBuff:
        """
        右上角人物buff
        :return:
        """
        _buff = PersonStatusAndBuff()
        _buff.run_goods_ready = self.project_dir + self.__datas["PersonBuff"]["yu_feng_shen_shui_ready"]
        _buff.run_goods_buff = self.project_dir + self.__datas["PersonBuff"]["yu_feng_shen_shui_run"]
        _buff.sit_blood = self.project_dir + self.__datas["PersonBuff"]["person_blood_full"]
        _buff.null_blood = self.project_dir + self.__datas["PersonBuff"]["person_blood_less"]
        return _buff

    def find_person_point(self) -> MapPointNum:
        """
        人物右上角的坐标值
        :return:
        """
        _point: MapPointNum = MapPointNum()
        _point.zero = self.project_dir + self.__datas["PersonPoint"]["zero"]
        _point.one = self.project_dir + self.__datas["PersonPoint"]["one"]
        _point.two = self.project_dir + self.__datas["PersonPoint"]["two"]
        _point.three = self.project_dir + self.__datas["PersonPoint"]["three"]
        _point.four = self.project_dir + self.__datas["PersonPoint"]["four"]
        _point.five = self.project_dir + self.__datas["PersonPoint"]["five"]
        _point.six = self.project_dir + self.__datas["PersonPoint"]["six"]
        _point.seven = self.project_dir + self.__datas["PersonPoint"]["seven"]
        _point.eight = self.project_dir + self.__datas["PersonPoint"]["eight"]
        _point.nine = self.project_dir + self.__datas["PersonPoint"]["nine"]
        _point.d = self.project_dir + self.__datas["PersonPoint"]["d"]
        _point.f = self.project_dir + self.__datas["PersonPoint"]["f"]
        return _point

    def find_my_fight(self) -> MyFight:
        """
        我的战斗
        :return:
        """
        _my_fight: MyFight = MyFight()
        _my_fight.my_fight = self.project_dir + self.__datas["MyFight"]["my_fight"]
        _my_fight.xuan_ji_mi_jing = self.project_dir + self.__datas["MyFight"]["xuan_ji_mi_jing"]
        _my_fight.registration_competition = self.project_dir + self.__datas["MyFight"]["registration"]  # 个人报名
        return _my_fight
