import re
import util
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

keywords = ['placa de vídeo', 'placa de video']


def pichau_items(result_path):
    store = 'Pichau'
    webpage = 'https://www.pichau.com.br/hardware/placa-de-video'

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get(webpage)

    cookie_bt = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="rcc-confirm-button"]')))
    cookie_bt.click()

    while(True):
        count = 1
        while(True):
            try:
                sleep(0.25)
                description = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="__next"]/main/div[2]/div/div[1]/div[2]/div[{count}]/a/div/div[2]/h2'))).get_attribute('innerHTML').lower()
                price_area = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="__next"]/main/div[2]/div/div[1]/div[2]/div[{count}]/a/div/div[2]/div/div[1]/div'))).get_attribute('innerHTML')
                link = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="__next"]/main/div[2]/div/div[1]/div[2]/div[{count}]/a'))).get_attribute('href')

                price = re.findall(r'[1-9]\d{0,2}(?:\.\d{3})*,\d{2}', price_area)
                price = price[1] if len(price) > 1 else price[0]

                util.write_csv_file(result_path, [description, link, store, price])

                print([description, link, store, price], '\n')

                count += 1
            except:
                break
        if count < 36:
            break
        try:
            next_bt = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="__next"]/main[1]/div[2]/div[1]/div[1]/nav[1]/ul[1]/li[9]/button[1]')))
            next_bt.click()
        except:
            break


def kabum_items(result_path):
    store = 'Kabum'
    webpage = 'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1&page_size=100&facet_filters=eyJwcmljZSI6eyJtaW4iOjMwNi4wMiwibWF4IjoyMDk5MH19&sort=most_searched'

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get(webpage)

    while(True):
        count = 1
        while(True):
            try:
                sleep(0.25)
                description = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, f'/html/body/div[2]/main/article/section/div[3]/div/main/div[{count}]/a/div/div[1]/h2/span'))).get_attribute('innerHTML').lower()
                price = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, f'/html/body/div[2]/main/article/section/div[3]/div/main/div[{count}]/a/div/div[2]/span[2]'))).get_attribute('innerHTML')
                link = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, f'/html/body/div[2]/main/article/section/div[3]/div/main/div[{count}]/a'))).get_attribute('href')

                if keywords[0] in description or keywords[1] in description:
                    # new_price = re.findall('\d.\d{3},\d{2}|d{2}.\d{3},\d{2}|\d{3},\d{2}', price)
                    new_price = re.findall(r'[1-9]\d{0,2}(?:\.\d{3})*,\d{2}', price)
                    new_price = price[1] if len(new_price) > 1 else new_price[0]
                    new_price = new_price.replace('&nbsp;', '')
                    util.write_csv_file(result_path, [description, link, store, new_price])
                    print([description, link, store, new_price], '\n')

                count += 1
            except:
                break

        if count < 100:
            break
        try:
            next_bt = WebDriverWait(driver, 1000).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="listingPagination"]/ul/li[7]/a')))
            next_bt.click()
        except:
            break


def terabyte_items(result_path):
    store = 'Terabyte'
    webpage = 'https://www.terabyteshop.com.br/hardware/placas-de-video'

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get(webpage)

    # load all items
    count = 0
    while(True):
        try:
            next_bt = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/departamento/div[3]/div[3]/div[5]/a')))
            driver.execute_script("arguments[0].click();", next_bt)
            count += 1
        except:
            break

    # main XPATH group
    count = 1
    while(True):
        try:
            sleep(0.25)
            description = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div[4]/departamento/div[3]/div[3]/div[3]/div[{count}]/div/div[1]/a[2]/h2'))).get_attribute('innerHTML').lower()
            price = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div[4]/departamento/div[3]/div[3]/div[3]/div[{count}]/div/div[2]/div[1]/div[2]/span'))).get_attribute('innerHTML')
            link = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, f'/html/body/div[4]/departamento/div[3]/div[3]/div[3]/div[{count}]/div/div[1]/a[2]'))).get_attribute('href')

            util.write_csv_file(result_path, [description, link, store, price])
            print([description, link, store, price], '\n')

            count += 1
        except:
            break

    # Second XPATH group
    cdpmore_count = 2
    count = 1
    while(True):
        while(True):
            try:
                sleep(0.25)
                description = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="cpdmore{cdpmore_count}"]/div[{count}]/div/div[1]/a[2]/h2'))).get_attribute('innerHTML').lower()
                price = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="cpdmore{cdpmore_count}"]/div[{count}]/div/div[2]/div[1]/div[2]/span'))).get_attribute('innerHTML')
                link = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="cpdmore{cdpmore_count}"]/div[{count}]/div/div[1]/a[2]'))).get_attribute('href')

                util.write_csv_file(result_path, [description, link, store, price])
                print([description, link, store, price], '\n')

                count += 1
            except:
                break

        cdpmore_count += 1
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="cpdmore{cdpmore_count}"]/div[{count}]/div/div[2]/div[1]/div[2]/span')))
        except:
            break


# if __name__ == '__main__':
#     pichau_items(r'C:\Users\dan_z\Documents\projects\WebScrapingVC2\files\pichauResult.csv')
