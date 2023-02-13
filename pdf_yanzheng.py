import os
# -*- coding: utf-8 -*-
import PyPDF2
# import chardet
# from chardet import detect as char_detect


def read_pdf(filename):
    try:
        pdfFileObj = open(filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
        print(filename, "pages cnt:", pdfReader.numPages)
        pdfFileObj.close()
        with open(rf'D:\文件/结果.txt', 'a', encoding='utf-8') as f:
            f.write(f'{filename} pages cnt: {pdfReader.numPages}\n')
    except:
        print(filename, "pages cnt: ERROR")
        with open(rf'D:\文件/结果.txt', 'a', encoding='utf-8') as f:
            f.write(f'{filename} pages cnt: ERROR\n')


if __name__ == "__main__":
    path = r"\\192.168.2.138\\iciseePDF\\datasheet\\20230105"  # 待读取的文件夹
    path_list = os.listdir(path)
    for p in path_list:
        # print(path + '\\\\'+p)
        read_pdf(path + '\\\\' + p)
