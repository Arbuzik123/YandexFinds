import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Searchengines.AddVal import add_value_to_next_empty_cell_in_row
import undetected_chromedriver as uc
from Searchengines.Find_Captcha import Captcha
from Searchengines.ConverExtract import convert_symbols_in_brackets
import pandas as pd
import re
import os
import uuid
def SearchYandex(e, path, lock,X,Y,positions):
    def process_elementya(element,text,file_path):
        print("Подцикл")
        words = ['поршень', 'ремень', 'статор', 'шнек', 'трос', 'свеча', 'узел', 'регулятор', 'фильтр', 'реле',
                 'стартер', 'шатун', 'катушка', 'карбюратор', 'подушки', 'подшипник', 'щетка', 'кран', 'мешок', 'мешки',
                 'цепь', 'зарядное', 'шина', 'гайка', 'выключатель', 'рычаг', 'шаблон', 'мембрана', 'кожух','отвал','насадка','канат','головка','подушки']
        link = element.get_attribute("href")
        text = element.find_element(By.XPATH,".//span[@data-auto='snippet-title']").text
        text = convert_symbols_in_brackets(text)
        text = re.sub(r'[^\w\s]', '', text).replace(" ", "").lower()
        our_text = df.iloc[index, 3].replace(" ", "").lower()
        our_text = convert_symbols_in_brackets(our_text)
        our_text = re.sub(r'[^\w\s]', '', our_text)
        text = text.replace("brait","")
        our_text = our_text.replace("brait","")
        pattern = rf'{our_text}$|{our_text}(?![a-z])'
        print(text)
        print(our_text)
        print(link)
        matches = re.findall(pattern, text)
        if matches:
            print("Подходит")
            if not any(word in text for word in words):
                print(str(link))
                # print(index)
                add_value_to_next_empty_cell_in_row(df, index, str(link))
                df.to_excel(file_path, index=False)
                print("Успешно добавлено")

    custom_dir = "driver"

    # Создаем директорию, если она не существует
    os.makedirs(custom_dir, exist_ok=True)

    # Создаем патчер с указанием пользовательского пути для сохранения chromedriver
    unique_id = str(uuid.uuid4())

    # Задаем уникальный путь для сохранения chromedriver
    custom_dir = f"driver_{unique_id}"

    # Создаем директорию, если она не существует
    os.makedirs(custom_dir, exist_ok=True)

    # Создаем патчер с указанием пользовательского пути для сохранения chromedriver
    patcher = uc.Patcher(executable_path=os.path.join(custom_dir, 'chromedriver.exe'))
    patcher.auto()  # Автоматическая настройка патчера

    # Опции для Chrome
    unique_id = str(uuid.uuid4())

    # Задаем уникальный путь для сохранения chromedriver
    custom_dir = f"driver_{unique_id}"

    # Создаем директорию, если она не существует
    os.makedirs(custom_dir, exist_ok=True)

    # Создаем патчер с указанием пользовательского пути для сохранения chromedriver
    patcher = uc.Patcher(executable_path=os.path.join(custom_dir, 'chromedriver.exe'))
    patcher.auto()  # Автоматическая настройка патчера

    # Опции для Chrome
    options = webdriver.ChromeOptions()
    # Используем уникальные пользовательские данные и профиль для каждого процесса
    options.add_argument(f"--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data/{unique_id}")
    options.add_argument(f'--profile-directory=Profile_{unique_id}')

    # Создание экземпляра Chrome с патчером
    driver = uc.Chrome(options=options, patcher=patcher)
    driver.set_window_size(X, Y)
    driver.set_window_position(*positions, windowHandle='current')
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    df = pd.read_excel(file_path)
    print("Стартуем")
    time.sleep(1)
    driver.get("https://market.yandex.ru/")
    time.sleep(2)
    for index, row in df.iloc[:, 1].items():
        # try:
        product = "BRAIT " + str(df.iloc[index, 1]).split()[0] + " " + df.iloc[index, 3]
        Captcha(driver, product,None)
        links_to_get = []
        driver.find_element(By.XPATH, "//input[@type='search']").clear()
        driver.find_element(By.XPATH, "//input[@type='search']").send_keys(product)
        driver.find_element(By.XPATH,"//button[@data-auto='search-button']").click()
        time.sleep(10)
        Captcha(driver,product,None)
        page_height = driver.execute_script("return Math.max(document.body.scrollHeiВght, "
                                            "document.body.offsetHeight, document.documentElement.clientHeight, "
                                            "document.documentElement.scrollHeight, "
                                            "document.documentElement.offsetHeight);")
        driver.execute_script("window.scrollTo(0, arguments[0]);", page_height)
        wait = WebDriverWait(driver, 5)
        # try:
        elementyas = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-baobab-name='title']//div[@data-cs-name='navigate']/a[@data-auto='snippet-link' or @tabindex='-1']")))
        elementyas = driver.find_elements(By.XPATH, "//div[@data-baobab-name='title']//div[@data-cs-name='navigate']/a[@data-auto='snippet-link' or @tabindex='-1']")
        text = df.iloc[index,3]
        print('Элементы нашло')
        for elemente in elementyas:
            print("Цикл идет")
            process_elementya(elemente,text,file_path)
    de = pd.read_excel(file_path)
    driver.get(f"https://market.yandex.ru/")
    time.sleep(10)
    for index, row in de.iterrows():
        for column, value in row[4:].items():
            if pd.notna(value) and pd.notnull(value):
                print(value)
                try:
                    try:
                        match = re.search(r'/(\d+)\?hid', value)
                        article = match.group(1)
                    except:
                        try:
                            match = re.search(r'/(\d+)\?sponsored', value)
                            article = match.group(1)
                        except:
                            match = re.search(r'/(\d+)\?sku', value)
                            article = match.group(1)
                    print(article)
                    # "https://market.yandex.ru/product--/1780172787/offers?"1735591401
                    gettedlink = rf"https://market.yandex.ru/product--/{article}/offers?"
                    driver.get(gettedlink)
                    time.sleep(3)
                    Captcha(driver, row, gettedlink)
                    wait = WebDriverWait(driver, 20)
                    # try:
                    moreProds = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-zone-name='snippetList']/div")))
                    moreProds = driver.find_elements(By.XPATH, "//div[@data-zone-name='snippetList']/div")
                    for moreProd in moreProds:
                        # text_element = moreProd.find_element(By.XPATH, ".//h3[@data-zone-name='title']").text
                        link = moreProd.find_element(By.XPATH,".//h3[@data-zone-name='title']/a").get_attribute("href")
                        try:
                            price = moreProd.find_element(By.XPATH,".//div[@data-zone-name='price']/a/div/div/div[2]/span").text
                        except:
                            try:
                                price = moreProd.find_element(By.XPATH, ".//span[@data-auto='snippet-price-old']").text
                            except:
                                price = moreProd.find_element(By.XPATH,".//span[@data-auto='mainPrice']").text
                        # new_row = {'Наименование': text_element, 'Ссылка': link,
                        #            'Цена': price.replace("₽", "").replace(" ", "")}
                        new_data = {
                            'Наименование': df.iloc[index, 3],
                            'Store Name': moreProd.find_element(By.XPATH,".//div[@data-auto='top-offer-snippet-shop-info']/div//span/span/span").text,
                            'Price': str(str(price).replace("₽", "").replace(" ", "").replace("без:", "").replace(
                                "Вместо:", "").replace(" ", "")),
                            'Link': link
                        }
                        print("Цена:" + str(price).replace("₽", "").replace(" ", "").replace("без:", "").replace(
                                "Вместо:", "").replace(" ", "")+" Магазин: "+moreProd.find_element(By.XPATH,".//div[@data-auto='top-offer-snippet-shop-info']/div//span/span/span").text)
                        row_index = de.index[de['Наименование'] == new_data['Наименование']]
                        if len(row_index) > 0:
                            store_col = f"{' '.join(new_data['Store Name'].split()).title()}"
                            if store_col in de.columns:
                                de.loc[row_index, store_col] = str(new_data['Price'])
                                de.loc[row_index, f"{store_col} Link"] = new_data['Link']
                            else:
                                de[store_col] = np.nan
                                de.loc[row_index, store_col] = new_data['Price']
                                de.loc[row_index, f"{store_col} Link"] = new_data['Link']
                        else:
                            new_row = {
                                'Наименование': new_data['Наименование'],
                                'Store A': np.nan,
                                'Store B': np.nan,
                                'Store C': np.nan
                            }
                            store_col = f"{' '.join(new_data['Store Name'].split()).title()}"
                            new_row[store_col] = new_data['Price']
                            new_row[f"{store_col} Link"] = new_data['Link']
                            de = pd.concat([de, pd.DataFrame([new_row])], ignore_index=True)
                            # de.to_excel(file_path, index=False)
                            print("Добавлено")
                        de.to_excel("YandexComplete.xlsx", index=False, na_rep='')
                        de.to_excel(file_path, index=False)
                except:
                    print("Unlucky")
                # except:
                #     print("NoMoreProds")
                #     de.to_excel(file_path, index=False)