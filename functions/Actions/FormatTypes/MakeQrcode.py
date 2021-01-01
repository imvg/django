# -*- coding: utf-8 -*-
import time, requests
from selenium import webdriver


def MakeQrcode(dataurl, save_path, style):
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        browser = webdriver.Chrome(options=options)
        browser.implicitly_wait(120)
        browser.get("https://www.unitag.io/qrcode")
        browser.find_element_by_xpath('//*[@id="url-url"]').send_keys(dataurl)
        browser.find_element_by_xpath('//*[@id="social-wrapper"]/div/div/button').click()
        style(browser)
        time.sleep(1)
        res = browser.find_element_by_xpath('/html/body/div[2]/div[2]/section/div/div[1]/div[2]/div/div[2]/div[1]/div/img').get_attribute('src')
        open(save_path, "wb").write(requests.get(res).content)
        return True
    except Exception as e:
        print("asdasd", e)
        return False


def style1(browser):
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[2]').click()
    browser.find_element_by_xpath('//*[@id="options-settings"]/div[2]/div[2]/div[3]/div[1]/div/div[1]').click()
    browser.find_element_by_xpath('//*[@id="color1"]').send_keys('929619')
    browser.find_element_by_xpath('//*[@id="color2"]').send_keys('9c23ba')


def style2(browser):
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[3]').click()
    browser.find_element_by_xpath('//*[@id="module-choose"]/div[2]/a[5]').click()
    browser.find_element_by_xpath('//*[@id="eye-choose"]/div[2]/a[12]').click()
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[2]').click()
    browser.find_element_by_xpath('//*[@id="options-settings"]/div[2]/div[2]/div[3]/div[1]/div/div[1]').click()
    browser.find_element_by_xpath('//*[@id="color1"]').send_keys('bf648d')
    browser.find_element_by_xpath('//*[@id="color2"]').send_keys('2d7da8')


def style3(browser):
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[3]').click()
    browser.find_element_by_xpath('//*[@id="module-choose"]/div[2]/a[9]').click()
    browser.find_element_by_xpath('//*[@id="eye-choose"]/div[2]/a[18]').click()
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[2]').click()
    browser.find_element_by_xpath('//*[@id="options-settings"]/div[2]/div[2]/div[3]/div[1]/div/div[1]').click()
    browser.find_element_by_xpath('//*[@id="color1"]').send_keys('e08145')
    browser.find_element_by_xpath('//*[@id="color2"]').send_keys('4c61d9')


def style4(browser):
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[3]').click()
    browser.find_element_by_xpath('//*[@id="module-choose"]/div[2]/a[14]').click()
    browser.find_element_by_xpath('//*[@id="eye-choose"]/div[2]/a[10]').click()
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[2]').click()
    browser.find_element_by_xpath('//*[@id="options-settings"]/div[2]/div[2]/div[3]/div[1]/div/div[1]').click()
    browser.find_element_by_xpath('//*[@id="color1"]').send_keys('3abfc9')
    browser.find_element_by_xpath('//*[@id="color2"]').send_keys('d94cbf')


def style5(browser):
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[3]').click()
    browser.find_element_by_xpath('//*[@id="module-choose"]/div[2]/a[6]').click()
    browser.find_element_by_xpath('//*[@id="eye-choose"]/div[2]/a[9]').click()
    browser.find_element_by_xpath('//*[@id="options-menu"]/div[2]/a[2]').click()
    browser.find_element_by_xpath('//*[@id="options-settings"]/div[2]/div[2]/div[3]/div[1]/div/div[1]').click()
    browser.find_element_by_xpath('//*[@id="color1"]').send_keys('3a46c9')
    browser.find_element_by_xpath('//*[@id="color2"]').send_keys('4cd0d9')
