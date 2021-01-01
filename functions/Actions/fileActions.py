# -*- coding: utf-8 -*-
import time
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from .FormatTypes.pdf2excel import pdf2excel
from .FormatTypes.pdf2jpg import pdf2jpg
from .FormatTypes.pdf2ppt import pdf2ppt
from .FormatTypes.pdf2word import pdf2word
from .FormatTypes.pdfcompression import pdfcompression
from .FormatTypes.pdfdecrypt import pdfdecrypt
from .FormatTypes.pdfencrypt import pdfencrypt
from .FormatTypes.pdfmerge import pdfmerge
from .FormatTypes.pdfsplit import pdfsplit


def auth_token(ctype, token, client):
    try:
        cursor = connection.cursor()
        cursor.execute(f'select status from functions_conversionlog where token="{token}";')
        res = cursor.fetchone()
        if res:
            if int(res[0]) == 0:
                cursor.execute(f'UPDATE functions_conversionlog SET ctype="{ctype}", status=1, time="{int(time.time())}", client="{client}" where token="{token}"')
                return True
            else:
                print(f"Token已使用 {token}")
                return False
        else:
            cursor.execute(f'select status from functions_admintoken where token="{token}";')
            admin_res = cursor.fetchone()
            if admin_res:
                if int(admin_res[0]) == 0:
                    cursor.execute(f'UPDATE functions_admintoken SET time="{int(time.time())}" where token="{token}"')
                    return True
                else:
                    print(f"管理员Token已被禁用 {token}")
                    return False
            else:
                print(f"Token不存在 {token}")
                return False
    except Exception as e:
        print(f"Token处理异常 {e}")
        return False


@require_http_methods(['POST'])
def fileAction(request):
    client_data = eval(str(request.body, 'utf-8'))
    con_type = client_data['ctype']
    filelist = client_data['filelist']
    token = client_data['token']
    actdict = {
        'pdf2word': pdf2word,
        'pdf2excel': pdf2excel,
        'pdf2ppt': pdf2ppt,
        'pdf2img': pdf2jpg,
        'pdfencrypt': pdfencrypt,
        'pdfdecrypt': pdfdecrypt,
        'pdfcop': pdfcompression,
        'pdfmerge': pdfmerge,
        'pdfsplit': pdfsplit
    }
    if auth_token(con_type, token, request.META['REMOTE_ADDR']):
        if con_type == "pdfencrypt":
            res = actdict[con_type](filelist, client_data['password'])
        else:
            res = actdict[con_type](filelist)
    else:
        res = {
            'code': 1,
            'msg': '口令错误',
            'data': ''
        }
    return JsonResponse(data=res, status=200)

