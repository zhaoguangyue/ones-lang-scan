# 根据path读取文件，转换为表结构
# -*- coding: UTF-8 -*-

import json
import glob
import utils
import os


def generateJsonData(path, sourceLang):
    fileList = glob.glob(path)
    langData = {}

    

    sourcePath = utils.getLangPath(fileList, sourceLang)
    sourceFileContent = utils.getJsonFileContent(sourcePath)
    utils.generateLangData(sourceFileContent, langData, sourceLang, True)

    for file_path in fileList: 
      lang = utils.getLang(file_path)
      if lang == sourceLang:
        continue

      fileContent = utils.getJsonFileContent(file_path)
      utils.generateLangData(fileContent, langData, lang)

    return langData.values()

  
# 读配置
configList = open('./config.json')
sheetDataList = {}
for config in json.load(configList):
  print(str(config))
  if config.get('fileType') == 'json':
    sheetDataList[config.get('sheetName')] = generateJsonData(config.get('path'), config.get('sourceLang'))
  elif config.get('fileType') == 'js':
    utils.generateConfig(config)
    os.system('./scripts/js_generateExcel.sh' + ' ' + config.get("scriptPath") )


utils.generateExcel(sheetDataList)

