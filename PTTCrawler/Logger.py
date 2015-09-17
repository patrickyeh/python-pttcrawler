'''
Created on Jul 5, 2012

@author: PatrickYeh
'''
import logging,os,datetime,stat
logging.getLogger("requests").setLevel(logging.WARNING)
def getLogger(loggerName = 'PttCrawler'):
    log=logging.getLogger(loggerName)
    strLogPath = os.path.join('Logs','%d-%d-%d.log'%(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.today().day))
    if not os.path.exists(os.path.dirname(strLogPath)):
        os.mkdir(os.path.dirname(strLogPath))
    objFileHandler = logging.FileHandler(strLogPath)
    objFileHandler.setLevel(logging.INFO)
    objStreamHandler = logging.StreamHandler()
    objStreamHandler.setLevel(logging.INFO)
    objFormat = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    objStreamHandler.setFormatter(objFormat)
    objFileHandler.setFormatter(objFormat)
    log.addHandler(objFileHandler)
    log.addHandler(objStreamHandler)
    log.setLevel(logging.DEBUG)
    try:
        os.chmod(strLogPath, 0777)
    except:
        pass
    return log