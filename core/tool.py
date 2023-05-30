from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from config import *


class GlobalConfig:
    def __init__(self):
        self.insNum = INS_NUM
        self.pageNum = PAGE_NUM
        self.pageInsNum = PAGE_INS_NUM
        self.algo = ALGORITHM
        self.order = ORDER
        self.animDuration = ANIM_DURATION


def getPage(ins: int, pageLen: int) -> list[int, int]:
    return [ins // pageLen, ins % pageLen]


def getRoundedPixmap(pixmap, radius):
    # 创建一个空的圆角图片
    rounded_pixmap = QPixmap(pixmap.size())
    rounded_pixmap.fill(Qt.GlobalColor.transparent)

    # 使用 QPainter 绘制圆角图片
    painter = QPainter(rounded_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
    path = QPainterPath()
    path.addRoundedRect(QRectF(pixmap.rect()), radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(pixmap.rect(), pixmap)
    painter.end()

    return rounded_pixmap


BOLD_FONT = QFont()
BOLD_FONT.setBold(True)
TITLE_FONT = QFont()
TITLE_FONT.setBold(True)
TITLE_FONT.setPointSize(24)


class Item:
    def __init__(self, insID: int, pageID: int, offset: int, miss: bool, replace: int):
        self._insID = insID
        self._pageID = pageID
        self._offset = offset
        self._miss = miss
        self._replace = replace
