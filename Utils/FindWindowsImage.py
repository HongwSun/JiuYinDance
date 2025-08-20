"""
查询游戏窗口中的图标
"""

from collections import namedtuple
from ctypes import windll, c_ubyte, wintypes, pointer, byref, sizeof
from typing import List

import cv2
import numpy as np
import psutil
import win32api
import win32con
import win32gui
import win32process
import win32ui
from numpy import frombuffer, fromfile, uint8
from shapely import buffer

from Utils.ImageUtils.FindImageTemplate import find_all_template
from Utils.ImageUtils.MonitorDisplay import coordinate_change_from_windows

PicCapture = namedtuple("PicCapture", ["pic_content", "pic_width", "pic_height"])


class WindowsCapture:
    """
    窗口截图
    """
    def __init__(self):
        self.GetDC = windll.user32.GetDC
        self.CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
        self.GetClientRect = windll.user32.GetClientRect
        self.CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
        self.SelectObject = windll.gdi32.SelectObject
        self.BitBlt = windll.gdi32.BitBlt
        self.SRCCOPY = 0x00CC0020
        self.GetBitmapBits = windll.gdi32.GetBitmapBits
        self.DeleteObject = windll.gdi32.DeleteObject
        self.ReleaseDC = windll.user32.ReleaseDC

    @staticmethod
    def windows_handle_visible(handle_id: int) -> bool:
        """
        查询Windows窗口是否存在
        :param handle_id: 窗口id
        :return:
        """
        _check_result: bool = True
        if not win32gui.IsWindow(handle_id):
            _check_result = False
        else:
            if win32gui.IsIconic(handle_id):
                # IsIconic‌：返回一个布尔值，表示窗口是否最小化。如果窗口最小化，返回TRUE；否则返回FALSE。
                _check_result = False
            elif not win32gui.IsWindowVisible(handle_id):
                # IsWindowVisible‌：返回一个布尔值，表示窗口是否可见。如果窗口可见，返回TRUE；否则返回FALSE。
                _check_result = False
        return _check_result

    @staticmethod
    def __check_capture_width_height(cap_pic_temp: PicCapture) -> bool:
        """
        检测这个截图是否有效
        :param cap_pic_temp: 截图
        :return: True，有效， False,无效
        """
        if 0 in [cap_pic_temp.pic_width, cap_pic_temp.pic_height]:
            # 如果宽或者高为0，表示这张图片有问题
            return False
        return True

    def capture(self, handle: int) -> PicCapture or None:
        """
        窗口区域显示在屏幕上的地方截图
        :param handle: 窗口句柄
        :return: 截图数据 numpy.ndarray格式 和 图片宽度, 图片高度
        """
        handle = int(handle)

        if self.windows_handle_visible(handle) is False:
            return None

        r = wintypes.RECT()
        self.GetClientRect(handle, byref(r))
        width, height = r.right, r.bottom
        # 开始截图
        dc = self.GetDC(handle)
        cdc = self.CreateCompatibleDC(dc)
        bitmap = self.CreateCompatibleBitmap(dc, width, height)
        self.SelectObject(cdc, bitmap)
        self.BitBlt(cdc, 0, 0, width, height, dc, 0, 0, self.SRCCOPY)
        # 截图是BGRA排列，因此总元素个数需要乘以4
        total_bytes = width * height * 4
        buffer = bytearray(total_bytes)
        byte_array = c_ubyte * total_bytes
        self.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        # 清理资源
        self.DeleteObject(bitmap)
        self.DeleteObject(cdc)
        self.ReleaseDC(handle, dc)
        # 返回截图数据为numpy.ndarray
        # cap_pic = PicCapture(frombuffer(buffer, dtype=uint8).reshape(height, width, 4)[:, :, :3], width, height)
        cap_pic = PicCapture(frombuffer(buffer, dtype=uint8).reshape(height, width, 4), width, height)

        if not self.__check_capture_width_height(cap_pic):
            return None
        return cap_pic


class WindowsHandle:

    @staticmethod
    def get_windows_handle() -> List[int]:
        """
        通过便利的方式获取所有的窗口id，然后过滤出我要的
        :return:
        """
        handle_list: List[int] = []
        hwnd_list: List[int] = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnd_list)
        for handle_id in hwnd_list:
            main_text: str = win32gui.GetWindowText(handle_id)

            # 读取任务进程id
            thread_id, process_id = win32process.GetWindowThreadProcessId(handle_id)
            # Get the process name and executable path
            process: psutil.Process = psutil.Process(process_id)
            process_name: str = process.name()

            if main_text.find("九阴真经 ") == 0 and process_name == 'fxgame.exe':
                handle_list.append(handle_id)
        handle_list.sort()
        return handle_list

    @staticmethod
    def activate_windows(windows_handle: int) -> bool:
        """
        激活窗口
        :param windows_handle:
        :return:
        """
        if windows_handle != win32gui.GetForegroundWindow():
            try:
                win32api.keybd_event(0xC, 0, 0, 0)
                win32gui.ShowWindow(windows_handle, win32con.SW_SHOWNA)
                win32gui.SetForegroundWindow(windows_handle)
            except Exception:
                return False
        return True


