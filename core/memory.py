from enum import Enum
from core.tool import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from abc import *


class MemOption(Enum):
    LRU = 0
    FIFO = 1


class MemAlgorithm(ABC):
    @abstractmethod
    def replace(self, pageID: int, list: list) -> list[int, list, int]:
        pass

    @abstractmethod
    def check(self, pageID: int, list: list, new: bool) -> list:
        pass


class MemController(QObject):
    # insID, pageID, offset, miss, replace
    signal = pyqtSignal(Item)
    memSignal = pyqtSignal(int, list, int, int)

    def __init__(self, space: int, pageLen: int, op: MemOption):
        super().__init__()
        self.check = -1
        self.space = space
        self.changeList = []
        # 创建固定大小的内存空间
        self.spaceList = [None] * space
        self.op = op
        self.pageLen = pageLen
        if op == MemOption.LRU:
            self.al = LRU()
        elif op == MemOption.FIFO:
            self.al = FIFO()

    def __check(self, pageID: int) -> bool:
        # 检查页是否在内存中
        # 在内存中
        if pageID in self.spaceList:
            self.spaceList = self.al.check(pageID, self.spaceList, False)
            return True
        # 内存中有空位
        elif None in self.spaceList:
            index = len(self.spaceList) - self.spaceList[::-1].index(None) - 1
            self.spaceList[index] = pageID
            self.spaceList = self.al.check(pageID, self.spaceList, True)
            self.check = len(self.spaceList) - index - 1
            return True
        # 不在内存中，且内存已满
        else:
            return False

    def inMem(self, ins: int):
        pageID, offset = getPage(ins, self.pageLen)
        # 算法实现写入或替换
        # 首先要检查是不是已经在内存中吧，如果已经在内存中或者没装满都返回true
        miss = None
        repalce = None
        self.check = -1
        if not self.__check(pageID):
            miss = True
            repalce, self.spaceList, self.check = self.al.replace(
                pageID, self.spaceList
            )
        else:
            miss = False
        # 同时要信号槽更新界面
        self.signal.emit(Item(ins, pageID, offset, miss, repalce))
        self.memSignal.emit(self.check, self.spaceList, pageID, offset)


class LRU(MemAlgorithm):
    def replace(self, pageID: int, list: list) -> list[int, list, int]:
        # 置换最前面的元素，其他前移，把pageID放到最后
        replace = list[0]
        list = list[1:] + [pageID]
        check = len(list) - 1
        return replace, list, check

    def check(self, pageID: int, list: list, new: bool) -> list:
        # 移动元素到最后
        index = list.index(pageID)
        list = list[:index] + list[index + 1 :] + [list[index]]
        return list


class FIFO(MemAlgorithm):
    def replace(self, pageID: int, list: list) -> list[int, list, int]:
        # 置换最后面的元素，其他前移，把pageID放到最后
        replace = list[0]
        list = list[1:] + [pageID]
        check = len(list) - 1
        return replace, list, check

    def check(self, pageID: int, list: list, new: bool) -> list:
        if new:
            index = list.index(pageID)
            list = list[:index] + list[index + 1 :] + [list[index]]
        return list
