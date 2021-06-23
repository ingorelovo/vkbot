from selenium.webdriver.common.keys import Keys
import config
import random
import time
import pymysql
import mysql_connect
import selenium
import db_functions
from selenium.webdriver.common.action_chains import ActionChains

#авторизируемся в вк
def auth(login, pswrd, driver):
    driver.get('https://vk.com')
    user_name = driver.find_element_by_id("index_email")
    humanInput(login, user_name)
    password = driver.find_element_by_id("index_pass")
    humanInput(pswrd, password)
    driver.find_element_by_id('index_login_button').click()
    time.sleep(5)
    checkCaptcha(driver)

#проверяем, не получили ли мы модалку False - модалки нет | True - модалка есть
def checkModal(driver):
    print("Проверяем, не получили ли мы модалку")
    try:
        popup = driver.find_element_by_class_name("PushNotifierPopup__popup-box_type--suggest")
    except selenium.common.exceptions.NoSuchElementException:
        print("Никаких блядских модалок не вылезло, все хорошо")
        return False
    else:
        print("Вылезла блядская модалка")
        return True

#проверяем, не получили ли мы каптчу:
def checkCaptcha(driver):
    print("Проверяем не попросили ли каптчу...")
    try:
        capthca = driver.find_element_by_class_name("box_title").text
        print("Обнаружен запрос на ввод каптчи, ожидаем ввод...")
        time.sleep(5)
        checkCaptcha(driver)
    except selenium.common.exceptions.NoSuchElementException:
        print("Каптча не была запрошена, все хорошо")

#закрыть блядскую модалку
def modalClose(driver):
    driver.find_element_by_class_name("PushNotifierPopup__close-button").click()
    print("Блядская модалка закрыта")

#иммитация человеческого ввода текста.
def humanInput(text, inputfield, ot=0.14, do=0.21):
    count = 0
    while count < len(text):
        inputfield.send_keys(text[count])
        rand_sleep = random.uniform(ot,do)
        time.sleep(rand_sleep)
        count +=1

# парсим данные с группы
def parser(driver, limit=10000, query_url = config.query_url):
    driver.get(query_url)
    checkCaptcha(driver)
    #получим количество юзеров в выборке, преобразуем данные в число
    print("получим количество юзеров в выборке, преобразуем данные в число")
    count_accounts = driver.find_element_by_class_name("page_block_header_count").text
    count_accounts = list(count_accounts)
    count = 0
    while count < len(count_accounts):
        if count_accounts[count] == ' ':
            count_accounts.pop(count)
        count += 1
    count_accounts = ''.join(count_accounts)
    count_accounts = int(count_accounts)
    print("Количество объектов для парсинга: ", count_accounts)
    print("Ограничение на количество объектов: ", limit)

    #проскролим всю выборку аяксом до конца, что бы получить id всех юзеров
    print("начинаем проскроливать список подписчиков...")
    count_objects = len(driver.find_elements_by_xpath('//div[@class="people_row search_row clear_fix"]'))
    while count_objects <= limit and count_objects != count_accounts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        count_objects = len(driver.find_elements_by_xpath('//div[@class="people_row search_row clear_fix"]'))
        print("Количество юзеров на странице: ", count_objects)
    print("Закончили скроллинг... Количество юзеров на странице: ", count_objects)

    print("Начинаем записывать юзеров в БД...")
    mysql = mysql_connect.getConnect()  # открываем соединение с БД
    cursor = mysql.cursor()  # инициализируем курсор
    count = 1
    while count < limit and count < count_accounts:
        # для формирования xpath запроса одной строкой. между str1 и str3 будет переменная count
        str1 = '//div[@class="people_row search_row clear_fix"]['
        str3 = ']'
        count = str(count)
        xpatch_id = str1 + count + str3
        vk_id = driver.find_element_by_xpath(xpatch_id).get_attribute("data-id")
        print("vk_id: ", vk_id)
        str4 = '// *[ @ id = "results"] / div['
        str5 = '] / div[3] / div / a'
        xpatch_name = str4 + count + str5
        name = driver.find_element_by_xpath(xpatch_name).text
        first_name = getFirstName(name)
        last_name = getLastName(name)
        print("name: ", name)
        print("порядковый номер объекта парсинга: ", count)
        count = int(count)

        sql = "INSERT INTO `vk_users` (`vk_id`, `first_name`, `last_name`, `query_link`) VALUES (%s, %s, %s, %s);"
        try:
            cursor.execute(sql, (
                vk_id,
                first_name,
                last_name,
                query_url
            ))
        except pymysql.err.IntegrityError:
            count += 1
            print("Этот пользователь уже был записанн раннее, прпоускаем.")
            continue
        count += 1
        mysql.commit()

    mysql.close()  # ЗАКРЫВАЕМ соединение с БД
    print("Запись юзеров в БД окончена")

#обрежим фамилию, вернем имя
def getFirstName(text):
    result = ''
    for i in text:
        if i != ' ':
            result += i
        else:
            break
    return result

#обрежим имя, вернем фамилию
def getLastName(text):
    result = ""
    probelFlag = 0
    for i in text:
        if i == ' ':
            probelFlag = 1
            continue
        if i != ' ' and probelFlag == 0:
            continue
        if i != ' ' and probelFlag == 1:
            result += i
            continue
    return result

