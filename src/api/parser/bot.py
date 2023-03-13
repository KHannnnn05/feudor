from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from time import sleep


class ParseBot():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.url = 'https://nsso.ru/check_policy/gop/tsnumber/'
        self.base_url = 'https://nsso.ru'
        self.driver = webdriver.Chrome(options=chrome_options)
        self.data = {}

    def parse(self, car_number):
        self.driver.get(self.url)
        '''Заполнение данных об авто'''
        input_number = self.driver.find_element(By.ID, 'sDocNo_TS')
        input_number.click()
        input_number.send_keys(str(car_number))
        '''Снимаем флажок, для вывода всех данных'''
        self.driver.find_element(By.ID, 'show_contracts_by_date') \
            .click()
        '''Нажимаем на кнопку'''
        self.driver.find_element(By.CLASS_NAME, 'form_content') \
                    .find_element(By.CLASS_NAME, 'check') \
                    .click()
        sleep(5)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table = soup.find('table', class_='check_result_table') \
                    .find('div', class_='Block') \
                    .findAll('div', class_='result_message_sub')

        if table is None:
            return None

        for i, info in enumerate(table):
            inshur_number = (re.findall(r'№: \S{18}', info.text.strip()))[0].replace('№: ', '')
            if (re.findall(r'Наименование страховщика: \w* "\S*"', info.text.strip())):
                inshur_company = (
                    re.findall(r'Наименование страховщика: \w* "\S*"', info.text.strip()))[0].replace('Наименование страховщика:', '')
            elif (re.findall(r'Наименование страховщика: \w* "\S* \S*"', info.text.strip())):
                inshur_company = (
                    re.findall(r'Наименование страховщика: \w* "\S* \S*"', info.text.strip()))[0].replace('Наименование страховщика: ', '')
            elif (re.findall(r'Наименование страховщика: \w* \w* "\S*"', info.text.strip())):
                inshur_company = (
                    re.findall(r'Наименование страховщика: \w* \w* "\S*"',info.text.strip()))[0].replace('Наименование страховщика: ', '')
            inshur_start_data = (
                re.findall(r'Дата начала ответственности: \S{10}', info.text.strip()))[0].replace('Дата начала ответственности: ', '')
            inshur_close_data = (
                re.findall(r'Дата окончания ответственности: \S{10}',info.text.strip()))[0].replace('Дата окончания ответственности: ','')
            inshur_doc_url = self.base_url + info.find('a').get('href')

            self.data.update({i: {
                'contract_number': inshur_number, 
                'inshur_company': inshur_company, 
                'inshur_start_data': inshur_start_data,
                'inshur_close_data': inshur_close_data, 
                'pdf_document_link': inshur_doc_url
                }})

        return self.data
