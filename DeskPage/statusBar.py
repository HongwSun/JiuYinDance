from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QProgressBar


class StatusBarProcess(QtWidgets.QStatusBar):
    """
    底部的进度条一共分为2个效果。
    左侧的时间显示和 跑马灯效果
    右侧的显示一共执行了多少次
    """
    def __init__(self):
        super().__init__()

        # 左侧区域
        # 给状态栏显示文字用的，显示时分秒
        self.status_bar_label_left = QtWidgets.QLabel(QtCore.QTime.currentTime().toString('HH:mm:ss'))
        self.progress_time = QtCore.QTimer(self)
        self.progress_time.timeout.connect(self.update_time)
        self.progress_time.start(1000)  # 1000 毫秒 = 1 秒

        # 状态栏本身显示的信息 第二个参数是信息停留的时间，单位是毫秒，默认是0（0表示在下一个操作来临前一直显示）
        # 在状态栏左侧新增显示控件
        self.addWidget(self.status_bar_label_left, stretch=1)

        # 加载一个进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)  # 默认不显示这个进度条，等任务启动后再显示
        self.progress_bar.setInvertedAppearance(False)  # 进度条的走向
        self.progress_bar.setOrientation(QtCore.Qt.Orientation.Horizontal)  # 进度条的方向
        # 出现跑马灯的效果
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 设置跑马灯颜色
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #05B8CC; }")

        self.addWidget(self.progress_bar, stretch=3)

        # 右侧区域
        self.status_bar_label_right = QtWidgets.QLabel()
        self.update_execute_num(0)  # 初始化显示，一共识别了 0 轮
        self.status_bar_label_right.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.addWidget(self.status_bar_label_right, stretch=1)

        self.setContentsMargins(8, 0, 0, 0)

    def update_time(self):
        # 获取当前时间并格式化为字符串
        current_time = QtCore.QTime.currentTime().toString('HH:mm:ss')
        self.status_bar_label_left.setText(current_time)

    def update_execute_num(self, e_num: int):
        """
        在界面右下角显示执行了多少次
        :param e_num: 执行次数
        :return:
        """
        self.status_bar_label_right.setText(f"一共识别了 {e_num} 轮")

    def run_status(self, status: bool):
        """
        启动状态栏底部的进度条
        :param status:
        :return:
        """
        if status:
            self.progress_bar.setVisible(True)
        else:
            self.progress_bar.setVisible(False)
