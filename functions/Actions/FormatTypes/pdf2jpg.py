# -*- coding: utf-8 -*-
from selenium import webdriver
import time, requests, re
from django.conf import settings
import pdfplumber


def pdf2jpg(file):
    config = settings.PDF_CONFIG
    srcfile = config['upload_dir'] + file
    f = pdfplumber.open(srcfile)
    maxpage = len(f.pages)
    f.close()
    if maxpage != 1:
        formatfilename = re.split('\.', file)[0] + '.zip'
    else:
        formatfilename = re.split('\.', file)[0] + '.jpg'
    desfile = config['download_dir'] + formatfilename

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path='/bin/chromedriver', options=options)
    try:
        browser.get("https://www.ilovepdf.com/zh-cn/pdf_to_jpg")
        browser.implicitly_wait(120)
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/div[3]/input').send_keys(srcfile)
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/button').click()
        while True:
            if "download" in browser.current_url:
                for s in browser.find_elements_by_xpath('//*[@id="pickfiles"]'):
                    file_url = s.get_attribute('href')
                    browser.close()
                    browser.quit()
                    open(desfile, "wb").write(requests.get(file_url).content)
                    data = {
                        'code': 0,
                        'msg': '',
                        'data': config['domain'] + formatfilename
                    }
                    return data
                break
            time.sleep(0.3)
            continue
    except:
        browser.close()
        browser.quit()
        data = {
            'code': 1,
            'msg': '转换失败',
            'data': ''
        }
        return data
