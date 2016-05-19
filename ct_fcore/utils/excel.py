# -*- coding:utf-8 -*-
import xlrd

class ExcelRead(object):
    def __init__(self, uri, index = 0):
        '''打开并处理Excel

        :param uri: 文件资源地址
        :param index: 需要打开的sheet的编号
        :return:
        '''
        self.bk = xlrd.open_workbook(uri)
        self.table = self.bk.sheet_by_index(0)

    def getSize(self):
        '''得到sheet的尺寸

        :return: (行数, 列数)
        '''
        return (self.table.nrows, self.table.ncols)

    def get(self, row, col):
        '''得到sheet中某个单元格的数据

        :param row: 行号
        :param col: 列号
        :return: 目标单元格的数据
        '''
        return self.table.cell(row, col).value