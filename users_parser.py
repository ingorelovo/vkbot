import config
import time
import functions

driver = config.driver
functions.auth('79612750550', 'Klizmach2', driver)
functions.parser(driver, limit=100)

