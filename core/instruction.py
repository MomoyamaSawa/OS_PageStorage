from core.tool import *
from core.memory import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import random, copy
from core.tool import *


class InsController:
    def __init__(self, insNum: int, pageLen: int):
        self.insNum = insNum
        self.pageLen = pageLen
        # 分页
        self.pageNum, self.lastPageLen = getPage(insNum, pageLen)
        self.nowIns = None

    def getInstruction(self) -> int:
        # 随机生成指令
        # 如果是第一次生成是随机生成指令
        if self.nowIns is None:
            self.nowIns = self.__getRandomFir()
        # 如果不是第一次就采取随机策略 TODO 让这个随即策略的参数可以改吧？
        else:
            randomN = random.randint(0, 100)
            # 50%概率是顺序执行
            if randomN <= 50:
                self.nowIns += 1
                if self.nowIns >= self.insNum:
                    self.nowIns = 0
            # 25%概率是均与分布在前地址部份
            elif randomN <= 75:
                if self.nowIns - 1 <= 0:
                    self.nowIns = random.randint(self.nowIns + 1, self.insNum - 1)
                self.nowIns = random.randint(0, self.nowIns - 1)
            # 25%概率是均与分布在后地址部份
            else:
                if self.nowIns + 1 >= self.insNum:
                    self.nowIns = random.randint(0, self.nowIns - 1)
                self.nowIns = random.randint(self.nowIns + 1, self.insNum - 1)
        return self.nowIns

    def __getRandomFir(self) -> int:
        # 随机生成第一条指令
        return random.randint(0, self.insNum - 1)


class Reader(QObject):
    finishSignal = pyqtSignal()

    def __init__(self, con: InsController, mem: MemController, config: GlobalConfig):
        super().__init__()
        self.config: GlobalConfig = copy.copy(config)
        self.insCon = con
        self.pageNotNum = 0
        self.memCon = mem
        self.order = None
        self.num = 0
        if self.config.order == 1:
            self.order = open(FILE_PATH, "r")

    def read(self):
        self.num += 1
        ins = None
        if self.config.order == 1:
            ins = self.order.readline()
            if ins == "" or None:
                self.finishSignal.emit()
                ins = None
            else:
                ins = int(ins)
        else:
            # 执行读取指令，要去随机一条指令然后检查memory完成替换什么的
            ins = self.insCon.getInstruction()
            if self.num >= self.config.insNum:
                self.finishSignal.emit()
        if ins is not None:
            self.memCon.inMem(ins)

    def __del__(self):
        if self.config.order == 1:
            self.order.close()
