# -*- coding: utf-8 -*-
from selenium import webdriver
import time, requests, re, os, django
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.mysite.settings")


def pdfsplit(file):
    now = int(time.time())
    desfile = f"{settings.PDF_CONFIG['download_dir']}{now}.zip"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path='/bin/chromedriver', options=options)
    try:
        browser.get("https://www.ilovepdf.com/split_pdf")
        browser.implicitly_wait(120)
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/div[3]/input').send_keys(f"{settings.PDF_CONFIG['upload_dir']}{file}")
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/ul/li[2]').click()
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
                        'data': settings.PDF_CONFIG['domain'] + f"{now}.zip"
                    }
                    return data
                break
            time.sleep(0.3)
            continue
    except Exception as e:
        browser.close()
        browser.quit()
        data = {
            'code': 0,
            'msg': f'转换失败 {e}',
            'data': ''
        }
        return data

