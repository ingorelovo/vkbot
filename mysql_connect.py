import pymysql

def getConnect():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='vk_bot',
        charset='utf8',
    )
    return(connection)