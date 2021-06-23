from selenium import webdriver
import mysql_connect
from datetime import timedelta, datetime
import os

driver = webdriver.Chrome('chromedriver86')
core_patch = "C:/soft/vkbot"

#url страницы подписчиков сообщества с уже выбранными фильтрами
query_url = 'https://vk.com/search?c%5Bgroup%5D=87172323&c%5Bname%5D=1&c%5Bonline%5D=1&c%5Bper_page%5D=40&c%5Bphoto%5D=1&c%5Bsection%5D=people&c%5Bsex%5D=2&c%5Bsort%5D=1'

base_path = os.path.dirname(os.path.abspath(__file__)) #абсолютный путь до корневой папки проекта
logger_base_path = base_path+'\logger'  # местоположение лог-файлов
SCRIPT_STEPS_LIMIT = 5   #количество исходящих от бота сообщений в скрипте. Счет с 0.

#настройки времени
today = datetime.today()
today = today.date()  # текущая дата
old_data = "2019-01-24"
default_time = " 00:01:00"

month_ago = today - timedelta(days=30)
yesterday = today - timedelta(days=1)

todayStr = str(today)
yesterdayStr = str(yesterday)
month_ago_str = str(month_ago)

today_datetime = todayStr + default_time
yesterday_datetime = yesterdayStr + default_time
month_ago_datetime = month_ago_str + default_time
old_datetime = old_data + default_time