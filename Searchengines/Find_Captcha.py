import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
def Captcha(driver,product,link):
    while True:
        try:
            driver.find_element(By.XPATH, "//input[@class='CheckboxCaptcha-Button']").click()
            time.sleep(5)
            wait = WebDriverWait(driver, 20)
            try:
                driver.find_element(By.XPATH, "//*[contains(text(),'Нажмите в таком порядке')]")
                time.sleep(60)
                # driver.close()
                # driver.quit()
                # driver = create_proxy_webdriver(1)
                # driver.execute_script("window.localStorage.clear();")  # Очистить Local Storage
                # driver.execute_script("window.sessionStorage.clear();")  # Очистить Session Storage
                # driver.get(link)
                moreProds = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-zone-name='snippetList']/div")))
            except:
                print("Капча закончилась")
                time.sleep(10)
                break
        except:
            print("Капчи нет")
            break