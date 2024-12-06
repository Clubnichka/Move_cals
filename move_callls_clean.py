import os
import sys
from bs4 import BeautifulSoup
import requests

wiki_login = os.getenv('WIKI_LOGIN')
wiki_pass = os.getenv('WIKI_PASS')
mango_login = os.getenv('MANGO_LOGIN')
mango_pass = os.getenv('MANGO_PASS')
mtm_bot_token = os.getenv('MTM_BOT_TOKEN')
mtm_channel = os.getenv('MTM_CHANNEL')

from atlassian import Confluence as Conf
from datetime import datetime
import re

#wiki
#инициализируем объект для доступа к викамS
c = Conf("https://wiki.wsoft.ru",
               'alebedev',
               '3gA7YpGA')

space_id = ''


#получаем пространство со статьей про график смотрящих за алармами\
page = c.get_page_by_title('TEST', 'График')

if not(page):
    print("Page not found.")


    # Проверяем наличие ключа 'body'

response = requests.get(
    f'https://wiki.wsoft.ru/rest/api/content/{page['id']}?expand=body.storage',
    auth=('alebedev', '3gA7YpGA')
)

if response.status_code == 200:
    page_data = response.json()
    
    # Проверяем наличие ключа 'body'
    if 'body' in page_data and 'storage' in page_data['body']:
        content = page_data['body']['storage']['value']
        
        # Использование BeautifulSoup для разбора HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Найдите заголовок "График"
       
            # Найдите родительский элемент заголовка (например, div или section)
        tables = soup.find_all('table')  # Предполагается, что таблица идет сразу после заголовка

        for index,table in enumerate(tables):
            if index==0:
                data_array = []
                rows = table.find_all('tr')
                    
                for row in rows[1:]:  # Пропускаем заголовок таблицы
                    cols = row.find_all('td')
                    if len(cols) == 3:  # Убедитесь, что есть три столбца
                        number = cols[0].get_text(strip=True)
                        login = cols[1].get_text(strip=True)
                        name = cols[2].get_text(strip=True)
                        data_array.append({'номер': number, 'имя': name, 'логин':login})
            elif index!=1:
                print("Таблица не найдена.")

            if index==1:
                today_day = int(datetime.now().strftime("%d"))
                rows=table.find_all('tr')
                for row in rows:
                    # Получаем ячейки в строке
                    cells = row.find_all(['td', 'th'])  # 'td' для данных, 'th' для заголовков
                    cell_data = [cell.get_text(strip=True) for cell in cells]
                    for num in cell_data:
                        if num!='':
                            if int(num.split(':')[0])==today_day:
                                current_person_id=int(num.split(':')[1])
            elif index!=0:
                print('Второй таблицы не найдено')
    else:
        print("Ключ 'body' отсутствует в ответе.")
else:
    print(f"Ошибка при получении страницы: {response.status_code} - {response.text}")

#---------------------------------------------------------------------------------------------Current_person_found---------------------------------------------------------------------------------------------



from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import requests
from datetime import datetime, timedelta

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome(options=options)

#открываем страницу манго
browser.get('https://crowd.wsoft.ru/crowd/console/login.action')
sleep(1)

#вводим логин и пароль
elem = browser.find_element(By.NAME, 'username')
elem.send_keys("alebedev")
elem = browser.find_element(By.NAME, 'password')
elem.send_keys("3gA7YpGA" + Keys.RETURN)
sleep(5)

browser.get('https://wiki.wsoft.ru/display/WSOFTWIKI/calendars')
sleep(5)



try:
    elem = browser.find_element(By.XPATH, '//*[@id="20241206"]/li/div[1]/div[3]/strong')
    event=elem.text
    sleep(5)
    
except:
    print("События нет")

try:
    event_array=event.split(" ")
    if event_array[0]=="отпуск":
        free_person=event_array[1]+" "+event_array[2]
        print(f"Сегодня в отпуске {free_person}")
except:
    print("")









for line in data_array:
    if int(line['номер'])==current_person_id:
        current_person=line['имя']
        current_person_login=line['логин']
        break




if current_person==free_person:
    current_person="Паша Цветков"

print(f"Сегодня дежурит - {current_person}")
#mango


sleep(1)


options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome(options=options)

#открываем страницу манго
browser.get('https://lk.mango-office.ru/')
sleep(10)
assert 'Личный кабинет' in browser.title

#вводим логин и пароль
elem = browser.find_element(By.NAME, 'login')
elem.send_keys("ptsvetkov@wsoft.ru")
elem = browser.find_element(By.NAME, 'password')
elem.send_keys("c)U7XGbr3UTD" + Keys.RETURN)
sleep(10)

#проверяем, есть ли плашка с сообщением о схеме работы в праздничные дни

#переходим на страницу с сотрудниками группы супорта
browser.get('https://lk.mango-office.ru/300007626/300011669/members/grouped/autoopen/228158')
sleep(10)

#переходим на вкладку с сотрудниками
elem = browser.find_element(By.XPATH, '//*[@id="app-modal"]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/button[2]/span')
elem.click()
sleep(10)
try:
    #меняем приоритет 1 на 2
    elem = browser.find_element(By.XPATH, '//*[@id="app-modal"]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div/div/input')
    elem.click()
    elem.clear()
    elem.send_keys('2')
    sleep(10)
except:
    print("Приоритет не изменён")
try:
    elem = browser.find_element(By.XPATH, f"//*[@id='app-modal']/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div/div[div[2]/span='" + current_person + "']/div[1]/div/div/div/div/input")
    elem.click()
    elem.clear()
    elem.send_keys('1')
except:
    print('Дежурство не изменено')
#нажимаем кнопку Сохранить

try:
    elem = browser.find_element(By.XPATH, "//*[@id='app-modal']/div/div/div[2]/div/div[2]/div/div[3]/div/div[1]/button")
    elem.click()
    sleep(10)
except:
    print('Данные не сохранены')

browser.quit()

#mtm
import mattermost


mm = mattermost.MMApi("https://mtm.wsoft.ru/api")

mm.login("alebedev@wsoft.ru","Koro1iShut")

channel_id = "1yt5wkhcgjb6pycue5o4jzxgny"


#пишем сообщение в канал
mm.create_post(channel_id, 'Сегодня за алармами следит @'+current_person_login)