#отправляем пользователю сообщение через кнопку "написать сообщение". Нужно уже находиться на странице его профиля.
#Обычно используется для инициации общения(пишим ему первым).
def sendMessage(message, vk_id, driver):
    driver.get('https://vk.com/id'+vk_id)
    try:
        driver.find_element_by_class_name("profile_btn_cut_left").click()
        time.sleep(1)
        input_field = driver.find_element_by_id("mail_box_editable")
        humanInput(message, input_field)
        driver.find_element_by_id("mail_box_send").click()
    except:
        print("Юзер недоступен, удаляем его из БД")
        db_functions.delUserFormDb(vk_id)

#отправляем пользователю сообщение в текущий открытый диалог
def sendMessageInOpenDialog(message, driver):
    time.sleep(1)
    input_field = driver.find_element_by_id("im_editable0")
    humanInput(message, input_field)
    send_btn = driver.find_element_by_class_name("im-send-btn_send")
    driver.execute_script("arguments[0].click();", send_btn)

#получаем текст скрипта
def getTextByScript(step, scriptname):
    step = str(step)
    f = open(config.core_patch+'/textscripts/'+scriptname+'/step'+step+'.txt', 'r')
    text = f.read()
    f.close()
    return text

#перейдем в список непрочитанных личных сообщений и кликнем по самому первому из них
def openUnreadDialog(driver):
    driver.get('https://vk.com/im?tab=unread')
    driver.find_element_by_class_name("nim-dialog_unread").click()

# возьмем id первого непрочитанного диалога
def getVkFromUnreadDialog(driver):
    driver.get('https://vk.com/im?tab=unread')  # перейдем в диалоги
    vk_id = driver.find_element_by_class_name("nim-dialog_unread").get_attribute("data-peer")  # возьмем id первого непрочитанного диалога
    return vk_id

#удаляем активный(текущий открытый) диалог, если это беседа, а не л.с
def dialogDel(driver):
    dialog_href = driver.find_element_by_class_name("im-page--title-main-inner").get_attribute("href")
    print(dialog_href)
    for i in dialog_href:
        print(i)
        if i == "?":
            driver.find_element_by_css_selector("._im_dialog_selected .nim-dialog--close").click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="box_layer"]/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/button').click()

#Чекает счетчик непрочитанные диалогов вк. Пустая строка - непрочитанных диалогов нет, иначе - вернет кло-во не прочитанных диалогов.
def checkNewMessages(driver):
    count_messages = driver.find_element_by_css_selector('#l_msg .left_count').text
    return count_messages

#Получаем id пользователя вк c которым есть диалог (первый из не прочитанных)
def getVkIdFromDialog(driver):
    vk_id = driver.find_element_by_class_name("nim-dialog_unread").get_attribute("data-peer")
    print("vk_id собеседника: "+ vk_id)
    return vk_id

#удаляет первый непрочитанный диалог, который найдет или же по vk_id, если передан
def delUndreadDialog(driver, vk_id = ""):
    #script = 'document.styleSheets[0].insertRule("[dir=ltr] .nim-dialog .nim-dialog--close { display:block !important;}", 0 )'
    #driver.execute_script(script)
    if vk_id == "":
        # наведем фокус на первый не прочитанный диалог, что бы выскачил крестик, по которому можно будет удалить диалог
        hover = ActionChains(driver).move_to_element(driver.find_element_by_css_selector(".nim-dialog_unread"))
        hover.perform()
        #закроем диалог
        driver.find_element_by_css_selector(".nim-dialog_unread .nim-dialog--close").click()
    else:
        # наведем фокус на нужный не прочитанный диалог, что бы выскачил крестик, по которому можно будет удалить диалог
        hover = ActionChains(driver).move_to_element(driver.find_element_by_css_selector(f"._im_dialog_{vk_id}"))
        hover.perform()
        #закроем диалог
        driver.find_element_by_css_selector(f"._im_dialog_{vk_id} .nim-dialog--close").click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="box_layer"]/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/button').click()
    time.sleep(2)

#открывает первый из списка не прочитанный диалог или же диалог по vk_id собеседника
def selectUnreadDialog(driver, vk_id = ""):
    if vk_id == "" :
        driver.find_element_by_class_name("nim-dialog_unread").click()
    else:
        driver.find_element_by_class_name(f"_im_dialog_{vk_id}").click()

#удаляет текущий открытый диалог
def deleteSelectedDialog(driver):
    driver.find_element_by_css_selector("._im_dialog_selected _im_dialog_close").click()
    driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/button").click()

#проверка после целевого действия (не привысили ли мы лимит сообщений и т.д)
# 0 - все ок
# 1 - привышен лимит сообщений отправляемых не френд.листу. (скорее всего уникальных диалогов). Разблокировка через сутки
def checkEror(driver):
    msg_limit = driver.find_element_by_id("system_msg").text()
    if msg_limit == "Сообщение не может быть отправлено, так как Вы разослали слишком много сообщений за последнее время. #74348159":
        print("привышен лимит сообщений отправляемых не френд.листу. (скорее всего уникальных диалогов). Разблокировка через сутки")
        return 1
    else:
        return 0
