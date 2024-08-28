import math
import time
import os
import re
import pandas as pd
from tqdm import tqdm
import undetected_chromedriver as uc
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui
import asyncio
import datetime
import random
import chromedriver_autoinstaller
from multiprocessing import Process, Lock, Semaphore
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from unidecode import unidecode
import time
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import re
from selenium.webdriver.support.ui import WebDriverWait
import time
import undetected_chromedriver as uc
from DefOzon.Find_Captcha import Captcha
import requests
import json
from collections import Counter
drivers = []
def updateOzon(e, path, lock,X,Y,positions):
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")
    # options.add_argument(f'--profile-directory=Profile 1')
    driver = uc.Chrome(options=options)
    driver.set_window_size(X, Y)
    driver.set_window_position(*positions, windowHandle='current')
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    df = pd.read_excel(file_path)
    driver.get("https://seller.ozon.ru/app/brand-products/all")
    time.sleep(1)
    driver.find_element("xpath","//button[@type='submit']").click()
    time.sleep(3)
    driver.find_element("xpath","//input[@name='autocomplete']").send_keys("9960839655")
    driver.find_element("xpath","//button[@type='submit']").click()
    time.sleep(30)
    lock.release()
    wait = WebDriverWait(driver, 5)
    i = 0
    for col_name in df.columns[4:]:
        for index, value in df[col_name].items():
            if str(value) != "nan" and pd.api.types.is_numeric_dtype(value) == False and str(value).startswith(
                    'http'):
                print(value)
                if str(value).startswith('https://www.ozon.ru/'):
                    match = re.search(r'-(\d+)(?=/\?asb=)', value)
                    if match:
                        art = match.group(1)
                    print(art)
                    element = wait.until(EC.presence_of_element_located(("xpath", "//input[@type='text']")))
                    driver.find_element("xpath", "//input[@type='text']").clear()
                    driver.find_element("xpath", "//input[@type='text']").send_keys(art)
                    time.sleep(1)
                    try:
                        driver.find_element("xpath", "//td[.=' Нет записей ']")
                        price = "НЕ НАШ БРЕНД"
                        print("Элементов не найдено")
                    except:
                        element = wait.until(EC.presence_of_element_located(("xpath", "//tbody/tr/td[6]")))
                        price = driver.find_element("xpath", "//tbody/tr/td[6]").text
                    prev_col_index = df.columns.get_loc(col_name) - 1
                    prev_col_name = df.columns[prev_col_index]
                    df.loc[index, prev_col_name] = price
                    df.to_excel(file_path, index=False)
    driver.quit()
