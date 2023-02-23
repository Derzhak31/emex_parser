import lxml
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path=r'"C:\Users\79611\Desktop\Mekka\emex\emex_parser\chromedriver.exe"')
original_window = driver.current_window_handle

try:
    with open('emex.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(('Категория', 'Запись', 'Модификация', 'Наименование', 'Артикул', 'ШТ'))
    driver.get('https://emex.ru/maintenance2')
    ps_mark = driver.page_source
    soup_mark = BeautifulSoup(ps_mark, 'lxml')
    text_mark = soup_mark.find(class_="sqj9idy").find_all(class_="iirmwcx")
    for t in text_mark:
        mark_text = t.text
        if mark_text == 'ЗАЗ':
            driver.get(url='https://emex.ru/maintenance2/zaz')
        elif mark_text == 'ТагАЗ':
            driver.get(url='https://emex.ru/maintenance2/tagaz')
        elif mark_text == 'ford usa':
            driver.get(url='https://emex.ru/maintenance2/ford-usa')
        elif mark_text == 'Land Rover':
            driver.get(url='https://emex.ru/maintenance2/land-rover')
        else:
            driver.get(url=f'https://emex.ru/maintenance2/{mark_text}')
        
        models = driver.find_elements(By.CLASS_NAME, 'clolzkm')
        for model in models:
            model.click()
            ps_model = driver.page_source
            soup_model = BeautifulSoup(ps_model, 'lxml')
            models_url = soup_model.find_all('a', class_="s1peesfo")
            for te in models_url:
                model_url = 'https://emex.ru' + te.get('href')
                text1 = te.find(class_="cwnvyck").text
                text2 = te.find(class_="cdq4n3s").text
                model_text = mark_text + ' ' + text1 + ' ' + text2
                driver.switch_to.new_window('tab')
                driver.get(url=model_url)
                ps_mod = driver.page_source
                soup_mod = BeautifulSoup(ps_mod, 'lxml')
                soup_prod = BeautifulSoup(ps_mod, 'lxml')
                # prod_url = soup_prod.find_all(class_="djy8dqu")
                title_url = soup_mod.find_all(class_="w1xdm79g")
                product = ''
                for t in title_url:
                    title1 = t.find(class_="cs27n20")
                    title2 = title1.find_next(class_="cs27n20")
                    title3 = title2.find_next(class_="cs27n20")
                    title4 = title3.find_next(class_="cs27n20")
                    title5 = title4.find_next(class_="cs27n20")
                    title6 = title5.find_next(class_="cs27n20")
                    product = product + '<h2>' + title1.text + ' ' + title2.text + ' ' + title3.text + ' ' + title4.text + ' ' + title5.text + ' ' + title6.text + '</h2>'
                    prod_url = t.find(class_="djy8dqu").find_all('a')
                    prod_text = ''
                    for a in prod_url:
                        name_text = '<td>' + a.find(style="--c76iom0-0:flex;--c76iom0-1:flex-start;--c76iom0-2:#000000;--c76iom0-4:none;--c76iom0-5:flex-end").text + '</td>'
                        pcs_text = '<td>' + a.find(style="--c76iom0-0:flex;--c76iom0-1:flex-start;--c76iom0-2:#000000;--c76iom0-4:none;--c76iom0-5:flex-end").find_next().text + '</td>'
                        href_text = '<td>' + a.get('href').split('/')[2] + '</td>'
                        prod = '<tr>' + name_text + pcs_text + href_text + '</tr>'
                        prod_text = prod_text + prod
                    product = product + '<table>' + prod_text + '</table>'
                data = [mark_text, model_text, product]
                with open('emex.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)
                driver.close()
                driver.switch_to.window(original_window)
                time.sleep(1)
except Exception as ex:
    pass
finally:
    driver.close()
    driver.quit()