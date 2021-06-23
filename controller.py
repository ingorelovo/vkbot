import config
import functions
import db_functions
import time
from logger import logger

driver = config.driver
functions.auth('79254896933', 'LDdsdsl2rs', driver)
#инициация общения с новым пользователем (пишим ему первым)
def createDialog(driver):
    vk_id = db_functions.getOneUserId()
    print("Получили id юзера из БД: "+vk_id)
    step_script = db_functions.findUserStepScript(vk_id)
    first_name = db_functions.getFirstNameByVkId(vk_id)
    if step_script == 0:
        functions.sendMessage(f"{first_name}, приветулии)", vk_id, driver)
        db_functions.updateStepCount(vk_id)
    elif step_script == config.SCRIPT_STEPS_LIMIT:
        functions.deleteSelectedDialog(driver, vk_id)
    else:
        step_script = db_functions.findUserStepScript(vk_id) #теперь получим заного новый этап скрипта
        message = functions.getTextByScript(step_script, "script1")
        functions.sendMessage(message, vk_id, driver)
        db_functions.updateStepCount(vk_id)

#отвечаем пользователю, если он ответил нам на первое сообщение
def replToUser(driver):
    count_messages = functions.checkNewMessages(driver)
    if count_messages != "":
        vk_id_from_dialog = functions.getVkFromUnreadDialog(driver)
        step_script = db_functions.findUserStepScript(vk_id_from_dialog)
        #logger.writeError(f"controller.replToUser step_script: {step_script}")
        print(f"controller.replToUser step_script: {step_script}")
        if step_script != None:
            message = db_functions.getTextScript(1, step_script)
            print(f"Получили сообщение из бд для юзера: {message}")
            functions.selectUnreadDialog(driver, vk_id_from_dialog)
            send_mes = functions.sendMessageInOpenDialog(message, driver)
            if send_mes == 0:
                db_functions.updateStepCount(vk_id)
                print("Отправили сообщение, сдвинули счетчик")
            else:
                print("Сообщение почему то не отправилось.")
        else:
            functions.delUndreadDialog(driver, vk_id_from_dialog)

count = 0
while count !=1:
    replToUser(driver)
    time.sleep(2)
    createDialog(driver)


