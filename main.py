import lxml
import csv
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path=r'C:\Users\79611\Desktop\Mekka\emex_parser\chromedriver.exe')
original_window = driver.current_window_handle

try:
    driver.get('https://emex.ru/maintenance2')
    ps_mark = driver.page_source
    soup_mark = BeautifulSoup(ps_mark, 'lxml')
    mark_text = soup_mark.find(class_="sqj9idy").find_all(class_="iirmwcx")
    for t in mark_text:
        text_mark = t.text
        with open('emex.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([text_mark])
        if text_mark == 'ЗАЗ':
            driver.get(url='https://emex.ru/maintenance2/zaz')
        elif text_mark == 'ТагАЗ':
            driver.get(url='https://emex.ru/maintenance2/tagaz')
        elif text_mark == 'ford usa':
            driver.get(url='https://emex.ru/maintenance2/ford-usa')
        elif text_mark == 'Land Rover':
            driver.get(url='https://emex.ru/maintenance2/land-rover')
        else:
            driver.get(url=f'https://emex.ru/maintenance2/{text_mark}')
        
        models = driver.find_elements(By.CLASS_NAME, 'clolzkm')
        for model in models:
            model.click()
            time.sleep(1)
            ps_model = driver.page_source
            soup_model = BeautifulSoup(ps_model, 'lxml')
            models_url = soup_model.find_all('a', class_="s1peesfo")
            for te in models_url:
                time.sleep(1)
                model_url = 'https://emex.ru' + te.get('href')
                model_text = te.text
                with open('emex.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([model_text])
                driver.switch_to.new_window('tab')
                driver.get(url=model_url)
                time.sleep(1)
                
                ps_mod = driver.page_source
                soup_mod = BeautifulSoup(ps_mod, 'lxml')
                soup_prod = BeautifulSoup(ps_mod, 'lxml')
                prod_url = soup_prod.find(class_="djy8dqu").find_all('a')
                title_url = soup_mod.find_all(class_="r1u7yq88")
                for t in title_url:
                    title = t.text
                    with open('emex.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([title])
                        writer.writerow(('Наименование', 'Артикул', 'шт'))
                    for p in prod_url:
                        name = re.match(r'\D+', p.text).group(0)
                        pcs = re.search(r'\d', p.text).group(0)
                        href = p.get('href').split('/')[2]
                        with open('emex.csv', 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow((name, href, pcs))
                driver.close()
                driver.switch_to.window(original_window)
                time.sleep(1)
except Exception as ex:
    pass
finally:
    driver.close()
    driver.quit()