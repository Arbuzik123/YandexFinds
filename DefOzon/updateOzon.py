import pandas as pd
from selenium import webdriver
import re
import time
import undetected_chromedriver as uc
from DefOzon.Find_Captcha import Captcha

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



