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


class FindGiftCard:

    def __init__(self):
        self._config = GetConfig().get_backpack_item_pic()  # 物品背包
        self._opt_status = GetConfig().get_goods_opt_status()  # 物品使用
        self.windows_opt = WindowsHandle()
        self.windows_find = FindWindowsImageTemplate()
        self._goods_pic_bag_unclick = _load_pic(self._config.goods_bag_tag_clickable)
        self._goods_pic_bag_clicked = _load_pic(self._config.goods_bag_tag_clicked)

        self._goods_pic_bag_gift_card = _load_pic(self._config.gift_card)
        self._goods_pic_bag_gift_card = bitwise_and(self._goods_pic_bag_gift_card)

        self._goods_pic_open_loading = _load_pic(self._opt_status.open_loading)
        self._button_ok = _load_pic(self._opt_status.get_all_goods)

    def open_bag(self, hwnd: int) -> bool:
        """
        获取物品背包,看看有没有礼卡
        """
        for index in range(3):
            _open_backpack = self.windows_find.get_windows_image_rect(hwnd, read_image=self._goods_pic_bag_clicked)
            _un_open_backpack = self.windows_find.get_windows_image_rect(hwnd, read_image=self._goods_pic_bag_unclick)

            if _un_open_backpack is None and _open_backpack is None:
                # 如果还没有打开背包
                self.windows_opt.activate_windows(hwnd)
                time.sleep(0.5)
                SetGhostBoards().click_press_and_release_by_key_code_hold_time(66, 0.3)  # 按B，打开背包
                time.sleep(0.5)

        _open_backpack = self.windows_find.get_windows_image_rect(hwnd, read_image=self._goods_pic_bag_clicked)
        if _open_backpack is None:
            _un_open_backpack = self.windows_find.get_windows_image_rect(hwnd, read_image=self._goods_pic_bag_unclick)
            if _un_open_backpack is not None:
                # 如果还没有点到物品栏，那么需要点一下
                SetGhostMouse().move_mouse_to(_un_open_backpack[0], _un_open_backpack[1])
                SetGhostMouse().click_mouse_left_button()
                time.sleep(0.5)

        # 看看礼卡在不在
        _goods_un_clicked = self.windows_find.get_windows_image_rect(hwnd, read_image=self._goods_pic_bag_gift_card)
        if _goods_un_clicked is not None:
            return True
        return False

    def find_gift_card(self, hwnd: int) -> bool:
        """
        找到第一个礼品卡(优先点击左上)
        """
        __rec_goods_bag_tag_clickable = self.windows_find.get_windows_image_rect(hwnd, read_image=self._goods_pic_bag_gift_card)
        if __rec_goods_bag_tag_clickable is not None:
            SetGhostMouse().move_mouse_to(__rec_goods_bag_tag_clickable[0], __rec_goods_bag_tag_clickable[1])
            return True
        return False

    def click_ok(self, hwnd: int):
        """
        点击确定按钮
        """
        time.sleep(1)
        __rec_goods_bag_tag_clickable = self.windows_find.get_windows_image_rect(hwnd, read_image=self._button_ok)
        if __rec_goods_bag_tag_clickable is not None:
            SetGhostMouse().move_mouse_to(__rec_goods_bag_tag_clickable[0], __rec_goods_bag_tag_clickable[1])
            time.sleep(0.2)
            SetGhostMouse().click_mouse_left_button()
            return True
        return False

    def find_open_loading(self, hwnd: int):
        """
        查询打开状态
        """
        __rec_goods_bag_open_loading = self.windows_find.get_windows_image_rect(hwnd,
                                                                                read_image=self._goods_pic_open_loading,
                                                                                threshold=0.85)
        if __rec_goods_bag_open_loading is not None:
            return True
        return False
