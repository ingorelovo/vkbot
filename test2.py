#import config
import time
import functions
import db_functions

#driver = config.driver
message = db_functions.getTextScript(1, "1")
print(message)
