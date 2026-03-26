import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QScrollArea,QHBoxLayout, QComboBox, QMenu, QAction,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(23, 20, 37);")
        self.resize(500, 200)
        self.setMaximumSize(500, 200)

        self.color_obj_array = []
        self.color_txt_array = []
        self.user_algs_arrays = [[], [], [], []]
        self.user_algs_colors = [[], [], [], []]



        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.WindowDoesNotAcceptFocus
        )
        self.move(500, 500)
        self.setWindowOpacity(0.9)

        main_vlayout = QVBoxLayout(self)


        self.scroll_area = QScrollArea(self)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFixedHeight(40)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.horizontalScrollBar().setStyleSheet("""
                                    QScrollBar::horizontal {
                                        border: 2px solid #443B6E; 
                                        border-radius: 7px;
                                        background-color: #5C5090;
                                    }
                                    QScrollBar::handle:horizontal {
                                        background: #BEB2F7;
                                        min-width: 20px;
                                        border-radius: 5px;
                                        border: none;
                                    }
                                    QScrollBar::add-line:horizontal,
                                    QScrollBar::sub-line:horizontal {
                                        background: none;
                                        width: 0px;
                                        height: 0px;
                                    }
                                    QScrollBar::add-page:horizontal,
                                    QScrollBar::sub-page:horizontal {
                                        background: none;
                                    }
                                """)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.tmpWrapper = QWidget()
        self.tmpWrapper.setStyleSheet("border-radius: 7px; background-color: #100E1A")
        self.bet_layout = QHBoxLayout(self.tmpWrapper)
        self.scroll_area.setWidget(self.tmpWrapper)
        main_vlayout.addWidget(self.scroll_area, alignment=Qt.AlignTop)

        self.sys_alg_layout = QHBoxLayout(self)
        self.sys_alg_layoutWrapper = QWidget()
        self.sys_alg_layoutWrapper.setStyleSheet("border-bottom: 2px solid #443B6E;")
        self.sys_alg_layoutWrapper.setLayout(self.sys_alg_layout)

        self.sys_txt = QPushButton(self)
        self.sys_txt.setObjectName("sys_txt")
        self.sys_txt.setFixedSize(100, 30)
        self.sys_txt.setStyleSheet("background-color: transparent; border: none; color: white;")
        font = QFont("Comfortaa", 15, QFont.Bold)
        self.sys_txt.setText("System")
        self.sys_txt.setFont(font)

        self.sys_algs = QComboBox(self)
        self.sys_algs.setObjectName("sys_algs")
        self.sys_algs.setFixedSize(380, 30)
        self.sys_algs.addItem( " " * 32 + "Основной")
        self.sys_algs.addItem( " " * 31 + "Инверсный")
        self.sys_algs.setStyleSheet("""
                    QComboBox {
                        background-color: rgb(23, 20, 37);
                        color: #D6CDFF;
                        border-left: 2px solid #443B6E;
                        border-top: none;
                        border-bottom: none;
                        border-right: none;
                    }
                    QComboBox::drop-down::button { 
                        border: none;
                    }
                """)
        font_cb = QFont("Comfortaa", 11, QFont.Bold)
        self.sys_algs.setFont(font_cb)
        self.sys_algs.currentIndexChanged.connect(self.sys_algsIsChanged)

        self.sys_alg_layout.addWidget(self.sys_txt, alignment=Qt.AlignLeft)
        self.sys_alg_layout.addWidget(self.sys_algs, alignment=Qt.AlignRight)

        main_vlayout.addWidget(self.sys_alg_layoutWrapper)

        ####################################################

        self.user_alg_layout = QHBoxLayout(self)
        self.user_alg_layoutWrapper = QWidget()
        self.user_alg_layoutWrapper.setStyleSheet("border-bottom: 2px solid #443B6E;")
        self.user_alg_layoutWrapper.setLayout(self.user_alg_layout)

        self.user_txt = QPushButton(self)
        self.user_txt.setObjectName("user_txt")
        self.user_txt.setFixedSize(100, 30)
        self.user_txt.setStyleSheet("background-color: transparent; border: none; color: white")
        font = QFont("Comfortaa", 15, QFont.Bold)
        self.user_txt.setText("User")
        self.user_txt.setFont(font)

        self.user_algs = QComboBox(self)
        self.user_algs.setObjectName("user_algs")
        self.user_algs.setFixedSize(380, 30)
        self.user_algs.addItem(" " * 18 + "Последовательность №1")
        self.user_algs.addItem(" " * 18 + "Последовательность №2")
        self.user_algs.addItem(" " * 18 + "Последовательность №3")
        self.user_algs.addItem(" " * 18 + "Последовательность №4")
        self.user_algs.setStyleSheet("""
                    QComboBox {
                        background-color: rgb(23, 20, 37);
                        color: #D6CDFF;
                        border-left: 2px solid #443B6E;
                        border-top: none;
                        border-bottom: none;
                        border-right: none;
                    }
                    QComboBox::drop-down::button { 
                        border: none;
                    }
                """)
        self.user_algs.setFont(font_cb)
        self.user_algs.currentIndexChanged.connect(self.user_algsIsChanged)

        self.user_alg_layout.addWidget(self.user_txt, alignment=Qt.AlignLeft)
        self.user_alg_layout.addWidget(self.user_algs, alignment=Qt.AlignRight)

        main_vlayout.addWidget(self.user_alg_layoutWrapper)

        #####################################################################################

        self.buttons_layout = QHBoxLayout(self)
        self.buttons_layoutWrapper = QWidget()
        self.buttons_layoutWrapper.setLayout(self.buttons_layout)

        self.rb_layout = QHBoxLayout(self)
        self.rb_layoutWrapper = QWidget()
        self.rb_layoutWrapper.setFixedSize(70, 30)
        self.rb_layoutWrapper.setStyleSheet("border: none")
        self.rb_layoutWrapper.setLayout(self.rb_layout)

        self.red_btn = QPushButton(self)
        self.red_btn.setObjectName("red_btn")
        self.red_btn.setFixedSize(30, 30)
        self.red_btn.setStyleSheet("background-color: red; border: 1px solid white; border-radius: 5px; color: white")
        font_btn = QFont("Comfortaa", 13, QFont.Bold)
        self.red_btn.setFont(font_btn)
        self.red_btn.setText("+K")
        self.red_btn.clicked.connect(self.red_isClicked)

        self.blue_btn = QPushButton(self)
        self.blue_btn.setObjectName("blue_btn")
        self.blue_btn.setFixedSize(30, 30)
        self.blue_btn.setStyleSheet("background-color: blue; border: 1px solid white; border-radius: 5px; color: white")
        font_btn = QFont("Comfortaa", 13, QFont.Bold)
        self.blue_btn.setFont(font_btn)
        self.blue_btn.setText("+С")
        self.blue_btn.clicked.connect(self.blue_isClicked)

        self.rb_layout.addWidget(self.red_btn, alignment=Qt.AlignLeft)
        self.rb_layout.addWidget(self.blue_btn, alignment=Qt.AlignRight)
        self.buttons_layout.addWidget(self.rb_layoutWrapper, alignment=Qt.AlignLeft)

        #######################################################################

        self.funcs_btn = QHBoxLayout(self)
        self.funcs_btnWrapper = QWidget()
        self.funcs_btnWrapper.setFixedSize(150, 40)
        self.funcs_btnWrapper.setStyleSheet("border: none")
        self.funcs_btnWrapper.setLayout(self.funcs_btn)

        self.delete_elem = QPushButton(self)
        self.delete_elem.setFixedHeight(30)
        self.delete_elem.setObjectName("delete_elem")
        self.delete_elem.setStyleSheet("border-radius: 5px; color: white;")
        self.delete_elem.setText("⤶")
        self.delete_elem.setFont(font)
        self.delete_elem.clicked.connect(self.delete_elemIsClicked)

        self.delete_all = QPushButton(self)
        self.delete_all.setFixedHeight(30)
        self.delete_all.setObjectName("delete_all")
        self.delete_all.setStyleSheet("border-radius: 5px; color: red;")
        font_delete_all = QFont("Comfortaa", 20, QFont.Bold)
        self.delete_all.setText("❌")
        self.delete_all.setFont(font_delete_all)
        self.delete_all.clicked.connect(self.delete_allIsClicked)

        self.save_array = QPushButton(self)
        self.save_array.setFixedHeight(30)
        self.save_array.setObjectName("save_array")
        self.save_array.setText("✅")
        self.save_array.setFont(font)
        self.save_array.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                color: #14D410;
            }
            QPushButton::menu-indicator {
                width: 0; 
                height: 0;
            }
        """)
        self.save_menu = QMenu(self.save_array)
        self.save_menu.setStyleSheet("""
                QMenu::item {
                    color: white;
                }
                QMenu::item:selected{
                    color: #14D410;
                }
            """)
        menu_font = QFont("Comfortaa", 10, QFont.Bold)
        self.save_menu.setFont(menu_font)
        self.action1 = QAction("Подтвердить изменения", self.save_menu)
        self.action2 = QAction("Сохранить и выйти", self.save_menu)
        self.save_menu.addAction(self.action1)
        self.save_menu.addAction(self.action2)
        self.save_array.setMenu(self.save_menu)
        self.action1.triggered.connect(lambda: self.save_arrayIsClicked(self.action1))
        self.action2.triggered.connect(lambda: self.save_arrayIsClicked(self.action2))

        self.funcs_btn.addWidget(self.delete_elem, alignment=Qt.AlignLeft)
        self.funcs_btn.addWidget(self.delete_all)
        self.funcs_btn.addWidget(self.save_array, alignment=Qt.AlignRight)

        self.buttons_layout.addWidget(self.funcs_btnWrapper, alignment=Qt.AlignRight)
        main_vlayout.addWidget(self.buttons_layoutWrapper)
        main_vlayout.setContentsMargins(10, 5, 10, 5)
        self.user_alg_layout.setContentsMargins(5, 10, 5, 0)
        self.buttons_layout.setContentsMargins(7, 0, 7, 0)
        self.rb_layout.setContentsMargins(0, 0, 0, 0)
        self.bet_layout.setContentsMargins(5, 0, 5, 0)
        self.sys_alg_layout.setContentsMargins(5, 10, 5, 0)

    #  -> Отображает системные последовательности в лэйауте <-
    def sys_algsIsChanged(self, index):
            if index == 0:
                self.delete_allIsClicked()
                self.red_isClicked()
                self.blue_isClicked()
                self.red_isClicked()
                self.blue_isClicked()
                self.red_isClicked()
                self.red_isClicked()
                self.blue_isClicked()
                self.blue_isClicked()
                self.red_isClicked()
                self.red_isClicked()
                self.red_isClicked()
                self.red_isClicked()
                self.blue_isClicked()
                self.blue_isClicked()
                self.blue_isClicked()
                self.red_isClicked()

            elif index == 1:
                self.delete_allIsClicked()
                self.blue_isClicked()
                self.red_isClicked()
                self.blue_isClicked()
                self.red_isClicked()
                self.blue_isClicked()
                self.blue_isClicked()
                self.red_isClicked()
                self.red_isClicked()
                self.blue_isClicked()
                self.blue_isClicked()
                self.blue_isClicked()
                self.blue_isClicked()
                self.red_isClicked()
                self.red_isClicked()
                self.red_isClicked()
                self.blue_isClicked()

    def user_algsIsChanged(self, index):
        self.delete_allIsClicked()
        for i in self.user_algs_colors[index]:
            if i == "К":
                self.red_isClicked()
            elif i == "С":
                self.blue_isClicked()

    def save_arrayIsClicked(self, action):
        if action.text() == "Подтвердить изменения":
            current_index = self.user_algs.currentIndex()

            self.user_algs_colors[current_index].clear()

            for color in self.color_txt_array:
                self.user_algs_colors[current_index].append(color)

        elif action.text() == "Сохранить и выйти":
            if len(self.color_txt_array) != 0:
                folder_name = "algs"
                file_name = "1.txt"
                file_path = os.path.join(folder_name, file_name)

                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(" ".join(self.color_txt_array))
            elif len(self.color_txt_array) == 0:
                self.sys_algsIsChanged(0)
                self.save_arrayIsClicked(self.action2)
            self.hide()

    def red_isClicked(self):
        tmp_red = QPushButton(self)
        tmp_red.setFixedSize(20, 20)
        tmp_red.setStyleSheet("background-color: red; border-radius: 5px; border: none; color: white;")
        font = QFont("Comfortaa", 12, QFont.Bold)
        tmp_red.setFont(font)
        tmp_red.setText("К")
        self.color_obj_array.append(tmp_red)
        self.color_txt_array.append("К")
        self.bet_layout.addWidget(tmp_red, alignment=Qt.AlignLeft)

    def blue_isClicked(self):
        tmp_blue = QPushButton(self)
        tmp_blue.setFixedSize(20, 20)
        tmp_blue.setStyleSheet("background-color: blue; border-radius: 5px; border: none; color: white;")
        font = QFont("Comfortaa", 12, QFont.Bold)
        tmp_blue.setFont(font)
        tmp_blue.setText("С")
        self.color_obj_array.append(tmp_blue)
        self.color_txt_array.append("С")
        self.bet_layout.addWidget(tmp_blue, alignment=Qt.AlignLeft)

    def delete_elemIsClicked(self):
        if len(self.color_txt_array) != 0:
            last_element = self.color_obj_array[-1]
            self.bet_layout.removeWidget(last_element)
            self.color_obj_array.pop(-1)
            self.color_txt_array.pop(-1)

    def delete_allIsClicked(self):
        for i in self.color_obj_array:
            self.bet_layout.removeWidget(i)
        self.color_obj_array.clear()
        self.color_txt_array.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())