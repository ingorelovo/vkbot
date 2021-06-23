import config
import time
import functions
import selenium

driver = config.driver

try:
    functions.auth('79254896933', 'LDdsdsl2rs', driver)
    functions.openUnreadDialog(driver)
    time.sleep(1)
    functions.dialogDel(driver)
except selenium.common.exceptions.ElementClickInterceptedException: #когда вылазиет модалка с прозьбой подтвердить e-mail - перезапускаем
    functions.auth('79254896933', 'LDdsdsl2rs', driver)
    functions.openUnreadDialog(driver)
    time.sleep(1)
    functions.dialogDel(driver)

#driver.quit(); закрытие браузера