def updateYandex(e, path, lock,X,Y,positions):
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir=C:/Users/Dimulka/AppData/Local/Google/Chrome/User Data")
    # options.add_argument(f'--profile-directory=Default')
    driver = uc.Chrome(options=options)
    driver.set_window_size(X, Y)
    driver.set_window_position(*positions, windowHandle='current')
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    df = pd.read_excel(file_path)
    # driver.get("https://passport.yandex.ru/auth")
    # driver.find_element("xpath","//button[@data-type='phone']").click()
    # driver.find_element("xpath","//input[@inputmode='tel']").send_keys("9960839655")
    # driver.find_element("xpath","//button[@id='passp:sign-in']").click()
    # time.sleep(20)
    # driver.find_element("xpath","//a[@aria-label='Имя nasibulin.dmitr, Логин nasibulin.dmitr, ']").click()
    time.sleep(10)
    # lock.release()
    for col_name in df.columns[5:]:
        for index, value in df[col_name].items():
            if str(value) != "nan" and pd.api.types.is_numeric_dtype(value) == False and str(value).startswith(
                    'http'):
                print(value)
                if str(value).startswith('https://market.yandex.ru/'):
                    try:
                        try:
                            driver.get(value)
                            Captcha(driver)
                            # try:
                            #     try:
                            price_element = driver.find_element("xpath","//span[@data-auto='snippet-price-old']")
                            price = price_element.text
                            # print("Не чищенный" + price)
                            # Use a regular expression to extract the price between 'без:' and '₽'
                            # match = re.search(r'без:\D*(\d+)\D*₽', str(price))
                            # if match:
                            #     price = int(match.group(1))
                            #     print("Чищенный"+str(price))
                            # else:
                            #     # price = driver.find_element("xpath","//span[@data-auto='snippet-price-old']").text
                            #     price = 0
                            main_span = driver.find_element("xpath","//div[@data-auto='main']//div[@data-walter-collection='price']//span[@data-auto='snippet-price-old']")

                            # Теперь используем JavaScript, чтобы получить только текст из основного span
                            main_span_text = driver.execute_script("return arguments[0].innerText;",main_span)
                            match = re.search(r'Вместо:\s*([^\₽]+)\s*₽', main_span_text)
                            if match:
                                price = match.group(1).strip()
                                print("Извлеченный текст: ", price)
                            else:
                                print("Текст не найден.")
                            # print(main_span_text)
                        except:
                            try:
                                main_span = driver.find_element("xpath",
                                                                "//div[@data-auto='main']//div[@data-walter-collection='price']//span[@data-auto='snippet-price-old']")

                                # Теперь используем JavaScript, чтобы получить только текст из основного span
                                main_span_text = driver.execute_script("return arguments[0].innerText;", main_span)
                            except:
                                price = "Нет в продаже"
                                print(price)
                    except:
                        price = 0
                        print("Price ne naiden")
                    prev_col_index = df.columns.get_loc(col_name) - 1
                    prev_col_name = df.columns[prev_col_index]
                    # print(price)
                    df.loc[index, prev_col_name] = price
                    df.to_excel("yaup.xlsx", index=False)
    driver.quit()

def updateWildberries(e, path, lock,X,Y,positions):
    # options = webdriver.ChromeOptions()
    # # options.add_argument("--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")
    # # options.add_argument(f'--profile-directory=Profile 1')
    # options.add_argument(rf"--load-extension=C:\Users\Dimulka\Downloads\Spp12")
    # driver = uc.Chrome(options=options)
    # lock.release()
    # driver.set_window_size(X, Y)
    # driver.set_window_position(*positions, windowHandle='current')
    # file_path = path.split("_")[0]
    # file_path = rf'{file_path}_{e + 1}.xlsx'
    # df = pd.read_excel(file_path)
    # print("UpdateWB rabotaet")
    # for col_name in df.columns[4:]:
    #     for index, value in df[col_name].items():
    #         if str(value) != "nan" and pd.api.types.is_numeric_dtype(value) == False and str(value).startswith('http'):
    #             driver.get(value)
    #             time.sleep(1)
    #             wait = WebDriverWait(driver, 15)
    #             try:
    #                 w8 = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='product-page__seller-wrap section-border hide-desktop']//span[@class='seller-info__name']")))
    #                 magazin = driver.find_element("xpath","//div[@class='product-page__seller-wrap section-border hide-desktop']//span[@class='seller-info__name']").text
    #                 print("norm")
    #             except:
    #                 try:
    #                     # w8 = wait.until(EC.presence_of_element_located(("xpath", "//a[@class='seller-info__name seller-info__name--link']")))
    #                     magazin = "unknown"
    #                 except:
    #                     continue
    #             try:
    #                 w8 = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='wbcon__check-prices']")))
    #                 element = driver.find_element("xpath","//div[@class='wbcon__check-prices']")
    #                 driver.execute_script("arguments[0].scrollIntoView(true);", element)
    #                 price = driver.find_element("xpath", "//div[@class='wbcon__check-prices']").click()
    #                 w8 = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='wbcon__check-prices-second wbcon__check-prices-cell']")))
    #                 price = driver.find_element("xpath","//div[@class='wbcon__check-prices-second wbcon__check-prices-cell']").text
    #             except:
    #                 price = "Нет в наличии"
    #             print(f"Цена   {price}Магазин   {magazin} Валуе {value}")
    #             price1 = re.sub(r"\D", "", price)
    #             # current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    #             # new_column_name = f'Цена за {current_date}'
    #             # # df[new_column_name] = current_date
    #             # df.loc[index, new_column_name] = price1
    #             prev_col_index = df.columns.get_loc(col_name) - 1
    #             prev_col_name = df.columns[prev_col_index]
    #             # df[new_column_name] = current_date
    #             df.loc[index, prev_col_name] = price1
    #             # result_file_path = os.path.join(result_directoryWB, "" + file)
    #             df.to_excel(file_path, index=False)
    # driver.quit()
    lock.release()
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    df = pd.read_excel(file_path)
    print("UpdateWB rabotaet")
    regex_pattern = r"https://www.wildberries.ru/catalog/(\d+)/detail.aspx"
    # Применяем регулярное выражение
    for col_name in df.columns[4:]:
        for index, value in df[col_name].items():
            if str(value) != "nan" and pd.api.types.is_numeric_dtype(value) == False and str(value).startswith('http'):
                match = re.search(regex_pattern, value)
                if match:
                    article = match.group(1)
                    response1 = requests.get('http://92.63.192.39:371/spp')
                    if response1.status_code == 200:
                        data = response1.json()
                        spp = int(data['spp'])
                        print(spp)
                        url = "https://card.wb.ru/cards/detail?appType=2&curr=rub&dest=-1257786&spp=" + str(
                            spp) + "&nm=" + article
                        print(url)
                        response = requests.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            try:
                                price = float(data['data']['products'][0]['extended']['basicPriceU']) / 100
                            except:
                                price = float(data['data']['products'][0]['priceU']) / 100
                        prev_col_index = df.columns.get_loc(col_name) - 1
                        prev_col_name = df.columns[prev_col_index]
                        # df[new_column_name] = current_date
                        df.loc[index, prev_col_name] = price
                        # result_file_path = os.path.join(result_directoryWB, "" + file)
                        df.to_excel(file_path, index=False)


