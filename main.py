#region IMPORTS
#web crawling/download
from bs4 import BeautifulSoup
import requests

#zip extraction
from zipfile import ZipFile

#folder utilities
import shutil
import os

#markdown
import html_generator

#log
from logger import log


#endregion

#region CONSTANTS
LATEST_ZIP = "https://github.com/sayterdarkwynd/FrackinUniverse/archive/master.zip"
LATEST_PAGE = "https://github.com/sayterdarkwynd/FrackinUniverse/releases/latest"

FU_PATH     = 'FrackinUniverse-master'
FU_VERSION  = "fu_version.txt"
FU_ZIP      = 'fu.zip'

SUPPORTED_TYPES = [
    'recipe'    ,
    'json'      ,
    'liqitem'   ,
    'matitem'   ,
    'item'      ,
    'activeitem',
    'head'      ,
    'chest'     ,
    'legs'      ,
    'material'  ,
]

IGNORED_TYPES = [
    'gitignore',
    'png',
    'metadata',
    '_previewimage'
]
#endregion

data = {}

def main():
    checkFrackinUniverseUpdate()
    #getting all files
    files = []
    for root, dirs, files in os.walk(FU_PATH):
        print('DIR:',dirs)
        for file in map(lambda file: os.path.join(root, file),files):
            fileType = supported(file)
            if fileType:
                log('\n----------------------')
                log("Reading:", file)
                fileContent = html_generator.loadJsonData(file)
                if('itemName' in fileContent):
                    itemName = fileContent['itemName']
                    if itemName not in data:
                        data[itemName] = fileContent
                    else:
                        raise NotImplementedError()
                else:
                    log("NO ITEM NAME FOUND:",file)
                
                
                """
                markdown_generator_function = getattr(data_generator, "parse_"+fileType, None);
                if markdown_generator_function is not None:
                    log("Parser found for type:", fileType)
                    #creating markdown
                    md = markdown_generator_function(file)[0]

                    #creating html
                    html = markdown2.markdown(md)

                    #creating output folder
                    htmlFileName = file.replace(FU_PATH,'wiki').replace('.'+fileType,'.html')
                    os.makedirs(htmlFileName.rsplit('\\',1)[0] , exist_ok=True)

                    #creating output file
                    with open(htmlFileName,'w') as htmlFile:
                        htmlFile.write(html)
                else:
                    log("PARSER MISSING FOR:",fileType)
                """
            elif not ignored(file):
                log("CAN'T READ!!!", file)
                pass

    log("END!")

def checkFrackinUniverseUpdate():
    #region read FU stored version
    log("LOCAL FU VERSION: ",end='')
    storedFUVer = ""
    try:
        storedFUVer = open(FU_VERSION).read()
        log(storedFUVer)
    except:
        log("Not found")
    #endregion

    #region read FU online version
    log("ONLINE FU VERSION: ",end='')
    soup = BeautifulSoup(requests.get(LATEST_PAGE).text, "lxml")
    onlineFUVer = soup.select_one('.release-header a').text
    log(onlineFUVer)
    #endregion

    # IF stored != online
    if storedFUVer != onlineFUVer:
        log("Version mismatch, updating.")
        updateFU(onlineFUVer)
        log('Done, current version:', onlineFUVer)
    else:
        log("Same version, all fine.")

def updateFU(onlineFUVer:str):
    #deleting old FU
    log("Deleting old FU")
    shutil.rmtree(FU_PATH, ignore_errors=True)
    os.unlink(FU_ZIP)

    #downloading FU master zip
    log('Downloading FU latest commit...')
    with open(FU_ZIP, 'wb') as fuZip:
        fuZip.write(requests.get(LATEST_ZIP).content)

    #unzipping
    log('Unzipping...')
    with ZipFile(FU_ZIP, 'r') as zip_ref:
        zip_ref.extractall('./')
    
    #saving new version
    fuVersionFile = open(FU_VERSION, 'w')
    fuVersionFile.write(onlineFUVer)
    fuVersionFile.close()

def supported(fileName:str):
    return _fileHasSuffix(fileName, SUPPORTED_TYPES)

def ignored(fileName:str):
    return _fileHasSuffix(fileName, IGNORED_TYPES)

def _fileHasSuffix(fileName, suffixes):
    for end in suffixes:
        if fileName.endswith('.'+end):
            return end
    
    return False

main()