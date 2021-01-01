# -*- coding: utf-8 -*-
from selenium import webdriver
import time, requests, re, os
from django.conf import settings


def pdf2word(file):
    config = settings.PDF_CONFIG
    srcfile = config['upload_dir'] + file
    formatfilename = re.split('\.', file)[0] + '.docx'
    desfile = config['download_dir'] + formatfilename

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path='/bin/chromedriver', options=options)
    try:
        browser.get("https://www.ilovepdf.com/zh-cn/pdf_to_word")
        browser.implicitly_wait(120)
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div[3]/input').send_keys(srcfile)
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
            'code': 0,
            'msg': '转换失败',
            'data': ''
        }
        return data


def ilovepdf(file):
    config = settings.PDF_CONFIG
    srcfile = config['upload_dir'] + file
    formatfilename = re.split('\.', file)[0] + '.docx'
    desfile = config['download_dir'] + formatfilename

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path='/bin/chromedriver', options=options)
    try:
        browser.get("https://www.ilovepdf.com/zh-cn/pdf_to_word")
        browser.implicitly_wait(120)
        browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div[3]/input').send_keys(srcfile)
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
            'code': 0,
            'msg': '转换失败',
            'data': ''
        }
        return data


def speedpdf(file):
    config = settings.PDF_CONFIG
    srcfile = config['upload_dir'] + file
    formatfilename = re.split('\.', file)[0] + '.docx'
    desfile = config['download_dir'] + formatfilename

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=options)
    try:
        browser.get("https://speedpdf.com/en/convert/pdf-to-word")
        browser.implicitly_wait(120)
        browser.find_element_by_xpath('//*[@id="fileInputs"]').send_keys(srcfile)
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="result1_0"]').click()
        start = 1
        while True:
            if start >= 10:
                break
            try:
                print(start)
                file_url = browser.find_element_by_xpath('//*[@id="result1_0"]/div/img').get_attribute('url')
                browser.close()
                browser.quit()
                open(desfile, "wb").write(requests.get(file_url).content)
                data = {
                    'code': 0,
                    'msg': '',
                    'data': config['domain'] + formatfilename
                }
                return data
            except:
                time.sleep(1)
                start += 1
                continue
    except Exception as e:
        print(e)
        browser.close()
        browser.quit()
        data = {
            'code': 1,
            'msg': '转换失败',
            'data': ''
        }
        return data

