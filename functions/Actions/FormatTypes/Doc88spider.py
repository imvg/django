# -*- coding: utf-8 -*-
import re
import base64
import time
import os
from reportlab.pdfgen import canvas
from PIL import Image
from django.conf import settings


from selenium import webdriver


def doc88(link):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        driver.implicitly_wait(60)
        docName = driver.find_element_by_xpath('//*[@id="box1"]/div/h1').text
        docMeta = driver.find_element_by_xpath('//*[@id="box1"]/div/div/div[1]').text.encode("gbk", 'ignore').decode("gbk", "ignore")
        # docType = re.split('：', re.split(',', docMeta.replace('  ',',').replace(' ','').strip())[0])[-1]
        docPage = int(re.split('：', re.split(',', docMeta.replace('  ',',').replace(' ','').strip())[1])[-1].replace('页',''))
        driver.implicitly_wait(3)
        try:
            driver.find_element_by_xpath('//*[@id="continueButton"]/i').click()
        except:
            pass
        driver.implicitly_wait(60)
        pageHeight = driver.execute_script("return document.body.scrollHeight")
        time.sleep(5)
        for d in range(1, int(pageHeight), 100):
            driver.execute_script(f"window.scrollTo(0,{d})")
            time.sleep(0.15)
        time.sleep(3)
        pageList = []
        for page in range(1, docPage+1):
            js = '''if (document.getElementById('page_' + %s) !== null) {
        var pageCanvas = document.getElementById('page_' + %s);
        var image = pageCanvas.toDataURL("image/png");
        return image
    }
    ''' % (page, page)
            docImg = driver.execute_script(js)
            b64 = docImg.replace('data:image/png;base64,', '')
            pageData = base64.b64decode(b64)
            now = int(time.time())
            with open(f'{settings.PDF_CONFIG["upload_dir"]}{now}_{page}.png', 'wb') as f:
                f.write(pageData)
            pageList.append(f'{settings.PDF_CONFIG["upload_dir"]}{now}_{page}.png')
        driver.close()
        driver.quit()
        if makePdf(f"{settings.PDF_CONFIG['download_dir']}{docName}.pdf", pageList):
            for pageFile in pageList: os.remove(pageFile)
            data = {
                'code': 0,
                'msg': '',
                'data': settings.PDF_CONFIG['domain'] + docName+".pdf"
            }
            return data
        else:
            data = {
                'code': 1,
                'msg': '合并文件失败, 请联系站长',
                'data': ''
            }
            return data
    except Exception as e:
        data = {
            'code': 1,
            'msg': '解析文件失败, 请联系站长',
            'data': ''
        }
        print(e)
        return data


def makePdf(pdfPath, imgList):
    try:
        pages = 0
        cover = Image.open(imgList[0])
        width, height = cover.size
        c = canvas.Canvas(pdfPath, pagesize=(width, height))
        for i in imgList:
            c.drawImage(i, 0, 0, width, height)
            c.showPage()
            pages = pages + 1
        c.save()
        return True
    except Exception as e:
        print(e)
        return False

