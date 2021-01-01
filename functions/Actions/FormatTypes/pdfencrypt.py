# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.conf import settings


def pdfencrypt(file, password):
    config = settings.PDF_CONFIG
    srcfile = config['upload_dir'] + file
    formatfilename = file
    desfile = config['download_dir'] + formatfilename
    try:
        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(srcfile)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
        pdf_writer.encrypt(user_pwd=password, use_128bit=True)
        with open(desfile, 'wb') as fh:
            pdf_writer.write(fh)
        data = {
            'code': 0,
            'msg': '',
            'data': config['domain'] + formatfilename
        }
        return data
    except:
        data = {
            'code': 1,
            'msg': '转换失败',
            'data': ''
        }
        return data
