# -- coding: utf-8 --
# author : Alexxander Lugovskoy
# vk.com/delta85

import config
from datetime import datetime
import os

#message - сообщение, которое нужно записать в лог
#src - путь до лог.файла(включая имя файла), в который будем записывать
def writeError(message, src= config.logger_base_path + "\main_debug" + f"\{config.todayStr}_main_debug.log"):
    f = open(src, 'a', encoding="utf-8")
    f.write("["+str(datetime.now())+"] "+message + "\n")
    f.close()

#print(os.path.abspath("./") + "\main_debug" + f"\{config.todayStr}_main_debug.log")
#writeError('loh')
