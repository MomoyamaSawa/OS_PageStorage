from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
from config import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from core.tool import *
from core.instruction import *
from core.memory import *
import copy


# TODO 有时间还想搞一个状态机qwq


class MySpinbox(SpinBox):
    def __init__(self, min, max):
        super().__init__()
        self.setMaximum(max)
        self.setMinimum(min)


class Slider(QWidget):
    insNumSignal = pyqtSignal(int)
    pageInsNumSignal = pyqtSignal(int)
    pageNumSignal = pyqtSignal(int)
    algoSignal = pyqtSignal(int)
    orderSignal = pyqtSignal(int)

    def __init__(self, config: GlobalConfig):
        super().__init__()
        self.setFixedWidth(SLIDER_WIDTH)
        self.config = copy.copy(config)

        # 添加图片
        self.image_label = QLabel(self)
        pixmap = QPixmap(PROFILE_PATH)
        pixmap = pixmap.scaled(
            self.width() // 2, self.height() // 2, Qt.AspectRatioMode.KeepAspectRatio
        )
        rounded_pixmap = getRoundedPixmap(pixmap, 20)  # 获取圆角图片
        self.image_label.setPixmap(rounded_pixmap)
        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.label1 = QLabel("作业指令总数")
        self.label1.setFont(BOLD_FONT)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.option1 = MySpinbox(10, 1000)
        self.option1.setValue(config.insNum)
        self.option1.valueChanged.connect(
            lambda: self.insNumSignal.emit(self.option1.value())
        )
        self.label2 = QLabel("每页存放指令数")
        self.label2.setFont(BOLD_FONT)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.option2 = MySpinbox(5, 25)
        self.option2.setValue(config.pageInsNum)
        self.option2.valueChanged.connect(
            lambda: self.pageInsNumSignal.emit(self.option2.value())
        )
        self.label3 = QLabel("作业占用内存页数")
        self.label3.setFont(BOLD_FONT)
        self.label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.option3 = MySpinbox(2, 12)
        self.option3.setValue(config.pageNum)
        self.option3.valueChanged.connect(
            lambda: self.pageNumSignal.emit(self.option3.value())
        )
        self.label4 = QLabel("页面置换算法")
        self.label4.setFont(BOLD_FONT)
        self.label4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.option4 = ComboBox()
        self.option4.addItems(["LRU", "FIFO"])
        self.option4.setCurrentIndex(config.algo)
        self.option4.currentIndexChanged.connect(
            lambda: self.algoSignal.emit(self.option4.currentIndex())
        )
        self.label5 = QLabel("指令执行顺序")
        self.label5.setFont(BOLD_FONT)
        self.label5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.option5 = ComboBox()
        self.option5.addItems(["随机执行", "预设执行"])
        self.option5.setCurrentIndex(config.order)
        self.option5.currentIndexChanged.connect(
            lambda: self.orderSignal.emit(self.option5.currentIndex())
        )
        self.vlayout = QVBoxLayout()
        # 创建一个横线控件并设置样式
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.label6 = QLabel("缺页数")
        self.label6.setFont(BOLD_FONT)
        self.label6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label7 = QLabel("None")
        self.label7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label8 = QLabel("缺页率")
        self.label8.setFont(BOLD_FONT)
        self.label8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label9 = QLabel("None")
        self.label9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__initLayout()
        self.__initStyle()

    def __initLayout(self):
        # 将图片控件添加到布局中
        self.vlayout.addSpacing(10)
        self.vlayout.addWidget(self.image_label)
        self.vlayout.addWidget(self.label1)
        self.vlayout.addSpacing(-20)
        self.vlayout.addWidget(self.option1)
        self.vlayout.addWidget(self.label2)
        self.vlayout.addSpacing(-20)
        self.vlayout.addWidget(self.option2)
        self.vlayout.addWidget(self.label3)
        self.vlayout.addSpacing(-20)
        self.vlayout.addWidget(self.option3)
        self.vlayout.addWidget(self.label4)
        self.vlayout.addSpacing(-20)
        self.vlayout.addWidget(self.option4)
        self.vlayout.addWidget(self.label5)
        self.vlayout.addSpacing(-20)
        self.vlayout.addWidget(self.option5)
        self.vlayout.addSpacing(20)
        # 将横线控件添加到布局中
        self.vlayout.addWidget(self.line)
        self.vlayout.addWidget(self.label6)
        self.vlayout.addSpacing(-20)
        self.vlayout.addWidget(self.label7)
        self.vlayout.addSpacing(-10)
        self.vlayout.addWidget(self.label8)
        self.vlayout.addSpacing(-20)
        self.vlayout.addWidget(self.label9)
        self.setLayout(self.vlayout)

    def __initStyle(self):
        self.line.setStyleSheet("background-color: rgba(128, 128, 128, 64);")

    def paintEvent(self, event):
        # 设置圆角和颜色
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(SLIDER_COLOR)
        color.setAlpha(64)
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect()
        radius = 20.0  # 圆角半径，可以根据需要调整
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        painter.drawPath(path)

    def setAll(self, insNum: int, missRate: float):
        self.label7.setText(str(insNum))
        self.label9.setText("{:.3%}".format(missRate))

    def reset(self):
        self.label7.setText("None")
        self.label9.setText("None")


