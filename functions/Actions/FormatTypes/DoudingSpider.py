# -*- coding: utf-8 -*-
import re
import base64
import time
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.pdfgen import canvas
from PIL import Image
import os

from selenium import webdriver


def spider(link):
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        driver.implicitly_wait(60)
        docName = driver.find_element_by_xpath('//*[@id="page"]/div[2]/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text
        docPage = int(driver.find_element_by_xpath('//*[@id="page"]/div[1]/div[1]/div[3]/div[1]/span').text.replace('/', ''))
        driver.implicitly_wait(60)
        pageHeight = driver.execute_script("return document.body.scrollHeight")
        time.sleep(5)
        for d in range(1, int(pageHeight), 100):
            driver.execute_script(f"window.scrollTo(0,{d})")
            time.sleep(0.15)
        time.sleep(3)
        pageList = []
        for page in range(1, docPage + 1):
            js = '''const rootEl = document.getElementsByClassName("hkswf-content")[%s]
const pageCanvas = rootEl.querySelector('canvas');
var image = pageCanvas.toDataURL("image/png");
console.log(image)
    ''' % (page - 1)
            docImg = driver.execute_script(js)
            b64 = docImg.replace('data:image/png;base64,', '')
            pageData = base64.b64decode(b64)
            now = int(time.time())
            with open(f'temp/{now}_{page}.png', 'wb') as f:
                f.write(pageData)
            pageList.append(f'temp/{now}_{page}.png')
        driver.close()
        driver.quit()
        makePdf(f"temp/{docName}.pdf", pageList)
        for pageFile in pageList: os.remove(pageFile)
        return f"temp/{docName}.pdf"
    except Exception as e:
        print(f"下载文件失败 {e}")


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
        return pdfPath
    except Exception as e:
        print(f"合并PDF失败 {e}")


if __name__ == '__main__':
    spider('https://jz.docin.com/p-2557621859.html?building=1&fid=2569&sid=0')