class FindWindowsImageTemplate:
    """
    查询游戏窗口中的图标的位置
    """
    def __init__(self):
        self._windows_cap = WindowsCapture()

    def get_windows_image_rect(self, hwnd: int, read_image: np.ndarray, threshold: float = 0.7, edge: bool = False) -> ():
        """
        查询图标模板在游戏窗口中的匹配度最高的坐标，并将坐标映射到Windows窗口中。
        此坐标可被鼠标直接使用
        :param edge: 是否支持透明图层
        :param threshold: 匹配度 0 - 1
        :param hwnd: 窗口id
        :param read_image: 需要寻找的模板
        :return: None 或者 （x, y）
        """
        _windows_cap: PicCapture = self._windows_cap.capture(hwnd)

        _cap_point: list = []

        if _windows_cap is not None:
            if isinstance(read_image, str):
                # img_read = cv2.cv2.imread(img)   # 这个方法无法处理带中文的路径
                image = cv2.imdecode(fromfile(read_image, dtype=uint8), cv2.IMREAD_UNCHANGED)
            else:
                image = read_image.copy()
            match_result = find_all_template(_windows_cap.pic_content, image, threshold, edge=edge)
            """
            match_result = [{'result': (951.0, 770.0), 'rectangle': ((933, 752), (933, 788), (969, 752), (969, 788)), 'confidence': 0.9120017886161804}, 
                            {'result': (911.0, 770.0), 'rectangle': ((893, 752), (893, 788), (929, 752), (929, 788)), 'confidence': 0.9051406979560852}, 
                            {'result': (871.0, 770.0), 'rectangle': ((853, 752), (853, 788), (889, 752), (889, 788)), 'confidence': 0.90046226978302}, 
                            {'result': (831.0, 770.0), 'rectangle': ((813, 752), (813, 788), (849, 752), (849, 788)), 'confidence': 0.884774923324585}]
            """
            max_confidence_match_point: tuple = ()
            check_confidence: float = 0
            for match_result_l in match_result:
                # 拿出所有匹配的坐标(x, y),校验一下匹配度大小
                rect_re: float = match_result_l['confidence']
                if rect_re < check_confidence:
                    continue
                check_confidence = rect_re
                max_confidence_match_point = match_result_l['result']
            if len(max_confidence_match_point) != 0:
                _p: tuple = coordinate_change_from_windows(hwnd=hwnd, coordinate=max_confidence_match_point)
                return _p
        return None

    @staticmethod
    def get_image_all_rect(orign_image: np.ndarray, read_image: np.ndarray, threshold: float = 0.7, edge: bool = False,
                           hwnd: int = None) -> []:
        """
        查询所有相似度匹配的坐标，并映射到windows窗口中，此坐标可被鼠标直接使用
        :param hwnd: 窗口句柄，如果传了的话，那么就返回图片在桌面窗口中的坐标，不传就返回图片在游戏窗口中的坐标
        :param orign_image: 原图(完整图片)
        :param read_image: 需要查询的图片模板(小图)
        :param threshold: 相似度
        :param edge: 是否支持透明图层
        :return: None 或者 [(x1, y1), (x2, y2)]
        """
        img_result = []
        if orign_image is not None:

            if isinstance(read_image, str):
                # img_read = cv2.cv2.imread(img)   # 这个方法无法处理带中文的路径
                image = cv2.imdecode(fromfile(read_image, dtype=uint8), cv2.IMREAD_UNCHANGED)
            else:
                image = read_image.copy()

            match_result = find_all_template(orign_image, image, threshold, edge=edge)

            """
            match_result = [{'result': (951.0, 770.0), 'rectangle': ((933, 752), (933, 788), (969, 752), (969, 788)), 'confidence': 0.9120017886161804}, 
                            {'result': (911.0, 770.0), 'rectangle': ((893, 752), (893, 788), (929, 752), (929, 788)), 'confidence': 0.9051406979560852}, 
                            {'result': (871.0, 770.0), 'rectangle': ((853, 752), (853, 788), (889, 752), (889, 788)), 'confidence': 0.90046226978302}, 
                            {'result': (831.0, 770.0), 'rectangle': ((813, 752), (813, 788), (849, 752), (849, 788)), 'confidence': 0.884774923324585}]
            """

            for match_result_l in match_result:
                # 拿出所有匹配的坐标(x, y)
                rect_re = match_result_l['result']
                img_result.append(rect_re)

        point_result: list = []
        if hwnd is not None:
            # 传入了 窗口句柄，返回窗口桌面中的坐标
            for point in img_result:
                _p: tuple = coordinate_change_from_windows(hwnd=hwnd, coordinate=point)
                point_result.append(_p)
            if len(point_result) == 0:
                return None
        else:
            # 没有传入句柄，那么就返回在游戏窗口中的坐标
            if len(img_result) == 0:
                return None
            else:
                point_result = img_result
        return point_result
