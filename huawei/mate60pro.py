#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2023/10/7 10:52
import time

from fengluU import n2u
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def mate60pro():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    # option.add_argument('--no-sandbox')
    # option.add_argument('--disable-gpu')
    option.add_argument('--start-maximized')
    option.add_argument(f'user-agent={headers.get("User-Agent")}')
    webdriver.Chrome()
    service = webdriver.ChromeService(executable_path='/Users/king/CODEMONKEY/App/chromedriver-mac-x64')
    browser = webdriver.Chrome(options=option)
    browser.get('https://www.vmall.com/product/10086009079805.html#2601010452815')
    browser.implicitly_wait(1)
    browser.find_element(By.ID, 'top-index-loginUrl').click()
    browser.implicitly_wait(2)
    browser.find_element(By.CSS_SELECTOR, '.hwid-icon-ic_third_weixin.hwid_icon_padding-20').click()
    # ovm = browser.find_element(By.CSS_SELECTOR, '[ht="click_authentication_otherWay"]')
    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(browser, timeout=600, poll_frequency=.2, ignored_exceptions=errors)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[ht="click_authentication_otherWay"]'))).click()

    browser.implicitly_wait(1)
    browser.find_element(By.CSS_SELECTOR, '[ht="click_openOtherAuthWay_1"]').click()
    browser.implicitly_wait(1)
    browser.find_element(By.CSS_SELECTOR, '[ht="click_authentication_getAuthcode"]').click()

    authcode = browser.find_element(By.CSS_SELECTOR, '[ht="input_authentication_authcode"]')
    wait.until(lambda d: len(authcode.get_attribute('value')) == 6)
    browser.find_element(By.CSS_SELECTOR, '[ht="click_dialog_rightbtn"]').click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[ht="click_login_trustBrowser_trust"]'))).click()

    # 循环监测是否开卖
    idx = 1
    btn = None
    while True:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="雅川青"]'))).click()
        browser.find_element(By.CSS_SELECTOR, 'a[title="12GB+512GB"]').click()
        browser.find_element(By.CSS_SELECTOR, 'a[title="全款购买"]').click()
        btns = browser.find_elements(By.XPATH, '//*[@id="pro-operation"]/a')
        btn = btns[len(btns) - 1]
        btn_text = btn.find_element(By.TAG_NAME, 'span').text
        if btn_text == '暂不售卖':
            print(f'第{n2u.number2upper(idx)}次刷新结果：' + btn_text)
            idx += 1
            browser.refresh()
            time.sleep(5)
        else:
            print("开抢！")
            break
    btn.click()

    time.sleep(3000)

if __name__ == '__main__':
    mate60pro()
