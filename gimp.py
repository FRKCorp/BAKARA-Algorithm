import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout,
    QScrollArea, QGraphicsOpacityEffect, QHBoxLayout, QSizePolicy, QLabel, QFrame, QComboBox, QMessageBox,
)
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QIcon, QLinearGradient
from PyQt5.QtCore import Qt, QRectF, QPointF, QEasingCurve, QPropertyAnimation, QSize, QRect, QTimer, qWarning, QPoint

import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout,
    QScrollArea, QGraphicsOpacityEffect,
)
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRectF, QPointF, QEasingCurve, QPropertyAnimation


class DialWidget(QWidget):
    def __init__(self, parent=None, x=0, y=0, w=200, h=200):
        super().__init__(parent)
        self.paint_angle = 0
        self.text_ = 0
        self.new_mistake_range = False
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.animation_ = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.setGeometry(x, y, w, h)
        self.setFixedSize(w, h)
        self.setMinimumSize(100, 100)


    def getText_(self):
        return self.text_

    def setAngle(self, angle):
        self.paint_angle = angle
        self.text_ += 1
        self.update()



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("transparent"))

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        radius = w / 2 * 0.9
        rect = QRectF(cx - radius, cy - radius, 2 * radius, 2 * radius)

        end_angle_rad = math.radians(self.paint_angle - 180 + 6)
        end_y = cx + radius * math.cos(end_angle_rad)
        end_x = cy - radius * math.sin(end_angle_rad)

        painter.drawLine(QPointF(cx, cy), QPointF(end_x, end_y))
        painter.drawLine(QPointF(cx, cy),
                         QPointF(cx + radius * math.cos(math.radians(90)),
                                 cy - radius * math.sin(math.radians(90))))

        painter.setBrush(QBrush(QColor("#4EBF40")))
        painter.drawEllipse(rect)
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(rect)

        start_angle = 90 * 16
        span_angle = -1 * self.paint_angle * 16
        if 0 <= self.text_ < 6:
            painter.setBrush(QBrush(QColor("#4EBF40")))
        elif 6 <= self.text_ <= 10:
            painter.setBrush(QBrush(QColor("#D3E61D")))
        elif 11 <= self.text_ <= 20:
            painter.setBrush(QBrush(QColor("#FF7136")))
        elif 20 <= self.text_ < 40:
            painter.setBrush(QBrush(QColor("#FF3E3E")))
        else:
            start_angle = 0
            span_angle = 360 * 16
            painter.setBrush(QBrush(QColor("#F51022")))
            self.opacity_effect.setOpacity(1.0)
            self.setGraphicsEffect(self.opacity_effect)
            self.animation_.setDuration(600)
            self.animation_.setStartValue(1.0)
            self.animation_.setEndValue(0.0)
            self.animation_.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation_.setLoopCount(-1)
            self.animation_.start()

        painter.drawPie(rect, start_angle, span_angle)

        font = QFont("Arial", 20, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor("rgb(23, 20, 37)"))


        if w == 150:
            if self.text_ >= 10:
                painter.drawText(60, 82, str(self.text_))
            else:
                painter.drawText(68, 82, str(self.text_))
        else:
            if self.text_ >= 10:
                painter.drawText(52, 72, str(self.text_))
            else:
                painter.drawText(58, 73, str(self.text_))

        painter.end()



