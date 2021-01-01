# -*- coding: utf-8 -*-
import hashlib, re
from functools import partial
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.conf import settings


def md5(data, block_size=65536):
    m = hashlib.md5()
    for item in iter(partial(data.read, block_size), b''):
        m.update(item)
    str_md5 = m.hexdigest()
    return str_md5


@require_http_methods(['POST'])
def upload(request):
    files = request.FILES.getlist('files')
    files_res = []
    for f in files:
        if f.size <= 1024*1024*1024*1024 and re.split("\.", f.name)[-1] in ["pdf","PDF"]:
            md5_code = md5(f)
            filename = f"{settings.PDF_CONFIG['upload_dir']}{md5_code}.pdf"
            with open(filename, 'wb') as wf:
                for chu in f.chunks():
                    wf.write(chu)
            data_dict = {"name": f.name, "dest": f"{settings.PDF_CONFIG['preview']}{md5_code}.pdf"}
            files_res.append(data_dict)
    res = {"code": 0, "msg": "", "data": files_res}
    return JsonResponse(data=res, status=200)
