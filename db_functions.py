import mysql_connect

#возвращает vk id пользователя из нашей базы данных где step_script равен 0. Для инициации диалога.
def getOneUserId(step_script = 0, limit = 1):
    mysql = mysql_connect.getConnect()
    cursor = mysql.cursor()
    cursor.execute(f"SELECT `vk_id` FROM `vk_users` WHERE `step_script` = {step_script} LIMIT {limit}")
    print("db_functions.getOneUserId сформированный запрос: "+cursor._last_executed)
    mysql.close()
    vk_id = cursor.fetchone()
    vk_id = str(vk_id)
    vk_id = vk_id[1:-2]
    return vk_id

#проверяет есть ли юзер в нашей БД по переданному vk_id и возвращает step_script(int), если находит строку с таким id, иначе возвращает None
def findUserStepScript(vk_id):
    mysql = mysql_connect.getConnect()
    cursor = mysql.cursor()
    cursor.execute(f"SELECT step_script FROM `vk_users` WHERE `vk_id` = {vk_id} LIMIT 1")
    result = cursor.fetchone()
    mysql.close()
    if result != None:
        return result[0]
    else:
        return None

# увеличивет значение в step_count на единицу
def updateStepCount(vk_id):
    mysql = mysql_connect.getConnect()
    cursor = mysql.cursor()
    cursor.execute(f"UPDATE vk_users SET `step_script` = `step_script` + 1 WHERE `vk_id` = {vk_id}")
    mysql.commit()
    mysql.close()

def getFirstNameByVkId(vk_id):
    mysql = mysql_connect.getConnect()
    cursor = mysql.cursor()
    cursor.execute(f"SELECT first_name FROM `vk_users` WHERE `vk_id` = {vk_id}")
    result = cursor.fetchone()
    mysql.close()
    if result != None:
        return result[0]
    else:
        return None
    return vk_id

#удаляет пользователя вк из нашей бд
def delUserFormDb(vk_id):
    mysql = mysql_connect.getConnect()
    cursor = mysql.cursor()
    cursor.execute(f"DELETE FROM vk_users  WHERE `vk_id` = {vk_id}")
    mysql.commit()
    mysql.close()

#возвращает текст шага скрипта бота по его id
def getTextScript(script_id, step_id):
    mysql = mysql_connect.getConnect()
    cursor = mysql.cursor()
    cursor.execute(f"SELECT `text` FROM `scripts_for_bot` WHERE `script_id` = {script_id} AND `step_id` = {step_id}")
    result = cursor.fetchone()
    mysql.close()
    return result[0]

#определяет количество шагов скрипта(длину скрипта) по id скрипта
def getLenScriptsStep(script_id):
    mysql = mysql_connect.getConnect()
    cursor = mysql.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM `scripts_for_bot` WHERE `script_id` = {script_id}")
    result = cursor.fetchone()
    mysql.close()
    return result[0]