class HorizontalLabel(QWidget):
    def __init__(self, parent=None, cnt_=1, size=130):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.size_ = size
        self.dial = QWidget()
        self.cnt_ = cnt_

        font = QFont("Arial", 15, QFont.Bold)
        self.tNum = QPushButton(self)
        self.tNum.setGeometry(0, 0, 30, 30)
        self.tNum.setStyleSheet("background-color: transparent; border: none; color: white;")
        self.tNum.setObjectName("tNum")
        self.tNum.setText(f"{self.cnt_}")
        self.tNum.setFont(font)

        self.redraw_btn = QPushButton(self)
        self.redraw_btn.setGeometry(0, 0, size, size)
        self.redraw_btn.setText("")
        self.redraw_btn.setObjectName("redraw_btn")
        self.redraw_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.0);
            }
        """)
        icon_tmp = QIcon("watch_.png")
        self.redraw_btn.setIcon(icon_tmp)
        self.dial = DialWidget(self, w=self.size_, h=self.size_)
        self.dial.hide()
        self.redraw_btn.setIconSize(QSize(80, 80))
        QTimer.singleShot(2000, self.aftertime)
        self.redraw_btn.clicked.connect(self.rotate_dial)
        self.redraw_btn.raise_()

    def show_warning(self, type):
        msg = QMessageBox()
        msg.setWindowTitle("Внимание!")

        if type == "norm":
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Новый диапазон серии поражений.\nСтол №{self.cnt_}")
            msg.setStyleSheet("""
                        QMessageBox {
                            background-color: #f8f9fa;
                            border-top: 2px solid #443B6E;
                        }

                        QMessageBox QLabel {
                            color: #333;
                            font-size: 18px;
                            font-family: Comfortaa;
                        }

                        QMessageBox QPushButton {
                            background-color: rgb(23, 20, 37);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 6px;
                            font-size: 13px;
                            min-width: 80px;
                        }

                        QMessageBox QPushButton:hover {
                            background-color: #443B6E;
                        }
                    """)
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Критическое количество поражений.\nСтол №{self.cnt_}")
            msg.setStyleSheet("""
                        QMessageBox {
                            background-color: #f8f9fa;
                            border-top: 2px solid #443B6E;
                        }

                        QMessageBox QLabel {
                            color: red;
                            font-size: 18px;
                            font-family: Comfortaa;
                        }

                        QMessageBox QPushButton {
                            background-color: rgb(23, 20, 37);
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 6px;
                            font-size: 13px;
                            min-width: 80px;
                        }

                        QMessageBox QPushButton:hover {
                            background-color: #443B6E;
                        }
                    """)
        msg.exec_()

    def aftertime(self):
        self.redraw_btn.setIcon(QIcon())
        self.dial.show()
        self.dial.update()

    def rotate_dial(self):
        tmp_txt = self.dial.getText_()
        new_angle = tmp_txt * 9
        self.dial.setAngle(new_angle)
        if tmp_txt == 5 or tmp_txt == 10 or tmp_txt == 20:
            self.show_warning("norm")
        if tmp_txt == 39:
            self.show_warning("gg")


class GreetingsPal(QWidget):
    def __init__(self, parent=None, login_="Саня Маляр", psw_="qwerty"):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgb(23, 20, 37);")
        self.resize(500, 200)
        self.setMaximumSize(500, 200)
        self.login_ = login_
        self.psw_ = psw_

        self.main_vlayout = QVBoxLayout(self)

        self.welcome_txt = QPushButton(self)
        self.welcome_txt.setObjectName("welcome_txt")
        self.welcome_txt.setStyleSheet("""
            QPushButton {
                background-color: rgba(159, 148, 215, 0.2);
                color: white;
                border: none;
                border-radius: 7px;
            }
        """)
        font = QFont("Comfortaa", 17, QFont.Bold)
        self.welcome_txt.setFont(font)
        self.welcome_txt.setText("♧ Добро пожаловать в Baccarat ♧")
        self.main_vlayout.addWidget(self.welcome_txt, alignment=Qt.AlignTop)

        self.login_txt = QPushButton(self)
        self.login_txt.setObjectName("login_txt")
        self.login_txt.setStyleSheet(
            "background-color: transparent; color: rgb(159, 148, 215); border: none; border-radius: 5px;")
        font_login_psw = QFont("Comfortaa", 15, QFont.Bold)
        self.login_txt.setFont(font_login_psw)
        self.login_txt.setText("Логин:")

        self.login_val = QPushButton(self)
        self.login_val.setObjectName("login_val")
        self.login_val.setStyleSheet("background-color: transparent; color: white; border: none;")
        font_val = QFont("Comfortaa", 13, QFont.Bold)
        self.login_val.setFont(font_val)
        self.login_val.setText("⇾  " + "Саня Маляр" + "  ⇽")

        login_layout = QHBoxLayout(self)
        login_layout.addWidget(self.login_txt, alignment=Qt.AlignLeft)
        login_layout.addWidget(self.login_val, alignment=Qt.AlignLeft)
        login_layout.setContentsMargins(0, 0, 0, 0)

        self.psw_txt = QPushButton(self)
        self.psw_txt.setObjectName("psw_txt")
        self.psw_txt.setStyleSheet(
            "background-color: transparent; color: rgb(159, 148, 215); border: none; border-radius: 5px;")
        font_login_psw = QFont("Comfortaa", 15, QFont.Bold)
        self.psw_txt.setFont(font_login_psw)
        self.psw_txt.setText("Пароль:")

        self.psw_val = QPushButton(self)
        self.psw_val.setObjectName("psw_val")
        self.psw_val.setStyleSheet(
            "background-color: transparent; color: white; border: none;")
        font_val = QFont("Comfortaa", 13, QFont.Bold)
        self.psw_val.setFont(font_val)
        self.psw_val.setText(f"{"♢" * len(self.psw_)}")
        self.psw_val.clicked.connect(self.changeVisibility)

        login_layout = QHBoxLayout(self)
        login_layout.addWidget(self.login_txt, alignment=Qt.AlignLeft)
        login_layout.addWidget(self.login_val)
        login_layout.setContentsMargins(50, 0, 20, 0)
        login_layoutWrapper = QWidget()
        login_layoutWrapper.setLayout(login_layout)

        psw_layout = QHBoxLayout(self)
        psw_layout.addWidget(self.psw_txt, alignment=Qt.AlignLeft)
        psw_layout.addWidget(self.psw_val)
        psw_layout.setContentsMargins(50, 0, 20, 0)
        psw_layoutWrapper = QWidget()
        psw_layoutWrapper.setLayout(psw_layout)
        login_layoutWrapper.setStyleSheet("background-color: transparent;")
        psw_layoutWrapper.setStyleSheet("background-color: transparent;")
        self.main_vlayout.addWidget(login_layoutWrapper)
        self.main_vlayout.addWidget(psw_layoutWrapper)

        self.enter_btn = QPushButton(self)
        self.enter_btn.setObjectName('enter_btn')
        self.enter_btn.setStyleSheet(
            "background-color: transparent; color: white; border: none; text-decoration: underline")
        self.enter_btn.setText("Продолжить")
        self.enter_btn.setFont(font_val)
        self.main_vlayout.addWidget(self.enter_btn)
        self.enter_btn.clicked.connect(self.startThyGame)

        self.main_vlayout.setContentsMargins(10, 20, 10, 22)

        self.animation = QPropertyAnimation(self, b"windowOpacity")




    def startThyGame(self):
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.finished.connect(lambda: self.hide())
        self.animation.start()

    def changeVisibility(self):
        if self.psw_val.text() == ("♢" * len(self.psw_)):
            self.psw_val.setText(self.psw_)
        else:
            self.psw_val.setText("♢" * len(self.psw_))

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(QPoint(0, 0), QPoint(self.width(), self.height()))
        gradient.setColorAt(0, QColor(23, 20, 37))
        gradient.setColorAt(1, QColor(50, 40, 70))
        painter.fillRect(self.rect(), gradient)


class MainHorizontalLabel(HorizontalLabel):
    pass

class TableElement(QWidget):
    def __init__(self, parent=None, cnt_=1):
        super().__init__(parent)
        self.main_vertical_layout = QVBoxLayout(self)
        main_elem_layout = QHBoxLayout()

        self.main_elem_circle = MainHorizontalLabel(self, cnt_=cnt_, size=130)
        self.win_txt = QPushButton(self)
        self.win_txt.setObjectName("win_txt")
        self.win_txt.setStyleSheet("background-color: rgb(23, 20, 37); color: white; border: none")
        font = QFont("Comfortaa", 13, QFont.Bold)
        self.win_txt.setFont(font)
        self.win_txt.setText("Победы:")

        self.win_val = QPushButton(self)
        self.win_val.setObjectName("win_val")
        self.win_val.setStyleSheet("background-color: rgb(23, 20, 37); color: #36852C; border: none")
        self.win_val.setFont(font)
        self.win_val.setText("       13⭡")

        self.lose_txt = QPushButton(self)
        self.lose_txt.setObjectName("lose_txt")
        self.lose_txt.setStyleSheet("background-color: rgb(23, 20, 37); color: white; border: none")
        self.lose_txt.setFont(font)
        self.lose_txt.setText("Поражения:")

        self.lose_val = QPushButton(self)
        self.lose_val.setObjectName("lose_val")
        self.lose_val.setStyleSheet("background-color: rgb(23, 20, 37); color: red; border: none")
        self.lose_val.setFont(font)
        self.lose_val.setText(" 20⭣")

        self.bet_txt = QPushButton(self)
        self.bet_txt.setObjectName("bet_txt")
        self.bet_txt.setStyleSheet("background-color: rgb(23, 20, 37); color: white; border: none")
        self.bet_txt.setFont(font)
        self.bet_txt.setText("Ставка:")

        self.bet_val = QComboBox(self)
        self.bet_val.setObjectName("bet_val")
        self.bet_val.setFixedSize(100, 20)
        self.bet_val.setStyleSheet("""
            QComboBox {
                background-color: rgb(23, 20, 37);
                color: #4EBF40;
            }
            QComboBox::drop-down::button { 
                border:none;
            }
        """)
        self.bet_val.setFont(font)
        self.bet_val.addItem("           1$")
        self.bet_val.addItem("       100$")
        self.bet_val.addItem("      200$")
        self.bet_val.addItem("      500$")
        self.bet_val.addItem("     1000$")

        self.rec_txt = QPushButton(self)
        self.rec_txt.setObjectName("rec_txt")
        self.rec_txt.setStyleSheet(
            "background-color: rgb(23, 20, 37); color: white; border-bottom: 3px solid #443B6E; border-radius: 0px;")
        self.rec_txt.setFont(font)
        self.rec_txt.setText("Рекомендации:")

        self.pattern = QPushButton(self)
        self.pattern.setObjectName("pattern")
        self.pattern.setStyleSheet("background-color: rgb(23, 20, 37); color: white; border: none")
        self.pattern.setFont(font)
        self.pattern.setText("Некрасивый")

        self.color_ = QPushButton(self)
        self.color_.setObjectName("color_")
        self.color_.setStyleSheet("background-color: rgb(23, 20, 37); color: red; border: none")
        self.color_.setFont(font)
        self.color_.setText("Банкир")

        self.line_decorate = QWidget()
        self.line_decorate.setFixedSize(3, 150)
        self.line_decorate.setStyleSheet("background-color: #443B6E; ")

        tmp_win_layout = QHBoxLayout()
        tmp_win_layout.addWidget(self.win_txt, alignment=Qt.AlignLeft)
        tmp_win_layout.addWidget(self.win_val)
        tmp_win_layout.setContentsMargins(0, 0, 0, 0)
        tmp_win_layoutWrapper = QWidget()
        tmp_win_layoutWrapper.setLayout(tmp_win_layout)

        tmp_lose_layout = QHBoxLayout()
        tmp_lose_layout.addWidget(self.lose_txt, alignment=Qt.AlignLeft)
        tmp_lose_layout.addWidget(self.lose_val)
        tmp_lose_layout.setContentsMargins(0, 0, 0, 0)
        tmp_lose_layoutWrapper = QWidget()
        tmp_lose_layoutWrapper.setLayout(tmp_lose_layout)

        tmp_bet_layout = QHBoxLayout()
        tmp_bet_layout.addWidget(self.bet_txt, alignment=Qt.AlignLeft)
        tmp_bet_layout.addWidget(self.bet_val, alignment=Qt.AlignRight)
        tmp_bet_layout.setContentsMargins(0, 0, 0, 0)
        tmp_bet_layoutWrapper = QWidget()
        tmp_bet_layoutWrapper.setLayout(tmp_bet_layout)

        tmp_vertical_wl_layout = QVBoxLayout()
        tmp_vertical_wl_layout.addWidget(tmp_win_layoutWrapper)
        tmp_vertical_wl_layout.addWidget(tmp_lose_layoutWrapper)
        tmp_vertical_wl_layout.addWidget(tmp_bet_layoutWrapper)
        tmp_vertical_wl_layout.setContentsMargins(0, 16, 0, 16)
        tmp_vertical_wl_layoutWrapper = QWidget()
        tmp_vertical_wl_layoutWrapper.setLayout(tmp_vertical_wl_layout)
        tmp_vertical_wl_layoutWrapper.setStyleSheet("border: none")

        tmp_rec_layout = QVBoxLayout()
        tmp_rec_layout.addWidget(self.rec_txt)
        tmp_rec_layout.addWidget(self.pattern)
        tmp_rec_layout.addWidget(self.color_)
        tmp_rec_layoutWrapper = QWidget()
        tmp_rec_layoutWrapper.setLayout(tmp_rec_layout)
        tmp_rec_layoutWrapper.setStyleSheet("border: none")

        main_elem_layout.addWidget(self.main_elem_circle, alignment=Qt.AlignLeft)
        main_elem_layout.addWidget(tmp_vertical_wl_layoutWrapper)
        main_elem_layout.addWidget(self.line_decorate)
        main_elem_layout.addWidget(tmp_rec_layoutWrapper)

        self.main_elem_wrapper = QWidget()
        self.main_elem_wrapper.setLayout(main_elem_layout)
        self.main_elem_wrapper.setFixedSize(500, 165)
        self.main_elem_wrapper.setStyleSheet("border: 3px solid #443B6E; border-radius: 7px")
        self.main_vertical_layout.addWidget(self.main_elem_wrapper)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)

    def add_btn(self, plusik):
        self.main_vertical_layout.addWidget(plusik)

    def turn_off_borders(self):
        self.main_elem_wrapper.setStyleSheet("border-bottom: 3px solid #443B6E;")
        self.main_elem_wrapper.setContentsMargins(0, 0, 3, 0)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Casino Royal")
        self.setStyleSheet("background-color: rgb(23, 20, 37);")
        self.resize(500, 200)
        self.setMaximumSize(500, 200)

        supermainL = QVBoxLayout(self)

        self.main_element = TableElement(self)

        font_add_widget = QFont("Comfortaa", 15, QFont.Bold)
        self.add_widget = QPushButton(self)
        self.add_widget.setObjectName("add_widget")
        self.add_widget.setFixedSize(500, 20)
        self.add_widget.setStyleSheet("background-color: #443B6E; border-radius: 7px; color: white")
        self.add_widget.setText("+")
        self.add_widget.setFont(font_add_widget)
        self.add_widget.clicked.connect(self.add_tables_btn)
        self.main_element.add_btn(self.add_widget)
        supermainL.addWidget(self.main_element, alignment=Qt.AlignTop)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
                    QScrollArea:vertical {
                        border: 3px solid #443B6E; 
                        border-radius: 7px;           
                    }
                    QScrollBar:vertical {
                        background-color: red;
                        min-height: 20px;
                        border-radius: 5px;
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }
                """)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        supermainL.addWidget(self.scroll_area)

        self.vertical_list_tablesWrapper = QWidget()
        self.vertical_list_tables = QVBoxLayout(self.vertical_list_tablesWrapper)
        self.scroll_area.setWidget(self.vertical_list_tablesWrapper)
        self.tables_list = []
        self.scroll_area.hide()
        self.add_widget.hide()
        self.main_element.hide()

        self.welcomeFriend = GreetingsPal(self)
        self.welcomeFriend.enter_btn.clicked.connect(self.mainElShow)
        supermainL.addWidget(self.welcomeFriend)
        supermainL.setContentsMargins(0, 0, 0, 0)

    def mainElShow(self):
        QTimer.singleShot(300, lambda : (self.main_element.show(), self.add_widget.show()))

    def add_tables_btn(self):
        if self.size().height() <= 400:
            self.setMaximumSize(500, self.size().height() + 170)
            self.resize(500, self.size().height() + 170)

        tmp_table_obj = TableElement(self.vertical_list_tablesWrapper, cnt_=len(self.tables_list) + 2)
        tmp_table_obj.turn_off_borders()
        self.vertical_list_tables.addWidget(tmp_table_obj, alignment=Qt.AlignTop)
        self.vertical_list_tables.setContentsMargins(0, 0, 0, 0)
        self.tables_list.append(tmp_table_obj)
        self.scroll_area.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())