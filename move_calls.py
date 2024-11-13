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
# for space in c.get_all_spaces().get("results"):
#     if space.get('key') == 'TEST':
#         space_id = space.get('id')
# if space_id=='':
#     print("Нет такого пространства")
#     sys.exit()
if page:
    print(f"Page ID: {page['id']}")
    print(f"Page Title: {page['title']}")
else:
    print("Page not found.")

if page:
    # Выводим содержимое страницы для отладки
    print("Содержимое страницы:", page)

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
        table = soup.find('table')  # Предполагается, что таблица идет сразу после заголовка
            
        if table:
            data_array = []
            rows = table.find_all('tr')
                
            for row in rows[1:]:  # Пропускаем заголовок таблицы
                cols = row.find_all('td')
                if len(cols) == 2:  # Убедитесь, что есть два столбца
                    number = cols[0].get_text(strip=True)
                    name = cols[1].get_text(strip=True)
                    data_array.append({'номер': number, 'имя': name})
                
            print(data_array)
        else:
            print("Таблица не найдена.")

    else:
        print("Ключ 'body' отсутствует в ответе.")
else:
    print(f"Ошибка при получении страницы: {response.status_code} - {response.text}")

file=open("current_person.txt", 'r+')
current_person_id=int(file.read())
for line in data_array:
    if int(line['номер'])==current_person_id:
        current_person=line['имя']
        break
#current_person=data_array[current_person_id]
print(current_person)
file.close()
if current_person_id==3:
    current_person_id=0
file=open("current_person.txt", 'w')
file.write(f"{current_person_id+1}")
file.close()
#получаем содержимое статьи
#text = c.get_page_by_title(space_id, "График смотрящих за алармами в нерабочее время", expand="body.storage").get('body').get("storage").get("value")

#парсим содержимое для получения списка сотрудников и графика
# support_team = []
# is_first_table_reached = False
# is_second_table_reached = False
# current_day = 0
# current_month = ''
# current_person = ''

# months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
# today_month = months[int(datetime.now().strftime("%m")) - 1]
# today_day = int(datetime.now().strftime("%d"))

# for line in text.split('><'):
#     #обрабатываем таблицы
#     if line in ['tbody', '/tbody']:
#         if len(line) == 5:
#             #вычисляем, какую из таблиц мы достигли
#             if len(support_team) == 0:
#                 is_first_table_reached = True
#             else:
#                 is_second_table_reached = True
#         else:
#             is_first_table_reached = False

#     #обрабатываем таблицу с сотрудниками. Жирность после цвета. Имя внутри тега span
#     if is_first_table_reached:
#         if line[:2] == 'sp':
#             r = re.search('rgb\((.+)\);">(.+)</span', line)
#             person = {}
#             person[r.group(1)] = r.group(2)
#             support_team.append(person)

#     #обрабатываем таблицу с календаремю Сначала жирный, потом цветной. Дата внутри тега strong
#     if is_second_table_reached:
#         #ищем месяц
#         if line[:2] == 'td':
#             r = re.search('>(.+)<', line)
#             if r is not None:
#                 current_month = r.group(1)
#         #определяем цвет ячейки по тегу span
#         if line[:2] == 'sp':
#             r = re.search('rgb\((.+)\);"', line)
#             current_person = r.group(1)
#         #определяем день по тегу strong
#         if line[:2] == 'st':
#             r = re.search('>(.+)<', line)
#             #если нашли нужный день и месяц, опередяем сотрудника
#             if r is not None and int(r.group(1)) == today_day and current_month == today_month:
#                 for person in support_team:
#                     if person.get(current_person) is not None:
#                         current_person = person.get(current_person)
#                         break
#                 break



# mango
# from time import sleep
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver

# sleep(15)

# #options = webdriver.FirefoxOptions()
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-ssl-errors=yes')
# options.add_argument('--ignore-certificate-errors')
# browser = webdriver.Chrome(options=options)

# #открываем страницу манго
# browser.get('https://lk.mango-office.ru/')
# sleep(10)
# assert 'Личный кабинет' in browser.title

# #вводим логин и пароль
# elem = browser.find_element(By.NAME, 'login')
# elem.send_keys(mango_login)
# elem = browser.find_element(By.NAME, 'password')
# elem.send_keys(mango_pass + Keys.RETURN)
# sleep(15)

# #проверяем, есть ли плашка с сообщением о схеме работы в праздничные дни
# #elem = browser.find_element(By.XPATH, '/html/body/div[14]/div/div/div[3]/button[2]')
# #if elem is not None:
# #    elem.click()
# #    sleep(3)

# #переходим на страницу с сотрудниками группы супорта
# browser.get('https://lk.mango-office.ru/300007626/300011669/members/grouped/autoopen/228158')
# sleep(15)

# #переходим на вкладку с сотрудниками
# elem = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[1]/div[2]')
# elem.click()
# sleep(10)

# #меняем приоритет 1 на 2
# elem = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/div/input[@value=1]')
# elem.click()
# elem.clear()
# elem.send_keys('2')
# sleep(3)

# #ищем сотрудника из вик и меняем ему приоритет на 1
# #elem = browser.find_element(By.XPATH, f"/html/body/div[5]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[div[2]/span='{current_person}']/div[1]/div/div/input")
# #elem = browser.find_element(By.XPATH, f"/html/body/div[5]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[div[2][span='{current_person}']]/div[1]/div/div/input")
# #elem = browser.find_element(By.XPATH, f"/html/body/div[5]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[div[2][span[text()=`{current_person}`]]]/div[1]/div/div/input")
# elem = browser.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[div[2]/span='" + current_person + "']/div[1]/div/div/input")
# elem.click()
# elem.clear()
# elem.send_keys('1')

# #нажимаем кнопку Сохранить
# elem = browser.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div[3]/div[1]/button")
# elem.click()
# sleep(3)

# browser.quit()

#mtm
import mattermost

#заходим в MTM
mm = mattermost.MMApi("https://mtm.wsoft.ru/api")
#support-informer
mm.login("alebedev@wsoft.ru","Koro1iShut")

#получаем id пользователя и команды
# user_id = mm.get_user().get('id')
# team_id = next(mm.get_teams()).get('id')

#ищем id канала, в который будем писать
channel_id = "1yt5wkhcgjb6pycue5o4jzxgny"
# channel_id = ''
# for channel in mm.get_channels_for_user(user_id, team_id):
#     if channel.get("display_name") == "Support tea":
#         channel_id = channel.get("id")

#пишем сообщение в канал
mm.create_post(channel_id, 'Сегодня за алармами следит @'+current_person)

