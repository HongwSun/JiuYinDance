from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QCheckBox
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot

checkbox_list: list = []
windows_hwnd_checked_list: list = []

"""
获取窗口
"""


class MonitorWindowsPage(QWidget):
    def __init__(self, items: list):
        super().__init__()
        self.lay_out_windows_hwnd_list = QHBoxLayout(self)
        self.lay_out_windows_hwnd_list.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.update_checkboxes(items)

    def clear_checkboxes(self):
        global checkbox_list
        for checkbox in checkbox_list:
            self.lay_out_windows_hwnd_list.removeWidget(checkbox)
            checkbox.deleteLater()
        checkbox_list = []

    def update_checkboxes(self, items: list):
        self.clear_checkboxes()
        for item in items:
            checkbox = QCheckBox(str(item), self)
            checkbox.setChecked(True)  # 找到后，默认勾选起来
            # checkbox.stateChanged.connect(self.on_state_changed)
            self.lay_out_windows_hwnd_list.addWidget(checkbox)
            checkbox_list.append(checkbox)

    @Slot(int)  # 指定槽函数的参数类型为int，对应QCheckBox的stateChanged信号的参数类型int（Qt::CheckState）
    def on_state_changed(self, state):
        global windows_hwnd_checked_list
        _check_text: str = self.sender().text()
        if state == Qt.CheckState.Checked.value:
            # print("选中:", _check_text)  # 使用sender()获取触发信号的发送者对象（即当前CheckBox）并获取其文本内容。
            if _check_text not in windows_hwnd_checked_list:
                windows_hwnd_checked_list.append(_check_text)
        else:
            # print("取消选中:", _check_text)  # 同上，但状态为未选中。
            if _check_text in windows_hwnd_checked_list:
                windows_hwnd_checked_list.remove(_check_text)
        # print(windows_hwnd_checked_list)


class WindowsButton(QWidget):
    """
    获取窗口，测试窗口，开始执行
    """

    def __init__(self):
        super().__init__()

        self.push_button_get_windows = QtWidgets.QPushButton("获取窗口", self)
        self.push_button_test_windows = QtWidgets.QPushButton("测试窗口", self)
        self.push_button_run_windows = QtWidgets.QPushButton("开始执行", self)
        self.push_button_run_windows.setFixedHeight(40)
        self.push_button_test_windows.setFixedHeight(40)
        self.push_button_get_windows.setFixedHeight(40)

        self._lay_out_windows_button = QtWidgets.QHBoxLayout()
        self._lay_out_windows_button.addWidget(self.push_button_get_windows)
        self._lay_out_windows_button.addWidget(self.push_button_test_windows)
        self._lay_out_windows_button.addWidget(self.push_button_run_windows)

        self.__tips_label_game_windows_is_None = QtWidgets.QLabel("未发现游戏窗口")

        self._lay_out_button_check = QtWidgets.QVBoxLayout(self)
        self._lay_out_button_check.setSpacing(10)
        self._lay_out_button_check.addLayout(self._lay_out_windows_button)
        self._lay_out_button_check.addWidget(self.__tips_label_game_windows_is_None, alignment=Qt.AlignmentFlag.AlignCenter)

    def get_windows(self, hwnd_list: list):
        """
        获取并渲染窗口数量
        :return:
        """
        _game_windows: list[str] = hwnd_list
        if len(_game_windows) > 0:
            _widget_windows_monitor = MonitorWindowsPage(_game_windows)
            if self._lay_out_button_check.count() == 2:
                self._lay_out_button_check.takeAt(1)
            self._lay_out_button_check.addWidget(_widget_windows_monitor)
            self._lay_out_button_check.removeWidget(self.__tips_label_game_windows_is_None)
            self.__tips_label_game_windows_is_None.hide()
        else:
            self.__tips_label_game_windows_is_None.show()

    def get_windows_checked(self):
        """
        看看已经选择了哪些游戏窗口的句柄
        :return:
        """
        _checked_hwnd_list: list[str] = []
        for item in self.findChildren(QCheckBox):
            if item.isChecked():
                _checked_hwnd_list.append(item.text())
        return _checked_hwnd_list


if __name__ == "__main__":
    app = QApplication([])
    window = WindowsButton()
    window.show()
    app.exec()