def updateSberMega(e, path, lock,X,Y,positions):
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")
    # options.add_argument(f'--profile-directory=Profile 1')
    driver = uc.Chrome(options=options)
    driver.set_window_size(X, Y)
    driver.set_window_position(*positions, windowHandle='current')
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    df = pd.read_excel(file_path)
    # driver.get("https://megamarket.ru/login?returnUrl=%2Fpersonal%2Forder%2F")
    # time.sleep(1)
    # driver.find_element("xpath","//button[@class='auth-main__phone-login c-button c-button_theme_special-gray c-button_size_large c-button_fullwidth']").click()
    # time.sleep(1)
    # driver.find_element("xpath","//input[@type='text']").send_keys("9960839655")
    # time.sleep(1)
    # driver.find_element("xpath","//button[@type='submit']").click()
    # time.sleep(20)
    lock.release()
    print("UpdateSM rabotaet")
    for col_name in df.columns[4:]:
        for index, value in df[col_name].items():
            if str(value) != "nan" and pd.api.types.is_numeric_dtype(value) == False and str(value).startswith('http'):
                driver.get(value)
                time.sleep(5)
                wait = WebDriverWait(driver, 5)
                try:
                    w8 = wait.until(EC.presence_of_element_located(("xpath", "//span[@class='sales-block-offer-price__price-final']")))
                    price = driver.find_element("xpath", "//span[@class='sales-block-offer-price__price-final']").text.replace(" ₽","")
                    print(price)
                except:
                    price = "Нет в наличии"
                price1 = re.sub(r"\D", "", price)
                # _%H-%M-%S
                # current_date = datetime.datetime.now().strftime('%d-%m-%Y')
                # new_column_name = f'Цена за {current_date}'
                # # df[new_column_name] = current_date
                # df.loc[index, new_column_name] = price1
                prev_col_index = df.columns.get_loc(col_name) - 1
                prev_col_name = df.columns[prev_col_index]
                # df[new_column_name] = current_date
                df.loc[index, prev_col_name] = price1
                df.to_excel(file_path, index=False)
    driver.quit()

