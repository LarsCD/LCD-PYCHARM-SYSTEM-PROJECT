'''
/////////////////////////////////////////////////////////////////////
SLIMg 1.5

Save and Load Internal Module - Game (SLIMg)
Program to save and load data for games

/////////////////////////////////////////////////////////////////////
Documentation:

1) SLIMg.init()
    Use .init() at beginning of your application to initiate
    SLIMg, it will create a 'system' folder and a 'log.txt'file
    within the 'system' folder


2) SLIMg.saveData(data, dirName='dirName', fileName='fileName')
    Use .saveData() to save data to a file, it takes one 
    possitional argument and two keyword arguments. The one
    possitional argument is used for the data input. The two
    keyword arguments can be used to specify the folder or 
    filename, the default will be the 'system' folder and 
    'save' file. 


3) SLIMg.loadData(dirName='dirName', fileName='fileName')
    Use .loadData() to load data from a file, it takes two
    keyword arguments for the folder and file name. The default 
    will be the 'system' folder and 'save' file. 


4) Logging capabilities
    In the SLIMg.py file (this file) the logEnabled variable will
    allow the program to log  The 'log.txt' file will be stored in 
    the 'system' folder.


Created by LCD.
/////////////////////////////////////////////////////////////////////
'''

import pickle
import os
from os import listdir
from os.path import isfile, join
import sys
from pathlib import Path
import traceback
import datetime



# //// VARIABLES ////

thisDir = os.getcwd()
print(f'thisDir = {thisDir}')
saveDirName = 'system'
saveFileName = 'save'
logFileName = 'log.txt'
logEnabled = True



# //// FILE MANAGEMENT OPERATIONS ////

class fileManager:

    saveInit = None

    def init():
        # log.log('i', 'init saveFile:')
        try:
            if fileManager.checkPath(saveDirName) == True:
                if fileManager.checkFile(saveDirName, saveFileName) == False:
                    fileManager.createFile(saveDirName, saveFileName)
                else:
                    log.log('s', 'save file exists')
            else:
                fileManager.createDir(saveDirName)
                fileManager.init()
        except Exception as e:
            eMessage = str(type(e).__name__)
            log.log('e', 'saveFile init unsuccesful: ' + str(eMessage))
        else:
            log.log('i', 'saveFile init succesful')


    def checkPath(dirName):
        # check if path exists
        dirExists = None
        if os.path.isdir(dirName):
            dirExists = True
        else:
            dirExists = False
        log.log('s', 'Checking dir: \'' + str(dirName) + '\', dir exists=' + str(dirExists))
        return dirExists


    def checkFile(dir, name):
        # check if file exists
        fileExists = None
        dir_ = os.path.join(thisDir, dir)
        path = os.path.join(dir_, name)
        if isfile(path):
            fileExists = True
        else:
            fileExists = False
        log.log('s', 'Checking file: \'' + str(name) + '\', file exists=' + str(fileExists))
        return fileExists


    def createDir(name):
        log.log('o', 'Creating dir: \'' + str(name) + '\'...')
        # create dir
        path = os.path.join(thisDir, name)
        try:
            os.mkdir(path)
        except FileExistsError:
            log.log('e', 'Cannot create dir: \'' + str(name) + '\' already exists')
        else:
            log.log('s', 'Succsesfully created dir: \'' + str(name) + '\'')


    def createFile(dirName, name):
        # create save file (in save dir)
        log.log('o', 'Creating save file: \'' + str(name) + '\'')
        try:
            dir = os.path.join(thisDir, dirName)
            path = os.path.join(dir, name)
            file = open(path, 'a+').close()
        except Exception as e:
            eMessage = str(type(e).__name__)
            log.log('e', 'Creating file \'' + str(name) + '\' unsuccesful: ' + str(eMessage))
        else:
            log.log('s', 'Creating file \'' + str(name) + '\' succesful')



# //// LOG OPERATION ////

class log:

    logType = {
            's': 'SYSTEM ',
            'e': 'ERROR  ',
            'r': 'REQUEST',
            'c': 'REQ_SCS',
            'u': 'REQ_ERR',
            't': 'START  ',
            'o': 'OPPERAT',
            'i': 'INIT   ',
            'n': '',
    }

    def clear():
        dir = os.path.join(thisDir, saveDirName)
        path = os.path.join(dir, logFileName)
        clear = open(path, 'w')

    def log(type, message):
        if logEnabled == True:
            if type == 'n':
                text = log.logType[str(type)]
            else:
                time = str(datetime.datetime.now())
                log_type = str(log.logType[str(type)])
                text = str('> ' + log_type + ' - [' + time + ']: ' + str(message))
            try: 
                log.write(text)
            except:
                pass
            print(text)
        else:
            pass

    def write(message):
        dir = os.path.join(thisDir, saveDirName)
        path = os.path.join(dir, logFileName)
        logFile = open(path, 'a')
        logFile.write(str(message + '\n'))
        logFile.close()



# //// MODULE OPERATION ////

class SLIMg:

    def init():
        try:
            fileManager.init()
            log.clear()
            log.log('t', 'SLIMg start')
            log.log('n', '')
            log.log('i', 'Init SLIMg...')
        except Exception as e:
            eMessage = str(type(e).__name__)
            log.log('u', f'SLIMg init unsuccesful: {str(eMessage)}')
        else:
            log.log('i', 'SLIMg init succesful')


    def saveData(data, dirName=saveDirName, fileName=saveFileName):
        dataSize = sys.getsizeof(data)
        log.log('n', '')
        log.log('r', f'Saving data ({str(dataSize)}b) to file \'{str(dirName)}\\{str(fileName)}\'')
        dirExists = fileManager.checkPath(dirName)
        if not dirExists:
            fileManager.createDir(dirName)
        fileExists = fileManager.checkFile(dirName, fileName)
        if not fileExists:
            fileManager.createFile(dirName, fileName)

        # save data to save file
        dir = os.path.join(thisDir, dirName)
        path = os.path.join(dir, fileName)
        try:
            with open(path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            eMessage = str(type(e).__name__)
            log.log('u', f'Could not save data ({str(dataSize)}b) to file \'{str(dirName)}\\{str(fileName)}\': {str(eMessage)}')
            print(e)
            try:
                f.close()
            except:
                pass
            return 0
        else:
            log.log('c', f'Data succesfully saved ({str(dataSize)}b)')
            f.close()
            return 1
    

    def loadData(dirName=saveDirName, fileName=saveFileName): 
        log.log('n', '')
        log.log('r', f'Loading data from file \'{str(dirName)}\\{str(fileName)}\'')
        # load data from save file
        dir = os.path.join(thisDir, dirName)
        path = os.path.join(dir, fileName)
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
        except Exception as e:
            eMessage = str(type(e).__name__)
            log.log('u', f'Could not load data from file \'{str(dirName)}\\{str(fileName)}\': {str(eMessage)}')
            print(e)
            try:
                f.close()
            except:
                pass
            return 0
        else:
            dataSize = sys.getsizeof(data)
            log.log('c', f'Data succesfully loaded ({str(dataSize)}b)')
            f.close()
            return data



# //// TEST CODE EXECUTION ////

def main():
    x = 'Hello World'

    SLIMg.init()
    SLIMg.saveData(x, fileName='save1')
    SLIMg.loadData(fileName='save1')
    
    
    click = input('press [_] to exit')

if __name__ == '__main__':
    main()
