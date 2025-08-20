from PySide6 import QtWidgets, QtCore

from Utils.loadResources import update_map_goods_point_list, get_map_goods_point_list


class MapPointTable(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("设置采集坐标")
        self.resize(530, 300)

        # 设置一个表格
        self._table_map_goods_point = QtWidgets.QTableWidget(self)
        self._table_map_goods_point.setRowCount(1)
        self._table_map_goods_point.setColumnCount(2)

        __widget_map_goods_point = QtWidgets.QWidget()
        self._button_add_map_goods_point_row = QtWidgets.QPushButton("新增")
        self._button_del_map_goods_point_row = QtWidgets.QPushButton("删除")
        self._button_save_map_goods_point_table = QtWidgets.QPushButton("保存")

        self._button_save_map_goods_point_table.setToolTip("首次运行新路线时,需要人工监控。\n"
                                                           "如果出现坐标在点击小地图时没用采集而是向其他方法移动,说明此坐标地形干扰大。"
                                                           "请尝试调整坐标(x或者y轴加减1反复调试)。\n"
                                                           "如果物资旁边有个NPC,在自动采集时很大概率会自动点击到此NPC,这种坐标请跳过。")

        _label_goods_point_selected = QtWidgets.QLabel("执行路线 ")
        self._combo_box_goods_point_selected = QtWidgets.QComboBox()
        _label_goods_point_selected.setVisible(False)
        self._combo_box_goods_point_selected.setVisible(False)

        __lay_table_ui_button_map_goods_point = QtWidgets.QHBoxLayout(__widget_map_goods_point)
        __lay_table_ui_button_map_goods_point.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        __lay_table_ui_button_map_goods_point.addWidget(_label_goods_point_selected)
        __lay_table_ui_button_map_goods_point.addWidget(self._combo_box_goods_point_selected, QtCore.Qt.AlignmentFlag.AlignLeft)
        __lay_table_ui_button_map_goods_point.addSpacing(250)
        __lay_table_ui_button_map_goods_point.addWidget(self._button_add_map_goods_point_row, QtCore.Qt.AlignmentFlag.AlignRight)
        __lay_table_ui_button_map_goods_point.addWidget(self._button_del_map_goods_point_row, QtCore.Qt.AlignmentFlag.AlignRight)
        __lay_table_ui_button_map_goods_point.addWidget(self._button_save_map_goods_point_table, QtCore.Qt.AlignmentFlag.AlignRight)
        __lay_table_ui_button_map_goods_point.setSpacing(1)

        __lay_table_ui_map_goods_point = QtWidgets.QVBoxLayout(self)
        __lay_table_ui_map_goods_point.addWidget(__widget_map_goods_point)
        __lay_table_ui_map_goods_point.addWidget(self._table_map_goods_point)
        __lay_table_ui_map_goods_point.setSpacing(2)
        __lay_table_ui_map_goods_point.setContentsMargins(5, 5, 5, 5)

        self._button_add_map_goods_point_row.clicked.connect(self.add_map_goods_point_table_row)    # 更新选中的路线
        self._button_del_map_goods_point_row.clicked.connect(self.del_map_goods_point_table_row_table_row)   # 删除行的按钮也更新一下
        self._button_save_map_goods_point_table.clicked.connect(self.save_map_goods_point_table)

        self.init_table()  # 先初始化以下

    def init_table(self):
        # 填充初始数据（最后一列留空放按钮）
        self._table_map_goods_point.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("路线名"))
        for i in range(1, self._table_map_goods_point.columnCount()):
            self._table_map_goods_point.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(f"坐标 {i}"))
        for row in range(self._table_map_goods_point.rowCount()):
            for col in range(self._table_map_goods_point.columnCount() - 1):
                self.set_cell_data(row, col)
        # 添加按钮列
        self.update_button_column()

    def add_new_column(self):
        # 添加新列
        new_col = self._table_map_goods_point.columnCount()
        self._table_map_goods_point.setColumnCount(new_col + 1)

        # 填充新列数据（倒数第二列）
        for row in range(self._table_map_goods_point.rowCount()):
            self.set_cell_data(row, new_col - 1)

        # 更新按钮到新最后一列
        self.update_button_column()
        for i in range(1, self._table_map_goods_point.columnCount()):
            self._table_map_goods_point.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(f"坐标 {i}"))

    def set_cell_data(self, row: int, col: int):
        if col == 0:
            item = QtWidgets.QTableWidgetItem(f"路线{row + 1}")
            # else:
            #     item = QtWidgets.QTableWidgetItem(f"x,y")
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self._table_map_goods_point.setItem(row, col, item)

    def load_map_goods_point_table(self):
        """
        在表格中加载配置文件中的地图采集路线
        """
        point_list: list = get_map_goods_point_list()  # 配置文件中的所有路线

        # 先把表格清理一下
        row_index: int = 0  # 初始化表格的 row

        point_line_name_list: list = []

        for point_dict in point_list:

            if self._table_map_goods_point.rowCount() - 1 < row_index:
                # 如果当前 row 不够，那么就新增一个
                self.add_map_goods_point_table_row()

            _line_name: str = point_dict.get("line_name")  # 路线名
            _line_map_point_list: list = point_dict.get("map_point")  # 坐标列表

            point_line_name_list.append(point_dict.get("line_name"))

            # 把第一列的路线名设置一下
            item = QtWidgets.QTableWidgetItem(_line_name)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self._table_map_goods_point.setItem(row_index, 0, QtWidgets.QTableWidgetItem(item))

            # 把坐标设置一下
            for point_index in range(len(_line_map_point_list)):
                item = QtWidgets.QTableWidgetItem(_line_map_point_list[point_index])
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if self._table_map_goods_point.columnCount() - 2 == point_index:
                    # 如果当前最大格子 减去开头和结束的2个格子，刚好等于 point_index ，说明现在没有多余的格子可以使用，需要增加一下
                    self.add_new_column()
                self._table_map_goods_point.setItem(row_index, point_index+1, QtWidgets.QTableWidgetItem(item))
            row_index += 1  # 加一行
        self._update_combox_map_goods_point()

    def del_map_goods_point_table_row_table_row(self):
        """
        删除行，需要选中具体的行
        :return:
        """

        selected_row = self._table_map_goods_point.currentRow()
        if selected_row == 0 and not self._table_map_goods_point.selectedItems():
            QtWidgets.QMessageBox.information(self, '提示', "请选择需要删除路线")
            return False
        self._table_map_goods_point.removeRow(selected_row)
        self._update_combox_map_goods_point()
        return True

    def add_map_goods_point_table_row(self):
        """
        新增行
        如果没有选择制定的行，那么就插入在最后面
        :return:
        """
        selected_row = self._table_map_goods_point.currentRow() + 1
        if not self._table_map_goods_point.selectedItems():
            selected_row = self._table_map_goods_point.rowCount()
        self._table_map_goods_point.insertRow(selected_row)

        # 显示一下路线名
        item = QtWidgets.QTableWidgetItem(f"路线{selected_row + 1}")
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._table_map_goods_point.setItem(selected_row, 0, item)

        self.update_button_column()

    def update_button_column(self):
        last_col = self._table_map_goods_point.columnCount() - 1

        # 清除原有按钮
        for row in range(self._table_map_goods_point.rowCount()):
            if self._table_map_goods_point.cellWidget(row, last_col - 1):
                self._table_map_goods_point.removeCellWidget(row, last_col - 1)

        # 添加新按钮
        for row in range(self._table_map_goods_point.rowCount()):
            btn = QtWidgets.QPushButton("添加列")
            btn.clicked.connect(self.add_new_column)
            self._table_map_goods_point.setCellWidget(row, last_col, btn)

    def __show_dialog(self, tips: str):
        """
        创建一个消息框，并显示
        :param tips:
        :return:
        """
        QtWidgets.QMessageBox.information(self, '提示', tips)

    def __check_table_map_point_line_name(self) -> bool:
        """
        检测路线名称是否有重复
        """
        _table_line_name_list: list = []
        for row in range(self._table_map_goods_point.rowCount()):
            if self._table_map_goods_point.item(row, 0) is None:
                continue
            _line_name: str = self._table_map_goods_point.item(row, 0).text()
            if _line_name in _table_line_name_list:
                self.__show_dialog(f"路线名: {_line_name} 已经存在")
                return False
            _table_line_name_list.append(_line_name)
        return True

    def save_map_goods_point_table(self):
        """
        list:[{
            line_name: 路线1,
            selected: true.
            map_point: [[100, 1], [200, 20], [300, 30]]
        }]
        """
        _map_point_list: list = []

        # 先检测一下路线名是不是相同的
        if self.__check_table_map_point_line_name() is False:
            return None

        # 下拉框当前选中的路线
        current_text: str = self._combo_box_goods_point_selected.currentText()

        for row in range(self._table_map_goods_point.rowCount()):
            _line_name: str = ""
            point_list: list = []
            line_dict: dict = {}
            for cul in range(self._table_map_goods_point.columnCount()-1):
                if self._table_map_goods_point.item(row, cul) is None:
                    continue
                _content = self._table_map_goods_point.item(row, cul).text()
                if cul == 0:
                    # 第0列是标题
                    _line_name = _content
                    line_dict["line_name"] = _line_name
                    line_dict["selected"] = True if current_text == _line_name else False
                    continue
                else:
                    # 检测是否没填
                    if _content == "":
                        continue

                    # 检查是否写错了分隔符
                    char_list = ['.', '，', '。', '/']  # 有可能输入错了分隔符
                    result: bool = any(char in _content for char in char_list)
                    if result:
                        separator = next(char for char in char_list if char in _content)
                        _content: str = _content.replace(separator, ",")

                    if _content.count(",") > 1:
                        self.__show_dialog(f"坐标 {_content} 输错错误,请按照格式 例如: 100,231 输入到表格中")
                        return None
                    # 检查是否写的时 x,y 这种标准格式
                    _t_x, _t_y = _content.split(",")
                    if "" in [_t_x, _t_y]:
                        self.__show_dialog(f"坐标 {_content} 输错错误,请按照格式 例如: 100,231 输入到表格中")
                        return None
                    # 检测结束，加入数组吧
                    point_list.append(_content)
            if len(point_list) == 0:
                # 如果这一行没有填写任何数据，那么就继续下一行
                continue
            line_dict["map_point"] = point_list
            _map_point_list.append(line_dict)

            """
            字段的判断
            """
            if _line_name == "":
                self.__show_dialog("路线名不能为空")
                return None
        update_map_goods_point_list(_map_point_list)
        self.__show_dialog("保存成功,请重启脚本")

    def _update_combox_map_goods_point(self):
        """
        更新地图路线的下拉框的值
        """
        # 先获取表格中的所有路线名
        _table_line_name_list: list = []
        for row in range(self._table_map_goods_point.rowCount()):
            _line_name: str = self._table_map_goods_point.item(row, 0).text()
            if _line_name not in _table_line_name_list:
                _table_line_name_list.append(_line_name)

        self._combo_box_goods_point_selected.clear()
        self._combo_box_goods_point_selected.addItems(_table_line_name_list)

        # 数据更新后继续设置一下默认选项
        point_list: list = get_map_goods_point_list()  # 配置文件中的所有路线
        for point_dict in point_list:
            _line_name: str = point_dict.get("line_name")  # 路线名
            if point_dict.get("selected") is True:
                if _line_name in _table_line_name_list:
                    self._combo_box_goods_point_selected.setCurrentText(_line_name)