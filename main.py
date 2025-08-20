import ctypes
import sys

from PySide6.QtWidgets import QApplication
from DeskFunc.QtConnect.connect import TaskConnect


if __name__ == '__main__':
    ctypes.windll.shcore.SetProcessDpiAwareness(False)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = TaskConnect()

    w.log_print("\n\n更新日期: 2025-08-10\n"
                "更新内容: \n"
                "新增内容: 玄机秘境自动报名\n"
                "优化内容: 优化地图右上角坐标识别率")

    w.show()
    app.exec()

