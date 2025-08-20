from PySide6 import QtWidgets, QtCore

from Utils.loadResources import GetConfig, get_skill_group_list, update_skill_group_list


class SkillSetting(QtWidgets.QDialog):
    """
    技能设置
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._skill_config = GetConfig()

        self.setWindowTitle("设置技能")
        self.setFixedSize(530, 260)
        self._skill_table = QtWidgets.QTableWidget(self)
        self._skill_table.setRowCount(1)
        self._skill_table.setColumnCount(5)
        __widget = QtWidgets.QWidget()
        self._button_add_skill_table_row = QtWidgets.QPushButton("新增")
        self._button_del_skill_table_row = QtWidgets.QPushButton("删除")
        self._button_save_skill_table = QtWidgets.QPushButton("保存")

        __lay_table_ui_button = QtWidgets.QHBoxLayout(__widget)
        __lay_table_ui_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        __lay_table_ui_button.addWidget(self._button_add_skill_table_row)
        __lay_table_ui_button.addWidget(self._button_del_skill_table_row)
        __lay_table_ui_button.addWidget(self._button_save_skill_table)
        __lay_table_ui_button.setSpacing(1)

        __lay_table_ui = QtWidgets.QVBoxLayout(self)
        __lay_table_ui.addWidget(__widget)
        __lay_table_ui.addWidget(self._skill_table)
        __lay_table_ui.setSpacing(2)
        __lay_table_ui.setContentsMargins(5, 5, 5, 5)

        self._button_add_skill_table_row.clicked.connect(self.add_skill_table_row)
        self._button_del_skill_table_row.clicked.connect(self.del_skill_table_row)
        self._button_save_skill_table.clicked.connect(self.save_skill_table)

    def del_skill_table_row(self):
        """
        删除行，需要选中具体的行
        :return:
        """
        selected_row = self._skill_table.currentRow()
        if selected_row == 0 and not self._skill_table.selectedItems():
            QtWidgets.QMessageBox.information(self, '提示', "请选择需要删除的技能")
            return False
        self._skill_table.removeRow(selected_row)
        return True

    def add_skill_table_row(self):
        """
        新增行
        如果没有选择制定的行，那么就插入在最后面
        :return:
        """
        selected_row = self._skill_table.currentRow() + 1
        if not self._skill_table.selectedItems():
            selected_row = self._skill_table.rowCount()
        self._skill_table.insertRow(selected_row)

    def load_skill_table(self):
        """
        加载文件中的打怪套路设置
        :return:
        """
        _skill_obj: dict = get_skill_group_list().get("打怪套路")  # 当前正在使用的技能组

        self._skill_table.clear()
        self._skill_table.setHorizontalHeaderLabels(['技能名', '技能冷却(秒)', '释放时间(秒)', '释放优先级', '键盘Key'])

        row_index: int = 0
        for skill_name in _skill_obj:
            if self._skill_table.rowCount() < row_index + 1:
                self._skill_table.insertRow(self._skill_table.rowCount())

            # 技能名称
            item = QtWidgets.QTableWidgetItem(str(skill_name).format(row_index, 1))
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self._skill_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(item))

            _skill: dict = _skill_obj.get(skill_name)
            # 技能CD
            if _skill.get("CD") is not None:
                column_index: int = 1
                item = QtWidgets.QTableWidgetItem(str(_skill.get("CD")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))

            # 技能释放时间
            if _skill.get("active_cd") is not None:
                column_index: int = 2
                item = QtWidgets.QTableWidgetItem(str(_skill.get("active_cd")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))
            # 技能释放优先级
            if _skill.get("level") is not None:
                column_index: int = 3
                item = QtWidgets.QTableWidgetItem(str(_skill.get("level")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))
            # 技能释放优先级
            if _skill.get("key") is not None:
                column_index: int = 4
                item = QtWidgets.QTableWidgetItem(str(_skill.get("key")).format(row_index, column_index))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self._skill_table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(item))
            row_index += 1

    def save_skill_table(self):
        """
        保存技能设置
        {
            "打怪套路": {
                "梵心降魔": {"CD": 2, "active_cd": 1, "level": 2, "key": "Q"},
                "三阳开泰": {"CD": 6, "active_cd": 1.8, "level": 1, "key": "R"},
                "五气呈祥": {"CD": 2, "active_cd": 1, "level": 2, "key": "1"},
                "罡风推云": {"CD": 6, "active_cd": 1, "level": 3, "key": "3"},
                "气贯长虹": {"CD": 8, "active_cd": 1, "level": 2, "key": "2"}
            }
        }
        """
        skill_dict_json: dict = {}
        for row in range(self._skill_table.rowCount()):

            _skill_name: str = ""
            _skill_cd: int = 0
            _skill_active_cd: float = 0.0
            _skill_level: int = 0
            _skill_key: str = ""

            for cum in range(self._skill_table.columnCount()):
                __content = self._skill_table.item(row, cum).text()
                if cum == 0:
                    _skill_name = __content
                elif cum == 1:
                    _skill_cd = int(__content)
                elif cum == 2:
                    _skill_active_cd = float(__content)
                elif cum == 3:
                    _skill_level = int(__content)
                elif cum == 4:
                    _skill_key = __content
            skill_dict_json[str(_skill_name)] = {"CD": _skill_cd,
                                                 "active_cd": _skill_active_cd,
                                                 "level": _skill_level,
                                                 "key": _skill_key}
        update_skill_group_list(_skill_dict=skill_dict_json)
        QtWidgets.QMessageBox.information(self, '提示', "保存成功,请重启脚本!")


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    main_gui = SkillSetting()
    main_gui.show()
    sys.exit(app.exec())
