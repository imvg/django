# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfpage import PDFTextExtractionNotAllowed


def check(sfile):
    parser = PDFParser(open(sfile, 'rb'))
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed("文字无法被提取")
    else:
        resmag = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(resmag, laparams=laparams)
        interpreter = PDFPageInterpreter(resmag, device)
        res = False
        page = next(PDFPage.create_pages(document))
        interpreter.process_page(page)
        layout = device.get_result()
        for y in layout:
            if (isinstance(y, LTTextBoxHorizontal)):
                res = True
            else:
                res = False
            break
        if res:
            print("成功")
        else:
            print("失败")


if __name__ == '__main__':
    check('/Users/vg/Desktop/2014_PDF.pdf')
