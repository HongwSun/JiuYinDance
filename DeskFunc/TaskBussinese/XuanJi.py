import time

import cv2
import numpy as np
from numpy import fromfile

from Utils.FindWindowsImage import WindowsHandle, FindWindowsImageTemplate
from Utils.KeyMouseDriver.GhostSoft.get_driver_v3 import SetGhostBoards, SetGhostMouse
from Utils.loadResources import GetConfig


def bitwise_and(image: np.ndarray):
    """
    给图片加个掩膜遮罩，避免干扰
    :param image: 图片
    :param mask_position: # 指定掩膜位置（左上角坐标， 右下角坐标） mask_position = (50, 50, 200, 200)
    """
    if image is not None:
        # 绘制掩膜（矩形）
        # 参数分别为：图像、矩形左上角坐标、矩形右下角坐标、颜色（BGR）、线条粗细
        return cv2.rectangle(image, (33, 29), (39, 38), (0, 255, 0), -1)
    return image


def _load_pic(img_path: str) -> np.array:
    """
    加载图片
    :param img_path:
    :return:
    """
    return cv2.imdecode(fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)


class FindMyFight:

    def __init__(self):
        self._config = GetConfig().find_my_fight()  # 物品背包
        self._opt_status = GetConfig().get_goods_opt_status()  # 物品使用
        self.windows_opt = WindowsHandle()
        self.windows_find = FindWindowsImageTemplate()

        self._status_config = GetConfig().get_goods_opt_status()

        self._my_fight_pic = _load_pic(self._config.my_fight)
        self._x_ji_mi_ji = _load_pic(self._config.xuan_ji_mi_jing)
        self.bao_ming = _load_pic(self._config.registration_competition)  # 个人报名

    def find_my_fight(self, hwnd: int) -> bool:
        """
        找到我的战斗
        """
        __rec_my_fight = self.windows_find.get_windows_image_rect(hwnd, read_image=self._my_fight_pic)
        if __rec_my_fight is not None:
            SetGhostMouse().move_mouse_to(__rec_my_fight[0], __rec_my_fight[1])
            return True
        return False

    def find_xuan_ji_mi_jing(self, hwnd: int) -> bool:
        """
        查询玄机秘境
        """
        __rec_x_ji_mi_ji = self.windows_find.get_windows_image_rect(hwnd, read_image=self._x_ji_mi_ji)
        if __rec_x_ji_mi_ji is not None:
            SetGhostMouse().move_mouse_to(__rec_x_ji_mi_ji[0], __rec_x_ji_mi_ji[1])
            return True
        return False

    def find_bao_ming(self, hwnd: int) -> bool:
        """
        玄机秘境-个人报名
        :param hwnd:
        :return:
        """
        __rec_bao_ming = self.windows_find.get_windows_image_rect(hwnd, read_image=self.bao_ming)
        if __rec_bao_ming is not None:
            SetGhostMouse().move_mouse_to(__rec_bao_ming[0], __rec_bao_ming[1])
            return True
        return False

    def find_open_loading(self, hwnd: int):
        """
        查询打开状态
        """
        __rec_goods_bag_open_loading = self.windows_find.get_windows_image_rect(hwnd,
                                                                                read_image=_load_pic(self._status_config.open_loading))
        if __rec_goods_bag_open_loading is not None:
            return True
        return False