class PageCard(QFrame):
    def __init__(self, pageID: int, num: int, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "background-color: white; border-radius: 20px;"
        )  # 设置背景颜色为白色，边框圆角为20像素
        self.setFixedWidth(125)
        self.ID = pageID
        self.label = QLabel(f"第{pageID}页")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels: list[QLabel] = []
        self.layout = QVBoxLayout(self)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(10)
        for i in range(num):
            label = QLabel(f"{i}", self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # 这里圆角设置不好还看不出来
            label.setStyleSheet("background-color: #BFC8D7; border-radius: 10px;")
            label.setFixedHeight(30)
            label.setFixedWidth(90)
            self.labels.append(label)
            self.layout.addWidget(label)
            self.layout.addSpacing(-5)
        self.layout.addSpacing(5)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

    def getID(self) -> int:
        return self.ID


class RoundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(SLIDER_COLOR)
        color.setAlpha(64)
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)


class Window1(QWidget):
    def __init__(self, config: GlobalConfig):
        super().__init__()
        self.lastPage = None
        self.lastOffset = None
        self.config = copy.copy(config)
        self.pageNum = 0
        self.pages: list[PageCard] = [None] * config.pageNum
        self.label = QLabel("内存中的界面展示")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(TITLE_FONT)
        self.roundWidget = RoundWidget(self)
        self.scrollArea = SmoothScrollArea(self.roundWidget)
        self.scrolWidget = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrolWidget)
        self.scrollArea.setViewportMargins(0, 5, 0, 5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.flowLayout = FlowLayout(self.scrolWidget, isTight=True, needAni=True)
        # customize animation
        self.flowLayout.setAnimation(250, QEasingCurve.Type.OutQuad)
        self.vlayout = QVBoxLayout()
        self.__initLayout()
        self.__initStyle()

        # INFO 这里的定时器是为了让布局可以更新，因为这个动画效果结束的信号发出来了也不代表动画影响消失了，直接更新好像没用，所以要一直检测，而且还用了第三方库的东西，错综复杂了属于是
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(lambda: self.flowLayout.update())
        self.timer.start()

    def __initLayout(self):
        self.flowLayout.setContentsMargins(10, 10, 10, 10)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(10)
        self.vlayout.addWidget(self.label)
        self.vlayout.addSpacing(5)
        self.vlayout.addWidget(self.roundWidget)
        self.setLayout(self.vlayout)
        self.roundWidget.setLayout(QVBoxLayout())
        self.roundWidget.layout().addWidget(self.scrollArea)
        self.scrolWidget.setLayout(self.flowLayout)

    def __initStyle(self):
        # 这个一定要标类名吗？
        self.scrollArea.setStyleSheet(
            "QScrollArea { background-color: transparent; border: none; }"
        )
        self.scrolWidget.setStyleSheet(
            "QWidget { background-color: transparent; border: none; }"
        )

    def addPage(self, pageID: int, pos: int):
        # INFO 因为本来这个组件就有动画效果，那其实我就可以把里面的东西拉一下位置，然后让他重新布局它就有动画了
        # 还有这里明显的问题就是这个流式布局也有动画，然后动画没播完确实是不能重新布局，要等
        if self.pages[pos] != None:
            item = self.flowLayout.takeAt(pos)
            item.deleteLater()
        self.pages[pos] = PageCard(pageID, self.config.pageInsNum)
        self.flowLayout.addWidget(self.pages[pos])
        self.pageNum += 1
        self.pages[pos].move(500, 500)

    def update(self, check: int, spaceList: list, pageID: int, offset: int):
        spaceList.reverse()
        if check != -1:
            self.addPage(pageID, check)
        pages = []
        labels = []
        for i in range(len(self.pages)):
            if self.pages[i] != None:
                labels.append(self.pages[i].getID())
                # INFO takeAt之后标签的顺序就变了
                pages.append(self.flowLayout.takeAt(0))
        for i in range(len(spaceList)):
            if spaceList[i] != None:
                index = labels.index(spaceList[i])
                self.pages[i] = pages[index]
                self.flowLayout.addWidget(pages[index])
            else:
                self.pages[i] = None
        index = spaceList.index(pageID)
        if self.lastPage != None:
            self.lastPage.labels[self.lastOffset].setStyleSheet(
                "background-color: #BFC8D7; border-radius: 10px;"
            )
        self.pages[index].labels[offset].setStyleSheet(
            "background-color: #E2D2D2; border-radius: 10px;"
        )
        self.lastPage = self.pages[index]
        self.lastOffset = offset

    def reset(self, config: GlobalConfig):
        self.pageNum = 0
        item_list = list(range(self.flowLayout.count()))
        item_list.reverse()
        for i in item_list:
            item = self.flowLayout.takeAt(i)
            if item:
                item.deleteLater()
        self.pages = [None] * config.pageNum
        self.config = copy.copy(config)
        self.lastPage = None
        self.lastOffset = None


class Window2(QWidget):
    def __init__(self):
        super().__init__()
        self.num = 0
        self.label = QLabel("已执行指令")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(TITLE_FONT)
        self.tableView = TableWidget(self)
        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(60)
        self.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.setColumnCount(5)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        songInfos = []
        songInfos += songInfos
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.tableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.resizeColumnsToContents()
        self.tableView.setHorizontalHeaderLabels(["执行序号", "物理地址", "是否缺页", "换出页", "需求页"])

        self.vlayout = QVBoxLayout()
        self.__initLayout()
        self.__initStyle()

    def __initLayout(self):
        self.vlayout.addWidget(self.label)
        self.vlayout.addSpacing(10)
        self.vlayout.addWidget(self.tableView)
        self.setLayout(self.vlayout)

    def __initStyle(self):
        # 不覆盖之前的
        current_style_sheet = self.tableView.styleSheet()
        new_style_sheet = "{border-radius: 20px;}"
        self.tableView.setStyleSheet(current_style_sheet + new_style_sheet)

    def reset(self):
        self.tableView.clearContents()
        self.num = 0

    def setItem(self, item: Item):
        self.tableView.insertRow(self.num)
        self.tableView.setItem(self.num, 0, QTableWidgetItem(str(self.num)))
        self.tableView.setItem(self.num, 1, QTableWidgetItem(str(item._insID)))
        self.tableView.setItem(self.num, 2, QTableWidgetItem(str(item._miss)))
        self.tableView.setItem(self.num, 3, QTableWidgetItem(str(item._replace)))
        self.tableView.setItem(self.num, 4, QTableWidgetItem(str(item._pageID)))
        last_row = self.tableView.item(self.num, 0)
        self.tableView.scrollToItem(last_row)
        self.num += 1


class Window3(QWidget):
    resetSignal = pyqtSignal()
    sinSignal = pyqtSignal()
    continueSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.buttom1 = PrimaryPushButton("单步执行", self, FIF.CHEVRON_RIGHT)
        self.buttom2 = PrimaryPushButton("连续执行", self, FIF.SEND_FILL)
        self.buttom3 = PushButton("重置", self, FIF.SYNC)
        self.buttom3.clicked.connect(self.resetSignal.emit)
        self.buttom1.clicked.connect(self.sinSignal.emit)
        self.buttom2.clicked.connect(self.continueSignal.emit)

        self.hlayout = QHBoxLayout()
        self.__initUI()

    def __initUI(self):
        self.hlayout.addWidget(self.buttom1)
        self.hlayout.addWidget(self.buttom2)
        self.hlayout.addWidget(self.buttom3)
        self.setLayout(self.hlayout)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle(TITLE_NAME)
        self.resize(MAIN_WINDOW_SIZE["w"], MAIN_WINDOW_SIZE["h"])
        self.__initConfig()
        self.insNum = 0
        self.missNum = 0

        self.mainLayout = QHBoxLayout()
        self.subLayout0 = QVBoxLayout()
        self.subLayout00 = QHBoxLayout()

        self.timer = QTimer()
        self.timer.setInterval(1000)

        self.slider = Slider(self.config)
        self.window1 = Window1(self.config)
        self.window2 = Window2()
        self.window3 = Window3()
        self.stateTooltip = None
        self.__reset()
        self.window3.resetSignal.connect(self.__reset)
        self.window3.resetSignal.connect(self.createSuccessInfoBar)
        self.window3.continueSignal.connect(self.continueRead)
        self.window3.continueSignal.connect(self.onButtonClicked)
        self.slider.insNumSignal.connect(self.changeInsNum)
        self.slider.pageInsNumSignal.connect(self.changePageInsNum)
        self.slider.pageNumSignal.connect(self.changePageNum)
        self.slider.algoSignal.connect(self.changeAlgo)
        self.slider.orderSignal.connect(self.changeOrder)
        self.showDia = False
        self.slider.insNumSignal.connect(self.showDialog)
        self.slider.pageInsNumSignal.connect(self.showDialog)
        self.slider.pageNumSignal.connect(self.showDialog)
        self.slider.algoSignal.connect(self.showDialog)
        self.slider.orderSignal.connect(self.showDialog)

        self.__initUI()

    def changeOrder(self, order: int):
        self.config.order = order

    def changeAlgo(self, algo: int):
        self.config.algo = algo

    def changeInsNum(self, num: int):
        self.config.insNum = num

    def changePageInsNum(self, num: int):
        self.config.pageInsNum = num

    def changePageNum(self, num: int):
        self.config.pageNum = num

    def continueRead(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def __initUI(self):
        self.subLayout00.addWidget(self.window1)
        self.subLayout00.addWidget(self.window2)
        self.subLayout0.addLayout(self.subLayout00)
        self.subLayout0.addWidget(self.window3)
        self.mainLayout.addWidget(self.slider)
        self.mainLayout.addLayout(self.subLayout0)
        self.setLayout(self.mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(BACK_COLOR)
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

    def __reset(self):
        self.timer.stop()
        self.insNum = 0
        self.missNum = 0
        self.slider.reset()
        self.window1.reset(self.config)
        self.window2.reset()
        self.insCon = InsController(self.config.insNum, self.config.pageInsNum)
        self.memCon = MemController(  # 这里的参数是不是应该改一下？
            self.config.pageNum,
            self.config.pageInsNum,
            MemOption(self.config.algo),
        )
        self.reader = Reader(self.insCon, self.memCon, self.config)
        self.reader.finishSignal.connect(self.finish)
        self.memCon.signal.connect(self.__update)
        self.memCon.memSignal.connect(self.window1.update)
        self.window3.sinSignal.connect(self.reader.read)
        self.timer.timeout.connect(self.reader.read)
        if self.stateTooltip:
            self.stateTooltip.setState(True)
            self.stateTooltip = None

    def finish(self):
        title = "指定数量的指令已全部完成😊"
        content = """请重置！！！！！"""
        w = MessageBox(title, content, self)
        w.exec()
        self.showDia = True

    def __initConfig(self):
        self.config = GlobalConfig()

    def __update(self, item: Item):
        self.window2.setItem(item)
        self.insNum += 1
        self.missNum += 1 if item._miss else 0
        self.slider.setAll(self.missNum, self.missNum / self.insNum)

    def showDialog(self):
        if self.showDia:
            return
        title = "请注意！！这是只有一次的提示！！！"
        content = """修改侧边栏参数后需要点击右下角重置按钮后才会生效😊"""
        # w = MessageDialog(title, content, self)   # Win10 style message box
        w = MessageBox(title, content, self)
        w.exec()
        self.showDia = True

    def createSuccessInfoBar(self):
        # convenient class mothod
        InfoBar.success(
            title="成功！",
            content="已重置😊",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self,
        )

    def onButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent("结束啦 😆")
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip("自动连续执行", "执行中（再次点击以结束）", self)
            geo = self.geometry()
            self.stateTooltip.move(geo.width() // 2, 15)
            self.stateTooltip.show()


if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建窗口对象并显示
    window = MyWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec())
